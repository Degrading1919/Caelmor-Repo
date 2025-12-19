using System;
using System.Threading;
using Caelmor.Runtime;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Replication;

namespace Caelmor.Runtime.Transport
{
    public interface IOutboundTransportSender
    {
        /// <summary>
        /// Attempts to send a serialized snapshot. Ownership transfers to the sender on success;
        /// the sender is responsible for disposing the snapshot when delivery completes.
        /// </summary>
        bool TrySend(SessionId sessionId, SerializedSnapshot snapshot);
    }

    /// <summary>
    /// Transport-thread send pump that drains serialized replication snapshots without touching the tick thread.
    /// Deterministically iterates active sessions and dispatches bounded batches per iteration to avoid unbounded work.
    /// </summary>
    public sealed class OutboundSendPump : IDisposable
    {
        private readonly PooledTransportRouter _transport;
        private readonly IOutboundTransportSender _sender;
        private readonly IActiveSessionIndex _sessions;
        private readonly ReplicationSnapshotCounters? _counters;
        private readonly int _maxPerSession;
        private readonly int _maxPerIteration;
        private readonly int _idleDelayMs;
        private readonly RuntimePipelineHealth? _pipelineHealth;
        private readonly Func<long>? _tickProvider;
        private readonly object _gate = new object();

        private Thread? _thread;
        private CancellationTokenSource? _cts;
        private bool _running;

        public OutboundSendPump(
            PooledTransportRouter transport,
            IOutboundTransportSender sender,
            IActiveSessionIndex sessions,
            RuntimeBackpressureConfig config,
            ReplicationSnapshotCounters? counters = null,
            int maxPerIteration = 0,
            int idleDelayMs = 1,
            RuntimePipelineHealth pipelineHealth = null,
            Func<long> tickProvider = null)
        {
            _transport = transport ?? throw new ArgumentNullException(nameof(transport));
            _sender = sender ?? throw new ArgumentNullException(nameof(sender));
            _sessions = sessions ?? throw new ArgumentNullException(nameof(sessions));
            _counters = counters;
            _pipelineHealth = pipelineHealth;
            _tickProvider = tickProvider;

            if (config == null) throw new ArgumentNullException(nameof(config));
            _maxPerSession = Math.Max(1, config.MaxOutboundSnapshotsPerSession);
            _maxPerIteration = maxPerIteration > 0 ? maxPerIteration : _maxPerSession * 4;
            _idleDelayMs = idleDelayMs < 0 ? 0 : idleDelayMs;

            if (_pipelineHealth != null && _tickProvider == null)
                throw new ArgumentNullException(nameof(tickProvider));
        }

        public void Start()
        {
            lock (_gate)
            {
                if (_running)
                    return;

                _cts = new CancellationTokenSource();
                _thread = new Thread(() => Run(_cts.Token))
                {
                    IsBackground = true,
                    Name = "Caelmor.OutboundSendPump"
                };

                _running = true;
                _thread.Start();
            }
        }

        public void Stop()
        {
            CancellationTokenSource? cts;
            Thread? thread;

            lock (_gate)
            {
                if (!_running)
                    return;

                _running = false;
                cts = _cts;
                thread = _thread;
                _cts = null;
                _thread = null;
            }

            try { cts?.Cancel(); } catch { /* no-op */ }

            if (thread != null && Thread.CurrentThread != thread)
            {
                try { thread.Join(); } catch { /* no-op */ }
            }
        }

        public int PumpOnce(int maxSnapshots = 0)
        {
            var limit = maxSnapshots > 0 ? maxSnapshots : _maxPerIteration;
            if (limit <= 0)
                return 0;

            if (_pipelineHealth != null)
                _pipelineHealth.MarkOutboundSend(_tickProvider!.Invoke());

            var sessions = _sessions.SnapshotSessionsDeterministic();
            int dispatched = 0;

            for (int i = 0; i < sessions.Count && dispatched < limit; i++)
            {
                var sessionId = sessions[i];
                int perSession = 0;

                while (perSession < _maxPerSession && dispatched < limit && _transport.TryDequeueOutbound(sessionId, out var snapshot))
                {
                    _counters?.RecordSnapshotDequeuedForSend();
                    bool sent = false;

                    try
                    {
                        sent = _sender.TrySend(sessionId, snapshot);
                    }
                    catch
                    {
                        sent = false;
                    }

                    if (!sent)
                    {
                        _counters?.RecordSnapshotDropped();
                        snapshot.Dispose();
                    }

                    perSession++;
                    dispatched++;
                }
            }

            return dispatched;
        }

        public void Dispose()
        {
            Stop();
        }

        private void Run(CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {
                PumpOnce(_maxPerIteration);

                if (_idleDelayMs > 0)
                    Thread.Sleep(_idleDelayMs);
                else
                    Thread.Yield();
            }
        }
    }
}
