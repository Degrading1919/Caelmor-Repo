// CombatIntentQueueSystem.cs
// NOTE: Save location must follow existing project structure.
// This file intentionally contains only the CombatIntentQueueSystem and minimal supporting types.
// No combat resolution, no combat state checks, no persistence, no CombatEvents emission.

using System;
using System.Collections;
using System.Collections.Generic;
using System.Buffers;
using System.Diagnostics;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Tick;

namespace Caelmor.Combat
{
    /// <summary>
    /// CombatIntentQueueSystem
    /// - Owns authoritative combat intent queue (frozen per tick)
    /// - Accepts server-side submissions (payloads)
    /// - Performs structural schema validation only (Stage 11.2)
    /// - Orders deterministically (not based on arrival time; not influenced by client-controlled data)
    /// - Freezes at tick boundary: submissions during tick T become the frozen queue for tick T+1
    /// - Emits observable rejection results for structurally invalid intents (no success outcomes)
    /// - Exposes deterministic snapshots for Stage 9 validation harness
    /// </summary>
    // IL2CPP/AOT SAFETY: No runtime code generation or Reflection.Emit permitted; all runtime entrypoints must be
    // explicitly registered and editor-only APIs avoided. Reflection-based paths (none here) require explicit
    // preservation to survive managed code stripping.
    public sealed class CombatIntentQueueSystem
    {
        private readonly ITickSource _tickSource;
        private readonly IEntityIdValidator _entityIdValidator;
        private readonly IIntentRejectionSink _rejectionSink;

        // Staging: intents received during a tick T, to be frozen for tick T+1.
        private readonly Dictionary<int, StagingBucket> _stagedBySubmitTick = new();
        private readonly StagingBucketPool _stagingBucketPool = new StagingBucketPool(maxSize: 8);

        // Frozen queue exposed for the current authoritative tick.
        private FrozenQueueSnapshot _currentFrozen;
        private readonly Dictionary<int, FrozenQueueSnapshot> _frozenSnapshotsByTick = new();
        private readonly FrozenQueueSnapshotPool _frozenSnapshotPool = new FrozenQueueSnapshotPool(maxSize: 4);

        // Deterministic per-actor sequence assignment for a given frozen tick.
        // Derived deterministically during FreezeForTick() by sorting, not by arrival order.
        private readonly Dictionary<(int FrozenTick, EntityHandle Actor), int> _sequenceCounters = new();

        // Metrics and diagnostics (monotonic counters; deterministic updates).
        private long _structuralRejectCount;
        private long _overflowRejectCount;
        private long _combatIntentsStaged;
        private long _combatIntentsDropped;
        private long _combatAllocWarnings;
        private int _peakStagingUsage;
        private int _lastFrozenCount;

        // Fixed deterministic caps to prevent unbounded growth. Overflow policy is drop-newest with rejection.
        private const int ActorIntentCapPerTick = 8;
        private const int SessionIntentCapPerTick = 64;
        private const int ActorCountCapacityHint = 8;
        private const OverflowPolicy DeterministicOverflowPolicy = OverflowPolicy.DropNewest;

        public CombatIntentQueueSystem(
            ITickSource tickSource,
            IEntityIdValidator entityIdValidator,
            IIntentRejectionSink rejectionSink)
        {
            _tickSource = tickSource ?? throw new ArgumentNullException(nameof(tickSource));
            _entityIdValidator = entityIdValidator ?? throw new ArgumentNullException(nameof(entityIdValidator));
            _rejectionSink = rejectionSink ?? throw new ArgumentNullException(nameof(rejectionSink));

            _tickSource.OnTickAdvanced += HandleTickAdvanced;

            _currentFrozen = RentFrozenSnapshot();
            _currentFrozen.Commit(_tickSource.CurrentTick, 0);
            _frozenSnapshotsByTick[_currentFrozen.AuthoritativeTick] = _currentFrozen;
        }

        /// <summary>
        /// Server-side intake entry point. Validates structure and stages for the current tick.
        /// IMPORTANT:
        /// - No combat resolution
        /// - No combat state legality checks
        /// - No success outcomes emitted
        /// - No dedupe that would break save/load determinism
        /// </summary>
        public IntakeReceipt SubmitIntent(CombatIntentSubmission submission)
        {
            if (submission == null) throw new ArgumentNullException(nameof(submission));

            int submitTick = _tickSource.CurrentTick;

            // DEBUG guardrails: forbid hot-path string entity IDs and dictionary payloads.
            RuntimeGuardrailChecks.AssertTickThreadEntry();
            RuntimeGuardrailChecks.AssertNoDictionaryPayload(submission.Payload);
            RuntimeGuardrailChecks.AssertNoStringEntityId(submission.Payload.Interact.InteractableId);

            if (!CombatIntentStructuralValidator.TryValidate(submission, _entityIdValidator, out var reject))
            {
                var rejection = new IntentRejection(
                    intentId: submission.IntentId ?? string.Empty,
                    actorEntity: submission.ActorEntity,
                    intentType: submission.IntentType,
                    authoritativeTick: submitTick,
                    reasonCode: reject.ReasonCode);

                _structuralRejectCount++;
                _combatIntentsDropped++;
                _rejectionSink.OnRejected(rejection);
                return IntakeReceipt.Rejected(submission.IntentId ?? string.Empty, submitTick, reject.ReasonCode);
            }

            if (!_stagedBySubmitTick.TryGetValue(submitTick, out var bucket))
            {
                bool allocatedNew;
                bucket = _stagingBucketPool.Rent(out allocatedNew);
                NoteAllocWarningIfNeeded(allocatedNew);
                bucket.Prepare(SessionIntentCapPerTick);
                _stagedBySubmitTick.Add(submitTick, bucket);
            }

            if (bucket.SubmissionsCount >= SessionIntentCapPerTick)
            {
                return RejectOverflow(submission, submitTick, RejectReasonCodes.OverflowSessionIntentCap);
            }

            if (bucket.GetActorCount(submission.ActorEntity) >= ActorIntentCapPerTick)
            {
                return RejectOverflow(submission, submitTick, RejectReasonCodes.OverflowActorIntentCap);
            }

            bucket.IncrementActor(submission.ActorEntity);
            bucket.AddSubmission(new StagedSubmission(submission, submitTick));
            _peakStagingUsage = Math.Max(_peakStagingUsage, bucket.SubmissionsCount);

            _combatIntentsStaged++;
            // No success emissions here (explicit).
            return IntakeReceipt.Staged(submission.IntentId!, submitTick);
        }

