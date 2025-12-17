using System.Diagnostics;
using System.Threading;

namespace Caelmor.Runtime.Diagnostics
{
    /// <summary>
    /// DEBUG-only guard that asserts execution on the captured tick thread.
    /// Capturing and assertion are allocation-free to keep the tick loop GC-neutral.
    /// </summary>
    internal static class TickThreadAssert
    {
#if DEBUG
        private const string TickThreadOnlyMessage = "TICK_THREAD_ONLY";
        private static int _tickThreadId;

        public static void CaptureTickThread(Thread thread)
        {
            _tickThreadId = thread?.ManagedThreadId ?? 0;
        }

        public static void ClearTickThread()
        {
            _tickThreadId = 0;
        }

        [Conditional("DEBUG")]
        public static void AssertTickThread()
        {
            if (_tickThreadId == 0)
                return;

            Debug.Assert(Thread.CurrentThread.ManagedThreadId == _tickThreadId, TickThreadOnlyMessage);
        }
#else
        public static void CaptureTickThread(Thread thread) { }
        public static void ClearTickThread() { }
        public static void AssertTickThread() { }
#endif
    }
}
