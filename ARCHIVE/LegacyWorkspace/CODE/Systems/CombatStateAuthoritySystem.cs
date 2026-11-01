// CombatStateAuthoritySystem.cs
// NOTE: Save location must follow existing project structure.
// This file implements CombatStateAuthoritySystem only.
// No combat resolution, no damage/mitigation, no CombatEvents emission, no persistence.

using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace Caelmor.Combat
{
    /// <summary>
    /// CombatStateAuthoritySystem
    /// - Owns authoritative CombatEntityState per entity
    /// - Consumes frozen intent queues (Stage 12.1)
    /// - Deterministically gates each intent based on current CombatState (Stage 10.2)
    /// - Preserves frozen ordering; does not short-circuit
    /// - Produces:
    ///   - Ordered list of validated intents for downstream resolution (accepted only)
    ///   - Observable rejection results for rejected intents
    /// - Exposes pre/post gating snapshots for validation harness
    ///
    /// HARD NON-RESPONSIBILITIES:
    /// - Does not resolve outcomes
    /// - Does not calculate damage/mitigation
    /// - Does not emit CombatEvents
    /// - Does not persist state
    /// - Does not modify intent payloads
    /// - Does not reorder intents
    /// </summary>
    public sealed class CombatStateAuthoritySystem
    {
        private readonly ITickSource _tickSource;
        private readonly IEntityIdValidator _entityIdValidator;
        private readonly IIntentGateRejectionSink _rejectionSink;

        // Authoritative state store (server-only).
        private readonly Dictionary<string, CombatEntityState> _statesByEntityId =
            new Dictionary<string, CombatEntityState>(StringComparer.Ordinal);

        public CombatStateAuthoritySystem(
            ITickSource tickSource,
            IEntityIdValidator entityIdValidator,
            IIntentGateRejectionSink rejectionSink)
        {
            _tickSource = tickSource ?? throw new ArgumentNullException(nameof(tickSource));
            _entityIdValidator = entityIdValidator ?? throw new ArgumentNullException(nameof(entityIdValidator));
            _rejectionSink = rejectionSink ?? throw new ArgumentNullException(nameof(rejectionSink));
        }

        // -----------------------------
        // State Ownership (Authoritative)
        // -----------------------------

        public CombatEntityState GetState(string entityId)
        {
            if (string.IsNullOrWhiteSpace(entityId)) throw new ArgumentException("entityId missing.", nameof(entityId));
            if (!_entityIdValidator.IsValidEntityId(entityId)) throw new ArgumentException("entityId invalid.", nameof(entityId));

            if (!_statesByEntityId.TryGetValue(entityId, out var state))
            {
                state = CombatEntityState.CreateIdle(entityId);
                _statesByEntityId.Add(entityId, state);
            }

            return state;
        }

        /// <summary>
        /// Authoritative mutation API.
        /// Used by the combat runtime coordinator in the phase where mutation is allowed (Stage 11.3).
        /// This system does not infer transitions during gating.
        /// </summary>
        public void ApplyStateChange(CombatStateChange change)
        {
            // Mutation must be called only from the allowed tick phase by the coordinator.
            // This method does not enforce tick-phase; it enforces structural state invariants only.
            if (change == null) throw new ArgumentNullException(nameof(change));

            if (string.IsNullOrWhiteSpace(change.EntityId))
                throw new InvalidOperationException("CombatStateChange.EntityId missing.");

            if (!_entityIdValidator.IsValidEntityId(change.EntityId))
                throw new InvalidOperationException("CombatStateChange.EntityId invalid.");

            var prior = GetState(change.EntityId);
            var next = prior.ApplyChange(change, authoritativeTick: _tickSource.CurrentTick);

            // Enforce schema-level state invariants (Stage 11.2).
            ValidateStateInvariantsOrThrow(next);

            _statesByEntityId[change.EntityId] = next;
        }

        /// <summary>
        /// Convenience API to authoritatively establish combat context.
        /// Transitions CombatIdle -> CombatEngaged and assigns combat_context_id.
        /// Must be invoked only when the server authoritatively establishes engagement.
        /// </summary>
        public void EstablishCombatContext(string entityId, string combatContextId)
        {
            if (string.IsNullOrWhiteSpace(entityId)) throw new ArgumentException("entityId missing.", nameof(entityId));
            if (!_entityIdValidator.IsValidEntityId(entityId)) throw new ArgumentException("entityId invalid.", nameof(entityId));
            if (string.IsNullOrWhiteSpace(combatContextId)) throw new ArgumentException("combatContextId missing.", nameof(combatContextId));

            var prior = GetState(entityId);

            // Only assign/transition here; no other gameplay behavior.
            var change = CombatStateChange.ToEngaged(entityId, combatContextId);
            var next = prior.ApplyChange(change, authoritativeTick: _tickSource.CurrentTick);

            ValidateStateInvariantsOrThrow(next);

            _statesByEntityId[entityId] = next;
        }

        // -----------------------------
        // Intent Gating (Read-Only)
        // -----------------------------

        /// <summary>
        /// Evaluates a frozen queue snapshot and produces:
        /// - ordered accepted intents for downstream resolution
        /// - ordered gate dispositions (accepted/rejected) for validation
        /// - observable rejection outputs (for rejected intents)
        ///
        /// This method:
        /// - DOES NOT mutate any CombatEntityState
        /// - DOES NOT reorder intents
        /// - DOES NOT short-circuit evaluation
        /// </summary>
        public GatedIntentBatch GateFrozenQueue(FrozenQueueSnapshot frozenQueue)
        {
            if (frozenQueue == null) throw new ArgumentNullException(nameof(frozenQueue));

            // Pre-gating snapshot (read-only).
            var pre = CombatStateSnapshot.Capture(_statesByEntityId);

            var gateRows = new List<IntentGateRow>(frozenQueue.Intents.Count);
            var accepted = new List<FrozenIntentRecord>(capacity: frozenQueue.Intents.Count);

            for (int i = 0; i < frozenQueue.Intents.Count; i++)
            {
                var intent = frozenQueue.Intents[i];

                // Deterministic evaluation order == frozen queue order.
                var actorState = GetState(intent.ActorEntityId);

                // If state is structurally invalid, fail-loud for that intent (reject, do not auto-repair).
                if (!IsStructurallyValidState(actorState, out var invalidReason))
                {
                    RejectIntent(intent, GateRejectReasonCodes.InvalidCombatState, invalidReason);
                    gateRows.Add(IntentGateRow.Rejected(intent, GateRejectReasonCodes.InvalidCombatState));
                    continue;
                }

                // State-based legality check (Stage 10.2).
                if (!IsIntentAllowedInState(intent.IntentType, actorState.State))
                {
                    RejectIntent(intent, GateRejectReasonCodes.IntentBlockedByState, actorState.State.ToString());
                    gateRows.Add(IntentGateRow.Rejected(intent, GateRejectReasonCodes.IntentBlockedByState));
                    continue;
                }

                // Combat context requirement:
                // - Non-idle states must have combat_context_id (Stage 11.2).
                // - If the entity is non-idle but lacks context, reject without mutation.
                if (actorState.State != CombatState.CombatIdle && string.IsNullOrWhiteSpace(actorState.CombatContextId))
                {
                    RejectIntent(intent, GateRejectReasonCodes.MissingCombatContext, "combat_context_id missing for non-idle state");
                    gateRows.Add(IntentGateRow.Rejected(intent, GateRejectReasonCodes.MissingCombatContext));
                    continue;
                }

                // Accepted for downstream resolution (still not resolved; no outcomes here).
                accepted.Add(intent);
                gateRows.Add(IntentGateRow.Accepted(intent));
            }

            // Post-gating snapshot (still read-only; gating must not mutate state).
            var post = CombatStateSnapshot.Capture(_statesByEntityId);

            var batch = new GatedIntentBatch(
                authoritativeTick: frozenQueue.AuthoritativeTick,
                acceptedIntentsInOrder: new ReadOnlyCollection<FrozenIntentRecord>(accepted),
                gateResultsInOrder: new ReadOnlyCollection<IntentGateRow>(gateRows),
                preGatingStateSnapshot: pre,
                postGatingStateSnapshot: post
            );

            return batch;
        }

        private void RejectIntent(FrozenIntentRecord intent, string reasonCode, string details)
        {
            // Observable rejection output for invalid intents.
            // Not CombatEvents; this is intake/gating observability only.
            _rejectionSink.OnRejected(new IntentGateRejection(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntityId: intent.ActorEntityId,
                authoritativeTick: _tickSource.CurrentTick,
                reasonCode: reasonCode,
                details: details
            ));
        }

        // -----------------------------
        // State gating rules (Stage 10.2)
        // -----------------------------

        private static bool IsIntentAllowedInState(CombatIntentType intentType, CombatState state)
        {
            switch (state)
            {
                case CombatState.CombatIdle:
                    // Allowed: Movement, Interact
                    return intentType == CombatIntentType.CombatMovementIntent
                        || intentType == CombatIntentType.CombatInteractIntent;

                case CombatState.CombatEngaged:
                    // Allowed: Attack, Defend, Ability, Movement, Interact
                    // Blocked: Cancel
                    return intentType == CombatIntentType.CombatAttackIntent
                        || intentType == CombatIntentType.CombatDefendIntent
                        || intentType == CombatIntentType.CombatAbilityIntent
                        || intentType == CombatIntentType.CombatMovementIntent
                        || intentType == CombatIntentType.CombatInteractIntent;

                case CombatState.CombatActing:
                    // Allowed: Cancel only
                    return intentType == CombatIntentType.CombatCancelIntent;

                case CombatState.CombatDefending:
                    // Allowed: Cancel only
                    return intentType == CombatIntentType.CombatCancelIntent;

                case CombatState.CombatRestricted:
                    // Allowed: Defend, Movement, Cancel
                    return intentType == CombatIntentType.CombatDefendIntent
                        || intentType == CombatIntentType.CombatMovementIntent
                        || intentType == CombatIntentType.CombatCancelIntent;

                case CombatState.CombatIncapacitated:
                    // Allowed: Cancel only
                    return intentType == CombatIntentType.CombatCancelIntent;

                default:
                    return false;
            }
        }

        // -----------------------------
        // Structural state invariants (Stage 11.2)
        // -----------------------------

        private static bool IsStructurallyValidState(CombatEntityState state, out string reason)
        {
            reason = string.Empty;

            if (string.IsNullOrWhiteSpace(state.EntityId))
            {
                reason = "entity_id missing";
                return false;
            }

            // combat_context_id MAY be empty only when state is CombatIdle
            if (state.State == CombatState.CombatIdle)
            {
                // committed_intent_id MUST be absent when idle
                if (!string.IsNullOrWhiteSpace(state.CommittedIntentId))
                {
                    reason = "committed_intent_id must be absent in CombatIdle";
                    return false;
                }

                return true;
            }

            if (string.IsNullOrWhiteSpace(state.CombatContextId))
            {
                reason = "combat_context_id must be present for non-idle states";
                return false;
            }

            // committed_intent_id presence rules
            if (state.State == CombatState.CombatActing || state.State == CombatState.CombatDefending)
            {
                if (string.IsNullOrWhiteSpace(state.CommittedIntentId))
                {
                    reason = "committed_intent_id must be present in CombatActing/CombatDefending";
                    return false;
                }
            }
            else
            {
                // MUST be absent in CombatEngaged (and also intended absent in others except acting/defending)
                if (state.State == CombatState.CombatEngaged && !string.IsNullOrWhiteSpace(state.CommittedIntentId))
                {
                    reason = "committed_intent_id must be absent in CombatEngaged";
                    return false;
                }
            }

            return true;
        }

        private static void ValidateStateInvariantsOrThrow(CombatEntityState next)
        {
            if (!IsStructurallyValidState(next, out var reason))
                throw new InvalidOperationException($"Invalid CombatEntityState invariants: {reason}");
        }
    }

    // --------------------------------------------------------------------
    // Data Models
    // --------------------------------------------------------------------

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
        public string CombatContextId { get; } // may be empty only for Idle
        public string? CommittedIntentId { get; } // required for Acting/Defending; absent for Idle/Engaged
        public int StateChangeTick { get; } // optional in schema; always set here for determinism/validation

        private CombatEntityState(
            string entityId,
            CombatState state,
            string combatContextId,
            string? committedIntentId,
            int stateChangeTick)
        {
            EntityId = entityId;
            State = state;
            CombatContextId = combatContextId;
            CommittedIntentId = committedIntentId;
            StateChangeTick = stateChangeTick;
        }

        public static CombatEntityState CreateIdle(string entityId)
            => new CombatEntityState(
                entityId: entityId,
                state: CombatState.CombatIdle,
                combatContextId: string.Empty,
                committedIntentId: null,
                stateChangeTick: 0);

        public CombatEntityState ApplyChange(CombatStateChange change, int authoritativeTick)
        {
            if (!string.Equals(EntityId, change.EntityId, StringComparison.Ordinal))
                throw new InvalidOperationException("CombatStateChange entity mismatch.");

            switch (change.Kind)
            {
                case CombatStateChangeKind.ToIdle:
                    return new CombatEntityState(
                        entityId: EntityId,
                        state: CombatState.CombatIdle,
                        combatContextId: string.Empty,
                        committedIntentId: null,
                        stateChangeTick: authoritativeTick);

                case CombatStateChangeKind.ToEngaged:
                    return new CombatEntityState(
                        entityId: EntityId,
                        state: CombatState.CombatEngaged,
                        combatContextId: change.CombatContextId ?? string.Empty,
                        committedIntentId: null,
                        stateChangeTick: authoritativeTick);

                case CombatStateChangeKind.ToActing:
                    return new CombatEntityState(
                        entityId: EntityId,
                        state: CombatState.CombatActing,
                        combatContextId: change.CombatContextId ?? CombatContextId,
                        committedIntentId: change.CommittedIntentId,
                        stateChangeTick: authoritativeTick);

                case CombatStateChangeKind.ToDefending:
                    return new CombatEntityState(
                        entityId: EntityId,
                        state: CombatState.CombatDefending,
                        combatContextId: change.CombatContextId ?? CombatContextId,
                        committedIntentId: change.CommittedIntentId,
                        stateChangeTick: authoritativeTick);

                case CombatStateChangeKind.ToRestricted:
                    return new CombatEntityState(
                        entityId: EntityId,
                        state: CombatState.CombatRestricted,
                        combatContextId: change.CombatContextId ?? CombatContextId,
                        committedIntentId: null,
                        stateChangeTick: authoritativeTick);

                case CombatStateChangeKind.ToIncapacitated:
                    return new CombatEntityState(
                        entityId: EntityId,
                        state: CombatState.CombatIncapacitated,
                        combatContextId: change.CombatContextId ?? CombatContextId,
                        committedIntentId: change.CommittedIntentId ?? CommittedIntentId,
                        stateChangeTick: authoritativeTick);

                default:
                    throw new InvalidOperationException($"Unknown CombatStateChangeKind: {change.Kind}");
            }
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

        public static CombatStateChange ToIdle(string entityId)
            => new CombatStateChange(entityId, CombatStateChangeKind.ToIdle, combatContextId: null, committedIntentId: null);

        public static CombatStateChange ToEngaged(string entityId, string combatContextId)
            => new CombatStateChange(entityId, CombatStateChangeKind.ToEngaged, combatContextId: combatContextId, committedIntentId: null);

        public static CombatStateChange ToActing(string entityId, string combatContextId, string committedIntentId)
            => new CombatStateChange(entityId, CombatStateChangeKind.ToActing, combatContextId: combatContextId, committedIntentId: committedIntentId);

        public static CombatStateChange ToDefending(string entityId, string combatContextId, string committedIntentId)
            => new CombatStateChange(entityId, CombatStateChangeKind.ToDefending, combatContextId: combatContextId, committedIntentId: committedIntentId);

        public static CombatStateChange ToRestricted(string entityId, string combatContextId)
            => new CombatStateChange(entityId, CombatStateChangeKind.ToRestricted, combatContextId: combatContextId, committedIntentId: null);

        public static CombatStateChange ToIncapacitated(string entityId, string combatContextId, string? committedIntentId = null)
            => new CombatStateChange(entityId, CombatStateChangeKind.ToIncapacitated, combatContextId: combatContextId, committedIntentId: committedIntentId);
    }

    // --------------------------------------------------------------------
    // Gating Outputs (Ordered)
    // --------------------------------------------------------------------

    public sealed class GatedIntentBatch
    {
        public int AuthoritativeTick { get; }

        // Ordered accepted intents (preserves frozen ordering subset).
        public IReadOnlyList<FrozenIntentRecord> AcceptedIntentsInOrder { get; }

        // Ordered disposition rows for every intent in the frozen queue.
        public IReadOnlyList<IntentGateRow> GateResultsInOrder { get; }

        // Validation snapshots
        public CombatStateSnapshot PreGatingStateSnapshot { get; }
        public CombatStateSnapshot PostGatingStateSnapshot { get; }

        public GatedIntentBatch(
            int authoritativeTick,
            IReadOnlyList<FrozenIntentRecord> acceptedIntentsInOrder,
            IReadOnlyList<IntentGateRow> gateResultsInOrder,
            CombatStateSnapshot preGatingStateSnapshot,
            CombatStateSnapshot postGatingStateSnapshot)
        {
            AuthoritativeTick = authoritativeTick;
            AcceptedIntentsInOrder = acceptedIntentsInOrder ?? throw new ArgumentNullException(nameof(acceptedIntentsInOrder));
            GateResultsInOrder = gateResultsInOrder ?? throw new ArgumentNullException(nameof(gateResultsInOrder));
            PreGatingStateSnapshot = preGatingStateSnapshot ?? throw new ArgumentNullException(nameof(preGatingStateSnapshot));
            PostGatingStateSnapshot = postGatingStateSnapshot ?? throw new ArgumentNullException(nameof(postGatingStateSnapshot));
        }
    }

    public readonly struct IntentGateRow
    {
        public readonly string IntentId;
        public readonly CombatIntentType IntentType;
        public readonly string ActorEntityId;
        public readonly IntentGateStatus Status;
        public readonly string ReasonCode;

        private IntentGateRow(string intentId, CombatIntentType intentType, string actorEntityId, IntentGateStatus status, string reasonCode)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntityId = actorEntityId;
            Status = status;
            ReasonCode = reasonCode;
        }

        public static IntentGateRow Accepted(FrozenIntentRecord intent)
            => new IntentGateRow(intent.IntentId, intent.IntentType, intent.ActorEntityId, IntentGateStatus.Accepted, reasonCode: string.Empty);

        public static IntentGateRow Rejected(FrozenIntentRecord intent, string reasonCode)
            => new IntentGateRow(intent.IntentId, intent.IntentType, intent.ActorEntityId, IntentGateStatus.Rejected, reasonCode);
    }

    public enum IntentGateStatus
    {
        Accepted,
        Rejected
    }

    public static class GateRejectReasonCodes
    {
        public const string IntentBlockedByState = "IntentBlockedByState";
        public const string MissingCombatContext = "MissingCombatContext";
        public const string InvalidCombatState = "InvalidCombatState";
    }

    // --------------------------------------------------------------------
    // Observable rejection sink (not CombatEvents)
    // --------------------------------------------------------------------

    public sealed class IntentGateRejection
    {
        public string IntentId { get; }
        public CombatIntentType IntentType { get; }
        public string ActorEntityId { get; }
        public int AuthoritativeTick { get; }
        public string ReasonCode { get; }
        public string Details { get; }

        public IntentGateRejection(
            string intentId,
            CombatIntentType intentType,
            string actorEntityId,
            int authoritativeTick,
            string reasonCode,
            string details)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntityId = actorEntityId;
            AuthoritativeTick = authoritativeTick;
            ReasonCode = reasonCode;
            Details = details;
        }
    }

    public interface IIntentGateRejectionSink
    {
        void OnRejected(IntentGateRejection rejection);
    }

    // --------------------------------------------------------------------
    // Validation Snapshot Shape
    // --------------------------------------------------------------------

    public sealed class CombatStateSnapshot
    {
        // Deterministic ordering: keys are stored sorted by entity_id.
        public IReadOnlyList<CombatStateSnapshotRow> Rows { get; }

        private CombatStateSnapshot(IReadOnlyList<CombatStateSnapshotRow> rows)
        {
            Rows = rows;
        }

        public static CombatStateSnapshot Capture(Dictionary<string, CombatEntityState> statesByEntityId)
        {
            var rows = new List<CombatStateSnapshotRow>(statesByEntityId.Count);

            foreach (var kv in statesByEntityId)
            {
                var s = kv.Value;
                rows.Add(new CombatStateSnapshotRow(
                    entityId: s.EntityId,
                    state: s.State,
                    combatContextId: s.CombatContextId,
                    committedIntentId: s.CommittedIntentId ?? string.Empty,
                    stateChangeTick: s.StateChangeTick
                ));
            }

            rows.Sort((a, b) => StringComparer.Ordinal.Compare(a.EntityId, b.EntityId));
            return new CombatStateSnapshot(new ReadOnlyCollection<CombatStateSnapshotRow>(rows));
        }
    }

    public readonly struct CombatStateSnapshotRow
    {
        public readonly string EntityId;
        public readonly CombatState State;
        public readonly string CombatContextId;
        public readonly string CommittedIntentId;
        public readonly int StateChangeTick;

        public CombatStateSnapshotRow(string entityId, CombatState state, string combatContextId, string committedIntentId, int stateChangeTick)
        {
            EntityId = entityId;
            State = state;
            CombatContextId = combatContextId;
            CommittedIntentId = committedIntentId;
            StateChangeTick = stateChangeTick;
        }
    }

    // --------------------------------------------------------------------
    // Dependencies (must be satisfied by existing runtime)
    // --------------------------------------------------------------------

    public interface ITickSource
    {
        int CurrentTick { get; }
    }

    public interface IEntityIdValidator
    {
        bool IsValidEntityId(string entityId);
    }

    // These types are produced by Stage 12.1 and consumed here.
    // They are declared here only to make this file self-contained; in-project, reference the existing definitions.
    public enum CombatIntentType
    {
        CombatAttackIntent,
        CombatDefendIntent,
        CombatAbilityIntent,
        CombatMovementIntent,
        CombatInteractIntent,
        CombatCancelIntent
    }

    public sealed class FrozenQueueSnapshot
    {
        public int AuthoritativeTick { get; }
        public IReadOnlyList<FrozenIntentRecord> Intents { get; }

        public FrozenQueueSnapshot(int authoritativeTick, IReadOnlyList<FrozenIntentRecord> intents)
        {
            AuthoritativeTick = authoritativeTick;
            Intents = intents ?? throw new ArgumentNullException(nameof(intents));
        }
    }

    public readonly struct FrozenIntentRecord
    {
        public readonly string IntentId;
        public readonly CombatIntentType IntentType;
        public readonly string ActorEntityId;
        public readonly int SubmitTick;
        public readonly int DeterministicSequence;
        public readonly IReadOnlyDictionary<string, object?> Payload;

        public FrozenIntentRecord(
            string intentId,
            CombatIntentType intentType,
            string actorEntityId,
            int submitTick,
            int deterministicSequence,
            IReadOnlyDictionary<string, object?> payload)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntityId = actorEntityId;
            SubmitTick = submitTick;
            DeterministicSequence = deterministicSequence;
            Payload = payload;
        }
    }
}
