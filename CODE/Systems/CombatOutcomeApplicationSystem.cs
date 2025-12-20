// CombatOutcomeApplicationSystem.cs
// NOTE: Save location must follow existing project structure.
// Implements CombatOutcomeApplicationSystem only.
// No intent validation, no intent resolution, no damage/mitigation calculation, no persistence I/O.

using System;
using System.Buffers;
using System.Collections.Generic;
using System.Threading;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Tick;

namespace Caelmor.Combat
{
    /// <summary>
    /// CombatOutcomeApplicationSystem
    ///
    /// Responsibilities:
    /// - Consume resolved outcome records (IntentResult + DamageOutcome + MitigationOutcome)
    /// - Apply outcomes exactly once (idempotent per tick)
    /// - Mutate combat-related authoritative state ONLY (CombatEntityState via provided state writer)
    /// - Emit CombatEvents ONLY after application
    /// - Request persistence checkpoints (request-only; no persistence writes)
    /// - Expose post-application validation snapshots
    ///
    /// Hard non-responsibilities:
    /// - Does not resolve intents
    /// - Does not reorder outcomes
    /// - Does not validate intent legality
    /// - Does not calculate damage or mitigation
    /// - Does not read from persistence
    /// - Does not auto-repair or silently clamp
    /// </summary>
    // IL2CPP/AOT SAFETY: No runtime code generation or Reflection.Emit permitted. Any reflection-based access must
    // be explicitly preserved for managed stripping (none present); keep tick-thread hot paths deterministic and
    // free of editor-only APIs.
    public sealed class CombatOutcomeApplicationSystem
    {
        private readonly ITickSource _tickSource;
        private readonly ICombatStateWriter _stateWriter;
        private readonly ICombatEventSink _eventSink;
        private readonly ICheckpointRequester _checkpointRequester;

        // Idempotence guard: applied payload IDs are scoped per authoritative tick.
        // Not global across session; not persisted.
        private readonly Dictionary<int, AppliedIdSet> _appliedPayloadIdsByTick = new(8);
        private readonly Stack<AppliedIdSet> _appliedPayloadIdPool = new(8);
        private readonly HashSet<ulong> _duplicateCheckSet = new();

        private const int MaxTrackedPayloadIdsPerTick = 4096;
        private const int AppliedIdSetPoolCapacity = 8;

        // Counters (monotonic).
        private long _combatOutcomesApplied;
        private long _combatDuplicateOutcomesRejected;
        private long _combatIdempotenceOverflow;
        private long _combatEventsCreated;

        // Validation support: last resolved intent per entity (snapshot-only; not authoritative gameplay state).
        private readonly Dictionary<EntityHandle, string> _lastResolvedIntentIdByEntity =
            new Dictionary<EntityHandle, string>();

        public CombatOutcomeApplicationSystem(
            ITickSource tickSource,
            ICombatStateWriter stateWriter,
            ICombatEventSink eventSink,
            ICheckpointRequester checkpointRequester)
        {
            _tickSource = tickSource ?? throw new ArgumentNullException(nameof(tickSource));
            _stateWriter = stateWriter ?? throw new ArgumentNullException(nameof(stateWriter));
            _eventSink = eventSink ?? throw new ArgumentNullException(nameof(eventSink));
            _checkpointRequester = checkpointRequester ?? throw new ArgumentNullException(nameof(checkpointRequester));
        }

