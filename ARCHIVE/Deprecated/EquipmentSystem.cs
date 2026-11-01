// EquipmentSystem.cs
using System;
using System.Collections.Generic;

namespace Caelmor.VS
{
    /// <summary>
    /// Server-authoritative equipment management for a single entity.
    /// Works in tandem with InventorySystem (ID-based stacks) while using
    /// ItemInstance objects for equipped items (Model B hybrid architecture).
    ///
    /// Requirements:
    /// - 1 instance per entity
    /// - Inventory remains ID/quantity-based
    /// - Equipped items are ItemInstances
    /// - Derived stats accumulated from ItemDefinitions
    /// </summary>
    public class EquipmentSystem
    {
        // ------------------------------------------------------------------
        // Delegates (connected by InventorySystem or Entity initialization)
        // ------------------------------------------------------------------

        /// <summary>
        /// Called when the server attempts to remove 1 item from inventory.
        /// Expected to use InventorySystem.ConsumeItems(entity, item.itemId, 1).
        /// </summary>
        public Func<ItemInstance, bool> TryConsumeFromInventory { get; set; }

        /// <summary>
        /// Called when the server attempts to return 1 item to inventory.
        /// Expected to use InventorySystem.TryAddItem(...).
        /// </summary>
        public Func<ItemInstance, bool> TryReturnToInventory { get; set; }

        // ------------------------------------------------------------------
        // Events
        // ------------------------------------------------------------------

        public event Action<EquipmentSlot, ItemInstance> OnEquipped;
        public event Action<EquipmentSlot, ItemInstance> OnUnequipped;

        // ------------------------------------------------------------------
        // Internal State
        // ------------------------------------------------------------------

        /// <summary>
        /// Internal map of slot → equipped item (or null).
        /// </summary>
        private readonly Dictionary<EquipmentSlot, ItemInstance> _equipped;

        /// <summary>
        /// Last reason code after operations (for UI).
        /// </summary>
        public string LastOperationReason { get; private set; } = "success";

        public EquipmentSystem()
        {
            _equipped = new Dictionary<EquipmentSlot, ItemInstance>();
            InitializeSlots();
        }

        private void InitializeSlots()
        {
            foreach (EquipmentSlot slot in Enum.GetValues(typeof(EquipmentSlot)))
                _equipped[slot] = null;
        }

        // ------------------------------------------------------------------
        // Public API
        // ------------------------------------------------------------------

        public ItemInstance GetEquippedItem(EquipmentSlot slot)
        {
            return _equipped.TryGetValue(slot, out var item) ? item : null;
        }

        public IReadOnlyDictionary<EquipmentSlot, ItemInstance> GetAllEquipped()
        {
            return _equipped;
        }

        /// <summary>
        /// Attempts to equip an item instance (constructed from an itemId)
        /// after inventory has been validated.
        /// </summary>
        public bool TryEquip(ItemInstance instance, out string reason)
        {
            if (instance == null || instance.Definition == null)
            {
                reason = "item_null";
                LastOperationReason = reason;
                return false;
            }

            // Determine slot from definition.
            EquipmentSlot? slot = instance.Definition.GetEquipSlot();
            if (!slot.HasValue)
            {
                reason = "invalid_slot_for_item";
                LastOperationReason = reason;
                return false;
            }

            var targetSlot = slot.Value;

            // Inventory Enforcement: consume 1 unit of the item.
            if (TryConsumeFromInventory != null)
            {
                if (!TryConsumeFromInventory(instance))
                {
                    reason = "consume_failed";
                    LastOperationReason = reason;
                    return false;
                }
            }

            // Handle swap (return old item first)
            var previous = _equipped[targetSlot];
            if (previous != null && TryReturnToInventory != null)
            {
                if (!TryReturnToInventory(previous))
                {
                    // rollback consumed item
                    TryReturnToInventory?.Invoke(instance);

                    reason = "inventory_full";
                    LastOperationReason = reason;
                    return false;
                }
            }

            // Commit
            _equipped[targetSlot] = instance;
            OnEquipped?.Invoke(targetSlot, instance);

            reason = "success";
            LastOperationReason = reason;
            return true;
        }

        /// <summary>
        /// Attempts to unequip the item from a given slot.
        /// Returns the unequipped instance if successful.
        /// </summary>
        public bool TryUnequip(EquipmentSlot slot, out ItemInstance returnedInstance)
        {
            string r;
            var ok = TryUnequip(slot, out returnedInstance, out r);
            LastOperationReason = r;
            return ok;
        }

        public bool TryUnequip(EquipmentSlot slot, out ItemInstance returnedInstance, out string reason)
        {
            returnedInstance = null;

            if (!_equipped.ContainsKey(slot) || _equipped[slot] == null)
            {
                reason = "nothing_equipped";
                return false;
            }

            var instance = _equipped[slot];

            if (TryReturnToInventory != null)
            {
                if (!TryReturnToInventory(instance))
                {
                    reason = "inventory_full";
                    return false;
                }
            }

            _equipped[slot] = null;
            returnedInstance = instance;

            OnUnequipped?.Invoke(slot, instance);
            reason = "success";
            return true;
        }

        // ------------------------------------------------------------------
        // Stat Calculation
        // ------------------------------------------------------------------

        /// <summary>
        /// Applies all equipped contributions to base stats.
        /// </summary>
        public CharacterStats GetDerivedStats(CharacterStats baseStats)
        {
            int atk = baseStats.AttackPower;
            int def = baseStats.Defense;

            foreach (var kvp in _equipped)
            {
                var inst = kvp.Value;
                if (inst == null || inst.Definition == null)
                    continue;

                atk += inst.Definition.GetAttackPower();
                def += inst.Definition.GetDefense();
            }

            return new CharacterStats(atk, def);
        }

        // ------------------------------------------------------------------
        // Persistence
        // ------------------------------------------------------------------

        [Serializable]
        public class EquipmentSaveData
        {
            public string slot;
            public string itemId;
            public string instanceId; // for future unique items
        }

        public List<EquipmentSaveData> ToSaveData()
        {
            var list = new List<EquipmentSaveData>();

            foreach (var kvp in _equipped)
            {
                var slot = kvp.Key;
                var inst = kvp.Value;

                list.Add(new EquipmentSaveData
                {
                    slot = slot.ToString(),
                    itemId = inst?.itemId,
                    instanceId = inst?.instanceId
                });
            }

            return list;
        }

        /// <summary>
        /// Loads equipment from saved data.
        /// A resolver must create ItemInstances from itemIds.
        /// </summary>
        public void LoadFromSaveData(IEnumerable<EquipmentSaveData> data,
                                     Func<string, string, ItemInstance> instanceResolver)
        {
            ClearAll();

            if (data == null || instanceResolver == null)
                return;

            foreach (var entry in data)
            {
                if (!Enum.TryParse(entry.slot, true, out EquipmentSlot slot))
                    continue;

                if (string.IsNullOrEmpty(entry.itemId))
                {
                    _equipped[slot] = null;
                    continue;
                }

                var inst = instanceResolver(entry.itemId, entry.instanceId);
                _equipped[slot] = inst;
            }
        }

        public void ClearAll()
        {
            foreach (var key in _equipped.Keys)
                _equipped[key] = null;

            LastOperationReason = "success";
        }
    }
}
