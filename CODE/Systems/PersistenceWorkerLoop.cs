using System;
using System.Collections.Generic;
using System.Threading;
using Caelmor.Runtime.Transport;

namespace Caelmor.Runtime.Persistence
{
    /// <summary>
    /// Executes persistence writes off-thread and posts completions back through the bounded completion queue.
    /// Deterministic ordering is preserved by draining the write queue FIFO with a bounded batch size.
    /// </summary>
    public sealed class PersistenceWorkerLoop : IDisposable
    {
        private readonly PersistenceWriteQueue _writeQueue;
        private readonly PersistenceCompletionQueue _completionQueue;
        private readonly IPersistenceWriter _writer;
        private readonly PersistencePipelineCounters? _counters;
        private readonly int _maxPerIteration;
        private readonly int _idleDelayMs;
        private readonly object _gate = new object();

        private Thread? _thread;
        private CancellationTokenSource? _cts;
        private bool _running;

        public PersistenceWorkerLoop(
            PersistenceWriteQueue writeQueue,
            PersistenceCompletionQueue completionQueue,
            IPersistenceWriter writer,
            PersistencePipelineCounters counters = null,
            int maxPerIteration = 0,
            int idleDelayMs = 1)
        {
            _writeQueue = writeQueue ?? throw new ArgumentNullException(nameof(writeQueue));
            _completionQueue = completionQueue ?? throw new ArgumentNullException(nameof(completionQueue));
            _writer = writer ?? throw new ArgumentNullException(nameof(writer));
            _counters = counters;
            _idleDelayMs = idleDelayMs < 0 ? 0 : idleDelayMs;
            _maxPerIteration = maxPerIteration > 0 ? maxPerIteration : 8;
        }

        public void Start()
        {
            lock (_gate)
            {
                if (_running)
                    return;

                _cts = new CancellationTokenSource();
                _thread = new Thread(() => Run(_cts.Token))
                {
                    IsBackground = true,
                    Name = "Caelmor.PersistenceWorker"
                };
                _running = true;
                _thread.Start();
            }
        }

        public void Stop()
        {
            CancellationTokenSource? cts;
            Thread? thread;

            lock (_gate)
            {
                if (!_running)
                    return;

                _running = false;
                cts = _cts;
                thread = _thread;
                _cts = null;
                _thread = null;
            }

            try { cts?.Cancel(); } catch { /* no-op */ }

            if (thread != null && Thread.CurrentThread != thread)
            {
                try { thread.Join(); } catch { /* no-op */ }
            }
        }

        public int PumpOnce(int maxRequests = 0)
        {
            var limit = maxRequests > 0 ? maxRequests : _maxPerIteration;
            if (limit <= 0)
                return 0;

            int processed = 0;

            while (processed < limit && _writeQueue.TryDequeue(out var record))
            {
                var result = ExecuteWrite(record);
                var completion = new PersistenceCompletion(
                    record.Request,
                    result.Status,
                    result.Payload,
                    result.FailureReason);

                if (!_completionQueue.TryEnqueue(completion))
                {
                    processed++;
                    continue;
                }

                processed++;
            }

            return processed;
        }

        public void Dispose()
        {
            Stop();
        }

        private PersistenceWriteResult ExecuteWrite(in PersistenceWriteRecord record)
        {
            PersistenceWriteResult result;
            try
            {
                result = _writer.Execute(record, _cts?.Token ?? CancellationToken.None);
            }
            catch
            {
                result = PersistenceWriteResult.Failed(PersistenceFailureReason.Unknown);
            }

            bool ok = result.Status == PersistenceCompletionStatus.Succeeded;
            _counters?.RecordWriteResult(ok);
            return result;
        }

        private void Run(CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {
                PumpOnce(_maxPerIteration);

                if (_idleDelayMs > 0)
                    Thread.Sleep(_idleDelayMs);
                else
                    Thread.Yield();
            }
        }
    }

