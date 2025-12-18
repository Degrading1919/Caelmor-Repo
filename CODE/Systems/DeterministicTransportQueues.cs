using System;
using System.Buffers;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using System.Threading;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Persistence;
using Caelmor.Runtime.Replication;
using EntityHandle = global::Caelmor.Runtime.Tick.EntityHandle;
using PlayerId = global::Caelmor.Runtime.Onboarding.PlayerId;
using RuntimeBackpressureConfig = global::Caelmor.Runtime.RuntimeBackpressureConfig;
using SessionId = global::Caelmor.Runtime.Onboarding.SessionId;

namespace Caelmor.Runtime.Transport
{
    /// <summary>
    /// Pooled payload lease with explicit ownership. The queue owns buffer lifetime and returns the
    /// underlying byte[] via Dispose; Dispose is idempotent to protect against accidental copies.
    /// </summary>
    public sealed class PooledPayloadLease : IDisposable
    {
        private const int MaxPooledLeases = 512;
        private static readonly Stack<PooledPayloadLease> LeasePool = new Stack<PooledPayloadLease>(MaxPooledLeases);
        private byte[] _buffer;
        private int _length;
        private int _disposed;

        private PooledPayloadLease() { }

        public byte[] Buffer => _buffer ?? Array.Empty<byte>();
        public int Length => _length;

        public static PooledPayloadLease Rent(ReadOnlySpan<byte> payload)
        {
            var lease = Acquire();
            var buffer = ArrayPool<byte>.Shared.Rent(payload.Length);
            payload.CopyTo(buffer.AsSpan(0, payload.Length));
            lease.Initialize(buffer, payload.Length);
            return lease;
        }

        private static PooledPayloadLease Acquire()
        {
            lock (LeasePool)
            {
                if (LeasePool.Count > 0)
                    return LeasePool.Pop();
            }

            return new PooledPayloadLease();
        }

        private void Initialize(byte[] buffer, int length)
        {
            _disposed = 0;
            _buffer = buffer ?? throw new ArgumentNullException(nameof(buffer));
            _length = length;
        }

        public void Dispose()
        {
            if (Interlocked.Exchange(ref _disposed, 1) == 1)
                return;

            var buffer = _buffer;
            _buffer = null;
            _length = 0;

            if (buffer != null)
                ArrayPool<byte>.Shared.Return(buffer, clearArray: true);

            lock (LeasePool)
            {
                if (LeasePool.Count < MaxPooledLeases)
                    LeasePool.Push(this);
            }
        }
    }

    /// <summary>
    /// Deterministic inbound command ingestion. Enforces per-session command and byte budgets
    /// and rejects overflow rather than blocking the tick thread.
    /// </summary>
    public sealed class AuthoritativeCommandIngress
    {
        private readonly RuntimeBackpressureConfig _config;
        private readonly Dictionary<SessionId, Queue<CommandEnvelope>> _queues = new Dictionary<SessionId, Queue<CommandEnvelope>>();
        private readonly Dictionary<SessionId, SessionQueueMetrics> _metrics = new Dictionary<SessionId, SessionQueueMetrics>();
        private readonly Dictionary<SessionId, int> _bytesBySession = new Dictionary<SessionId, int>();
        private SessionId[] _snapshotKeys = Array.Empty<SessionId>();
        private SessionQueueMetricsSnapshot[] _snapshotBuffer = Array.Empty<SessionQueueMetricsSnapshot>();
        private long _nextSequence;

        public AuthoritativeCommandIngress(RuntimeBackpressureConfig config)
        {
            _config = config ?? throw new ArgumentNullException(nameof(config));
        }

        public CommandIngressResult TryEnqueue(SessionId sessionId, ReadOnlySpan<byte> payload, string commandType, long submitTick)
        {
            var pooled = PooledPayloadLease.Rent(payload);
            return TryEnqueue(sessionId, pooled, commandType, submitTick);
        }

        public CommandIngressResult TryEnqueue(SessionId sessionId, PooledPayloadLease payload, string commandType, long submitTick)
        {
            return EnqueueInternal(sessionId, payload, commandType, submitTick);
        }

        public int DrainDeterministic(Span<CommandEnvelope> destination, int maxCommands)
        {
            if (maxCommands <= 0 || destination.Length == 0)
                return 0;

            int sessionCount = _queues.Count;
            if (sessionCount == 0)
                return 0;

            EnsureCapacity(ref _snapshotKeys, sessionCount);

            int index = 0;
            foreach (var kvp in _queues)
                _snapshotKeys[index++] = kvp.Key;

            Array.Sort(_snapshotKeys, 0, index, SessionIdValueComparer.Instance);

            int written = 0;
            while (written < destination.Length && written < maxCommands)
            {
                bool found = false;
                SessionId selectedSession = default;
                long bestSequence = long.MaxValue;

                for (int i = 0; i < index; i++)
                {
                    var sessionId = _snapshotKeys[i];
                    if (!_queues.TryGetValue(sessionId, out var queue) || queue.Count == 0)
                        continue;

                    var candidate = queue.Peek();
                    var sequence = candidate.DeterministicSequence;

                    if (!found || sequence < bestSequence ||
                        (sequence == bestSequence && SessionIdValueComparer.Instance.Compare(sessionId, selectedSession) < 0))
                    {
                        found = true;
                        bestSequence = sequence;
                        selectedSession = sessionId;
                    }
                }

                if (!found)
                    break;

                if (!TryDequeue(selectedSession, out var envelope))
                    break;

                destination[written++] = envelope;
            }

            return written;
        }

        private CommandIngressResult EnqueueInternal(SessionId sessionId, PooledPayloadLease payload, string commandType, long submitTick)
        {
            if (sessionId.Equals(default(SessionId)))
            {
                payload.Dispose();
                return CommandIngressResult.Rejected(CommandRejectionReason.InvalidSession);
            }

            int payloadSize = payload.Length;

            if (!_queues.TryGetValue(sessionId, out var queue))
            {
                queue = new Queue<CommandEnvelope>();
                _queues[sessionId] = queue;
            }

            if (!_metrics.TryGetValue(sessionId, out var metrics))
            {
                metrics = new SessionQueueMetrics();
            }

            _bytesBySession.TryGetValue(sessionId, out int currentBytes);

            if (queue.Count >= _config.MaxInboundCommandsPerSession || currentBytes + payloadSize > _config.MaxQueuedBytesPerSession)
            {
                metrics.Rejected++;
                metrics.RejectedBytes += payloadSize;
                metrics.Peak = Math.Max(metrics.Peak, queue.Count);
                metrics.CurrentBytes = currentBytes;
                metrics.PeakBytes = Math.Max(metrics.PeakBytes, currentBytes);
                _metrics[sessionId] = metrics;
                payload.Dispose();
                return CommandIngressResult.Rejected(CommandRejectionReason.BackpressureLimitHit);
            }

            long sequence = ++_nextSequence;
            var envelope = new CommandEnvelope(sessionId, submitTick, sequence, commandType ?? string.Empty, payload);
            queue.Enqueue(envelope);
            var updatedBytes = currentBytes + payloadSize;
            _bytesBySession[sessionId] = updatedBytes;

            metrics.Peak = Math.Max(metrics.Peak, queue.Count);
            metrics.Current = queue.Count;
            metrics.CurrentBytes = updatedBytes;
            metrics.PeakBytes = Math.Max(metrics.PeakBytes, updatedBytes);
            _metrics[sessionId] = metrics;

            return CommandIngressResult.Accepted(sequence);
        }

