using System;
using System.Collections.Generic;
using UnityEngine;

namespace Caelmor.VerticalSlice
{
    /// <summary>
    /// Server-authoritative inventory system for the Vertical Slice.
    /// Responsibilities:
    /// - Maintain per-entity inventories (stacking, limits, moves, splits).
    /// - Provide drag/drop style operations (move, swap, split).
    /// - Provide equip/unequip helpers and hooks.
    /// - Expose persistence-ready data structures for SaveSystem.
    ///
    /// NOTE: All methods are intended to be called on the HOST ONLY.
    /// Clients must never mutate inventory directly.
    /// </summary>
    public class InventorySystem
    {
        // --------------------------------------------------------------------
        // Public hooks
        // --------------------------------------------------------------------

        /// <summary>
        /// Fired after an item is equipped into an equipment slot.
        /// Args: (entity, equipSlotName, itemDef).
        /// </summary>
        public event Action<Entity, string, ItemDef> OnItemEquipped;

        /// <summary>
        /// Fired after an item is unequipped from an equipment slot.
        /// Args: (entity, equipSlotName, itemDef).
        /// </summary>
        public event Action<Entity, string, ItemDef> OnItemUnequipped;

        // External references
        public WorldManager    WorldManager    { get; set; }
        public EquipmentSystem EquipmentSystem { get; set; }

        // --------------------------------------------------------------------
        // Persistence-ready core types
        // --------------------------------------------------------------------

        /// <summary>
        /// Single inventory slot in memory.
        /// NOTE: InventoryComponent.Slots is expected to be InventorySlot[].
        /// </summary>
        [Serializable]
        public struct InventorySlot
        {
            public int Index;
            public string ItemId;
            public int Quantity;

            public bool IsEmpty => string.IsNullOrEmpty(ItemId) || Quantity <= 0;

            public void Clear()
            {
                ItemId = null;
                Quantity = 0;
            }
        }

        /// <summary>
        /// Serializable representation of a slot for SaveSystem.
        /// </summary>
        [Serializable]
        public struct InventorySlotSave
        {
            public int Index;
            public string ItemId;
            public int Quantity;
        }

        /// <summary>
        /// Helper to convert inventory component to/from save data.
        /// </summary>
        public static class InventorySerialization
        {
            public static InventorySlotSave[] ToSaveData(InventoryComponent inv)
            {
                if (inv == null || inv.Slots == null)
                    return Array.Empty<InventorySlotSave>();

                var result = new InventorySlotSave[inv.Slots.Length];
                for (int i = 0; i < inv.Slots.Length; i++)
                {
                    var slot = inv.Slots[i];
                    result[i] = new InventorySlotSave
                    {
                        Index    = slot.Index,
                        ItemId   = slot.ItemId,
                        Quantity = slot.Quantity
                    };
                }
                return result;
            }

            public static void FromSaveData(InventoryComponent inv, InventorySlotSave[] data)
            {
                if (inv == null)
                    return;

                if (data == null || data.Length == 0)
                {
                    if (inv.Slots == null)
                        inv.Slots = Array.Empty<InventorySlot>();
                    else
                    {
                        for (int i = 0; i < inv.Slots.Length; i++)
                        {
                            var s = inv.Slots[i];
                            s.Clear();
                            inv.Slots[i] = s;
                        }
                    }
                    return;
                }

                if (inv.Slots == null || inv.Slots.Length != data.Length)
                    inv.Slots = new InventorySlot[data.Length];

                for (int i = 0; i < data.Length; i++)
                {
                    inv.Slots[i] = new InventorySlot
                    {
                        Index    = data[i].Index,
                        ItemId   = data[i].ItemId,
                        Quantity = data[i].Quantity
                    };
                }
            }
        }

        // --------------------------------------------------------------------
        // Public API: Query helpers
        // --------------------------------------------------------------------

        /// <summary>
        /// Check if an entity has at least a certain quantity of an item.
        /// </summary>
        public bool HasItems(Entity entity, string itemId, int quantity)
        {
            if (entity?.Inventory?.Slots == null || string.IsNullOrEmpty(itemId) || quantity <= 0)
                return false;

            int count = 0;
            var slots = entity.Inventory.Slots;

            for (int i = 0; i < slots.Length; i++)
            {
                if (slots[i].ItemId == itemId)
                    count += slots[i].Quantity;

                if (count >= quantity)
                    return true;
            }

            return false;
        }

