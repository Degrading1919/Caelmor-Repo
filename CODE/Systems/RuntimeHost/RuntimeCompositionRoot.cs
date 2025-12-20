// - Active runtime code only.
// - Fixed 10 Hz authoritative tick. No tick-thread blocking I/O.
// - Zero/low GC steady state after warm-up: no per-tick allocations in hot paths (do not introduce any).
// - Bounded growth/backpressure with deterministic overflow + metrics.
// - Deterministic ordering. No Dictionary iteration order reliance.
// - Thread ownership must be explicit and enforced: tick-thread asserts OR mailbox marshalling.
// - Deterministic cleanup on disconnect/shutdown; no leaks.
// - AOT/IL2CPP safe patterns only.
using System;
using Caelmor.Combat;
using Caelmor.Runtime;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Integration;
using Caelmor.Runtime.InterestManagement;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Persistence;
using Caelmor.Runtime.Replication;
using Caelmor.Runtime.Sessions;
using Caelmor.Runtime.Threading;
using Caelmor.Runtime.Transport;
using Caelmor.Runtime.WorldSimulation;
using Caelmor.Runtime.WorldState;

namespace Caelmor.Runtime.Host
{
    /// <summary>
    /// Composition root that constructs the runtime dependency graph explicitly without reflection.
    /// Provides a single CreateAndStart surface for host entrypoints.
    /// </summary>
    public static class RuntimeCompositionRoot
    {
        public static ServerRuntimeHost CreateHost(RuntimeCompositionSettings settings)
        {
            return Create(settings);
        }

        public static ServerRuntimeHost CreateAndStart(RuntimeCompositionSettings settings)
        {
            var host = Create(settings);
            host.Start();
            return host;
        }

