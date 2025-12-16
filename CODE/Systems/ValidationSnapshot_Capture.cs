using System;
using System.Collections.Generic;
using Caelmor.Economy.Inventory;
using Caelmor.Economy.ResourceNodes;
using Caelmor.Persistence;

namespace Caelmor.Systems
{
    /// <summary>
    /// Stage 9.3: Snapshot capture helpers.
    /// - Read-only
    /// - Deterministic ordering
    /// - No gameplay events
    /// - No state mutation
    /// </summary>
    public static class ValidationSnapshotCapture
    {
        // ----------------------------
        // Inventory capture (runtime)
        // ----------------------------

        public static ValidationSnapshot_Inventory CaptureInventory(SimplePlayerInventoryStore inventory, int playerId)
        {
            if (inventory == null) throw new ArgumentNullException(nameof(inventory));

            // Use existing read-only enumeration hook (added in 8.7 plumbing).
            var scratch = new List<ValidationInventoryEntry>(64);

            foreach (var kv in inventory.DebugEnumerate(playerId))
            {
                // Fail loudly on invalid runtime state (should not happen).
                if (string.IsNullOrWhiteSpace(kv.Key))
                    throw new InvalidOperationException($"Validation snapshot: runtime inventory contains empty key for PlayerId={playerId}.");
                if (kv.Value < 0)
                    throw new InvalidOperationException($"Validation snapshot: runtime inventory contains negative count for key='{kv.Key}', PlayerId={playerId}.");

                // Count==0 should not exist in store; treat as a bug but capture it anyway.
                scratch.Add(new ValidationInventoryEntry(kv.Key, kv.Value));
            }

            scratch.Sort(static (a, b) => string.Compare(a.ResourceItemKey, b.ResourceItemKey, StringComparison.Ordinal));

            return new ValidationSnapshot_Inventory(playerId, scratch.ToArray());
        }

        // ----------------------------
        // Nodes capture (runtime)
        // ----------------------------

        /// <summary>
        /// Captures a node list snapshot from persistence-level WorldSave snapshot,
        /// which is the only guaranteed place to see respawn ticks remaining without
        /// modifying Stage 8.3 runtime query surfaces.
        /// </summary>
        public static ValidationSnapshot_Nodes CaptureNodesFromWorldSave(PersistedWorldSave worldSave)
        {
            if (worldSave == null) throw new ArgumentNullException(nameof(worldSave));

            var scratch = new List<ValidationNodeEntry>(worldSave.NodeOverrides.Count);

            for (int i = 0; i < worldSave.NodeOverrides.Count; i++)
            {
                var dto = worldSave.NodeOverrides[i];

                // Fail loudly on corrupt save contents; no auto-repair.
                if (dto.NodeInstanceId <= 0)
                    throw new InvalidOperationException($"Validation snapshot: corrupt WorldSave node override id={dto.NodeInstanceId}.");

                ValidationNodeAvailability avail = dto.State switch
                {
                    PersistedNodeState.Available => ValidationNodeAvailability.Available,
                    PersistedNodeState.Depleted => ValidationNodeAvailability.Depleted,
                    _ => ValidationNodeAvailability.Unknown
                };

                // ticks_remaining is authoritative in v1 persistence.
                var ticks = (avail == ValidationNodeAvailability.Depleted)
                    ? ValidationOptionalInt.Known(dto.TicksRemaining)
                    : ValidationOptionalInt.Known(0);

                scratch.Add(new ValidationNodeEntry(
                    nodeInstanceId: dto.NodeInstanceId,
                    exists: true,
                    availability: avail,
                    respawnTicksRemaining: ticks));
            }

            scratch.Sort(static (a, b) => a.NodeInstanceId.CompareTo(b.NodeInstanceId));
            return new ValidationSnapshot_Nodes(scratch.ToArray());
        }

        /// <summary>
        /// Captures node availability for a known list of ids directly from runtime.
        /// Respawn ticks are unknown because the runtime query surface does not expose them.
        /// </summary>
        public static ValidationSnapshot_Nodes CaptureNodesAvailabilityOnly(ResourceNodeRuntimeSystem nodeRuntime, IReadOnlyList<int> nodeInstanceIds)
        {
            if (nodeRuntime == null) throw new ArgumentNullException(nameof(nodeRuntime));
            if (nodeInstanceIds == null) throw new ArgumentNullException(nameof(nodeInstanceIds));

            var scratch = new List<ValidationNodeEntry>(nodeInstanceIds.Count);

            for (int i = 0; i < nodeInstanceIds.Count; i++)
            {
                int id = nodeInstanceIds[i];
                bool exists = nodeRuntime.TryGetNodeAvailability(id, out var a);

                var avail = ValidationNodeAvailability.Unknown;
                if (exists)
                {
                    avail = (a == ResourceNodeAvailability.Available)
                        ? ValidationNodeAvailability.Available
                        : ValidationNodeAvailability.Depleted;
                }

                scratch.Add(new ValidationNodeEntry(
                    nodeInstanceId: id,
                    exists: exists,
                    availability: avail,
                    respawnTicksRemaining: ValidationOptionalInt.Unknown()));
            }

            scratch.Sort(static (x, y) => x.NodeInstanceId.CompareTo(y.NodeInstanceId));
            return new ValidationSnapshot_Nodes(scratch.ToArray());
        }
    }
}
