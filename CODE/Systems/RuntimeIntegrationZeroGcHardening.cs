using System;
using System.Buffers;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using System.Threading;
using Caelmor.Runtime;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.InterestManagement;
using Caelmor.Runtime.Persistence;
using Caelmor.Runtime.Replication;
using Caelmor.Runtime.Sessions;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.WorldSimulation;

namespace Caelmor.Runtime.Integration
{
    /// <summary>
    /// Authoritative input ingestion with fixed per-session command rings.
    /// - Transport thread enqueues only.
    /// - Tick thread freezes deterministically at the start of each authoritative tick.
    /// - No per-tick allocations after warm-up; arrays are rented once per session and reused.
    /// </summary>
    public sealed class AuthoritativeCommandIngestor : IAuthoritativeCommandIngestor
    {
        private readonly RuntimeBackpressureConfig _config;
        private readonly Dictionary<SessionId, SessionCommandState> _perSession = new Dictionary<SessionId, SessionCommandState>(64);
        private readonly ArrayPool<AuthoritativeCommand> _commandPool;
        private readonly Dictionary<SessionId, SessionCommandMetrics> _metrics = new Dictionary<SessionId, SessionCommandMetrics>(64);
        private readonly object _gate = new object();

        private SessionId[] _sessionKeySnapshot = Array.Empty<SessionId>();
        private SessionCommandMetricsSnapshot[] _metricsBuffer = Array.Empty<SessionCommandMetricsSnapshot>();
        private long _nextSequence;

#if DEBUG
        private int _maxCommandsPerSession;
#endif

        public AuthoritativeCommandIngestor(RuntimeBackpressureConfig? config = null, ArrayPool<AuthoritativeCommand>? commandPool = null)
        {
            _config = config ?? RuntimeBackpressureConfig.Default;
            _commandPool = commandPool ?? ArrayPool<AuthoritativeCommand>.Shared;
        }

        public bool TryEnqueue(SessionId sessionId, in AuthoritativeCommand command)
        {
            if (!sessionId.IsValid)
                return false;

            lock (_gate)
            {
                if (!_perSession.TryGetValue(sessionId, out var state))
                {
                    state = SessionCommandState.Create(_config.MaxInboundCommandsPerSession, _commandPool);
                }

                if (command.AuthoritativeTick < state.LastFrozenTick)
                {
                    state.Metrics.DroppedStale++;
                    _perSession[sessionId] = state;
                    _metrics[sessionId] = state.Metrics;
                    return false;
                }

                var enriched = command.WithSequence(Interlocked.Increment(ref _nextSequence));
                // Deterministic overflow policy: reject the newest command when the ring is full.
                var success = state.Ring.TryPush(enriched);

                if (!success)
                {
                    state.Metrics.DroppedOverflow++;
                    _perSession[sessionId] = state;
                    _metrics[sessionId] = state.Metrics;
                    return false;
                }

                state.Metrics.Accepted++;
                state.Metrics.PeakBuffered = Math.Max(state.Metrics.PeakBuffered, state.Ring.Count);
                _perSession[sessionId] = state;
                _metrics[sessionId] = state.Metrics;

#if DEBUG
                if (state.Ring.Count > _maxCommandsPerSession)
                    _maxCommandsPerSession = state.Ring.Count;
#endif

                return true;
            }
        }

        public void FreezeAllSessions(long authoritativeTick)
        {
            lock (_gate)
            {
                int count = _perSession.Count;
                EnsureCapacity(ref _sessionKeySnapshot, count);

                int index = 0;
                foreach (var kvp in _perSession)
                    _sessionKeySnapshot[index++] = kvp.Key;

                Array.Sort(_sessionKeySnapshot, 0, index, Caelmor.Runtime.Transport.SessionIdValueComparer.Instance);

                for (int i = 0; i < index; i++)
                    FreezeSessionLocked(_sessionKeySnapshot[i], authoritativeTick);
            }
        }

        public void FreezeSessions(long authoritativeTick, IReadOnlyList<SessionId> activeSessions)
        {
            if (activeSessions is null) throw new ArgumentNullException(nameof(activeSessions));

            lock (_gate)
            {
                EnsureCapacity(ref _sessionKeySnapshot, activeSessions.Count);

                for (int i = 0; i < activeSessions.Count; i++)
                    _sessionKeySnapshot[i] = activeSessions[i];

                Array.Sort(_sessionKeySnapshot, 0, activeSessions.Count, Caelmor.Runtime.Transport.SessionIdValueComparer.Instance);

                for (int i = 0; i < activeSessions.Count; i++)
                    FreezeSessionLocked(_sessionKeySnapshot[i], authoritativeTick);
            }
        }