        public bool TryDequeue(SessionId sessionId, out CommandEnvelope envelope)
        {
            envelope = default;
            if (!_queues.TryGetValue(sessionId, out var queue) || queue.Count == 0)
                return false;

            envelope = queue.Dequeue();
            if (_bytesBySession.TryGetValue(sessionId, out var existingBytes))
                _bytesBySession[sessionId] = Math.Max(0, existingBytes - envelope.Payload.Length);
            else
                _bytesBySession[sessionId] = 0;

            if (_metrics.TryGetValue(sessionId, out var metrics))
            {
                metrics.Current = queue.Count;
                _bytesBySession.TryGetValue(sessionId, out var bytes);
                metrics.CurrentBytes = bytes;
                _metrics[sessionId] = metrics;
            }

            return true;
        }

        public bool DropSession(SessionId sessionId)
        {
            if (!_queues.TryGetValue(sessionId, out var queue))
                return false;

            int droppedBytes = 0;
            int droppedCount = 0;
            while (queue.Count > 0)
            {
                var entry = queue.Dequeue();
                droppedBytes += entry.Payload.Length;
                droppedCount++;
                entry.Dispose();
            }

            _queues.Remove(sessionId);
            _bytesBySession.Remove(sessionId);

            if (_metrics.TryGetValue(sessionId, out var metrics))
            {
                metrics.Current = 0;
                metrics.CurrentBytes = 0;
                metrics.Dropped += droppedCount;
                metrics.DroppedBytes += droppedBytes;
                _metrics[sessionId] = metrics;
            }
            else if (droppedCount > 0 || droppedBytes > 0)
            {
                _metrics[sessionId] = new SessionQueueMetrics
                {
                    Current = 0,
                    CurrentBytes = 0,
                    Dropped = droppedCount,
                    DroppedBytes = droppedBytes
                };
            }

            return true;
        }

        public void Clear()
        {
            foreach (var kvp in _queues)
            {
                var queue = kvp.Value;
                while (queue.Count > 0)
                {
                    var entry = queue.Dequeue();
                    entry.Dispose();
                }
            }

            _queues.Clear();
            _metrics.Clear();
            _bytesBySession.Clear();
            _nextSequence = 0;
        }

        public CommandIngressMetrics SnapshotMetrics()
        {
            int count = _metrics.Count;
            if (count == 0)
                return CommandIngressMetrics.Empty;

            EnsureCapacity(ref _snapshotKeys, count);
            EnsureCapacity(ref _snapshotBuffer, count);

            int index = 0;
            foreach (var kvp in _metrics)
                _snapshotKeys[index++] = kvp.Key;

            Array.Sort(_snapshotKeys, 0, count, SessionIdValueComparer.Instance);

            int maxPeak = 0;
            int maxBytes = 0;
            int totalDropped = 0;
            int totalRejected = 0;
            int totalDroppedBytes = 0;
            int totalRejectedBytes = 0;

            for (int i = 0; i < count; i++)
            {
                var sessionId = _snapshotKeys[i];
                var metrics = _metrics[sessionId];
                _snapshotBuffer[i] = new SessionQueueMetricsSnapshot(sessionId, metrics, metrics.CurrentBytes);

                if (metrics.Peak > maxPeak)
                    maxPeak = metrics.Peak;
                if (metrics.PeakBytes > maxBytes)
                    maxBytes = metrics.PeakBytes;
                totalDropped += metrics.Dropped;
                totalDroppedBytes += metrics.DroppedBytes;
                totalRejected += metrics.Rejected;
                totalRejectedBytes += metrics.RejectedBytes;
            }

            var budget = new QueueBudgetSnapshot(maxPeak, maxBytes, totalDropped, totalDroppedBytes, totalRejected, totalRejectedBytes, totalTrims: 0);
            return new CommandIngressMetrics(_snapshotBuffer, count, budget);
        }

        private static void EnsureCapacity<T>(ref T[] buffer, int required)
        {
            if (buffer.Length >= required)
                return;

            var next = buffer.Length == 0 ? required : buffer.Length;
            while (next < required)
                next *= 2;
            buffer = new T[next];
        }
    }

    /// <summary>
    /// Command envelope handed to authoritative consumers. Ownership: caller must Dispose to return
    /// the payload buffer. Dispose is idempotent through the underlying lease.
    /// </summary>
    public readonly struct CommandEnvelope : IDisposable
    {
        public readonly SessionId SessionId;
        public readonly long SubmitTick;
        public readonly long DeterministicSequence;
        public readonly string CommandType;
        public readonly PooledPayloadLease Payload;

        public CommandEnvelope(SessionId sessionId, long submitTick, long deterministicSequence, string commandType, PooledPayloadLease payload)
        {
            SessionId = sessionId;
            SubmitTick = submitTick;
            DeterministicSequence = deterministicSequence;
            CommandType = commandType;
            Payload = payload;
        }

        public void Dispose() => Payload.Dispose();
    }

    public readonly struct CommandIngressResult
    {
        private CommandIngressResult(bool ok, CommandRejectionReason rejectionReason, long sequence)
        {
            Ok = ok;
            RejectionReason = rejectionReason;
            Sequence = sequence;
        }

        public bool Ok { get; }
        public CommandRejectionReason RejectionReason { get; }
        public long Sequence { get; }

        public static CommandIngressResult Accepted(long sequence) => new CommandIngressResult(true, CommandRejectionReason.None, sequence);
        public static CommandIngressResult Rejected(CommandRejectionReason reason) => new CommandIngressResult(false, reason, sequence: -1);
    }

    public enum CommandRejectionReason
    {
        None = 0,
        InvalidSession = 1,
        BackpressureLimitHit = 2
    }

    public struct SessionQueueMetrics
    {
        public int Current { get; set; }
        public int CurrentBytes { get; set; }
        public int Peak { get; set; }
        public int PeakBytes { get; set; }
        public int Rejected { get; set; }
        public int Dropped { get; set; }
        public int RejectedBytes { get; set; }
        public int DroppedBytes { get; set; }
        public int Trims { get; set; }
    }