        public static ServerRuntimeHost Create(RuntimeCompositionSettings settings)
        {
            if (settings is null) throw new ArgumentNullException(nameof(settings));

            var backpressure = settings.BackpressureConfig ?? RuntimeBackpressureConfig.Default;
            var replicationCounters = settings.ReplicationCounters ?? new ReplicationSnapshotCounters();
            var transport = new PooledTransportRouter(backpressure, replicationCounters);

            var activeSessions = settings.ActiveSessions ?? new DeterministicActiveSessionIndex();
            var commands = new AuthoritativeCommandIngestor(backpressure);
            var commandHandlers = settings.CommandHandlers ?? new CommandHandlerRegistry();
            if (settings.ConfigureCommandHandlers != null)
            {
                if (commandHandlers is not CommandHandlerRegistry registry)
                    throw new InvalidOperationException("CommandHandlers must be a CommandHandlerRegistry to register handlers.");

                settings.ConfigureCommandHandlers(registry);
            }

            var entityRegistry = settings.EntityRegistry ?? new DeterministicEntityRegistry();
            var simulation = new WorldSimulationCore(entityRegistry);

            var visibility = settings.VisibilityCulling ?? new VisibilityCullingService(
                settings.ZoneSpatialIndex ?? new ZoneSpatialIndex(settings.SpatialCellSize),
                initialQueryCapacity: settings.VisibilityQueryCapacity);

            var handshakes = new SessionHandshakePipeline(settings.HandshakeCapacity, settings.PlayerSessions, settings.OnboardingHandoff);

            TickDiagnostics ownedTimeSliceDiagnostics = null;
            var timeSliceDiagnostics = settings.TimeSliceDiagnostics;
            if (settings.TimeSlicer == null && timeSliceDiagnostics == null)
            {
                ownedTimeSliceDiagnostics = new TickDiagnostics();
                timeSliceDiagnostics = ownedTimeSliceDiagnostics;
            }

            var timeSlicer = settings.TimeSlicer ?? new TimeSlicedWorkScheduler(timeSliceDiagnostics ?? throw new InvalidOperationException("Time slice diagnostics missing."));

            var replication = new ClientReplicationSnapshotSystem(
                activeSessions,
                settings.SnapshotEligibility,
                settings.ReplicationEligibilityGate ?? visibility,
                settings.ReplicationStateReader,
                transport,
                timeSlicer,
                settings.SnapshotBudget,
                replicationCounters);

            var combatEventBuffer = settings.CombatEventBuffer ?? new CombatEventBuffer(settings.CombatMaxEventsPerTick);
            var combatReplication = settings.CombatReplicationSystem ?? new CombatReplicationSystem(
                settings.CombatClientRegistry ?? new ActiveSessionCombatClientRegistry(activeSessions),
                settings.CombatVisibilityPolicy ?? new AlwaysVisibleCombatVisibilityPolicy(),
                settings.CombatNetworkSender ?? new NullCombatNetworkSender(),
                settings.CombatReplicationValidationSink ?? new NullCombatReplicationValidationSink(),
                settings.CombatDeliveryGuardInitialCapacity,
                settings.CombatDeliveryGuardMaxCount);
            var combatReplicationHook = new CombatReplicationTickHook(combatEventBuffer, combatReplication);

            var lifecycleMailbox = new TickThreadMailbox(backpressure);
            var lifecycleApplier = new LifecycleApplier(transport, commands, handshakes, visibility, replication, combatReplication);
            var persistenceEnabled = settings.Persistence != null && settings.Persistence.Writer != null;
            var pipelineHealth = new RuntimePipelineHealth(handshakeEnabled: true, persistenceEnabled: persistenceEnabled);
            replication.AttachPipelineHealth(pipelineHealth);

            var lifecycleHook = new LifecycleMailboxPhaseHook(lifecycleMailbox, lifecycleApplier, pipelineHealth);
            var inboundPump = new InboundPumpTickHook(
                transport,
                commands,
                activeSessions,
                settings.InboundFramesPerTick,
                settings.IngressCommandsPerTick,
                pipelineHealth);
            var commandConsumeHook = new AuthoritativeCommandConsumeTickHook(commands, commandHandlers, activeSessions, pipelineHealth);
            var handshakeHook = new HandshakeProcessingPhaseHook(handshakes, settings.HandshakePerTickBudget, pipelineHealth);

            PersistenceCompletionQueue persistenceCompletions = null;
            PersistenceWriteQueue persistenceWrites = null;
            PersistenceWorkerLoop persistenceWorker = null;
            PersistencePipelineCounters persistenceCounters = null;
            PersistenceCompletionPhaseHook persistenceHook = null;
            PersistenceApplyState persistenceApplyState = null;

            if (persistenceEnabled)
            {
                persistenceCounters = settings.Persistence.Counters ?? new PersistencePipelineCounters();
                persistenceWrites = settings.Persistence.WriteQueue ?? new PersistenceWriteQueue(backpressure, persistenceCounters);
                persistenceCompletions = settings.Persistence.CompletionQueue ?? new PersistenceCompletionQueue(backpressure, persistenceCounters);
                persistenceApplyState = settings.Persistence.ApplyState ?? new PersistenceApplyState(settings.Persistence.ApplyStateCapacity);
                var completionApplier = settings.Persistence.CompletionApplier ?? new PersistenceCompletionApplier(persistenceApplyState, persistenceCounters);

                persistenceWorker = new PersistenceWorkerLoop(
                    persistenceWrites,
                    persistenceCompletions,
                    settings.Persistence.Writer,
                    persistenceCounters,
                    settings.Persistence.WorkerMaxPerIteration,
                    settings.Persistence.WorkerIdleDelayMs);

                persistenceHook = new PersistenceCompletionPhaseHook(persistenceCompletions, completionApplier, pipelineHealth);
            }

            int baseHooks = 6;
            int hookCount = settings.PhaseHooks.Length + baseHooks + (persistenceHook != null ? 1 : 0);
            var combinedHooks = new PhaseHookRegistration[hookCount];
            int index = 0;

            combinedHooks[index++] = new PhaseHookRegistration(lifecycleHook, settings.LifecycleHookOrderKey);
            combinedHooks[index++] = new PhaseHookRegistration(inboundPump, settings.CommandFreezeHookOrderKey);
            combinedHooks[index++] = new PhaseHookRegistration(commandConsumeHook, settings.CommandConsumeHookOrderKey);
            combinedHooks[index++] = new PhaseHookRegistration(handshakeHook, settings.HandshakeProcessingHookOrderKey);
            combinedHooks[index++] = new PhaseHookRegistration(combatReplicationHook, settings.CombatReplicationHookOrderKey);

            for (int i = 0; i < settings.PhaseHooks.Length; i++)
                combinedHooks[index++] = settings.PhaseHooks[i];

            if (persistenceHook != null)
                combinedHooks[index++] = new PhaseHookRegistration(persistenceHook, settings.PersistenceCompletionHookOrderKey);

            combinedHooks[index++] = new PhaseHookRegistration(replication, settings.ReplicationHookOrderKey);

            WorldBootstrapRegistration.Apply(simulation, settings.EligibilityGates, settings.Participants, combinedHooks);

            var outboundPump = new OutboundSendPump(
                transport,
                settings.OutboundSender,
                activeSessions,
                backpressure,
                replicationCounters,
                settings.OutboundSendPerIteration,
                settings.OutboundPumpIdleMs,
                pipelineHealth,
                simulation.GetCurrentTickIndex);

            var runtimeLoop = new RuntimeServerLoop(
                simulation,
                transport,
                handshakes,
                commands,
                visibility,
                replication,
                entityRegistry,
                lifecycleMailbox,
                inboundPump,
                commandConsumeHook,
                outboundPump,
                lifecycleHook,
                handshakeHook,
                persistenceHook,
                pipelineHealth,
                settings.PipelineStaleTicks,
                persistenceCompletions,
                persistenceWrites,
                persistenceWorker,
                persistenceCounters);

            return new ServerRuntimeHost(
                simulation,
                runtimeLoop,
                inboundPump,
                commandConsumeHook,
                lifecycleHook,
                replication,
                outboundPump,
                activeSessions,
                replicationCounters,
                persistenceCounters,
                persistenceWrites,
                persistenceCompletions,
                persistenceWorker,
                persistenceApplyState,
                ownedTimeSliceDiagnostics);
        }
    }

