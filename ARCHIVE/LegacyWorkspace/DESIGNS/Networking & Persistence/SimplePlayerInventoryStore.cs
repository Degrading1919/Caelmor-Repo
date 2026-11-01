// File: Economy/Inventory/SimplePlayerInventoryStore.cs
// Minimal implementation to unblock Stage 8.5 tests.
// No persistence I/O. No capacity rules.

using System;
using System.Collections.Generic;

namespace Caelmor.Economy.Inventory
{
    public sealed class SimplePlayerInventoryStore : IPlayerInventoryStore
    {
        private readonly Dictionary<int, Dictionary<string, int>> _byPlayer =
            new Dictionary<int, Dictionary<string, int>>(128);

        private readonly HashSet<int> _writable = new HashSet<int>();

        public void MarkWritable(int playerId)
        {
            _writable.Add(playerId);
            if (!_byPlayer.ContainsKey(playerId))
                _byPlayer[playerId] = new Dictionary<string, int>(64);
        }

        public void MarkNotWritable(int playerId)
        {
            _writable.Remove(playerId);
        }

        public bool IsInventoryWritable(int playerId) => _writable.Contains(playerId);

        public bool TryApplyDeltasAtomic(
            int playerId,
            IReadOnlyList<(string key, int delta)> deltas,
            out string? failureReason)
        {
            failureReason = null;

            if (!IsInventoryWritable(playerId))
            {
                failureReason = "inventory_not_writable";
                return false;
            }

            if (!_byPlayer.TryGetValue(playerId, out var inv))
            {
                failureReason = "inventory_missing";
                return false;
            }

            // Pre-validate (no mutation) to preserve atomicity.
            for (int i = 0; i < deltas.Count; i++)
            {
                var (key, delta) = deltas[i];
                if (string.IsNullOrWhiteSpace(key))
                {
                    failureReason = "invalid_item_key";
                    return false;
                }

                if (delta == 0)
                {
                    failureReason = "invalid_delta_zero";
                    return false;
                }

                inv.TryGetValue(key, out int current);
                long next = (long)current + delta;
                if (next < 0)
                {
                    failureReason = "insufficient_items";
                    return false;
                }
                if (next > int.MaxValue)
                {
                    failureReason = "count_overflow";
                    return false;
                }
            }

            // Apply after validation.
            for (int i = 0; i < deltas.Count; i++)
            {
                var (key, delta) = deltas[i];
                inv.TryGetValue(key, out int current);
                int next = current + delta;

                if (next == 0)
                    inv.Remove(key);
                else
                    inv[key] = next;
            }

            return true;
        }
    }
}