    public readonly struct QueueBudgetSnapshot
    {
        public QueueBudgetSnapshot(int maxCount, int maxBytes, int totalDropped, int totalDroppedBytes, int totalRejected, int totalRejectedBytes, int totalTrims)
        {
            MaxCount = maxCount;
            MaxBytes = maxBytes;
            TotalDropped = totalDropped;
            TotalDroppedBytes = totalDroppedBytes;
            TotalRejected = totalRejected;
            TotalRejectedBytes = totalRejectedBytes;
            TotalTrims = totalTrims;
        }

        public int MaxCount { get; }
        public int MaxBytes { get; }
        public int TotalDropped { get; }
        public int TotalDroppedBytes { get; }
        public int TotalRejected { get; }
        public int TotalRejectedBytes { get; }
        public int TotalTrims { get; }
    }

    internal readonly struct SessionQueueMetricsReadOnlyList : IReadOnlyList<SessionQueueMetricsSnapshot>
    {
        private readonly SessionQueueMetricsSnapshot[] _buffer;
        private readonly int _count;

        public SessionQueueMetricsReadOnlyList(SessionQueueMetricsSnapshot[] buffer, int count)
        {
            _buffer = buffer ?? Array.Empty<SessionQueueMetricsSnapshot>();
            _count = count;
        }

        public SessionQueueMetricsSnapshot this[int index]
        {
            get
            {
                if ((uint)index >= (uint)_count)
                    throw new ArgumentOutOfRangeException(nameof(index));
                return _buffer[index];
            }
        }

        public int Count => _count;

        public Enumerator GetEnumerator() => new Enumerator(_buffer, _count);

        IEnumerator<SessionQueueMetricsSnapshot> IEnumerable<SessionQueueMetricsSnapshot>.GetEnumerator() => GetEnumerator();

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        internal struct Enumerator : IEnumerator<SessionQueueMetricsSnapshot>
        {
            private readonly SessionQueueMetricsSnapshot[] _buffer;
            private readonly int _count;
            private int _index;

            public Enumerator(SessionQueueMetricsSnapshot[] buffer, int count)
            {
                _buffer = buffer;
                _count = count;
                _index = -1;
            }

            public SessionQueueMetricsSnapshot Current => _buffer[_index];

            object IEnumerator.Current => Current;

            public bool MoveNext()
            {
                var next = _index + 1;
                if (next >= _count)
                    return false;
                _index = next;
                return true;
            }

            public void Reset() => _index = -1;

            public void Dispose()
            {
            }
        }
    }

    public sealed class CommandIngressMetrics
    {
        public static CommandIngressMetrics Empty { get; } = new CommandIngressMetrics(Array.Empty<SessionQueueMetricsSnapshot>(), 0, default);

        internal CommandIngressMetrics(SessionQueueMetricsSnapshot[] perSession, int count, QueueBudgetSnapshot budget)
        {
            _buffer = perSession ?? Array.Empty<SessionQueueMetricsSnapshot>();
            _count = count;
            _view = new SessionQueueMetricsReadOnlyList(_buffer, _count);
            Budget = budget;
        }

        private readonly SessionQueueMetricsSnapshot[] _buffer;
        private readonly int _count;
        private readonly SessionQueueMetricsReadOnlyList _view;

        public int Count => _count;
        public QueueBudgetSnapshot Budget { get; }
        public IReadOnlyList<SessionQueueMetricsSnapshot> PerSession => _view;
    }

    /// <summary>
    /// Transport router that ties inbound command ingestion to outbound snapshot delivery.
    /// Policies are deterministic: inbound overflow is rejected, outbound overflow drops oldest snapshots.
    /// </summary>
    // IL2CPP/AOT SAFETY: Runtime transport routing must never rely on Reflection.Emit or dynamic proxies.
    // Any reflection-based access must be explicitly preserved (none used here), and managed stripping
    // assumptions must be guarded by explicit registration in build pipelines.
    public sealed class DeterministicTransportRouter
    {
        private readonly AuthoritativeCommandIngress _ingress;
        private readonly BoundedReplicationSnapshotQueue _snapshotQueue;

        public DeterministicTransportRouter(RuntimeBackpressureConfig config, ReplicationSnapshotCounters? counters = null)
        {
#if DEBUG
            IdentifierNamespaceGuardrails.AssertCanonicalIdentifierNamespaces();
#endif
            _ingress = new AuthoritativeCommandIngress(config);
            _snapshotQueue = new BoundedReplicationSnapshotQueue(config, counters);
        }

        public CommandIngressResult RouteInbound(SessionId sessionId, ReadOnlySpan<byte> payload, string commandType, long submitTick)
        {
            return _ingress.TryEnqueue(sessionId, payload, commandType, submitTick);
        }

        public CommandIngressResult RouteInbound(SessionId sessionId, PooledPayloadLease payload, string commandType, long submitTick)
        {
            return _ingress.TryEnqueue(sessionId, payload, commandType, submitTick);
        }

        public void RouteSnapshot(Caelmor.ClientReplication.ClientReplicationSnapshot snapshot)
        {
            _snapshotQueue.Enqueue(snapshot.SessionId, snapshot);
        }

        public int DrainIngressDeterministic(Span<CommandEnvelope> destination, int maxCommands)
        {
            return _ingress.DrainDeterministic(destination, maxCommands);
        }

        public bool TryDequeueSnapshot(SessionId sessionId, out SerializedSnapshot snapshot)
        {
            return _snapshotQueue.TryDequeue(sessionId, out snapshot);
        }

        public void DropSession(SessionId sessionId)
        {
            _ingress.DropSession(sessionId);
            _snapshotQueue.DropSession(sessionId);
        }

        public void Clear()
        {
            _ingress.Clear();
            _snapshotQueue.Clear();
        }

        public TransportBackpressureDiagnostics CaptureDiagnostics()
        {
            return new TransportBackpressureDiagnostics(_ingress.SnapshotMetrics(), _snapshotQueue.SnapshotMetrics());
        }
    }

    public sealed class TransportBackpressureDiagnostics
    {
        public TransportBackpressureDiagnostics(CommandIngressMetrics ingress, SnapshotQueueMetrics snapshots)
        {
            Ingress = ingress;
            Snapshots = snapshots;
        }

        public CommandIngressMetrics Ingress { get; }
        public SnapshotQueueMetrics Snapshots { get; }

        public QueueBudgetSnapshot IngressBudget => Ingress.Budget;
        public QueueBudgetSnapshot SnapshotBudget => Snapshots.Budget;
        public ReplicationSnapshotCounterSnapshot SnapshotCounters => Snapshots.Counters;