    public sealed class RuntimeCompositionSettings
    {
        public RuntimeCompositionSettings(
            IPlayerSessionSystem playerSessions,
            IOnboardingHandoffService onboardingHandoff,
            ISnapshotEligibilityView snapshotEligibility,
            IReplicationStateReader replicationStateReader,
            IOutboundTransportSender outboundSender,
            int handshakeCapacity = 64)
        {
            PlayerSessions = playerSessions ?? throw new ArgumentNullException(nameof(playerSessions));
            OnboardingHandoff = onboardingHandoff ?? throw new ArgumentNullException(nameof(onboardingHandoff));
            SnapshotEligibility = snapshotEligibility ?? throw new ArgumentNullException(nameof(snapshotEligibility));
            ReplicationStateReader = replicationStateReader ?? throw new ArgumentNullException(nameof(replicationStateReader));
            OutboundSender = outboundSender ?? throw new ArgumentNullException(nameof(outboundSender));
            HandshakeCapacity = Math.Max(1, handshakeCapacity);
        }

        public RuntimeBackpressureConfig BackpressureConfig { get; set; }
        public IPlayerSessionSystem PlayerSessions { get; }
        public IOnboardingHandoffService OnboardingHandoff { get; }
        public ISnapshotEligibilityView SnapshotEligibility { get; }
        public IReplicationStateReader ReplicationStateReader { get; }
        public IOutboundTransportSender OutboundSender { get; }
        public DeterministicActiveSessionIndex ActiveSessions { get; set; }
        public ICommandHandlerRegistry CommandHandlers { get; set; }
        public Action<CommandHandlerRegistry> ConfigureCommandHandlers { get; set; }
        public DeterministicEntityRegistry EntityRegistry { get; set; }
        public VisibilityCullingService VisibilityCulling { get; set; }
        public ZoneSpatialIndex ZoneSpatialIndex { get; set; }
        public int SpatialCellSize { get; set; } = 1;
        public int VisibilityQueryCapacity { get; set; } = 64;
        public IReplicationEligibilityGate ReplicationEligibilityGate { get; set; }
        public SnapshotSerializationBudget SnapshotBudget { get; set; } = SnapshotSerializationBudget.Default;
        public TickDiagnostics TimeSliceDiagnostics { get; set; }
        public TimeSlicedWorkScheduler TimeSlicer { get; set; }
        public int HandshakeCapacity { get; }
        public int HandshakePerTickBudget { get; set; } = 4;
        public int InboundFramesPerTick { get; set; }
        public int IngressCommandsPerTick { get; set; }
        public int OutboundSendPerIteration { get; set; }
        public int OutboundPumpIdleMs { get; set; } = 1;
        public int PipelineStaleTicks { get; set; } = RuntimePipelineHealth.DefaultStaleTicks;
        public ReplicationSnapshotCounters ReplicationCounters { get; set; }
        public PersistenceSettings Persistence { get; set; }
        public CombatEventBuffer CombatEventBuffer { get; set; }
        public CombatReplicationSystem CombatReplicationSystem { get; set; }
        public IClientRegistry CombatClientRegistry { get; set; }
        public IVisibilityPolicy CombatVisibilityPolicy { get; set; }
        public INetworkSender CombatNetworkSender { get; set; }
        public IReplicationValidationSink CombatReplicationValidationSink { get; set; }
        public int CombatMaxEventsPerTick { get; set; } = 512;
        public int CombatDeliveryGuardInitialCapacity { get; set; } = 256;
        public int CombatDeliveryGuardMaxCount { get; set; } = 512;
        public ISimulationEligibilityGate[] EligibilityGates { get; set; } = Array.Empty<ISimulationEligibilityGate>();
        public ParticipantRegistration[] Participants { get; set; } = Array.Empty<ParticipantRegistration>();
        public PhaseHookRegistration[] PhaseHooks { get; set; } = Array.Empty<PhaseHookRegistration>();
        public int LifecycleHookOrderKey { get; set; } = int.MinValue;
        public int CommandFreezeHookOrderKey { get; set; } = int.MinValue;
        public int CommandConsumeHookOrderKey { get; set; } = int.MinValue + 1;
        public int HandshakeProcessingHookOrderKey { get; set; } = int.MinValue + 2;
        public int PersistenceCompletionHookOrderKey { get; set; } = -1024;
        public int CombatReplicationHookOrderKey { get; set; } = int.MaxValue - 640;
        public int ReplicationHookOrderKey { get; set; } = int.MaxValue - 512;
    }

    public sealed class PersistenceSettings
    {
        public PersistenceSettings(IPersistenceWriter writer)
        {
            Writer = writer ?? throw new ArgumentNullException(nameof(writer));
        }

        public IPersistenceWriter Writer { get; }
        public PersistencePipelineCounters Counters { get; set; }
        public PersistenceWriteQueue WriteQueue { get; set; }
        public PersistenceCompletionQueue CompletionQueue { get; set; }
        public IPersistenceCompletionApplier CompletionApplier { get; set; }
        public PersistenceApplyState ApplyState { get; set; }
        public int ApplyStateCapacity { get; set; } = 16;
        public int WorkerMaxPerIteration { get; set; } = 8;
        public int WorkerIdleDelayMs { get; set; } = 1;
    }
}
