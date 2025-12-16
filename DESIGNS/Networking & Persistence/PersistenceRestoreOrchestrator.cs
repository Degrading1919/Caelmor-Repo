// File: Persistence/PersistenceRestoreOrchestrator.cs
// Stage 8.7 — deterministic restore wiring (hydration only, no events).

using System;
using System.Collections.Generic;
using Caelmor.Economy.ResourceNodes;

namespace Caelmor.Persistence
{
    public sealed class PersistenceRestoreOrchestrator
    {
        private readonly string _worldId;
        private readonly IPlayerSaveStorage _playerStorage;
        private readonly IWorldSaveStorage _worldStorage;
        private readonly IInventoryPersistenceAdapter _inventoryAdapter;
        private readonly IWorldNodePersistenceAdapter _nodeAdapter;

        public PersistenceRestoreOrchestrator(
            string worldId,
            IPlayerSaveStorage playerStorage,
            IWorldSaveStorage worldStorage,
            IInventoryPersistenceAdapter inventoryAdapter,
            IWorldNodePersistenceAdapter nodeAdapter)
        {
            _worldId = worldId ?? throw new ArgumentNullException(nameof(worldId));
            _playerStorage = playerStorage ?? throw new ArgumentNullException(nameof(playerStorage));
            _worldStorage = worldStorage ?? throw new ArgumentNullException(nameof(worldStorage));
            _inventoryAdapter = inventoryAdapter ?? throw new ArgumentNullException(nameof(inventoryAdapter));
            _nodeAdapter = nodeAdapter ?? throw new ArgumentNullException(nameof(nodeAdapter));
        }

        // Server startup: load world save once; zones will apply relevant overrides on load.
        public PersistedWorldSave LoadWorldSaveForStartup()
        {
            // May throw on corruption/missing. Fail loudly per Stage 7.5. :contentReference[oaicite:5]{index=5}
            return _worldStorage.LoadWorld(_worldId);
        }

        // Zone load: placements come from content; overrides are applied by stable NodeInstanceId.
        public IReadOnlyList<PersistedNodeOverride> BuildZoneNodeOverrides(PersistedWorldSave worldSave)
        {
            return _nodeAdapter.ConvertToRuntimeOverrides(worldSave);
        }

        // Player reconnect: hydrate inventory exactly; no events.
        public void RestorePlayerInventory(int playerId)
        {
            var save = _playerStorage.LoadPlayer(playerId);
            _inventoryAdapter.ApplyPlayerSaveSnapshot(save);
        }
    }
}
