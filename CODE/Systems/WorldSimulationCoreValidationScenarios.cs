using System;
using System.Collections.Generic;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.WorldSimulation;
using Caelmor.Systems;
using Caelmor.Validation;

namespace Caelmor.Validation.WorldSimulation
{
    /// <summary>
    /// Validation scenarios for Stage 28.B2 — World Simulation Core Validation Scenarios.
    /// Uses deterministic fakes to prove phase ordering, eligibility gating, invariant enforcement,
    /// and side-effect containment.
    /// </summary>
    public static class WorldSimulationCoreValidationScenarios
    {
        public static IReadOnlyList<IValidationScenario> GetScenarios()
        {
            return new IValidationScenario[]
            {
                new ValidationScenarioAdapter(new Scenario1_TickPhasesExecuteInOrder()),
                new ValidationScenarioAdapter(new Scenario2_EligibilityEvaluatedPreTickOnly()),
                new ValidationScenarioAdapter(new Scenario3_MidTickEligibilityChangeRejected()),
                new ValidationScenarioAdapter(new Scenario4_DeterministicExecutionOrder()),
                new ValidationScenarioAdapter(new Scenario5_NonEligibleEntitiesAreExcluded()),
                new ValidationScenarioAdapter(new Scenario6_NoSideEffectsEscapeTickBoundary())
            };
        }

        private sealed class Scenario1_TickPhasesExecuteInOrder : Caelmor.Validation.IValidationScenario
        {
            public string Name => "Scenario 1 — Tick Phases Execute In Order";

            public void Run(IAssert a)
            {
                var log = new List<string>();
                var rig = Rig.Create(new[] { new EntityHandle(1) });

                rig.Hook.OnPre = (ctx, eligible) => log.Add("pre");
                rig.Hook.OnPost = (ctx, eligible) => log.Add("post");
                rig.Participant.OnExecute = (entity, ctx) => log.Add("simulate");

                rig.Core.ExecuteSingleTick();

                a.Equal(3, log.Count, "Exactly three phase markers must be recorded.");
                a.Equal("pre", log[0], "Pre-Tick Gate Evaluation must run first.");
                a.Equal("simulate", log[1], "Simulation execution must follow pre-tick.");
                a.Equal("post", log[2], "Post-Tick finalization must run last.");
            }
        }

        private sealed class Scenario2_EligibilityEvaluatedPreTickOnly : Caelmor.Validation.IValidationScenario
        {
            public string Name => "Scenario 2 — Eligibility Evaluated Pre-Tick Only";

            public void Run(IAssert a)
            {
                var timeline = new List<string>();
                var rig = Rig.Create(new[] { new EntityHandle(1), new EntityHandle(2) });

                var gate = new RecordingGate("gate", timeline);
                rig.Core.RegisterEligibilityGate(gate);

                rig.Hook.OnPre = (ctx, eligible) => timeline.Add("pre");
                rig.Participant.OnExecute = (entity, ctx) => timeline.Add($"simulate:{entity.Value}");
                rig.Hook.OnPost = (ctx, eligible) => timeline.Add("post");

                rig.Core.ExecuteSingleTick();

                // Two gate evaluations per entity: one during pre-tick gating, one during stability enforcement.
                a.Equal(8, timeline.Count, "Timeline should include gating, pre, simulation, stability checks, and post.");
                a.Equal("gate:1", timeline[0], "Gate must evaluate before any hooks for entity 1.");
                a.Equal("gate:2", timeline[1], "Gate must evaluate before any hooks for entity 2.");
                a.Equal("pre", timeline[2], "Pre hook must run after gating.");
                a.Equal("simulate:1", timeline[3], "Simulation must use pre-evaluated eligibility for entity 1.");
                a.Equal("simulate:2", timeline[4], "Simulation must use pre-evaluated eligibility for entity 2.");
                a.Equal("gate:1", timeline[5], "Stability enforcement must re-check eligibility deterministically for entity 1.");
                a.Equal("gate:2", timeline[6], "Stability enforcement must re-check eligibility deterministically for entity 2.");
                a.Equal("post", timeline[7], "Post hook must conclude after stability enforcement.");
            }
        }

