using System.Collections.Generic;

namespace Caelmor.VerticalSlice
{
    public class ItemDef
    {
        public string ItemId;
        public bool   IsRanged;
        public int    ArmorBonus;
        public int    WeaponDamage;
    }

    public static class ContentDatabase
    {
        // In VS, you can manually populate this in a bootstrap script
        // or via ScriptableObjects that feed into a runtime DB.
        public static readonly Dictionary<string, ItemDef> Items =
            new Dictionary<string, ItemDef>();
    }
}
