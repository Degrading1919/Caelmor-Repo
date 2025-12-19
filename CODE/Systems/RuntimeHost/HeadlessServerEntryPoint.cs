using System;
using System.Threading;
using Caelmor.Runtime.Integration;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Persistence;
using Caelmor.Runtime.Replication;
using Caelmor.Runtime.Sessions;
using Caelmor.Systems;

namespace Caelmor.Runtime.Host
{
    /// <summary>
    /// Headless runtime entrypoint that constructs and runs the authoritative host without Unity.
    /// </summary>
    public static class HeadlessServerEntryPoint
    {
        private const string PersistenceModeEnvKey = "CAELMOR_PERSISTENCE";
        private const string PersistenceWriterEnvKey = "CAELMOR_PERSISTENCE_WRITER";

        public static int Main(string[] args)
        {
            if (InProcTransportProofHarness.TryRun(args, out var proofExitCode))
                return proofExitCode;

            var metrics = new HeadlessServerEntryPointMetrics();
            metrics.RecordLaunch();

            if (!TryBuildSettings(args, metrics, out var settings, out var persistenceLog, out var errorMessage))
            {
                Console.Error.WriteLine(errorMessage);
                return 2;
            }

            Console.WriteLine(persistenceLog);

            ServerRuntimeHost host;
            try
            {
                host = RuntimeCompositionRoot.CreateHost(settings);
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"RUNTIME_HOST_BUILD_FAILED: {ex}");
                metrics.RecordHostBuildFailed();
                return 1;
            }

            var shutdownSignal = new ManualResetEventSlim(false);
            var shutdownGate = new ShutdownGate(shutdownSignal);

            Console.CancelKeyPress += shutdownGate.OnCancelKeyPress;
            AppDomain.CurrentDomain.ProcessExit += shutdownGate.OnProcessExit;

            try
            {
                host.Start();
                metrics.RecordHostStarted();
                Console.WriteLine("Headless runtime host started.");
                shutdownSignal.Wait();
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"RUNTIME_HOST_START_FAILED: {ex}");
                metrics.RecordHostStartFailed();
                return 1;
            }
            finally
            {
                try
                {
                    host.Stop();
                }
                finally
                {
                    host.Dispose();
                }

                Console.WriteLine("Headless runtime host stopped.");
            }