        public bool IsWithinBudgets(RuntimeBackpressureConfig config)
        {
            if (config is null) throw new ArgumentNullException(nameof(config));

            return IngressBudget.MaxCount <= config.MaxInboundCommandsPerSession
                && IngressBudget.MaxBytes <= config.MaxQueuedBytesPerSession
                && SnapshotBudget.MaxCount <= config.MaxOutboundSnapshotsPerSession
                && SnapshotBudget.MaxBytes <= config.MaxQueuedBytesPerSession;
        }
    }

    public readonly struct SessionQueueMetricsSnapshot
    {
        public SessionQueueMetricsSnapshot(SessionId sessionId, SessionQueueMetrics metrics, int queuedBytes)
        {
            SessionId = sessionId;
            Metrics = metrics;
            QueuedBytes = queuedBytes;
        }

        public SessionId SessionId { get; }
        public SessionQueueMetrics Metrics { get; }
        public int QueuedBytes { get; }
    }

    /// <summary>
    /// Deterministic snapshot queue implementation with explicit byte and item caps.
    /// Drops oldest snapshots when caps are exceeded and returns pooled buffers for any dropped payloads.
    /// </summary>
    public sealed class BoundedReplicationSnapshotQueue : Caelmor.ClientReplication.ISerializedSnapshotQueue
    {
        private readonly RuntimeBackpressureConfig _config;
        private readonly SnapshotDeltaSerializer _serializer;
        private readonly Dictionary<SessionId, Queue<SerializedSnapshot>> _queues = new Dictionary<SessionId, Queue<SerializedSnapshot>>();
        private readonly Dictionary<SessionId, int> _bytesBySession = new Dictionary<SessionId, int>();
        private readonly Dictionary<SessionId, SessionQueueMetrics> _metrics = new Dictionary<SessionId, SessionQueueMetrics>();
        private readonly Dictionary<SessionId, Dictionary<EntityHandle, string>> _fingerprints = new Dictionary<SessionId, Dictionary<EntityHandle, string>>();
        private readonly ReplicationSnapshotCounters? _counters;
        private SessionId[] _snapshotKeys = Array.Empty<SessionId>();
        private SessionQueueMetricsSnapshot[] _snapshotBuffer = Array.Empty<SessionQueueMetricsSnapshot>();

        public BoundedReplicationSnapshotQueue(RuntimeBackpressureConfig config, ReplicationSnapshotCounters? counters = null)
        {
            _config = config ?? throw new ArgumentNullException(nameof(config));
            _serializer = new SnapshotDeltaSerializer();
            _counters = counters;
        }

        public void Enqueue(SessionId sessionId, Caelmor.ClientReplication.ClientReplicationSnapshot snapshot)
        {
            if (!_queues.TryGetValue(sessionId, out var queue))
            {
                queue = new Queue<SerializedSnapshot>();
                _queues[sessionId] = queue;
            }

            if (!_metrics.TryGetValue(sessionId, out var metrics))
                metrics = new SessionQueueMetrics();

            var baseline = GetOrCreateFingerprintMap(sessionId);
            var serialized = _serializer.Serialize(snapshot, baseline);
            _counters?.RecordSnapshotSerialized();

            _bytesBySession.TryGetValue(sessionId, out int currentBytes);

            queue.Enqueue(serialized);
            var updatedBytes = currentBytes + serialized.ByteLength;
            _bytesBySession[sessionId] = updatedBytes;
            metrics.Peak = Math.Max(metrics.Peak, queue.Count);
            metrics.Current = queue.Count;
            metrics.CurrentBytes = updatedBytes;
            metrics.PeakBytes = Math.Max(metrics.PeakBytes, updatedBytes);
            _metrics[sessionId] = metrics;

            _counters?.RecordSnapshotEnqueued();

            EnforceCaps(sessionId, queue);
        }

        private Dictionary<EntityHandle, string> GetOrCreateFingerprintMap(SessionId sessionId)
        {
            if (!_fingerprints.TryGetValue(sessionId, out var map))
            {
                map = new Dictionary<EntityHandle, string>();
                _fingerprints[sessionId] = map;
            }

            return map;
        }

        private void EnforceCaps(SessionId sessionId, Queue<SerializedSnapshot> queue)
        {
            _bytesBySession.TryGetValue(sessionId, out int bytes);
            if (!_metrics.TryGetValue(sessionId, out var metrics))
                metrics = new SessionQueueMetrics();

            while ((queue.Count > _config.MaxOutboundSnapshotsPerSession) || bytes > _config.MaxQueuedBytesPerSession)
            {
                var dropped = queue.Dequeue();
                bytes -= dropped.ByteLength;
                dropped.Dispose();
                metrics.Dropped++;
                metrics.DroppedBytes += dropped.ByteLength;
                metrics.Trims++;
                _counters?.RecordSnapshotDropped();
            }

            _bytesBySession[sessionId] = Math.Max(0, bytes);
            metrics.Current = queue.Count;
            metrics.CurrentBytes = Math.Max(0, bytes);
            _metrics[sessionId] = metrics;
        }

        public bool TryDequeue(SessionId sessionId, out SerializedSnapshot snapshot)
        {
            snapshot = default;
            if (!_queues.TryGetValue(sessionId, out var queue) || queue.Count == 0)
                return false;

            snapshot = queue.Dequeue();
            if (_bytesBySession.TryGetValue(sessionId, out var existingBytes))
                _bytesBySession[sessionId] = Math.Max(0, existingBytes - snapshot.ByteLength);
            else
                _bytesBySession[sessionId] = 0;

            if (_metrics.TryGetValue(sessionId, out var metrics))
            {
                metrics.Current = queue.Count;
                _bytesBySession.TryGetValue(sessionId, out var bytes);
                metrics.CurrentBytes = bytes;
                _metrics[sessionId] = metrics;
            }

            return true;
        }

        public SnapshotQueueMetrics SnapshotMetrics()
        {
            int count = _metrics.Count;
            if (count == 0)
                return SnapshotQueueMetrics.Empty;

            EnsureCapacity(ref _snapshotKeys, count);
            EnsureCapacity(ref _snapshotBuffer, count);

            int index = 0;
            foreach (var kvp in _metrics)
                _snapshotKeys[index++] = kvp.Key;

            Array.Sort(_snapshotKeys, 0, count, SessionIdValueComparer.Instance);

            int maxPeak = 0;
            int maxBytes = 0;
            int totalDropped = 0;
            int totalDroppedBytes = 0;
            int totalTrims = 0;

            for (int i = 0; i < count; i++)
            {
                var sessionId = _snapshotKeys[i];
                var metrics = _metrics[sessionId];

                _snapshotBuffer[i] = new SessionQueueMetricsSnapshot(sessionId, metrics, metrics.CurrentBytes);

                if (metrics.Peak > maxPeak)
                    maxPeak = metrics.Peak;
                if (metrics.PeakBytes > maxBytes)
                    maxBytes = metrics.PeakBytes;
                totalDropped += metrics.Dropped;
                totalDroppedBytes += metrics.DroppedBytes;
                totalTrims += metrics.Trims;
            }

            var budget = new QueueBudgetSnapshot(maxPeak, maxBytes, totalDropped, totalDroppedBytes, 0, 0, totalTrims);
            var counters = _counters?.Snapshot() ?? ReplicationSnapshotCounterSnapshot.Empty;
            return new SnapshotQueueMetrics(_snapshotBuffer, count, budget, counters);
        }

