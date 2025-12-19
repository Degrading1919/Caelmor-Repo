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
            maxInboundCommandAgeTicks: 4,
            maxInboundCommandLeadTicks: 0,
            maxOutboundSnapshotsPerSession: 8,
            maxQueuedBytesPerSession: 256 * 1024,
            maxPersistenceWritesPerPlayer: 16,
            maxPersistenceWritesGlobal: 128,
            maxPersistenceWriteBytesPerPlayer: 1024 * 1024,
            maxPersistenceWriteBytesGlobal: 8 * 1024 * 1024,
            maxPersistenceCompletions: 128,
            maxPersistenceCompletionBytes: 512 * 1024,
            maxLifecycleOps: 256,
            maxLifecycleOpBytes: 64 * 1024,
            expectedMaxSessions: 128,
            expectedMaxCommandsPerSessionPerTick: 32,
            expectedMaxSnapshotsQueuedPerSession: 8);

        public RuntimeBackpressureConfig(
            int maxInboundCommandsPerSession,
            int maxInboundCommandAgeTicks,
            int maxInboundCommandLeadTicks,
            int maxOutboundSnapshotsPerSession,
            int maxQueuedBytesPerSession,
            int maxPersistenceWritesPerPlayer,
            int maxPersistenceWritesGlobal,
            int maxPersistenceWriteBytesPerPlayer,
            int maxPersistenceWriteBytesGlobal,
            int maxPersistenceCompletions,
            int maxPersistenceCompletionBytes,
            int expectedMaxSessions,
            int expectedMaxCommandsPerSessionPerTick,
            int expectedMaxSnapshotsQueuedPerSession)
            : this(
                maxInboundCommandsPerSession,
                maxInboundCommandAgeTicks,
                maxInboundCommandLeadTicks,
                maxOutboundSnapshotsPerSession,
                maxQueuedBytesPerSession,
                maxPersistenceWritesPerPlayer,
                maxPersistenceWritesGlobal,
                maxPersistenceWriteBytesPerPlayer,
                maxPersistenceWriteBytesGlobal,
                maxPersistenceCompletions,
                maxPersistenceCompletionBytes,
                maxLifecycleOps: 256,
                maxLifecycleOpBytes: 64 * 1024,
                expectedMaxSessions: expectedMaxSessions,
                expectedMaxCommandsPerSessionPerTick: expectedMaxCommandsPerSessionPerTick,
                expectedMaxSnapshotsQueuedPerSession: expectedMaxSnapshotsQueuedPerSession,
                skipValidation: false)
        {
        }

        public RuntimeBackpressureConfig(
            int maxInboundCommandsPerSession,
            int maxInboundCommandAgeTicks,
            int maxInboundCommandLeadTicks,
            int maxOutboundSnapshotsPerSession,
            int maxQueuedBytesPerSession,
            int maxPersistenceWritesPerPlayer,
            int maxPersistenceWritesGlobal,
            int maxPersistenceWriteBytesPerPlayer,
            int maxPersistenceWriteBytesGlobal,
            int expectedMaxSessions,
            int expectedMaxCommandsPerSessionPerTick,
            int expectedMaxSnapshotsQueuedPerSession)
            : this(
                maxInboundCommandsPerSession,
                maxInboundCommandAgeTicks,
                maxInboundCommandLeadTicks,
                maxOutboundSnapshotsPerSession,
                maxQueuedBytesPerSession,
                maxPersistenceWritesPerPlayer,
                maxPersistenceWritesGlobal,
                maxPersistenceWriteBytesPerPlayer,
                maxPersistenceWriteBytesGlobal,
                maxPersistenceCompletions: 128,
                maxPersistenceCompletionBytes: 512 * 1024,
                maxLifecycleOps: 256,
                maxLifecycleOpBytes: 64 * 1024,
                expectedMaxSessions: expectedMaxSessions,
                expectedMaxCommandsPerSessionPerTick: expectedMaxCommandsPerSessionPerTick,
                expectedMaxSnapshotsQueuedPerSession: expectedMaxSnapshotsQueuedPerSession,
                skipValidation: false)
        {
        }

        public RuntimeBackpressureConfig(
            int maxInboundCommandsPerSession,
            int maxInboundCommandAgeTicks,
            int maxInboundCommandLeadTicks,
            int maxOutboundSnapshotsPerSession,
            int maxQueuedBytesPerSession,
            int maxPersistenceWritesPerPlayer,
            int maxPersistenceWritesGlobal)
            : this(
                maxInboundCommandsPerSession,
                maxInboundCommandAgeTicks,
                maxInboundCommandLeadTicks,
                maxOutboundSnapshotsPerSession,
                maxQueuedBytesPerSession,
                maxPersistenceWritesPerPlayer,
                maxPersistenceWritesGlobal,
                maxPersistenceWriteBytesPerPlayer: 1024 * 1024,
                maxPersistenceWriteBytesGlobal: 8 * 1024 * 1024,
                maxPersistenceCompletions: 128,
                maxPersistenceCompletionBytes: 512 * 1024,
                maxLifecycleOps: 256,
                maxLifecycleOpBytes: 64 * 1024,
                expectedMaxSessions: 128,
                expectedMaxCommandsPerSessionPerTick: 32,
                expectedMaxSnapshotsQueuedPerSession: 8,
                skipValidation: false)
        {
        }

        public RuntimeBackpressureConfig(
            int maxInboundCommandsPerSession,
            int maxInboundCommandAgeTicks,
            int maxInboundCommandLeadTicks,
            int maxOutboundSnapshotsPerSession,
            int maxQueuedBytesPerSession,
            int maxPersistenceWritesPerPlayer,
            int maxPersistenceWritesGlobal,
            int maxPersistenceWriteBytesPerPlayer,
            int maxPersistenceWriteBytesGlobal,
            int maxPersistenceCompletions,
            int maxPersistenceCompletionBytes,
            int maxLifecycleOps,
            int maxLifecycleOpBytes,
            int expectedMaxSessions,
            int expectedMaxCommandsPerSessionPerTick,
            int expectedMaxSnapshotsQueuedPerSession)
            : this(
                maxInboundCommandsPerSession,
                maxInboundCommandAgeTicks,
                maxInboundCommandLeadTicks,
                maxOutboundSnapshotsPerSession,
                maxQueuedBytesPerSession,
                maxPersistenceWritesPerPlayer,
                maxPersistenceWritesGlobal,
                maxPersistenceWriteBytesPerPlayer,
                maxPersistenceWriteBytesGlobal,
                maxPersistenceCompletions,
                maxPersistenceCompletionBytes,
                maxLifecycleOps,
                maxLifecycleOpBytes,
                expectedMaxSessions,
                expectedMaxCommandsPerSessionPerTick,
                expectedMaxSnapshotsQueuedPerSession,
                skipValidation: false)
        {
        }

        private RuntimeBackpressureConfig(
            int maxInboundCommandsPerSession,
            int maxInboundCommandAgeTicks,
            int maxInboundCommandLeadTicks,
            int maxOutboundSnapshotsPerSession,
            int maxQueuedBytesPerSession,
            int maxPersistenceWritesPerPlayer,
            int maxPersistenceWritesGlobal,
            int maxPersistenceWriteBytesPerPlayer,
            int maxPersistenceWriteBytesGlobal,
            int maxPersistenceCompletions,
            int maxPersistenceCompletionBytes,
            int maxLifecycleOps,
            int maxLifecycleOpBytes,
            int expectedMaxSessions,
            int expectedMaxCommandsPerSessionPerTick,
            int expectedMaxSnapshotsQueuedPerSession,
            bool skipValidation)
        {
            if (!skipValidation)
            {
                if (maxInboundCommandsPerSession <= 0) throw new ArgumentOutOfRangeException(nameof(maxInboundCommandsPerSession));
                if (maxInboundCommandAgeTicks < 0) throw new ArgumentOutOfRangeException(nameof(maxInboundCommandAgeTicks));
                if (maxInboundCommandLeadTicks < 0) throw new ArgumentOutOfRangeException(nameof(maxInboundCommandLeadTicks));
                if (maxOutboundSnapshotsPerSession <= 0) throw new ArgumentOutOfRangeException(nameof(maxOutboundSnapshotsPerSession));
                if (maxQueuedBytesPerSession <= 0) throw new ArgumentOutOfRangeException(nameof(maxQueuedBytesPerSession));
                if (maxPersistenceWritesPerPlayer <= 0) throw new ArgumentOutOfRangeException(nameof(maxPersistenceWritesPerPlayer));
                if (maxPersistenceWritesGlobal <= 0) throw new ArgumentOutOfRangeException(nameof(maxPersistenceWritesGlobal));
                if (maxPersistenceWriteBytesPerPlayer <= 0) throw new ArgumentOutOfRangeException(nameof(maxPersistenceWriteBytesPerPlayer));
                if (maxPersistenceWriteBytesGlobal <= 0) throw new ArgumentOutOfRangeException(nameof(maxPersistenceWriteBytesGlobal));
                if (maxPersistenceCompletions <= 0) throw new ArgumentOutOfRangeException(nameof(maxPersistenceCompletions));
                if (maxPersistenceCompletionBytes <= 0) throw new ArgumentOutOfRangeException(nameof(maxPersistenceCompletionBytes));
                if (maxLifecycleOps <= 0) throw new ArgumentOutOfRangeException(nameof(maxLifecycleOps));
                if (maxLifecycleOpBytes <= 0) throw new ArgumentOutOfRangeException(nameof(maxLifecycleOpBytes));
                if (expectedMaxSessions <= 0) throw new ArgumentOutOfRangeException(nameof(expectedMaxSessions));
                if (expectedMaxCommandsPerSessionPerTick <= 0) throw new ArgumentOutOfRangeException(nameof(expectedMaxCommandsPerSessionPerTick));
                if (expectedMaxSnapshotsQueuedPerSession <= 0) throw new ArgumentOutOfRangeException(nameof(expectedMaxSnapshotsQueuedPerSession));
            }

            MaxInboundCommandsPerSession = maxInboundCommandsPerSession;
            MaxInboundCommandAgeTicks = maxInboundCommandAgeTicks;
            MaxInboundCommandLeadTicks = maxInboundCommandLeadTicks;
            MaxOutboundSnapshotsPerSession = maxOutboundSnapshotsPerSession;
            MaxQueuedBytesPerSession = maxQueuedBytesPerSession;
            MaxPersistenceWritesPerPlayer = maxPersistenceWritesPerPlayer;
            MaxPersistenceWritesGlobal = maxPersistenceWritesGlobal;
            MaxPersistenceWriteBytesPerPlayer = maxPersistenceWriteBytesPerPlayer;
            MaxPersistenceWriteBytesGlobal = maxPersistenceWriteBytesGlobal;
            MaxPersistenceCompletions = maxPersistenceCompletions;
            MaxPersistenceCompletionBytes = maxPersistenceCompletionBytes;
            MaxLifecycleOps = maxLifecycleOps;
            MaxLifecycleOpBytes = maxLifecycleOpBytes;
            ExpectedMaxSessions = expectedMaxSessions;
            ExpectedMaxCommandsPerSessionPerTick = expectedMaxCommandsPerSessionPerTick;
            ExpectedMaxSnapshotsQueuedPerSession = expectedMaxSnapshotsQueuedPerSession;
        }

        public int MaxInboundCommandsPerSession { get; }
        public int MaxInboundCommandAgeTicks { get; }
        public int MaxInboundCommandLeadTicks { get; }
        public int MaxOutboundSnapshotsPerSession { get; }
        public int MaxQueuedBytesPerSession { get; }
        public int MaxPersistenceWritesPerPlayer { get; }
        public int MaxPersistenceWritesGlobal { get; }
        public int MaxPersistenceWriteBytesPerPlayer { get; }
        public int MaxPersistenceWriteBytesGlobal { get; }
        public int MaxPersistenceCompletions { get; }
        public int MaxPersistenceCompletionBytes { get; }
        public int MaxLifecycleOps { get; }
        public int MaxLifecycleOpBytes { get; }
        public int ExpectedMaxSessions { get; }
        public int ExpectedMaxCommandsPerSessionPerTick { get; }
        public int ExpectedMaxSnapshotsQueuedPerSession { get; }
    }
}
