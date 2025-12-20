// - Active runtime code only.
// - Fixed 10 Hz authoritative tick. No tick-thread blocking I/O.
// - Zero/low GC steady state after warm-up: no per-tick allocations in hot paths (do not introduce any).
// - Bounded growth/backpressure with deterministic overflow + metrics.
// - Deterministic ordering. No Dictionary iteration order reliance.
// - Thread ownership must be explicit and enforced: tick-thread asserts OR mailbox marshalling.
// - Deterministic cleanup on disconnect/shutdown; no leaks.
// - AOT/IL2CPP safe patterns only.
using System;
using System.Collections.Generic;
using Caelmor.Combat;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Integration;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Persistence;
using Caelmor.Runtime.Replication;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.Transport;
using Caelmor.Runtime.WorldSimulation;
using Caelmor.Runtime.WorldState;

namespace Caelmor.Runtime.Host
{
    /// <summary>
    /// Server-side runtime loop coordinator. Owns deterministic start/stop and cleanup paths
    /// for transport routing, handshakes, command ingestion, visibility caches, and entity registration.
    /// Ensures no lingering registrations across disconnects, zone unloads, or server shutdown.
    /// Persistence completions are staged through a bounded mailbox and drained on the tick thread via phase hooks.
    /// </summary>
    // IL2CPP/AOT SAFETY: Do not introduce Reflection.Emit, runtime codegen, or implicit reflection-based discovery
    // in this entry point. Managed stripping must be accounted for via explicit registration; tick-thread paths
    // must remain deterministic and free of editor-only APIs.
    public sealed class RuntimeServerLoop : IDisposable
    {
        private readonly WorldSimulationCore _simulation;
        private readonly PooledTransportRouter _transport;
        private readonly SessionHandshakePipeline _handshakes;
        private readonly AuthoritativeCommandIngestor _commands;
        private readonly AuthoritativeCommandConsumeTickHook _commandConsumeHook;
        private readonly VisibilityCullingService _visibility;
        private readonly ClientReplicationSnapshotSystem _replication;
        private readonly DeterministicEntityRegistry _entities;
        private readonly PersistenceCompletionQueue _persistenceCompletions;
        private readonly PersistenceWriteQueue _persistenceWrites;
        private readonly PersistenceWorkerLoop _persistenceWorker;
        private readonly PersistencePipelineCounters _persistenceCounters;
        private readonly TickThreadMailbox _lifecycleMailbox;
        private readonly InboundPumpTickHook _inboundPump;
        private readonly OutboundSendPump _outboundPump;
        private readonly LifecycleMailboxPhaseHook _lifecycleHook;
        private readonly HandshakeProcessingPhaseHook _handshakeHook;
        private readonly PersistenceCompletionPhaseHook _persistenceHook;
        private readonly RuntimePipelineHealth _pipelineHealth;
        private readonly int _pipelineStaleTicks;

        private readonly object _gate = new object();
        private bool _started;

        public event Action<TickStallEvent> TickStallDetected;

