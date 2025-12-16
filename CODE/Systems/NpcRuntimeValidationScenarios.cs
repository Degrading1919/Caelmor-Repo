using System;
using System.Collections.Generic;
using Caelmor.Runtime.Npcs;
using Caelmor.Runtime.WorldSimulation;
using Caelmor.Systems;
using Caelmor.Validation;

namespace Caelmor.Validation.Npcs
{
    /// <summary>
    /// Validation scenarios for Stage 24.B2 — NPC Runtime Validation Scenarios.
    /// Deterministic, no-network tests proving lifecycle invariants, residency enforcement,
    /// mid-tick mutation rejection, and deterministic iteration ordering.
    /// </summary>
    public static class NpcRuntimeValidationScenarios
    {
        public static IReadOnlyList<IValidationScenario> GetScenarios()
        {
            return new IValidationScenario[]
            {
                new ValidationScenarioAdapter(new Scenario1_NpcsOnlySimulatedWhenActive()),
                new ValidationScenarioAdapter(new Scenario2_ActivationRequiresZoneResidency()),
                new ValidationScenarioAdapter(new Scenario3_SingleZoneResidencyOnly()),
                new ValidationScenarioAdapter(new Scenario4_StateChangesRejectedMidTick()),
                new ValidationScenarioAdapter(new Scenario5_DeterministicIterationOrdering()),
                new ValidationScenarioAdapter(new Scenario6_ExplicitSpawnAndDespawn())
            };
        }

        private sealed class Scenario1_NpcsOnlySimulatedWhenActive : IValidationScenario
        {
            public string Name => "Scenario 1 — NPCs only simulated when Active";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var npc = new NpcId(Guid.Parse("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"));
                var zone = new ZoneId(1);

                var spawned = rig.Runtime.Spawn(npc);
                a.True(spawned.Ok, "Spawn must succeed under server authority.");

                var attached = rig.Runtime.AttachNpcToZone(npc, zone);
                a.True(attached.Ok, "Zone attach must succeed.");

                rig.Simulation.ExecuteSingleTick();
                a.Equal(0, rig.Participant.Executions.Count, "Spawned NPC without activation must not be simulated.");

                var activated = rig.Runtime.Activate(npc);
                a.True(activated.Ok, "Activation must succeed when resident.");

                rig.Simulation.ExecuteSingleTick();
                a.Equal(1, rig.Participant.Executions.Count, "Exactly one execution after activation is expected.");
                a.Equal(spawned.Snapshot.Handle, rig.Participant.Executions[0], "Executed entity must match spawned NPC handle.");
            }
        }

        private sealed class Scenario2_ActivationRequiresZoneResidency : IValidationScenario
        {
            public string Name => "Scenario 2 — Activation requires zone residency";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var npc = new NpcId(Guid.Parse("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"));

                var spawned = rig.Runtime.Spawn(npc);
                a.True(spawned.Ok, "Spawn must succeed.");