        private sealed class Scenario3_MidTickEligibilityChangeRejected : Caelmor.Validation.IValidationScenario
        {
            public string Name => "Scenario 3 — Mid-Tick Eligibility Change Rejected";

            public void Run(IAssert a)
            {
                var rig = Rig.Create(new[] { new EntityHandle(3) });
                var mutableGate = new MutableGate(true);
                rig.Core.RegisterEligibilityGate(mutableGate);
                var effectMarker = new EffectFlagMarker();

                rig.Participant.OnExecute = (entity, ctx) =>
                {
                    mutableGate.IsAllowed = false; // Attempt to revoke eligibility mid-tick.
                    ctx.BufferEffect(SimulationEffectCommand.FlagSignal(effectMarker, label: "effect"));
                };

                try
                {
                    rig.Core.ExecuteSingleTick();
                    a.False(true, "Tick must fail when eligibility changes mid-tick.");
                }
                catch (InvalidOperationException)
                {
                    // Expected invariant violation.
                }

                a.False(effectMarker.IsMarked, "Buffered effects must not commit when invariants are violated.");
            }
        }

        private sealed class Scenario4_DeterministicExecutionOrder : Caelmor.Validation.IValidationScenario
        {
            public string Name => "Scenario 4 — Deterministic Execution Order";

            public void Run(IAssert a)
            {
                var firstRun = RunOrderedTick();
                var secondRun = RunOrderedTick();

                a.Equal(firstRun.Count, secondRun.Count, "Execution trace counts must match.");
                for (int i = 0; i < firstRun.Count; i++)
                {
                    a.Equal(firstRun[i], secondRun[i], "Execution order must be identical across runs.");
                }
            }

            private static List<string> RunOrderedTick()
            {
                var rig = Rig.Create(new[] { new EntityHandle(10), new EntityHandle(20) });
                rig.Gate.IsAllowed = true;

                var p1 = new RecordingParticipant("p1");
                var p2 = new RecordingParticipant("p2");
                rig.Core.RegisterParticipant(p1, orderKey: 1);
                rig.Core.RegisterParticipant(p2, orderKey: 2);

                rig.Core.ExecuteSingleTick();

                var trace = new List<string>();
                trace.AddRange(p1.Executions);
                trace.AddRange(p2.Executions);
                return trace;
            }
        }

        private sealed class Scenario5_NonEligibleEntitiesAreExcluded : Caelmor.Validation.IValidationScenario
        {
            public string Name => "Scenario 5 — Non-Eligible Entities Are Excluded";

            public void Run(IAssert a)
            {
                var rig = Rig.Create(new[] { new EntityHandle(100), new EntityHandle(200) });
                rig.Gate.AllowedPredicate = e => e.Value == 100;

                var executed = new List<int>();
                rig.Participant.OnExecute = (entity, ctx) => executed.Add(entity.Value);

                rig.Core.ExecuteSingleTick();

                a.Equal(1, executed.Count, "Only one entity should be simulated.");
                a.Equal(100, executed[0], "Only eligible entity must be simulated.");
            }
        }

        private sealed class Scenario6_NoSideEffectsEscapeTickBoundary : Caelmor.Validation.IValidationScenario
        {
            public string Name => "Scenario 6 — No Side Effects Escape Tick Boundary";

            public void Run(IAssert a)
            {
                var log = new List<string>();
                var rig = Rig.Create(new[] { new EntityHandle(500) });

                rig.Hook.OnPre = (ctx, eligible) => log.Add("pre");
                rig.Hook.OnPost = (ctx, eligible) => log.Add("post");
                rig.Participant.OnExecute = (entity, ctx) =>
                {
                    log.Add("simulate");
                    ctx.BufferEffect(SimulationEffectCommand.AppendLog(log, entry: "commit", label: "commit"));
                };

                rig.Core.ExecuteSingleTick();

                a.Equal(4, log.Count, "Log must include pre, simulate, commit, post.");
                a.Equal("pre", log[0], "Pre phase must execute first.");
                a.Equal("simulate", log[1], "Simulation must execute after pre.");
                a.Equal("commit", log[2], "Side effects must commit at tick end only.");
                a.Equal("post", log[3], "Post-tick finalization must complete after commits.");
            }
        }