        public RuntimeServerLoop(
            WorldSimulationCore simulation,
            PooledTransportRouter transport,
            SessionHandshakePipeline handshakes,
            AuthoritativeCommandIngestor commands,
            VisibilityCullingService visibility,
            ClientReplicationSnapshotSystem replication,
            DeterministicEntityRegistry entities,
            TickThreadMailbox lifecycleMailbox,
            InboundPumpTickHook inboundPump,
            AuthoritativeCommandConsumeTickHook commandConsumeHook,
            OutboundSendPump outboundPump,
            LifecycleMailboxPhaseHook lifecycleHook = null,
            HandshakeProcessingPhaseHook handshakeHook = null,
            PersistenceCompletionPhaseHook persistenceHook = null,
            RuntimePipelineHealth pipelineHealth = null,
            int pipelineStaleTicks = RuntimePipelineHealth.DefaultStaleTicks,
            PersistenceCompletionQueue persistenceCompletions = null,
            PersistenceWriteQueue persistenceWrites = null,
            PersistenceWorkerLoop persistenceWorker = null,
            PersistencePipelineCounters persistenceCounters = null)
        {
            _simulation = simulation ?? throw new ArgumentNullException(nameof(simulation));
            _transport = transport ?? throw new ArgumentNullException(nameof(transport));
            _handshakes = handshakes ?? throw new ArgumentNullException(nameof(handshakes));
            _commands = commands ?? throw new ArgumentNullException(nameof(commands));
            _commandConsumeHook = commandConsumeHook ?? throw new ArgumentNullException(nameof(commandConsumeHook));
            _visibility = visibility ?? throw new ArgumentNullException(nameof(visibility));
            _replication = replication ?? throw new ArgumentNullException(nameof(replication));
            _entities = entities ?? throw new ArgumentNullException(nameof(entities));
            _lifecycleMailbox = lifecycleMailbox ?? throw new ArgumentNullException(nameof(lifecycleMailbox));
            _inboundPump = inboundPump ?? throw new ArgumentNullException(nameof(inboundPump));
            _outboundPump = outboundPump ?? throw new ArgumentNullException(nameof(outboundPump));
            _lifecycleHook = lifecycleHook;
            _handshakeHook = handshakeHook;
            _persistenceHook = persistenceHook;
            _pipelineHealth = pipelineHealth;
            _pipelineStaleTicks = Math.Max(1, pipelineStaleTicks);
            _persistenceCompletions = persistenceCompletions;
            _persistenceWrites = persistenceWrites;
            _persistenceWorker = persistenceWorker;
            _persistenceCounters = persistenceCounters;

            _simulation.StallDetected += OnTickStalled;
        }