                var activated = rig.Runtime.Activate(npc);
                a.False(activated.Ok, "Activation must fail without residency.");
                a.Equal(ActivateNpcFailureReason.MissingZoneResidency, activated.FailureReason, "Missing zone residency must be reported.");
            }
        }

        private sealed class Scenario3_SingleZoneResidencyOnly : IValidationScenario
        {
            public string Name => "Scenario 3 — NPCs cannot have multiple zone residencies";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var npc = new NpcId(Guid.Parse("cccccccc-cccc-cccc-cccc-cccccccccccc"));

                var spawned = rig.Runtime.Spawn(npc);
                a.True(spawned.Ok, "Spawn must succeed.");

                var zone1 = new ZoneId(10);
                var zone2 = new ZoneId(20);

                var attach1 = rig.Runtime.AttachNpcToZone(npc, zone1);
                a.True(attach1.Ok, "First residency attach must succeed.");

                var attach2 = rig.Runtime.AttachNpcToZone(npc, zone2);
                a.False(attach2.Ok, "Second residency attach must be rejected.");
                a.Equal(AttachNpcToZoneFailureReason.AlreadyResident, attach2.FailureReason, "Failure reason must indicate existing residency.");
                a.True(attach2.ExistingZone.HasValue && attach2.ExistingZone.Value.Equals(zone1), "Existing zone must be preserved deterministically.");
            }
        }

        private sealed class Scenario4_StateChangesRejectedMidTick : IValidationScenario
        {
            public string Name => "Scenario 4 — State changes are rejected mid-tick";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var npc = new NpcId(Guid.Parse("dddddddd-dddd-dddd-dddd-dddddddddddd"));
                var zone = new ZoneId(2);

                rig.SpawnActivate(npc, zone);

                DeactivateNpcResult deactivateResult = default;
                DespawnNpcResult despawnResult = default;

                rig.Participant.OnExecute = (entity, ctx) =>
                {
                    deactivateResult = rig.Runtime.Deactivate(npc);
                    despawnResult = rig.Runtime.Despawn(npc);
                };

                rig.Simulation.ExecuteSingleTick();

                a.False(deactivateResult.Ok, "Deactivate must be rejected during tick execution.");
                a.Equal(DeactivateNpcFailureReason.MidTickMutation, deactivateResult.FailureReason, "Mid-tick mutation must be signaled for deactivate.");

                a.False(despawnResult.Ok, "Despawn must be rejected during tick execution.");
                a.Equal(DespawnNpcFailureReason.MidTickMutation, despawnResult.FailureReason, "Mid-tick mutation must be signaled for despawn.");

                var stillActive = rig.Runtime.TryGetSnapshot(npc, out var snapshot);
                a.True(stillActive, "NPC must remain present after rejected mid-tick operations.");
                a.Equal(NpcRuntimeState.Active, snapshot.State, "NPC state must remain Active after rejected operations.");
            }
        }

        private sealed class Scenario5_DeterministicIterationOrdering : IValidationScenario
        {
            public string Name => "Scenario 5 — Deterministic ordering for NPC iteration";

            public void Run(IAssert a)
            {
                var first = RunOne();
                var second = RunOne();

                a.Equal(first.Count, second.Count, "Execution counts must match across runs.");
                for (int i = 0; i < first.Count; i++)
                {
                    a.Equal(first[i], second[i], "Execution ordering must be deterministic.");
                }
            }

            private static List<EntityHandle> RunOne()
            {
                var rig = Rig.Create();

                rig.SpawnActivate(new NpcId(Guid.Parse("11111111-2222-3333-4444-555555555555")), new ZoneId(3));
                rig.SpawnActivate(new NpcId(Guid.Parse("99999999-8888-7777-6666-555555555555")), new ZoneId(3));

                rig.Simulation.ExecuteSingleTick();

                return new List<EntityHandle>(rig.Participant.Executions);
            }
        }

        private sealed class Scenario6_ExplicitSpawnAndDespawn : IValidationScenario
        {
            public string Name => "Scenario 6 — Spawn/despawn transitions are explicit and safe";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var npc = new NpcId(Guid.Parse("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"));
                var zone = new ZoneId(4);

                var spawned = rig.Runtime.Spawn(npc);
                a.True(spawned.Ok, "Spawn must succeed deterministically.");
                a.True(rig.Runtime.Exists(npc), "NPC must exist after spawn.");

                rig.SpawnActivate(npc, zone, skipSpawn: true);
                a.Equal(1, rig.Runtime.SnapshotEntitiesDeterministic().Length, "Active resident NPC must be exposed to simulation.");

                var despawned = rig.Runtime.Despawn(npc);
                a.True(despawned.Ok, "Despawn must succeed deterministically.");

                rig.Simulation.ExecuteSingleTick();
                a.Equal(0, rig.Participant.Executions.Count, "Despawned NPC must not be simulated.");

                var existsAfter = rig.Runtime.Exists(npc);
                a.False(existsAfter, "NPC must not exist after despawn.");
            }
        }

        private sealed class Rig
        {
            public FakeAuthority Authority { get; }
            public NpcRuntimeSystem Runtime { get; }
            public WorldSimulationCore Simulation { get; }
            public RecordingParticipant Participant { get; }

            private Rig(FakeAuthority authority, NpcRuntimeSystem runtime, WorldSimulationCore simulation, RecordingParticipant participant)
            {
                Authority = authority;
                Runtime = runtime;
                Simulation = simulation;
                Participant = participant;
            }

            public static Rig Create()
            {
                var authority = new FakeAuthority(isServerAuthoritative: true);
                var runtime = new NpcRuntimeSystem(authority);
                var participant = new RecordingParticipant();
                var simulation = new WorldSimulationCore(runtime);

                simulation.RegisterEligibilityGate(runtime);
                simulation.RegisterParticipant(participant, orderKey: 0);
                simulation.RegisterPhaseHook(runtime, orderKey: 0);

                return new Rig(authority, runtime, simulation, participant);
            }

            public void SpawnActivate(NpcId npc, ZoneId zone, bool skipSpawn = false)
            {
                if (!skipSpawn)
                {
                    var spawned = Runtime.Spawn(npc);
                    if (!spawned.Ok) throw new InvalidOperationException("Precondition failed: spawn");
                }

                var attached = Runtime.AttachNpcToZone(npc, zone);
                if (!attached.Ok) throw new InvalidOperationException("Precondition failed: attach");

                var activated = Runtime.Activate(npc);
                if (!activated.Ok) throw new InvalidOperationException("Precondition failed: activate");
            }
        }

        private sealed class FakeAuthority : IServerAuthority
        {
            public FakeAuthority(bool isServerAuthoritative)
            {
                IsServerAuthoritative = isServerAuthoritative;
            }

            public bool IsServerAuthoritative { get; }
        }

        private sealed class RecordingParticipant : ISimulationParticipant
        {
            public readonly List<EntityHandle> Executions = new List<EntityHandle>();

            public Action<EntityHandle, SimulationTickContext>? OnExecute { get; set; }

            public void Execute(EntityHandle entity, SimulationTickContext context)
            {
                Executions.Add(entity);
                OnExecute?.Invoke(entity, context);
            }
        }
    }
}
