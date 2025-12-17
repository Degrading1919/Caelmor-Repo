using System;
using System.Buffers;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.WorldSimulation;
using Caelmor.Runtime.Threading;

namespace Caelmor.Runtime.Replication
{
    /// <summary>
    /// Stage 29.B — Client Replication & Snapshot Runtime.
    ///
    /// Responsibilities:
    /// - Capture immutable, deterministic snapshots after tick finalization
    /// - Enforce replication eligibility gates per session and entity
    /// - Queue snapshots for downstream delivery without performing transport
    /// - Never mutate simulation state or influence simulation outcomes
    ///
    /// This system executes only during Post-Tick Finalization and rejects
    /// any mid-tick snapshot generation attempts.
    /// </summary>
    public sealed class ClientReplicationSnapshotSystem : ITickPhaseHook
    {
        private readonly IActiveSessionIndex _sessionIndex;
        private readonly ISnapshotEligibilityView _sessionEligibility;
        private readonly IReplicationEligibilityGate _eligibilityGate;
        private readonly IReplicationStateReader _stateReader;
        private readonly IReplicationSnapshotQueue _queue;
        private readonly TimeSlicedWorkScheduler _timeSlicer;
        private readonly SnapshotSerializationBudget _budget;

        private long? _tickInProgress;
        private bool _postTickPhaseActive;

        private readonly ArrayPool<ReplicatedEntitySnapshot> _snapshotPool = ArrayPool<ReplicatedEntitySnapshot>.Shared;
        private readonly ArrayPool<EntityHandle> _entityPool = ArrayPool<EntityHandle>.Shared;

#if DEBUG
        private long _snapshotsCaptured;
        private long _entitiesCaptured;
        private long _arraysRented;
        private long _arraysReturned;
        private int _maxEntitiesInSnapshot;
#endif

        public ClientReplicationSnapshotSystem(
            IActiveSessionIndex sessionIndex,
            ISnapshotEligibilityView sessionEligibility,
            IReplicationEligibilityGate eligibilityGate,
            IReplicationStateReader stateReader,
            IReplicationSnapshotQueue queue,
            TimeSlicedWorkScheduler timeSlicer,
            SnapshotSerializationBudget? budget = null)
        {
            _sessionIndex = sessionIndex ?? throw new ArgumentNullException(nameof(sessionIndex));
            _sessionEligibility = sessionEligibility ?? throw new ArgumentNullException(nameof(sessionEligibility));
            _eligibilityGate = eligibilityGate ?? throw new ArgumentNullException(nameof(eligibilityGate));
            _stateReader = stateReader ?? throw new ArgumentNullException(nameof(stateReader));
            _queue = queue ?? throw new ArgumentNullException(nameof(queue));
            _timeSlicer = timeSlicer ?? throw new ArgumentNullException(nameof(timeSlicer));
            _budget = budget ?? SnapshotSerializationBudget.Default;
        }

        public void OnPreTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            // Guard against mid-tick snapshot generation.
            _tickInProgress = context.TickIndex;
            _postTickPhaseActive = false;
        }

        public void OnPostTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            _tickInProgress = context.TickIndex;
            _postTickPhaseActive = true;

            try
            {
                var sessions = _sessionIndex.SnapshotSessionsDeterministic();

                for (int i = 0; i < sessions.Count; i++)
                {
                    var sessionId = sessions[i];

                    if (!_sessionEligibility.IsSnapshotEligible(sessionId))
                        continue;

                    var workItem = CreateWorkItem(sessionId, context.TickIndex, eligibleEntities);
                    _timeSlicer.Enqueue(workItem);
                }

                _timeSlicer.ExecuteSlices(_budget.SliceBudgetPerTick, _budget.MaxSlicesPerTick);
            }
            finally
            {
                _postTickPhaseActive = false;
            }
        }

        /// <summary>
        /// Captures an immutable snapshot for a specific client session.
        /// Only valid during Post-Tick Finalization; throws otherwise.
        /// </summary>
        public ClientReplicationSnapshot CaptureSnapshotForSession(
            SessionId sessionId,
            long authoritativeTick,
            IReadOnlyList<EntityHandle> eligibleEntities)
        {
            if (!_postTickPhaseActive || !_tickInProgress.HasValue || _tickInProgress.Value != authoritativeTick)
                throw new InvalidOperationException("Snapshots can only be captured during post-tick finalization.");

            var captureBuffer = new List<ReplicatedEntitySnapshot>(Math.Max(eligibleEntities.Count, _budget.EntitiesPerSlice));

            for (int i = 0; i < eligibleEntities.Count; i++)
            {
                var entity = eligibleEntities[i];
                if (!_eligibilityGate.IsEntityReplicationEligible(sessionId, entity))
                    continue;

                var state = _stateReader.ReadCommittedState(entity);
                captureBuffer.Add(new ReplicatedEntitySnapshot(entity, state));
            }

            var count = captureBuffer.Count;
            if (count == 0)
            {
                return new ClientReplicationSnapshot(sessionId, authoritativeTick, Array.Empty<ReplicatedEntitySnapshot>(), 0, _snapshotPool, OnSnapshotDisposed);
            }

            var buffer = _snapshotPool.Rent(count);

            for (int i = 0; i < count; i++)
                buffer[i] = captureBuffer[i];

            Array.Sort(buffer, 0, count, ReplicatedEntitySnapshotComparer.Instance);

#if DEBUG
            TrackSnapshotAllocated(count);
#endif

            return new ClientReplicationSnapshot(sessionId, authoritativeTick, buffer, count, _snapshotPool, OnSnapshotDisposed);
        }

        private void OnSnapshotDisposed()
        {
#if DEBUG
            _arraysReturned++;
#endif
        }

