// File: Persistence/EconomyPersistedDtos.cs
// Stage 8.7 — persisted shapes (in-memory DTOs, not file/db formats)

using System;
using System.Collections.Generic;

namespace Caelmor.Persistence
{
    public readonly struct PersistedInventoryEntry
    {
        public readonly string ResourceItemKey;
        public readonly int Count;

        public PersistedInventoryEntry(string resourceItemKey, int count)
        {
            ResourceItemKey = resourceItemKey;
            Count = count;
        }
    }

    public sealed class PersistedPlayerSave
    {
        public int PlayerId;
        public List<PersistedInventoryEntry> Inventory = new List<PersistedInventoryEntry>(64);
    }

    public sealed class PersistedWorldSave
    {
        // Node runtime overrides keyed by stable NodeInstanceId.
        public List<PersistedNodeOverrideDto> NodeOverrides = new List<PersistedNodeOverrideDto>(512);
    }

    public enum PersistedNodeState : byte
    {
        Available = 0,
        Depleted = 1
    }

    public readonly struct PersistedNodeOverrideDto
    {
        public readonly int NodeInstanceId;
        public readonly PersistedNodeState State;
        public readonly int TicksRemaining; // ticks-remaining persistence (Stage 7.5 locked v1)

        public PersistedNodeOverrideDto(int nodeInstanceId, PersistedNodeState state, int ticksRemaining)
        {
            NodeInstanceId = nodeInstanceId;
            State = state;
            TicksRemaining = ticksRemaining;
        }
    }
}