        private IntakeReceipt RejectOverflow(CombatIntentSubmission submission, int submitTick, string reasonCode)
        {
            if (DeterministicOverflowPolicy != OverflowPolicy.DropNewest)
                throw new InvalidOperationException("Unsupported overflow policy.");

            _overflowRejectCount++;
            _combatIntentsDropped++;

            if (DeterministicOverflowPolicy == OverflowPolicy.DropNewest)
            {
                var rejection = new IntentRejection(
                    intentId: submission.IntentId ?? string.Empty,
                    actorEntity: submission.ActorEntity,
                    intentType: submission.IntentType,
                    authoritativeTick: submitTick,
                    reasonCode: reasonCode);

                _rejectionSink.OnRejected(rejection);
            }

            return IntakeReceipt.Rejected(submission.IntentId ?? string.Empty, submitTick, reasonCode);
        }

        /// <summary>
        /// Returns the frozen queue snapshot for the current authoritative tick.
        /// This snapshot is immutable and stable once created.
        /// </summary>
        public FrozenQueueSnapshot GetFrozenQueueForCurrentTick()
        {
            int tick = _tickSource.CurrentTick;
            if (_currentFrozen.AuthoritativeTick == tick)
                return _currentFrozen;

            if (_frozenSnapshotsByTick.TryGetValue(tick, out var existing))
            {
                _currentFrozen = existing;
                return _currentFrozen;
            }

            var emptySnapshot = RentFrozenSnapshot();
            emptySnapshot.Commit(tick, 0);
            _frozenSnapshotsByTick[tick] = emptySnapshot;
            _currentFrozen = emptySnapshot;
            return _currentFrozen;
        }

        /// <summary>
        /// Deterministic snapshot for Stage 9 harness comparisons.
        /// - Stable ordering
        /// - Minimal stable fields only
        /// </summary>
        public CombatIntentQueueValidationSnapshot GetQueueValidationSnapshot()
        {
            var frozen = GetFrozenQueueForCurrentTick();
            return CombatIntentQueueValidationSnapshot.FromFrozen(frozen);
        }

        public CombatIntentQueueDiagnosticsSnapshot GetDiagnosticsSnapshot()
        {
            return new CombatIntentQueueDiagnosticsSnapshot(
                structuralRejectCount: _structuralRejectCount,
                overflowRejectCount: _overflowRejectCount,
                combatIntentsStaged: _combatIntentsStaged,
                combatIntentsDropped: _combatIntentsDropped,
                combatAllocWarnings: _combatAllocWarnings,
                peakStagingUsage: _peakStagingUsage,
                lastFrozenCount: _lastFrozenCount);
        }

        public void ResetSessionState()
        {
            foreach (var bucket in _stagedBySubmitTick.Values)
                _stagingBucketPool.Return(bucket);

            _stagedBySubmitTick.Clear();

            foreach (var snapshot in _frozenSnapshotsByTick.Values)
                _frozenSnapshotPool.Return(snapshot);

            _frozenSnapshotsByTick.Clear();
            _sequenceCounters.Clear();

            _structuralRejectCount = 0;
            _overflowRejectCount = 0;
            _combatIntentsStaged = 0;
            _combatIntentsDropped = 0;
            _combatAllocWarnings = 0;
            _peakStagingUsage = 0;
            _lastFrozenCount = 0;

            var resetSnapshot = RentFrozenSnapshot();
            resetSnapshot.Commit(_tickSource.CurrentTick, 0);
            _currentFrozen = resetSnapshot;
            _frozenSnapshotsByTick[_currentFrozen.AuthoritativeTick] = _currentFrozen;
        }

        private FrozenQueueSnapshot RentFrozenSnapshot()
        {
            bool allocatedNew;
            var snapshot = _frozenSnapshotPool.Rent(out allocatedNew);
            NoteAllocWarningIfNeeded(allocatedNew);
            return snapshot;
        }

        [Conditional("DEBUG")]
        private void NoteAllocWarningIfNeeded(bool allocatedNew)
        {
            if (allocatedNew)
            {
                RuntimeGuardrailChecks.MarkHotPathAllocationSuspicion();
                _combatAllocWarnings++;
            }
        }

        private void HandleTickAdvanced(int newTick)
        {
            // Tick boundary semantics:
            // - Submissions received during tick (newTick - 1) become frozen queue for tick newTick.
            int sourceSubmitTick = newTick - 1;
            FreezeForTick(newTick, sourceSubmitTick);

            // Runtime hygiene only (not persistence): prune old staging buffers.
            PruneStaging(keepFromTickInclusive: newTick - 4);
        }

