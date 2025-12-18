using System;
using System.Collections.Generic;
using Caelmor.Runtime;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Transport;
using Caelmor.Runtime.WorldSimulation;

namespace Caelmor.Runtime.Persistence
{
    /// <summary>
    /// Thread-safe persistence completion mailbox. Persistence workers enqueue completion results
    /// off-thread; the tick thread drains and applies them deterministically during a tick phase hook.
    /// Overflow drops oldest completions and disposes pooled payloads to keep memory bounded.
    /// </summary>
    public sealed class PersistenceCompletionQueue : IDisposable
    {
        private readonly object _gate = new object();
        private readonly Queue<PersistenceCompletion> _queue;
        private readonly int _maxCompletions;
        private readonly int _maxBytes;
        private readonly PersistencePipelineCounters? _counters;
        private CompletionQueueMetrics _metrics;

        public PersistenceCompletionQueue(RuntimeBackpressureConfig config, PersistencePipelineCounters counters = null)
        {
            if (config is null) throw new ArgumentNullException(nameof(config));
            _maxCompletions = config.MaxPersistenceCompletions;
            _maxBytes = config.MaxPersistenceCompletionBytes;
            _queue = new Queue<PersistenceCompletion>(_maxCompletions);
            _counters = counters;
        }

        /// <summary>
        /// Off-thread enqueue. Deterministic drop-oldest policy keeps the mailbox bounded.
        /// </summary>
        public bool TryEnqueue(PersistenceCompletion completion)
        {
            int payloadBytes = completion.PayloadLength;
            if (payloadBytes > _maxBytes)
            {
                RegisterDrop(payloadBytes);
                completion.Dispose();
                return false;
            }

            lock (_gate)
            {
                EnforceCapsLocked(payloadBytes);

                _queue.Enqueue(completion);
                _metrics.Current = _queue.Count;
                _metrics.CurrentBytes += payloadBytes;
                if (_metrics.Peak < _metrics.Current)
                    _metrics.Peak = _metrics.Current;
                _counters?.RecordCompletionBacklog(_metrics.Current, _metrics.CurrentBytes);
                return true;
            }
        }

        /// <summary>
        /// Tick-thread-only drain. Applies completions deterministically and returns pooled payloads.
        /// </summary>
        public int Drain(IPersistenceCompletionApplier applier, long tickIndex)
        {
            if (applier is null) throw new ArgumentNullException(nameof(applier));

            TickThreadAssert.AssertTickThread();

            int drained = 0;
            lock (_gate)
            {
                while (_queue.Count > 0)
                {
                    var completion = _queue.Dequeue();
                    _metrics.CurrentBytes = Math.Max(0, _metrics.CurrentBytes - completion.PayloadLength);

                    drained++;
                    applier.Apply(in completion, tickIndex);
                    completion.Dispose();
                }

                _metrics.Current = 0;
                _metrics.CurrentBytes = 0;
            }

            return drained;
        }

        public CompletionQueueMetrics SnapshotMetrics()
        {
            lock (_gate)
            {
                return _metrics;
            }
        }

        public void Clear()
        {
            lock (_gate)
            {
                while (_queue.Count > 0)
                {
                    var completion = _queue.Dequeue();
                    completion.Dispose();
                }

                _metrics = default;
            }
        }

        public void Dispose()
        {
            Clear();
        }

        private void EnforceCapsLocked(int incomingBytes)
        {
            while (_queue.Count > 0 &&
                   (_queue.Count >= _maxCompletions || _metrics.CurrentBytes + incomingBytes > _maxBytes))
            {
                var dropped = _queue.Dequeue();
                var droppedBytes = dropped.PayloadLength;
                _metrics.CurrentBytes = Math.Max(0, _metrics.CurrentBytes - droppedBytes);
                RegisterDrop(droppedBytes);
                dropped.Dispose();
            }
        }

        private void RegisterDrop(int payloadBytes)
        {
            _metrics.Dropped++;
            _metrics.DroppedBytes += payloadBytes;
            _counters?.RecordDrop();
        }
    }

    /// <summary>
    /// Completion DTO returned by persistence workers. Payload is pooled and disposed after apply.
    /// </summary>
    public readonly struct PersistenceCompletion : IDisposable
    {
        public PersistenceCompletion(
            PersistenceWriteRequest request,
            PersistenceCompletionStatus status,
            PooledPayloadLease payload,
            PersistenceFailureReason failureReason)
        {
            Request = request;
            Status = status;
            Payload = payload;
            FailureReason = failureReason;
        }

        public PersistenceWriteRequest Request { get; }
        public PersistenceCompletionStatus Status { get; }
        public PooledPayloadLease Payload { get; }
        public PersistenceFailureReason FailureReason { get; }
        public int PayloadLength => Payload?.Length ?? 0;

        public void Dispose()
        {
            Payload?.Dispose();
        }
    }

    /// <summary>
    /// Tick-thread applier invoked from a deterministic tick phase hook.
    /// Implementations must not block or allocate in hot paths.
    /// </summary>
    public interface IPersistenceCompletionApplier
    {
        void Apply(in PersistenceCompletion completion, long tickIndex);
    }

    /// <summary>
    /// Phase hook that drains completions during pre-tick and applies them on the tick thread.
    /// </summary>
    public sealed class PersistenceCompletionPhaseHook : ITickPhaseHook
    {
        private readonly PersistenceCompletionQueue _queue;
        private readonly IPersistenceCompletionApplier _applier;

        public PersistenceCompletionPhaseHook(PersistenceCompletionQueue queue, IPersistenceCompletionApplier applier)
        {
            _queue = queue ?? throw new ArgumentNullException(nameof(queue));
            _applier = applier ?? throw new ArgumentNullException(nameof(applier));
        }

        public void OnPreTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            _queue.Drain(_applier, context.TickIndex);
        }

        public void OnPostTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
        }
    }

    public enum PersistenceCompletionStatus
    {
        Succeeded = 1,
        Failed = 2
    }

    public enum PersistenceFailureReason
    {
        None = 0,
        IoError = 1,
        ValidationFailed = 2,
        Unknown = 3
    }

    public struct CompletionQueueMetrics
    {
        public int Current { get; set; }
        public int Peak { get; set; }
        public int Dropped { get; set; }
        public int DroppedBytes { get; set; }
        public int CurrentBytes { get; set; }
    }
}