        public void DropSession(SessionId sessionId)
        {
            if (_queues.TryGetValue(sessionId, out var queue))
            {
                int droppedCount = 0;
                int droppedBytes = 0;
                while (queue.Count > 0)
                {
                    var snapshot = queue.Dequeue();
                    droppedBytes += snapshot.ByteLength;
                    droppedCount++;
                    snapshot.Dispose();
                    _counters?.RecordSnapshotDropped();
                }

                _queues.Remove(sessionId);
                _bytesBySession.Remove(sessionId);

                if (_metrics.TryGetValue(sessionId, out var metrics))
                {
                    metrics.Current = 0;
                    metrics.CurrentBytes = 0;
                    metrics.Dropped += droppedCount;
                    metrics.DroppedBytes += droppedBytes;
                    metrics.Trims += droppedCount;
                    _metrics[sessionId] = metrics;
                }
                else if (droppedCount > 0 || droppedBytes > 0)
                {
                    _metrics[sessionId] = new SessionQueueMetrics
                    {
                        Current = 0,
                        CurrentBytes = 0,
                        Dropped = droppedCount,
                        DroppedBytes = droppedBytes,
                        Trims = droppedCount
                    };
                }
            }

            _bytesBySession.Remove(sessionId);

            if (_metrics.TryGetValue(sessionId, out var existingMetrics))
            {
                existingMetrics.Current = 0;
                existingMetrics.CurrentBytes = 0;
                _metrics[sessionId] = existingMetrics;
            }

            _fingerprints.Remove(sessionId);
        }

        public void Clear()
        {
            foreach (var kvp in _queues)
            {
                var queue = kvp.Value;
                while (queue.Count > 0)
                {
                    queue.Dequeue().Dispose();
                    _counters?.RecordSnapshotDropped();
                }
            }

            _queues.Clear();
            _bytesBySession.Clear();
            _metrics.Clear();
            _fingerprints.Clear();
        }

        private static void EnsureCapacity<T>(ref T[] buffer, int required)
        {
            if (buffer.Length >= required)
                return;

            var next = buffer.Length == 0 ? required : buffer.Length;
            while (next < required)
                next *= 2;
            buffer = new T[next];
        }
    }

    public sealed class SnapshotQueueMetrics
    {
        public static SnapshotQueueMetrics Empty { get; } = new SnapshotQueueMetrics(Array.Empty<SessionQueueMetricsSnapshot>(), 0, default, ReplicationSnapshotCounterSnapshot.Empty);

        internal SnapshotQueueMetrics(SessionQueueMetricsSnapshot[] perSession, int count, QueueBudgetSnapshot budget, ReplicationSnapshotCounterSnapshot counters)
        {
            _buffer = perSession ?? Array.Empty<SessionQueueMetricsSnapshot>();
            _count = count;
            _view = new SessionQueueMetricsReadOnlyList(_buffer, _count);
            Budget = budget;
            Counters = counters;
        }

        private readonly SessionQueueMetricsSnapshot[] _buffer;
        private readonly int _count;
        private readonly SessionQueueMetricsReadOnlyList _view;

        public QueueBudgetSnapshot Budget { get; }
        public int Count => _count;
        public IReadOnlyList<SessionQueueMetricsSnapshot> PerSession => _view;
        public ReplicationSnapshotCounterSnapshot Counters { get; }
    }

    /// <summary>
    /// Persistence write queue with per-player and global caps. Overflow drops the oldest
    /// pending write deterministically to avoid blocking the tick loop while respecting
    /// both count and byte budgets without rebuilding queues.
    /// </summary>
    public sealed class PersistenceWriteQueue
    {
        private readonly RuntimeBackpressureConfig _config;
        private readonly object _gate = new object();
        private readonly PersistencePipelineCounters? _counters;
        private readonly Queue<PersistenceWriteRecord> _globalQueue = new Queue<PersistenceWriteRecord>();
        private readonly Dictionary<PlayerId, Queue<PersistenceWriteRecord>> _perPlayer = new Dictionary<PlayerId, Queue<PersistenceWriteRecord>>();
        private readonly Dictionary<PlayerId, int> _bytesByPlayer = new Dictionary<PlayerId, int>();
        private readonly Dictionary<PlayerId, SessionQueueMetrics> _metrics = new Dictionary<PlayerId, SessionQueueMetrics>();
        private int _globalBytes;
        private int _globalPeakBytes;
        private int _globalPeakCount;
        private int _globalTrims;
        private PlayerId[] _snapshotKeys = Array.Empty<PlayerId>();
        private PersistenceQueueMetricsSnapshot[] _snapshotBuffer = Array.Empty<PersistenceQueueMetricsSnapshot>();

        public PersistenceWriteQueue(RuntimeBackpressureConfig config, PersistencePipelineCounters counters = null)
        {
            _config = config ?? throw new ArgumentNullException(nameof(config));
            _counters = counters;
        }

        public void Enqueue(PlayerId playerId, PersistenceWriteRequest request)
        {
            lock (_gate)
            {
                int payloadBytes = request.EstimatedBytes;
                var record = new PersistenceWriteRecord(playerId, request);

                if (!_perPlayer.TryGetValue(playerId, out var queue))
                {
                    queue = new Queue<PersistenceWriteRecord>();
                    _perPlayer[playerId] = queue;
                }

                if (!_metrics.TryGetValue(playerId, out var metrics))
                    metrics = new SessionQueueMetrics();

                _bytesByPlayer.TryGetValue(playerId, out var currentBytes);

                queue.Enqueue(record);
                _globalQueue.Enqueue(record);
                currentBytes += payloadBytes;
                _bytesByPlayer[playerId] = currentBytes;
                _globalBytes += payloadBytes;

                metrics.Peak = Math.Max(metrics.Peak, queue.Count);
                metrics.Current = queue.Count;
                metrics.CurrentBytes = currentBytes;
                metrics.PeakBytes = Math.Max(metrics.PeakBytes, currentBytes);
                _metrics[playerId] = metrics;

                _globalPeakCount = Math.Max(_globalPeakCount, _globalQueue.Count);
                _globalPeakBytes = Math.Max(_globalPeakBytes, _globalBytes);

                EnforceCaps(playerId, queue);
                EnforceGlobalCap();

                _counters?.RecordRequestEnqueued(_globalQueue.Count, _globalBytes);
                _counters?.RecordWriteBacklog(_globalPeakCount, _globalPeakBytes);
            }
        }

