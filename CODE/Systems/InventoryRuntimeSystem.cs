using System;
using System.Collections.Generic;
using System.Threading;
using Caelmor.Systems;

namespace Caelmor.Economy.Inventory
{
    /// <summary>
    /// Stage 26.B — Authoritative item + inventory runtime integration.
    /// Manages item instances, enforces single-owner invariant, and exposes deterministic queries.
    /// No persistence, no simulation execution, no client authority.
    /// </summary>
    public sealed class InventoryRuntimeSystem
    {
        private readonly IServerAuthority _authority;

        private readonly object _gate = new object();
        private readonly Dictionary<int, InventoryRecord> _inventories = new Dictionary<int, InventoryRecord>();
        private readonly Dictionary<ItemInstanceId, ItemRecord> _items = new Dictionary<ItemInstanceId, ItemRecord>();

        private int _nextInstanceId = 1;
        private int _mutationBlockDepth;

        public InventoryRuntimeSystem(IServerAuthority authority)
        {
            _authority = authority ?? throw new ArgumentNullException(nameof(authority));
        }

        /// <summary>
        /// Returns true when mutation is currently blocked due to simulation tick execution.
        /// </summary>
        public bool IsMutationBlocked => Volatile.Read(ref _mutationBlockDepth) > 0;

        /// <summary>
        /// Marks the start of a simulation tick. Mutations are forbidden until <see cref="ExitSimulation"/> is called.
        /// Idempotent and nestable for safety.
        /// </summary>
        public void EnterSimulation()
        {
            Interlocked.Increment(ref _mutationBlockDepth);
        }

        /// <summary>
        /// Marks the end of a simulation tick. Balances <see cref="EnterSimulation"/>.
        /// </summary>
        public void ExitSimulation()
        {
            int next = Interlocked.Decrement(ref _mutationBlockDepth);
            if (next < 0)
                Interlocked.Exchange(ref _mutationBlockDepth, 0);
        }

        /// <summary>
        /// Ensures an inventory exists for the given owner. Idempotent.
        /// </summary>
        public bool EnsureInventory(int ownerId, out bool wasCreated, out string? failureReason)
        {
            wasCreated = false;
            failureReason = null;

            if (!ValidateAuthority(out failureReason))
                return false;

            if (ownerId <= 0)
            {
                failureReason = "invalid_owner";
                return false;
            }

            lock (_gate)
            {
                if (_inventories.ContainsKey(ownerId))
                    return true;

                _inventories[ownerId] = new InventoryRecord(ownerId);
                wasCreated = true;
                return true;
            }
        }

        /// <summary>
        /// Creates a new item instance and assigns it to the owner's inventory.
        /// Atomic and ordered by monotonically increasing ItemInstanceId.
        /// </summary>
        public bool TryCreateItem(int ownerId, string definitionKey, out ItemInstanceId itemId, out string? failureReason)
        {
            itemId = default;
            failureReason = null;

            if (!ValidateAuthority(out failureReason))
                return false;

            if (IsMutationBlocked)
            {
                failureReason = "mid_tick_mutation_blocked";
                return false;
            }

            if (ownerId <= 0)
            {
                failureReason = "invalid_owner";
                return false;
            }

            if (string.IsNullOrWhiteSpace(definitionKey))
            {
                failureReason = "invalid_definition_key";
                return false;
            }

            lock (_gate)
            {
                if (!_inventories.TryGetValue(ownerId, out var inventory))
                {
                    failureReason = "inventory_missing";
                    return false;
                }

                itemId = AllocateId();
                var record = new ItemRecord(itemId, ownerId, definitionKey.Trim());
                _items.Add(itemId, record);
                inventory.Add(itemId);
                return true;
            }
        }

        /// <summary>
        /// Removes an item instance from its owning inventory. Fails if ownership does not match.
        /// </summary>
        public bool TryRemoveItem(int ownerId, ItemInstanceId itemId, out string? failureReason)
        {
            failureReason = null;

            if (!ValidateAuthority(out failureReason))
                return false;

            if (IsMutationBlocked)
            {
                failureReason = "mid_tick_mutation_blocked";
                return false;
            }

            if (ownerId <= 0 || !itemId.IsValid)
            {
                failureReason = "invalid_arguments";
                return false;
            }

            lock (_gate)
            {
                if (!_items.TryGetValue(itemId, out var item))
                {
                    failureReason = "item_missing";
                    return false;
                }

                if (item.OwnerId != ownerId)
                {
                    failureReason = "ownership_mismatch";
                    return false;
                }

                if (!_inventories.TryGetValue(ownerId, out var inventory))
                {
                    failureReason = "inventory_missing";
                    return false;
                }

                inventory.Remove(itemId);
                _items.Remove(itemId);
                return true;
            }
        }