        /// <summary>
        /// Applies a resolved batch for a single authoritative tick.
        /// Ordering must be the provided ordering; this system never reorders.
        /// </summary>
        public CombatApplicationResult Apply(CombatOutcomeBatch batch)
        {
            TickThreadAssert.AssertTickThread();
            if (batch == null) throw new ArgumentNullException(nameof(batch));

            int nowTick = _tickSource.CurrentTick;
            if (batch.AuthoritativeTick != nowTick)
                throw new InvalidOperationException($"Outcome batch tick mismatch. batch={batch.AuthoritativeTick} now={nowTick}");

            // Defensive: ensure payload identifiers are unique WITHIN this batch (fail-loud).
            // Idempotence is for repeated application attempts of the SAME batch, not for ambiguous duplicates inside one call.
            EnsureNoDuplicateIdsInBatchOrThrow(batch);

            var appliedSet = GetOrCreateAppliedSetForTick(nowTick);

            // Pre-application snapshot (validation harness support)
            var pre = _stateWriter.CaptureWorldValidationSnapshot(
                authoritativeTick: nowTick,
                lastResolvedIntentByEntity: _lastResolvedIntentIdByEntity);

            // Apply in canonical order: IntentResults first, then Damage/Mitigation, then any explicit StateChanges (if provided).
            // NOTE: We do not invent resolution math. We only apply declared results deterministically.

            int appliedCount = 0;

            // 1) Apply IntentResults (may mutate CombatEntityState only, if and only if the result dictates a transition).
            for (int i = 0; i < batch.IntentResultsInOrder.Count; i++)
            {
                var r = batch.IntentResultsInOrder[i];

                ulong payloadId = PayloadId.IntentResult(r.IntentIdKey);
                if (!TryRegisterPayloadId(appliedSet, payloadId))
                    continue; // idempotent: already applied this payload for this tick

                ApplyIntentResultStateEffectsOrThrow(r);

                var combatEvent = CombatEvent.CreateIntentResultEvent(
                    authoritativeTick: nowTick,
                    combatContextId: batch.CombatContextId,
                    subjectEntity: r.ActorEntity,
                    intentResult: r,
                    payloadId: payloadId);
                Interlocked.Increment(ref _combatEventsCreated);
                EmitEventAfterApply(combatEvent);

                appliedCount++;
            }

            // 2) Apply DamageOutcomes (no combat state fields exist for HP here; this system does not invent them).
            for (int i = 0; i < batch.DamageOutcomesInOrder.Count; i++)
            {
                var d = batch.DamageOutcomesInOrder[i];

                ulong payloadId = PayloadId.DamageOutcome(d.OutcomeId);
                if (!TryRegisterPayloadId(appliedSet, payloadId))
                    continue;

                var combatEvent = CombatEvent.CreateDamageOutcomeEvent(
                    authoritativeTick: nowTick,
                    combatContextId: batch.CombatContextId,
                    subjectEntity: d.TargetEntity,
                    damageOutcome: d,
                    payloadId: payloadId);
                Interlocked.Increment(ref _combatEventsCreated);
                EmitEventAfterApply(combatEvent);

                appliedCount++;
            }

            // 3) Apply MitigationOutcomes (no mutation; broadcast reflects applied results).
            for (int i = 0; i < batch.MitigationOutcomesInOrder.Count; i++)
            {
                var m = batch.MitigationOutcomesInOrder[i];

                ulong payloadId = PayloadId.MitigationOutcome(m.OutcomeId);
                if (!TryRegisterPayloadId(appliedSet, payloadId))
                    continue;

                var combatEvent = CombatEvent.CreateMitigationOutcomeEvent(
                    authoritativeTick: nowTick,
                    combatContextId: batch.CombatContextId,
                    subjectEntity: m.TargetEntity,
                    mitigationOutcome: m,
                    payloadId: payloadId);
                Interlocked.Increment(ref _combatEventsCreated);
                EmitEventAfterApply(combatEvent);

                appliedCount++;
            }

            // 4) Apply explicit state changes (if provided by upstream systems).
            // This is the only allowed mechanism here to enter Restricted/Incapacitated/Recovery transitions
            // without inventing logic in this system.
            for (int i = 0; i < batch.StateChangesInOrder.Count; i++)
            {
                var sc = batch.StateChangesInOrder[i];

                ulong payloadId = PayloadId.StateChange(sc.Entity.Value, sc.Kind);
                if (!TryRegisterPayloadId(appliedSet, payloadId))
                    continue;

                _stateWriter.ApplyStateChange(sc);

                // After mutation, emit state snapshot event reflecting applied state.
                var state = _stateWriter.GetState(sc.Entity);

                var combatEvent = CombatEvent.CreateStateChangeEvent(
                    authoritativeTick: nowTick,
                    combatContextId: batch.CombatContextId,
                    subjectEntity: sc.Entity,
                    stateSnapshot: state,
                    payloadId: payloadId);
                Interlocked.Increment(ref _combatEventsCreated);
                EmitEventAfterApply(combatEvent);

                appliedCount++;
            }

            // Request checkpoint at the valid boundary (request-only).
            // Only request if we actually applied something new for this tick.
            if (appliedCount > 0)
                _checkpointRequester.RequestCheckpoint(nowTick);

            if (appliedCount > 0)
                Interlocked.Add(ref _combatOutcomesApplied, appliedCount);

            // Post-application snapshot (validation harness support)
            var post = _stateWriter.CaptureWorldValidationSnapshot(
                authoritativeTick: nowTick,
                lastResolvedIntentByEntity: _lastResolvedIntentIdByEntity);

            // Runtime hygiene: keep idempotence sets bounded.
            PruneAppliedSets(keepFromTickInclusive: nowTick - 4);

            return new CombatApplicationResult(
                authoritativeTick: nowTick,
                appliedPayloadCount: appliedCount,
                preApplicationSnapshot: pre,
                postApplicationSnapshot: post);
        }