        private void EnforceCaps(PlayerId playerId, Queue<PersistenceWriteRecord> queue)
        {
            if (!_metrics.TryGetValue(playerId, out var metrics))
                metrics = new SessionQueueMetrics();

            _bytesByPlayer.TryGetValue(playerId, out var currentBytes);

            while (queue.Count > _config.MaxPersistenceWritesPerPlayer || currentBytes > _config.MaxPersistenceWriteBytesPerPlayer)
            {
                var dropped = queue.Dequeue();
                int droppedBytes = dropped.Request.EstimatedBytes;
                currentBytes = Math.Max(0, currentBytes - droppedBytes);
                metrics.Dropped++;
                metrics.DroppedBytes += droppedBytes;
                metrics.Trims++;
                RemoveFromGlobal(dropped, droppedBytes, countAsTrim: true);
                _counters?.RecordDrop();
            }

            metrics.Current = queue.Count;
            metrics.CurrentBytes = currentBytes;
            metrics.Peak = Math.Max(metrics.Peak, metrics.Current);
            metrics.PeakBytes = Math.Max(metrics.PeakBytes, currentBytes);
            _metrics[playerId] = metrics;
            _bytesByPlayer[playerId] = currentBytes;
        }

        private void EnforceGlobalCap()
        {
            while (_globalQueue.Count > _config.MaxPersistenceWritesGlobal || _globalBytes > _config.MaxPersistenceWriteBytesGlobal)
            {
                var dropped = _globalQueue.Dequeue();
                int droppedBytes = dropped.Request.EstimatedBytes;
                _globalBytes = Math.Max(0, _globalBytes - droppedBytes);
                _globalTrims++;

                DropFromPerPlayer(dropped, droppedBytes, countAsTrim: true, countDrop: false);
                _counters?.RecordDrop();
            }
        }

        private void DropFromPerPlayer(in PersistenceWriteRecord dropped, int droppedBytes, bool countAsTrim = true, bool countDrop = true)
        {
            if (!_perPlayer.TryGetValue(dropped.PlayerId, out var queue) || queue.Count == 0)
                return;

            int count = queue.Count;
            bool removed = false;
            for (int i = 0; i < count; i++)
            {
                var candidate = queue.Dequeue();
                if (!removed && candidate.Request.Equals(dropped.Request))
                {
                    removed = true;
                    continue;
                }

                queue.Enqueue(candidate);
            }

            if (!removed)
                return;

            _bytesByPlayer.TryGetValue(dropped.PlayerId, out var playerBytes);
            playerBytes = Math.Max(0, playerBytes - droppedBytes);
            _bytesByPlayer[dropped.PlayerId] = playerBytes;

            if (!_metrics.TryGetValue(dropped.PlayerId, out var metrics))
                metrics = new SessionQueueMetrics();

            metrics.Dropped++;
            metrics.DroppedBytes += droppedBytes;
            if (countAsTrim)
                metrics.Trims++;
            metrics.Current = queue.Count;
            metrics.CurrentBytes = playerBytes;
            metrics.Peak = Math.Max(metrics.Peak, metrics.Current);
            metrics.PeakBytes = Math.Max(metrics.PeakBytes, playerBytes);
            _metrics[dropped.PlayerId] = metrics;

            if (countDrop)
                _counters?.RecordDrop();
        }

        private void RemoveFromGlobal(PersistenceWriteRecord dropped, int droppedBytes, bool countAsTrim)
        {
            if (_globalQueue.Count == 0)
                return;

            int count = _globalQueue.Count;
            bool removed = false;
            for (int i = 0; i < count; i++)
            {
                var record = _globalQueue.Dequeue();
                if (!removed && record.PlayerId.Equals(dropped.PlayerId) && record.Request.Equals(dropped.Request))
                {
                    removed = true;
                    _globalBytes = Math.Max(0, _globalBytes - droppedBytes);
                    if (countAsTrim)
                        _globalTrims++;
                    continue;
                }

                _globalQueue.Enqueue(record);
            }
        }

        public bool TryDequeue(out PersistenceWriteRecord record)
        {
            lock (_gate)
            {
                record = default;
                if (_globalQueue.Count == 0)
                    return false;

                record = _globalQueue.Dequeue();
                var recordBytes = record.Request.EstimatedBytes;
                _globalBytes = Math.Max(0, _globalBytes - recordBytes);

                if (_perPlayer.TryGetValue(record.PlayerId, out var queue) && queue.Count > 0 && queue.Peek().Request.Equals(record.Request))
                {
                    queue.Dequeue();
                    _bytesByPlayer.TryGetValue(record.PlayerId, out var playerBytes);
                    playerBytes = Math.Max(0, playerBytes - recordBytes);
                    _bytesByPlayer[record.PlayerId] = playerBytes;
                    if (_metrics.TryGetValue(record.PlayerId, out var metrics))
                    {
                        metrics.Current = queue.Count;
                        metrics.CurrentBytes = playerBytes;
                        _metrics[record.PlayerId] = metrics;
                    }
                }
                else
                {
                    DropFromPerPlayer(record, recordBytes, countAsTrim: false);
                }

                _counters?.RecordRequestDrained(_globalQueue.Count, _globalBytes);
                _counters?.RecordWriteBacklog(_globalQueue.Count, _globalBytes);
                return true;
            }
        }

        public PersistenceQueueMetrics SnapshotMetrics()
        {
            lock (_gate)
            {
                int count = _metrics.Count;
                if (count == 0)
                    return new PersistenceQueueMetrics(Array.Empty<PersistenceQueueMetricsSnapshot>(), 0, default, _globalQueue.Count, _globalBytes, _globalPeakBytes, _globalPeakCount, _globalTrims);

                EnsureCapacity(ref _snapshotKeys, count);
                EnsureCapacity(ref _snapshotBuffer, count);

                int index = 0;
                foreach (var kvp in _metrics)
                    _snapshotKeys[index++] = kvp.Key;

                Array.Sort(_snapshotKeys, 0, count, PlayerIdValueComparer.Instance);

                int maxPeak = 0;
                int maxPeakBytes = 0;
                int totalDropped = 0;
                int totalDroppedBytes = 0;
                int totalTrims = 0;

                for (int i = 0; i < count; i++)
                {
                    var playerId = _snapshotKeys[i];
                    var metrics = _metrics[playerId];
                    _snapshotBuffer[i] = new PersistenceQueueMetricsSnapshot(playerId, metrics);

                    if (metrics.Peak > maxPeak)
                        maxPeak = metrics.Peak;
                    if (metrics.PeakBytes > maxPeakBytes)
                        maxPeakBytes = metrics.PeakBytes;
                    totalDropped += metrics.Dropped;
                    totalDroppedBytes += metrics.DroppedBytes;
                    totalTrims += metrics.Trims;
                }

                var budget = new QueueBudgetSnapshot(maxPeak, maxPeakBytes, totalDropped, totalDroppedBytes, 0, 0, totalTrims);
                return new PersistenceQueueMetrics(_snapshotBuffer, count, budget, _globalQueue.Count, _globalBytes, _globalPeakBytes, _globalPeakCount, _globalTrims);
            }
        }

