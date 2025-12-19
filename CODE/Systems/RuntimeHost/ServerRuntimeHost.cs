using System;
using System.Collections.Generic;
using System.Threading;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Integration;
using Caelmor.Runtime.Persistence;
using Caelmor.Runtime.Replication;
using Caelmor.Runtime.WorldSimulation;

namespace Caelmor.Runtime.Host
{
    /// <summary>
    /// Runtime host that owns lifecycle start/stop, thread shutdown, and proof-of-life counters.
    /// </summary>
    public sealed class ServerRuntimeHost : IDisposable
    {
        private readonly WorldSimulationCore _simulation;
        private readonly RuntimeServerLoop _runtimeLoop;
        private readonly InboundPumpTickHook _inboundPump;
        private readonly AuthoritativeCommandConsumeTickHook _commandConsumeHook;
        private readonly LifecycleMailboxPhaseHook _lifecycleHook;
        private readonly ClientReplicationSnapshotSystem _replication;
        private readonly OutboundSendPump _outboundPump;
        private readonly IActiveSessionIndex _activeSessions;
        private readonly ReplicationSnapshotCounters _replicationCounters;
        private readonly PersistencePipelineCounters _persistenceCounters;
        private readonly PersistenceWriteQueue _persistenceWrites;
        private readonly PersistenceCompletionQueue _persistenceCompletions;
        private readonly PersistenceWorkerLoop _persistenceWorker;
        private readonly PersistenceApplyState _persistenceApplyState;
        private readonly TickDiagnostics _timeSliceDiagnostics;
        private readonly ServerRuntimeHostCounters _counters = new ServerRuntimeHostCounters();
        private readonly object _gate = new object();
        private bool _started;

        public ServerRuntimeHost(
            WorldSimulationCore simulation,
            RuntimeServerLoop runtimeLoop,
            InboundPumpTickHook inboundPump,
            AuthoritativeCommandConsumeTickHook commandConsumeHook,
            LifecycleMailboxPhaseHook lifecycleHook,
            ClientReplicationSnapshotSystem replication,
            OutboundSendPump outboundPump,
            IActiveSessionIndex activeSessions,
            ReplicationSnapshotCounters replicationCounters,
            PersistencePipelineCounters persistenceCounters,
            PersistenceWriteQueue persistenceWrites,
            PersistenceCompletionQueue persistenceCompletions,
            PersistenceWorkerLoop persistenceWorker,
            PersistenceApplyState persistenceApplyState,
            TickDiagnostics timeSliceDiagnostics)
        {
            _simulation = simulation ?? throw new ArgumentNullException(nameof(simulation));
            _runtimeLoop = runtimeLoop ?? throw new ArgumentNullException(nameof(runtimeLoop));
            _inboundPump = inboundPump ?? throw new ArgumentNullException(nameof(inboundPump));
            _commandConsumeHook = commandConsumeHook ?? throw new ArgumentNullException(nameof(commandConsumeHook));
            _lifecycleHook = lifecycleHook ?? throw new ArgumentNullException(nameof(lifecycleHook));
            _replication = replication ?? throw new ArgumentNullException(nameof(replication));
            _outboundPump = outboundPump ?? throw new ArgumentNullException(nameof(outboundPump));
            _activeSessions = activeSessions ?? throw new ArgumentNullException(nameof(activeSessions));
            _replicationCounters = replicationCounters ?? throw new ArgumentNullException(nameof(replicationCounters));
            _persistenceCounters = persistenceCounters;
            _persistenceWrites = persistenceWrites;
            _persistenceCompletions = persistenceCompletions;
            _persistenceWorker = persistenceWorker;
            _persistenceApplyState = persistenceApplyState;
            _timeSliceDiagnostics = timeSliceDiagnostics;

            _simulation.TickLoopStarted += OnTickLoopStarted;
        }

