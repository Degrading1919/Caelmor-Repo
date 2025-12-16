using System;
using System.Collections.Generic;
using Caelmor.Runtime.WorldSimulation;
using Caelmor.Systems;

namespace Caelmor.Runtime.Npcs
{
    /// <summary>
    /// Server-authoritative NPC runtime (Stage 24.B).
    /// Tracks NPC identity, lifecycle state, and zone residency,
    /// and integrates with the world simulation core for deterministic eligibility.
    /// No AI, combat, networking, or persistence logic is present.
    /// </summary>
    public sealed class NpcRuntimeSystem : ISimulationEntityIndex, ISimulationEligibilityGate, ITickPhaseHook
    {
        private readonly IServerAuthority _authority;
        private readonly object _gate = new object();

        private readonly Dictionary<NpcId, NpcRecord> _byId = new Dictionary<NpcId, NpcRecord>();
        private readonly Dictionary<EntityHandle, NpcId> _idByHandle = new Dictionary<EntityHandle, NpcId>();

        private int _nextHandle = 1;
        private bool _tickInProgress;

        public NpcRuntimeSystem(IServerAuthority authority)
        {
            _authority = authority ?? throw new ArgumentNullException(nameof(authority));
        }

        public string Name => "npc_state_gate";

        public SpawnNpcResult Spawn(NpcId npcId)
        {
            if (!_authority.IsServerAuthoritative)
                return SpawnNpcResult.Failed(SpawnNpcFailureReason.NotServerAuthority);

            if (!npcId.IsValid)
                return SpawnNpcResult.Failed(SpawnNpcFailureReason.InvalidNpcId);

            lock (_gate)
            {
                if (_tickInProgress)
                    return SpawnNpcResult.Failed(SpawnNpcFailureReason.MidTickMutation);

                if (_byId.ContainsKey(npcId))
                    return SpawnNpcResult.Failed(SpawnNpcFailureReason.NpcAlreadyExists);

                var handle = AllocateHandle();
                var record = new NpcRecord(npcId, handle, NpcRuntimeState.Spawned, residentZone: null);

                _byId.Add(npcId, record);
                _idByHandle.Add(handle, npcId);

                return SpawnNpcResult.Success(new NpcRuntimeSnapshot(record));
            }
        }

        public DespawnNpcResult Despawn(NpcId npcId)
        {
            if (!_authority.IsServerAuthoritative)
                return DespawnNpcResult.Failed(DespawnNpcFailureReason.NotServerAuthority);

            if (!npcId.IsValid)
                return DespawnNpcResult.Failed(DespawnNpcFailureReason.InvalidNpcId);

            lock (_gate)
            {
                if (_tickInProgress)
                    return DespawnNpcResult.Failed(DespawnNpcFailureReason.MidTickMutation);

                if (!_byId.TryGetValue(npcId, out var record))
                    return DespawnNpcResult.Failed(DespawnNpcFailureReason.NotFound);

                _byId.Remove(npcId);
                _idByHandle.Remove(record.Handle);

                return DespawnNpcResult.Success(new NpcRuntimeSnapshot(record.WithState(NpcRuntimeState.Despawned, record.ResidentZone)));
            }
        }

        public AttachNpcToZoneResult AttachNpcToZone(NpcId npcId, ZoneId zone)
        {
            if (!_authority.IsServerAuthoritative)
                return AttachNpcToZoneResult.Failed(AttachNpcToZoneFailureReason.NotServerAuthority);

            if (!npcId.IsValid)
                return AttachNpcToZoneResult.Failed(AttachNpcToZoneFailureReason.InvalidNpcId);

            if (zone.Value <= 0)
                return AttachNpcToZoneResult.Failed(AttachNpcToZoneFailureReason.InvalidZoneId);

            lock (_gate)
            {
                if (_tickInProgress)
                    return AttachNpcToZoneResult.Failed(AttachNpcToZoneFailureReason.MidTickMutation);

                if (!_byId.TryGetValue(npcId, out var record))
                    return AttachNpcToZoneResult.Failed(AttachNpcToZoneFailureReason.NotFound);

                if (record.ResidentZone.HasValue)
                {
                    if (record.ResidentZone.Value.Equals(zone))
                        return AttachNpcToZoneResult.Failed(AttachNpcToZoneFailureReason.AlreadyResident, record.ResidentZone);

                    return AttachNpcToZoneResult.Failed(AttachNpcToZoneFailureReason.AlreadyResident, record.ResidentZone);
                }

                record = record.WithState(record.State, zone);
                _byId[npcId] = record;

                return AttachNpcToZoneResult.Success(new NpcRuntimeSnapshot(record));
            }
        }

