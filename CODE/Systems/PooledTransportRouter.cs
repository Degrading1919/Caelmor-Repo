using System;
using System.Collections.Generic;
using Caelmor.ClientReplication;
using Caelmor.Runtime;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Onboarding;

namespace Caelmor.Runtime.Transport
{
    /// <summary>
    /// Transport-agnostic router that bridges transport threads and the deterministic tick thread.
    /// Inbound payloads are staged in bounded, pooled mailboxes and drained on the tick thread into
    /// <see cref="DeterministicTransportRouter"/>. Outbound snapshots are dequeued by transport threads
    /// and emitted without mutating gameplay state.
    /// </summary>
    public sealed class PooledTransportRouter : IDisposable
    {
        private readonly object _inboundGate = new object();
        private readonly object _snapshotGate = new object();

        private readonly RuntimeBackpressureConfig _config;
        private readonly DeterministicTransportRouter _deterministic;
        private readonly Dictionary<SessionId, Queue<InboundEnvelope>> _inboundQueues = new Dictionary<SessionId, Queue<InboundEnvelope>>(64);
        private readonly Dictionary<SessionId, int> _bytesBySession = new Dictionary<SessionId, int>(64);
        private readonly Dictionary<SessionId, SessionQueueMetrics> _metrics = new Dictionary<SessionId, SessionQueueMetrics>(64);
        private readonly List<SessionId> _sessionOrder = new List<SessionId>(64);

        public PooledTransportRouter(RuntimeBackpressureConfig config)
        {
            _config = config ?? throw new ArgumentNullException(nameof(config));
            _deterministic = new DeterministicTransportRouter(config);
        }

        /// <summary>
        /// Enqueues an inbound payload from a transport thread. Payload bytes are copied into a pooled
        /// lease to avoid lifetime hazards across threads.
        /// </summary>
        public bool EnqueueInbound(SessionId sessionId, ReadOnlySpan<byte> payload, string commandType, long submitTick)
        {
            var lease = PooledPayloadLease.Rent(payload);
            return EnqueueInbound(sessionId, lease, commandType, submitTick);
        }

        /// <summary>
        /// Enqueues an inbound payload using an existing pooled lease (no extra copy).
        /// Caller relinquishes ownership on success or rejection; this router will dispose on failure paths.
        /// </summary>
        public bool EnqueueInbound(SessionId sessionId, PooledPayloadLease payload, string commandType, long submitTick)
        {
            if (!sessionId.IsValid)
            {
                payload.Dispose();
                return false;
            }

            int payloadSize = payload.Length;

            lock (_inboundGate)
            {
                if (!_inboundQueues.TryGetValue(sessionId, out var queue))
                {
                    queue = new Queue<InboundEnvelope>();
                    _inboundQueues[sessionId] = queue;
                }

                _bytesBySession.TryGetValue(sessionId, out var currentBytes);
                if (!_metrics.TryGetValue(sessionId, out var metrics))
                    metrics = new SessionQueueMetrics();

                if (queue.Count >= _config.MaxInboundCommandsPerSession ||
                    currentBytes + payloadSize > _config.MaxQueuedBytesPerSession)
                {
                    metrics.Rejected++;
                    metrics.RejectedBytes += payloadSize;
                    metrics.Peak = Math.Max(metrics.Peak, queue.Count);
                    _metrics[sessionId] = metrics;
                    payload.Dispose();
                    return false;
                }

                queue.Enqueue(new InboundEnvelope(sessionId, commandType ?? string.Empty, submitTick, payload));
                _bytesBySession[sessionId] = currentBytes + payloadSize;

                metrics.Peak = Math.Max(metrics.Peak, queue.Count);
                metrics.Current = queue.Count;
                _metrics[sessionId] = metrics;
                return true;
            }
        }

        /// <summary>
        /// Drains inbound mailboxes in deterministic session order and routes payloads into the
        /// authoritative ingress. Must be invoked from the tick thread.
        /// </summary>
        public int RouteQueuedInbound()
        {
            TickThreadAssert.AssertTickThread();

            int processed = 0;
            lock (_inboundGate)
            {
                _sessionOrder.Clear();
                foreach (var kvp in _inboundQueues)
                    _sessionOrder.Add(kvp.Key);

                _sessionOrder.Sort(SessionIdComparer.Instance);

                for (int i = 0; i < _sessionOrder.Count; i++)
                {
                    var sessionId = _sessionOrder[i];
                    if (!_inboundQueues.TryGetValue(sessionId, out var queue) || queue.Count == 0)
                        continue;

                    while (queue.Count > 0)
                    {
                        var envelope = queue.Dequeue();
                        processed++;
                        _bytesBySession[sessionId] = Math.Max(0, _bytesBySession[sessionId] - envelope.Payload.Length);

                        var result = _deterministic.RouteInbound(envelope.SessionId, envelope.Payload, envelope.CommandType, envelope.SubmitTick);
                        if (!result.Ok)
                        {
                            RegisterDrop(sessionId, envelope.Payload.Length);
                            envelope.Payload.Dispose();
                        }
                    }

                    UpdateCurrentMetrics(sessionId, queue.Count);
                }
            }

            return processed;
        }

