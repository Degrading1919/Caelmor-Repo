// File: Persistence/InventoryPersistenceAdapter.cs
// Stage 8.7 — inventory <-> PlayerSave wiring

using System;
using System.Collections.Generic;
using Caelmor.Economy.Inventory;

namespace Caelmor.Persistence
{
    /// <summary>
    /// Bridge between authoritative runtime inventory store and PlayerSave DTOs.
    /// Restore MUST NOT emit gameplay events; this adapter only hydrates state.
    /// </summary>
    public interface IInventoryPersistenceAdapter
    {
        PersistedPlayerSave BuildPlayerSaveSnapshot(int playerId);
        void ApplyPlayerSaveSnapshot(PersistedPlayerSave save);
    }

    public sealed class SimpleInventoryPersistenceAdapter : IInventoryPersistenceAdapter
    {
        private readonly SimplePlayerInventoryStore _inventory; // Stage 8.5 minimal store

        public SimpleInventoryPersistenceAdapter(SimplePlayerInventoryStore inventory)
        {
            _inventory = inventory ?? throw new ArgumentNullException(nameof(inventory));
        }

        public PersistedPlayerSave BuildPlayerSaveSnapshot(int playerId)
        {
            // NOTE: SimplePlayerInventoryStore currently holds internal state; add a controlled snapshot API.
            // To avoid changing gameplay behavior, this is pure read.
            var save = new PersistedPlayerSave { PlayerId = playerId };

            foreach (var entry in _inventory.Enumerate(playerId))
            {
                // entry.Key, entry.Value are authoritative counts
                save.Inventory.Add(new PersistedInventoryEntry(entry.Key, entry.Value));
            }

            return save;
        }

        public void ApplyPlayerSaveSnapshot(PersistedPlayerSave save)
        {
            if (save == null) throw new ArgumentNullException(nameof(save));

            // Hydration only:
            // - clear and set exact counts
            // - do not emit grant/craft events
            _inventory.SetExactSnapshot(save.PlayerId, save.Inventory);
        }
    }

    // Minimal controlled snapshot API added to SimplePlayerInventoryStore via extension methods or partial class.
    // This is persistence plumbing, not gameplay behavior.
    public static class SimplePlayerInventoryStoreSnapshotExtensions
    {
        public static IEnumerable<KeyValuePair<string, int>> Enumerate(this SimplePlayerInventoryStore store, int playerId)
            => store.DebugEnumerate(playerId);

        public static void SetExactSnapshot(this SimplePlayerInventoryStore store, int playerId, List<PersistedInventoryEntry> entries)
            => store.DebugSetExact(playerId, entries);
    }
}
