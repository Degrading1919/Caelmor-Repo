using System;
using System.Diagnostics;
using System.Threading;

namespace Caelmor.Runtime.Diagnostics
{
    /// <summary>
    /// Lightweight tick diagnostics used by the runtime loop.
    /// Tracks min/max/avg tick durations, overrun counters, and stall watchdog events.
    /// Allocation-free steady state: all state is stored in primitive fields or pooled primitives.
    /// </summary>
    public sealed class TickDiagnostics : IDisposable
    {
        private long _tickCount;
        private long _totalTicksNanoseconds;
        private int _minNanoseconds = int.MaxValue;
        private int _maxNanoseconds;
        private long _overrunCount;
        private long _catchUpClampedCount;
        private long _timeSliceDeferrals;
        private TickStallWatchdog _stallWatchdog;

#if DEBUG
        private long _participantSnapshotResizes;
        private long _maxParticipantsObserved;
#endif

        public void RecordTick(TimeSpan duration, bool overrun, bool catchUpClamped)
        {
            var nanos = (int)(duration.Ticks * 100); // 1 tick = 100ns
            Interlocked.Increment(ref _tickCount);
            Interlocked.Add(ref _totalTicksNanoseconds, nanos);
            _stallWatchdog?.NotifyProgress(Stopwatch.GetTimestamp());

            int currentMin = _minNanoseconds;
            while (nanos < currentMin)
            {
                var observed = Interlocked.CompareExchange(ref _minNanoseconds, nanos, currentMin);
                if (observed == currentMin)
                    break;
                currentMin = observed;
            }

            int currentMax = _maxNanoseconds;
            while (nanos > currentMax)
            {
                var observed = Interlocked.CompareExchange(ref _maxNanoseconds, nanos, currentMax);
                if (observed == currentMax)
                    break;
                currentMax = observed;
            }

            if (overrun)
                Interlocked.Increment(ref _overrunCount);
            if (catchUpClamped)
                Interlocked.Increment(ref _catchUpClampedCount);
        }

        public void RecordTimeSliceDeferral() => Interlocked.Increment(ref _timeSliceDeferrals);

#if DEBUG
        public void RecordParticipantSnapshotResize(int newCapacity)
        {
            Interlocked.Increment(ref _participantSnapshotResizes);
        }

        public void RecordParticipantCountObserved(int count)
        {
            var observed = Interlocked.Read(ref _maxParticipantsObserved);
            while (count > observed)
            {
                var prior = Interlocked.CompareExchange(ref _maxParticipantsObserved, count, observed);
                if (prior == observed)
                    break;
                observed = prior;
            }
        }
#endif

        public TickDiagnosticsSnapshot Snapshot()
        {
            var ticks = Interlocked.Read(ref _tickCount);
            var totalNano = Interlocked.Read(ref _totalTicksNanoseconds);
            var avgNano = ticks == 0 ? 0 : totalNano / ticks;
            var stallCount = _stallWatchdog?.StallCount ?? 0;
            var stallDurationTicks = _stallWatchdog?.LastStallStopwatchTicks ?? 0;
            var stallDurationNanoseconds = stallDurationTicks == 0
                ? 0
                : (long)((stallDurationTicks * 1_000_000_000L) / Stopwatch.Frequency);

#if DEBUG
            var participantSnapshotResizes = Interlocked.Read(ref _participantSnapshotResizes);
            var maxParticipantsObserved = Interlocked.Read(ref _maxParticipantsObserved);
#endif

            return new TickDiagnosticsSnapshot(
                ticks,
                _minNanoseconds == int.MaxValue ? 0 : _minNanoseconds,
                _maxNanoseconds,
                avgNano,
                Interlocked.Read(ref _overrunCount),
                Interlocked.Read(ref _catchUpClampedCount),
                Interlocked.Read(ref _timeSliceDeferrals),
                stallCount,
                stallDurationNanoseconds
#if DEBUG
                ,
                participantSnapshotResizes,
                maxParticipantsObserved
#endif
                );
        }