        /// <summary>
        /// Tick-thread only: enqueues a serialized snapshot for transport delivery.
        /// </summary>
        public void RouteSnapshot(ClientReplicationSnapshot snapshot)
        {
            if (snapshot == null) throw new ArgumentNullException(nameof(snapshot));

            TickThreadAssert.AssertTickThread();

            lock (_snapshotGate)
            {
                _deterministic.RouteSnapshot(snapshot);
            }
        }

        /// <summary>
        /// Transport thread dequeue for outbound snapshots. Disposes responsibility moves to caller.
        /// </summary>
        public bool TryDequeueOutbound(SessionId sessionId, out SerializedSnapshot snapshot)
        {
            lock (_snapshotGate)
            {
                return _deterministic.TryDequeueSnapshot(sessionId, out snapshot);
            }
        }

        public TransportBackpressureDiagnostics CaptureDiagnostics()
        {
            lock (_snapshotGate)
            {
                return _deterministic.CaptureDiagnostics();
            }
        }

        public void DropAllForSession(SessionId sessionId)
        {
            DropInboundForSession(sessionId);

            lock (_snapshotGate)
            {
                _deterministic.DropSession(sessionId);
            }
        }

        public void Clear()
        {
            lock (_inboundGate)
            {
                foreach (var kvp in _inboundQueues)
                {
                    var queue = kvp.Value;
                    while (queue.Count > 0)
                    {
                        var entry = queue.Dequeue();
                        RegisterDrop(entry.SessionId, entry.Payload.Length);
                        entry.Payload.Dispose();
                    }
                }

                _inboundQueues.Clear();
                _bytesBySession.Clear();
                _metrics.Clear();
                _sessionOrder.Clear();
            }

            lock (_snapshotGate)
            {
                _deterministic.Clear();
            }
        }

        public void Dispose()
        {
            Clear();
        }

        private void DropInboundForSession(SessionId sessionId)
        {
            lock (_inboundGate)
            {
                if (_inboundQueues.TryGetValue(sessionId, out var queue))
                {
                    while (queue.Count > 0)
                    {
                        var entry = queue.Dequeue();
                        RegisterDrop(sessionId, entry.Payload.Length);
                        entry.Payload.Dispose();
                    }

                    _inboundQueues.Remove(sessionId);
                }

                _bytesBySession.Remove(sessionId);

                if (_metrics.TryGetValue(sessionId, out var metrics))
                {
                    metrics.Current = 0;
                    _metrics[sessionId] = metrics;
                }
            }
        }

        private void UpdateCurrentMetrics(SessionId sessionId, int current)
        {
            if (_metrics.TryGetValue(sessionId, out var metrics))
            {
                metrics.Current = current;
                _metrics[sessionId] = metrics;
            }
        }

        private void RegisterDrop(SessionId sessionId, int payloadBytes)
        {
            if (!_metrics.TryGetValue(sessionId, out var metrics))
                metrics = new SessionQueueMetrics();

            metrics.Dropped++;
            metrics.DroppedBytes += payloadBytes;
            _metrics[sessionId] = metrics;
        }

        private readonly struct InboundEnvelope
        {
            public readonly SessionId SessionId;
            public readonly string CommandType;
            public readonly long SubmitTick;
            public readonly PooledPayloadLease Payload;

            public InboundEnvelope(SessionId sessionId, string commandType, long submitTick, PooledPayloadLease payload)
            {
                SessionId = sessionId;
                CommandType = commandType;
                SubmitTick = submitTick;
                Payload = payload;
            }
        }

        private sealed class SessionIdComparer : IComparer<SessionId>
        {
            public static SessionIdComparer Instance { get; } = new SessionIdComparer();

            public int Compare(SessionId x, SessionId y)
            {
                return x.Value.CompareTo(y.Value);
            }
        }
    }
}