        private void FreezeForTick(int frozenTick, int sourceSubmitTick)
        {
            if (!_stagedBySubmitTick.TryGetValue(sourceSubmitTick, out var staged) || staged.SubmissionsCount == 0)
            {
                if (_stagedBySubmitTick.TryGetValue(sourceSubmitTick, out var emptyBucket))
                {
                    _stagedBySubmitTick.Remove(sourceSubmitTick);
                    emptyBucket.Reset();
                    _stagingBucketPool.Return(emptyBucket);
                }

                var emptySnapshot = RentFrozenSnapshot();
                emptySnapshot.Commit(frozenTick, 0);
                _currentFrozen = emptySnapshot;
                _frozenSnapshotsByTick[frozenTick] = emptySnapshot;
                _lastFrozenCount = 0;
                return;
            }

            // Deterministic ordering inputs ONLY:
            // 1) actor_entity_id (ordinal)
            // 2) intent_id (ordinal) -- used as a stable identifier for ordering; no client_nonce involvement
            //
            // NOTE: Ordering must not depend on arrival time or any client-supplied correlation fields.
            staged.Sort(StagedSubmissionComparer.Instance);

            var snapshot = RentFrozenSnapshot();
            if (snapshot.BufferCapacity < staged.SubmissionsCount)
                NoteAllocWarningIfNeeded(true);
            var buffer = snapshot.AcquireBuffer(staged.SubmissionsCount);

            for (int i = 0; i < staged.SubmissionsCount; i++)
            {
                var s = staged[i];
                int seq = NextSequenceForActor(frozenTick, s.Submission.ActorEntity);

                // Payload already fixed-layout struct; copy by value only.
                var frozenPayload = s.Submission.Payload;

                buffer[i] = new FrozenIntentRecord(
                    intentId: s.Submission.IntentId!,
                    intentType: s.Submission.IntentType,
                    actorEntity: s.Submission.ActorEntity,
                    submitTick: s.SubmitTick,
                    deterministicSequence: seq,
                    payload: frozenPayload
                );
            }

            snapshot.Commit(frozenTick, staged.SubmissionsCount);
            _currentFrozen = snapshot;
            _frozenSnapshotsByTick[frozenTick] = snapshot;
            _lastFrozenCount = staged.SubmissionsCount;

            _stagedBySubmitTick.Remove(sourceSubmitTick);
            staged.Reset();
            _stagingBucketPool.Return(staged);
        }

        private int NextSequenceForActor(int frozenTick, EntityHandle actor)
        {
            var key = (frozenTick, actor);
            if (!_sequenceCounters.TryGetValue(key, out int current))
                current = 0;

            current++;
            _sequenceCounters[key] = current;
            return current;
        }

        private void PruneStaging(int keepFromTickInclusive)
        {
            int count = _stagedBySubmitTick.Count;
            if (count == 0)
                return;

            var keys = ArrayPool<int>.Shared.Rent(count);
            int index = 0;
            foreach (var kvp in _stagedBySubmitTick)
                keys[index++] = kvp.Key;

            for (int i = 0; i < index; i++)
            {
                if (keys[i] < keepFromTickInclusive)
                {
                    if (_stagedBySubmitTick.TryGetValue(keys[i], out var bucket))
                    {
                        bucket.Reset();
                        _stagingBucketPool.Return(bucket);
                        _stagedBySubmitTick.Remove(keys[i]);
                    }
                }
            }

            ArrayPool<int>.Shared.Return(keys, clearArray: true);

            PruneFrozenSnapshots(keepFromTickInclusive);
            PruneSequenceCounters(keepFromTickInclusive);
        }

        private void PruneSequenceCounters(int keepFromTickInclusive)
        {
            int count = _sequenceCounters.Count;
            if (count == 0)
                return;

            var keys = ArrayPool<(int FrozenTick, EntityHandle Actor)>.Shared.Rent(count);
            int index = 0;
            foreach (var kvp in _sequenceCounters)
                keys[index++] = kvp.Key;

            for (int i = 0; i < index; i++)
            {
                if (keys[i].FrozenTick < keepFromTickInclusive)
                    _sequenceCounters.Remove(keys[i]);
            }

            ArrayPool<(int, EntityHandle)>.Shared.Return(keys, clearArray: true);
        }

        private void PruneFrozenSnapshots(int keepFromTickInclusive)
        {
            int count = _frozenSnapshotsByTick.Count;
            if (count == 0)
                return;

            var keys = ArrayPool<int>.Shared.Rent(count);
            int index = 0;
            foreach (var kvp in _frozenSnapshotsByTick)
                keys[index++] = kvp.Key;

            for (int i = 0; i < index; i++)
            {
                int tick = keys[i];
                if (tick < keepFromTickInclusive && _frozenSnapshotsByTick.TryGetValue(tick, out var snapshot))
                {
                    _frozenSnapshotsByTick.Remove(tick);
                    _frozenSnapshotPool.Return(snapshot);
                }
            }

            ArrayPool<int>.Shared.Return(keys, clearArray: true);
        }

        private readonly struct StagedSubmission
        {
            public readonly CombatIntentSubmission Submission;
            public readonly int SubmitTick;

            public StagedSubmission(CombatIntentSubmission submission, int submitTick)
            {
                Submission = submission;
                SubmitTick = submitTick;
            }
        }

        private sealed class StagingBucket
        {
            private readonly List<StagedSubmission> _submissions;
            private readonly Dictionary<EntityHandle, int> _actorCounts;

            public StagingBucket()
            {
                _submissions = new List<StagedSubmission>(SessionIntentCapPerTick);
                _actorCounts = new Dictionary<EntityHandle, int>(ActorCountCapacityHint);
            }

            public int SubmissionsCount => _submissions.Count;

            public StagedSubmission this[int index] => _submissions[index];

            public void Prepare(int sessionCap)
            {
                _submissions.Clear();
                _actorCounts.Clear();
                _submissions.EnsureCapacity(sessionCap);

            }