        // ---------------------------
        // IntentResult state effects
        // ---------------------------

        private void ApplyIntentResultStateEffectsOrThrow(IntentResult r)
        {
            if (r == null) throw new ArgumentNullException(nameof(r));
            if (string.IsNullOrWhiteSpace(r.IntentId)) throw new InvalidOperationException("IntentResult.intent_id missing.");
            if (!r.ActorEntity.IsValid) throw new InvalidOperationException("IntentResult.actor_entity missing.");

            // This system applies RESOLVED RESULTS only.
            // "Accepted" at this stage is an upstream contract violation.
            if (r.ResultStatus == IntentResultStatus.Accepted)
                throw new InvalidOperationException("IntentResult with status=Accepted is not valid for application.");

            // Rejected: MUST NOT mutate state (Stage 12.2 already guaranteed no mutation on reject).
            if (r.ResultStatus == IntentResultStatus.Rejected)
                return;

            // Resolved / Canceled:
            // Apply only the minimal canonical state clearing that is schema-supported:
            // - If entity is CombatActing or CombatDefending AND committed_intent_id matches this intent,
            //   transition back to CombatEngaged (committed cleared).
            // - Otherwise, do not invent transitions; fail-loud if the committed intent mismatches the state.
            var state = _stateWriter.GetState(r.ActorEntity);

            if (state.State == CombatState.CombatActing || state.State == CombatState.CombatDefending)
            {
                if (!string.Equals(state.CommittedIntentId, r.IntentId, StringComparison.Ordinal))
                    throw new InvalidOperationException(
                        $"Committed intent mismatch for entity {r.ActorEntity.Value}. state.committed={state.CommittedIntentId} result.intent={r.IntentId}");

                // Transition back to engaged (no new combat_context_id invented here).
                _stateWriter.ApplyStateChange(CombatStateChange.ToEngaged(r.ActorEntity, state.CombatContextId));

                // Snapshot-only helper for validation
                _lastResolvedIntentIdByEntity[r.ActorEntity] = r.IntentId;

                return;
            }

            // If not Acting/Defending, we do not invent any state mutation here.
            // Resolution may still be meaningful (e.g., movement/interaction outcomes),
            // but those effects are not represented in CombatEntityState schema.
            _lastResolvedIntentIdByEntity[r.ActorEntity] = r.IntentId;
        }

        // ---------------------------
        // Events
        // ---------------------------

        private void EmitEventAfterApply(CombatEvent e)
        {
            if (e == null) throw new ArgumentNullException(nameof(e));

            // Event emission occurs strictly after application in this method.
            _eventSink.Emit(e);
        }

        // ---------------------------
        // Idempotence + hygiene
        // ---------------------------

        private AppliedIdSet GetOrCreateAppliedSetForTick(int tick)
        {
            if (_appliedPayloadIdsByTick.TryGetValue(tick, out var set))
                return set;

            var rented = RentAppliedIdSet();
            _appliedPayloadIdsByTick.Add(tick, rented);
            return rented;
        }

        private void PruneAppliedSets(int keepFromTickInclusive)
        {
            int count = _appliedPayloadIdsByTick.Count;
            if (count == 0)
                return;

            var keys = ArrayPool<int>.Shared.Rent(count);
            int index = 0;
            foreach (var kvp in _appliedPayloadIdsByTick)
                keys[index++] = kvp.Key;

            for (int i = 0; i < index; i++)
            {
                if (keys[i] < keepFromTickInclusive && _appliedPayloadIdsByTick.TryGetValue(keys[i], out var set))
                {
                    _appliedPayloadIdsByTick.Remove(keys[i]);
                    ReturnAppliedIdSet(set);
                }
            }

            ArrayPool<int>.Shared.Return(keys, clearArray: true);
        }