        public void Start()
        {
            lock (_gate)
            {
                if (_started)
                    return;

                ValidateRequiredHooks();

                _runtimeLoop.Start();
                _counters.RecordHostStarted();
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

            _runtimeLoop.Stop();
        }

        public ServerRuntimeHostProofOfLifeSnapshot CaptureProofOfLife()
        {
            var inbound = _inboundPump.Diagnostics;
            var consume = _commandConsumeHook.Diagnostics;
            var replication = _replicationCounters.Snapshot();
            var persistence = _persistenceCounters?.Snapshot();

            return new ServerRuntimeHostProofOfLifeSnapshot(
                _counters.HostStartedCount,
                _counters.TickStartedCount,
                inbound.InboundPumpTicksExecuted,
                consume.FrozenBatchesConsumed,
                replication.SnapshotsDequeuedForSend,
                persistence?.CompletionsApplied ?? 0);
        }

        public RuntimeServerLoop RuntimeLoop => _runtimeLoop;
        public WorldSimulationCore Simulation => _simulation;
        public IActiveSessionIndex ActiveSessions => _activeSessions;

        public void Dispose()
        {
            _simulation.TickLoopStarted -= OnTickLoopStarted;
            Stop();
            _runtimeLoop.Dispose();
            _simulation.Dispose();
            _persistenceWorker?.Dispose();
            _persistenceWrites?.Dispose();
            _persistenceCompletions?.Dispose();
            _timeSliceDiagnostics?.Dispose();
        }

        private void OnTickLoopStarted()
        {
            _counters.RecordTickStarted();
        }

        private void ValidateRequiredHooks()
        {
            var missing = new List<string>(8);

            if (!_simulation.IsPhaseHookRegistered(_inboundPump))
                missing.Add("inbound_pump_hook");

            if (!_simulation.IsPhaseHookRegistered(_commandConsumeHook))
                missing.Add("command_consume_hook");

            bool freezeRegistered = _simulation.HasPhaseHook<AuthoritativeCommandFreezeHook>() || _simulation.IsPhaseHookRegistered(_inboundPump);
            if (!freezeRegistered)
                missing.Add("command_freeze_hook");

            if (!_simulation.IsPhaseHookRegistered(_lifecycleHook))
                missing.Add("lifecycle_mailbox_hook");

            if (!_simulation.IsPhaseHookRegistered(_replication))
                missing.Add("replication_hook");

            if (_outboundPump == null)
                missing.Add("outbound_send_pump");

            bool persistenceEnabled = _persistenceWorker != null || _persistenceWrites != null || _persistenceCompletions != null || _persistenceApplyState != null;
            if (persistenceEnabled && !_simulation.HasPhaseHook<PersistenceCompletionPhaseHook>())
                missing.Add("persistence_completion_hook");

            if (missing.Count > 0)
                throw new InvalidOperationException($"RUNTIME_PIPELINE_MISSING_HOOKS: {string.Join(", ", missing)}");
        }
    }

    public readonly struct ServerRuntimeHostProofOfLifeSnapshot
    {
        public ServerRuntimeHostProofOfLifeSnapshot(
            long hostStartedCount,
            long tickStartedCount,
            long inboundPumpTicksExecuted,
            long frozenBatchesConsumed,
            long snapshotsDequeuedForSend,
            long persistenceCompletionsApplied)
        {
            HostStartedCount = hostStartedCount;
            TickStartedCount = tickStartedCount;
            InboundPumpTicksExecuted = inboundPumpTicksExecuted;
            FrozenBatchesConsumed = frozenBatchesConsumed;
            SnapshotsDequeuedForSend = snapshotsDequeuedForSend;
            PersistenceCompletionsApplied = persistenceCompletionsApplied;
        }

        public long HostStartedCount { get; }
        public long TickStartedCount { get; }
        public long InboundPumpTicksExecuted { get; }
        public long FrozenBatchesConsumed { get; }
        public long SnapshotsDequeuedForSend { get; }
        public long PersistenceCompletionsApplied { get; }
    }

    public sealed class ServerRuntimeHostCounters
    {
        private long _hostStarted;
        private long _tickStarted;

        public long HostStartedCount => Interlocked.Read(ref _hostStarted);
        public long TickStartedCount => Interlocked.Read(ref _tickStarted);

        public void RecordHostStarted() => Interlocked.Increment(ref _hostStarted);
        public void RecordTickStarted() => Interlocked.Increment(ref _tickStarted);
    }
}