        public FrozenCommandBatch GetFrozenBatch(SessionId sessionId)
        {
            lock (_gate)
            {
                if (_perSession.TryGetValue(sessionId, out var state))
                    return state.Frozen;
            }

            return FrozenCommandBatch.Empty(sessionId);
        }

        /// <summary>
        /// Drops all buffered commands for a session (disconnect/unload) and returns pooled buffers.
        /// </summary>
        public bool DropSession(SessionId sessionId)
        {
            lock (_gate)
            {
                if (!_perSession.TryGetValue(sessionId, out var state))
                    return false;

                state.ReturnBuffer(_commandPool);
                _perSession.Remove(sessionId);
                _metrics.Remove(sessionId);
                return true;
            }
        }

        /// <summary>
        /// Clears all session buffers. Invoked during server shutdown to avoid retention leaks.
        /// </summary>
        public void Clear()
        {
            lock (_gate)
            {
                foreach (var kvp in _perSession)
                    kvp.Value.ReturnBuffer(_commandPool);

                _perSession.Clear();
                _metrics.Clear();
                _nextSequence = 0;
            }
        }

        public CommandIngestorDiagnostics SnapshotMetrics()
        {
            lock (_gate)
            {
                int count = _metrics.Count;
                if (count == 0)
                    return CommandIngestorDiagnostics.Empty;

                EnsureCapacity(ref _sessionKeySnapshot, count);
                EnsureCapacity(ref _metricsBuffer, count);

                int index = 0;
                foreach (var kvp in _metrics)
                    _sessionKeySnapshot[index++] = kvp.Key;

                Array.Sort(_sessionKeySnapshot, 0, index, Caelmor.Runtime.Transport.SessionIdValueComparer.Instance);

                int totalDroppedOverflow = 0;
                int totalDroppedStale = 0;
                int totalAccepted = 0;
                int totalFrozen = 0;
                int maxBuffered = 0;

                for (int i = 0; i < index; i++)
                {
                    var sessionId = _sessionKeySnapshot[i];
                    var metrics = _metrics[sessionId];
                    _metricsBuffer[i] = new SessionCommandMetricsSnapshot(sessionId, metrics);

                    totalDroppedOverflow += metrics.DroppedOverflow;
                    totalDroppedStale += metrics.DroppedStale;
                    totalAccepted += metrics.Accepted;
                    totalFrozen += metrics.LastFrozenCount;
                    if (metrics.PeakBuffered > maxBuffered)
                        maxBuffered = metrics.PeakBuffered;
                }

                var totals = new CommandIngestorTotals(totalAccepted, totalDroppedOverflow, totalDroppedStale, totalFrozen, maxBuffered);
                return new CommandIngestorDiagnostics(_metricsBuffer, index, totals);
            }
        }

        private void FreezeSessionLocked(SessionId sessionId, long authoritativeTick)
        {
            if (!_perSession.TryGetValue(sessionId, out var state))
                return;

            state.LastFrozenTick = authoritativeTick;

            if (state.Scratch == null || state.Scratch.Length == 0)
                state.Scratch = _commandPool.Rent(_config.MaxInboundCommandsPerSession);

            var destination = state.Scratch.AsSpan();
            int drained = state.Ring.TryPopAll(destination);

            if (drained > 1)
                Array.Sort(state.Scratch, 0, drained, AuthoritativeCommandComparer.Instance);

            state.Frozen = new FrozenCommandBatch(sessionId, authoritativeTick, state.Scratch, drained);
            state.Metrics.LastFrozenCount = drained;
            _perSession[sessionId] = state;
            _metrics[sessionId] = state.Metrics;
        }

        private static void EnsureCapacity<T>(ref T[] buffer, int required)
        {
            if (buffer.Length >= required)
                return;

            var next = buffer.Length == 0 ? required : buffer.Length;
            while (next < required)
                next <<= 1;
            buffer = new T[next];
        }

        private struct SessionCommandState
        {
            public CommandRing Ring;
            public AuthoritativeCommand[] Scratch;
            public FrozenCommandBatch Frozen;
            public SessionCommandMetrics Metrics;
            public long LastFrozenTick;