        public DetachNpcFromZoneResult DetachNpcFromZone(NpcId npcId, ZoneId zone)
        {
            if (!_authority.IsServerAuthoritative)
                return DetachNpcFromZoneResult.Failed(DetachNpcFromZoneFailureReason.NotServerAuthority);

            if (!npcId.IsValid)
                return DetachNpcFromZoneResult.Failed(DetachNpcFromZoneFailureReason.InvalidNpcId);

            if (zone.Value <= 0)
                return DetachNpcFromZoneResult.Failed(DetachNpcFromZoneFailureReason.InvalidZoneId);

            lock (_gate)
            {
                if (_tickInProgress)
                    return DetachNpcFromZoneResult.Failed(DetachNpcFromZoneFailureReason.MidTickMutation);

                if (!_byId.TryGetValue(npcId, out var record))
                    return DetachNpcFromZoneResult.Failed(DetachNpcFromZoneFailureReason.NotFound);

                if (!record.ResidentZone.HasValue)
                    return DetachNpcFromZoneResult.Failed(DetachNpcFromZoneFailureReason.NotResident);

                if (!record.ResidentZone.Value.Equals(zone))
                    return DetachNpcFromZoneResult.Failed(DetachNpcFromZoneFailureReason.ResidentInDifferentZone, record.ResidentZone);

                record = record.WithState(record.State, residentZone: null);
                if (record.State == NpcRuntimeState.Active)
                    record = record.WithState(NpcRuntimeState.Dormant, residentZone: null);

                _byId[npcId] = record;

                return DetachNpcFromZoneResult.Success(new NpcRuntimeSnapshot(record));
            }
        }

        public ActivateNpcResult Activate(NpcId npcId)
        {
            if (!_authority.IsServerAuthoritative)
                return ActivateNpcResult.Failed(ActivateNpcFailureReason.NotServerAuthority);

            if (!npcId.IsValid)
                return ActivateNpcResult.Failed(ActivateNpcFailureReason.InvalidNpcId);

            lock (_gate)
            {
                if (_tickInProgress)
                    return ActivateNpcResult.Failed(ActivateNpcFailureReason.MidTickMutation);

                if (!_byId.TryGetValue(npcId, out var record))
                    return ActivateNpcResult.Failed(ActivateNpcFailureReason.NotFound);

                if (!record.ResidentZone.HasValue)
                    return ActivateNpcResult.Failed(ActivateNpcFailureReason.MissingZoneResidency);

                if (record.State == NpcRuntimeState.Active)
                    return ActivateNpcResult.Success(new NpcRuntimeSnapshot(record), wasStateChanged: false);

                record = record.WithState(NpcRuntimeState.Active, record.ResidentZone);
                _byId[npcId] = record;

                return ActivateNpcResult.Success(new NpcRuntimeSnapshot(record), wasStateChanged: true);
            }
        }

        public DeactivateNpcResult Deactivate(NpcId npcId)
        {
            if (!_authority.IsServerAuthoritative)
                return DeactivateNpcResult.Failed(DeactivateNpcFailureReason.NotServerAuthority);

            if (!npcId.IsValid)
                return DeactivateNpcResult.Failed(DeactivateNpcFailureReason.InvalidNpcId);

            lock (_gate)
            {
                if (_tickInProgress)
                    return DeactivateNpcResult.Failed(DeactivateNpcFailureReason.MidTickMutation);

                if (!_byId.TryGetValue(npcId, out var record))
                    return DeactivateNpcResult.Failed(DeactivateNpcFailureReason.NotFound);

                if (record.State != NpcRuntimeState.Active)
                    return DeactivateNpcResult.Failed(DeactivateNpcFailureReason.NotActive);

                record = record.WithState(NpcRuntimeState.Dormant, record.ResidentZone);
                _byId[npcId] = record;

                return DeactivateNpcResult.Success(new NpcRuntimeSnapshot(record));
            }
        }

        public bool Exists(NpcId npcId)
        {
            if (!npcId.IsValid)
                return false;

            lock (_gate)
            {
                return _byId.ContainsKey(npcId);
            }
        }

        public bool TryGetSnapshot(NpcId npcId, out NpcRuntimeSnapshot snapshot)
        {
            snapshot = default;

            if (!npcId.IsValid)
                return false;

            lock (_gate)
            {
                if (!_byId.TryGetValue(npcId, out var record))
                    return false;

                snapshot = new NpcRuntimeSnapshot(record);
                return true;
            }
        }

