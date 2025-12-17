using System;
using System.Collections.Generic;
using Caelmor.Runtime.Diagnostics;

namespace Caelmor.Runtime.Threading
{
    /// <summary>
    /// Deterministic, allocation-free scheduler for time-sliced work executed on the tick thread.
    /// Work items are processed in FIFO order with a fixed slice cap per tick to avoid frame spikes.
    /// </summary>
    public sealed class TimeSlicedWorkScheduler
    {
        private readonly Queue<ITimeSlicedWorkItem> _queue = new Queue<ITimeSlicedWorkItem>();
        private readonly TickDiagnostics _diagnostics;

        public TimeSlicedWorkScheduler(TickDiagnostics diagnostics)
        {
            _diagnostics = diagnostics ?? throw new ArgumentNullException(nameof(diagnostics));
        }

        public int PendingCount => _queue.Count;

        public void Enqueue(ITimeSlicedWorkItem item)
        {
            if (item is null) throw new ArgumentNullException(nameof(item));
            _queue.Enqueue(item);
        }

        /// <summary>
        /// Executes a bounded number of slices within the provided time budget.
        /// If the budget is exceeded or slices remain, work is deferred to the next tick.
        /// </summary>
        public void ExecuteSlices(TimeSpan maxBudget, int maxSlices)
        {
            if (_queue.Count == 0 || maxSlices <= 0)
                return;

            var slicesExecuted = 0;
            long consumedTicks = 0;

            while (_queue.Count > 0 && slicesExecuted < maxSlices)
            {
                var item = _queue.Peek();
                var remainingBudget = maxBudget - new TimeSpan(consumedTicks);
                if (remainingBudget <= TimeSpan.Zero)
                {
                    _diagnostics.RecordTimeSliceDeferral();
                    return;
                }

                var completed = item.ExecuteSlice(remainingBudget, out var elapsed);
                slicesExecuted++;
                consumedTicks += elapsed.Ticks;

                if (completed)
                {
                    _queue.Dequeue();
                }
                else if (new TimeSpan(consumedTicks) >= maxBudget)
                {
                    _diagnostics.RecordTimeSliceDeferral();
                    return;
                }
            }
        }
    }

    public interface ITimeSlicedWorkItem
    {
        /// <summary>
        /// Executes a bounded slice of work.
        /// Implementations must avoid blocking I/O and respect the provided budget.
        /// Returns true when the work item has fully completed.
        /// </summary>
        bool ExecuteSlice(TimeSpan budget, out TimeSpan elapsed);
    }
}
