using UnityEngine;

namespace Caelmor.VerticalSlice
{
    public class Entity
    {
        public string EntityId;
        public bool   IsPlayer;

        public Vector3 Position;
        public float   RotationY;

        public StatsComponent     Stats;
        public CombatComponent    Combat;
        public InventoryComponent Inventory;
        public EquipmentComponent Equipment;
        public SkillComponent     Skills;
        public AIController       AIController;

        // Dirty flags for persistence / snapshots
        public bool PositionDirty;

        public void MarkPositionDirty() => PositionDirty = true;
    }

    public class StatsComponent
    {
        public int MaxHp;
        public int CurrentHp;
        public int ArmorRating;
    }

    public class CombatComponent
    {
        public bool   IsAutoAttacking;
        public string TargetId;
        public string WeaponItemId;

        public int  AttackSpeedTicks;
        public long NextAttackTick;

        public int   AttackDamage;
        public float AttackRange;
    }

    // Minimal placeholders; you’ll likely swap these for your schema-backed data.
    public class InventoryComponent { }
    public class EquipmentComponent { }
    public class SkillComponent
    {
        public void AddXp(string skillId, int amount)
        {
            // Implement per-skill XP tracking here.
        }
    }
}
