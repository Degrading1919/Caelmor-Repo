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
            maxPersistenceWritesGlobal: 128,
            maxPersistenceCompletions: 128,
            maxPersistenceCompletionBytes: 512 * 1024);

        public RuntimeBackpressureConfig(
            int maxInboundCommandsPerSession,
            int maxOutboundSnapshotsPerSession,
            int maxQueuedBytesPerSession,
            int maxPersistenceWritesPerPlayer,
            int maxPersistenceWritesGlobal,
            int maxPersistenceCompletions,
            int maxPersistenceCompletionBytes)
            : this(
                maxInboundCommandsPerSession,
                maxOutboundSnapshotsPerSession,
                maxQueuedBytesPerSession,
                maxPersistenceWritesPerPlayer,
                maxPersistenceWritesGlobal,
                maxPersistenceCompletions,
                maxPersistenceCompletionBytes,
                skipValidation: false)
        {
        }

        public RuntimeBackpressureConfig(
            int maxInboundCommandsPerSession,
            int maxOutboundSnapshotsPerSession,
            int maxQueuedBytesPerSession,
            int maxPersistenceWritesPerPlayer,
            int maxPersistenceWritesGlobal)
            : this(
                maxInboundCommandsPerSession,
                maxOutboundSnapshotsPerSession,
                maxQueuedBytesPerSession,
                maxPersistenceWritesPerPlayer,
                maxPersistenceWritesGlobal,
                maxPersistenceCompletions: 128,
                maxPersistenceCompletionBytes: 512 * 1024,
                skipValidation: false)
        {
        }

        private RuntimeBackpressureConfig(
            int maxInboundCommandsPerSession,
            int maxOutboundSnapshotsPerSession,
            int maxQueuedBytesPerSession,
            int maxPersistenceWritesPerPlayer,
            int maxPersistenceWritesGlobal,
            int maxPersistenceCompletions,
            int maxPersistenceCompletionBytes,
            bool skipValidation)
        {
            if (!skipValidation)
            {
                if (maxInboundCommandsPerSession <= 0) throw new ArgumentOutOfRangeException(nameof(maxInboundCommandsPerSession));
                if (maxOutboundSnapshotsPerSession <= 0) throw new ArgumentOutOfRangeException(nameof(maxOutboundSnapshotsPerSession));
                if (maxQueuedBytesPerSession <= 0) throw new ArgumentOutOfRangeException(nameof(maxQueuedBytesPerSession));
                if (maxPersistenceWritesPerPlayer <= 0) throw new ArgumentOutOfRangeException(nameof(maxPersistenceWritesPerPlayer));
                if (maxPersistenceWritesGlobal <= 0) throw new ArgumentOutOfRangeException(nameof(maxPersistenceWritesGlobal));
                if (maxPersistenceCompletions <= 0) throw new ArgumentOutOfRangeException(nameof(maxPersistenceCompletions));
                if (maxPersistenceCompletionBytes <= 0) throw new ArgumentOutOfRangeException(nameof(maxPersistenceCompletionBytes));
            }

            MaxInboundCommandsPerSession = maxInboundCommandsPerSession;
            MaxOutboundSnapshotsPerSession = maxOutboundSnapshotsPerSession;
            MaxQueuedBytesPerSession = maxQueuedBytesPerSession;
            MaxPersistenceWritesPerPlayer = maxPersistenceWritesPerPlayer;
            MaxPersistenceWritesGlobal = maxPersistenceWritesGlobal;
            MaxPersistenceCompletions = maxPersistenceCompletions;
            MaxPersistenceCompletionBytes = maxPersistenceCompletionBytes;
        }

        public int MaxInboundCommandsPerSession { get; }
        public int MaxOutboundSnapshotsPerSession { get; }
        public int MaxQueuedBytesPerSession { get; }
        public int MaxPersistenceWritesPerPlayer { get; }
        public int MaxPersistenceWritesGlobal { get; }
        public int MaxPersistenceCompletions { get; }
        public int MaxPersistenceCompletionBytes { get; }
    }
}
