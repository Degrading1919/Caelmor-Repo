// CombatResolutionEngine.cs
// NOTE: Save location must follow existing project structure.
// This file implements CombatResolutionEngine only.
// No state mutation, no damage application, no events, no persistence.

using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace Caelmor.Combat
{
    /// <summary>
    /// CombatResolutionEngine
    ///
    /// Responsibilities:
    /// - Consume ordered, validated intents (Stage 12.2)
    /// - Execute canonical resolution order (Stage 10.3)
    /// - Produce CombatOutcome records ONLY (Stage 11.2 schemas)
    ///
    /// Hard guarantees:
    /// - Stateless and side-effect free
    /// - Deterministic (same inputs → same outputs)
    /// - No combat state mutation
    /// - No damage application
    /// - No mitigation application
    /// - No event emission
    /// - No persistence
    /// </summary>
    public sealed class CombatResolutionEngine
    {
        public CombatResolutionResult Resolve(GatedIntentBatch gatedBatch)
        {
            if (gatedBatch == null) throw new ArgumentNullException(nameof(gatedBatch));

            // Pre-resolution snapshot for validation
            var preSnapshot = CombatResolutionSnapshot.CapturePre(
                gatedBatch.AuthoritativeTick,
                gatedBatch.AcceptedIntentsInOrder
            );

            var outcomes = new List<CombatOutcome>(capacity: gatedBatch.AcceptedIntentsInOrder.Count);

            // Resolution proceeds strictly in accepted intent order
            for (int i = 0; i < gatedBatch.AcceptedIntentsInOrder.Count; i++)
            {
                var intent = gatedBatch.AcceptedIntentsInOrder[i];

                // Resolution must never short-circuit.
                // Each intent is processed deterministically.
                var outcome = ResolveSingleIntent(intent, gatedBatch.AuthoritativeTick);

                outcomes.Add(outcome);
            }

            // Post-resolution snapshot for validation
            var postSnapshot = CombatResolutionSnapshot.CapturePost(
                gatedBatch.AuthoritativeTick,
                outcomes
            );

            return new CombatResolutionResult(
                authoritativeTick: gatedBatch.AuthoritativeTick,
                outcomesInOrder: new ReadOnlyCollection<CombatOutcome>(outcomes),
                preResolutionSnapshot: preSnapshot,
                postResolutionSnapshot: postSnapshot
            );
        }

        private static CombatOutcome ResolveSingleIntent(
            FrozenIntentRecord intent,
            int authoritativeTick)
        {
            // Dispatch strictly by intent type.
            // No state inspection, no mutation, no external reads.
            switch (intent.IntentType)
            {
                case CombatIntentType.CombatAttackIntent:
                    return ResolveAttack(intent, authoritativeTick);

                case CombatIntentType.CombatDefendIntent:
                    return ResolveDefend(intent, authoritativeTick);

                case CombatIntentType.CombatAbilityIntent:
                    return ResolveAbility(intent, authoritativeTick);

                case CombatIntentType.CombatMovementIntent:
                    return ResolveMovement(intent, authoritativeTick);

                case CombatIntentType.CombatInteractIntent:
                    return ResolveInteract(intent, authoritativeTick);

                case CombatIntentType.CombatCancelIntent:
                    return ResolveCancel(intent, authoritativeTick);

                default:
                    throw new InvalidOperationException(
                        $"Unhandled CombatIntentType during resolution: {intent.IntentType}");
            }
        }

        // ------------------------------------------------------------------
        // Intent-specific resolution (OUTCOME CONSTRUCTION ONLY)
        // ------------------------------------------------------------------

        private static CombatOutcome ResolveAttack(FrozenIntentRecord intent, int tick)
        {
            return CombatOutcome.IntentResolved(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntityId: intent.ActorEntityId,
                authoritativeTick: tick,
                outcomeKind: CombatOutcomeKind.AttackProposed
            );
        }

        private static CombatOutcome ResolveDefend(FrozenIntentRecord intent, int tick)
        {
            return CombatOutcome.IntentResolved(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntityId: intent.ActorEntityId,
                authoritativeTick: tick,
                outcomeKind: CombatOutcomeKind.DefenseProposed
            );
        }

        private static CombatOutcome ResolveAbility(FrozenIntentRecord intent, int tick)
        {
            return CombatOutcome.IntentResolved(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntityId: intent.ActorEntityId,
                authoritativeTick: tick,
                outcomeKind: CombatOutcomeKind.AbilityProposed
            );
        }

        private static CombatOutcome ResolveMovement(FrozenIntentRecord intent, int tick)
        {
            return CombatOutcome.IntentResolved(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntityId: intent.ActorEntityId,
                authoritativeTick: tick,
                outcomeKind: CombatOutcomeKind.MovementProposed
            );
        }

        private static CombatOutcome ResolveInteract(FrozenIntentRecord intent, int tick)
        {
            return CombatOutcome.IntentResolved(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntityId: intent.ActorEntityId,
                authoritativeTick: tick,
                outcomeKind: CombatOutcomeKind.InteractionProposed
            );
        }

        private static CombatOutcome ResolveCancel(FrozenIntentRecord intent, int tick)
        {
            return CombatOutcome.IntentResolved(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntityId: intent.ActorEntityId,
                authoritativeTick: tick,
                outcomeKind: CombatOutcomeKind.CancellationEvaluated
            );
        }
    }

    // ------------------------------------------------------------------
    // Resolution Outputs
    // ------------------------------------------------------------------

    public sealed class CombatResolutionResult
    {
        public int AuthoritativeTick { get; }
        public IReadOnlyList<CombatOutcome> OutcomesInOrder { get; }
        public CombatResolutionSnapshot PreResolutionSnapshot { get; }
        public CombatResolutionSnapshot PostResolutionSnapshot { get; }

        public CombatResolutionResult(
            int authoritativeTick,
            IReadOnlyList<CombatOutcome> outcomesInOrder,
            CombatResolutionSnapshot preResolutionSnapshot,
            CombatResolutionSnapshot postResolutionSnapshot)
        {
            AuthoritativeTick = authoritativeTick;
            OutcomesInOrder = outcomesInOrder ?? throw new ArgumentNullException(nameof(outcomesInOrder));
            PreResolutionSnapshot = preResolutionSnapshot ?? throw new ArgumentNullException(nameof(preResolutionSnapshot));
            PostResolutionSnapshot = postResolutionSnapshot ?? throw new ArgumentNullException(nameof(postResolutionSnapshot));
        }
    }

    // ------------------------------------------------------------------
    // CombatOutcome (Schema-conformant, no application)
    // ------------------------------------------------------------------

    public sealed class CombatOutcome
    {
        public string IntentId { get; }
        public CombatIntentType IntentType { get; }
        public string ActorEntityId { get; }
        public int AuthoritativeTick { get; }
        public CombatOutcomeKind OutcomeKind { get; }

        private CombatOutcome(
            string intentId,
            CombatIntentType intentType,
            string actorEntityId,
            int authoritativeTick,
            CombatOutcomeKind outcomeKind)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntityId = actorEntityId;
            AuthoritativeTick = authoritativeTick;
            OutcomeKind = outcomeKind;
        }

        public static CombatOutcome IntentResolved(
            string intentId,
            CombatIntentType intentType,
            string actorEntityId,
            int authoritativeTick,
            CombatOutcomeKind outcomeKind)
        {
            if (string.IsNullOrWhiteSpace(intentId))
                throw new InvalidOperationException("CombatOutcome requires intent_id.");

            return new CombatOutcome(
                intentId,
                intentType,
                actorEntityId,
                authoritativeTick,
                outcomeKind
            );
        }
    }

    public enum CombatOutcomeKind
    {
        AttackProposed,
        DefenseProposed,
        AbilityProposed,
        MovementProposed,
        InteractionProposed,
        CancellationEvaluated
    }

    // ------------------------------------------------------------------
    // Validation Snapshots
    // ------------------------------------------------------------------

    public sealed class CombatResolutionSnapshot
    {
        public int AuthoritativeTick { get; }
        public IReadOnlyList<string> OrderedIntentIds { get; }
        public IReadOnlyList<string> OrderedOutcomeIntentIds { get; }

        private CombatResolutionSnapshot(
            int authoritativeTick,
            IReadOnlyList<string> orderedIntentIds,
            IReadOnlyList<string> orderedOutcomeIntentIds)
        {
            AuthoritativeTick = authoritativeTick;
            OrderedIntentIds = orderedIntentIds;
            OrderedOutcomeIntentIds = orderedOutcomeIntentIds;
        }

        public static CombatResolutionSnapshot CapturePre(
            int tick,
            IReadOnlyList<FrozenIntentRecord> intents)
        {
            var ids = new List<string>(intents.Count);
            for (int i = 0; i < intents.Count; i++)
                ids.Add(intents[i].IntentId);

            return new CombatResolutionSnapshot(
                tick,
                new ReadOnlyCollection<string>(ids),
                Array.Empty<string>()
            );
        }

        public static CombatResolutionSnapshot CapturePost(
            int tick,
            IReadOnlyList<CombatOutcome> outcomes)
        {
            var ids = new List<string>(outcomes.Count);
            for (int i = 0; i < outcomes.Count; i++)
                ids.Add(outcomes[i].IntentId);

            return new CombatResolutionSnapshot(
                tick,
                Array.Empty<string>(),
                new ReadOnlyCollection<string>(ids)
            );
        }
    }

    // ------------------------------------------------------------------
    // Dependencies (existing runtime definitions)
    // ------------------------------------------------------------------

    public enum CombatIntentType
    {
        CombatAttackIntent,
        CombatDefendIntent,
        CombatAbilityIntent,
        CombatMovementIntent,
        CombatInteractIntent,
        CombatCancelIntent
    }

    public sealed class FrozenIntentRecord
    {
        public string IntentId { get; }
        public CombatIntentType IntentType { get; }
        public string ActorEntityId { get; }

        public FrozenIntentRecord(
            string intentId,
            CombatIntentType intentType,
            string actorEntityId)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntityId = actorEntityId;
        }
    }

    public sealed class GatedIntentBatch
    {
        public int AuthoritativeTick { get; }
        public IReadOnlyList<FrozenIntentRecord> AcceptedIntentsInOrder { get; }

        public GatedIntentBatch(int authoritativeTick, IReadOnlyList<FrozenIntentRecord> accepted)
        {
            AuthoritativeTick = authoritativeTick;
            AcceptedIntentsInOrder = accepted;
        }
    }
}