            public int GetActorCount(EntityHandle actor)
            {
                if (_actorCounts.TryGetValue(actor, out var count))
                    return count;

                return 0;
            }

            public void IncrementActor(EntityHandle actor)
            {
                if (_actorCounts.TryGetValue(actor, out var count))
                    _actorCounts[actor] = count + 1;
                else
                    _actorCounts[actor] = 1;
            }

            public void AddSubmission(StagedSubmission submission)
            {
                _submissions.Add(submission);
            }

            public void Sort(IComparer<StagedSubmission> comparer)
            {
                _submissions.Sort(comparer);
            }

            public void Reset()
            {
                _submissions.Clear();
                _actorCounts.Clear();
            }
        }

        private sealed class StagingBucketPool
        {
            private readonly Stack<StagingBucket> _pool = new Stack<StagingBucket>();
            private readonly int _maxSize;

            public StagingBucketPool(int maxSize)
            {
                _maxSize = maxSize;
            }

            public StagingBucket Rent(out bool allocatedNew)
            {
                if (_pool.Count > 0)
                {
                    allocatedNew = false;
                    return _pool.Pop();
                }

                allocatedNew = true;
                return new StagingBucket();
            }

            public void Return(StagingBucket bucket)
            {
                bucket.Reset();

                if (_pool.Count < _maxSize)
                    _pool.Push(bucket);
            }
        }

        private sealed class StagedSubmissionComparer : IComparer<StagedSubmission>
        {
            public static readonly StagedSubmissionComparer Instance = new StagedSubmissionComparer();

            public int Compare(StagedSubmission x, StagedSubmission y)
            {
                int actorCompare = x.Submission.ActorEntity.Value.CompareTo(y.Submission.ActorEntity.Value);
                if (actorCompare != 0)
                    return actorCompare;

                return string.CompareOrdinal(x.Submission.IntentId ?? string.Empty, y.Submission.IntentId ?? string.Empty);
            }
        }

        private enum OverflowPolicy
        {
            DropNewest,
            DropOldest
        }
    }

    // ---------------------------
    // Intake models + snapshots
    // ---------------------------

    public sealed class CombatIntentSubmission
    {
        public string? IntentId { get; init; }
        public CombatIntentType IntentType { get; init; }
        public EntityHandle ActorEntity { get; init; }

        // Optional per schema (correlation only; must not affect ordering)
        public string? ClientNonce { get; init; }

        // Fixed-layout payload (no dictionaries, no dynamic shapes).
        public CombatIntentPayload Payload { get; init; } = CombatIntentPayload.Empty;
    }

    public enum CombatIntentType
    {
        CombatAttackIntent,
        CombatDefendIntent,
        CombatAbilityIntent,
        CombatMovementIntent,
        CombatInteractIntent,
        CombatCancelIntent
    }

    public enum CombatMovementMode : byte
    {
        Unknown = 0,
        Translate = 1,
        Strafe = 2,
        Backstep = 3
    }

    public readonly struct CombatIntentPayload
    {
        public static CombatIntentPayload Empty => new CombatIntentPayload();

        public readonly CombatIntentType IntentType;
        public readonly AttackIntentPayload Attack;
        public readonly DefendIntentPayload Defend;
        public readonly AbilityIntentPayload Ability;
        public readonly MovementIntentPayload Movement;
        public readonly InteractIntentPayload Interact;
        public readonly CancelIntentPayload Cancel;

        private CombatIntentPayload(
            CombatIntentType intentType,
            AttackIntentPayload attack,
            DefendIntentPayload defend,
            AbilityIntentPayload ability,
            MovementIntentPayload movement,
            InteractIntentPayload interact,
            CancelIntentPayload cancel)
        {
            IntentType = intentType;
            Attack = attack;
            Defend = defend;
            Ability = ability;
            Movement = movement;
            Interact = interact;
            Cancel = cancel;
        }

        public static CombatIntentPayload ForAttack(in AttackIntentPayload payload)
        {
            return new CombatIntentPayload(CombatIntentType.CombatAttackIntent, payload, default, default, default, default, default);
        }

        public static CombatIntentPayload ForDefend(in DefendIntentPayload payload)
        {
            return new CombatIntentPayload(CombatIntentType.CombatDefendIntent, default, payload, default, default, default, default);
        }

        public static CombatIntentPayload ForAbility(in AbilityIntentPayload payload)
        {
            return new CombatIntentPayload(CombatIntentType.CombatAbilityIntent, default, default, payload, default, default, default);
        }

        public static CombatIntentPayload ForMovement(in MovementIntentPayload payload)
        {
            return new CombatIntentPayload(CombatIntentType.CombatMovementIntent, default, default, default, payload, default, default);
        }

        public static CombatIntentPayload ForInteract(in InteractIntentPayload payload)
        {
            return new CombatIntentPayload(CombatIntentType.CombatInteractIntent, default, default, default, default, payload, default);
        }

        public static CombatIntentPayload ForCancel(in CancelIntentPayload payload)
        {
            return new CombatIntentPayload(CombatIntentType.CombatCancelIntent, default, default, default, default, default, payload);
        }
    }

    public readonly struct OptionalString
    {
        public readonly string? Value;

        public OptionalString(string? value)
        {
            if (string.IsNullOrWhiteSpace(value))
            {
                Value = null;
            }
            else
            {
                Value = value;
            }
        }

        public bool HasValue => Value != null;
    }

    public readonly struct OptionalEntityHandle
    {
        public readonly EntityHandle Value;
        public readonly bool HasValue;

        public OptionalEntityHandle(EntityHandle value)
        {
            Value = value;
            HasValue = value.IsValid;
        }
    }

