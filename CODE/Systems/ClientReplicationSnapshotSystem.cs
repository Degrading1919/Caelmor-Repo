using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.WorldSimulation;

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

        private long? _tickInProgress;
        private bool _postTickPhaseActive;

        public ClientReplicationSnapshotSystem(
            IActiveSessionIndex sessionIndex,
            ISnapshotEligibilityView sessionEligibility,
            IReplicationEligibilityGate eligibilityGate,
            IReplicationStateReader stateReader,
            IReplicationSnapshotQueue queue)
        {
            _sessionIndex = sessionIndex ?? throw new ArgumentNullException(nameof(sessionIndex));
            _sessionEligibility = sessionEligibility ?? throw new ArgumentNullException(nameof(sessionEligibility));
            _eligibilityGate = eligibilityGate ?? throw new ArgumentNullException(nameof(eligibilityGate));
            _stateReader = stateReader ?? throw new ArgumentNullException(nameof(stateReader));
            _queue = queue ?? throw new ArgumentNullException(nameof(queue));
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

                    var snapshot = CaptureSnapshotForSession(sessionId, context.TickIndex, eligibleEntities);
                    _queue.Enqueue(sessionId, snapshot);
                }
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

            var entries = new List<ReplicatedEntitySnapshot>(eligibleEntities.Count);
            for (int i = 0; i < eligibleEntities.Count; i++)
            {
                var entity = eligibleEntities[i];
                if (!_eligibilityGate.IsEntityReplicationEligible(sessionId, entity))
                    continue;

                var state = _stateReader.ReadCommittedState(entity);
                entries.Add(new ReplicatedEntitySnapshot(entity, state));
            }

            entries.Sort(static (a, b) => a.Entity.Value.CompareTo(b.Entity.Value));

            return new ClientReplicationSnapshot(sessionId, authoritativeTick, entries);
        }
    }

    /// <summary>
    /// Immutable client replication snapshot captured after tick finalization.
    /// </summary>
    public sealed class ClientReplicationSnapshot
    {
        public SessionId SessionId { get; }
        public long AuthoritativeTick { get; }
        public IReadOnlyList<ReplicatedEntitySnapshot> Entities { get; }

        public ClientReplicationSnapshot(
            SessionId sessionId,
            long authoritativeTick,
            IReadOnlyList<ReplicatedEntitySnapshot> entities)
        {
            SessionId = sessionId;
            AuthoritativeTick = authoritativeTick;
            Entities = new ReadOnlyCollection<ReplicatedEntitySnapshot>(
                (entities != null)
                    ? new List<ReplicatedEntitySnapshot>(entities)
                    : throw new ArgumentNullException(nameof(entities)));
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