        /// <summary>
        /// Return total count of a given item in the entity inventory.
        /// </summary>
        public int CountItems(Entity entity, string itemId)
        {
            if (entity?.Inventory?.Slots == null || string.IsNullOrEmpty(itemId))
                return 0;

            int count = 0;
            var slots = entity.Inventory.Slots;

            for (int i = 0; i < slots.Length; i++)
            {
                if (slots[i].ItemId == itemId)
                    count += slots[i].Quantity;
            }

            return count;
        }

        // --------------------------------------------------------------------
        // Public API: Add / Consume / Crafting Helpers
        // --------------------------------------------------------------------

        /// <summary>
        /// Try to add quantity of itemId to entity inventory,
        /// respecting stack limits. Returns true if all quantity
        /// was added, false if some remains (outRemaining > 0).
        /// </summary>
        public bool TryAddItem(Entity entity, string itemId, int quantity, out int outRemaining)
        {
            outRemaining = quantity;
            if (entity?.Inventory?.Slots == null || string.IsNullOrEmpty(itemId) || quantity <= 0)
                return false;

            var inv   = entity.Inventory;
            var slots = inv.Slots;
            var def   = GetItemDef(itemId);
            int maxStack = GetMaxStack(def);

            // 1. Fill existing stacks
            for (int i = 0; i < slots.Length && outRemaining > 0; i++)
            {
                if (slots[i].ItemId != itemId)
                    continue;

                int canAdd = maxStack - slots[i].Quantity;
                if (canAdd <= 0)
                    continue;

                int toAdd = Mathf.Min(canAdd, outRemaining);
                slots[i].Quantity += toAdd;
                outRemaining -= toAdd;
            }

            // 2. Use empty slots
            for (int i = 0; i < slots.Length && outRemaining > 0; i++)
            {
                if (!slots[i].IsEmpty)
                    continue;

                int toAdd = Mathf.Min(maxStack, outRemaining);
                slots[i].ItemId   = itemId;
                slots[i].Quantity = toAdd;
                slots[i].Index    = i;
                outRemaining -= toAdd;
            }

            // Apply
            inv.Slots = slots;
            return outRemaining == 0;
        }

        /// <summary>
        /// Consume a quantity of an item from the inventory.
        /// Returns true if fully consumed; false if not enough items.
        /// </summary>
        public bool ConsumeItems(Entity entity, string itemId, int quantity)
        {
            if (!HasItems(entity, itemId, quantity))
                return false;

            var slots = entity.Inventory.Slots;
            int remaining = quantity;

            for (int i = 0; i < slots.Length && remaining > 0; i++)
            {
                if (slots[i].ItemId != itemId)
                    continue;

                int take = Mathf.Min(slots[i].Quantity, remaining);
                slots[i].Quantity -= take;
                remaining -= take;

                if (slots[i].Quantity <= 0)
                    slots[i].Clear();
            }

            entity.Inventory.Slots = slots;
            return true;
        }

        /// <summary>
        /// For crafting: check if entity has all required ingredient stacks.
        /// </summary>
        public bool HasIngredients(Entity entity, IEnumerable<RecipeIngredient> ingredients)
        {
            if (entity == null || ingredients == null)
                return false;

            foreach (var ing in ingredients)
            {
                if (!HasItems(entity, ing.ItemId, ing.Quantity))
                    return false;
            }
            return true;
        }

        /// <summary>
        /// For crafting: consume all required ingredients, assuming HasIngredients() already checked.
        /// </summary>
        public bool ConsumeIngredients(Entity entity, IEnumerable<RecipeIngredient> ingredients)
        {
            if (entity == null || ingredients == null)
                return false;

            foreach (var ing in ingredients)
            {
                if (!ConsumeItems(entity, ing.ItemId, ing.Quantity))
                    return false; // if this happens, state is inconsistent
            }
            return true;
        }

        // --------------------------------------------------------------------
        // Public API: Drag/Drop style operations
        // --------------------------------------------------------------------