        /// <summary>
        /// Factory helper that applies explicit, deterministic simulation registration before constructing the loop.
        /// </summary>
        public static RuntimeServerLoop Create(
            WorldSimulationCore simulation,
            PooledTransportRouter transport,
            SessionHandshakePipeline handshakes,
            AuthoritativeCommandIngestor commands,
            ICommandHandlerRegistry commandHandlers,
            VisibilityCullingService visibility,
            ClientReplicationSnapshotSystem replication,
            DeterministicEntityRegistry entities,
            ReadOnlySpan<ISimulationEligibilityGate> eligibilityGates,
            ReadOnlySpan<ParticipantRegistration> participants,
            ReadOnlySpan<PhaseHookRegistration> phaseHooks,
            IActiveSessionIndex activeSessions = null,
            int commandFreezeHookOrderKey = int.MinValue,
            int commandConsumeHookOrderKey = int.MinValue + 1,
            int lifecycleHookOrderKey = int.MinValue,
            int handshakeProcessingHookOrderKey = int.MinValue + 2,
            int handshakePerTickBudget = 4,
            PersistenceCompletionQueue persistenceCompletions = null,
            IPersistenceCompletionApplier persistenceCompletionApplier = null,
            int persistenceCompletionHookOrderKey = -1024,
            int inboundFramesPerTick = 0,
            int ingressCommandsPerTick = 0,
            IOutboundTransportSender outboundSender = null,
            int outboundSendPerIteration = 0,
            int outboundPumpIdleMs = 1,
            ReplicationSnapshotCounters? replicationCounters = null,
            int replicationHookOrderKey = int.MaxValue - 512,
            CombatEventBuffer combatEventBuffer = null,
            CombatReplicationSystem combatReplication = null,
            IClientRegistry combatClientRegistry = null,
            IVisibilityPolicy combatVisibilityPolicy = null,
            INetworkSender combatNetworkSender = null,
            IReplicationValidationSink combatReplicationValidationSink = null,
            int combatMaxEventsPerTick = 512,
            int combatDeliveryGuardInitialCapacity = 256,
            int combatDeliveryGuardMaxCount = 512,
            int combatReplicationHookOrderKey = int.MaxValue - 640,
            PersistenceWriteQueue persistenceWrites = null,
            PersistenceWorkerLoop persistenceWorker = null,
            PersistencePipelineCounters persistenceCounters = null,
            bool skipLifecycleHookRegistration = false,
            int pipelineStaleTicks = RuntimePipelineHealth.DefaultStaleTicks)
        {
            if (activeSessions == null)
                throw new ArgumentNullException(nameof(activeSessions));
            if (replication == null)
                throw new ArgumentNullException(nameof(replication));
            if (commandHandlers == null)
                throw new ArgumentNullException(nameof(commandHandlers));

#if DEBUG
            if (commandConsumeHookOrderKey <= commandFreezeHookOrderKey)
                throw new InvalidOperationException("AuthoritativeCommandConsumeTickHook must run after the freeze hook.");
#endif

            combatEventBuffer ??= new CombatEventBuffer(combatMaxEventsPerTick);
            combatReplication ??= new CombatReplicationSystem(
                combatClientRegistry ?? new ActiveSessionCombatClientRegistry(activeSessions),
                combatVisibilityPolicy ?? new AlwaysVisibleCombatVisibilityPolicy(),
                combatNetworkSender ?? new NullCombatNetworkSender(),
                combatReplicationValidationSink ?? new NullCombatReplicationValidationSink(),
                combatDeliveryGuardInitialCapacity,
                combatDeliveryGuardMaxCount);
            var combatReplicationHook = new CombatReplicationTickHook(combatEventBuffer, combatReplication);

            int baseHooks = skipLifecycleHookRegistration ? 5 : 6;
            int hookCount = phaseHooks.Length + baseHooks;
            bool includePersistence = persistenceCompletions != null && persistenceCompletionApplier != null;
            if (includePersistence)
                hookCount++;

            var combinedHooks = new PhaseHookRegistration[hookCount];
            int index = 0;

            var lifecycleMailbox = new TickThreadMailbox(transport.Config);
            var lifecycleApplier = new LifecycleApplier(transport, commands, handshakes, visibility, replication, combatReplication);
            bool persistenceEnabled = includePersistence || persistenceWrites != null || persistenceWorker != null || persistenceCounters != null;
            var pipelineHealth = new RuntimePipelineHealth(handshakeEnabled: true, persistenceEnabled: persistenceEnabled);
            replication.AttachPipelineHealth(pipelineHealth);
            var lifecycleHook = new LifecycleMailboxPhaseHook(lifecycleMailbox, lifecycleApplier, pipelineHealth);
            if (!skipLifecycleHookRegistration)
                combinedHooks[index++] = new PhaseHookRegistration(lifecycleHook, lifecycleHookOrderKey);

            var inboundPump = new InboundPumpTickHook(transport, commands, activeSessions, inboundFramesPerTick, ingressCommandsPerTick, pipelineHealth);
            combinedHooks[index++] = new PhaseHookRegistration(inboundPump, commandFreezeHookOrderKey);

            var consumeHook = new AuthoritativeCommandConsumeTickHook(commands, commandHandlers, activeSessions, pipelineHealth);
            combinedHooks[index++] = new PhaseHookRegistration(consumeHook, commandConsumeHookOrderKey);

            var handshakeHook = new HandshakeProcessingPhaseHook(handshakes, handshakePerTickBudget, pipelineHealth);
            combinedHooks[index++] = new PhaseHookRegistration(
                handshakeHook,
                handshakeProcessingHookOrderKey);
            combinedHooks[index++] = new PhaseHookRegistration(combatReplicationHook, combatReplicationHookOrderKey);

            for (int i = 0; i < phaseHooks.Length; i++)
                combinedHooks[index++] = phaseHooks[i];

            PersistenceCompletionPhaseHook persistenceHook = null;
            if (includePersistence)
            {
                persistenceHook = new PersistenceCompletionPhaseHook(persistenceCompletions, persistenceCompletionApplier, pipelineHealth);
                combinedHooks[index++] = new PhaseHookRegistration(
                    persistenceHook,
                    persistenceCompletionHookOrderKey);
            }

            combinedHooks[index++] = new PhaseHookRegistration(replication, replicationHookOrderKey);

            var counters = replicationCounters ?? transport.SnapshotCounters;
            var sender = outboundSender ?? NullOutboundTransportSender.Instance;
            var outboundPump = new OutboundSendPump(
                transport,
                sender,
                activeSessions,
                transport.Config,
                counters,
                outboundSendPerIteration,
                outboundPumpIdleMs,
                pipelineHealth,
                simulation.GetCurrentTickIndex);

            WorldBootstrapRegistration.Apply(simulation, eligibilityGates, participants, combinedHooks);
            return new RuntimeServerLoop(
                simulation,
                transport,
                handshakes,
                commands,
                visibility,
                replication,
                entities,
                lifecycleMailbox,
                inboundPump,
                consumeHook,
                outboundPump,
                lifecycleHook,
                handshakeHook,
                persistenceHook,
                pipelineHealth,
                pipelineStaleTicks,
                persistenceCompletions,
                persistenceWrites,
                persistenceWorker,
                persistenceCounters);
        }

