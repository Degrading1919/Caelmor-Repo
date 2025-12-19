using System;
using System.Buffers;
using System.Collections.Generic;
using System.Threading;
using Caelmor.Runtime;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Host;
using Caelmor.Runtime.Integration;
using Caelmor.Runtime.InterestManagement;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Persistence;
using Caelmor.Runtime.Replication;
using Caelmor.Runtime.Sessions;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.Transport;
using Caelmor.Runtime.Threading;
using Caelmor.Runtime.WorldSimulation;
using Caelmor.Runtime.WorldState;
using Caelmor.Systems;
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
                new Scenario4_DeterministicSnapshotContents(),
                new Scenario5_OutboundSendPumpDrainsSnapshots(),
                new Scenario6_LifecycleMailboxAppliesDisconnectOnTick(),
                new Scenario7_FingerprintChangesWithStateMutation()
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
                    ComputeDeterministicFingerprint("committed_state"),
                    snapshot.Entities[0].State.Fingerprint,
                    "Snapshot must reflect committed post-tick state only.");

                rig.StateReader.SetState(entity, "mutated_after_delivery");
                assert.Equal(
                    ComputeDeterministicFingerprint("committed_state"),
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

        private sealed class Scenario5_OutboundSendPumpDrainsSnapshots : IValidationScenario
        {
            public string Name => "Scenario 5 — Outbound Send Pump Drains Snapshots";

            public void Run(IAssert assert)
            {
                var counters = new ReplicationSnapshotCounters();
                var config = RuntimeBackpressureConfig.Default;
                var transport = new PooledTransportRouter(config, counters);
                var eligibility = new SnapshotEligibilityRegistry();

                var authority = new StubAuthority();
                var saveBinding = new StubSaveBinding();
                var restore = new StubRestoreQuery();
                var mutationGate = new AllowMutationGate();
                var sessionEvents = new StubSessionEvents();

                var playerId = new PlayerId(Guid.Parse("99999999-9999-9999-9999-999999999999"));
                var saveId = new SaveId(Guid.Parse("11111111-2222-3333-4444-555555555555"));
                saveBinding.Bind(playerId, saveId);

                var sessions = new PlayerSessionSystem(authority, saveBinding, restore, eligibility, mutationGate, sessionEvents);
                var sessionId = new SessionId(Guid.Parse("cccccccc-cccc-cccc-cccc-cccccccccccc"));
                var activation = sessions.ActivateSession(sessionId, playerId);

                assert.True(activation.Ok, "Session activation must succeed for outbound pump validation.");

                var gate = new ConfigurableGate();
                var stateReader = new RecordingStateReader();
                stateReader.SetState(new EntityHandle(12), "serialized_state");

                var diagnostics = new TickDiagnostics();
                var slicer = new TimeSlicedWorkScheduler(diagnostics);

                var replication = new ClientReplicationSnapshotSystem(
                    sessions,
                    eligibility,
                    gate,
                    stateReader,
                    transport,
                    slicer,
                    SnapshotSerializationBudget.Default,
                    counters);

                var tickContext = new SimulationTickContext(5, TimeSpan.Zero, new SimulationEffectBuffer());
                var eligibleEntities = new[] { new EntityHandle(12) };

                replication.OnPreTick(tickContext, eligibleEntities);
                replication.OnPostTick(tickContext, eligibleEntities);

                var sender = new RecordingSender();
                var pump = new OutboundSendPump(transport, sender, sessions, config, counters, config.MaxOutboundSnapshotsPerSession, idleDelayMs: 0);
                var dispatched = pump.PumpOnce();

                var snapshot = counters.Snapshot();

                assert.Equal(1, dispatched, "Outbound pump must dequeue a serialized snapshot.");
                assert.Equal(1, sender.Sent.Count, "Outbound sender must receive the snapshot payload.");
                assert.True(snapshot.SnapshotsBuilt >= 1, "SnapshotsBuilt counter must increment.");
                assert.True(snapshot.SnapshotsSerialized >= 1, "SnapshotsSerialized counter must increment.");
                assert.True(snapshot.SnapshotsEnqueued >= 1, "SnapshotsEnqueued counter must increment.");
                assert.True(snapshot.SnapshotsDequeuedForSend >= 1, "SnapshotsDequeuedForSend counter must increment.");
                assert.Equal(0, snapshot.SnapshotsDropped, "Happy-path send should not drop snapshots.");
            }
        }

        private sealed class Scenario6_LifecycleMailboxAppliesDisconnectOnTick : IValidationScenario
        {
            public string Name => "Scenario 6 — Lifecycle Mailbox Applies Disconnect On Tick";

            public void Run(IAssert assert)
            {
                var config = RuntimeBackpressureConfig.Default;
                var counters = new ReplicationSnapshotCounters();
                var transport = new PooledTransportRouter(config, counters);
                var commands = new AuthoritativeCommandIngestor(config);
                var authority = new StubAuthority();
                var saveBinding = new StubSaveBinding();
                var restore = new StubRestoreQuery();
                var mutationGate = new AllowMutationGate();
                var sessionEvents = new StubSessionEvents();
                var sessionEligibility = new SnapshotEligibilityRegistry();
                var sessions = new PlayerSessionSystem(authority, saveBinding, restore, sessionEligibility, mutationGate, sessionEvents);
                var handoff = new StubHandoffService();
                var handshakes = new SessionHandshakePipeline(capacity: 4, sessions, handoff);
                var entities = new DeterministicEntityRegistry();
                var simulation = new WorldSimulationCore(entities);
                var spatial = new ZoneSpatialIndex(cellSize: 1);
                var visibility = new VisibilityCullingService(spatial);

                var gate = new ConfigurableGate();
                var stateReader = new RecordingStateReader();
                var diagnostics = new TickDiagnostics();
                var slicer = new TimeSlicedWorkScheduler(diagnostics);
                var replication = new ClientReplicationSnapshotSystem(
                    sessions,
                    sessionEligibility,
                    gate,
                    stateReader,
                    transport,
                    slicer,
                    SnapshotSerializationBudget.Default,
                    counters);

                var commandHandlers = new CommandHandlerRegistry();
                commandHandlers.Register(1, new NoOpCommandHandler());

                var sessionId = new SessionId(Guid.Parse("dddddddd-1111-2222-3333-444444444444"));
                var zone = new ZoneId(1);
                var entity = new EntityHandle(100);

                TickThreadAssert.CaptureTickThread(Thread.CurrentThread);
                try
                {
                    visibility.Track(entity, zone, new ZonePosition(0, 0));
                    visibility.RefreshVisibility(sessionId, new ZoneInterestQuery(zone, new ZonePosition(0, 0), range: 1));

                    var snapshot = new ClientReplicationSnapshot(
                        sessionId,
                        authoritativeTick: 1,
                        Array.Empty<ReplicatedEntitySnapshot>(),
                        count: 0,
                        ArrayPool<ReplicatedEntitySnapshot>.Shared,
                        () => { });
                    transport.RouteSnapshot(snapshot);
                }
                finally
                {
                    TickThreadAssert.ClearTickThread();
                }

                commands.TryEnqueue(sessionId, new AuthoritativeCommand(authoritativeTick: 1, commandType: 1, payloadA: 7, payloadB: 9));
                var beforeMetrics = commands.SnapshotMetrics();
                assert.Equal(1, beforeMetrics.Count, "Command metrics should record the session before disconnect.");

                var runtime = RuntimeServerLoop.Create(
                    simulation,
                    transport,
                    handshakes,
                    commands,
                    commandHandlers,
                    visibility,
                    replication,
                    entities,
                    ReadOnlySpan<ISimulationEligibilityGate>.Empty,
                    ReadOnlySpan<ParticipantRegistration>.Empty,
                    ReadOnlySpan<PhaseHookRegistration>.Empty,
                    sessions);

                runtime.OnSessionDisconnected(sessionId);

                TickThreadAssert.CaptureTickThread(Thread.CurrentThread);
                try
                {
                    simulation.ExecuteSingleTick();
                }
                finally
                {
                    TickThreadAssert.ClearTickThread();
                }

                assert.False(visibility.IsEntityReplicationEligible(sessionId, entity), "Visibility cache must be cleared after disconnect.");

                var afterMetrics = commands.SnapshotMetrics();
                assert.Equal(0, afterMetrics.Count, "Command metrics must drop after disconnect cleanup.");

                bool dequeued = transport.TryDequeueOutbound(sessionId, out var droppedSnapshot);
                if (dequeued)
                {
                    droppedSnapshot.Dispose();
                }

                assert.False(dequeued, "Outbound snapshots must be dropped after disconnect cleanup.");

                runtime.Dispose();
            }
        }

        private sealed class Scenario7_FingerprintChangesWithStateMutation : IValidationScenario
        {
            public string Name => "Scenario 7 — Fingerprints Change With State Mutation";

            public void Run(IAssert assert)
            {
                var rig = Rig.Create();
                var entity = new EntityHandle(21);

                rig.StateReader.SetState(entity, "state_alpha");
                var firstContext = rig.CreateTickContext(tickIndex: 100);
                rig.System.OnPreTick(firstContext, new[] { entity });
                rig.System.OnPostTick(firstContext, new[] { entity });

                rig.StateReader.SetState(entity, "state_beta");
                var secondContext = rig.CreateTickContext(tickIndex: 101);
                rig.System.OnPreTick(secondContext, new[] { entity });
                rig.System.OnPostTick(secondContext, new[] { entity });

                assert.Equal(2, rig.Queue.Enqueued.Count, "Two snapshots must be queued for state mutation validation.");

                var first = rig.Queue.Enqueued[0].snapshot.Entities[0].State.Fingerprint;
                var second = rig.Queue.Enqueued[1].snapshot.Entities[0].State.Fingerprint;

                assert.True(first != second, "Fingerprint must change when committed state changes.");
                assert.Equal(ComputeDeterministicFingerprint("state_alpha"), first, "Fingerprint must be deterministic for initial state.");
                assert.Equal(ComputeDeterministicFingerprint("state_beta"), second, "Fingerprint must be deterministic for mutated state.");
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
            private readonly Dictionary<EntityHandle, ulong> _states = new Dictionary<EntityHandle, ulong>();

            public void SetState(EntityHandle entity, string fingerprint)
            {
                _states[entity] = ComputeDeterministicFingerprint(fingerprint);
            }

            public ReplicatedEntityState ReadCommittedState(EntityHandle entity)
            {
                if (!_states.TryGetValue(entity, out var fp))
                    fp = 0;

                return new ReplicatedEntityState(fp);
            }
        }

        private static ulong ComputeDeterministicFingerprint(string value)
        {
            if (value == null)
                return 0;

            const ulong offsetBasis = 14695981039346656037UL;
            const ulong prime = 1099511628211UL;
            ulong hash = offsetBasis;

            for (int i = 0; i < value.Length; i++)
            {
                hash ^= value[i];
                hash *= prime;
            }

            return hash;
        }

        private sealed class StubAuthority : IServerAuthority
        {
            public bool IsServerAuthoritative => true;
        }

        private sealed class StubSaveBinding : IPlayerSaveBindingQuery
        {
            private readonly Dictionary<PlayerId, SaveId> _bindings = new Dictionary<PlayerId, SaveId>();

            public void Bind(PlayerId playerId, SaveId saveId) => _bindings[playerId] = saveId;

            public bool TryGetSaveForPlayer(PlayerId playerId, out SaveId saveId)
            {
                return _bindings.TryGetValue(playerId, out saveId);
            }
        }

        private sealed class StubRestoreQuery : IPersistenceRestoreQuery
        {
            public bool IsRestoreCompleted(SaveId saveId) => true;
        }

        private sealed class AllowMutationGate : ISessionMutationGate
        {
            public bool CanMutateSessionsNow() => true;
        }

        private sealed class StubSessionEvents : ISessionEvents
        {
            public void OnSessionActivated(SessionId sessionId, PlayerId playerId, SaveId saveId)
            {
            }

            public void OnSessionParticipationEnded(SessionId sessionId, PlayerId playerId, SaveId saveId, DeactivationReason reason)
            {
            }

            public void OnSessionDeactivated(SessionId sessionId, PlayerId playerId, SaveId saveId, DeactivationReason reason)
            {
            }
        }

        private sealed class StubHandoffService : IOnboardingHandoffService
        {
            public void NotifyOnboardingSuccess(IServerSession session)
            {
            }

            public void NotifyOnboardingFailure(IServerSession session)
            {
            }

            public bool IsClientAuthorized(SessionId sessionId) => false;
        }

        private sealed class RecordingSender : IOutboundTransportSender
        {
            public readonly List<(SessionId session, long tick, int bytes)> Sent = new List<(SessionId, long, int)>();

            public bool TrySend(SessionId sessionId, SerializedSnapshot snapshot)
            {
                Sent.Add((sessionId, snapshot.Tick, snapshot.ByteLength));
                snapshot.Dispose();
                return true;
            }
        }
    }
}