            return 0;
        }

        private static bool TryBuildSettings(
            string[] args,
            HeadlessServerEntryPointMetrics metrics,
            out RuntimeCompositionSettings settings,
            out string persistenceLog,
            out string errorMessage)
        {
            settings = null;
            persistenceLog = string.Empty;
            errorMessage = string.Empty;

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

            var controlChannel = new NullClientControlChannel();
            var handoff = new OnboardingHandoffService(controlChannel);
            var stateReader = new NullReplicationStateReader();
            var outboundSender = NullOutboundTransportSender.Instance;

            settings = new RuntimeCompositionSettings(sessionSystem, handoff, snapshotEligibility, stateReader, outboundSender)
            {
                ActiveSessions = activeSessions,
                ConfigureCommandHandlers = RegisterNoOpCommandHandlers
            };

            var persistenceMode = ResolvePersistenceMode(args);
            if (!TryConfigurePersistence(persistenceMode, metrics, out var persistenceSettings, out persistenceLog, out errorMessage))
            {
                return false;
            }

            settings.Persistence = persistenceSettings;
            return true;
        }

        private static void RegisterNoOpCommandHandlers(CommandHandlerRegistry registry)
        {
            if (registry == null) throw new ArgumentNullException(nameof(registry));
            registry.Register(1, new NoOpCommandHandler());
        }

        private static PersistenceMode ResolvePersistenceMode(string[] args)
        {
            if (args != null)
            {
                for (int i = 0; i < args.Length; i++)
                {
                    var arg = args[i];
                    if (string.IsNullOrWhiteSpace(arg))
                        continue;

                    if (arg.StartsWith("--persistence=", StringComparison.OrdinalIgnoreCase))
                    {
                        var value = arg.Substring("--persistence=".Length);
                        if (TryParsePersistenceMode(value, out var mode))
                            return mode;
                    }

                    if (string.Equals(arg, "--persistence", StringComparison.OrdinalIgnoreCase) && i + 1 < args.Length)
                    {
                        var value = args[i + 1];
                        if (TryParsePersistenceMode(value, out var mode))
                            return mode;
                    }
                }
            }

            var env = Environment.GetEnvironmentVariable(PersistenceModeEnvKey);
            if (!string.IsNullOrWhiteSpace(env) && TryParsePersistenceMode(env, out var envMode))
                return envMode;

            return PersistenceMode.Auto;
        }

        private static bool TryConfigurePersistence(
            PersistenceMode mode,
            HeadlessServerEntryPointMetrics metrics,
            out PersistenceSettings persistenceSettings,
            out string persistenceLog,
            out string errorMessage)
        {
            persistenceSettings = null;
            persistenceLog = string.Empty;
            errorMessage = string.Empty;

            if (mode == PersistenceMode.Disabled)
            {
                metrics.RecordPersistenceDisabled(PersistenceDisableReason.ExplicitlyDisabled);
                persistenceLog = "Persistence disabled by configuration.";
                return true;
            }

            var writer = TryCreatePersistenceWriter(out var writerDescription);
            if (writer == null)
            {
                metrics.RecordPersistenceDisabled(PersistenceDisableReason.MissingWriter);
                persistenceLog = "Persistence disabled (no writer available).";

                if (mode == PersistenceMode.Enabled)
                {
                    errorMessage = "Persistence was forced on but no writer is available. Set CAELMOR_PERSISTENCE_WRITER=memory or provide a writer implementation.";
                    return false;
                }

                return true;
            }

            metrics.RecordPersistenceEnabled();
            persistenceLog = $"Persistence enabled ({writerDescription}).";
            persistenceSettings = new PersistenceSettings(writer);
            return true;
        }

        private static IPersistenceWriter TryCreatePersistenceWriter(out string description)
        {
            description = "none";
            var writerMode = Environment.GetEnvironmentVariable(PersistenceWriterEnvKey);
            if (string.IsNullOrWhiteSpace(writerMode))
                return null;

            if (string.Equals(writerMode, "memory", StringComparison.OrdinalIgnoreCase))
            {
                description = "in-memory writer";
                return new InMemoryPersistenceWriter();
            }

            description = $"unknown writer '{writerMode}'";
            return null;
        }

        private static bool TryParsePersistenceMode(string value, out PersistenceMode mode)
        {
            if (string.Equals(value, "1", StringComparison.OrdinalIgnoreCase) ||
                string.Equals(value, "true", StringComparison.OrdinalIgnoreCase) ||
                string.Equals(value, "on", StringComparison.OrdinalIgnoreCase) ||
                string.Equals(value, "enabled", StringComparison.OrdinalIgnoreCase))
            {
                mode = PersistenceMode.Enabled;
                return true;
            }

            if (string.Equals(value, "0", StringComparison.OrdinalIgnoreCase) ||
                string.Equals(value, "false", StringComparison.OrdinalIgnoreCase) ||
                string.Equals(value, "off", StringComparison.OrdinalIgnoreCase) ||
                string.Equals(value, "disabled", StringComparison.OrdinalIgnoreCase))
            {
                mode = PersistenceMode.Disabled;
                return true;
            }

            if (string.Equals(value, "auto", StringComparison.OrdinalIgnoreCase))
            {
                mode = PersistenceMode.Auto;
                return true;
            }

            mode = PersistenceMode.Auto;
            return false;
        }

        private sealed class ShutdownGate
        {
            private readonly ManualResetEventSlim _signal;
            private int _signaled;

            public ShutdownGate(ManualResetEventSlim signal)
            {
                _signal = signal ?? throw new ArgumentNullException(nameof(signal));
            }

            public void OnCancelKeyPress(object sender, ConsoleCancelEventArgs e)
            {
                e.Cancel = true;
                Signal();
            }

            public void OnProcessExit(object sender, EventArgs e)
            {
                Signal();
            }

            private void Signal()
            {
                if (Interlocked.Exchange(ref _signaled, 1) == 0)
                {
                    _signal.Set();
                }
            }
        }

        private enum PersistenceMode
        {
            Auto = 0,
            Enabled = 1,
            Disabled = 2
        }

        private enum PersistenceDisableReason
        {
            ExplicitlyDisabled = 0,
            MissingWriter = 1
        }

        private sealed class HeadlessServerEntryPointMetrics
        {
            private long _launchCount;
            private long _hostStarted;
            private long _hostBuildFailed;
            private long _hostStartFailed;
            private long _persistenceEnabled;
            private long _persistenceDisabledExplicit;
            private long _persistenceDisabledMissingWriter;

            public void RecordLaunch() => Interlocked.Increment(ref _launchCount);
            public void RecordHostStarted() => Interlocked.Increment(ref _hostStarted);
            public void RecordHostBuildFailed() => Interlocked.Increment(ref _hostBuildFailed);
            public void RecordHostStartFailed() => Interlocked.Increment(ref _hostStartFailed);
            public void RecordPersistenceEnabled() => Interlocked.Increment(ref _persistenceEnabled);

            public void RecordPersistenceDisabled(PersistenceDisableReason reason)
            {
                if (reason == PersistenceDisableReason.ExplicitlyDisabled)
                    Interlocked.Increment(ref _persistenceDisabledExplicit);
                else
                    Interlocked.Increment(ref _persistenceDisabledMissingWriter);
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