    public readonly struct AttackIntentPayload
    {
        public readonly OptionalEntityHandle TargetEntity;
        public readonly OptionalString AttackProfileKey;

        public AttackIntentPayload(OptionalEntityHandle targetEntity, OptionalString attackProfileKey)
        {
            TargetEntity = targetEntity;
            AttackProfileKey = attackProfileKey;
        }
    }

    public readonly struct DefendIntentPayload
    {
        public readonly OptionalString DefendProfileKey;

        public DefendIntentPayload(OptionalString defendProfileKey)
        {
            DefendProfileKey = defendProfileKey;
        }
    }

    public readonly struct AbilityIntentPayload
    {
        public readonly string AbilityKey;
        public readonly OptionalEntityHandle TargetEntity;
        public readonly IdentifierContext AbilityContext;
        public readonly bool HasAbilityContext;

        public AbilityIntentPayload(string abilityKey, OptionalEntityHandle targetEntity, IdentifierContext abilityContext, bool hasAbilityContext)
        {
            AbilityKey = abilityKey ?? string.Empty;
            TargetEntity = targetEntity;
            AbilityContext = abilityContext;
            HasAbilityContext = hasAbilityContext;
        }
    }

    public readonly struct MovementIntentPayload
    {
        public readonly CombatMovementMode MovementMode;
        public readonly OptionalEntityHandle TargetEntity;
        public readonly IdentifierContext MovementContext;
        public readonly bool HasMovementContext;

        public MovementIntentPayload(CombatMovementMode movementMode, OptionalEntityHandle targetEntity, IdentifierContext movementContext, bool hasMovementContext)
        {
            MovementMode = movementMode;
            TargetEntity = targetEntity;
            MovementContext = movementContext;
            HasMovementContext = hasMovementContext;
        }
    }

    public readonly struct InteractIntentPayload
    {
        public readonly string InteractableId;
        public readonly OptionalString InteractionKind;

        public InteractIntentPayload(string interactableId, OptionalString interactionKind)
        {
            InteractableId = interactableId ?? string.Empty;
            InteractionKind = interactionKind;
        }
    }

    public readonly struct CancelIntentPayload
    {
        public readonly string CancelTargetIntentId;
        public readonly OptionalString CancelReason;

        public CancelIntentPayload(string cancelTargetIntentId, OptionalString cancelReason)
        {
            CancelTargetIntentId = cancelTargetIntentId ?? string.Empty;
            CancelReason = cancelReason;
        }
    }

    public readonly struct IdentifierContext
    {
        private const int MaxEntries = 4;

        private readonly ContextEntry _entry0;
        private readonly ContextEntry _entry1;
        private readonly ContextEntry _entry2;
        private readonly ContextEntry _entry3;
        private readonly byte _count;

        public IdentifierContext(ContextEntry entry0, ContextEntry entry1, ContextEntry entry2, ContextEntry entry3, byte count)
        {
            _entry0 = entry0;
            _entry1 = entry1;
            _entry2 = entry2;
            _entry3 = entry3;
            _count = count;
        }

        public int Count => _count;

        public ContextEntry this[int index]
        {
            get
            {
                return index switch
                {
                    0 when _count > 0 => _entry0,
                    1 when _count > 1 => _entry1,
                    2 when _count > 2 => _entry2,
                    3 when _count > 3 => _entry3,
                    _ => throw new ArgumentOutOfRangeException(nameof(index))
                };
            }
        }

        public static IdentifierContext Empty => new IdentifierContext(default, default, default, default, 0);

        public IdentifierContextBuilder ToBuilder()
        {
            var builder = new IdentifierContextBuilder();
            for (int i = 0; i < _count; i++)
            {
                var entry = this[i];
                builder.TryAdd(entry.Key, entry.Value);
            }

            return builder;
        }

        public readonly struct IdentifierContextBuilder
        {
            private ContextEntry _builderEntry0;
            private ContextEntry _builderEntry1;
            private ContextEntry _builderEntry2;
            private ContextEntry _builderEntry3;
            private byte _builderCount;

            public bool TryAdd(string key, string value)
            {
                if (string.IsNullOrWhiteSpace(key) || string.IsNullOrWhiteSpace(value))
                    return false;

                if (_builderCount >= MaxEntries)
                    return false;

                var entry = new ContextEntry(key, value);
                switch (_builderCount)
                {
                    case 0:
                        _builderEntry0 = entry;
                        break;
                    case 1:
                        _builderEntry1 = entry;
                        break;
                    case 2:
                        _builderEntry2 = entry;
                        break;
                    case 3:
                        _builderEntry3 = entry;
                        break;
                }

                _builderCount++;
                return true;
            }

            public IdentifierContext Build()
            {
                return new IdentifierContext(_builderEntry0, _builderEntry1, _builderEntry2, _builderEntry3, _builderCount);
            }
        }
    }

    public readonly struct ContextEntry
    {
        public readonly string Key;
        public readonly string Value;

        public ContextEntry(string key, string value)
        {
            Key = key ?? string.Empty;
            Value = value ?? string.Empty;
        }
    }

    public sealed class FrozenQueueSnapshot
    {
        private FrozenIntentRecord[] _buffer;
        private int _count;
        private readonly FrozenIntentList _intentList;

        public int AuthoritativeTick { get; private set; }
        public IReadOnlyList<FrozenIntentRecord> Intents => _intentList;
        internal int BufferCapacity => _buffer.Length;

        private FrozenQueueSnapshot()
        {
            _buffer = Array.Empty<FrozenIntentRecord>();
            _intentList = new FrozenIntentList();
        }

        internal FrozenIntentRecord[] AcquireBuffer(int requiredCapacity)
        {
            if (_buffer.Length < requiredCapacity)
            {
                if (_buffer.Length > 0)
                    ArrayPool<FrozenIntentRecord>.Shared.Return(_buffer, clearArray: true);

                _buffer = ArrayPool<FrozenIntentRecord>.Shared.Rent(requiredCapacity);
            }

            return _buffer;
        }

