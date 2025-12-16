using System;

namespace Caelmor.Runtime
{
    /// <summary>
    /// Centralized runtime budgets for inbound/outbound queues and persistence write buffers.
    /// The defaults are intentionally conservative to avoid LOH fragmentation and to keep
    /// tick execution deterministic under backpressure.
    /// </summary>
    public sealed class RuntimeBackpressureConfig
    {
        public static RuntimeBackpressureConfig Default { get; } = new RuntimeBackpressureConfig(
            maxInboundCommandsPerSession: 64,
            maxOutboundSnapshotsPerSession: 8,
            maxQueuedBytesPerSession: 256 * 1024,
            maxPersistenceWritesPerPlayer: 16,
            maxPersistenceWritesGlobal: 128);

        public RuntimeBackpressureConfig(
            int maxInboundCommandsPerSession,
            int maxOutboundSnapshotsPerSession,
            int maxQueuedBytesPerSession,
            int maxPersistenceWritesPerPlayer,
            int maxPersistenceWritesGlobal)
        {
            if (maxInboundCommandsPerSession <= 0) throw new ArgumentOutOfRangeException(nameof(maxInboundCommandsPerSession));
            if (maxOutboundSnapshotsPerSession <= 0) throw new ArgumentOutOfRangeException(nameof(maxOutboundSnapshotsPerSession));
            if (maxQueuedBytesPerSession <= 0) throw new ArgumentOutOfRangeException(nameof(maxQueuedBytesPerSession));
            if (maxPersistenceWritesPerPlayer <= 0) throw new ArgumentOutOfRangeException(nameof(maxPersistenceWritesPerPlayer));
            if (maxPersistenceWritesGlobal <= 0) throw new ArgumentOutOfRangeException(nameof(maxPersistenceWritesGlobal));

            MaxInboundCommandsPerSession = maxInboundCommandsPerSession;
            MaxOutboundSnapshotsPerSession = maxOutboundSnapshotsPerSession;
            MaxQueuedBytesPerSession = maxQueuedBytesPerSession;
            MaxPersistenceWritesPerPlayer = maxPersistenceWritesPerPlayer;
            MaxPersistenceWritesGlobal = maxPersistenceWritesGlobal;
        }

        public int MaxInboundCommandsPerSession { get; }
        public int MaxOutboundSnapshotsPerSession { get; }
        public int MaxQueuedBytesPerSession { get; }
        public int MaxPersistenceWritesPerPlayer { get; }
        public int MaxPersistenceWritesGlobal { get; }
    }
}
