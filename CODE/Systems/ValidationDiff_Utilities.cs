using System;
using System.Collections.Generic;
using System.Text;

namespace Caelmor.Systems
{
    /// <summary>
    /// Stage 9.3: Deterministic diff helpers.
    /// Produces minimal, human-readable diffs that identify the smallest failing unit.
    /// No noisy formatting; stable ordering; no randomness.
    /// </summary>
    public static class ValidationDiff
    {
        // ----------------------------
        // Inventory diff
        // ----------------------------

        public static bool TryDiff(
            ValidationSnapshot_Inventory expected,
            ValidationSnapshot_Inventory actual,
            out string diff)
        {
            if (expected == null) throw new ArgumentNullException(nameof(expected));
            if (actual == null) throw new ArgumentNullException(nameof(actual));

            var sb = new StringBuilder(256);
            bool ok = true;

            if (expected.PlayerId != actual.PlayerId)
            {
                ok = false;
                sb.AppendLine($"player_id_mismatch expected={expected.PlayerId} actual={actual.PlayerId}");
            }

            // Both arrays are sorted by key. Merge-walk for determinism and minimal output.
            int i = 0, j = 0;
            while (i < expected.Entries.Length || j < actual.Entries.Length)
            {
                if (i >= expected.Entries.Length)
                {
                    // extra actual
                    ok = false;
                    sb.AppendLine($"extra_item key={actual.Entries[j].ResourceItemKey} count={actual.Entries[j].Count}");
                    j++;
                    continue;
                }

                if (j >= actual.Entries.Length)
                {
                    // missing actual
                    ok = false;
                    sb.AppendLine($"missing_item key={expected.Entries[i].ResourceItemKey} expected_count={expected.Entries[i].Count}");
                    i++;
                    continue;
                }

                var e = expected.Entries[i];
                var a = actual.Entries[j];

                int cmp = string.Compare(e.ResourceItemKey, a.ResourceItemKey, StringComparison.Ordinal);
                if (cmp == 0)
                {
                    if (e.Count != a.Count)
                    {
                        ok = false;
                        sb.AppendLine($"count_mismatch key={e.ResourceItemKey} expected={e.Count} actual={a.Count}");
                    }
                    i++;
                    j++;
                }
                else if (cmp < 0)
                {
                    ok = false;
                    sb.AppendLine($"missing_item key={e.ResourceItemKey} expected_count={e.Count}");
                    i++;
                }
                else
                {
                    ok = false;
                    sb.AppendLine($"extra_item key={a.ResourceItemKey} count={a.Count}");
                    j++;
                }
            }

            diff = ok ? string.Empty : sb.ToString().TrimEnd();
            return ok;
        }

        // ----------------------------
        // Nodes diff
        // ----------------------------

        public static bool TryDiff(
            ValidationSnapshot_Nodes expected,
            ValidationSnapshot_Nodes actual,
            out string diff)
        {
            if (expected == null) throw new ArgumentNullException(nameof(expected));
            if (actual == null) throw new ArgumentNullException(nameof(actual));

            var sb = new StringBuilder(256);
            bool ok = true;

            // Both arrays are sorted by NodeInstanceId. Merge-walk.
            int i = 0, j = 0;
            while (i < expected.Entries.Length || j < actual.Entries.Length)
            {
                if (i >= expected.Entries.Length)
                {
                    ok = false;
                    var a = actual.Entries[j++];
                    sb.AppendLine($"extra_node id={a.NodeInstanceId} exists={a.Exists} state={a.Availability} ticks={a.RespawnTicksRemaining}");
                    continue;
                }

                if (j >= actual.Entries.Length)
                {
                    ok = false;
                    var e = expected.Entries[i++];
                    sb.AppendLine($"missing_node id={e.NodeInstanceId} expected_state={e.Availability} expected_ticks={e.RespawnTicksRemaining}");
                    continue;
                }

                var ex = expected.Entries[i];
                var ac = actual.Entries[j];

                if (ex.NodeInstanceId == ac.NodeInstanceId)
                {
                    if (ex.Exists != ac.Exists)
                    {
                        ok = false;
                        sb.AppendLine($"exists_mismatch id={ex.NodeInstanceId} expected={ex.Exists} actual={ac.Exists}");
                    }

                    if (ex.Availability != ac.Availability)
                    {
                        ok = false;
                        sb.AppendLine($"state_mismatch id={ex.NodeInstanceId} expected={ex.Availability} actual={ac.Availability}");
                    }

                    // Only compare ticks when BOTH are known.
                    if (ex.RespawnTicksRemaining.HasValue && ac.RespawnTicksRemaining.HasValue)
                    {
                        if (ex.RespawnTicksRemaining.Value != ac.RespawnTicksRemaining.Value)
                        {
                            ok = false;
                            sb.AppendLine($"ticks_mismatch id={ex.NodeInstanceId} expected={ex.RespawnTicksRemaining.Value} actual={ac.RespawnTicksRemaining.Value}");
                        }
                    }

                    i++;
                    j++;
                }
                else if (ex.NodeInstanceId < ac.NodeInstanceId)
                {
                    ok = false;
                    sb.AppendLine($"missing_node id={ex.NodeInstanceId} expected_state={ex.Availability} expected_ticks={ex.RespawnTicksRemaining}");
                    i++;
                }
                else
                {
                    ok = false;
                    sb.AppendLine($"extra_node id={ac.NodeInstanceId} exists={ac.Exists} state={ac.Availability} ticks={ac.RespawnTicksRemaining}");
                    j++;
                }
            }

            diff = ok ? string.Empty : sb.ToString().TrimEnd();
            return ok;
        }
    }
}
