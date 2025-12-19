using System;
using System.Threading;

namespace Caelmor.Runtime.Diagnostics
{
    /// <summary>
    /// Diagnostics for runtime pipeline liveness. Tracks last tick each critical hook executed,
    /// plus proof-of-life execution counts.
    /// </summary>
    public sealed class RuntimePipelineHealth
    {
        public const int DefaultStaleTicks = 5;

        private readonly RuntimePipelineHookState _lifecycleMailbox = new RuntimePipelineHookState("lifecycle_mailbox");
        private readonly RuntimePipelineHookState _inboundPump = new RuntimePipelineHookState("inbound_pump");
        private readonly RuntimePipelineHookState _commandConsume = new RuntimePipelineHookState("command_consume");
        private readonly RuntimePipelineHookState _handshake = new RuntimePipelineHookState("handshake");
        private readonly RuntimePipelineHookState _replication = new RuntimePipelineHookState("replication");
        private readonly RuntimePipelineHookState _persistenceApply = new RuntimePipelineHookState("persistence_apply");
        private readonly RuntimePipelineHookState _outboundPump = new RuntimePipelineHookState("outbound_send");

        private readonly bool _handshakeEnabled;
        private readonly bool _persistenceEnabled;

        public RuntimePipelineHealth(bool handshakeEnabled, bool persistenceEnabled)
        {
            _handshakeEnabled = handshakeEnabled;
            _persistenceEnabled = persistenceEnabled;
        }

        public void MarkLifecycleMailbox(long tickIndex) => _lifecycleMailbox.Mark(tickIndex);
        public void MarkInboundPump(long tickIndex) => _inboundPump.Mark(tickIndex);
        public void MarkCommandConsume(long tickIndex) => _commandConsume.Mark(tickIndex);
        public void MarkHandshake(long tickIndex) => _handshake.Mark(tickIndex);
        public void MarkReplication(long tickIndex) => _replication.Mark(tickIndex);
        public void MarkPersistenceApply(long tickIndex) => _persistenceApply.Mark(tickIndex);
        public void MarkOutboundSend(long tickIndex) => _outboundPump.Mark(tickIndex);

        public RuntimePipelineHealthSnapshot Snapshot(long currentTick, int staleThresholdTicks)
        {
            var threshold = Math.Max(1, staleThresholdTicks);
            return new RuntimePipelineHealthSnapshot(
                currentTick,
                threshold,
                _lifecycleMailbox.Snapshot(currentTick, threshold, enabled: true),
                _inboundPump.Snapshot(currentTick, threshold, enabled: true),
                _commandConsume.Snapshot(currentTick, threshold, enabled: true),
                _handshake.Snapshot(currentTick, threshold, enabled: _handshakeEnabled),
                _replication.Snapshot(currentTick, threshold, enabled: true),
                _persistenceApply.Snapshot(currentTick, threshold, enabled: _persistenceEnabled),
                _outboundPump.Snapshot(currentTick, threshold, enabled: true));
        }
    }

    public readonly struct RuntimePipelineHealthSnapshot
    {
        public RuntimePipelineHealthSnapshot(
            long currentTick,
            int staleThresholdTicks,
            RuntimePipelineHookSnapshot lifecycleMailbox,
            RuntimePipelineHookSnapshot inboundPump,
            RuntimePipelineHookSnapshot commandConsume,
            RuntimePipelineHookSnapshot handshake,
            RuntimePipelineHookSnapshot replication,
            RuntimePipelineHookSnapshot persistenceApply,
            RuntimePipelineHookSnapshot outboundSend)
        {
            CurrentTick = currentTick;
            StaleThresholdTicks = staleThresholdTicks;
            LifecycleMailbox = lifecycleMailbox;
            InboundPump = inboundPump;
            CommandConsume = commandConsume;
            Handshake = handshake;
            Replication = replication;
            PersistenceApply = persistenceApply;
            OutboundSend = outboundSend;
        }

        public long CurrentTick { get; }
        public int StaleThresholdTicks { get; }
        public RuntimePipelineHookSnapshot LifecycleMailbox { get; }
        public RuntimePipelineHookSnapshot InboundPump { get; }
        public RuntimePipelineHookSnapshot CommandConsume { get; }
        public RuntimePipelineHookSnapshot Handshake { get; }
        public RuntimePipelineHookSnapshot Replication { get; }
        public RuntimePipelineHookSnapshot PersistenceApply { get; }
        public RuntimePipelineHookSnapshot OutboundSend { get; }

        public bool HasStaleHooks =>
            LifecycleMailbox.IsStale ||
            InboundPump.IsStale ||
            CommandConsume.IsStale ||
            Handshake.IsStale ||
            Replication.IsStale ||
            PersistenceApply.IsStale ||
            OutboundSend.IsStale;
    }

    public readonly struct RuntimePipelineHookSnapshot
    {
        public RuntimePipelineHookSnapshot(string name, bool enabled, long lastTick, long executions, bool isStale)
        {
            Name = name ?? string.Empty;
            Enabled = enabled;
            LastTick = lastTick;
            Executions = executions;
            IsStale = enabled && isStale;
        }

        public string Name { get; }
        public bool Enabled { get; }
        public long LastTick { get; }
        public long Executions { get; }
        public bool IsStale { get; }
    }

    internal sealed class RuntimePipelineHookState
    {
        private readonly string _name;
        private long _lastTick;
        private long _executions;

        public RuntimePipelineHookState(string name)
        {
            _name = name ?? string.Empty;
        }

        public void Mark(long tickIndex)
        {
            Volatile.Write(ref _lastTick, tickIndex);
            Interlocked.Increment(ref _executions);
        }

        public RuntimePipelineHookSnapshot Snapshot(long currentTick, int threshold, bool enabled)
        {
            if (!enabled)
                return new RuntimePipelineHookSnapshot(_name, enabled: false, lastTick: 0, executions: 0, isStale: false);

            var lastTick = Volatile.Read(ref _lastTick);
            var executions = Interlocked.Read(ref _executions);
            bool stale = currentTick > 0 && (lastTick == 0 || currentTick - lastTick >= threshold);
            return new RuntimePipelineHookSnapshot(_name, enabled: true, lastTick, executions, stale);
        }
    }
}