        private void EnsureNoDuplicateIdsInBatchOrThrow(CombatOutcomeBatch batch)
        {
            _duplicateCheckSet.Clear();

            for (int i = 0; i < batch.IntentResultsInOrder.Count; i++)
            {
                var r = batch.IntentResultsInOrder[i];
                ulong id = PayloadId.IntentResult(r.IntentIdKey);
                if (!_duplicateCheckSet.Add(id))
                {
                    Interlocked.Increment(ref _combatDuplicateOutcomesRejected);
                    throw new InvalidOperationException($"Duplicate IntentResult payload in batch: {r.IntentId}");
                }
            }

            for (int i = 0; i < batch.DamageOutcomesInOrder.Count; i++)
            {
                var d = batch.DamageOutcomesInOrder[i];
                ulong id = PayloadId.DamageOutcome(d.OutcomeId);
                if (!_duplicateCheckSet.Add(id))
                {
                    Interlocked.Increment(ref _combatDuplicateOutcomesRejected);
                    throw new InvalidOperationException($"Duplicate DamageOutcome payload in batch: {d.OutcomeId}");
                }
            }

            for (int i = 0; i < batch.MitigationOutcomesInOrder.Count; i++)
            {
                var m = batch.MitigationOutcomesInOrder[i];
                ulong id = PayloadId.MitigationOutcome(m.OutcomeId);
                if (!_duplicateCheckSet.Add(id))
                {
                    Interlocked.Increment(ref _combatDuplicateOutcomesRejected);
                    throw new InvalidOperationException($"Duplicate MitigationOutcome payload in batch: {m.OutcomeId}");
                }
            }

            for (int i = 0; i < batch.StateChangesInOrder.Count; i++)
            {
                var sc = batch.StateChangesInOrder[i];
                ulong id = PayloadId.StateChange(sc.Entity.Value, sc.Kind);
                if (!_duplicateCheckSet.Add(id))
                {
                    Interlocked.Increment(ref _combatDuplicateOutcomesRejected);
                    throw new InvalidOperationException($"Duplicate StateChange payload in batch: {sc.Entity.Value}:{sc.Kind}");
                }
            }
        }

        private AppliedIdSet RentAppliedIdSet()
        {
            if (_appliedPayloadIdPool.Count > 0)
            {
                var set = _appliedPayloadIdPool.Pop();
                set.Reset();
                return set;
            }

            return new AppliedIdSet();
        }

        private void ReturnAppliedIdSet(AppliedIdSet set)
        {
            set.Reset();
            if (_appliedPayloadIdPool.Count < AppliedIdSetPoolCapacity)
                _appliedPayloadIdPool.Push(set);
        }

        private bool TryRegisterPayloadId(AppliedIdSet appliedSet, ulong payloadId)
        {
            if (appliedSet.Overflowed)
                return true;

            if (appliedSet.Set.Count >= MaxTrackedPayloadIdsPerTick)
            {
                appliedSet.Overflowed = true;
                Interlocked.Increment(ref _combatIdempotenceOverflow);
                return true;
            }

            if (!appliedSet.Set.Add(payloadId))
            {
                Interlocked.Increment(ref _combatDuplicateOutcomesRejected);
                return false;
            }

            return true;
        }

        public CombatOutcomeApplicationCounterSnapshot SnapshotCounters()
        {
            return new CombatOutcomeApplicationCounterSnapshot(
                Interlocked.Read(ref _combatOutcomesApplied),
                Interlocked.Read(ref _combatDuplicateOutcomesRejected),
                Interlocked.Read(ref _combatIdempotenceOverflow),
                Interlocked.Read(ref _combatEventsCreated));
        }
    }

    // --------------------------------------------------------------------
    // Batch Input (ordered, already resolved; produced upstream)
    // --------------------------------------------------------------------

    public sealed class CombatOutcomeBatch
    {
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }

