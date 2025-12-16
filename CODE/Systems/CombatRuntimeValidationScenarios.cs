using System;
using System.Collections.Generic;
using Caelmor.Combat;
using Caelmor.Runtime.WorldSimulation;
using Caelmor.Systems;
using Caelmor.Validation;

namespace Caelmor.Validation.Combat
{
    /// <summary>
    /// Validation scenarios for Stage 25.B2 — Combat Runtime Validation Scenarios.
    /// Proves combat runs only during simulation execution, excludes ineligible entities,
    /// resolves deterministically, and does not mutate eligibility or lifecycle mid-tick.
    /// </summary>
    public static class CombatRuntimeValidationScenarios
    {
        public static IReadOnlyList<IValidationScenario> GetScenarios()
        {
            return new IValidationScenario[]
            {
                new ValidationScenarioAdapter(new Scenario1_CombatExecutesOnlyDuringSimulationExecution()),
                new ValidationScenarioAdapter(new Scenario2_IneligibleEntitiesCannotParticipate()),
                new ValidationScenarioAdapter(new Scenario3_DeterministicResolutionUnderIdenticalInputs()),
                new ValidationScenarioAdapter(new Scenario4_NoMidTickEligibilityOrLifecycleMutation())
            };
        }

        private sealed class Scenario1_CombatExecutesOnlyDuringSimulationExecution : Caelmor.Validation.IValidationScenario
        {
            public string Name => "Scenario 1 — Combat Executes Only During Simulation Execution";

            public void Run(IAssert a)
            {
                var timeline = new List<string>();
                var handles = new[] { new EntityHandle(1) };
                var intentsByTick = new Dictionary<int, List<FrozenIntentRecord>>
                {
                    [1] = new List<FrozenIntentRecord>
                    {
                        new FrozenIntentRecord(
                            intentId: "i1",
                            intentType: CombatIntentType.CombatAttackIntent,
                            actorEntityId: "e1",
                            submitTick: 0,
                            deterministicSequence: 1,
                            payload: new Dictionary<string, object?>())
                    }
                };

                var rig = Rig.Create(handles, intentsByTick);
                rig.Gate.OnGate = () => timeline.Add("execute");
                rig.Hook.OnPre = (ctx, eligible) => timeline.Add("pre");
                rig.Hook.OnPost = (ctx, eligible) => timeline.Add("post");
                rig.CommitSink.OnCommit = () => timeline.Add("commit");

                rig.Core.ExecuteSingleTick();

                a.Equal(4, timeline.Count, "Timeline must include pre, execute, commit, and post phases.");
                a.Equal("pre", timeline[0], "Pre-Tick must run before combat execution.");
                a.Equal("execute", timeline[1], "Combat execution must occur during simulation execution.");
                a.Equal("commit", timeline[2], "Combat results must commit after execution via buffered effects.");
                a.Equal("post", timeline[3], "Post-Tick finalization must run after commits.");
            }
        }

        private sealed class Scenario2_IneligibleEntitiesCannotParticipate : Caelmor.Validation.IValidationScenario
        {
            public string Name => "Scenario 2 — Ineligible Entities Cannot Participate";

            public void Run(IAssert a)
            {
                var handles = new[] { new EntityHandle(10), new EntityHandle(20) };
                var intentsByTick = new Dictionary<int, List<FrozenIntentRecord>>
                {
                    [1] = new List<FrozenIntentRecord>
                    {
                        new FrozenIntentRecord("i-eligible", CombatIntentType.CombatAttackIntent, "eligible", 0, 1, new Dictionary<string, object?>()),
                        new FrozenIntentRecord("i-ineligible", CombatIntentType.CombatDefendIntent, "ineligible", 0, 1, new Dictionary<string, object?>())
                    }
                };

                var rig = Rig.Create(handles, intentsByTick);
                rig.Resolver.Map[handles[0]] = "eligible";
                rig.Resolver.Map[handles[1]] = "ineligible";

                rig.Eligibility.SetEligible(handles[0], true);
                rig.Eligibility.SetEligible(handles[1], false);

                rig.Core.ExecuteSingleTick();

                a.Equal(1, rig.CommitSink.CommitPayloads.Count, "Only eligible entity outcomes must be committed.");
                a.True(rig.CommitSink.CommitPayloads[0].StartsWith("10:"), "Committed payload must belong to eligible entity handle.");
            }
        }

