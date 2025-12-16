// File: Economy/Inventory/SimplePlayerInventoryStore.Persistence.cs
// Stage 8.7 — adds controlled snapshot hooks for persistence wiring.
// No gameplay behavior changes; no events emitted.

using System;
using System.Collections.Generic;
using Caelmor.Persistence;

namespace Caelmor.Economy.Inventory
{
    public sealed partial class SimplePlayerInventoryStore
    {
        // Enumerate current authoritative state (read-only).
        internal IEnumerable<KeyValuePair<string, int>> DebugEnumerate(int playerId)
        {
            if (!_byPlayer.TryGetValue(playerId, out var inv))
                yield break;

            foreach (var kv in inv)
                yield return kv;
        }

        // Set exact snapshot (hydration only). Clears existing keys first.
        internal void DebugSetExact(int playerId, List<PersistedInventoryEntry> entries)
        {
            if (!_byPlayer.TryGetValue(playerId, out var inv))
                _byPlayer[playerId] = inv = new Dictionary<string, int>(64);

            inv.Clear();

            for (int i = 0; i < entries.Count; i++)
            {
                var e = entries[i];

                // Fail loudly on corrupt/invalid data (no auto-repair).
                if (string.IsNullOrWhiteSpace(e.ResourceItemKey))
                    throw new InvalidOperationException($"Corrupt PlayerSave: empty ResourceItemKey for PlayerId={playerId}.");
                if (e.Count <= 0)
                    throw new InvalidOperationException($"Corrupt PlayerSave: non-positive count for key='{e.ResourceItemKey}', PlayerId={playerId}.");

                inv[e.ResourceItemKey] = e.Count;
            }
        }
    }
}