        public IReadOnlyList<IntentResult> IntentResultsInOrder { get; }
        public IReadOnlyList<DamageOutcome> DamageOutcomesInOrder { get; }
        public IReadOnlyList<MitigationOutcome> MitigationOutcomesInOrder { get; }

        // Optional: explicit state changes computed upstream (e.g., restriction/incapacitation/recovery).
        // This system applies them deterministically but does not invent them.
        public IReadOnlyList<CombatStateChange> StateChangesInOrder { get; }

        public CombatOutcomeBatch(
            int authoritativeTick,
            string combatContextId,
            IReadOnlyList<IntentResult> intentResultsInOrder,
            IReadOnlyList<DamageOutcome> damageOutcomesInOrder,
            IReadOnlyList<MitigationOutcome> mitigationOutcomesInOrder,
            IReadOnlyList<CombatStateChange>? stateChangesInOrder = null)
        {
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId ?? throw new ArgumentNullException(nameof(combatContextId));

            IntentResultsInOrder = intentResultsInOrder ?? throw new ArgumentNullException(nameof(intentResultsInOrder));
            DamageOutcomesInOrder = damageOutcomesInOrder ?? throw new ArgumentNullException(nameof(damageOutcomesInOrder));
            MitigationOutcomesInOrder = mitigationOutcomesInOrder ?? throw new ArgumentNullException(nameof(mitigationOutcomesInOrder));

            StateChangesInOrder = stateChangesInOrder ?? Array.Empty<CombatStateChange>();
        }
    }

    public sealed class CombatApplicationResult
    {
        public int AuthoritativeTick { get; }
        public int AppliedPayloadCount { get; }

        public CombatWorldValidationSnapshot PreApplicationSnapshot { get; }
        public CombatWorldValidationSnapshot PostApplicationSnapshot { get; }

        public CombatApplicationResult(
            int authoritativeTick,
            int appliedPayloadCount,
            CombatWorldValidationSnapshot preApplicationSnapshot,
            CombatWorldValidationSnapshot postApplicationSnapshot)
        {
            AuthoritativeTick = authoritativeTick;
            AppliedPayloadCount = appliedPayloadCount;
            PreApplicationSnapshot = preApplicationSnapshot ?? throw new ArgumentNullException(nameof(preApplicationSnapshot));
            PostApplicationSnapshot = postApplicationSnapshot ?? throw new ArgumentNullException(nameof(postApplicationSnapshot));
        }
    }

    // --------------------------------------------------------------------
    // Event envelope (Stage 11.2 structure)
    // --------------------------------------------------------------------

    public sealed class CombatEvent
    {
        public ulong EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public CombatEventType EventType { get; }

        public EntityHandle SubjectEntity { get; }

        public IntentResult? IntentResult { get; }
        public DamageOutcome? DamageOutcome { get; }
        public MitigationOutcome? MitigationOutcome { get; }
        public CombatEntityState? StateSnapshot { get; }

        private CombatEvent(
            ulong eventId,
            int authoritativeTick,
            string combatContextId,
            CombatEventType eventType,
            EntityHandle subjectEntity,
            IntentResult? intentResult,
            DamageOutcome? damageOutcome,
            MitigationOutcome? mitigationOutcome,
            CombatEntityState? stateSnapshot)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            EventType = eventType;

            SubjectEntity = subjectEntity;

            IntentResult = intentResult;
            DamageOutcome = damageOutcome;
            MitigationOutcome = mitigationOutcome;
            StateSnapshot = stateSnapshot;
        }

        public static CombatEvent CreateIntentResultEvent(
            int authoritativeTick,
            string combatContextId,
            EntityHandle subjectEntity,
            IntentResult intentResult,
            ulong payloadId)
        {
            if (intentResult == null) throw new ArgumentNullException(nameof(intentResult));

            ulong eventId = DeterministicEventId(authoritativeTick, CombatEventType.IntentResult, payloadId);
            return new CombatEvent(
                eventId,
                authoritativeTick,
                combatContextId,
                CombatEventType.IntentResult,
                subjectEntity,
                intentResult,
                damageOutcome: null,
                mitigationOutcome: null,
                stateSnapshot: null);
        }

        public static CombatEvent CreateDamageOutcomeEvent(
            int authoritativeTick,
            string combatContextId,
            EntityHandle subjectEntity,
            DamageOutcome damageOutcome,
            ulong payloadId)
        {
            if (damageOutcome == null) throw new ArgumentNullException(nameof(damageOutcome));

            ulong eventId = DeterministicEventId(authoritativeTick, CombatEventType.DamageOutcome, payloadId);
            return new CombatEvent(
                eventId,
                authoritativeTick,
                combatContextId,
                CombatEventType.DamageOutcome,
                subjectEntity,
                intentResult: null,
                damageOutcome: damageOutcome,
                mitigationOutcome: null,
                stateSnapshot: null);
        }

        public static CombatEvent CreateMitigationOutcomeEvent(
            int authoritativeTick,
            string combatContextId,
            EntityHandle subjectEntity,
            MitigationOutcome mitigationOutcome,
            ulong payloadId)
        {
            if (mitigationOutcome == null) throw new ArgumentNullException(nameof(mitigationOutcome));

            ulong eventId = DeterministicEventId(authoritativeTick, CombatEventType.MitigationOutcome, payloadId);
            return new CombatEvent(
                eventId,
                authoritativeTick,
                combatContextId,
                CombatEventType.MitigationOutcome,
                subjectEntity,
                intentResult: null,
                damageOutcome: null,
                mitigationOutcome: mitigationOutcome,
                stateSnapshot: null);
        }

        public static CombatEvent CreateStateChangeEvent(
            int authoritativeTick,
            string combatContextId,
            EntityHandle subjectEntity,
            CombatEntityState stateSnapshot,
            ulong payloadId)
        {
            if (stateSnapshot == null) throw new ArgumentNullException(nameof(stateSnapshot));

            ulong eventId = DeterministicEventId(authoritativeTick, CombatEventType.StateChange, payloadId);
            return new CombatEvent(
                eventId,
                authoritativeTick,
                combatContextId,
                CombatEventType.StateChange,
                subjectEntity,
                intentResult: null,
                damageOutcome: null,
                mitigationOutcome: null,
                stateSnapshot: stateSnapshot);
        }

        private static ulong DeterministicEventId(int tick, CombatEventType type, ulong payloadId)
        {
            // Deterministic, stable, no RNG, no wall-clock.
            // Mixes tick + event type + payload id to guarantee stable ids across replays.
            // Collisions are treated as a correctness failure in higher-level validation.
            unchecked
            {
                ulong hash = 14695981039346656037UL;
                hash = Mix(hash, (uint)tick);
                hash = Mix(hash, (uint)type);
                hash = Mix(hash, payloadId);
                return hash;
            }
        }

        private static ulong Mix(ulong hash, ulong data)
        {
            hash ^= data;
            hash *= 1099511628211UL;
            return hash;
        }
    }

    public enum CombatEventType
    {
        IntentResult,
        DamageOutcome,
        MitigationOutcome,
        StateChange
    }

    public interface ICombatEventSink
    {
        void Emit(CombatEvent combatEvent);
    }

    // --------------------------------------------------------------------
    // Checkpoint request (request-only)
    // --------------------------------------------------------------------

    public interface ICheckpointRequester
    {
        void RequestCheckpoint(int authoritativeTick);
    }

    // --------------------------------------------------------------------
    // Payload IDs (idempotence keys; deterministic)
    // --------------------------------------------------------------------

    internal static class PayloadId
    {
        private const ulong FnvOffset = 14695981039346656037UL;
        private const ulong FnvPrime = 1099511628211UL;

        public static ulong IntentResult(ulong intentIdKey) => Combine(PayloadKind.IntentResult, intentIdKey, 0);
        public static ulong DamageOutcome(ulong outcomeId) => Combine(PayloadKind.DamageOutcome, outcomeId, 0);
        public static ulong MitigationOutcome(ulong outcomeId) => Combine(PayloadKind.MitigationOutcome, outcomeId, 0);
        public static ulong StateChange(int entityValue, CombatStateChangeKind kind) => Combine(PayloadKind.StateChange, (uint)entityValue, (uint)kind);

        public static ulong HashIntentId(string intentId)
        {
            if (intentId == null)
                return 0;

            ulong hash = FnvOffset;
            for (int i = 0; i < intentId.Length; i++)
            {
                hash ^= intentId[i];
                hash *= FnvPrime;
            }
            return hash;
        }

        private static ulong Combine(PayloadKind kind, ulong partA, ulong partB)
        {
            ulong hash = FnvOffset;
            hash = Mix(hash, (ulong)kind);
            hash = Mix(hash, partA);
            hash = Mix(hash, partB);
            return hash;
        }

        private static ulong Mix(ulong hash, ulong data)
        {
            hash ^= data;
            hash *= FnvPrime;
            return hash;
        }
    }

    internal static class OutcomeIdFactory
    {
        public static ulong CreateOutcomeId(int authoritativeTick, EntityHandle actor, int sequence)
        {
            unchecked
            {
                ulong hash = 14695981039346656037UL;
                hash ^= (uint)authoritativeTick;
                hash *= 1099511628211UL;
                hash ^= (uint)actor.Value;
                hash *= 1099511628211UL;
                hash ^= (uint)sequence;
                hash *= 1099511628211UL;
                return hash;
            }
        }
    }

    internal enum PayloadKind : byte
    {
        IntentResult = 1,
        DamageOutcome = 2,
        MitigationOutcome = 3,
        StateChange = 4
    }

    internal sealed class AppliedIdSet
    {
        public readonly HashSet<ulong> Set = new HashSet<ulong>();
        public bool Overflowed;

        public void Reset()
        {
            Set.Clear();
            Overflowed = false;
        }
    }

    // --------------------------------------------------------------------
    // Dependencies / Schemas (Stage 11.2-aligned minimal shapes)
    // --------------------------------------------------------------------

    public interface ITickSource
    {
        int CurrentTick { get; }
    }

    public interface ICombatStateWriter
    {
        CombatEntityState GetState(EntityHandle entity);
        void ApplyStateChange(CombatStateChange change);

        // Validation hook integration: deterministic world snapshot.
        CombatWorldValidationSnapshot CaptureWorldValidationSnapshot(
            int authoritativeTick,
            IReadOnlyDictionary<EntityHandle, string> lastResolvedIntentByEntity);
    }

    public sealed class DamageOutcome
    {
        public ulong OutcomeId { get; }
        public EntityHandle SourceEntity { get; }
        public EntityHandle TargetEntity { get; }
        public string ResolvedIntentId { get; }
        public int DamageAmount { get; }

        public DamageOutcome(ulong outcomeId, EntityHandle sourceEntity, EntityHandle targetEntity, string resolvedIntentId, int damageAmount)
        {
            OutcomeId = outcomeId;
            SourceEntity = sourceEntity;
            TargetEntity = targetEntity;
            ResolvedIntentId = resolvedIntentId;
            DamageAmount = damageAmount;
        }
    }

    public sealed class MitigationOutcome
    {
        public ulong OutcomeId { get; }
        public EntityHandle SourceEntity { get; }
        public EntityHandle TargetEntity { get; }
        public string ResolvedIntentId { get; }
        public int MitigatedAmount { get; }

        public MitigationOutcome(ulong outcomeId, EntityHandle sourceEntity, EntityHandle targetEntity, string resolvedIntentId, int mitigatedAmount)
        {
            OutcomeId = outcomeId;
            SourceEntity = sourceEntity;
            TargetEntity = targetEntity;
            ResolvedIntentId = resolvedIntentId;
            MitigatedAmount = mitigatedAmount;
        }
    }

    public sealed class IntentResult
    {
        public string IntentId { get; }
        public ulong IntentIdKey { get; }
        public CombatIntentType IntentType { get; }
        public EntityHandle ActorEntity { get; }
        public IntentResultStatus ResultStatus { get; }
        public int AuthoritativeTick { get; }

        public string? ReasonCode { get; }
        public IReadOnlyList<ulong> ProducedOutcomeIds { get; }

        public IntentResult(
            string intentId,
            CombatIntentType intentType,
            EntityHandle actorEntity,
            IntentResultStatus resultStatus,
            int authoritativeTick,
            string? reasonCode = null,
            IReadOnlyList<ulong>? producedOutcomeIds = null)
        {
            IntentId = intentId;
            IntentIdKey = PayloadId.HashIntentId(intentId);
            IntentType = intentType;
            ActorEntity = actorEntity;
            ResultStatus = resultStatus;
            AuthoritativeTick = authoritativeTick;
            ReasonCode = reasonCode;
            ProducedOutcomeIds = producedOutcomeIds ?? Array.Empty<ulong>();
        }
    }

    public enum IntentResultStatus
    {
        Accepted,
        Rejected,
        Resolved,
        Canceled
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

    public enum CombatState
    {
        CombatIdle,
        CombatEngaged,
        CombatActing,
        CombatDefending,
        CombatRestricted,
        CombatIncapacitated
    }

    public sealed class CombatEntityState
    {
        public EntityHandle Entity { get; }
        public CombatState State { get; }
        public string CombatContextId { get; }
        public string? CommittedIntentId { get; }
        public int? StateChangeTick { get; }

        public CombatEntityState(
            EntityHandle entity,
            CombatState state,
            string combatContextId,
            string? committedIntentId = null,
            int? stateChangeTick = null)
        {
            Entity = entity;
            State = state;
            CombatContextId = combatContextId;
            CommittedIntentId = committedIntentId;
            StateChangeTick = stateChangeTick;
        }
    }

    public enum CombatStateChangeKind
    {
        ToIdle,
        ToEngaged,
        ToActing,
        ToDefending,
        ToRestricted,
        ToIncapacitated
    }

    public sealed class CombatStateChange
    {
        public EntityHandle Entity { get; }
        public CombatStateChangeKind Kind { get; }
        public string? CombatContextId { get; }
        public string? CommittedIntentId { get; }

        private CombatStateChange(EntityHandle entity, CombatStateChangeKind kind, string? combatContextId, string? committedIntentId)
        {
            Entity = entity;
            Kind = kind;
            CombatContextId = combatContextId;
            CommittedIntentId = committedIntentId;
        }

        public static CombatStateChange ToEngaged(EntityHandle entity, string combatContextId)
            => new CombatStateChange(entity, CombatStateChangeKind.ToEngaged, combatContextId, committedIntentId: null);
    }

    public sealed class CombatWorldValidationSnapshot
    {
        public int AuthoritativeTick { get; }
        public IReadOnlyList<CombatEntityValidationSnapshot> Entities { get; }
        public IReadOnlyList<string> ContextIds { get; }

        public CombatWorldValidationSnapshot(
            int authoritativeTick,
            IReadOnlyList<CombatEntityValidationSnapshot> entities,
            IReadOnlyList<string>? contextIds = null)
        {
            AuthoritativeTick = authoritativeTick;
            Entities = entities ?? throw new ArgumentNullException(nameof(entities));
            ContextIds = contextIds ?? Array.Empty<string>();
        }
    }

    public sealed class CombatEntityValidationSnapshot
    {
        public EntityHandle Entity { get; }
        public CombatState State { get; }
        public string CombatContextId { get; }
        public string? CommittedIntentId { get; }
        public string? LastResolvedIntentId { get; }

        public CombatEntityValidationSnapshot(
            EntityHandle entity,
            CombatState state,
            string combatContextId,
            string? committedIntentId = null,
            string? lastResolvedIntentId = null)
        {
            Entity = entity;
            State = state;
            CombatContextId = combatContextId;
            CommittedIntentId = committedIntentId;
            LastResolvedIntentId = lastResolvedIntentId;
        }
    }

    public readonly struct CombatOutcomeApplicationCounterSnapshot
    {
        public CombatOutcomeApplicationCounterSnapshot(
            long combatOutcomesApplied,
            long combatDuplicateOutcomesRejected,
            long combatIdempotenceOverflow,
            long combatEventsCreated)
        {
            CombatOutcomesApplied = combatOutcomesApplied;
            CombatDuplicateOutcomesRejected = combatDuplicateOutcomesRejected;
            CombatIdempotenceOverflow = combatIdempotenceOverflow;
            CombatEventsCreated = combatEventsCreated;
        }

        public long CombatOutcomesApplied { get; }
        public long CombatDuplicateOutcomesRejected { get; }
        public long CombatIdempotenceOverflow { get; }
        public long CombatEventsCreated { get; }

        public static CombatOutcomeApplicationCounterSnapshot Empty =>
            new CombatOutcomeApplicationCounterSnapshot(0, 0, 0, 0);
    }
}
