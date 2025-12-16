using System;
using System.Collections.Generic;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.WorldSimulation;

namespace Caelmor.Combat
{
    /// <summary>
    /// CombatRuntimeSystem
    ///
    /// Responsibilities (Stage 25.B):
    /// - Executes combat strictly during the Simulation Execution phase
    /// - Consumes locked combat intents and combat state gate outputs
    /// - Enforces combat eligibility via pre-tick gates (no mid-tick mutation)
    /// - Resolves combat deterministically using CombatResolutionEngine
    /// - Commits resolution outputs atomically via buffered effects (post-resolution)
    ///
    /// Prohibitions:
    /// - Does not modify lifecycle, residency, restore, or eligibility state
    /// - Does not perform persistence I/O
    /// - Does not add AI or input handling
    /// - Does not redefine shared identifiers
    /// </summary>
    public sealed class CombatRuntimeSystem : ISimulationParticipant, ITickPhaseHook
    {
        private readonly ICombatEligibilityService _eligibility;
        private readonly ICombatIntentSource _intentSource;
        private readonly ICombatIntentGate _intentGate;
        private readonly CombatResolutionEngine _resolutionEngine;
        private readonly ICombatOutcomeCommitSink _commitSink;
        private readonly ICombatantResolver _combatantResolver;

        private bool _executionWindowOpen;
        private long _executionWindowTick;

        public CombatRuntimeSystem(
            ICombatEligibilityService eligibility,
            ICombatIntentSource intentSource,
            ICombatIntentGate intentGate,
            CombatResolutionEngine resolutionEngine,
            ICombatOutcomeCommitSink commitSink,
            ICombatantResolver combatantResolver)
        {
            _eligibility = eligibility ?? throw new ArgumentNullException(nameof(eligibility));
            _intentSource = intentSource ?? throw new ArgumentNullException(nameof(intentSource));
            _intentGate = intentGate ?? throw new ArgumentNullException(nameof(intentGate));
            _resolutionEngine = resolutionEngine ?? throw new ArgumentNullException(nameof(resolutionEngine));
            _commitSink = commitSink ?? throw new ArgumentNullException(nameof(commitSink));
            _combatantResolver = combatantResolver ?? throw new ArgumentNullException(nameof(combatantResolver));
        }

        public void OnPreTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            _executionWindowOpen = true;
            _executionWindowTick = context.TickIndex;
        }

        public void OnPostTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            _executionWindowOpen = false;
            _executionWindowTick = 0;
        }

        /// <summary>
        /// Executes combat for a single eligible entity during the Simulation Execution phase.
        /// Deterministic ordering is inherited from the world simulation core participant ordering
        /// and the frozen intent ordering.
        /// </summary>
        public void Execute(EntityHandle entity, SimulationTickContext context)
        {
            if (!_executionWindowOpen || context.TickIndex != _executionWindowTick)
                throw new InvalidOperationException("Combat must execute only during the Simulation Execution phase.");

            if (!_eligibility.IsCombatEligible(entity))
                return;

            string entityId = _combatantResolver.ResolveCombatEntityId(entity);
            if (string.IsNullOrWhiteSpace(entityId))
                return;

            int authoritativeTick = checked((int)context.TickIndex);
            var frozen = _intentSource.GetFrozenQueue(authoritativeTick);

            if (frozen.AuthoritativeTick != authoritativeTick)
                throw new InvalidOperationException("Frozen intent queue tick does not match simulation tick.");

            var filteredIntents = FilterIntentsForEntity(frozen, entityId);
            if (filteredIntents.Count == 0)
                return;

            var filteredSnapshot = new FrozenQueueSnapshot(authoritativeTick, filteredIntents);
            var gated = _intentGate.Gate(filteredSnapshot);

            var resolution = _resolutionEngine.Resolve(gated);

            context.BufferEffect(
                label: $"combat_commit:{entity.Value}",
                commit: () => _commitSink.Commit(entity, resolution));
        }

        private static List<FrozenIntentRecord> FilterIntentsForEntity(FrozenQueueSnapshot frozen, string entityId)
        {
            var filtered = new List<FrozenIntentRecord>(capacity: frozen.Intents.Count);
            for (int i = 0; i < frozen.Intents.Count; i++)
            {
                var intent = frozen.Intents[i];
                if (string.Equals(intent.ActorEntityId, entityId, StringComparison.Ordinal))
                {
                    filtered.Add(intent);
                }
            }

            return filtered;
        }
    }

    /// <summary>
    /// Eligibility gate used by the world simulation core to enforce combat participation bounds
    /// prior to Simulation Execution. Deterministic and side-effect free.
    /// </summary>
    public sealed class CombatEligibilityGate : ISimulationEligibilityGate
    {
        private readonly ICombatEligibilityService _eligibility;

        public CombatEligibilityGate(ICombatEligibilityService eligibility)
        {
            _eligibility = eligibility ?? throw new ArgumentNullException(nameof(eligibility));
        }

        public string Name => "combat_eligibility";

        public bool IsEligible(EntityHandle entity)
        {
            return _eligibility.IsCombatEligible(entity);
        }
    }

    public interface ICombatEligibilityService
    {
        bool IsCombatEligible(EntityHandle entity);
    }

    public interface ICombatIntentSource
    {
        FrozenQueueSnapshot GetFrozenQueue(int authoritativeTick);
    }

    public interface ICombatIntentGate
    {
        GatedIntentBatch Gate(FrozenQueueSnapshot frozenQueue);
    }

    public interface ICombatOutcomeCommitSink
    {
        void Commit(EntityHandle entity, CombatResolutionResult resolutionResult);
    }

    public interface ICombatantResolver
    {
        string ResolveCombatEntityId(EntityHandle entity);
    }
}
