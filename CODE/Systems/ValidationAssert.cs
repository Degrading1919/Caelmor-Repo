using System;

namespace Caelmor.Systems
{
    /// <summary>
    /// Stage 9.3: Minimal assertion helper used by scenarios.
    /// If snapshots differ, we fail loudly with a human-readable diff.
    /// No correction, no retries, no repair.
    /// </summary>
    public static class ValidationAssert
    {
        public static void Equal(ValidationSnapshot_Inventory expected, ValidationSnapshot_Inventory actual, string label)
        {
            if (!ValidationDiff.TryDiff(expected, actual, out var diff))
                throw new InvalidOperationException($"VALIDATION_ASSERT_FAIL [{label}] inventory_diff:\n{diff}");
        }

        public static void Equal(ValidationSnapshot_Nodes expected, ValidationSnapshot_Nodes actual, string label)
        {
            if (!ValidationDiff.TryDiff(expected, actual, out var diff))
                throw new InvalidOperationException($"VALIDATION_ASSERT_FAIL [{label}] nodes_diff:\n{diff}");
        }
    }
}
