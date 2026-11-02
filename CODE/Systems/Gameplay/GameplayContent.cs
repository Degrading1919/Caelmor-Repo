#nullable disable
using System;
using System.Collections.Generic;
using System.Linq;

namespace Caelmor.Runtime.Gameplay
{
    // DTOs implement GameplayContent.schema.json, independent of a serializer or Unity.
    [Serializable] public sealed class GameplayContent
    {
        public int version; public string id, title; public GameplayTuning tuning;
        public ItemDefinition[] items; public SkillDefinition[] skills; public TargetDefinition[] targets;
        public ActionDefinition[] actions; public QuestDefinition[] quests; public EnemyDefinition[] enemies;
        public HazardDefinition[] hazards;
        public FlagGroup[] exclusiveFlags;
        public void Validate()
        {
            Need(version == 1 && !string.IsNullOrWhiteSpace(id) && tuning != null, "content_header");
            Need(tuning.health > 0 && tuning.damage > 0 && tuning.attackTicks > 0, "content_tuning");
            var itemIds = Ids(items, x => x.id); var skillIds = Ids(skills, x => x.id);
            var targetIds = Ids(targets, x => x.id); var actionIds = Ids(actions, x => x.id);
            var questIds = Ids(quests, x => x.id); Ids(enemies, x => x.id);
            Need(exclusiveFlags != null && exclusiveFlags.All(g=>g != null && g.flags != null && g.flags.Length>=2 && g.flags.Distinct().Count()==g.flags.Length), "exclusive_flags");
            foreach (var s in skills) Need(s.thresholds != null && s.thresholds.Length == 99 && s.thresholds[0] == 0 &&
                s.thresholds.Last() == 5000000 && s.thresholds.Skip(1).Zip(s.thresholds, (a,b) => a > b).All(x => x), "skill_thresholds");
            foreach (var t in targets) Need(Finite(t.x) && Finite(t.z) && Math.Abs(t.x) <= 1000 && Math.Abs(t.z) <= 1000 && t.all != null && t.none != null, "target_position");
            foreach (var q in quests) { Need(q.all != null && q.stages != null && q.stages.Length > 0, "quest_stages"); Ids(q.stages, x => x.id); foreach (var s in q.stages) Conditions(s.all, Array.Empty<string>(), s.any, s.anyCount); }
            foreach (var a in actions)
            {
                Need(targetIds.Contains(a.target) && a.ticks >= 0 && a.cooldown >= 0 && a.xp >= 0, "action_target_or_timing");
                Need(new[]{"enter","dialogue","inspect","channel","gather","craft","lift","deliver","consume"}.Contains(a.kind), "action_kind");
                Need(string.IsNullOrEmpty(a.quest) || questIds.Contains(a.quest), "action_quest");
                if (!string.IsNullOrEmpty(a.quest)) { var q = quests.First(x=>x.id==a.quest); Need(a.minStage >= 0 && a.minStage <= q.stages.Length && (a.maxStage == -1 || a.maxStage >= a.minStage && a.maxStage < q.stages.Length), "action_stage_range"); }
                Need(string.IsNullOrEmpty(a.tool) || itemIds.Contains(a.tool), "action_tool");
                Need(a.xp == 0 || skillIds.Contains(a.skill), "action_skill");
                Need(a.flags != null && a.inputs != null && a.outputs != null && a.removeItems != null && a.conditionalOutputs != null, "action_arrays");
                Conditions(a.all, a.none, a.any, a.anyCount);
                foreach (var i in a.inputs.Concat(a.outputs)) Need(itemIds.Contains(i.id) && i.count > 0, "action_item");
                foreach (var i in a.removeItems) Need(itemIds.Contains(i), "action_remove_item");
                foreach (var i in a.conditionalOutputs) Need(itemIds.Contains(i.id) && i.count>0 && i.all!=null && i.none!=null,"conditional_output");
                if(a.kind=="gather") Need(targets.First(t=>t.id==a.target).nodeInstanceId>0 && skillIds.Contains(a.skill),"gather_placement");
                if(a.kind=="craft") Need(a.removeItems.Length==0,"craft_has_transfer_effect");
            }
            Need(targets.Where(t=>t.nodeInstanceId>0).Select(t=>t.nodeInstanceId).Distinct().Count()==targets.Count(t=>t.nodeInstanceId>0),"duplicate_node_placement");
            foreach (var e in enemies) Need(targetIds.Contains(e.target) && e.health > 0 && e.damage > 0 && e.windup > 0 && e.cooldown > 0 && e.range > 0 && e.leash >= e.range && e.respawn >= 0 && !string.IsNullOrEmpty(e.killFlag) && (string.IsNullOrEmpty(e.lootAction) || actionIds.Contains(e.lootAction)), "enemy_contract");
            Ids(hazards,h=>h.id);
            foreach(var h in hazards) Need(targetIds.Contains(h.target) && h.all!=null && h.none!=null && !string.IsNullOrEmpty(h.once) && h.windup>0 && h.damage>0 && h.radius>0 && h.pushDistance>=0,"hazard_contract");
        }
        static HashSet<string> Ids<T>(T[] values, Func<T,string> key) { Need(values != null, "missing_array"); var ids=new HashSet<string>(StringComparer.Ordinal); foreach(var v in values) Need(v != null && !string.IsNullOrWhiteSpace(key(v)) && ids.Add(key(v)), "duplicate_or_empty_id"); return ids; }
        static void Conditions(string[] all, string[] none, string[] any, int count) { Need(all != null && none != null && any != null && count >= 0 && count <= any.Distinct().Count(), "conditions"); }
        internal static void Need(bool ok, string message) { if (!ok) throw new InvalidOperationException("GAMEPLAY_"+message); }
        internal static bool Finite(float n) => !float.IsNaN(n) && !float.IsInfinity(n);
    }
    [Serializable] public sealed class GameplayTuning { public int health, damage, attackTicks; public float respawnX, respawnZ; }
    [Serializable] public sealed class FlagGroup { public string[] flags; }
    [Serializable] public sealed class ItemDefinition { public string id, name; public int heal; public bool quest; }
    [Serializable] public sealed class SkillDefinition { public string id, name; public int[] thresholds; }
    [Serializable] public sealed class ItemAmount { public string id; public int count; public ItemAmount(){} public ItemAmount(string id,int count){this.id=id;this.count=count;} }
    [Serializable] public sealed class TargetDefinition { public string id, name, kind; public float x,z; public int nodeInstanceId; public string[] all,none; }
    [Serializable] public sealed class ConditionalAmount { public string id; public int count; public string[] all,none; }
    [Serializable] public sealed class ActionDefinition
    {
        public string id,target,label,text,kind,quest,once,tool,skill,carry,requiresCarry;
        public int minStage,maxStage,anyCount,ticks,cooldown,xp;
        public string[] all,none,any,flags,removeItems; public ItemAmount[] inputs,outputs;
        public ConditionalAmount[] conditionalOutputs;
    }
    [Serializable] public sealed class StageDefinition { public string id,objective; public string[] all,any; public int anyCount; }
    [Serializable] public sealed class QuestDefinition { public string id,name; public string[] all; public StageDefinition[] stages; }
    [Serializable] public sealed class EnemyDefinition { public string id,target,killFlag,lootAction; public string[] all,none; public int health,damage,windup,cooldown,respawn; public float range,leash; }
    [Serializable] public sealed class HazardDefinition { public string id,target,once; public string[] all,none; public int windup,damage; public float radius,pushDistance; }
    [Serializable] public sealed class HazardProgress { public string id; public int remaining; }
    [Serializable] public sealed class QuestProgress { public string id; public int stage; }
    [Serializable] public sealed class EnemyProgress { public string id; public int health,windup,cooldown,respawn; public bool loot; public float aimX,aimZ; }
    [Serializable] public sealed class ActionProgress { public string id; public int cooldown; }
    [Serializable] public sealed class GameplaySave
    {
        public int version; public string contentId; public long tick; public int health;
        public string[] flags; public ItemAmount[] items,xp; public QuestProgress[] quests;
        public EnemyProgress[] enemies; public ActionProgress[] actions;
        public HazardProgress[] hazards;
    }
}
