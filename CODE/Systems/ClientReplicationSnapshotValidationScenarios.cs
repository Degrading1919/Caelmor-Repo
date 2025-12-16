using System;
using System.Collections.Generic;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Replication;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.WorldSimulation;
using Caelmor.Validation;

namespace Caelmor.Validation.Replication
{
    /// <summary>
    /// Stage 29.B2 — Replication Validation Scenarios.
    /// Proves post-tick snapshot capture, eligibility enforcement, and deterministic outputs.
    /// </summary>
    public static class ClientReplicationSnapshotValidationScenarios
    {
        public static IReadOnlyList<IValidationScenario> GetScenarios()
        {
            return new IValidationScenario[]
            {
                new Scenario1_SnapshotsReflectCommittedState(),
                new Scenario2_NoMidTickSnapshots(),
                new Scenario3_EligibilityEnforced(),
                new Scenario4_DeterministicSnapshotContents()
            };
        }

        private sealed class Scenario1_SnapshotsReflectCommittedState : IValidationScenario
        {
            public string Name => "Scenario 1 — Snapshots Reflect Committed State";

            public void Run(IAssert assert)
            {
                var rig = Rig.Create();
                var entity = new EntityHandle(1);
                var tickContext = rig.CreateTickContext(tickIndex: 10);

                rig.StateReader.SetState(entity, "mid_tick_state");
                rig.System.OnPreTick(tickContext, new[] { entity });

                rig.StateReader.SetState(entity, "committed_state");
                rig.System.OnPostTick(tickContext, new[] { entity });

                assert.Equal(1, rig.Queue.Enqueued.Count, "Exactly one snapshot must be enqueued.");

                var snapshot = rig.Queue.Enqueued[0].snapshot;
                assert.Equal(1, snapshot.Entities.Count, "Snapshot must include the eligible entity.");
                assert.Equal(
                    "committed_state",
                    snapshot.Entities[0].State.Fingerprint,
                    "Snapshot must reflect committed post-tick state only.");

                rig.StateReader.SetState(entity, "mutated_after_delivery");
                assert.Equal(
                    "committed_state",
                    snapshot.Entities[0].State.Fingerprint,
                    "Snapshots must be immutable once enqueued.");
            }
        }

        private sealed class Scenario2_NoMidTickSnapshots : IValidationScenario
        {
            public string Name => "Scenario 2 — No Mid-Tick Snapshots";

            public void Run(IAssert assert)
            {
                var rig = Rig.Create();
                var entity = new EntityHandle(5);
                var tickContext = rig.CreateTickContext(tickIndex: 2);

                rig.System.OnPreTick(tickContext, new[] { entity });

                try
                {
                    rig.System.CaptureSnapshotForSession(rig.Sessions.Ordered[0], tickContext.TickIndex, new[] { entity });
                    assert.True(false, "Mid-tick snapshot generation must be rejected.");
                }
                catch (InvalidOperationException)
                {
                    // Expected guard.
                }

                assert.Equal(0, rig.Queue.Enqueued.Count, "No snapshots may be queued mid-tick.");
            }
        }

        private sealed class Scenario3_EligibilityEnforced : IValidationScenario
        {
            public string Name => "Scenario 3 — Eligibility Enforced";

            public void Run(IAssert assert)
            {
                var rig = Rig.Create();
                var eligibleSession = rig.Sessions.Ordered[0];
                var ineligibleSession = rig.Sessions.Ordered[1];

                var allowedEntity = new EntityHandle(7);
                var blockedEntity = new EntityHandle(9);

                rig.StateReader.SetState(allowedEntity, "allowed");
                rig.StateReader.SetState(blockedEntity, "blocked");

                rig.SessionEligibility.TrySetSnapshotEligible(eligibleSession, isEligible: true);
                rig.SessionEligibility.TrySetSnapshotEligible(ineligibleSession, isEligible: false);
                rig.Gate.AllowedPredicate = (session, entity) => entity.Equals(allowedEntity);

                var ctx = rig.CreateTickContext(tickIndex: 3);
                rig.System.OnPreTick(ctx, new[] { allowedEntity, blockedEntity });
                rig.System.OnPostTick(ctx, new[] { allowedEntity, blockedEntity });

                assert.Equal(1, rig.Queue.Enqueued.Count, "Only eligible sessions may receive snapshots.");

                var snapshot = rig.Queue.Enqueued[0].snapshot;
                assert.Equal(eligibleSession, snapshot.SessionId, "Snapshot must target the eligible session.");
                assert.Equal(1, snapshot.Entities.Count, "Only eligible entities must be replicated.");
                assert.Equal(allowedEntity, snapshot.Entities[0].Entity, "Blocked entities must be excluded.");
            }
        }

        private sealed class Scenario4_DeterministicSnapshotContents : IValidationScenario
        {
            public string Name => "Scenario 4 — Deterministic Snapshot Contents";