            public static SessionCommandState Create(int capacity, ArrayPool<AuthoritativeCommand> pool)
            {
                var buffer = pool.Rent(Math.Max(1, capacity));
                return new SessionCommandState
                {
                    Ring = new CommandRing(capacity),
                    Scratch = buffer,
                    Frozen = FrozenCommandBatch.Empty(default),
                    Metrics = default,
                    LastFrozenTick = 0
                };
            }

            public void ReturnBuffer(ArrayPool<AuthoritativeCommand> pool)
            {
                if (Scratch != null && Scratch.Length > 0)
                    pool.Return(Scratch, clearArray: false);

                Scratch = Array.Empty<AuthoritativeCommand>();
                var capacity = Ring.Capacity <= 0 ? 1 : Ring.Capacity;
                Ring = new CommandRing(capacity);
                Frozen = FrozenCommandBatch.Empty(default);
                Metrics = default;
                LastFrozenTick = 0;
            }
        }

        private struct CommandRing
        {
            private readonly int _capacity;
            private AuthoritativeCommand[] _commands;
            private int _head;
            private int _tail;

            public int Count { get; private set; }
            public int Capacity => _capacity;

            public CommandRing(int capacity)
            {
                _capacity = Math.Max(1, capacity);
                _commands = new AuthoritativeCommand[_capacity + 1];
                _head = 0;
                _tail = 0;
                Count = 0;
            }

            public bool TryPush(in AuthoritativeCommand command)
            {
                var nextTail = (_tail + 1) % _commands.Length;
                if (nextTail == _head)
                    return false;

                _commands[_tail] = command;
                _tail = nextTail;
                Count++;
                return true;
            }

            public int TryPopAll(Span<AuthoritativeCommand> destination)
            {
                var written = 0;
                while (_head != _tail && written < destination.Length)
                {
                    destination[written] = _commands[_head];
                    _commands[_head] = default;
                    _head = (_head + 1) % _commands.Length;
                    written++;
                    Count--;
                }
                return written;
            }
        }
    }

    /// <summary>
    /// Read-only frozen batch for a session within a single authoritative tick.
    /// Backed by a pooled buffer owned by the ingestor; callers must not mutate or retain past the tick.
    /// </summary>
    public readonly struct FrozenCommandBatch
    {
        public readonly SessionId SessionId;
        public readonly long AuthoritativeTick;
        public readonly AuthoritativeCommand[] Buffer;
        public readonly int Count;

        public FrozenCommandBatch(SessionId sessionId, long authoritativeTick, AuthoritativeCommand[] buffer, int count)
        {
            SessionId = sessionId;
            AuthoritativeTick = authoritativeTick;
            Buffer = buffer ?? Array.Empty<AuthoritativeCommand>();
            Count = Math.Max(0, count);
        }

        public static FrozenCommandBatch Empty(SessionId sessionId) => new FrozenCommandBatch(sessionId, authoritativeTick: 0, Array.Empty<AuthoritativeCommand>(), count: 0);

        public ReadOnlySpan<AuthoritativeCommand> AsSpan()
        {
            return Buffer.AsSpan(0, Count);
        }
    }

    public readonly struct AuthoritativeCommand
    {
        public readonly long AuthoritativeTick;
        public readonly int CommandType;
        public readonly int PayloadA;
        public readonly int PayloadB;
        public readonly long DeterministicSequence;

        public AuthoritativeCommand(long authoritativeTick, int commandType, int payloadA, int payloadB, long deterministicSequence = 0)
        {
            AuthoritativeTick = authoritativeTick;
            CommandType = commandType;
            PayloadA = payloadA;
            PayloadB = payloadB;
            DeterministicSequence = deterministicSequence;
        }

        public AuthoritativeCommand WithSequence(long sequence)
        {
            return new AuthoritativeCommand(AuthoritativeTick, CommandType, PayloadA, PayloadB, sequence);
        }
    }

    public sealed class AuthoritativeCommandComparer : IComparer<AuthoritativeCommand>
    {
        public static readonly AuthoritativeCommandComparer Instance = new AuthoritativeCommandComparer();