#if DEBUG
        private void TrackSnapshotAllocated(int entityCount)
        {
            _snapshotsCaptured++;
            _entitiesCaptured += entityCount;
            _arraysRented++;
            if (entityCount > _maxEntitiesInSnapshot)
                _maxEntitiesInSnapshot = entityCount;
        }
#endif

        private SnapshotWorkItem CreateWorkItem(SessionId sessionId, long tick, IReadOnlyList<EntityHandle> eligibleEntities)
        {
#if DEBUG
            Action<int>? onAllocated = TrackSnapshotAllocated;
#else
            Action<int>? onAllocated = null;
#endif
            var count = eligibleEntities.Count;
            if (count == 0)
            {
                return new SnapshotWorkItem(sessionId, tick, Array.Empty<EntityHandle>(), 0, _eligibilityGate, _stateReader, _queue, _snapshotPool, _entityPool, _budget.EntitiesPerSlice, new List<ReplicatedEntitySnapshot>(_budget.EntitiesPerSlice), onAllocated, OnSnapshotDisposed);
            }

            var buffer = _entityPool.Rent(count);
            for (int i = 0; i < count; i++)
                buffer[i] = eligibleEntities[i];

            return new SnapshotWorkItem(sessionId, tick, buffer, count, _eligibilityGate, _stateReader, _queue, _snapshotPool, _entityPool, _budget.EntitiesPerSlice, new List<ReplicatedEntitySnapshot>(_budget.EntitiesPerSlice), onAllocated, OnSnapshotDisposed);
        }

        private sealed class SnapshotWorkItem : ITimeSlicedWorkItem
        {
            private readonly SessionId _sessionId;
            private readonly long _tick;
            private readonly EntityHandle[] _eligible;
            private readonly int _eligibleCount;
            private readonly IReplicationEligibilityGate _eligibilityGate;
            private readonly IReplicationStateReader _stateReader;
            private readonly IReplicationSnapshotQueue _queue;
            private readonly ArrayPool<ReplicatedEntitySnapshot> _snapshotPool;
            private readonly ArrayPool<EntityHandle> _entityPool;
            private readonly List<ReplicatedEntitySnapshot> _captureBuffer;
            private readonly int _entitiesPerSlice;
            private readonly Action<int>? _onAllocated;
            private readonly Action _onDisposed;
            private int _cursor;

            public SnapshotWorkItem(
                SessionId sessionId,
                long tick,
                EntityHandle[] eligible,
                int eligibleCount,
                IReplicationEligibilityGate eligibilityGate,
                IReplicationStateReader stateReader,
                IReplicationSnapshotQueue queue,
                ArrayPool<ReplicatedEntitySnapshot> snapshotPool,
                ArrayPool<EntityHandle> entityPool,
                int entitiesPerSlice,
                List<ReplicatedEntitySnapshot> captureBuffer,
                Action<int>? onAllocated,
                Action onDisposed)
            {
                _sessionId = sessionId;
                _tick = tick;
                _eligible = eligible ?? Array.Empty<EntityHandle>();
                _eligibleCount = eligibleCount;
                _eligibilityGate = eligibilityGate;
                _stateReader = stateReader;
                _queue = queue;
                _snapshotPool = snapshotPool;
                _entityPool = entityPool;
                _entitiesPerSlice = Math.Max(1, entitiesPerSlice);
                _captureBuffer = captureBuffer;
                _captureBuffer.Clear();
                _onAllocated = onAllocated;
                _onDisposed = onDisposed ?? (() => { });
                _cursor = 0;
            }

            public bool ExecuteSlice(TimeSpan budget, out TimeSpan elapsed)
            {
                var stopwatch = Stopwatch.StartNew();
                var processed = 0;

                while (_cursor < _eligibleCount && processed < _entitiesPerSlice)
                {
                    if (stopwatch.Elapsed >= budget)
                        break;

                    var entity = _eligible[_cursor++];
                    if (_eligibilityGate.IsEntityReplicationEligible(_sessionId, entity))
                    {
                        var state = _stateReader.ReadCommittedState(entity);
                        _captureBuffer.Add(new ReplicatedEntitySnapshot(entity, state));
                    }

                    processed++;
                }

                stopwatch.Stop();
                elapsed = stopwatch.Elapsed;

                if (_cursor < _eligibleCount)
                    return false;

                var snapshot = BuildSnapshot();
                _queue.Enqueue(_sessionId, snapshot);
                _entityPool.Return(_eligible, clearArray: false);
                return true;
            }

            private ClientReplicationSnapshot BuildSnapshot()
            {
                var count = _captureBuffer.Count;
                if (count == 0)
                    return new ClientReplicationSnapshot(_sessionId, _tick, Array.Empty<ReplicatedEntitySnapshot>(), 0, _snapshotPool, () => { });

                var buffer = _snapshotPool.Rent(count);
                for (int i = 0; i < count; i++)
                    buffer[i] = _captureBuffer[i];

                Array.Sort(buffer, 0, count, ReplicatedEntitySnapshotComparer.Instance);
                _captureBuffer.Clear();
                _onAllocated?.Invoke(count);
                return new ClientReplicationSnapshot(_sessionId, _tick, buffer, count, _snapshotPool, _onDisposed);
            }
        }
    }

    public readonly struct SnapshotSerializationBudget
    {
        public readonly TimeSpan SliceBudgetPerTick;
        public readonly int MaxSlicesPerTick;
        public readonly int EntitiesPerSlice;

        public SnapshotSerializationBudget(TimeSpan sliceBudgetPerTick, int maxSlicesPerTick, int entitiesPerSlice)
        {
            if (maxSlicesPerTick <= 0) throw new ArgumentOutOfRangeException(nameof(maxSlicesPerTick));
            if (entitiesPerSlice <= 0) throw new ArgumentOutOfRangeException(nameof(entitiesPerSlice));

            SliceBudgetPerTick = sliceBudgetPerTick;
            MaxSlicesPerTick = maxSlicesPerTick;
            EntitiesPerSlice = entitiesPerSlice;
        }

        public static SnapshotSerializationBudget Default => new SnapshotSerializationBudget(TimeSpan.FromMilliseconds(3), 4, 32);
    }

    /// <summary>
    /// Immutable client replication snapshot captured after tick finalization.
    /// </summary>
    public sealed class ClientReplicationSnapshot : IDisposable
    {
        private ReplicatedEntitySnapshot[] _buffer;
        private readonly int _count;
        private readonly ArrayPool<ReplicatedEntitySnapshot> _pool;
        private readonly Action _onDispose;

        public SessionId SessionId { get; }
        public long AuthoritativeTick { get; }
        public int EntityCount => _count;

        public ClientReplicationSnapshot(
            SessionId sessionId,
            long authoritativeTick,
            ReplicatedEntitySnapshot[] buffer,
            int count,
            ArrayPool<ReplicatedEntitySnapshot> pool,
            Action onDispose)
        {
            SessionId = sessionId;
            AuthoritativeTick = authoritativeTick;
            _buffer = buffer ?? throw new ArgumentNullException(nameof(buffer));
            _count = count;
            _pool = pool ?? ArrayPool<ReplicatedEntitySnapshot>.Shared;
            _onDispose = onDispose ?? (() => { });
        }

        public ReadOnlySpan<ReplicatedEntitySnapshot> EntitiesSpan => new ReadOnlySpan<ReplicatedEntitySnapshot>(_buffer, 0, _count);
        public IReadOnlyList<ReplicatedEntitySnapshot> Entities => new SnapshotEntityList(_buffer, _count);

        public ReplicatedEntitySnapshot this[int index]
        {
            get
            {
                if ((uint)index >= (uint)_count)
                    throw new ArgumentOutOfRangeException(nameof(index));
                return _buffer[index];
            }
        }

        /// <summary>
        /// Returns the rented buffer back to the pool. Ownership: the replication transport/queue must
        /// call Dispose once delivery is completed to avoid leaks.
        /// </summary>
        public void Dispose()
        {
            var buffer = _buffer;
            _buffer = Array.Empty<ReplicatedEntitySnapshot>();
            if (buffer != null && buffer.Length > 0)
            {
                _pool.Return(buffer, clearArray: true);
            }

            _onDispose();
        }

        private readonly struct SnapshotEntityList : IReadOnlyList<ReplicatedEntitySnapshot>
        {
            private readonly ReplicatedEntitySnapshot[] _buffer;
            private readonly int _count;

            public SnapshotEntityList(ReplicatedEntitySnapshot[] buffer, int count)
            {
                _buffer = buffer ?? Array.Empty<ReplicatedEntitySnapshot>();
                _count = count;
            }

            public int Count => _count;

            public ReplicatedEntitySnapshot this[int index]
            {
                get
                {
                    if ((uint)index >= (uint)_count)
                        throw new ArgumentOutOfRangeException(nameof(index));
                    return _buffer[index];
                }
            }

            public Enumerator GetEnumerator() => new Enumerator(_buffer, _count);

            IEnumerator<ReplicatedEntitySnapshot> IEnumerable<ReplicatedEntitySnapshot>.GetEnumerator() => GetEnumerator();

            IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

            public struct Enumerator : IEnumerator<ReplicatedEntitySnapshot>
            {
                private readonly ReplicatedEntitySnapshot[] _array;
                private readonly int _count;
                private int _index;

                public Enumerator(ReplicatedEntitySnapshot[] array, int count)
                {
                    _array = array;
                    _count = count;
                    _index = -1;
                }

                public ReplicatedEntitySnapshot Current => _array[_index];

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
    }

    internal sealed class ReplicatedEntitySnapshotComparer : IComparer<ReplicatedEntitySnapshot>
    {
        public static readonly ReplicatedEntitySnapshotComparer Instance = new ReplicatedEntitySnapshotComparer();

        public int Compare(ReplicatedEntitySnapshot x, ReplicatedEntitySnapshot y)
        {
            return x.Entity.Value.CompareTo(y.Entity.Value);
        }
    }

    /// <summary>
    /// Immutable per-entity snapshot payload. Payload contents remain opaque to the runtime
    /// and are provided by an external committed-state reader.
    /// </summary>
    public readonly struct ReplicatedEntitySnapshot
    {
        public EntityHandle Entity { get; }
        public ReplicatedEntityState State { get; }

        public ReplicatedEntitySnapshot(EntityHandle entity, ReplicatedEntityState state)
        {
            Entity = entity;
            State = state;
        }
    }

    /// <summary>
    /// Minimal committed-state representation supplied by the simulation state reader.
    /// </summary>
    public readonly struct ReplicatedEntityState
    {
        public string Fingerprint { get; }

        public ReplicatedEntityState(string fingerprint)
        {
            Fingerprint = fingerprint ?? throw new ArgumentNullException(nameof(fingerprint));
        }
    }

    /// <summary>
    /// Deterministic session index used to enumerate snapshot recipients.
    /// </summary>
    public interface IActiveSessionIndex
    {
        IReadOnlyList<SessionId> SnapshotSessionsDeterministic();
    }

    /// <summary>
    /// Read-only session eligibility query surface used by replication.
    /// </summary>
    public interface ISnapshotEligibilityView
    {
        bool IsSnapshotEligible(SessionId sessionId);
    }

    /// <summary>
    /// Eligibility gate that decides whether an entity may be replicated to a session.
    /// Implementations MUST NOT mutate runtime state.
    /// </summary>
    public interface IReplicationEligibilityGate
    {
        bool IsEntityReplicationEligible(SessionId sessionId, EntityHandle entity);
    }

    /// <summary>
    /// Read-only committed state reader used to populate snapshots.
    /// Implementations must not allocate mutable references to runtime state.
    /// </summary>
    public interface IReplicationStateReader
    {
        ReplicatedEntityState ReadCommittedState(EntityHandle entity);
    }

    /// <summary>
    /// Delivery queue abstraction. This runtime only enqueues snapshots; transport is handled elsewhere.
    /// </summary>
    public interface IReplicationSnapshotQueue
    {
        void Enqueue(SessionId sessionId, ClientReplicationSnapshot snapshot);
    }

    /// <summary>
    /// Thread-safe registry for snapshot eligibility used by player lifecycle and replication.
    /// </summary>
    public sealed class SnapshotEligibilityRegistry : ISnapshotEligibilityRegistry, ISnapshotEligibilityView
    {
        private readonly System.Collections.Concurrent.ConcurrentDictionary<SessionId, byte> _eligible = new();

        public bool TrySetSnapshotEligible(SessionId sessionId, bool isEligible)
        {
            if (sessionId.Equals(default(SessionId)))
                return false;

            if (isEligible)
            {
                _eligible.TryAdd(sessionId, 0);
            }
            else
            {
                _eligible.TryRemove(sessionId, out _);
            }

            return true;
        }

        public bool IsSnapshotEligible(SessionId sessionId)
        {
            if (sessionId.Equals(default(SessionId)))
                return false;

            return _eligible.ContainsKey(sessionId);
        }
    }
}
