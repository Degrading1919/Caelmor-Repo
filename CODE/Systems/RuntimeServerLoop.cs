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
        private readonly DeterministicEntityRegistry _entities;
        private readonly PersistenceCompletionQueue _persistenceCompletions;

        private readonly object _gate = new object();
        private bool _started;

        public event Action<TickStallEvent> TickStallDetected;

        public RuntimeServerLoop(
            WorldSimulationCore simulation,
            PooledTransportRouter transport,
            SessionHandshakePipeline handshakes,
            AuthoritativeCommandIngestor commands,
            VisibilityCullingService visibility,
            DeterministicEntityRegistry entities,
            PersistenceCompletionQueue persistenceCompletions = null)
        {
            _simulation = simulation ?? throw new ArgumentNullException(nameof(simulation));
            _transport = transport ?? throw new ArgumentNullException(nameof(transport));
            _handshakes = handshakes ?? throw new ArgumentNullException(nameof(handshakes));
            _commands = commands ?? throw new ArgumentNullException(nameof(commands));
            _visibility = visibility ?? throw new ArgumentNullException(nameof(visibility));
            _entities = entities ?? throw new ArgumentNullException(nameof(entities));
            _persistenceCompletions = persistenceCompletions;

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
            DeterministicEntityRegistry entities,
            ReadOnlySpan<ISimulationEligibilityGate> eligibilityGates,
            ReadOnlySpan<ParticipantRegistration> participants,
            ReadOnlySpan<PhaseHookRegistration> phaseHooks,
            IActiveSessionIndex activeSessions = null,
            int commandFreezeHookOrderKey = int.MinValue,
            PersistenceCompletionQueue persistenceCompletions = null,
            IPersistenceCompletionApplier persistenceCompletionApplier = null,
            int persistenceCompletionHookOrderKey = -1024)
        {
            int hookCount = phaseHooks.Length + 1;
            bool includePersistence = persistenceCompletions != null && persistenceCompletionApplier != null;
            if (includePersistence)
                hookCount++;

            var combinedHooks = new PhaseHookRegistration[hookCount];
            int index = 0;

            combinedHooks[index++] = new PhaseHookRegistration(
                new AuthoritativeCommandFreezeHook(commands, activeSessions),
                commandFreezeHookOrderKey);

            for (int i = 0; i < phaseHooks.Length; i++)
                combinedHooks[index++] = phaseHooks[i];

            if (includePersistence)
            {
                combinedHooks[index++] = new PhaseHookRegistration(
                    new PersistenceCompletionPhaseHook(persistenceCompletions, persistenceCompletionApplier),
                    persistenceCompletionHookOrderKey);
            }

            WorldBootstrapRegistration.Apply(simulation, eligibilityGates, participants, combinedHooks);
            return new RuntimeServerLoop(simulation, transport, handshakes, commands, visibility, entities, persistenceCompletions);
        }

        public void Start()
        {
            lock (_gate)
            {
                if (_started)
                    return;

                _simulation.Start();
                _started = true;
            }
        }

        public void Stop()
        {
            lock (_gate)
            {
                if (!_started)
                    return;

                _simulation.Stop();
                ClearTransientState();
                _started = false;
            }
        }

        /// <summary>
        /// Session disconnect path: drop queued transport frames, commands, and visibility caches.
        /// </summary>
        public void OnSessionDisconnected(SessionId sessionId)
        {
            _transport.DropAllForSession(sessionId);
            _commands.DropSession(sessionId);
            _visibility.RemoveSession(sessionId);
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
            _visibility.Dispose();
            _entities.Dispose();
        }

        public RuntimeDiagnosticsSnapshot CaptureDiagnostics()
        {
            var transport = _transport.CaptureDiagnostics();
            var tick = _simulation.Diagnostics;
            var commands = _commands.SnapshotMetrics();
            var persistenceCompletions = _persistenceCompletions?.SnapshotMetrics();
            return new RuntimeDiagnosticsSnapshot(tick, transport, persistenceCompletions, commands);
        }

        private void ClearTransientState()
        {
            _transport.Clear();
            _handshakes.Reset();
            _commands.Clear();
            _visibility.Clear();
            _entities.ClearAll();
            _persistenceCompletions?.Clear();
        }

        private void OnTickStalled(TickStallEvent stall)
        {
            TickStallDetected?.Invoke(stall);
        }
    }

    public readonly struct RuntimeDiagnosticsSnapshot
    {
        public RuntimeDiagnosticsSnapshot(
            TickDiagnosticsSnapshot tick,
            TransportBackpressureDiagnostics transport,
            CompletionQueueMetrics? persistenceCompletionMailbox,
            CommandIngestorDiagnostics commands)
        {
            Tick = tick;
            Transport = transport;
            PersistenceCompletionMailbox = persistenceCompletionMailbox;
            Commands = commands;
        }

        public TickDiagnosticsSnapshot Tick { get; }
        public TransportBackpressureDiagnostics Transport { get; }
        public CompletionQueueMetrics? PersistenceCompletionMailbox { get; }
        public CommandIngestorDiagnostics Commands { get; }
        public bool HasDetectedStall => Tick.StallDetections > 0;
    }
}