        /// <summary>
        /// Move or merge a stack from one slot to another.
        /// - If dest empty: move whole stack.
        /// - If dest same item: merge up to stack limit.
        /// - If dest different item: swap.
        /// Returns true if any change occurred.
        /// </summary>
        public bool MoveSlot(Entity entity, int fromIndex, int toIndex)
        {
            if (entity?.Inventory?.Slots == null)
                return false;

            var slots = entity.Inventory.Slots;
            if (!IsValidIndex(slots, fromIndex) || !IsValidIndex(slots, toIndex) || fromIndex == toIndex)
                return false;

            var from = slots[fromIndex];
            var to   = slots[toIndex];

            if (from.IsEmpty)
                return false;

            // Destination empty → simple move
            if (to.IsEmpty)
            {
                slots[toIndex] = from;
                slots[toIndex].Index = toIndex;

                from.Clear();
                from.Index = fromIndex;
                slots[fromIndex] = from;
                entity.Inventory.Slots = slots;
                return true;
            }

            // Same item → try merge
            if (to.ItemId == from.ItemId)
            {
                var def = GetItemDef(from.ItemId);
                int maxStack = GetMaxStack(def);

                int canAdd = maxStack - to.Quantity;
                if (canAdd <= 0)
                {
                    // Nothing to merge, treat as swap
                    return SwapSlots(entity, fromIndex, toIndex);
                }

                int toMove = Mathf.Min(canAdd, from.Quantity);
                to.Quantity += toMove;
                from.Quantity -= toMove;

                if (from.Quantity <= 0)
                    from.Clear();

                slots[toIndex]   = to;
                slots[fromIndex] = from;
                entity.Inventory.Slots = slots;
                return true;
            }

            // Different items → swap
            return SwapSlots(entity, fromIndex, toIndex);
        }

        /// <summary>
        /// Split a stack from source into dest, up to splitAmount.
        /// Returns true if operation succeeded.
        /// </summary>
        public bool SplitStack(Entity entity, int fromIndex, int toIndex, int splitAmount)
        {
            if (entity?.Inventory?.Slots == null)
                return false;

            var slots = entity.Inventory.Slots;
            if (!IsValidIndex(slots, fromIndex) || !IsValidIndex(slots, toIndex) || splitAmount <= 0)
                return false;

            var from = slots[fromIndex];
            var to   = slots[toIndex];

            if (from.IsEmpty || from.Quantity <= splitAmount)
                return false; // nothing to split or not enough

            // If destination is non-empty, it must be same item.
            if (!to.IsEmpty && to.ItemId != from.ItemId)
                return false;

            var def = GetItemDef(from.ItemId);
            int maxStack = GetMaxStack(def);

            // Compute how much we can place into destination
            int destCurrent = to.IsEmpty ? 0 : to.Quantity;
            int canPlace    = maxStack - destCurrent;
            if (canPlace <= 0)
                return false;

            int actualSplit = Mathf.Min(splitAmount, canPlace);

            // Apply
            from.Quantity -= actualSplit;
            if (to.IsEmpty)
            {
                to.ItemId   = from.ItemId;
                to.Quantity = actualSplit;
                to.Index    = toIndex;
            }
            else
            {
                to.Quantity += actualSplit;
            }

            if (from.Quantity <= 0)
                from.Clear();

            slots[fromIndex] = from;
            slots[toIndex]   = to;
            entity.Inventory.Slots = slots;
            return true;
        }

        /// <summary>
        /// Swap two slots unconditionally (used by MoveSlot when needed).
        /// </summary>
        public bool SwapSlots(Entity entity, int indexA, int indexB)
        {
            if (entity?.Inventory?.Slots == null)
                return false;

            var slots = entity.Inventory.Slots;
            if (!IsValidIndex(slots, indexA) || !IsValidIndex(slots, indexB) || indexA == indexB)
                return false;

            var temp = slots[indexA];
            slots[indexA] = slots[indexB];
            slots[indexA].Index = indexA;
            slots[indexB] = temp;
            slots[indexB].Index = indexB;

            entity.Inventory.Slots = slots;
            return true;
        }

        // --------------------------------------------------------------------
        // Public API: Equip / Unequip
        // --------------------------------------------------------------------