        public void Clear()
        {
            lock (_gate)
            {
                _globalQueue.Clear();
                _perPlayer.Clear();
                _bytesByPlayer.Clear();
                _metrics.Clear();
                _globalBytes = 0;
                _globalPeakBytes = 0;
                _globalPeakCount = 0;
                _globalTrims = 0;
            }
        }

        private static void EnsureCapacity<T>(ref T[] buffer, int required)
        {
            if (buffer.Length >= required)
                return;

            var next = buffer.Length == 0 ? required : buffer.Length;
            while (next < required)
                next *= 2;
            buffer = new T[next];
        }
    }

    public readonly struct PersistenceWriteRecord
    {
        public readonly PlayerId PlayerId;
        public readonly PersistenceWriteRequest Request;

        public PersistenceWriteRecord(PlayerId playerId, PersistenceWriteRequest request)
        {
            PlayerId = playerId;
            Request = request;
        }
    }

    public sealed class PersistenceQueueMetrics
    {
        public static PersistenceQueueMetrics Empty { get; } = new PersistenceQueueMetrics(Array.Empty<PersistenceQueueMetricsSnapshot>(), 0, default, 0, 0, 0, 0, 0);

        internal PersistenceQueueMetrics(PersistenceQueueMetricsSnapshot[] perPlayer, int count, QueueBudgetSnapshot budget, int globalCount, int globalBytes, int globalPeakBytes, int globalPeakCount, int globalTrims)
        {
            _buffer = perPlayer ?? Array.Empty<PersistenceQueueMetricsSnapshot>();
            _count = count;
            _view = new PersistenceQueueMetricsReadOnlyList(_buffer, _count);
            Budget = budget;
            GlobalCount = globalCount;
            GlobalBytes = globalBytes;
            GlobalPeakBytes = globalPeakBytes;
            GlobalPeakCount = globalPeakCount;
            GlobalTrims = globalTrims;
        }

        private readonly PersistenceQueueMetricsSnapshot[] _buffer;
        private readonly int _count;
        private readonly PersistenceQueueMetricsReadOnlyList _view;

        public QueueBudgetSnapshot Budget { get; }
        public int GlobalCount { get; }
        public int GlobalBytes { get; }
        public int GlobalPeakBytes { get; }
        public int GlobalPeakCount { get; }
        public int GlobalTrims { get; }
        public int Count => _count;
        public IReadOnlyList<PersistenceQueueMetricsSnapshot> PerPlayer => _view;

        public bool IsWithinBudgets(RuntimeBackpressureConfig config)
        {
            if (config is null) throw new ArgumentNullException(nameof(config));

            return Budget.MaxCount <= config.MaxPersistenceWritesPerPlayer
                && Budget.MaxBytes <= config.MaxPersistenceWriteBytesPerPlayer
                && GlobalPeakCount <= config.MaxPersistenceWritesGlobal
                && Math.Max(GlobalBytes, GlobalPeakBytes) <= config.MaxPersistenceWriteBytesGlobal;
        }
    }

    internal readonly struct PersistenceQueueMetricsReadOnlyList : IReadOnlyList<PersistenceQueueMetricsSnapshot>
    {
        private readonly PersistenceQueueMetricsSnapshot[] _buffer;
        private readonly int _count;

        public PersistenceQueueMetricsReadOnlyList(PersistenceQueueMetricsSnapshot[] buffer, int count)
        {
            _buffer = buffer ?? Array.Empty<PersistenceQueueMetricsSnapshot>();
            _count = count;
        }

        public PersistenceQueueMetricsSnapshot this[int index]
        {
            get
            {
                if ((uint)index >= (uint)_count)
                    throw new ArgumentOutOfRangeException(nameof(index));
                return _buffer[index];
            }
        }

        public int Count => _count;

        public Enumerator GetEnumerator() => new Enumerator(_buffer, _count);

        IEnumerator<PersistenceQueueMetricsSnapshot> IEnumerable<PersistenceQueueMetricsSnapshot>.GetEnumerator() => GetEnumerator();

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        internal struct Enumerator : IEnumerator<PersistenceQueueMetricsSnapshot>
        {
            private readonly PersistenceQueueMetricsSnapshot[] _buffer;
            private readonly int _count;
            private int _index;

            public Enumerator(PersistenceQueueMetricsSnapshot[] buffer, int count)
            {
                _buffer = buffer;
                _count = count;
                _index = -1;
            }

            public PersistenceQueueMetricsSnapshot Current => _buffer[_index];

            object IEnumerator.Current => Current;

            public bool MoveNext()
            {
                var next = _index + 1;
                if (next >= _count)
                    return false;
                _index = next;
                return true;
            }

            public void Reset() => _index = -1;

            public void Dispose()
            {
            }
        }
    }

    public readonly struct PersistenceQueueMetricsSnapshot
    {
        public PersistenceQueueMetricsSnapshot(PlayerId playerId, SessionQueueMetrics metrics)
        {
            PlayerId = playerId;
            Metrics = metrics;
        }

        public PlayerId PlayerId { get; }
        public SessionQueueMetrics Metrics { get; }
    }

    internal sealed class SessionIdValueComparer : IComparer<SessionId>
    {
        public static readonly SessionIdValueComparer Instance = new SessionIdValueComparer();

        public int Compare(SessionId x, SessionId y) => x.Value.CompareTo(y.Value);
    }

    internal sealed class PlayerIdValueComparer : IComparer<PlayerId>
    {
        public static readonly PlayerIdValueComparer Instance = new PlayerIdValueComparer();

        public int Compare(PlayerId x, PlayerId y) => x.Value.CompareTo(y.Value);
    }

    /// <summary>
    /// Deterministic delta serializer for replication snapshots. Keeps a per-session baseline
    /// of the last fingerprints and emits only changed/removed entries.
    /// </summary>
    internal sealed class SnapshotDeltaSerializer
    {
        private readonly List<(EntityHandle entity, string fingerprint)> _changed = new List<(EntityHandle, string)>(64);
        private readonly List<EntityHandle> _removed = new List<EntityHandle>(64);
        private readonly HashSet<EntityHandle> _presentEntities = new HashSet<EntityHandle>();