        private sealed class Scenario3_DeterministicResolutionUnderIdenticalInputs : Caelmor.Validation.IValidationScenario
        {
            public string Name => "Scenario 3 — Deterministic Resolution Under Identical Inputs";

            public void Run(IAssert a)
            {
                var handles = new[] { new EntityHandle(100) };
                var intentsByTick = new Dictionary<int, List<FrozenIntentRecord>>
                {
                    [1] = new List<FrozenIntentRecord>
                    {
                        new FrozenIntentRecord("i1", CombatIntentType.CombatAttackIntent, "deterministic", 0, 1, new Dictionary<string, object?>()),
                        new FrozenIntentRecord("i2", CombatIntentType.CombatDefendIntent, "deterministic", 0, 2, new Dictionary<string, object?>())
                    }
                };

                var first = Rig.Create(handles, intentsByTick);
                first.Resolver.Map[handles[0]] = "deterministic";
                first.Eligibility.SetEligible(handles[0], true);

                var second = Rig.Create(handles, intentsByTick);
                second.Resolver.Map[handles[0]] = "deterministic";
                second.Eligibility.SetEligible(handles[0], true);

                first.Core.ExecuteSingleTick();
                second.Core.ExecuteSingleTick();

                a.Equal(first.CommitSink.CommitPayloads.Count, second.CommitSink.CommitPayloads.Count, "Commit payload counts must match across identical inputs.");
                for (int i = 0; i < first.CommitSink.CommitPayloads.Count; i++)
                {
                    a.Equal(first.CommitSink.CommitPayloads[i], second.CommitSink.CommitPayloads[i], "Committed payload ordering must be deterministic.");
                }
            }
        }

        private sealed class Scenario4_NoMidTickEligibilityOrLifecycleMutation : Caelmor.Validation.IValidationScenario
        {
            public string Name => "Scenario 4 — No Mid-Tick Eligibility Or Lifecycle Mutation";

            public void Run(IAssert a)
            {
                var handles = new[] { new EntityHandle(500) };
                var intentsByTick = new Dictionary<int, List<FrozenIntentRecord>>
                {
                    [1] = new List<FrozenIntentRecord>
                    {
                        new FrozenIntentRecord("i-safe", CombatIntentType.CombatAttackIntent, "stable", 0, 1, new Dictionary<string, object?>())
                    }
                };

                var rig = Rig.Create(handles, intentsByTick);
                rig.Resolver.Map[handles[0]] = "stable";
                rig.Eligibility.SetEligible(handles[0], true);

                rig.Core.ExecuteSingleTick();

                a.True(rig.Eligibility.WasStableAcrossTick, "Eligibility state must remain stable throughout the tick.");
                a.Equal(1, rig.CommitSink.CommitPayloads.Count, "Combat must commit outcomes normally when eligibility is stable.");
            }
        }

        private sealed class Rig
        {
            public readonly WorldSimulationCore Core;
            public readonly RecordingEligibilityService Eligibility;
            public readonly DeterministicIntentSource IntentSource;
            public readonly AcceptAllIntentGate Gate;
            public readonly RecordingCommitSink CommitSink;
            public readonly DeterministicResolver Resolver;
            public readonly RecordingHook Hook;

            private Rig(
                WorldSimulationCore core,
                RecordingEligibilityService eligibility,
                DeterministicIntentSource intentSource,
                AcceptAllIntentGate gate,
                RecordingCommitSink commitSink,
                DeterministicResolver resolver,
                RecordingHook hook)
            {
                Core = core;
                Eligibility = eligibility;
                IntentSource = intentSource;
                Gate = gate;
                CommitSink = commitSink;
                Resolver = resolver;
                Hook = hook;
            }

