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

        private const int IntentFilterCapacity = 64;
        private readonly FrozenIntentRecord[] _filteredIntentBuffer = new FrozenIntentRecord[IntentFilterCapacity];

        private bool _executionWindowOpen;
        private long _executionWindowTick;

        public CombatRuntimeSystem(
            ICombatEligibilityService eligibility,
            ICombatIntentSource intentSource,
            ICombatIntentGate intentGate,
            CombatResolutionEngine resolutionEngine,
            ICombatOutcomeCommitSink commitSink)
        {
            _eligibility = eligibility ?? throw new ArgumentNullException(nameof(eligibility));
            _intentSource = intentSource ?? throw new ArgumentNullException(nameof(intentSource));
            _intentGate = intentGate ?? throw new ArgumentNullException(nameof(intentGate));
            _resolutionEngine = resolutionEngine ?? throw new ArgumentNullException(nameof(resolutionEngine));
            _commitSink = commitSink ?? throw new ArgumentNullException(nameof(commitSink));
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

            int authoritativeTick = checked((int)context.TickIndex);
            var frozenBatch = _intentSource.GetFrozenBatch(authoritativeTick);

            if (frozenBatch.AuthoritativeTick != authoritativeTick)
                throw new InvalidOperationException("Frozen intent batch tick does not match simulation tick.");

            int filteredCount = FilterIntentsForEntity(frozenBatch, entity, _filteredIntentBuffer);
            if (filteredCount == 0)
                return;

            var filteredSnapshot = new FrozenIntentBatch(authoritativeTick, _filteredIntentBuffer, filteredCount);
            var gated = _intentGate.Gate(filteredSnapshot);

            var resolution = _resolutionEngine.Resolve(gated);
            gated.Release();

            context.BufferEffect(SimulationEffectCommand.CombatOutcomeCommit(
                entity: entity,
                commitSink: _commitSink,
                resolution: resolution,
                label: "combat_commit"));
        }

        private static int FilterIntentsForEntity(FrozenIntentBatch frozen, EntityHandle entity, FrozenIntentRecord[] buffer)
        {
            int count = 0;
            for (int i = 0; i < frozen.Count; i++)
            {
                var intent = frozen[i];
                if (intent.ActorEntity.Equals(entity))
                {
                    if (count >= buffer.Length)
                        throw new InvalidOperationException("Filtered intent buffer capacity exceeded.");

                    buffer[count++] = intent;
                }
            }

            return count;
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
        FrozenIntentBatch GetFrozenBatch(int authoritativeTick);
    }

    public interface ICombatIntentGate
    {
        GatedIntentBatch Gate(FrozenIntentBatch frozenQueue);
    }

    public interface ICombatOutcomeCommitSink
    {
        void Commit(EntityHandle entity, CombatResolutionResult resolutionResult);
    }
}
