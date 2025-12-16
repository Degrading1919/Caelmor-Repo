// ItemDefinition.cs
using System;
using UnityEngine;

namespace Caelmor.VS
{
    /// <summary>
    /// Data representation of an item as defined in content JSON.
    /// Matches VS Item Schema and supports helper functions
    /// used by Inventory, Equipment, and Combat/Stats systems.
    ///
    /// This object is loaded by ContentDatabase at startup.
    /// </summary>
    [Serializable]
    public class ItemDefinition
    {
        // ------------------------------------------------------------------
        // Core Identifiers
        // ------------------------------------------------------------------
        
        /// <summary>
        /// Unique ID used across the entire project (e.g., "lowmark_training_sword").
        /// Must match keys in ContentDatabase.Items.
        /// </summary>
        public string itemId;

        /// <summary>
        /// Broad category: "weapon", "armor", "material", etc.
        /// </summary>
        public string category;

        /// <summary>
        /// Subtype determines equip slot or usage: "head", "chest", "mainhand", "ore", etc.
        /// </summary>
        public string subType;

        // ------------------------------------------------------------------
        // Stats (Vertical Slice only)
        // ------------------------------------------------------------------

        /// <summary>
        /// Attack contribution if equipped (weapons).
        /// </summary>
        public int attackPower;

        /// <summary>
        /// Defense contribution if equipped (armor).
        /// </summary>
        public int defense;

        // ------------------------------------------------------------------
        // Inventory metadata
        // ------------------------------------------------------------------

        /// <summary>
        /// Maximum stack size for this item in inventory.
        /// </summary>
        public int maxStack = 1;

        // ------------------------------------------------------------------
        // Helper API
        // ------------------------------------------------------------------

        /// <summary>
        /// Returns TRUE if this item is equippable (weapons, armor).
        /// </summary>
        public bool IsEquippable()
        {
            if (string.IsNullOrEmpty(category))
                return false;

            var c = category.ToLowerInvariant();
            return c == "weapon" || c == "armor";
        }

        /// <summary>
        /// Resolves the intended equipment slot for this item.
        /// EquipmentSystem also has fallback logic, but this is the authoritative helper.
        /// </summary>
        public EquipmentSlot? GetEquipSlot()
        {
            if (!IsEquippable())
                return null;

            if (string.IsNullOrEmpty(subType))
                return null;

            string t = subType.ToLowerInvariant();

            switch (category.ToLowerInvariant())
            {
                case "weapon":
                    if (t == "offhand" || t == "shield")
                        return EquipmentSlot.OffHand;
                    return EquipmentSlot.MainHand;

                case "armor":
                    switch (t)
                    {
                        case "head":
                        case "helmet":
                            return EquipmentSlot.Head;

                        case "chest":
                        case "body":
                            return EquipmentSlot.Chest;

                        case "legs":
                        case "pants":
                            return EquipmentSlot.Legs;

                        case "hands":
                        case "gloves":
                            return EquipmentSlot.Hands;

                        case "feet":
                        case "boots":
                            return EquipmentSlot.Feet;

                        default:
                            return null;
                    }
            }

            return null;
        }

        /// <summary>
        /// Convenience helper for EquipmentSystem's stat accumulation.
        /// </summary>
        public int GetAttackPower() => attackPower;

        public int GetDefense() => defense;

        /// <summary>
        /// Getter used by InventorySystem for stack limits.
        /// </summary>
        public int GetMaxStack() => maxStack > 0 ? maxStack : 1;
    }
}