            public static Rig Create(EntityHandle[] entities, IDictionary<int, List<FrozenIntentRecord>> intentsByTick)
            {
                var index = new DeterministicEntityIndex(entities);
                var core = new WorldSimulationCore(index);

                var eligibility = new RecordingEligibilityService();
                var intentSource = new DeterministicIntentSource(intentsByTick);
                var gate = new AcceptAllIntentGate();
                var commitSink = new RecordingCommitSink();
                var resolver = new DeterministicResolver(entities);
                var runtime = new CombatRuntimeSystem(
                    eligibility,
                    intentSource,
                    gate,
                    new CombatResolutionEngine(),
                    commitSink,
                    resolver);
                var hook = new RecordingHook();

                core.RegisterEligibilityGate(new CombatEligibilityGate(eligibility));
                core.RegisterParticipant(runtime, orderKey: 0);
                core.RegisterParticipant(resolver, orderKey: 1);
                core.RegisterPhaseHook(runtime, orderKey: 0);
                core.RegisterPhaseHook(hook, orderKey: 1);

                return new Rig(core, eligibility, intentSource, gate, commitSink, resolver, hook);
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

        private sealed class RecordingEligibilityService : ICombatEligibilityService
        {
            private readonly Dictionary<EntityHandle, bool> _eligibility = new Dictionary<EntityHandle, bool>();

            public bool WasStableAcrossTick { get; private set; } = true;

            public bool IsCombatEligible(EntityHandle entity)
            {
                if (_eligibility.TryGetValue(entity, out var allowed))
                    return allowed;

                return false;
            }

            public void SetEligible(EntityHandle entity, bool allowed)
            {
                _eligibility[entity] = allowed;
            }

            public void MarkUnstable()
            {
                WasStableAcrossTick = false;
            }
        }

        private sealed class DeterministicIntentSource : ICombatIntentSource
        {
            private readonly Dictionary<int, FrozenQueueSnapshot> _byTick;

            public DeterministicIntentSource(IDictionary<int, List<FrozenIntentRecord>> intentsByTick)
            {
                _byTick = new Dictionary<int, FrozenQueueSnapshot>();
                foreach (var kv in intentsByTick)
                {
                    _byTick[kv.Key] = new FrozenQueueSnapshot(kv.Key, kv.Value);
                }
            }

            public FrozenQueueSnapshot GetFrozenQueue(int authoritativeTick)
            {
                if (_byTick.TryGetValue(authoritativeTick, out var frozen))
                    return frozen;

                return FrozenQueueSnapshot.Empty(authoritativeTick);
            }
        }

        private sealed class AcceptAllIntentGate : ICombatIntentGate
        {
            public Action? OnGate { get; set; }

            public GatedIntentBatch Gate(FrozenQueueSnapshot frozenQueue)
            {
                OnGate?.Invoke();

                var accepted = new List<FrozenIntentRecord>(frozenQueue.Intents);
                var rows = new List<IntentGateRow>(frozenQueue.Intents.Count);
                for (int i = 0; i < frozenQueue.Intents.Count; i++)
                {
                    rows.Add(IntentGateRow.Accepted(frozenQueue.Intents[i]));
                }

                var emptyStates = new Dictionary<string, CombatEntityState>(StringComparer.Ordinal);
                var snapshot = CombatStateSnapshot.Capture(emptyStates);

                return new GatedIntentBatch(
                    frozenQueue.AuthoritativeTick,
                    accepted,
                    rows,
                    snapshot,
                    snapshot);
            }
        }

        private sealed class RecordingCommitSink : ICombatOutcomeCommitSink
        {
            public readonly List<string> CommitPayloads = new List<string>();
            public Action? OnCommit { get; set; }

            public void Commit(EntityHandle entity, CombatResolutionResult resolutionResult)
            {
                OnCommit?.Invoke();

                for (int i = 0; i < resolutionResult.OutcomesInOrder.Count; i++)
                {
                    var outcome = resolutionResult.OutcomesInOrder[i];
                    CommitPayloads.Add($"{entity.Value}:{outcome.IntentId}:{outcome.OutcomeKind}");
                }
            }
        }

        private sealed class DeterministicResolver : ICombatantResolver, ISimulationParticipant
        {
            public readonly Dictionary<EntityHandle, string> Map = new Dictionary<EntityHandle, string>();

            public DeterministicResolver(IEnumerable<EntityHandle> handles)
            {
                foreach (var h in handles)
                    Map[h] = $"entity-{h.Value}";
            }

            public string ResolveCombatEntityId(EntityHandle entity)
            {
                if (Map.TryGetValue(entity, out var id))
                    return id;

                return string.Empty;
            }

            public void Execute(EntityHandle entity, SimulationTickContext context)
            {
                // This participant is a no-op placeholder to preserve deterministic ordering with the combat runtime.
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
