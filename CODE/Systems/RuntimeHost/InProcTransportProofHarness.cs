using System;
using System.Diagnostics;
using System.Threading;
using Caelmor.Runtime.Integration;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Replication;
using Caelmor.Runtime.Sessions;
using Caelmor.Runtime.Transport;
using Caelmor.Runtime.WorldSimulation;

namespace Caelmor.Runtime.Host
{
    internal static class InProcTransportProofHarness
    {
        private const string ProofFlag = "--transport-proof";
        private const string CommandTypeName = "validation.session_command_count";
        private const int ProofTicks = 4;
        private const int WaitTimeoutMs = 2000;

        public static bool TryRun(string[] args, out int exitCode)
        {
            exitCode = 0;

            if (!HasFlag(args))
                return false;

            try
            {
                RunProof();
                return true;
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"TRANSPORT_PROOF_FAILED: {ex.Message}");
                exitCode = 1;
                return true;
            }
        }

        private static bool HasFlag(string[] args)
        {
            if (args == null)
                return false;

            for (int i = 0; i < args.Length; i++)
            {
                if (string.Equals(args[i], ProofFlag, StringComparison.OrdinalIgnoreCase))
                    return true;
            }

            return false;
        }

        private static void RunProof()
        {
            var activeSessions = new DeterministicActiveSessionIndex();
            var snapshotEligibility = new SnapshotEligibilityRegistry();

            var authority = new ServerAuthority();
            var saveBinding = new DeterministicSaveBindingQuery();
            var restore = new AlwaysRestoredQuery();
            var mutationGate = new AlwaysAllowSessionMutationGate();
            var sessionEvents = new NoOpSessionEvents();

            var sessionSystem = new ActiveSessionIndexedPlayerSessionSystem(
                authority,
                saveBinding,
                restore,
                snapshotEligibility,
                mutationGate,
                sessionEvents,
                activeSessions);

            var handoff = new OnboardingHandoffService(new NullClientControlChannel());
            var stateReader = new NullReplicationStateReader();
            var commandHandlers = new CommandHandlerRegistry();
            var handler = new SessionCommandCounterHandler(sessionSystem.Inner);
            var commandType = PooledTransportRouter.ComputeStableCommandType(CommandTypeName);
            commandHandlers.Register(commandType, handler);

            var settings = new RuntimeCompositionSettings(
                sessionSystem,
                handoff,
                snapshotEligibility,
                stateReader,
                NullOutboundTransportSender.Instance)
            {
                ActiveSessions = activeSessions,
                CommandHandlers = commandHandlers
            };

            ServerRuntimeHost host = null;
            try
            {
                host = RuntimeCompositionRoot.CreateHost(settings);
                host.Start();

                var spawnHelper = new InProcSessionSpawnHelper(host.RuntimeLoop.Handshakes, sessionSystem);
                if (!spawnHelper.TryEnqueueSpawn(new PlayerId(1), out var sessionId))
                    throw new InvalidOperationException("TRANSPORT_PROOF_SESSION_ENQUEUE_FAILED");

                WaitForSessionActivation(spawnHelper, sessionId);

                var transport = new InProcTransportAdapter(host.RuntimeLoop.Transport);
                if (!transport.TryEnqueueInbound(sessionId, payloadA: 7, payloadB: 0, commandType: CommandTypeName, submitTick: 0))
                    throw new InvalidOperationException("TRANSPORT_PROOF_COMMAND_ENQUEUE_FAILED");

                WaitForTicks(host.Simulation, ProofTicks);

                var diagnostics = host.RuntimeLoop.CaptureDiagnostics();
                var proof = host.CaptureProofOfLife();

                if (diagnostics.InboundPump.CommandsEnqueuedToIngestor <= 0)
                    throw new InvalidOperationException("TRANSPORT_PROOF_NO_COMMANDS_ENQUEUED");

                if (proof.FrozenBatchesConsumed <= 0)
                    throw new InvalidOperationException("TRANSPORT_PROOF_NO_BATCHES_CONSUMED");

                if (!sessionSystem.Inner.TryGetCommandMetrics(sessionId, out var metrics) || metrics.CommandCount <= 0)
                    throw new InvalidOperationException("TRANSPORT_PROOF_NO_SESSION_MUTATION");

                if (handler.MutationsObserved <= 0)
                    throw new InvalidOperationException("TRANSPORT_PROOF_NO_HANDLER_MUTATION");
            }
            finally
            {
                if (host != null)
                {
                    host.Stop();
                    host.Dispose();
                }
            }
        }

        private static void WaitForSessionActivation(InProcSessionSpawnHelper spawnHelper, SessionId sessionId)
        {
            var watch = Stopwatch.StartNew();
            while (!spawnHelper.IsSessionActive(sessionId))
            {
                if (watch.ElapsedMilliseconds > WaitTimeoutMs)
                    throw new InvalidOperationException("TRANSPORT_PROOF_SESSION_TIMEOUT");

                Thread.Sleep(1);
            }
        }

        private static void WaitForTicks(WorldSimulationCore simulation, int ticksToAdvance)
        {
            var target = simulation.CurrentTickIndex + ticksToAdvance;
            var watch = Stopwatch.StartNew();

            while (simulation.CurrentTickIndex < target)
            {
                if (watch.ElapsedMilliseconds > WaitTimeoutMs)
                    throw new InvalidOperationException("TRANSPORT_PROOF_TICK_TIMEOUT");

                Thread.Sleep(1);
            }
        }

        private sealed class ServerAuthority : IServerAuthority
        {
            public bool IsServerAuthoritative => true;
        }

        private sealed class DeterministicSaveBindingQuery : IPlayerSaveBindingQuery
        {
            public bool TryGetSaveForPlayer(PlayerId playerId, out SaveId saveId)
            {
                if (!playerId.IsValid)
                {
                    saveId = default;
                    return false;
                }

                saveId = new SaveId(playerId.Value);
                return true;
            }
        }

        private sealed class AlwaysRestoredQuery : IPersistenceRestoreQuery
        {
            public bool IsRestoreCompleted(SaveId saveId) => saveId.IsValid;
        }

        private sealed class AlwaysAllowSessionMutationGate : ISessionMutationGate
        {
            public bool CanMutateSessionsNow() => true;
        }

        private sealed class NoOpSessionEvents : ISessionEvents
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

        private sealed class NullClientControlChannel : IClientControlChannel
        {
            public void AuthorizeClientControl(SessionId sessionId)
            {
            }
        }

        private sealed class NullReplicationStateReader : IReplicationStateReader
        {
            public ReplicatedEntityState ReadCommittedState(EntityHandle entity)
            {
                return default;
            }
        }
    }
}