        public void ConfigureStallWatchdog(TimeSpan stallThreshold, Action<TickStallEvent> onStall)
        {
            if (stallThreshold <= TimeSpan.Zero)
                throw new ArgumentOutOfRangeException(nameof(stallThreshold));
            if (onStall == null)
                throw new ArgumentNullException(nameof(onStall));

            var watchdog = new TickStallWatchdog(stallThreshold, onStall);
            var existing = Interlocked.Exchange(ref _stallWatchdog, watchdog);
            existing?.Dispose();
        }

        public void Dispose()
        {
            _stallWatchdog?.Dispose();
            _stallWatchdog = null;
        }
    }

    public readonly struct TickDiagnosticsSnapshot
    {
        public readonly long TickCount;
        public readonly long MinNanoseconds;
        public readonly long MaxNanoseconds;
        public readonly long AvgNanoseconds;
        public readonly long Overruns;
        public readonly long CatchUpClamped;
        public readonly long TimeSliceDeferrals;
        public readonly long StallDetections;
        public readonly long LastStallNanoseconds;

#if DEBUG
        public readonly long ParticipantSnapshotResizes;
        public readonly long MaxParticipantsObserved;
#endif

        public TickDiagnosticsSnapshot(
            long tickCount,
            long minNanoseconds,
            long maxNanoseconds,
            long avgNanoseconds,
            long overruns,
            long catchUpClamped,
            long timeSliceDeferrals,
            long stallDetections,
            long lastStallNanoseconds
#if DEBUG
            ,
            long participantSnapshotResizes,
            long maxParticipantsObserved
#endif
            )
        {
            TickCount = tickCount;
            MinNanoseconds = minNanoseconds;
            MaxNanoseconds = maxNanoseconds;
            AvgNanoseconds = avgNanoseconds;
            Overruns = overruns;
            CatchUpClamped = catchUpClamped;
            TimeSliceDeferrals = timeSliceDeferrals;
            StallDetections = stallDetections;
            LastStallNanoseconds = lastStallNanoseconds;
#if DEBUG
            ParticipantSnapshotResizes = participantSnapshotResizes;
            MaxParticipantsObserved = maxParticipantsObserved;
#endif
        }
    }

    public readonly struct TickStallEvent
    {
        public TickStallEvent(TimeSpan durationSinceLastTick)
        {
            DurationSinceLastTick = durationSinceLastTick;
        }

        public TimeSpan DurationSinceLastTick { get; }
    }

    internal sealed class TickStallWatchdog : IDisposable
    {
        private static readonly TimerCallback TimerCallback = OnTimer;

        private readonly long _thresholdStopwatchTicks;
        private readonly Action<TickStallEvent> _onStall;
        private readonly Timer _timer;
        private long _lastTickTimestamp;
        private long _stallCount;
        private long _lastStallDuration;
        private int _signaled;

        public TickStallWatchdog(TimeSpan threshold, Action<TickStallEvent> onStall)
        {
            _thresholdStopwatchTicks = (long)(Stopwatch.Frequency * threshold.TotalSeconds);
            _onStall = onStall ?? throw new ArgumentNullException(nameof(onStall));
            _lastTickTimestamp = Stopwatch.GetTimestamp();
            _timer = new Timer(TimerCallback, this, threshold, threshold);
        }

        public long StallCount => Interlocked.Read(ref _stallCount);
        public long LastStallStopwatchTicks => Interlocked.Read(ref _lastStallDuration);

        public void NotifyProgress(long timestamp)
        {
            Volatile.Write(ref _lastTickTimestamp, timestamp);
            Volatile.Write(ref _signaled, 0);
        }

        public void Dispose()
        {
            _timer.Dispose();
        }

        private static void OnTimer(object state)
        {
            var self = (TickStallWatchdog)state;
            var last = Volatile.Read(ref self._lastTickTimestamp);
            var now = Stopwatch.GetTimestamp();
            var elapsed = now - last;
            if (elapsed <= self._thresholdStopwatchTicks)
                return;

            if (Interlocked.Exchange(ref self._signaled, 1) == 1)
                return;

            Interlocked.Increment(ref self._stallCount);
            Interlocked.Exchange(ref self._lastStallDuration, elapsed);
            self._onStall(new TickStallEvent(TimeSpan.FromSeconds((double)elapsed / Stopwatch.Frequency)));
        }
    }
}
