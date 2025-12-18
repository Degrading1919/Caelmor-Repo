using System;
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
        private readonly VisibilityCullingService _visibility;
        private readonly ClientReplicationSnapshotSystem _replication;
        private readonly DeterministicEntityRegistry _entities;
        private readonly PersistenceCompletionQueue _persistenceCompletions;
        private readonly PersistenceWriteQueue _persistenceWrites;
        private readonly PersistenceWorkerLoop _persistenceWorker;
        private readonly PersistencePipelineCounters _persistenceCounters;
        private readonly InboundPumpTickHook _inboundPump;
        private readonly OutboundSendPump _outboundPump;

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
            InboundPumpTickHook inboundPump,
            OutboundSendPump outboundPump,
            PersistenceCompletionQueue persistenceCompletions = null,
            PersistenceWriteQueue persistenceWrites = null,
            PersistenceWorkerLoop persistenceWorker = null,
            PersistencePipelineCounters persistenceCounters = null)
        {
            _simulation = simulation ?? throw new ArgumentNullException(nameof(simulation));
            _transport = transport ?? throw new ArgumentNullException(nameof(transport));
            _handshakes = handshakes ?? throw new ArgumentNullException(nameof(handshakes));
            _commands = commands ?? throw new ArgumentNullException(nameof(commands));
            _visibility = visibility ?? throw new ArgumentNullException(nameof(visibility));
            _replication = replication ?? throw new ArgumentNullException(nameof(replication));
            _entities = entities ?? throw new ArgumentNullException(nameof(entities));
            _inboundPump = inboundPump ?? throw new ArgumentNullException(nameof(inboundPump));
            _outboundPump = outboundPump ?? throw new ArgumentNullException(nameof(outboundPump));
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
            VisibilityCullingService visibility,
            ClientReplicationSnapshotSystem replication,
            DeterministicEntityRegistry entities,
            ReadOnlySpan<ISimulationEligibilityGate> eligibilityGates,
            ReadOnlySpan<ParticipantRegistration> participants,
            ReadOnlySpan<PhaseHookRegistration> phaseHooks,
            IActiveSessionIndex activeSessions = null,
            int commandFreezeHookOrderKey = int.MinValue,
            int handshakeProcessingHookOrderKey = int.MinValue + 1,
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
            PersistenceWriteQueue persistenceWrites = null,
            PersistenceWorkerLoop persistenceWorker = null,
            PersistencePipelineCounters persistenceCounters = null)
        {
            if (activeSessions == null)
                throw new ArgumentNullException(nameof(activeSessions));
            if (replication == null)
                throw new ArgumentNullException(nameof(replication));

            int hookCount = phaseHooks.Length + 3;
            bool includePersistence = persistenceCompletions != null && persistenceCompletionApplier != null;
            if (includePersistence)
                hookCount++;

            var combinedHooks = new PhaseHookRegistration[hookCount];
            int index = 0;

            var inboundPump = new InboundPumpTickHook(transport, commands, activeSessions, inboundFramesPerTick, ingressCommandsPerTick);
            combinedHooks[index++] = new PhaseHookRegistration(inboundPump, commandFreezeHookOrderKey);

            combinedHooks[index++] = new PhaseHookRegistration(
                new HandshakeProcessingPhaseHook(handshakes, handshakePerTickBudget),
                handshakeProcessingHookOrderKey);

            for (int i = 0; i < phaseHooks.Length; i++)
                combinedHooks[index++] = phaseHooks[i];

            if (includePersistence)
            {
                combinedHooks[index++] = new PhaseHookRegistration(
                new PersistenceCompletionPhaseHook(persistenceCompletions, persistenceCompletionApplier),
                    persistenceCompletionHookOrderKey);
            }

            combinedHooks[index++] = new PhaseHookRegistration(replication, replicationHookOrderKey);

            var counters = replicationCounters ?? transport.SnapshotCounters;
            var sender = outboundSender ?? NullOutboundTransportSender.Instance;
            var outboundPump = new OutboundSendPump(transport, sender, activeSessions, transport.Config, counters, outboundSendPerIteration, outboundPumpIdleMs);

            WorldBootstrapRegistration.Apply(simulation, eligibilityGates, participants, combinedHooks);
            return new RuntimeServerLoop(
                simulation,
                transport,
                handshakes,
                commands,
                visibility,
                replication,
                entities,
                inboundPump,
                outboundPump,
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
            _transport.DropAllForSession(sessionId);
            _commands.DropSession(sessionId);
            _visibility.RemoveSession(sessionId);
            _replication.OnSessionDisconnected(sessionId);
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
            return new RuntimeDiagnosticsSnapshot(tick, transport, persistenceCompletions, commands, handshakes, inboundPump, persistenceCounters, persistenceQueue);
        }

        private void ClearTransientState()
        {
            _transport.Clear();
            _handshakes.Reset();
            _commands.Clear();
            _visibility.Clear();
            _entities.ClearAll();
            _persistenceCompletions?.Clear();
            _persistenceWrites?.Clear();
        }

        private void OnTickStalled(TickStallEvent stall)
        {
            TickStallDetected?.Invoke(stall);
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
            PersistenceQueueMetrics? persistenceQueue)
        {
            Tick = tick;
            Transport = transport;
            PersistenceCompletionMailbox = persistenceCompletionMailbox;
            Commands = commands;
            Handshakes = handshakes;
            InboundPump = inboundPump;
            PersistencePipelineCounters = persistencePipelineCounters;
            PersistenceQueue = persistenceQueue;
        }

        public TickDiagnosticsSnapshot Tick { get; }
        public TransportBackpressureDiagnostics Transport { get; }
        public CompletionQueueMetrics? PersistenceCompletionMailbox { get; }
        public CommandIngestorDiagnostics Commands { get; }
        public HandshakePipelineMetrics Handshakes { get; }
        public InboundPumpDiagnostics InboundPump { get; }
        public PersistencePipelineCounterSnapshot? PersistencePipelineCounters { get; }
        public PersistenceQueueMetrics? PersistenceQueue { get; }
        public bool HasDetectedStall => Tick.StallDetections > 0;
    }
}