        private sealed class Rig
        {
            public readonly WorldSimulationCore Core;
            public readonly DeterministicEntityIndex Index;
            public readonly ConfigurableGate Gate;
            public readonly RecordingParticipant Participant;
            public readonly RecordingHook Hook;

            private Rig(WorldSimulationCore core, DeterministicEntityIndex index, ConfigurableGate gate, RecordingParticipant participant, RecordingHook hook)
            {
                Core = core;
                Index = index;
                Gate = gate;
                Participant = participant;
                Hook = hook;
            }

            public static Rig Create(EntityHandle[] entities)
            {
                var index = new DeterministicEntityIndex(entities);
                var core = new WorldSimulationCore(index);
                var gate = new ConfigurableGate();
                var participant = new RecordingParticipant("default");
                var hook = new RecordingHook();

                core.RegisterEligibilityGate(gate);
                core.RegisterParticipant(participant, orderKey: 0);
                core.RegisterPhaseHook(hook, orderKey: 0);

                return new Rig(core, index, gate, participant, hook);
            }
        }

        private sealed class DeterministicEntityIndex : ISimulationEntityIndex
        {
            private readonly EntityHandle[] _entities;

            public DeterministicEntityIndex(EntityHandle[] entities)
            {
                _entities = entities ?? Array.Empty<EntityHandle>();
            }

            public EntityHandle[] SnapshotEntitiesDeterministic() => (EntityHandle[])_entities.Clone();
        }

        private sealed class ConfigurableGate : ISimulationEligibilityGate
        {
            public string Name => "configurable";

            public Func<EntityHandle, bool>? AllowedPredicate { get; set; }
            public bool IsAllowed { get; set; } = true;

            public bool IsEligible(EntityHandle entity)
            {
                if (AllowedPredicate != null)
                    return AllowedPredicate(entity);

                return IsAllowed;
            }
        }

        private sealed class RecordingGate : ISimulationEligibilityGate
        {
            private readonly List<string> _timeline;

            public RecordingGate(string name, List<string> timeline)
            {
                Name = name;
                _timeline = timeline;
            }

            public string Name { get; }

            public bool IsEligible(EntityHandle entity)
            {
                _timeline.Add($"{Name}:{entity.Value}");
                return true;
            }
        }

        private sealed class MutableGate : ISimulationEligibilityGate
        {
            public MutableGate(bool initial)
            {
                IsAllowed = initial;
            }

            public string Name => "mutable";

            public bool IsAllowed { get; set; }

            public bool IsEligible(EntityHandle entity) => IsAllowed;
        }

        private sealed class RecordingParticipant : ISimulationParticipant
        {
            private readonly string _label;
            public readonly List<string> Executions = new List<string>();

            public RecordingParticipant(string label)
            {
                _label = label;
            }

            public Action<EntityHandle, SimulationTickContext>? OnExecute { get; set; }

            public void Execute(EntityHandle entity, SimulationTickContext context)
            {
                Executions.Add($"{_label}:{entity.Value}");
                OnExecute?.Invoke(entity, context);
            }
        }

        private sealed class RecordingHook : ITickPhaseHook
        {
            public Action<SimulationTickContext, IReadOnlyList<EntityHandle>>? OnPre { get; set; }
            public Action<SimulationTickContext, IReadOnlyList<EntityHandle>>? OnPost { get; set; }

            public void OnPreTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
            {
                OnPre?.Invoke(context, eligibleEntities);
            }

            public void OnPostTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
            {
                OnPost?.Invoke(context, eligibleEntities);
            }
        }
    }
}
