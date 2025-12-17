using System;
using System.Threading;

namespace Caelmor.Runtime.Diagnostics
{
    /// <summary>
    /// Lightweight tick diagnostics used by the runtime loop.
    /// Tracks min/max/avg tick durations plus overrun counters.
    /// Allocation-free: all state is stored in primitive fields.
    /// </summary>
    public sealed class TickDiagnostics
    {
        private long _tickCount;
        private long _totalTicksNanoseconds;
        private int _minNanoseconds = int.MaxValue;
        private int _maxNanoseconds;
        private long _overrunCount;
        private long _catchUpClampedCount;
        private long _timeSliceDeferrals;

        public void RecordTick(TimeSpan duration, bool overrun, bool catchUpClamped)
        {
            var nanos = (int)(duration.Ticks * 100); // 1 tick = 100ns
            Interlocked.Increment(ref _tickCount);
            Interlocked.Add(ref _totalTicksNanoseconds, nanos);

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

        public TickDiagnosticsSnapshot Snapshot()
        {
            var ticks = Interlocked.Read(ref _tickCount);
            var totalNano = Interlocked.Read(ref _totalTicksNanoseconds);
            var avgNano = ticks == 0 ? 0 : totalNano / ticks;

            return new TickDiagnosticsSnapshot(
                ticks,
                _minNanoseconds == int.MaxValue ? 0 : _minNanoseconds,
                _maxNanoseconds,
                avgNano,
                Interlocked.Read(ref _overrunCount),
                Interlocked.Read(ref _catchUpClampedCount),
                Interlocked.Read(ref _timeSliceDeferrals));
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

        public TickDiagnosticsSnapshot(
            long tickCount,
            long minNanoseconds,
            long maxNanoseconds,
            long avgNanoseconds,
            long overruns,
            long catchUpClamped,
            long timeSliceDeferrals)
        {
            TickCount = tickCount;
            MinNanoseconds = minNanoseconds;
            MaxNanoseconds = maxNanoseconds;
            AvgNanoseconds = avgNanoseconds;
            Overruns = overruns;
            CatchUpClamped = catchUpClamped;
            TimeSliceDeferrals = timeSliceDeferrals;
        }
    }
}