    /// <summary>
    /// Tick-thread applier that tracks last-known persistence outcomes for deterministic queries.
    /// </summary>
    public sealed class PersistenceCompletionApplier : IPersistenceCompletionApplier
    {
        private readonly PersistenceApplyState _state;
        private readonly PersistencePipelineCounters? _counters;

        public PersistenceCompletionApplier(PersistenceApplyState state, PersistencePipelineCounters counters = null)
        {
            _state = state ?? throw new ArgumentNullException(nameof(state));
            _counters = counters;
        }

        public void Apply(in PersistenceCompletion completion, long tickIndex)
        {
            _state.Record(completion.Request.SaveId, completion, tickIndex);
            _counters?.RecordCompletionApplied();
        }
    }

    /// <summary>
    /// In-memory state tracker for persistence completion results. Allocation-free per apply after warmup.
    /// </summary>
    public sealed class PersistenceApplyState
    {
        private readonly Dictionary<SaveId, PersistenceApplyRecord> _records;

        public PersistenceApplyState(int initialCapacity = 16)
        {
            _records = new Dictionary<SaveId, PersistenceApplyRecord>(initialCapacity);
        }

        public void Record(SaveId saveId, in PersistenceCompletion completion, long tickIndex)
        {
            _records[saveId] = new PersistenceApplyRecord(completion.Request, completion.Status, completion.FailureReason, tickIndex);
        }

        public bool TryGetLatest(SaveId saveId, out PersistenceApplyRecord record)
        {
            return _records.TryGetValue(saveId, out record);
        }
    }

    public readonly struct PersistenceApplyRecord
    {
        public PersistenceApplyRecord(PersistenceWriteRequest request, PersistenceCompletionStatus status, PersistenceFailureReason failureReason, long appliedTick)
        {
            Request = request;
            Status = status;
            FailureReason = failureReason;
            AppliedTick = appliedTick;
        }

        public PersistenceWriteRequest Request { get; }
        public PersistenceCompletionStatus Status { get; }
        public PersistenceFailureReason FailureReason { get; }
        public long AppliedTick { get; }
    }

    /// <summary>
    /// Persistence write executor contract. Implementations must avoid blocking the tick thread and run off-thread only.
    /// </summary>
    public interface IPersistenceWriter
    {
        PersistenceWriteResult Execute(in PersistenceWriteRecord record, CancellationToken token);
    }

    public readonly struct PersistenceWriteResult
    {
        public PersistenceWriteResult(PersistenceCompletionStatus status, PersistenceFailureReason failureReason, PooledPayloadLease payload)
        {
            Status = status;
            FailureReason = failureReason;
            Payload = payload;
        }

        public PersistenceCompletionStatus Status { get; }
        public PersistenceFailureReason FailureReason { get; }
        public PooledPayloadLease Payload { get; }

        public static PersistenceWriteResult Succeeded(PooledPayloadLease payload = null)
            => new PersistenceWriteResult(PersistenceCompletionStatus.Succeeded, PersistenceFailureReason.None, payload);

        public static PersistenceWriteResult Failed(PersistenceFailureReason reason)
            => new PersistenceWriteResult(PersistenceCompletionStatus.Failed, reason, null);
    }

    /// <summary>
    /// Thread-safe counter accumulator for persistence pipeline proof-of-life metrics.
    /// </summary>
    public sealed class PersistencePipelineCounters
    {
        private long _requestsEnqueued;
        private long _requestsDrained;
        private long _writesSucceeded;
        private long _writesFailed;
        private long _completionsApplied;
        private long _drops;
        private long _writeBacklogPeakCount;
        private long _writeBacklogPeakBytes;
        private long _completionBacklogPeakCount;
        private long _completionBacklogPeakBytes;

        public void RecordRequestEnqueued(int globalCount, int globalBytes)
        {
            Interlocked.Increment(ref _requestsEnqueued);
            RecordWriteBacklog(globalCount, globalBytes);
        }

        public void RecordRequestDrained(int globalCount, int globalBytes)
        {
            Interlocked.Increment(ref _requestsDrained);
            RecordWriteBacklog(globalCount, globalBytes);
        }

