using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;

namespace Caelmor.Runtime.Diagnostics
{
    /// <summary>
    /// DEBUG-only guardrails to fail fast on hot-path drift.
    /// Designed to be allocation-free and safe for tick-thread usage.
    /// </summary>
    internal static class RuntimeGuardrailChecks
    {
#if DEBUG
        private const string StringEntityIdMessage = "COMBAT_STRING_ENTITY_ID_FORBIDDEN";
        private const string DictionaryPayloadMessage = "COMBAT_DICTIONARY_PAYLOAD_FORBIDDEN";
        private const string ClientTickOrderingMessage = "CLIENT_TICK_USED_FOR_ORDERING";

        private static long _hotPathAllocationSuspicion;

        public static long HotPathAllocationSuspicion => Interlocked.Read(ref _hotPathAllocationSuspicion);

        [Conditional("DEBUG")]
        public static void AssertTickThreadEntry()
        {
            TickThreadAssert.AssertTickThread();
        }

        [Conditional("DEBUG")]
        public static void MarkHotPathAllocationSuspicion()
        {
            Interlocked.Increment(ref _hotPathAllocationSuspicion);
        }

        [Conditional("DEBUG")]
        public static void AssertNoStringEntityId(string? entityId)
        {
            if (!string.IsNullOrEmpty(entityId))
                Debug.Assert(false, StringEntityIdMessage);
        }

        [Conditional("DEBUG")]
        public static void AssertNoDictionaryPayload<T>(in T payload)
        {
            if (typeof(T) == typeof(Dictionary<string, object?>))
                Debug.Assert(false, DictionaryPayloadMessage);
        }

        [Conditional("DEBUG")]
        public static void AssertNoClientTickOrdering(long clientSubmitTick)
        {
            if (clientSubmitTick != 0)
                Debug.Assert(false, ClientTickOrderingMessage);
        }
#else
        public static long HotPathAllocationSuspicion => 0;
        public static void AssertTickThreadEntry() { }
        public static void MarkHotPathAllocationSuspicion() { }
        public static void AssertNoStringEntityId(string? entityId) { }
        public static void AssertNoDictionaryPayload<T>(in T payload) { }
        public static void AssertNoClientTickOrdering(long clientSubmitTick) { }
#endif
    }
}