        public EntityHandle[] SnapshotEntitiesDeterministic()
        {
            lock (_gate)
            {
                var eligible = new List<EntityHandle>(_byId.Count);
                foreach (var record in _byId.Values)
                {
                    if (record.State == NpcRuntimeState.Active && record.ResidentZone.HasValue)
                        eligible.Add(record.Handle);
                }

                eligible.Sort(static (a, b) => a.Value.CompareTo(b.Value));
                return eligible.ToArray();
            }
        }

        public bool IsEligible(EntityHandle entity)
        {
            lock (_gate)
            {
                if (!_idByHandle.TryGetValue(entity, out var npcId))
                    return false;

                var record = _byId[npcId];
                return record.State == NpcRuntimeState.Active && record.ResidentZone.HasValue;
            }
        }

        public void OnPreTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            lock (_gate)
            {
                _tickInProgress = true;
            }
        }

        public void OnPostTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            lock (_gate)
            {
                _tickInProgress = false;
            }
        }

        private EntityHandle AllocateHandle()
        {
            var value = _nextHandle++;
            if (value <= 0) value = 1;
            return new EntityHandle(value);
        }

        private readonly struct NpcRecord
        {
            public readonly NpcId NpcId;
            public readonly EntityHandle Handle;
            public readonly NpcRuntimeState State;
            public readonly ZoneId? ResidentZone;

            public NpcRecord(NpcId npcId, EntityHandle handle, NpcRuntimeState state, ZoneId? residentZone)
            {
                NpcId = npcId;
                Handle = handle;
                State = state;
                ResidentZone = residentZone;
            }

            public NpcRecord WithState(NpcRuntimeState newState, ZoneId? residentZone)
                => new NpcRecord(NpcId, Handle, newState, residentZone);
        }
    }

    public readonly struct NpcRuntimeSnapshot
    {
        public readonly NpcId NpcId;
        public readonly EntityHandle Handle;
        public readonly NpcRuntimeState State;
        public readonly ZoneId? ResidentZone;

        public NpcRuntimeSnapshot(NpcId npcId, EntityHandle handle, NpcRuntimeState state, ZoneId? residentZone)
        {
            NpcId = npcId;
            Handle = handle;
            State = state;
            ResidentZone = residentZone;
        }

        internal NpcRuntimeSnapshot(NpcRuntimeSystem.NpcRecord record)
            : this(record.NpcId, record.Handle, record.State, record.ResidentZone)
        {
        }
    }

    public enum NpcRuntimeState
    {
        Spawned = 0,
        Active = 1,
        Dormant = 2,
        Despawned = 3
    }

    public readonly struct NpcId : IEquatable<NpcId>
    {
        public readonly Guid Value;

        public NpcId(Guid value)
        {
            Value = value;
        }

        public bool IsValid => Value != Guid.Empty;

        public bool Equals(NpcId other) => Value.Equals(other.Value);
        public override bool Equals(object obj) => obj is NpcId other && Equals(other);
        public override int GetHashCode() => Value.GetHashCode();
        public override string ToString() => Value.ToString();
    }

    public readonly struct SpawnNpcResult
    {
        private SpawnNpcResult(bool ok, SpawnNpcFailureReason failureReason, NpcRuntimeSnapshot snapshot)
        {
            Ok = ok;
            FailureReason = failureReason;
            Snapshot = snapshot;
        }

        public bool Ok { get; }
        public SpawnNpcFailureReason FailureReason { get; }
        public NpcRuntimeSnapshot Snapshot { get; }

        public static SpawnNpcResult Success(NpcRuntimeSnapshot snapshot) => new SpawnNpcResult(true, SpawnNpcFailureReason.None, snapshot);

        public static SpawnNpcResult Failed(SpawnNpcFailureReason reason) => new SpawnNpcResult(false, reason, default);
    }

    public enum SpawnNpcFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidNpcId = 2,
        NpcAlreadyExists = 3,
        MidTickMutation = 4
    }

    public readonly struct DespawnNpcResult
    {
        private DespawnNpcResult(bool ok, DespawnNpcFailureReason failureReason, NpcRuntimeSnapshot snapshot)
        {
            Ok = ok;
            FailureReason = failureReason;
            Snapshot = snapshot;
        }

        public bool Ok { get; }
        public DespawnNpcFailureReason FailureReason { get; }
        public NpcRuntimeSnapshot Snapshot { get; }

        public static DespawnNpcResult Success(NpcRuntimeSnapshot snapshot) => new DespawnNpcResult(true, DespawnNpcFailureReason.None, snapshot);

        public static DespawnNpcResult Failed(DespawnNpcFailureReason reason) => new DespawnNpcResult(false, reason, default);
    }

    public enum DespawnNpcFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidNpcId = 2,
        NotFound = 3,
        MidTickMutation = 4
    }

    public readonly struct AttachNpcToZoneResult
    {
        private AttachNpcToZoneResult(bool ok, AttachNpcToZoneFailureReason failureReason, NpcRuntimeSnapshot snapshot, ZoneId? existing)
        {
            Ok = ok;
            FailureReason = failureReason;
            Snapshot = snapshot;
            ExistingZone = existing;
        }

        public bool Ok { get; }
        public AttachNpcToZoneFailureReason FailureReason { get; }
        public NpcRuntimeSnapshot Snapshot { get; }
        public ZoneId? ExistingZone { get; }

        public static AttachNpcToZoneResult Success(NpcRuntimeSnapshot snapshot) => new AttachNpcToZoneResult(true, AttachNpcToZoneFailureReason.None, snapshot, snapshot.ResidentZone);

        public static AttachNpcToZoneResult Failed(AttachNpcToZoneFailureReason reason, ZoneId? existingZone = null)
            => new AttachNpcToZoneResult(false, reason, default, existingZone);
    }

    public enum AttachNpcToZoneFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidNpcId = 2,
        InvalidZoneId = 3,
        NotFound = 4,
        AlreadyResident = 5,
        MidTickMutation = 6
    }

    public readonly struct DetachNpcFromZoneResult
    {
        private DetachNpcFromZoneResult(bool ok, DetachNpcFromZoneFailureReason failureReason, NpcRuntimeSnapshot snapshot, ZoneId? previous)
        {
            Ok = ok;
            FailureReason = failureReason;
            Snapshot = snapshot;
            PreviousZone = previous;
        }

        public bool Ok { get; }
        public DetachNpcFromZoneFailureReason FailureReason { get; }
        public NpcRuntimeSnapshot Snapshot { get; }
        public ZoneId? PreviousZone { get; }

        public static DetachNpcFromZoneResult Success(NpcRuntimeSnapshot snapshot)
            => new DetachNpcFromZoneResult(true, DetachNpcFromZoneFailureReason.None, snapshot, snapshot.ResidentZone);

        public static DetachNpcFromZoneResult Failed(DetachNpcFromZoneFailureReason reason, ZoneId? previousZone = null)
            => new DetachNpcFromZoneResult(false, reason, default, previousZone);
    }

    public enum DetachNpcFromZoneFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidNpcId = 2,
        InvalidZoneId = 3,
        NotFound = 4,
        NotResident = 5,
        ResidentInDifferentZone = 6,
        MidTickMutation = 7
    }

    public readonly struct ActivateNpcResult
    {
        private ActivateNpcResult(bool ok, ActivateNpcFailureReason failureReason, NpcRuntimeSnapshot snapshot, bool wasStateChanged)
        {
            Ok = ok;
            FailureReason = failureReason;
            Snapshot = snapshot;
            WasStateChanged = wasStateChanged;
        }

        public bool Ok { get; }
        public ActivateNpcFailureReason FailureReason { get; }
        public NpcRuntimeSnapshot Snapshot { get; }
        public bool WasStateChanged { get; }

        public static ActivateNpcResult Success(NpcRuntimeSnapshot snapshot, bool wasStateChanged)
            => new ActivateNpcResult(true, ActivateNpcFailureReason.None, snapshot, wasStateChanged);

        public static ActivateNpcResult Failed(ActivateNpcFailureReason reason)
            => new ActivateNpcResult(false, reason, default, wasStateChanged: false);
    }

    public enum ActivateNpcFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidNpcId = 2,
        NotFound = 3,
        MissingZoneResidency = 4,
        MidTickMutation = 5
    }

    public readonly struct DeactivateNpcResult
    {
        private DeactivateNpcResult(bool ok, DeactivateNpcFailureReason failureReason, NpcRuntimeSnapshot snapshot)
        {
            Ok = ok;
            FailureReason = failureReason;
            Snapshot = snapshot;
        }

        public bool Ok { get; }
        public DeactivateNpcFailureReason FailureReason { get; }
        public NpcRuntimeSnapshot Snapshot { get; }

        public static DeactivateNpcResult Success(NpcRuntimeSnapshot snapshot)
            => new DeactivateNpcResult(true, DeactivateNpcFailureReason.None, snapshot);

        public static DeactivateNpcResult Failed(DeactivateNpcFailureReason reason)
            => new DeactivateNpcResult(false, reason, default);
    }

    public enum DeactivateNpcFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidNpcId = 2,
        NotFound = 3,
        NotActive = 4,
        MidTickMutation = 5
    }
}
