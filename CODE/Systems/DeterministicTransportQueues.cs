using System;
using System.Buffers;
using System.Collections.Generic;
using System.Text;
using System.Threading;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Persistence;
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
                _metrics[sessionId] = metrics;
                payload.Dispose();
                return CommandIngressResult.Rejected(CommandRejectionReason.BackpressureLimitHit);
            }

            long sequence = ++_nextSequence;
            var envelope = new CommandEnvelope(sessionId, submitTick, sequence, commandType ?? string.Empty, payload);
            queue.Enqueue(envelope);
            _bytesBySession[sessionId] = currentBytes + payloadSize;

            metrics.Peak = Math.Max(metrics.Peak, queue.Count);
            metrics.Current = queue.Count;
            _metrics[sessionId] = metrics;

            return CommandIngressResult.Accepted(sequence);
        }

        public bool TryDequeue(SessionId sessionId, out CommandEnvelope envelope)
        {
            envelope = default;
            if (!_queues.TryGetValue(sessionId, out var queue) || queue.Count == 0)
                return false;

            envelope = queue.Dequeue();
            _bytesBySession[sessionId] = Math.Max(0, _bytesBySession[sessionId] - envelope.Payload.Length);

            if (_metrics.TryGetValue(sessionId, out var metrics))
            {
                metrics.Current = queue.Count;
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
                metrics.Dropped += droppedCount;
                metrics.DroppedBytes += droppedBytes;
                _metrics[sessionId] = metrics;
            }
            else if (droppedCount > 0 || droppedBytes > 0)
            {
                _metrics[sessionId] = new SessionQueueMetrics
                {
                    Current = 0,
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
                return new CommandIngressMetrics(Array.Empty<SessionQueueMetricsSnapshot>());

            var keys = ArrayPool<SessionId>.Shared.Rent(count);
            int index = 0;
            foreach (var kvp in _metrics)
                keys[index++] = kvp.Key;

            Array.Sort(keys, 0, count, SessionIdValueComparer.Instance);

            var perSession = new List<SessionQueueMetricsSnapshot>(count);
            for (int i = 0; i < count; i++)
            {
                var sessionId = keys[i];
                _bytesBySession.TryGetValue(sessionId, out int bytes);
                perSession.Add(new SessionQueueMetricsSnapshot(sessionId, _metrics[sessionId], bytes));
            }

            ArrayPool<SessionId>.Shared.Return(keys, clearArray: true);
            return new CommandIngressMetrics(perSession);
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
        public int Peak { get; set; }
        public int Rejected { get; set; }
        public int Dropped { get; set; }
        public int RejectedBytes { get; set; }
        public int DroppedBytes { get; set; }
    }

    public sealed class CommandIngressMetrics
    {
        public CommandIngressMetrics(IReadOnlyList<SessionQueueMetricsSnapshot> perSession)
        {
            PerSession = perSession ?? Array.Empty<SessionQueueMetricsSnapshot>();
        }

        public IReadOnlyList<SessionQueueMetricsSnapshot> PerSession { get; }
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

        public DeterministicTransportRouter(RuntimeBackpressureConfig config)
        {
#if DEBUG
            IdentifierNamespaceGuardrails.AssertCanonicalIdentifierNamespaces();
#endif
            _ingress = new AuthoritativeCommandIngress(config);
            _snapshotQueue = new BoundedReplicationSnapshotQueue(config);
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

        public BoundedReplicationSnapshotQueue(RuntimeBackpressureConfig config)
        {
            _config = config ?? throw new ArgumentNullException(nameof(config));
            _serializer = new SnapshotDeltaSerializer();
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

            _bytesBySession.TryGetValue(sessionId, out int currentBytes);

            queue.Enqueue(serialized);
            _bytesBySession[sessionId] = currentBytes + serialized.ByteLength;
            metrics.Peak = Math.Max(metrics.Peak, queue.Count);
            metrics.Current = queue.Count;
            _metrics[sessionId] = metrics;

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
            }

            _bytesBySession[sessionId] = Math.Max(0, bytes);
            metrics.Current = queue.Count;
            _metrics[sessionId] = metrics;
        }

        public bool TryDequeue(SessionId sessionId, out SerializedSnapshot snapshot)
        {
            snapshot = default;
            if (!_queues.TryGetValue(sessionId, out var queue) || queue.Count == 0)
                return false;

            snapshot = queue.Dequeue();
            _bytesBySession[sessionId] = Math.Max(0, _bytesBySession[sessionId] - snapshot.ByteLength);

            if (_metrics.TryGetValue(sessionId, out var metrics))
            {
                metrics.Current = queue.Count;
                _metrics[sessionId] = metrics;
            }

            return true;
        }

        public SnapshotQueueMetrics SnapshotMetrics()
        {
            int count = _metrics.Count;
            if (count == 0)
                return new SnapshotQueueMetrics(Array.Empty<SessionQueueMetricsSnapshot>());

            var keys = ArrayPool<SessionId>.Shared.Rent(count);
            int index = 0;
            foreach (var kvp in _metrics)
                keys[index++] = kvp.Key;

            Array.Sort(keys, 0, count, SessionIdValueComparer.Instance);

            var perSession = new List<SessionQueueMetricsSnapshot>(count);
            for (int i = 0; i < count; i++)
            {
                var sessionId = keys[i];
                _bytesBySession.TryGetValue(sessionId, out int bytes);
                perSession.Add(new SessionQueueMetricsSnapshot(sessionId, _metrics[sessionId], bytes));
            }

            ArrayPool<SessionId>.Shared.Return(keys, clearArray: true);
            return new SnapshotQueueMetrics(perSession);
        }

        public void DropSession(SessionId sessionId)
        {
            if (_queues.TryGetValue(sessionId, out var queue))
            {
                while (queue.Count > 0)
                {
                    queue.Dequeue().Dispose();
                }

                _queues.Remove(sessionId);
            }

            _bytesBySession.Remove(sessionId);

            if (_metrics.TryGetValue(sessionId, out var metrics))
            {
                metrics.Current = 0;
                _metrics[sessionId] = metrics;
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
                }
            }

            _queues.Clear();
            _bytesBySession.Clear();
            _metrics.Clear();
            _fingerprints.Clear();
        }
    }

    public sealed class SnapshotQueueMetrics
    {
        public SnapshotQueueMetrics(IReadOnlyList<SessionQueueMetricsSnapshot> perSession)
        {
            PerSession = perSession ?? Array.Empty<SessionQueueMetricsSnapshot>();
        }

        public IReadOnlyList<SessionQueueMetricsSnapshot> PerSession { get; }
    }

    /// <summary>
    /// Persistence write queue with per-player and global caps. Overflow drops the oldest
    /// pending write deterministically to avoid blocking the tick loop.
    /// </summary>
    public sealed class PersistenceWriteQueue
    {
        private readonly RuntimeBackpressureConfig _config;
        private readonly Queue<PersistenceWriteRecord> _globalQueue = new Queue<PersistenceWriteRecord>();
        private readonly Dictionary<PlayerId, Queue<PersistenceWriteRecord>> _perPlayer = new Dictionary<PlayerId, Queue<PersistenceWriteRecord>>();
        private readonly Dictionary<PlayerId, SessionQueueMetrics> _metrics = new Dictionary<PlayerId, SessionQueueMetrics>();

        public PersistenceWriteQueue(RuntimeBackpressureConfig config)
        {
            _config = config ?? throw new ArgumentNullException(nameof(config));
        }

        public void Enqueue(PlayerId playerId, PersistenceWriteRequest request)
        {
            if (!_perPlayer.TryGetValue(playerId, out var queue))
            {
                queue = new Queue<PersistenceWriteRecord>();
                _perPlayer[playerId] = queue;
            }

            if (!_metrics.TryGetValue(playerId, out var metrics))
                metrics = new SessionQueueMetrics();

            queue.Enqueue(new PersistenceWriteRecord(playerId, request));
            _globalQueue.Enqueue(new PersistenceWriteRecord(playerId, request));
            metrics.Peak = Math.Max(metrics.Peak, queue.Count);
            metrics.Current = queue.Count;
            _metrics[playerId] = metrics;

            EnforceCaps(playerId, queue);
            EnforceGlobalCap();
        }

        private void EnforceCaps(PlayerId playerId, Queue<PersistenceWriteRecord> queue)
        {
            if (!_metrics.TryGetValue(playerId, out var metrics))
                metrics = new SessionQueueMetrics();

            while (queue.Count > _config.MaxPersistenceWritesPerPlayer)
            {
                var dropped = queue.Dequeue();
                metrics.Dropped++;
                metrics.DroppedBytes += dropped.Request.EstimatedBytes;
                RemoveFromGlobal(dropped);
            }

            metrics.Current = queue.Count;
            _metrics[playerId] = metrics;
        }

        private void EnforceGlobalCap()
        {
            while (_globalQueue.Count > _config.MaxPersistenceWritesGlobal)
            {
                var dropped = _globalQueue.Dequeue();
                if (_metrics.TryGetValue(dropped.PlayerId, out var metrics))
                {
                    metrics.Dropped++;
                    metrics.DroppedBytes += dropped.Request.EstimatedBytes;
                    metrics.Current = Math.Max(0, metrics.Current - 1);
                    _metrics[dropped.PlayerId] = metrics;
                }

                if (_perPlayer.TryGetValue(dropped.PlayerId, out var queue) && queue.Count > 0 && queue.Peek().Request.Equals(dropped.Request))
                    queue.Dequeue();
            }
        }

        private void RemoveFromGlobal(PersistenceWriteRecord dropped)
        {
            if (_globalQueue.Count == 0)
                return;

            var remaining = new Queue<PersistenceWriteRecord>(_globalQueue.Count);
            while (_globalQueue.Count > 0)
            {
                var record = _globalQueue.Dequeue();
                if (!(record.PlayerId.Equals(dropped.PlayerId) && record.Request.Equals(dropped.Request)))
                    remaining.Enqueue(record);
            }

            while (remaining.Count > 0)
                _globalQueue.Enqueue(remaining.Dequeue());
        }

        public bool TryDequeue(out PersistenceWriteRecord record)
        {
            record = default;
            if (_globalQueue.Count == 0)
                return false;

            record = _globalQueue.Dequeue();

            if (_perPlayer.TryGetValue(record.PlayerId, out var queue) && queue.Count > 0 && queue.Peek().Request.Equals(record.Request))
            {
                queue.Dequeue();
                if (_metrics.TryGetValue(record.PlayerId, out var metrics))
                {
                    metrics.Current = queue.Count;
                    _metrics[record.PlayerId] = metrics;
                }
            }

            return true;
        }

        public PersistenceQueueMetrics SnapshotMetrics()
        {
            int count = _metrics.Count;
            if (count == 0)
                return new PersistenceQueueMetrics(Array.Empty<PersistenceQueueMetricsSnapshot>(), _globalQueue.Count);

            var keys = ArrayPool<PlayerId>.Shared.Rent(count);
            int index = 0;
            foreach (var kvp in _metrics)
                keys[index++] = kvp.Key;

            Array.Sort(keys, 0, count, PlayerIdValueComparer.Instance);

            var perPlayer = new List<PersistenceQueueMetricsSnapshot>(count);
            for (int i = 0; i < count; i++)
            {
                var playerId = keys[i];
                perPlayer.Add(new PersistenceQueueMetricsSnapshot(playerId, _metrics[playerId]));
            }

            ArrayPool<PlayerId>.Shared.Return(keys, clearArray: true);
            return new PersistenceQueueMetrics(perPlayer, _globalQueue.Count);
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
        public PersistenceQueueMetrics(IReadOnlyList<PersistenceQueueMetricsSnapshot> perPlayer, int globalCount)
        {
            PerPlayer = perPlayer ?? Array.Empty<PersistenceQueueMetricsSnapshot>();
            GlobalCount = globalCount;
        }

        public IReadOnlyList<PersistenceQueueMetricsSnapshot> PerPlayer { get; }
        public int GlobalCount { get; }
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