        public void Start()
        {
            lock (_gate)
            {
                if (_started)
                    return;

#if DEBUG
                if (_commandConsumeHook.HandlerCount <= 0)
                    throw new InvalidOperationException("AuthoritativeCommandConsumeTickHook missing handler registration.");
                if (_commandConsumeHook.MutatingHandlerCount <= 0)
                    throw new InvalidOperationException("AuthoritativeCommandConsumeTickHook missing mutating handler registration.");
#endif
                ValidatePipelineWiring();

                _commands.Prewarm();
                _transport.Prewarm();

                _persistenceWorker?.Start();
                _simulation.Start();
                _outboundPump.Start();
                _started = true;
            }
        }

        public void Stop()
        {
            lock (_gate)
            {
                if (!_started)
                    return;

                _started = false;
            }

            _persistenceWorker?.Stop();
            _outboundPump.Stop();
            _simulation.Stop();
            ClearTransientState();
        }

        /// <summary>
        /// Session disconnect path: drop queued transport frames, commands, and visibility caches.
        /// </summary>
        public void OnSessionDisconnected(SessionId sessionId)
        {
            _lifecycleMailbox.TryEnqueueDisconnect(sessionId);
            _lifecycleMailbox.TryEnqueueUnregister(sessionId);
            _lifecycleMailbox.TryEnqueueClearVisibility(sessionId);
            _lifecycleMailbox.TryEnqueueCleanupReplication(sessionId);
        }

        /// <summary>
        /// Player unload path: identical to session disconnect today, but kept explicit for future player-only caches.
        /// </summary>
        public void OnPlayerUnloaded(SessionId sessionId)
        {
            OnSessionDisconnected(sessionId);
        }

        /// <summary>
        /// Zone unload path: despawn entities and drop visibility/spatial state.
        /// </summary>
        public void OnZoneUnloaded(ZoneId zone)
        {
            _entities.DespawnZone(zone);
            _visibility.RemoveZone(zone);
        }

        /// <summary>
        /// Controlled shutdown for host restart. Ensures no lingering references remain registered.
        /// </summary>
        public void ShutdownServer()
        {
            Stop();
            ClearTransientState();
        }

        public void Dispose()
        {
            ShutdownServer();
            _simulation.StallDetected -= OnTickStalled;
            _transport.Dispose();
            _outboundPump.Dispose();
            _visibility.Dispose();
            _entities.Dispose();
        }

        public RuntimeDiagnosticsSnapshot CaptureDiagnostics()
        {
            var transport = _transport.CaptureDiagnostics();
            var tick = _simulation.Diagnostics;
            var commands = _commands.SnapshotMetrics();
            var handshakes = _handshakes.SnapshotMetrics();
            var inboundPump = _inboundPump.Diagnostics;
            var persistenceCompletions = _persistenceCompletions?.SnapshotMetrics();
            var persistenceCounters = _persistenceCounters?.Snapshot();
            var persistenceQueue = _persistenceWrites?.SnapshotMetrics();
            var lifecycle = new LifecycleMailboxCounters(
                _lifecycleMailbox.LifecycleOpsEnqueued,
                _lifecycleMailbox.LifecycleOpsApplied,
                _lifecycleMailbox.DisconnectsApplied,
                _lifecycleMailbox.LifecycleOpsDropped);
            var pipeline = _pipelineHealth?.Snapshot(_simulation.CurrentTickIndex, _pipelineStaleTicks);
            return new RuntimeDiagnosticsSnapshot(tick, transport, persistenceCompletions, commands, handshakes, inboundPump, persistenceCounters, persistenceQueue, lifecycle, pipeline);
        }