            public void Run(IAssert assert)
            {
                var rig = Rig.Create();
                var entityA = new EntityHandle(11);
                var entityB = new EntityHandle(5);

                rig.StateReader.SetState(entityA, "state_a");
                rig.StateReader.SetState(entityB, "state_b");

                var ctx = rig.CreateTickContext(tickIndex: 42);

                rig.System.OnPreTick(ctx, new[] { entityA, entityB });
                rig.System.OnPostTick(ctx, new[] { entityA, entityB });

                rig.System.OnPreTick(ctx, new[] { entityA, entityB });
                rig.System.OnPostTick(ctx, new[] { entityA, entityB });

                assert.Equal(2, rig.Queue.Enqueued.Count, "Snapshots must be generated for each post-tick execution.");

                var first = rig.Queue.Enqueued[0].snapshot;
                var second = rig.Queue.Enqueued[1].snapshot;

                assert.Equal(first.Entities.Count, second.Entities.Count, "Entity counts must remain deterministic.");
                for (int i = 0; i < first.Entities.Count; i++)
                {
                    assert.Equal(first.Entities[i].Entity, second.Entities[i].Entity, "Entity ordering must be deterministic.");
                    assert.Equal(first.Entities[i].State.Fingerprint, second.Entities[i].State.Fingerprint, "Entity payloads must be deterministic.");
                }
            }
        }

        private sealed class Rig
        {
            public readonly ClientReplicationSnapshotSystem System;
            public readonly RecordingQueue Queue;
            public readonly DeterministicSessionIndex Sessions;
            public readonly SnapshotEligibilityRegistry SessionEligibility;
            public readonly ConfigurableGate Gate;
            public readonly RecordingStateReader StateReader;

            private Rig(
                ClientReplicationSnapshotSystem system,
                RecordingQueue queue,
                DeterministicSessionIndex sessions,
                SnapshotEligibilityRegistry sessionEligibility,
                ConfigurableGate gate,
                RecordingStateReader stateReader)
            {
                System = system;
                Queue = queue;
                Sessions = sessions;
                SessionEligibility = sessionEligibility;
                Gate = gate;
                StateReader = stateReader;
            }

            public static Rig Create()
            {
                var sessions = new DeterministicSessionIndex(
                    new SessionId(Guid.Parse("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")),
                    new SessionId(Guid.Parse("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")));

                var sessionEligibility = new SnapshotEligibilityRegistry();
                foreach (var s in sessions.Ordered)
                    sessionEligibility.TrySetSnapshotEligible(s, isEligible: true);

                var gate = new ConfigurableGate();
                var stateReader = new RecordingStateReader();
                var queue = new RecordingQueue();

                var system = new ClientReplicationSnapshotSystem(
                    sessions,
                    sessionEligibility,
                    gate,
                    stateReader,
                    queue);

                return new Rig(system, queue, sessions, sessionEligibility, gate, stateReader);
            }

            public SimulationTickContext CreateTickContext(long tickIndex)
            {
                return new SimulationTickContext(tickIndex, TimeSpan.Zero, new SimulationEffectBuffer());
            }
        }

        private sealed class RecordingQueue : IReplicationSnapshotQueue
        {
            public readonly List<(SessionId session, ClientReplicationSnapshot snapshot)> Enqueued = new List<(SessionId, ClientReplicationSnapshot)>();

            public void Enqueue(SessionId sessionId, ClientReplicationSnapshot snapshot)
            {
                Enqueued.Add((sessionId, snapshot));
            }
        }

        private sealed class DeterministicSessionIndex : IActiveSessionIndex
        {
            public IReadOnlyList<SessionId> Ordered { get; }

            public DeterministicSessionIndex(params SessionId[] sessions)
            {
                var list = new List<SessionId>(sessions ?? Array.Empty<SessionId>());
                list.Sort((a, b) => string.Compare(a.Value.ToString(), b.Value.ToString(), StringComparison.Ordinal));
                Ordered = list.ToArray();
            }

            public IReadOnlyList<SessionId> SnapshotSessionsDeterministic() => Ordered;
        }

        private sealed class ConfigurableGate : IReplicationEligibilityGate
        {
            public Func<SessionId, EntityHandle, bool>? AllowedPredicate { get; set; }

            public bool IsEntityReplicationEligible(SessionId sessionId, EntityHandle entity)
            {
                return AllowedPredicate?.Invoke(sessionId, entity) ?? true;
            }
        }

        private sealed class RecordingStateReader : IReplicationStateReader
        {
            private readonly Dictionary<EntityHandle, string> _states = new Dictionary<EntityHandle, string>();

            public void SetState(EntityHandle entity, string fingerprint)
            {
                _states[entity] = fingerprint;
            }

            public ReplicatedEntityState ReadCommittedState(EntityHandle entity)
            {
                if (!_states.TryGetValue(entity, out var fp))
                    fp = string.Empty;

                return new ReplicatedEntityState(fp);
            }
        }
    }
}
