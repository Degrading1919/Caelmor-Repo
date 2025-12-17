using System;
using Caelmor.Runtime.Integration;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Persistence;
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
            PersistenceCompletionQueue persistenceCompletions = null,
            IPersistenceCompletionApplier persistenceCompletionApplier = null,
            int persistenceCompletionHookOrderKey = -1024)
        {
            ReadOnlySpan<PhaseHookRegistration> hooksSpan = phaseHooks;
            PhaseHookRegistration[] combinedHooks = null;

            if (persistenceCompletions != null && persistenceCompletionApplier != null)
            {
                combinedHooks = new PhaseHookRegistration[phaseHooks.Length + 1];
                for (int i = 0; i < phaseHooks.Length; i++)
                    combinedHooks[i] = phaseHooks[i];

                combinedHooks[^1] = new PhaseHookRegistration(
                    new PersistenceCompletionPhaseHook(persistenceCompletions, persistenceCompletionApplier),
                    persistenceCompletionHookOrderKey);
                hooksSpan = combinedHooks;
            }

            WorldBootstrapRegistration.Apply(simulation, eligibilityGates, participants, hooksSpan);
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
            _transport.Dispose();
            _visibility.Dispose();
            _entities.Dispose();
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
    }
}