        private void ClearTransientState()
        {
            _transport.Clear();
            _handshakes.Reset();
            _commands.Clear();
            _visibility.Clear();
            _entities.ClearAll();
            _lifecycleMailbox.Clear();
            _persistenceCompletions?.Clear();
            _persistenceWrites?.Clear();
        }

        private void OnTickStalled(TickStallEvent stall)
        {
            TickStallDetected?.Invoke(stall);
        }

        private void ValidatePipelineWiring()
        {
            var missing = new List<string>(8);

            if (!_simulation.IsPhaseHookRegistered(_inboundPump))
                missing.Add("inbound_pump_hook");
            if (!_simulation.IsPhaseHookRegistered(_commandConsumeHook))
                missing.Add("command_consume_hook");

            if (_handshakes != null)
            {
                bool handshakeRegistered = _handshakeHook != null
                    ? _simulation.IsPhaseHookRegistered(_handshakeHook)
                    : _simulation.HasPhaseHook<HandshakeProcessingPhaseHook>();
                if (!handshakeRegistered)
                    missing.Add("handshake_processing_hook");
            }

            bool lifecycleRegistered = _lifecycleHook != null
                ? _simulation.IsPhaseHookRegistered(_lifecycleHook)
                : _simulation.HasPhaseHook<LifecycleMailboxPhaseHook>();
            if (!lifecycleRegistered)
                missing.Add("lifecycle_mailbox_hook");

            if (!_simulation.IsPhaseHookRegistered(_replication))
                missing.Add("replication_hook");
            if (_outboundPump == null)
                missing.Add("outbound_send_pump");

            bool persistenceEnabled = _persistenceCompletions != null || _persistenceWrites != null || _persistenceWorker != null;
            if (persistenceEnabled)
            {
                bool persistenceHookRegistered = _persistenceHook != null
                    ? _simulation.IsPhaseHookRegistered(_persistenceHook)
                    : _simulation.HasPhaseHook<PersistenceCompletionPhaseHook>();
                if (!persistenceHookRegistered)
                    missing.Add("persistence_completion_hook");
                if (_persistenceWorker == null)
                    missing.Add("persistence_worker_loop");
            }

            if (missing.Count > 0)
                throw new InvalidOperationException($"RUNTIME_PIPELINE_MISSING_HOOKS: {string.Join(", ", missing)}");
        }

        internal PooledTransportRouter Transport => _transport;
        internal SessionHandshakePipeline Handshakes => _handshakes;
    }

    internal sealed class LifecycleMailboxPhaseHook : ITickPhaseHook
    {
        private readonly TickThreadMailbox _mailbox;
        private readonly ILifecycleApplier _applier;
        private readonly RuntimePipelineHealth? _pipelineHealth;

        public LifecycleMailboxPhaseHook(TickThreadMailbox mailbox, ILifecycleApplier applier, RuntimePipelineHealth pipelineHealth = null)
        {
            _mailbox = mailbox ?? throw new ArgumentNullException(nameof(mailbox));
            _applier = applier ?? throw new ArgumentNullException(nameof(applier));
            _pipelineHealth = pipelineHealth;
        }

        public void OnPreTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            _pipelineHealth?.MarkLifecycleMailbox(context.TickIndex);
            _mailbox.Drain(_applier);
        }