        public int Compare(AuthoritativeCommand x, AuthoritativeCommand y)
        {
            var c = x.AuthoritativeTick.CompareTo(y.AuthoritativeTick);
            if (c != 0) return c;

            c = x.CommandType.CompareTo(y.CommandType);
            if (c != 0) return c;

            c = x.PayloadA.CompareTo(y.PayloadA);
            if (c != 0) return c;

            c = x.PayloadB.CompareTo(y.PayloadB);
            if (c != 0) return c;

            return x.DeterministicSequence.CompareTo(y.DeterministicSequence);
        }
    }

    public interface IAuthoritativeCommandIngestor
    {
        bool TryEnqueue(SessionId sessionId, in AuthoritativeCommand command);
        void FreezeAllSessions(long authoritativeTick);
        void FreezeSessions(long authoritativeTick, IReadOnlyList<SessionId> activeSessions);
        FrozenCommandBatch GetFrozenBatch(SessionId sessionId);
        bool DropSession(SessionId sessionId);
        void Clear();
        CommandIngestorDiagnostics SnapshotMetrics();
    }

    /// <summary>
    /// Tick-phase hook that freezes authoritative command ingestion at the start of each authoritative tick.
    /// Thread contract: invoked on the tick thread only. Transport/network threads enqueue only.
    /// </summary>
    public sealed class AuthoritativeCommandFreezeHook : ITickPhaseHook
    {
        private readonly IAuthoritativeCommandIngestor _ingestor;
        private readonly IActiveSessionIndex? _activeSessions;

        public AuthoritativeCommandFreezeHook(IAuthoritativeCommandIngestor ingestor, IActiveSessionIndex? activeSessions = null)
        {
            _ingestor = ingestor ?? throw new ArgumentNullException(nameof(ingestor));
            _activeSessions = activeSessions;
        }

        public void OnPreTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            if (_activeSessions != null)
            {
                _ingestor.FreezeSessions(context.TickIndex, _activeSessions.SnapshotSessionsDeterministic());
            }
            else
            {
                _ingestor.FreezeAllSessions(context.TickIndex);
            }
        }