        /// <summary>
        /// Equip one item from inventory slot into equipment slot.
        /// Replaces existing item in that equipment slot (if any),
        /// attempting to return it to inventory.
        /// </summary>
        public bool EquipFromSlot(Entity entity, int inventoryIndex, string equipSlotName)
        {
            if (entity?.Inventory?.Slots == null || entity.Equipment == null)
                return false;

            var slots = entity.Inventory.Slots;
            if (!IsValidIndex(slots, inventoryIndex))
                return false;

            var from = slots[inventoryIndex];
            if (from.IsEmpty)
                return false;

            var def = GetItemDef(from.ItemId);

            // TODO: validate equipSlotName against item definition (weapon vs armor etc.).

            // Take one item from stack
            from.Quantity -= 1;
            if (from.Quantity <= 0)
                from.Clear();
            slots[inventoryIndex] = from;

            // Store previous equipped item (if any)
            string prevItemId = null;
            if (entity.Equipment.Slots.TryGetValue(equipSlotName, out var current))
            {
                prevItemId = current;
            }

            // Equip new item
            entity.Equipment.Slots[equipSlotName] = def.ItemId;

            // Return previous to inventory if exists
            if (!string.IsNullOrEmpty(prevItemId))
            {
                TryAddItem(entity, prevItemId, 1, out int remaining);
                if (remaining > 0)
                {
                    // If no space, drop to world (optional / VS-specific)
                    DropItemToWorld(entity, prevItemId, 1);
                }
            }

            // Reapply derived stats
            EquipmentSystem?.UpdateDerivedStats(entity);

            entity.Inventory.Slots = slots;

            OnItemEquipped?.Invoke(entity, equipSlotName, def);
            return true;
        }

        /// <summary>
        /// Unequip item from equipSlotName back into inventory.
        /// </summary>
        public bool UnequipToSlot(Entity entity, string equipSlotName)
        {
            if (entity?.Equipment == null || entity.Inventory?.Slots == null)
                return false;

            if (!entity.Equipment.Slots.TryGetValue(equipSlotName, out var itemId))
                return false;

            if (string.IsNullOrEmpty(itemId))
                return false;

            var def = GetItemDef(itemId);

            bool added = TryAddItem(entity, itemId, 1, out int remaining);
            if (!added || remaining > 0)
            {
                // Inventory full, cannot unequip
                return false;
            }

            // Clear equipment slot
            entity.Equipment.Slots[equipSlotName] = null;
            EquipmentSystem?.UpdateDerivedStats(entity);

            OnItemUnequipped?.Invoke(entity, equipSlotName, def);
            return true;
        }

        // --------------------------------------------------------------------
        // Helpers
        // --------------------------------------------------------------------

        private static bool IsValidIndex(InventorySlot[] slots, int index)
        {
            return slots != null && index >= 0 && index < slots.Length;
        }

        private static ItemDef GetItemDef(string itemId)
        {
            if (string.IsNullOrEmpty(itemId))
                return null;

            ContentDatabase.Items.TryGetValue(itemId, out var def);
            return def;
        }

        /// <summary>
        /// Determine stack limit for an item definition.
        /// Requires ItemDef.MaxStack to exist; falls back to 1 if null/zero.
        /// </summary>
        private static int GetMaxStack(ItemDef def)
        {
            if (def == null)
                return 1;

            // Assumes ItemDef has MaxStack; if not, default to 1.
            return def.MaxStack > 0 ? def.MaxStack : 1;
        }

        /// <summary>
        /// VS stub: drops an item into the world when inventory is full.
        /// In a full implementation this would spawn a loot entity.
        /// </summary>
        private void DropItemToWorld(Entity entity, string itemId, int quantity)
        {
            if (WorldManager == null || entity == null || string.IsNullOrEmpty(itemId) || quantity <= 0)
                return;

            // TODO: Implement world drop spawn for VS, or leave as no-op until required.
        }
    }

    /// <summary>
    /// Basic ingredient description used by crafting.
    /// Matches the recipe schema and validation used for the VS crafting loop.
    /// </summary>
    public struct RecipeIngredient
    {
        public string ItemId;
        public int Quantity;
    }
}