        internal void Commit(int authoritativeTick, int count)
        {
            AuthoritativeTick = authoritativeTick;
            _count = count;
            _intentList.Reset(_buffer, _count);
        }

        internal void Reset()
        {
            if (_buffer.Length > 0)
            {
                ArrayPool<FrozenIntentRecord>.Shared.Return(_buffer, clearArray: true);
                _buffer = Array.Empty<FrozenIntentRecord>();
            }

            _count = 0;
            AuthoritativeTick = 0;
            _intentList.Reset(Array.Empty<FrozenIntentRecord>(), 0);
        }

        public static FrozenQueueSnapshot Empty(int tick)
        {
            var snapshot = new FrozenQueueSnapshot();
            snapshot.Commit(tick, 0);
            return snapshot;
        }
    }

    internal sealed class FrozenQueueSnapshotPool
    {
        private readonly Stack<FrozenQueueSnapshot> _pool = new Stack<FrozenQueueSnapshot>();
        private readonly int _maxSize;

        public FrozenQueueSnapshotPool(int maxSize)
        {
            _maxSize = maxSize;
        }

        public FrozenQueueSnapshot Rent(out bool allocatedNew)
        {
            if (_pool.Count > 0)
            {
                allocatedNew = false;
                return _pool.Pop();
            }

            allocatedNew = true;
            return new FrozenQueueSnapshot();
        }

        public void Return(FrozenQueueSnapshot snapshot)
        {
            snapshot.Reset();
            if (_pool.Count < _maxSize)
                _pool.Push(snapshot);
        }
    }