        public void OnPostTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            // No post-tick work required; freeze occurs at tick start.
        }
    }

    public readonly struct CommandIngestorDiagnostics
    {
        public static readonly CommandIngestorDiagnostics Empty = new CommandIngestorDiagnostics(Array.Empty<SessionCommandMetricsSnapshot>(), 0, default);

        private readonly SessionCommandMetricsSnapshot[] _buffer;
        private readonly SessionCommandMetricsReadOnlyList _view;

        public CommandIngestorDiagnostics(SessionCommandMetricsSnapshot[] buffer, int count, CommandIngestorTotals totals)
        {
            _buffer = buffer ?? Array.Empty<SessionCommandMetricsSnapshot>();
            Count = Math.Max(0, count);
            _view = new SessionCommandMetricsReadOnlyList(_buffer, Count);
            Totals = totals;
        }

        public int Count { get; }
        public CommandIngestorTotals Totals { get; }
        public IReadOnlyList<SessionCommandMetricsSnapshot> PerSession => _view;
    }

    public readonly struct CommandIngestorTotals
    {
        public CommandIngestorTotals(int accepted, int droppedOverflow, int droppedStale, int frozenLastTick, int peakBuffered)
        {
            Accepted = accepted;
            DroppedOverflow = droppedOverflow;
            DroppedStale = droppedStale;
            FrozenLastTick = frozenLastTick;
            PeakBuffered = peakBuffered;
        }

        public int Accepted { get; }
        public int DroppedOverflow { get; }
        public int DroppedStale { get; }
        public int FrozenLastTick { get; }
        public int PeakBuffered { get; }
    }

    public struct SessionCommandMetrics
    {
        public int Accepted;
        public int DroppedOverflow;
        public int DroppedStale;
        public int LastFrozenCount;
        public int PeakBuffered;
    }

    public readonly struct SessionCommandMetricsSnapshot
    {
        public SessionCommandMetricsSnapshot(SessionId sessionId, SessionCommandMetrics metrics)
        {
            SessionId = sessionId;
            Metrics = metrics;
        }

        public SessionId SessionId { get; }
        public SessionCommandMetrics Metrics { get; }
    }

    internal readonly struct SessionCommandMetricsReadOnlyList : IReadOnlyList<SessionCommandMetricsSnapshot>
    {
        private readonly SessionCommandMetricsSnapshot[] _buffer;
        private readonly int _count;

        public SessionCommandMetricsReadOnlyList(SessionCommandMetricsSnapshot[] buffer, int count)
        {
            _buffer = buffer ?? Array.Empty<SessionCommandMetricsSnapshot>();
            _count = count;
        }

        public SessionCommandMetricsSnapshot this[int index]
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

        IEnumerator<SessionCommandMetricsSnapshot> IEnumerable<SessionCommandMetricsSnapshot>.GetEnumerator() => GetEnumerator();

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        internal struct Enumerator : IEnumerator<SessionCommandMetricsSnapshot>
        {
            private readonly SessionCommandMetricsSnapshot[] _buffer;
            private readonly int _count;
            private int _index;

            public Enumerator(SessionCommandMetricsSnapshot[] buffer, int count)
            {
                _buffer = buffer;
                _count = count;
                _index = -1;
            }

            public SessionCommandMetricsSnapshot Current => _buffer[_index];

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

    /// <summary>
    /// Interest management implementation using per-session visibility caches backed by a spatial index.
    /// </summary>
    public sealed class VisibilityCullingService : IReplicationEligibilityGate, IDisposable
    {
        private readonly ZoneSpatialIndex _spatialIndex;
        private readonly ArrayPool<EntityHandle> _entityPool;
        private readonly Dictionary<SessionId, VisibilityBucket> _visibility = new Dictionary<SessionId, VisibilityBucket>(64);
        private readonly List<EntityHandle> _queryBuffer;

        public VisibilityCullingService(ZoneSpatialIndex spatialIndex, ArrayPool<EntityHandle>? entityPool = null, int initialQueryCapacity = 64)
        {
            _spatialIndex = spatialIndex ?? throw new ArgumentNullException(nameof(spatialIndex));
            _entityPool = entityPool ?? ArrayPool<EntityHandle>.Shared;
            _queryBuffer = new List<EntityHandle>(Math.Max(4, initialQueryCapacity));
        }

        /// <summary>
        /// Tracks or moves an entity within the zone spatial index without allocations.
        /// </summary>
        public void Track(EntityHandle entity, ZoneId zone, ZonePosition position)
        {
            _spatialIndex.Upsert(entity, zone, position);
        }

        /// <summary>
        /// Removes an entity from the spatial index. Safe to call when already absent.
        /// </summary>
        public void Remove(EntityHandle entity)
        {
            _spatialIndex.Remove(entity);
        }

        /// <summary>
        /// Rebuilds the deterministic visibility set for a session using the spatial index.
        /// </summary>
        public int RefreshVisibility(SessionId session, ZoneInterestQuery query)
        {
            _queryBuffer.Clear();
            _spatialIndex.Query(query, _queryBuffer);
            _queryBuffer.Sort(EntityHandleComparer.Instance);

            var bucket = _visibility.TryGetValue(session, out var existing)
                ? existing
                : new VisibilityBucket(_entityPool.Rent(_queryBuffer.Count == 0 ? 4 : _queryBuffer.Count));

            bucket.SetSorted(_queryBuffer, _entityPool);
            _visibility[session] = bucket;
            return bucket.Count;
        }

        /// <summary>
        /// Provides nearby entities for AI/target-selection surfaces using the same spatial index.
        /// Results are sorted deterministically by EntityHandle value.
        /// </summary>
        public int QueryNearbyTargets(ZoneInterestQuery query, List<EntityHandle> destination)
        {
            if (destination is null) throw new ArgumentNullException(nameof(destination));

            destination.Clear();
            _spatialIndex.Query(query, destination);
            destination.Sort(EntityHandleComparer.Instance);
            return destination.Count;
        }

        public bool IsEntityReplicationEligible(SessionId sessionId, EntityHandle entity)
        {
            if (!_visibility.TryGetValue(sessionId, out var bucket))
                return false;

            return bucket.Contains(entity);
        }

        /// <summary>
        /// Removes cached visibility for a disconnected session and returns rented buffers.
        /// </summary>
        public void RemoveSession(SessionId sessionId)
        {
            if (!_visibility.TryGetValue(sessionId, out var bucket))
                return;

            bucket.Release(_entityPool);
            _visibility.Remove(sessionId);
        }

        /// <summary>
        /// Drops spatial and visibility state for a zone unload.
        /// </summary>
        public void RemoveZone(ZoneId zone)
        {
            _spatialIndex.RemoveZone(zone);

            var sessionsToDrop = new List<SessionId>();
            foreach (var kvp in _visibility)
            {
                sessionsToDrop.Add(kvp.Key);
            }

            for (int i = 0; i < sessionsToDrop.Count; i++)
                RemoveSession(sessionsToDrop[i]);
        }

        /// <summary>
        /// Clears all cached visibility and spatial index state for shutdown.
        /// </summary>
        public void Clear()
        {
            foreach (var kvp in _visibility)
            {
                kvp.Value.Release(_entityPool);
            }

            _visibility.Clear();
            _spatialIndex.Clear();
        }

        public void Dispose()
        {
            Clear();
        }

        private struct VisibilityBucket
        {
            private EntityHandle[] _entities;
            private int _count;

            public VisibilityBucket(EntityHandle[] rented)
            {
                _entities = rented;
                _count = 0;
            }

            public int Count => _count;

            public void SetSorted(List<EntityHandle> source, ArrayPool<EntityHandle> pool)
            {
                EnsureCapacity(source.Count, pool);

                for (int i = 0; i < source.Count; i++)
                    _entities[i] = source[i];

                _count = source.Count;
            }

            public void Release(ArrayPool<EntityHandle> pool)
            {
                if (_entities != null && _entities.Length > 0)
                    pool.Return(_entities, clearArray: false);

                _entities = Array.Empty<EntityHandle>();
                _count = 0;
            }

            public bool Contains(EntityHandle entity)
            {
                int low = 0;
                int high = _count - 1;

                while (low <= high)
                {
                    var mid = low + ((high - low) >> 1);
                    var current = _entities[mid].Value;
                    var target = entity.Value;

                    if (current == target)
                        return true;

                    if (current < target)
                        low = mid + 1;
                    else
                        high = mid - 1;
                }

                return false;
            }

            private void EnsureCapacity(int required, ArrayPool<EntityHandle> pool)
            {
                if (_entities != null && _entities.Length >= required)
                {
                    return;
                }

                var next = _entities == null || _entities.Length == 0 ? Math.Max(4, required) : _entities.Length;
                while (next < required)
                    next *= 2;

                var rented = pool.Rent(next);
                if (_entities != null && _entities.Length > 0)
                    pool.Return(_entities, clearArray: false);

                _entities = rented;
            }
        }
    }

    /// <summary>
    /// Snapshot serializer using pooled byte buffers. Ownership of the rented buffer
    /// stays with the returned payload and must be disposed by the transport.
    /// </summary>
    public sealed class SnapshotSerializer
    {
        private readonly ArrayPool<byte> _pool;

        private long _bytesRented;
        private long _bytesReturned;

        public SnapshotSerializer(ArrayPool<byte>? pool = null)
        {
            _pool = pool ?? ArrayPool<byte>.Shared;
        }

        public PooledTransportPayload Serialize(in ClientReplicationSnapshot snapshot)
        {
            var estimated = 32 + snapshot.EntityCount * 32;
            var buffer = _pool.Rent(estimated);
            var span = buffer.AsSpan();
            var offset = 0;

            WriteInt64(snapshot.AuthoritativeTick, span, ref offset);
            WriteGuid(snapshot.SessionId.Value, span, ref offset);

            WriteInt32(snapshot.EntityCount, span, ref offset);
            var entities = snapshot.EntitiesSpan;
            for (int i = 0; i < snapshot.EntityCount; i++)
            {
                WriteInt32(entities[i].Entity.Value, span, ref offset);
                EnsureCapacity(ref buffer, ref span, offset, entities[i].State.Fingerprint.Length * 4 + offset + 1);
                offset += Encoding.UTF8.GetBytes(entities[i].State.Fingerprint.AsSpan(), span.Slice(offset));
                span[offset++] = 0; // delimiter
            }

            Interlocked.Add(ref _bytesRented, buffer.Length);

            return new PooledTransportPayload(buffer, offset, _pool, OnPayloadReturned);
        }

        private static void WriteInt32(int value, Span<byte> destination, ref int offset)
        {
            System.Buffers.Binary.BinaryPrimitives.WriteInt32LittleEndian(destination.Slice(offset, sizeof(int)), value);
            offset += sizeof(int);
        }

        private static void WriteInt64(long value, Span<byte> destination, ref int offset)
        {
            System.Buffers.Binary.BinaryPrimitives.WriteInt64LittleEndian(destination.Slice(offset, sizeof(long)), value);
            offset += sizeof(long);
        }

        private static void WriteGuid(Guid value, Span<byte> destination, ref int offset)
        {
            Span<byte> guidBytes = stackalloc byte[16];
            value.TryWriteBytes(guidBytes);
            guidBytes.CopyTo(destination.Slice(offset, guidBytes.Length));
            offset += guidBytes.Length;
        }

        private void EnsureCapacity(ref byte[] buffer, ref Span<byte> span, int used, int required)
        {
            if (required <= buffer.Length)
                return;

            var newBuffer = _pool.Rent(required);
            new Span<byte>(buffer, 0, used).CopyTo(newBuffer);
            _pool.Return(buffer, clearArray: false);
            Interlocked.Add(ref _bytesReturned, buffer.Length);
            Interlocked.Add(ref _bytesRented, newBuffer.Length);
            buffer = newBuffer;
            span = buffer.AsSpan();
        }

        private void OnPayloadReturned(int length)
        {
            Interlocked.Add(ref _bytesReturned, length);
        }
    }

    public readonly struct PooledTransportPayload : IDisposable
    {
        public readonly byte[] Buffer;
        public readonly int Length;
        private readonly ArrayPool<byte> _pool;
        private readonly Action<int> _onReturn;

        public PooledTransportPayload(byte[] buffer, int length, ArrayPool<byte> pool, Action<int> onReturn)
        {
            Buffer = buffer;
            Length = length;
            _pool = pool ?? ArrayPool<byte>.Shared;
            _onReturn = onReturn ?? (_ => { });
        }

        public void Dispose()
        {
            if (Buffer != null && Buffer.Length > 0)
            {
                _pool.Return(Buffer, clearArray: false);
                _onReturn(Length);
            }
        }
    }

    /// <summary>
    /// Persistence I/O hook using a fixed request buffer. Actual I/O must run off-thread.
    /// </summary>
    public sealed class PersistenceIoQueue
    {
        private readonly PersistenceRequest[] _requests;
        private int _head;
        private int _tail;

        public PersistenceIoQueue(int capacity)
        {
            if (capacity <= 0) throw new ArgumentOutOfRangeException(nameof(capacity));
            _requests = new PersistenceRequest[capacity];
        }

        public bool TryEnqueue(PersistenceRequest request)
        {
            var nextTail = (_tail + 1) % _requests.Length;
            if (nextTail == _head)
                return false;

            _requests[_tail] = request;
            _tail = nextTail;
            return true;
        }

        public bool TryDequeue(out PersistenceRequest request)
        {
            if (_head == _tail)
            {
                request = default;
                return false;
            }

            request = _requests[_head];
            _requests[_head] = default;
            _head = (_head + 1) % _requests.Length;
            return true;
        }
    }

    public readonly struct PersistenceRequest
    {
        public readonly SaveId SaveId;
        public readonly int Operation;

        public PersistenceRequest(SaveId saveId, int operation)
        {
            SaveId = saveId;
            Operation = operation;
        }
    }

    /// <summary>
    /// Lightweight diagnostics accumulator (thread-safe via Interlocked) without allocations in hot paths.
    /// </summary>
    public sealed class ServerDiagnostics
    {
        private long _errors;
        private long _warnings;
        private long _invariants;

        public void RegisterError() => Interlocked.Increment(ref _errors);
        public void RegisterWarning() => Interlocked.Increment(ref _warnings);
        public void RegisterInvariantViolation() => Interlocked.Increment(ref _invariants);

        public (long errors, long warnings, long invariants) Snapshot()
        {
            return (
                Interlocked.Read(ref _errors),
                Interlocked.Read(ref _warnings),
                Interlocked.Read(ref _invariants));
        }
    }

    /// <summary>
    /// Runtime host entrypoint that wires the tick and world simulation cores without blocking the tick thread.
    /// </summary>
    public sealed class ServerRuntimeHost : IDisposable
    {
        private readonly TickSystem _tickSystem;
        private readonly WorldSimulationCore _worldSimulation;

        public ServerRuntimeHost(TickSystem tickSystem, WorldSimulationCore worldSimulation)
        {
            _tickSystem = tickSystem ?? throw new ArgumentNullException(nameof(tickSystem));
            _worldSimulation = worldSimulation ?? throw new ArgumentNullException(nameof(worldSimulation));
        }

        public void Start()
        {
            _worldSimulation.Start();
            _tickSystem.Start();
        }

        public void Stop()
        {
            _tickSystem.Stop();
            _worldSimulation.Stop();
        }

        public void Dispose()
        {
            Stop();
        }
    }
}
