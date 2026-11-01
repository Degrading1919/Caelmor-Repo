// CombatOutcomeApplicationSystem.cs
// NOTE: Save location must follow existing project structure.
// Implements CombatOutcomeApplicationSystem only.
// No intent validation, no intent resolution, no damage/mitigation calculation, no persistence I/O.

using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

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
    public sealed class CombatOutcomeApplicationSystem
    {
        private readonly ITickSource _tickSource;
        private readonly ICombatStateWriter _stateWriter;
        private readonly ICombatEventSink _eventSink;
        private readonly ICheckpointRequester _checkpointRequester;

        // Idempotence guard: applied payload IDs are scoped per authoritative tick.
        // Not global across session; not persisted.
        private readonly Dictionary<int, HashSet<string>> _appliedPayloadIdsByTick = new();

        // Validation support: last resolved intent per entity (snapshot-only; not authoritative gameplay state).
        private readonly Dictionary<string, string> _lastResolvedIntentIdByEntity =
            new Dictionary<string, string>(StringComparer.Ordinal);

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

                string payloadId = PayloadId.IntentResult(r.IntentId);
                if (!appliedSet.Add(payloadId))
                    continue; // idempotent: already applied this payload for this tick

                ApplyIntentResultStateEffectsOrThrow(r);

                EmitEventAfterApply(CombatEvent.CreateIntentResultEvent(
                    authoritativeTick: nowTick,
                    combatContextId: batch.CombatContextId,
                    subjectEntityId: r.ActorEntityId,
                    intentResult: r));

                appliedCount++;
            }

            // 2) Apply DamageOutcomes (no combat state fields exist for HP here; this system does not invent them).
            for (int i = 0; i < batch.DamageOutcomesInOrder.Count; i++)
            {
                var d = batch.DamageOutcomesInOrder[i];

                string payloadId = PayloadId.DamageOutcome(d.OutcomeId);
                if (!appliedSet.Add(payloadId))
                    continue;

                EmitEventAfterApply(CombatEvent.CreateDamageOutcomeEvent(
                    authoritativeTick: nowTick,
                    combatContextId: batch.CombatContextId,
                    subjectEntityId: d.TargetEntityId,
                    damageOutcome: d));

                appliedCount++;
            }

            // 3) Apply MitigationOutcomes (no mutation; broadcast reflects applied results).
            for (int i = 0; i < batch.MitigationOutcomesInOrder.Count; i++)
            {
                var m = batch.MitigationOutcomesInOrder[i];

                string payloadId = PayloadId.MitigationOutcome(m.OutcomeId);
                if (!appliedSet.Add(payloadId))
                    continue;

                EmitEventAfterApply(CombatEvent.CreateMitigationOutcomeEvent(
                    authoritativeTick: nowTick,
                    combatContextId: batch.CombatContextId,
                    subjectEntityId: m.TargetEntityId,
                    mitigationOutcome: m));

                appliedCount++;
            }

            // 4) Apply explicit state changes (if provided by upstream systems).
            // This is the only allowed mechanism here to enter Restricted/Incapacitated/Recovery transitions
            // without inventing logic in this system.
            for (int i = 0; i < batch.StateChangesInOrder.Count; i++)
            {
                var sc = batch.StateChangesInOrder[i];

                string payloadId = PayloadId.StateChange(sc.EntityId, sc.Kind.ToString());
                if (!appliedSet.Add(payloadId))
                    continue;

                _stateWriter.ApplyStateChange(sc);

                // After mutation, emit state snapshot event reflecting applied state.
                var state = _stateWriter.GetState(sc.EntityId);

                EmitEventAfterApply(CombatEvent.CreateStateChangeEvent(
                    authoritativeTick: nowTick,
                    combatContextId: batch.CombatContextId,
                    subjectEntityId: sc.EntityId,
                    stateSnapshot: state));

                appliedCount++;
            }

            // Request checkpoint at the valid boundary (request-only).
            // Only request if we actually applied something new for this tick.
            if (appliedCount > 0)
                _checkpointRequester.RequestCheckpoint(nowTick);

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
            if (string.IsNullOrWhiteSpace(r.ActorEntityId)) throw new InvalidOperationException("IntentResult.actor_entity_id missing.");

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
            var state = _stateWriter.GetState(r.ActorEntityId);

            if (state.State == CombatState.CombatActing || state.State == CombatState.CombatDefending)
            {
                if (!string.Equals(state.CommittedIntentId, r.IntentId, StringComparison.Ordinal))
                    throw new InvalidOperationException(
                        $"Committed intent mismatch for entity {r.ActorEntityId}. state.committed={state.CommittedIntentId} result.intent={r.IntentId}");

                // Transition back to engaged (no new combat_context_id invented here).
                _stateWriter.ApplyStateChange(CombatStateChange.ToEngaged(r.ActorEntityId, state.CombatContextId));

                // Snapshot-only helper for validation
                _lastResolvedIntentIdByEntity[r.ActorEntityId] = r.IntentId;

                return;
            }

            // If not Acting/Defending, we do not invent any state mutation here.
            // Resolution may still be meaningful (e.g., movement/interaction outcomes),
            // but those effects are not represented in CombatEntityState schema.
            _lastResolvedIntentIdByEntity[r.ActorEntityId] = r.IntentId;
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

        private HashSet<string> GetOrCreateAppliedSetForTick(int tick)
        {
            if (!_appliedPayloadIdsByTick.TryGetValue(tick, out var set))
            {
                set = new HashSet<string>(StringComparer.Ordinal);
                _appliedPayloadIdsByTick.Add(tick, set);
            }
            return set;
        }

        private void PruneAppliedSets(int keepFromTickInclusive)
        {
            var keys = _appliedPayloadIdsByTick.Keys.ToArray();
            for (int i = 0; i < keys.Length; i++)
            {
                if (keys[i] < keepFromTickInclusive)
                    _appliedPayloadIdsByTick.Remove(keys[i]);
            }
        }

        private static void EnsureNoDuplicateIdsInBatchOrThrow(CombatOutcomeBatch batch)
        {
            var seen = new HashSet<string>(StringComparer.Ordinal);

            for (int i = 0; i < batch.IntentResultsInOrder.Count; i++)
            {
                var r = batch.IntentResultsInOrder[i];
                string id = PayloadId.IntentResult(r.IntentId);
                if (!seen.Add(id))
                    throw new InvalidOperationException($"Duplicate IntentResult payload in batch: {r.IntentId}");
            }

            for (int i = 0; i < batch.DamageOutcomesInOrder.Count; i++)
            {
                var d = batch.DamageOutcomesInOrder[i];
                string id = PayloadId.DamageOutcome(d.OutcomeId);
                if (!seen.Add(id))
                    throw new InvalidOperationException($"Duplicate DamageOutcome payload in batch: {d.OutcomeId}");
            }

            for (int i = 0; i < batch.MitigationOutcomesInOrder.Count; i++)
            {
                var m = batch.MitigationOutcomesInOrder[i];
                string id = PayloadId.MitigationOutcome(m.OutcomeId);
                if (!seen.Add(id))
                    throw new InvalidOperationException($"Duplicate MitigationOutcome payload in batch: {m.OutcomeId}");
            }

            for (int i = 0; i < batch.StateChangesInOrder.Count; i++)
            {
                var sc = batch.StateChangesInOrder[i];
                string id = PayloadId.StateChange(sc.EntityId, sc.Kind.ToString());
                if (!seen.Add(id))
                    throw new InvalidOperationException($"Duplicate StateChange payload in batch: {sc.EntityId}:{sc.Kind}");
            }
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
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public CombatEventType EventType { get; }

        public string? SubjectEntityId { get; }

        public IntentResult? IntentResult { get; }
        public DamageOutcome? DamageOutcome { get; }
        public MitigationOutcome? MitigationOutcome { get; }
        public CombatEntityState? StateSnapshot { get; }

        private CombatEvent(
            string eventId,
            int authoritativeTick,
            string combatContextId,
            CombatEventType eventType,
            string? subjectEntityId,
            IntentResult? intentResult,
            DamageOutcome? damageOutcome,
            MitigationOutcome? mitigationOutcome,
            CombatEntityState? stateSnapshot)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            EventType = eventType;

            SubjectEntityId = subjectEntityId;

            IntentResult = intentResult;
            DamageOutcome = damageOutcome;
            MitigationOutcome = mitigationOutcome;
            StateSnapshot = stateSnapshot;
        }

        public static CombatEvent CreateIntentResultEvent(
            int authoritativeTick,
            string combatContextId,
            string? subjectEntityId,
            IntentResult intentResult)
        {
            if (intentResult == null) throw new ArgumentNullException(nameof(intentResult));

            string eventId = DeterministicEventId(authoritativeTick, CombatEventType.IntentResult.ToString(), intentResult.IntentId);
            return new CombatEvent(
                eventId,
                authoritativeTick,
                combatContextId,
                CombatEventType.IntentResult,
                subjectEntityId,
                intentResult,
                damageOutcome: null,
                mitigationOutcome: null,
                stateSnapshot: null);
        }

        public static CombatEvent CreateDamageOutcomeEvent(
            int authoritativeTick,
            string combatContextId,
            string? subjectEntityId,
            DamageOutcome damageOutcome)
        {
            if (damageOutcome == null) throw new ArgumentNullException(nameof(damageOutcome));

            string eventId = DeterministicEventId(authoritativeTick, CombatEventType.DamageOutcome.ToString(), damageOutcome.OutcomeId);
            return new CombatEvent(
                eventId,
                authoritativeTick,
                combatContextId,
                CombatEventType.DamageOutcome,
                subjectEntityId,
                intentResult: null,
                damageOutcome: damageOutcome,
                mitigationOutcome: null,
                stateSnapshot: null);
        }

        public static CombatEvent CreateMitigationOutcomeEvent(
            int authoritativeTick,
            string combatContextId,
            string? subjectEntityId,
            MitigationOutcome mitigationOutcome)
        {
            if (mitigationOutcome == null) throw new ArgumentNullException(nameof(mitigationOutcome));

            string eventId = DeterministicEventId(authoritativeTick, CombatEventType.MitigationOutcome.ToString(), mitigationOutcome.OutcomeId);
            return new CombatEvent(
                eventId,
                authoritativeTick,
                combatContextId,
                CombatEventType.MitigationOutcome,
                subjectEntityId,
                intentResult: null,
                damageOutcome: null,
                mitigationOutcome: mitigationOutcome,
                stateSnapshot: null);
        }

        public static CombatEvent CreateStateChangeEvent(
            int authoritativeTick,
            string combatContextId,
            string? subjectEntityId,
            CombatEntityState stateSnapshot)
        {
            if (stateSnapshot == null) throw new ArgumentNullException(nameof(stateSnapshot));

            string eventId = DeterministicEventId(authoritativeTick, CombatEventType.StateChange.ToString(), stateSnapshot.EntityId);
            return new CombatEvent(
                eventId,
                authoritativeTick,
                combatContextId,
                CombatEventType.StateChange,
                subjectEntityId,
                intentResult: null,
                damageOutcome: null,
                mitigationOutcome: null,
                stateSnapshot: stateSnapshot);
        }

        private static string DeterministicEventId(int tick, string type, string payloadId)
        {
            // Deterministic, stable, no RNG, no wall-clock.
            // Collisions are treated as a correctness failure in higher-level validation.
            return $"ce:{tick}:{type}:{payloadId}";
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
        public static string IntentResult(string intentId) => $"ir:{intentId}";
        public static string DamageOutcome(string outcomeId) => $"do:{outcomeId}";
        public static string MitigationOutcome(string outcomeId) => $"mo:{outcomeId}";
        public static string StateChange(string entityId, string kind) => $"sc:{entityId}:{kind}";
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
        CombatEntityState GetState(string entityId);
        void ApplyStateChange(CombatStateChange change);

        // Validation hook integration: deterministic world snapshot.
        CombatWorldValidationSnapshot CaptureWorldValidationSnapshot(
            int authoritativeTick,
            IReadOnlyDictionary<string, string> lastResolvedIntentByEntity);
    }

    public sealed class DamageOutcome
    {
        public string OutcomeId { get; }
        public string SourceEntityId { get; }
        public string TargetEntityId { get; }
        public string ResolvedIntentId { get; }
        public int DamageAmount { get; }

        public DamageOutcome(string outcomeId, string sourceEntityId, string targetEntityId, string resolvedIntentId, int damageAmount)
        {
            OutcomeId = outcomeId;
            SourceEntityId = sourceEntityId;
            TargetEntityId = targetEntityId;
            ResolvedIntentId = resolvedIntentId;
            DamageAmount = damageAmount;
        }
    }

    public sealed class MitigationOutcome
    {
        public string OutcomeId { get; }
        public string SourceEntityId { get; }
        public string TargetEntityId { get; }
        public string ResolvedIntentId { get; }
        public int MitigatedAmount { get; }

        public MitigationOutcome(string outcomeId, string sourceEntityId, string targetEntityId, string resolvedIntentId, int mitigatedAmount)
        {
            OutcomeId = outcomeId;
            SourceEntityId = sourceEntityId;
            TargetEntityId = targetEntityId;
            ResolvedIntentId = resolvedIntentId;
            MitigatedAmount = mitigatedAmount;
        }
    }

    public sealed class IntentResult
    {
        public string IntentId { get; }
        public CombatIntentType IntentType { get; }
        public string ActorEntityId { get; }
        public IntentResultStatus ResultStatus { get; }
        public int AuthoritativeTick { get; }

        public string? ReasonCode { get; }
        public IReadOnlyList<string> ProducedOutcomeIds { get; }

        public IntentResult(
            string intentId,
            CombatIntentType intentType,
            string actorEntityId,
            IntentResultStatus resultStatus,
            int authoritativeTick,
            string? reasonCode = null,
            IReadOnlyList<string>? producedOutcomeIds = null)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntityId = actorEntityId;
            ResultStatus = resultStatus;
            AuthoritativeTick = authoritativeTick;
            ReasonCode = reasonCode;
            ProducedOutcomeIds = producedOutcomeIds ?? Array.Empty<string>();
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
        public string EntityId { get; }
        public CombatState State { get; }
        public string CombatContextId { get; }
        public string? CommittedIntentId { get; }
        public int? StateChangeTick { get; }

        public CombatEntityState(
            string entityId,
            CombatState state,
            string combatContextId,
            string? committedIntentId = null,
            int? stateChangeTick = null)
        {
            EntityId = entityId;
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
        public string EntityId { get; }
        public CombatStateChangeKind Kind { get; }
        public string? CombatContextId { get; }
        public string? CommittedIntentId { get; }

        private CombatStateChange(string entityId, CombatStateChangeKind kind, string? combatContextId, string? committedIntentId)
        {
            EntityId = entityId;
            Kind = kind;
            CombatContextId = combatContextId;
            CommittedIntentId = committedIntentId;
        }

        public static CombatStateChange ToEngaged(string entityId, string combatContextId)
            => new CombatStateChange(entityId, CombatStateChangeKind.ToEngaged, combatContextId, committedIntentId: null);
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
        public string EntityId { get; }
        public CombatState State { get; }
        public string CombatContextId { get; }
        public string? CommittedIntentId { get; }
        public string? LastResolvedIntentId { get; }

        public CombatEntityValidationSnapshot(
            string entityId,
            CombatState state,
            string combatContextId,
            string? committedIntentId = null,
            string? lastResolvedIntentId = null)
        {
            EntityId = entityId;
            State = state;
            CombatContextId = combatContextId;
            CommittedIntentId = committedIntentId;
            LastResolvedIntentId = lastResolvedIntentId;
        }
    }
}