    public readonly struct FrozenIntentRecord
    {
        public readonly string IntentId;
        public readonly CombatIntentType IntentType;
        public readonly EntityHandle ActorEntity;
        public readonly int SubmitTick;

        // Deterministic tie-breaker for per-actor intent ordering within the frozen tick.
        public readonly int DeterministicSequence;

        // Immutable, read-only payload as frozen at tick boundary.
        public readonly CombatIntentPayload Payload;

        public FrozenIntentRecord(
            string intentId,
            CombatIntentType intentType,
            EntityHandle actorEntity,
            int submitTick,
            int deterministicSequence,
            CombatIntentPayload payload)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntity = actorEntity;
            SubmitTick = submitTick;
            DeterministicSequence = deterministicSequence;
            Payload = payload;
        }
    }

    internal sealed class FrozenIntentList : IReadOnlyList<FrozenIntentRecord>
    {
        private FrozenIntentRecord[] _items = Array.Empty<FrozenIntentRecord>();
        private int _count;

        public FrozenIntentRecord this[int index]
        {
            get
            {
                if ((uint)index >= (uint)_count)
                    throw new ArgumentOutOfRangeException(nameof(index));

                return _items[index];
            }
        }

        public int Count => _count;

        public void Reset(FrozenIntentRecord[] items, int count)
        {
            _items = items;
            _count = count;
        }

        public Enumerator GetEnumerator() => new Enumerator(_items, _count);

        IEnumerator<FrozenIntentRecord> IEnumerable<FrozenIntentRecord>.GetEnumerator() => GetEnumerator();

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        public struct Enumerator : IEnumerator<FrozenIntentRecord>
        {
            private readonly FrozenIntentRecord[] _items;
            private readonly int _count;
            private int _index;

            public Enumerator(FrozenIntentRecord[] items, int count)
            {
                _items = items;
                _count = count;
                _index = -1;
            }

            public FrozenIntentRecord Current => _items[_index];

            object IEnumerator.Current => Current;

            public void Dispose()
            {
            }

            public bool MoveNext()
            {
                int next = _index + 1;
                if (next >= _count)
                    return false;

                _index = next;
                return true;
            }

            public void Reset()
            {
                _index = -1;
            }
        }
    }

    public readonly struct FrozenIntentBatch : IReadOnlyList<FrozenIntentRecord>
    {
        private readonly IReadOnlyList<FrozenIntentRecord>? _sourceList;
        private readonly FrozenIntentRecord[]? _buffer;

        public int AuthoritativeTick { get; }
        public int Count { get; }

        public FrozenIntentRecord this[int index]
        {
            get
            {
                if ((uint)index >= (uint)Count)
                    throw new ArgumentOutOfRangeException(nameof(index));

                if (_buffer != null)
                    return _buffer[index];

                return _sourceList![index];
            }
        }

        public FrozenIntentBatch(int authoritativeTick, IReadOnlyList<FrozenIntentRecord> intents)
        {
            AuthoritativeTick = authoritativeTick;
            _sourceList = intents ?? throw new ArgumentNullException(nameof(intents));
            _buffer = null;
            Count = intents.Count;
        }

        public FrozenIntentBatch(int authoritativeTick, FrozenIntentRecord[] buffer, int count)
        {
            if (buffer == null) throw new ArgumentNullException(nameof(buffer));
            if (count < 0 || count > buffer.Length) throw new ArgumentOutOfRangeException(nameof(count));

            AuthoritativeTick = authoritativeTick;
            _buffer = buffer;
            _sourceList = null;
            Count = count;
        }

        public Enumerator GetEnumerator() => new Enumerator(this);

        IEnumerator<FrozenIntentRecord> IEnumerable<FrozenIntentRecord>.GetEnumerator() => GetEnumerator();

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        public struct Enumerator : IEnumerator<FrozenIntentRecord>
        {
            private readonly FrozenIntentBatch _owner;
            private int _index;

            public Enumerator(FrozenIntentBatch owner)
            {
                _owner = owner;
                _index = -1;
            }

            public FrozenIntentRecord Current => _owner[_index];

            object IEnumerator.Current => Current;

            public void Dispose()
            {
            }

            public bool MoveNext()
            {
                int next = _index + 1;
                if (next >= _owner.Count)
                    return false;

                _index = next;
                return true;
            }

            public void Reset()
            {
                _index = -1;
            }
        }
    }

    // Deterministic validation snapshot for the harness.
    public sealed class CombatIntentQueueValidationSnapshot
    {
        public int AuthoritativeTick { get; }
        public IReadOnlyList<CombatIntentQueueValidationRow> Intents { get; }

        private CombatIntentQueueValidationSnapshot(int authoritativeTick, IReadOnlyList<CombatIntentQueueValidationRow> intents)
        {
            AuthoritativeTick = authoritativeTick;
            Intents = intents;
        }

        public static CombatIntentQueueValidationSnapshot FromFrozen(FrozenQueueSnapshot frozen)
        {
            var rows = new CombatIntentQueueValidationRow[frozen.Intents.Count];
            for (int i = 0; i < frozen.Intents.Count; i++)
            {
                var intent = frozen.Intents[i];
                rows[i] = new CombatIntentQueueValidationRow(
                    intentId: intent.IntentId,
                    intentType: intent.IntentType,
                    actorEntity: intent.ActorEntity,
                    submitTick: intent.SubmitTick,
                    deterministicSequence: intent.DeterministicSequence);
            }

            return new CombatIntentQueueValidationSnapshot(frozen.AuthoritativeTick, rows);
        }
    }

    public readonly struct CombatIntentQueueValidationRow
    {
        public readonly string IntentId;
        public readonly CombatIntentType IntentType;
        public readonly EntityHandle ActorEntity;
        public readonly int SubmitTick;
        public readonly int DeterministicSequence;

        public CombatIntentQueueValidationRow(
            string intentId,
            CombatIntentType intentType,
            EntityHandle actorEntity,
            int submitTick,
            int deterministicSequence)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntity = actorEntity;
            SubmitTick = submitTick;
            DeterministicSequence = deterministicSequence;
        }
    }

    // ---------------------------
    // Observable rejections
    // ---------------------------

    public sealed class IntentRejection
    {
        public string IntentId { get; }
        public EntityHandle ActorEntity { get; }
        public CombatIntentType IntentType { get; }
        public int AuthoritativeTick { get; }
        public string ReasonCode { get; }

        public IntentRejection(string intentId, EntityHandle actorEntity, CombatIntentType intentType, int authoritativeTick, string reasonCode)
        {
            IntentId = intentId;
            ActorEntity = actorEntity;
            IntentType = intentType;
            AuthoritativeTick = authoritativeTick;
            ReasonCode = reasonCode;
        }
    }

    public interface IIntentRejectionSink
    {
        void OnRejected(IntentRejection rejection);
    }

    public static class RejectReasonCodes
    {
        public const string MissingRequiredField = "MissingRequiredField";
        public const string InvalidIntentType = "InvalidIntentType";
        public const string InvalidEntityId = "InvalidEntityId";
        public const string ForbiddenFieldPresent = "ForbiddenFieldPresent";
        public const string InvalidContextValue = "InvalidContextValue";
        public const string InvalidMovementMode = "InvalidMovementMode";
        public const string InvalidPayloadShape = "InvalidPayloadShape";
        public const string OverflowSessionIntentCap = "OverflowSessionIntentCap";
        public const string OverflowActorIntentCap = "OverflowActorIntentCap";
    }

    public readonly struct IntakeReceipt
    {
        public readonly string IntentId;
        public readonly int SubmitTick;
        public readonly bool IsRejected;
        public readonly string ReasonCode;

        private IntakeReceipt(string intentId, int submitTick, bool isRejected, string reasonCode)
        {
            IntentId = intentId;
            SubmitTick = submitTick;
            IsRejected = isRejected;
            ReasonCode = reasonCode;
        }

        public static IntakeReceipt Staged(string intentId, int submitTick) =>
            new IntakeReceipt(intentId, submitTick, isRejected: false, reasonCode: string.Empty);

        public static IntakeReceipt Rejected(string intentId, int submitTick, string reasonCode) =>
            new IntakeReceipt(intentId, submitTick, isRejected: true, reasonCode: reasonCode);
    }

    public readonly struct CombatIntentQueueDiagnosticsSnapshot
    {
        public readonly long StructuralRejectCount;
        public readonly long OverflowRejectCount;
        public readonly long CombatIntentsStaged;
        public readonly long CombatIntentsDropped;
        public readonly long CombatAllocWarnings;
        public readonly int PeakStagingUsage;
        public readonly int LastFrozenCount;

        public CombatIntentQueueDiagnosticsSnapshot(
            long structuralRejectCount,
            long overflowRejectCount,
            long combatIntentsStaged,
            long combatIntentsDropped,
            long combatAllocWarnings,
            int peakStagingUsage,
            int lastFrozenCount)
        {
            StructuralRejectCount = structuralRejectCount;
            OverflowRejectCount = overflowRejectCount;
            CombatIntentsStaged = combatIntentsStaged;
            CombatIntentsDropped = combatIntentsDropped;
            CombatAllocWarnings = combatAllocWarnings;
            PeakStagingUsage = peakStagingUsage;
            LastFrozenCount = lastFrozenCount;
        }
    }

    // ---------------------------
    // Tick + entity id validation abstractions
    // ---------------------------

    public interface ITickSource
    {
        int CurrentTick { get; }
        event Action<int> OnTickAdvanced; // newTick
    }

    public interface IEntityIdValidator
    {
        bool IsValidEntityId(string entityId);
        bool IsValidInteractableId(string interactableId);
    }

    // ---------------------------
    // Structural schema validation (Stage 11.2 only)
    // ---------------------------

    internal static class CombatIntentStructuralValidator
    {
        public static bool TryValidate(
            CombatIntentSubmission submission,
            IEntityIdValidator entityIdValidator,
            out RejectInfo reject)
        {
            reject = default;

            if (string.IsNullOrWhiteSpace(submission.IntentId))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "intent_id missing.");
                return false;
            }

            if (!submission.ActorEntity.IsValid)
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "actor_entity missing.");
                return false;
            }

            if (submission.Payload.IntentType != submission.IntentType)
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidIntentType, "payload intent_type mismatch.");
                return false;
            }

            switch (submission.IntentType)
            {
                case CombatIntentType.CombatAttackIntent:
                    return ValidateAttack(submission, entityIdValidator, out reject);

                case CombatIntentType.CombatDefendIntent:
                    return ValidateDefend(submission, out reject);

                case CombatIntentType.CombatAbilityIntent:
                    return ValidateAbility(submission, entityIdValidator, out reject);

                case CombatIntentType.CombatMovementIntent:
                    return ValidateMovement(submission, entityIdValidator, out reject);

                case CombatIntentType.CombatInteractIntent:
                    return ValidateInteract(submission, entityIdValidator, out reject);

                case CombatIntentType.CombatCancelIntent:
                    return ValidateCancel(submission, out reject);

                default:
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidIntentType, "Unknown intent type.");
                    return false;
            }
        }

        private static bool ValidateAttack(CombatIntentSubmission s, IEntityIdValidator v, out RejectInfo reject)
        {
            reject = default;
            var payload = s.Payload.Attack;

            if (payload.TargetEntity.HasValue)
            {
                if (!payload.TargetEntity.Value.IsValid)
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "target_entity_id invalid.");
                    return false;
                }
            }

            if (payload.AttackProfileKey.HasValue && string.IsNullOrWhiteSpace(payload.AttackProfileKey.Value))
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "attack_profile_key invalid.");
                return false;
            }

            return true;
        }

        private static bool ValidateDefend(CombatIntentSubmission s, out RejectInfo reject)
        {
            reject = default;
            var payload = s.Payload.Defend;

            if (payload.DefendProfileKey.HasValue && string.IsNullOrWhiteSpace(payload.DefendProfileKey.Value))
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "defend_profile_key invalid.");
                return false;
            }

            return true;
        }

        private static bool ValidateAbility(CombatIntentSubmission s, IEntityIdValidator v, out RejectInfo reject)
        {
            reject = default;
            var payload = s.Payload.Ability;

            if (string.IsNullOrWhiteSpace(payload.AbilityKey))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "ability_key missing.");
                return false;
            }

            if (payload.TargetEntity.HasValue)
            {
                if (!payload.TargetEntity.Value.IsValid)
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "target_entity_id invalid.");
                    return false;
                }
            }

            if (payload.HasAbilityContext && !IsValidIdentifierContext(payload.AbilityContext))
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidContextValue, "ability_context must be identifiers-only.");
                return false;
            }

            return true;
        }

        private static bool ValidateMovement(CombatIntentSubmission s, IEntityIdValidator v, out RejectInfo reject)
        {
            reject = default;
            var payload = s.Payload.Movement;

            if (payload.MovementMode == CombatMovementMode.Unknown)
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "movement_mode missing.");
                return false;
            }

            if (payload.MovementMode != CombatMovementMode.Translate &&
                payload.MovementMode != CombatMovementMode.Strafe &&
                payload.MovementMode != CombatMovementMode.Backstep)
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidMovementMode, "movement_mode invalid.");
                return false;
            }

            if (payload.TargetEntity.HasValue)
            {
                if (!payload.TargetEntity.Value.IsValid)
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "target_entity_id invalid.");
                    return false;
                }
            }

            if (payload.HasMovementContext && !IsValidIdentifierContext(payload.MovementContext))
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidContextValue, "movement_context must be identifiers-only.");
                return false;
            }

            return true;
        }

        private static bool ValidateInteract(CombatIntentSubmission s, IEntityIdValidator v, out RejectInfo reject)
        {
            reject = default;
            var payload = s.Payload.Interact;

            if (string.IsNullOrWhiteSpace(payload.InteractableId))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "interactable_id missing.");
                return false;
            }

            if (!v.IsValidInteractableId(payload.InteractableId))
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "interactable_id invalid.");
                return false;
            }

            return true;
        }

        private static bool ValidateCancel(CombatIntentSubmission s, out RejectInfo reject)
        {
            reject = default;
            var payload = s.Payload.Cancel;

            if (string.IsNullOrWhiteSpace(payload.CancelTargetIntentId))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "cancel_target_intent_id missing.");
                return false;
            }

            if (payload.CancelReason.HasValue && string.IsNullOrWhiteSpace(payload.CancelReason.Value))
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "cancel_reason invalid.");
                return false;
            }

            return true;
        }

        private static bool IsValidIdentifierContext(IdentifierContext ctx)
        {
            for (int i = 0; i < ctx.Count; i++)
            {
                var entry = ctx[i];
                if (string.IsNullOrWhiteSpace(entry.Key) || string.IsNullOrWhiteSpace(entry.Value))
                    return false;
            }

            return true;
        }

        internal readonly struct RejectInfo
        {
            public readonly string ReasonCode;
            public readonly string Details;

            private RejectInfo(string reasonCode, string details)
            {
                ReasonCode = reasonCode;
                Details = details;
            }

            public static RejectInfo Of(string reasonCode, string details) => new RejectInfo(reasonCode, details);
        }
    }
}
