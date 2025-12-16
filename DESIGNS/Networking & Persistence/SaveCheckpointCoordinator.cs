// File: Persistence/SaveCheckpointCoordinator.cs
// Stage 8.7 — checkpoint coordinator that flushes PlayerSave + WorldSave together.
// No storage tech implied; uses injected storages. No retries/backoff.

using System;
using System.Collections.Generic;

namespace Caelmor.Persistence
{
    public interface ISaveRequestSink
    {
        void MarkPlayerDirty(int playerId, string reasonCode);
        void MarkWorldDirty(string reasonCode);
        void RequestCheckpoint(string reasonCode);
    }

    public sealed class SaveCheckpointCoordinator : ISaveRequestSink
    {
        private readonly string _worldId;
        private readonly IPlayerSaveStorage _playerStorage;
        private readonly IWorldSaveStorage _worldStorage;
        private readonly IInventoryPersistenceAdapter _inventoryAdapter;
        private readonly IWorldNodePersistenceAdapter _nodeAdapter;

        private readonly HashSet<int> _dirtyPlayers = new HashSet<int>();
        private bool _worldDirty;
        private bool _checkpointRequested;

        public SaveCheckpointCoordinator(
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

        public void MarkPlayerDirty(int playerId, string reasonCode)
        {
            _dirtyPlayers.Add(playerId);
        }

        public void MarkWorldDirty(string reasonCode)
        {
            _worldDirty = true;
        }

        public void RequestCheckpoint(string reasonCode)
        {
            _checkpointRequested = true;
        }

        /// <summary>
        /// Called by engine at checkpoint opportunities (tick end / disconnect / shutdown).
        /// This method enforces Stage 7.5 rule: player + world mutations from same action
        /// must be committed in the SAME checkpoint cycle. :contentReference[oaicite:2]{index=2}
        /// </summary>
        public void CommitCheckpointIfRequested()
        {
            if (!_checkpointRequested)
                return;

            CommitCheckpoint();
        }

        public void CommitCheckpoint()
        {
            // If anything throws during commit, we FAIL LOUD and keep dirty flags.
            // This prevents “clear dirty on partial write” foot-guns.
            try
            {
                // 1) Persist PlayerSave snapshots for dirty players.
                foreach (int playerId in _dirtyPlayers)
                {
                    var playerSave = _inventoryAdapter.BuildPlayerSaveSnapshot(playerId);
                    _playerStorage.SavePlayer(playerSave);
                }

                // 2) Persist WorldSave snapshot if dirty.
                if (_worldDirty)
                {
                    var worldSave = _nodeAdapter.BuildWorldSaveSnapshot();
                    _worldStorage.SaveWorld(_worldId, worldSave);
                }

                // 3) Clear dirty flags ONLY after all saves succeeded.
                _dirtyPlayers.Clear();
                _worldDirty = false;
                _checkpointRequested = false;
            }
            catch (Exception ex)
            {
                // No auto-repair, no retries. Fail loudly.
                throw new InvalidOperationException(
                    $"Persistence checkpoint commit FAILED (no auto-repair). WorldId='{_worldId}'. " +
                    $"DirtyPlayers={_dirtyPlayers.Count}, WorldDirty={_worldDirty}.",
                    ex);
            }
        }
    }
}
