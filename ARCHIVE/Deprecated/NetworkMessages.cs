using System.Collections.Generic;
using UnityEngine;

namespace Caelmor.VerticalSlice
{
    // ------------------------ Client → Host ------------------------

    public struct PlayerInput_Move
    {
        public string   PlayerId;
        public Vector2  Direction;
        public float    ClientTime;
    }

    public struct PlayerInput_Attack
    {
        public string PlayerId;
        public string TargetEntityId;
        public string AbilityId;   // null/empty for auto-attack
        public bool   IsStart;
    }

    // ------------------------ Host → Client ------------------------

    public struct TransformSnapshot
    {
        public struct Entry
        {
            public string  EntityId;
            public Vector3 Position;
            public float   RotationY;
        }

        public List<Entry> Transforms;
    }

    public struct HpSnapshot
    {
        public struct Entry
        {
            public string EntityId;
            public int    CurrentHp;
            public int    MaxHp;
        }

        public List<Entry> Entries;
        public float       ServerTime;
    }

    public struct Event_CombatResult
    {
        public long   TickIndex;
        public string SourceEntityId;
        public string TargetEntityId;
        public int    Damage;
        public int    NewHp;
        public bool   IsKill;
        public bool   IsCrit;
    }

    // ------------------------ Aggregation ------------------------

    public class InputBatch
    {
        public readonly List<PlayerInput_Move>   MovementCommands = new List<PlayerInput_Move>();
        public readonly List<PlayerInput_Attack> AttackCommands   = new List<PlayerInput_Attack>();
        // Add inventory / craft later as needed.
    }
}