        public SerializedSnapshot Serialize(Caelmor.ClientReplication.ClientReplicationSnapshot snapshot, Dictionary<EntityHandle, string> baseline)
        {
            if (snapshot == null) throw new ArgumentNullException(nameof(snapshot));
            if (baseline == null) throw new ArgumentNullException(nameof(baseline));

            _changed.Clear();
            _removed.Clear();
            _presentEntities.Clear();

            foreach (var entry in snapshot.Entities)
            {
                _presentEntities.Add(entry.Entity);
                baseline.TryGetValue(entry.Entity, out var prevFp);
                if (!string.Equals(prevFp, entry.State.Fingerprint, StringComparison.Ordinal))
                    _changed.Add((entry.Entity, entry.State.Fingerprint));
            }

            foreach (var kvp in baseline)
            {
                bool stillPresent = _presentEntities.Contains(kvp.Key);
                if (!stillPresent)
                    _removed.Add(kvp.Key);
            }

            _changed.Sort(ChangedEntryComparer.Instance);
            _removed.Sort(EntityHandleComparer.Instance);

            int totalBytes = ComputeLength(snapshot.AuthoritativeTick, _changed, _removed);
            var buffer = ArrayPool<byte>.Shared.Rent(totalBytes);
            int offset = 0;

            WriteInt64(buffer, ref offset, snapshot.AuthoritativeTick);
            WriteInt32(buffer, ref offset, _changed.Count);
            WriteInt32(buffer, ref offset, _removed.Count);

            foreach (var entry in _changed)
            {
                WriteInt32(buffer, ref offset, entry.entity.Value);
                WriteString(buffer, ref offset, entry.fingerprint);
            }

            foreach (var entity in _removed)
            {
                WriteInt32(buffer, ref offset, entity.Value);
            }

            // Update baseline deterministically after serialization completes.
            baseline.Clear();
            foreach (var entry in snapshot.Entities)
                baseline[entry.Entity] = entry.State.Fingerprint;

            return SerializedSnapshot.Rent(snapshot.SessionId, snapshot.AuthoritativeTick, buffer, offset, _changed.Count, _removed.Count);
        }

        private static int ComputeLength(long tick, List<(EntityHandle entity, string fingerprint)> changed, List<EntityHandle> removed)
        {
            int length = sizeof(long) + sizeof(int) + sizeof(int);
            foreach (var entry in changed)
            {
                length += sizeof(int); // entity id
                length += sizeof(int); // string length
                length += Encoding.UTF8.GetByteCount(entry.fingerprint);
            }

            length += removed.Count * sizeof(int);
            return length;
        }

        private static void WriteInt64(byte[] buffer, ref int offset, long value)
        {
            unchecked
            {
                buffer[offset++] = (byte)value;
                buffer[offset++] = (byte)(value >> 8);
                buffer[offset++] = (byte)(value >> 16);
                buffer[offset++] = (byte)(value >> 24);
                buffer[offset++] = (byte)(value >> 32);
                buffer[offset++] = (byte)(value >> 40);
                buffer[offset++] = (byte)(value >> 48);
                buffer[offset++] = (byte)(value >> 56);
            }
        }

        private static void WriteInt32(byte[] buffer, ref int offset, int value)
        {
            unchecked
            {
                buffer[offset++] = (byte)value;
                buffer[offset++] = (byte)(value >> 8);
                buffer[offset++] = (byte)(value >> 16);
                buffer[offset++] = (byte)(value >> 24);
            }
        }

        private static void WriteString(byte[] buffer, ref int offset, string value)
        {
            int byteCount = Encoding.UTF8.GetBytes(value, 0, value.Length, buffer, offset + sizeof(int));
            WriteInt32(buffer, ref offset, byteCount);
            offset += byteCount;
        }

        private sealed class ChangedEntryComparer : IComparer<(EntityHandle entity, string fingerprint)>
        {
            public static readonly ChangedEntryComparer Instance = new ChangedEntryComparer();

            public int Compare((EntityHandle entity, string fingerprint) x, (EntityHandle entity, string fingerprint) y)
            {
                return x.entity.Value.CompareTo(y.entity.Value);
            }
        }

        private sealed class EntityHandleComparer : IComparer<EntityHandle>
        {
            public static readonly EntityHandleComparer Instance = new EntityHandleComparer();

            public int Compare(EntityHandle x, EntityHandle y) => x.Value.CompareTo(y.Value);
        }
    }

    /// <summary>
    /// Pooled serialized snapshot lease. Ownership: dequeueing consumer must Dispose after send to
    /// ensure buffer and lease return to pools. Idempotent to guard against multiple Dispose calls.
    /// </summary>
    public sealed class SerializedSnapshot : IDisposable
    {
        private const int MaxPooledLeases = 512;
        private static readonly Stack<SerializedSnapshot> LeasePool = new Stack<SerializedSnapshot>(MaxPooledLeases);

        private int _disposed;

        private SerializedSnapshot() { }

        public SessionId SessionId { get; private set; }
        public long Tick { get; private set; }
        public byte[] Buffer { get; private set; }
        public int ByteLength { get; private set; }
        public int Changes { get; private set; }
        public int Removals { get; private set; }

        public static SerializedSnapshot Rent(SessionId sessionId, long tick, byte[] buffer, int byteLength, int changes, int removals)
        {
            if (buffer == null) throw new ArgumentNullException(nameof(buffer));

            var lease = Acquire();
            lease.SessionId = sessionId;
            lease.Tick = tick;
            lease.Buffer = buffer;
            lease.ByteLength = byteLength;
            lease.Changes = changes;
            lease.Removals = removals;
            lease._disposed = 0;
            return lease;
        }

        private static SerializedSnapshot Acquire()
        {
            lock (LeasePool)
            {
                if (LeasePool.Count > 0)
                    return LeasePool.Pop();
            }

            return new SerializedSnapshot();
        }

        public void Dispose()
        {
            if (Interlocked.Exchange(ref _disposed, 1) == 1)
                return;

            var buffer = Buffer;
            Buffer = null;
            ByteLength = 0;
            Changes = 0;
            Removals = 0;
            SessionId = default;
            Tick = 0;

            if (buffer != null)
                ArrayPool<byte>.Shared.Return(buffer, clearArray: true);

            lock (LeasePool)
            {
                if (LeasePool.Count < MaxPooledLeases)
                    LeasePool.Push(this);
            }
        }
    }
}

namespace Caelmor.ClientReplication
{
    using Caelmor.Runtime.Transport;
    using Caelmor.Runtime.Onboarding;

    /// <summary>
    /// Extension interface to enable dequeue of serialized snapshots for transport.
    /// </summary>
    public interface ISerializedSnapshotQueue : IReplicationSnapshotQueue
    {
        bool TryDequeue(SessionId sessionId, out SerializedSnapshot snapshot);
        SnapshotQueueMetrics SnapshotMetrics();
    }
}
