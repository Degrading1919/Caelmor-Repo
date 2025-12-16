using System;
using System.Collections.Generic;

namespace Caelmor.Systems
{
    // ----------------------------
    // Common
    // ----------------------------

    public readonly struct ValidationOptionalInt
    {
        public readonly bool HasValue;
        public readonly int Value;

        private ValidationOptionalInt(bool hasValue, int value)
        {
            HasValue = hasValue;
            Value = value;
        }

        public static ValidationOptionalInt Unknown() => new ValidationOptionalInt(false, 0);
        public static ValidationOptionalInt Known(int value) => new ValidationOptionalInt(true, value);

        public override string ToString() => HasValue ? Value.ToString() : "unknown";
    }

    // ----------------------------
    // Inventory snapshot
    // ----------------------------

    public readonly struct ValidationInventoryEntry
    {
        public readonly string ResourceItemKey;
        public readonly int Count;

        public ValidationInventoryEntry(string resourceItemKey, int count)
        {
            ResourceItemKey = resourceItemKey ?? throw new ArgumentNullException(nameof(resourceItemKey));
            Count = count;
        }
    }

    /// <summary>
    /// Deterministic inventory snapshot:
    /// - Entries are sorted lexicographically by ResourceItemKey (Ordinal).
    /// - Represents exact authoritative counts at capture time.
    /// </summary>
    public sealed class ValidationSnapshot_Inventory
    {
        public readonly int PlayerId;
        public readonly ValidationInventoryEntry[] Entries;

        public ValidationSnapshot_Inventory(int playerId, ValidationInventoryEntry[] entriesSorted)
        {
            PlayerId = playerId;
            Entries = entriesSorted ?? Array.Empty<ValidationInventoryEntry>();
        }

        public int IndexOf(string key)
        {
            // Binary search on sorted Entries by key.
            int lo = 0, hi = Entries.Length - 1;
            while (lo <= hi)
            {
                int mid = lo + ((hi - lo) >> 1);
                int cmp = string.Compare(Entries[mid].ResourceItemKey, key, StringComparison.Ordinal);
                if (cmp == 0) return mid;
                if (cmp < 0) lo = mid + 1;
                else hi = mid - 1;
            }
            return -1;
        }
    }

    // ----------------------------
    // Node snapshot
    // ----------------------------

    public enum ValidationNodeAvailability : byte
    {
        Unknown = 0,
        Available = 1,
        Depleted = 2
    }

    public readonly struct ValidationNodeEntry
    {
        public readonly int NodeInstanceId;
        public readonly bool Exists;
        public readonly ValidationNodeAvailability Availability;

        // Respawn ticks remaining may be unknown at runtime; persisted snapshots can provide it.
        public readonly ValidationOptionalInt RespawnTicksRemaining;

        public ValidationNodeEntry(
            int nodeInstanceId,
            bool exists,
            ValidationNodeAvailability availability,
            ValidationOptionalInt respawnTicksRemaining)
        {
            NodeInstanceId = nodeInstanceId;
            Exists = exists;
            Availability = availability;
            RespawnTicksRemaining = respawnTicksRemaining;
        }
    }

    /// <summary>
    /// Deterministic node state snapshot:
    /// - Entries are sorted ascending by NodeInstanceId.
    /// - RespawnTicksRemaining is "unknown" unless provided via persistence snapshot.
    /// </summary>
    public sealed class ValidationSnapshot_Nodes
    {
        public readonly ValidationNodeEntry[] Entries;

        public ValidationSnapshot_Nodes(ValidationNodeEntry[] entriesSortedById)
        {
            Entries = entriesSortedById ?? Array.Empty<ValidationNodeEntry>();
        }

        public int IndexOf(int nodeInstanceId)
        {
            int lo = 0, hi = Entries.Length - 1;
            while (lo <= hi)
            {
                int mid = lo + ((hi - lo) >> 1);
                int id = Entries[mid].NodeInstanceId;
                if (id == nodeInstanceId) return mid;
                if (id < nodeInstanceId) lo = mid + 1;
                else hi = mid - 1;
            }
            return -1;
        }
    }
}
