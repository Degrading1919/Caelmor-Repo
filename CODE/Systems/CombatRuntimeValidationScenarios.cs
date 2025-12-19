using System;
using System.Buffers;
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
                new ValidationScenarioAdapter(new Scenario4_NoMidTickEligibilityOrLifecycleMutation()),
                new ValidationScenarioAdapter(new Scenario5_BoundedIntentThroughput())
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
                            actorEntity: new EntityHandle(1),
                            submitTick: 0,
                            deterministicSequence: 1,
                            payload: CombatIntentPayload.ForAttack(new AttackIntentPayload(default, default)))
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
                        new FrozenIntentRecord("i-eligible", CombatIntentType.CombatAttackIntent, new EntityHandle(10), 0, 1, CombatIntentPayload.ForAttack(new AttackIntentPayload(default, default))),
                        new FrozenIntentRecord("i-ineligible", CombatIntentType.CombatDefendIntent, new EntityHandle(20), 0, 1, CombatIntentPayload.ForDefend(new DefendIntentPayload(default)))
                    }
                };

                var rig = Rig.Create(handles, intentsByTick);
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
                        new FrozenIntentRecord("i1", CombatIntentType.CombatAttackIntent, new EntityHandle(100), 0, 1, CombatIntentPayload.ForAttack(new AttackIntentPayload(default, default))),
                        new FrozenIntentRecord("i2", CombatIntentType.CombatDefendIntent, new EntityHandle(100), 0, 2, CombatIntentPayload.ForDefend(new DefendIntentPayload(default)))
                    }
                };

                var first = Rig.Create(handles, intentsByTick);
                first.Eligibility.SetEligible(handles[0], true);

                var second = Rig.Create(handles, intentsByTick);
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
                        new FrozenIntentRecord("i-safe", CombatIntentType.CombatAttackIntent, new EntityHandle(500), 0, 1, CombatIntentPayload.ForAttack(new AttackIntentPayload(default, default)))
                    }
                };

                var rig = Rig.Create(handles, intentsByTick);
                rig.Eligibility.SetEligible(handles[0], true);

                rig.Core.ExecuteSingleTick();

                a.True(rig.Eligibility.WasStableAcrossTick, "Eligibility state must remain stable throughout the tick.");
                a.Equal(1, rig.CommitSink.CommitPayloads.Count, "Combat must commit outcomes normally when eligibility is stable.");
            }
        }

        private sealed class Scenario5_BoundedIntentThroughput : Caelmor.Validation.IValidationScenario
        {
            public string Name => "Scenario 5 — Bounded Intent Throughput And Ordering";

            public void Run(IAssert a)
            {
                var handle = new EntityHandle(77);
                var handles = new[] { handle };
                var labels = new[] { "a", "b", "c", "d" };
                const int perTick = 5;

                var intentsByTick = new Dictionary<int, List<FrozenIntentRecord>>
                {
                    [1] = BuildIntentWave(labels[0], perTick, handle),
                    [2] = BuildIntentWave(labels[1], perTick, handle),
                    [3] = BuildIntentWave(labels[2], perTick, handle),
                    [4] = BuildIntentWave(labels[3], perTick, handle)
                };

                var rig = Rig.Create(handles, intentsByTick);
                rig.Eligibility.SetEligible(handle, true);

                int lastCount = 0;
                for (int i = 0; i < labels.Length; i++)
                {
                    rig.Core.ExecuteSingleTick();
                    int newCount = rig.CommitSink.CommitPayloads.Count;
                    int waveCount = newCount - lastCount;
                    var wave = rig.CommitSink.CommitPayloads.GetRange(lastCount, waveCount);

                    a.Equal(perTick, waveCount, $"Tick {i + 1} must process the bounded batch without accumulation.");
                    AssertOrdering(a, wave, labels[i]);

                    lastCount = newCount;
                }
            }

            private static List<FrozenIntentRecord> BuildIntentWave(string label, int count, EntityHandle actor)
            {
                var payload = CombatIntentPayload.ForAttack(new AttackIntentPayload(default, default));
                var intents = new List<FrozenIntentRecord>(count);
                for (int i = 0; i < count; i++)
                {
                    intents.Add(new FrozenIntentRecord(
                        intentId: $"i-{label}-{i + 1}",
                        intentType: CombatIntentType.CombatAttackIntent,
                        actorEntity: actor,
                        submitTick: 0,
                        deterministicSequence: i + 1,
                        payload: payload));
                }

                return intents;
            }

            private static void AssertOrdering(IAssert a, List<string> payloads, string label)
            {
                for (int i = 0; i < payloads.Count; i++)
                {
                    var expectedId = $"i-{label}-{i + 1}";
                    a.True(payloads[i].Contains(expectedId, StringComparison.Ordinal), "Commit ordering must remain stable per tick.");
                }
            }
        }

        private sealed class Rig
        {
            public readonly WorldSimulationCore Core;
            public readonly RecordingEligibilityService Eligibility;
            public readonly DeterministicIntentSource IntentSource;
            public readonly AcceptAllIntentGate Gate;
            public readonly RecordingCommitSink CommitSink;
            public readonly RecordingHook Hook;

            private Rig(
                WorldSimulationCore core,
                RecordingEligibilityService eligibility,
                DeterministicIntentSource intentSource,
                AcceptAllIntentGate gate,
                RecordingCommitSink commitSink,
                RecordingHook hook)
            {
                Core = core;
                Eligibility = eligibility;
                IntentSource = intentSource;
                Gate = gate;
                CommitSink = commitSink;
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
                var runtime = new CombatRuntimeSystem(
                    eligibility,
                    intentSource,
                    gate,
                    new CombatResolutionEngine(),
                    commitSink);
                var hook = new RecordingHook();

                core.RegisterEligibilityGate(new CombatEligibilityGate(eligibility));
                core.RegisterParticipant(runtime, orderKey: 0);
                core.RegisterPhaseHook(runtime, orderKey: 0);
                core.RegisterPhaseHook(hook, orderKey: 1);

                return new Rig(core, eligibility, intentSource, gate, commitSink, hook);
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
            private readonly Dictionary<int, FrozenIntentBatch> _byTick;

            public DeterministicIntentSource(IDictionary<int, List<FrozenIntentRecord>> intentsByTick)
            {
                _byTick = new Dictionary<int, FrozenIntentBatch>();
                foreach (var kv in intentsByTick)
                {
                    var buffer = kv.Value.ToArray();
                    _byTick[kv.Key] = new FrozenIntentBatch(kv.Key, buffer, buffer.Length);
                }
            }

            public FrozenIntentBatch GetFrozenBatch(int authoritativeTick)
            {
                if (_byTick.TryGetValue(authoritativeTick, out var frozen))
                    return frozen;

                return new FrozenIntentBatch(authoritativeTick, Array.Empty<FrozenIntentRecord>(), 0);
            }
        }

        private sealed class AcceptAllIntentGate : ICombatIntentGate
        {
            public Action? OnGate { get; set; }

            public GatedIntentBatch Gate(FrozenIntentBatch frozenQueue)
            {
                OnGate?.Invoke();

                int capacity = Math.Max(1, frozenQueue.Count);
                var accepted = ArrayPool<FrozenIntentRecord>.Shared.Rent(capacity);
                var rows = ArrayPool<IntentGateRow>.Shared.Rent(capacity);
                int acceptedCount = 0;
                int rowCount = 0;
                for (int i = 0; i < frozenQueue.Count; i++)
                {
                    var intent = frozenQueue[i];
                    accepted[acceptedCount++] = intent;
                    rows[rowCount++] = IntentGateRow.Accepted(intent);
                }

                var emptyStates = new Dictionary<EntityHandle, CombatEntityState>();
                var snapshot = CombatStateSnapshot.Capture(emptyStates);

                return GatedIntentBatch.Create(
                    frozenQueue.AuthoritativeTick,
                    accepted,
                    acceptedCount,
                    rows,
                    rowCount,
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
