// ItemInstance.cs
using System;
using UnityEngine;

namespace Caelmor.VS
{
    /// <summary>
    /// Represents a single equippable instance of an item.
    ///
    /// InventorySystem uses IDs + quantities (not instances), so ItemInstance
    /// is only created WHEN EQUIPPED or when a unique instance is explicitly needed.
    ///
    /// Future proof:
    /// - Can support durability
    /// - Can support affixes or modifiers
    /// - Can support soulbinding flags
    /// </summary>
    [Serializable]
    public class ItemInstance
    {
        /// <summary>
        /// Unique instance identifier, if needed later.
        /// For VS, generated but not functionally used.
        /// </summary>
        public string instanceId;

        /// <summary>
        /// The static item definition ID (matches ContentDatabase entry).
        /// </summary>
        public string itemId;

        /// <summary>
        /// Cached reference to the static definition object.
        /// Loaded via ContentDatabase when instance is created.
        /// </summary>
        public ItemDefinition Definition { get; private set; }

        public ItemInstance(string itemId)
        {
            this.itemId = itemId;
            this.instanceId = Guid.NewGuid().ToString();

            // Load definition now so EquipmentSystem can use it immediately.
            if (ContentDatabase.Items.TryGetValue(itemId, out var def))
            {
                Definition = def;
            }
            else
            {
                Debug.LogError($"ItemInstance created with unknown itemId: {itemId}");
                Definition = null;
            }
        }
    }
}