        public void RecordWriteResult(bool succeeded)
        {
            if (succeeded)
                Interlocked.Increment(ref _writesSucceeded);
            else
                Interlocked.Increment(ref _writesFailed);
        }

        public void RecordCompletionApplied()
        {
            Interlocked.Increment(ref _completionsApplied);
        }

        public void RecordDrop()
        {
            Interlocked.Increment(ref _drops);
        }

        public void RecordWriteBacklog(int count, int bytes)
        {
            UpdateMax(ref _writeBacklogPeakCount, count);
            UpdateMax(ref _writeBacklogPeakBytes, bytes);
        }

        public void RecordCompletionBacklog(int count, int bytes)
        {
            UpdateMax(ref _completionBacklogPeakCount, count);
            UpdateMax(ref _completionBacklogPeakBytes, bytes);
        }

        public PersistencePipelineCounterSnapshot Snapshot()
        {
            return new PersistencePipelineCounterSnapshot(
                Interlocked.Read(ref _requestsEnqueued),
                Interlocked.Read(ref _requestsDrained),
                Interlocked.Read(ref _writesSucceeded),
                Interlocked.Read(ref _writesFailed),
                Interlocked.Read(ref _completionsApplied),
                Interlocked.Read(ref _drops),
                Interlocked.Read(ref _writeBacklogPeakCount),
                Interlocked.Read(ref _writeBacklogPeakBytes),
                Interlocked.Read(ref _completionBacklogPeakCount),
                Interlocked.Read(ref _completionBacklogPeakBytes));
        }

        private static void UpdateMax(ref long target, long candidate)
        {
            long current = Interlocked.Read(ref target);
            while (candidate > current)
            {
                long prev = Interlocked.CompareExchange(ref target, candidate, current);
                if (prev == current)
                    break;
                current = prev;
            }
        }
    }

    public readonly struct PersistencePipelineCounterSnapshot
    {
        public PersistencePipelineCounterSnapshot(
            long requestsEnqueued,
            long requestsDrained,
            long writesSucceeded,
            long writesFailed,
            long completionsApplied,
            long drops,
            long writeBacklogPeakCount,
            long writeBacklogPeakBytes,
            long completionBacklogPeakCount,
            long completionBacklogPeakBytes)
        {
            RequestsEnqueued = requestsEnqueued;
            RequestsDrained = requestsDrained;
            WritesSucceeded = writesSucceeded;
            WritesFailed = writesFailed;
            CompletionsApplied = completionsApplied;
            Drops = drops;
            WriteBacklogPeakCount = writeBacklogPeakCount;
            WriteBacklogPeakBytes = writeBacklogPeakBytes;
            CompletionBacklogPeakCount = completionBacklogPeakCount;
            CompletionBacklogPeakBytes = completionBacklogPeakBytes;
        }

        public long RequestsEnqueued { get; }
        public long RequestsDrained { get; }
        public long WritesSucceeded { get; }
        public long WritesFailed { get; }
        public long CompletionsApplied { get; }
        public long Drops { get; }
        public long WriteBacklogPeakCount { get; }
        public long WriteBacklogPeakBytes { get; }
        public long CompletionBacklogPeakCount { get; }
        public long CompletionBacklogPeakBytes { get; }
    }

    /// <summary>
    /// Simple in-memory persistence writer used for validation harnesses.
    /// </summary>
    public sealed class InMemoryPersistenceWriter : IPersistenceWriter
    {
        private readonly Dictionary<SaveId, PersistenceWriteRequest> _writes = new Dictionary<SaveId, PersistenceWriteRequest>();

        public PersistenceWriteResult Execute(in PersistenceWriteRecord record, CancellationToken token)
        {
            lock (_writes)
            {
                _writes[record.Request.SaveId] = record.Request;
            }
            return PersistenceWriteResult.Succeeded();
        }

        public bool TryGetWrite(SaveId saveId, out PersistenceWriteRequest request)
        {
            lock (_writes)
            {
                return _writes.TryGetValue(saveId, out request);
            }
        }
    }
}