        /// <summary>
        /// Transfers an item from one owner inventory to another atomically.
        /// </summary>
        public bool TryTransferItem(ItemInstanceId itemId, int fromOwnerId, int toOwnerId, out string? failureReason)
        {
            failureReason = null;

            if (!ValidateAuthority(out failureReason))
                return false;

            if (IsMutationBlocked)
            {
                failureReason = "mid_tick_mutation_blocked";
                return false;
            }

            if (!itemId.IsValid || fromOwnerId <= 0 || toOwnerId <= 0)
            {
                failureReason = "invalid_arguments";
                return false;
            }

            lock (_gate)
            {
                if (!_items.TryGetValue(itemId, out var item))
                {
                    failureReason = "item_missing";
                    return false;
                }

                if (item.OwnerId != fromOwnerId)
                {
                    failureReason = "ownership_mismatch";
                    return false;
                }

                if (!_inventories.TryGetValue(fromOwnerId, out var fromInventory))
                {
                    failureReason = "source_inventory_missing";
                    return false;
                }

                if (!_inventories.TryGetValue(toOwnerId, out var toInventory))
                {
                    failureReason = "destination_inventory_missing";
                    return false;
                }

                fromInventory.Remove(itemId);
                toInventory.Add(itemId);
                item.OwnerId = toOwnerId;
                return true;
            }
        }

        /// <summary>
        /// Returns a deterministic snapshot of inventory contents ordered by ItemInstanceId ascending.
        /// </summary>
        public IReadOnlyList<ItemInstanceView> GetInventorySnapshot(int ownerId)
        {
            lock (_gate)
            {
                if (!_inventories.TryGetValue(ownerId, out var inventory))
                    return Array.Empty<ItemInstanceView>();

                if (inventory.Count == 0)
                    return Array.Empty<ItemInstanceView>();

                var list = new List<ItemInstanceView>(inventory.Count);
                foreach (var id in inventory.ItemIds)
                {
                    if (_items.TryGetValue(id, out var item))
                        list.Add(new ItemInstanceView(item.Id, item.DefinitionKey, item.OwnerId));
                }

                return list;
            }
        }

        /// <summary>
        /// Determines the owning inventory for a given item instance.
        /// </summary>
        public bool TryGetOwner(ItemInstanceId itemId, out int ownerId)
        {
            ownerId = default;

            lock (_gate)
            {
                if (!_items.TryGetValue(itemId, out var item))
                    return false;

                ownerId = item.OwnerId;
                return true;
            }
        }

        private bool ValidateAuthority(out string? failureReason)
        {
            failureReason = null;
            if (_authority.IsServerAuthoritative)
                return true;

            failureReason = "not_server_authority";
            return false;
        }

        private ItemInstanceId AllocateId()
        {
            int next;
            lock (_gate)
            {
                next = _nextInstanceId++;
                if (_nextInstanceId <= 0)
                    _nextInstanceId = 1;
            }

            return new ItemInstanceId(next);
        }

        private sealed class InventoryRecord
        {
            private readonly SortedSet<ItemInstanceId> _itemIds = new SortedSet<ItemInstanceId>();

            public InventoryRecord(int ownerId) => OwnerId = ownerId;

            public int OwnerId { get; }

            public int Count => _itemIds.Count;
            public IEnumerable<ItemInstanceId> ItemIds => _itemIds;

            public void Add(ItemInstanceId itemId)
            {
                _itemIds.Add(itemId);
            }

            public void Remove(ItemInstanceId itemId)
            {
                _itemIds.Remove(itemId);
            }
        }

        private sealed class ItemRecord
        {
            public ItemRecord(ItemInstanceId id, int ownerId, string definitionKey)
            {
                Id = id;
                OwnerId = ownerId;
                DefinitionKey = definitionKey;
            }

            public ItemInstanceId Id { get; }
            public int OwnerId { get; set; }
            public string DefinitionKey { get; }
        }
    }

    public readonly struct ItemInstanceId : IEquatable<ItemInstanceId>, IComparable<ItemInstanceId>
    {
        public readonly int Value;

        public ItemInstanceId(int value)
        {
            Value = value;
        }

        public bool IsValid => Value > 0;

        public override string ToString() => IsValid ? $"item:{Value}" : "item:invalid";

        public bool Equals(ItemInstanceId other) => Value == other.Value;
        public override bool Equals(object obj) => obj is ItemInstanceId other && Equals(other);
        public override int GetHashCode() => Value;

        public int CompareTo(ItemInstanceId other) => Value.CompareTo(other.Value);

        public static bool operator ==(ItemInstanceId left, ItemInstanceId right) => left.Equals(right);
        public static bool operator !=(ItemInstanceId left, ItemInstanceId right) => !left.Equals(right);
    }

    public readonly struct ItemInstanceView
    {
        public readonly ItemInstanceId ItemId;
        public readonly string DefinitionKey;
        public readonly int OwnerId;

        public ItemInstanceView(ItemInstanceId itemId, string definitionKey, int ownerId)
        {
            ItemId = itemId;
            DefinitionKey = definitionKey ?? string.Empty;
            OwnerId = ownerId;
        }
    }
}
