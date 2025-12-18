using System.Threading;

namespace Caelmor.Runtime.Replication
{
    /// <summary>
    /// Thread-safe, allocation-free counters for the replication snapshot pipeline.
    /// Shared across capture, serialization, queuing, and transport send pumps.
    /// </summary>
    public sealed class ReplicationSnapshotCounters
    {
        private long _snapshotsBuilt;
        private long _snapshotsSerialized;
        private long _snapshotsEnqueued;
        private long _snapshotsDequeuedForSend;
        private long _snapshotsDropped;

        public void RecordSnapshotBuilt() => Interlocked.Increment(ref _snapshotsBuilt);
        public void RecordSnapshotSerialized() => Interlocked.Increment(ref _snapshotsSerialized);
        public void RecordSnapshotEnqueued() => Interlocked.Increment(ref _snapshotsEnqueued);
        public void RecordSnapshotDequeuedForSend() => Interlocked.Increment(ref _snapshotsDequeuedForSend);
        public void RecordSnapshotDropped() => Interlocked.Increment(ref _snapshotsDropped);

        public ReplicationSnapshotCounterSnapshot Snapshot()
        {
            return new ReplicationSnapshotCounterSnapshot(
                Interlocked.Read(ref _snapshotsBuilt),
                Interlocked.Read(ref _snapshotsSerialized),
                Interlocked.Read(ref _snapshotsEnqueued),
                Interlocked.Read(ref _snapshotsDequeuedForSend),
                Interlocked.Read(ref _snapshotsDropped));
        }
    }

    public readonly struct ReplicationSnapshotCounterSnapshot
    {
        public ReplicationSnapshotCounterSnapshot(
            long snapshotsBuilt,
            long snapshotsSerialized,
            long snapshotsEnqueued,
            long snapshotsDequeuedForSend,
            long snapshotsDropped)
        {
            SnapshotsBuilt = snapshotsBuilt;
            SnapshotsSerialized = snapshotsSerialized;
            SnapshotsEnqueued = snapshotsEnqueued;
            SnapshotsDequeuedForSend = snapshotsDequeuedForSend;
            SnapshotsDropped = snapshotsDropped;
        }

        public long SnapshotsBuilt { get; }
        public long SnapshotsSerialized { get; }
        public long SnapshotsEnqueued { get; }
        public long SnapshotsDequeuedForSend { get; }
        public long SnapshotsDropped { get; }

        public static ReplicationSnapshotCounterSnapshot Empty => new ReplicationSnapshotCounterSnapshot(0, 0, 0, 0, 0);
    }
}
