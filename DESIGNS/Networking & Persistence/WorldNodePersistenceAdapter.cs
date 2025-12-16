// File: Persistence/WorldNodePersistenceAdapter.cs
// Stage 8.7 — ResourceNodeRuntimeSystem <-> WorldSave wiring

using System;
using System.Collections.Generic;
using Caelmor.Economy.ResourceNodes;

namespace Caelmor.Persistence
{
    public interface IWorldNodePersistenceAdapter
    {
        PersistedWorldSave BuildWorldSaveSnapshot();
        IReadOnlyList<PersistedNodeOverride> ConvertToRuntimeOverrides(PersistedWorldSave save);
    }

    public sealed class WorldNodePersistenceAdapter : IWorldNodePersistenceAdapter
    {
        private readonly ResourceNodeRuntimeSystem _nodeRuntime;
        private readonly List<PersistedNodeOverride> _scratchOverrides = new List<PersistedNodeOverride>(512);

        public WorldNodePersistenceAdapter(ResourceNodeRuntimeSystem nodeRuntime)
        {
            _nodeRuntime = nodeRuntime ?? throw new ArgumentNullException(nameof(nodeRuntime));
        }

        public PersistedWorldSave BuildWorldSaveSnapshot()
        {
            var save = new PersistedWorldSave();
            _scratchOverrides.Clear();

            _nodeRuntime.GetSaveSnapshot(_scratchOverrides);

            for (int i = 0; i < _scratchOverrides.Count; i++)
            {
                var ov = _scratchOverrides[i];

                var state = ov.Availability == ResourceNodeAvailability.Depleted
                    ? PersistedNodeState.Depleted
                    : PersistedNodeState.Available;

                // Persist ticks remaining (locked v1 decision).
                save.NodeOverrides.Add(new PersistedNodeOverrideDto(
                    nodeInstanceId: ov.NodeInstanceId,
                    state: state,
                    ticksRemaining: ov.RespawnTicksRemaining));
            }

            return save;
        }

        public IReadOnlyList<PersistedNodeOverride> ConvertToRuntimeOverrides(PersistedWorldSave save)
        {
            if (save == null) throw new ArgumentNullException(nameof(save));

            // Convert persisted DTOs into runtime overrides used by ResourceNodeRuntimeSystem.InitializeForZone(...)
            var list = new List<PersistedNodeOverride>(save.NodeOverrides.Count);

            for (int i = 0; i < save.NodeOverrides.Count; i++)
            {
                var dto = save.NodeOverrides[i];

                if (dto.State == PersistedNodeState.Depleted)
                {
                    list.Add(new PersistedNodeOverride(
                        dto.NodeInstanceId,
                        ResourceNodeAvailability.Depleted,
                        dto.TicksRemaining));
                }
                else
                {
                    list.Add(new PersistedNodeOverride(
                        dto.NodeInstanceId,
                        ResourceNodeAvailability.Available,
                        respawnTicksRemaining: 0));
                }
            }

            return list;
        }
    }
}