        public void OnPostTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
        }
    }

    internal sealed class LifecycleApplier : ILifecycleApplier
    {
        private readonly PooledTransportRouter _transport;
        private readonly AuthoritativeCommandIngestor _commands;
        private readonly SessionHandshakePipeline _handshakes;
        private readonly VisibilityCullingService _visibility;
        private readonly ClientReplicationSnapshotSystem _replication;
        private readonly CombatReplicationSystem _combatReplication;

        public LifecycleApplier(
            PooledTransportRouter transport,
            AuthoritativeCommandIngestor commands,
            SessionHandshakePipeline handshakes,
            VisibilityCullingService visibility,
            ClientReplicationSnapshotSystem replication,
            CombatReplicationSystem combatReplication)
        {
            _transport = transport ?? throw new ArgumentNullException(nameof(transport));
            _commands = commands ?? throw new ArgumentNullException(nameof(commands));
            _handshakes = handshakes ?? throw new ArgumentNullException(nameof(handshakes));
            _visibility = visibility ?? throw new ArgumentNullException(nameof(visibility));
            _replication = replication ?? throw new ArgumentNullException(nameof(replication));
            _combatReplication = combatReplication ?? throw new ArgumentNullException(nameof(combatReplication));
        }

        public void Apply(TickThreadMailbox.LifecycleOp op)
        {
            TickThreadAssert.AssertTickThread();

            switch (op.Kind)
            {
                case TickThreadMailbox.LifecycleOpKind.DisconnectSession:
                    _transport.DropAllForSession(op.SessionId);
                    _commands.DropSession(op.SessionId);
                    break;
                case TickThreadMailbox.LifecycleOpKind.UnregisterSession:
                    _handshakes.Drop(op.SessionId);
                    break;
                case TickThreadMailbox.LifecycleOpKind.ClearVisibility:
                    _visibility.RemoveSession(op.SessionId);
                    break;
                case TickThreadMailbox.LifecycleOpKind.CleanupReplication:
                    _replication.OnSessionDisconnected(op.SessionId);
                    _combatReplication.ReleaseClient(op.SessionId);
                    break;
            }
        }
    }

    internal sealed class NullOutboundTransportSender : IOutboundTransportSender
    {
        public static readonly NullOutboundTransportSender Instance = new NullOutboundTransportSender();

        private NullOutboundTransportSender()
        {
        }

        public bool TrySend(SessionId sessionId, SerializedSnapshot snapshot)
        {
            snapshot?.Dispose();
            return true;
        }
    }

    public readonly struct RuntimeDiagnosticsSnapshot
    {
        public RuntimeDiagnosticsSnapshot(
            TickDiagnosticsSnapshot tick,
            TransportBackpressureDiagnostics transport,
            CompletionQueueMetrics? persistenceCompletionMailbox,
            CommandIngestorDiagnostics commands,
            HandshakePipelineMetrics handshakes,
            InboundPumpDiagnostics inboundPump,
            PersistencePipelineCounterSnapshot? persistencePipelineCounters,
            PersistenceQueueMetrics? persistenceQueue,
            LifecycleMailboxCounters lifecycleMailbox,
            RuntimePipelineHealthSnapshot? pipelineHealth)
        {
            Tick = tick;
            Transport = transport;
            PersistenceCompletionMailbox = persistenceCompletionMailbox;
            Commands = commands;
            Handshakes = handshakes;
            InboundPump = inboundPump;
            PersistencePipelineCounters = persistencePipelineCounters;
            PersistenceQueue = persistenceQueue;
            LifecycleMailbox = lifecycleMailbox;
            PipelineHealth = pipelineHealth;
        }

        public TickDiagnosticsSnapshot Tick { get; }
        public TransportBackpressureDiagnostics Transport { get; }
        public CompletionQueueMetrics? PersistenceCompletionMailbox { get; }
        public CommandIngestorDiagnostics Commands { get; }
        public HandshakePipelineMetrics Handshakes { get; }
        public InboundPumpDiagnostics InboundPump { get; }
        public PersistencePipelineCounterSnapshot? PersistencePipelineCounters { get; }
        public PersistenceQueueMetrics? PersistenceQueue { get; }
        public LifecycleMailboxCounters LifecycleMailbox { get; }
        public RuntimePipelineHealthSnapshot? PipelineHealth { get; }
        public bool HasDetectedStall => Tick.StallDetections > 0;
    }

    public readonly struct LifecycleMailboxCounters
    {
        public LifecycleMailboxCounters(long enqueued, long applied, long disconnectsApplied, long dropped)
        {
            LifecycleOpsEnqueued = enqueued;
            LifecycleOpsApplied = applied;
            DisconnectsApplied = disconnectsApplied;
            LifecycleOpsDropped = dropped;
        }

        public long LifecycleOpsEnqueued { get; }
        public long LifecycleOpsApplied { get; }
        public long DisconnectsApplied { get; }
        public long LifecycleOpsDropped { get; }
    }
}
