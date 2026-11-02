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
        public FlockDefinition[] flocks;
        public PresentationDefinition[] presentationEvents;
        public RespawnRegion[] respawnRegions;
        public GateDefinition[] gates;
        public TrapDefinition[] traps;
        public ArenaDefinition[] arenas;
        public FlagGroup[] exclusiveFlags;
        public void Validate()
        {
            Need(version == 1 && !string.IsNullOrWhiteSpace(id) && tuning != null, "content_header");
            Need(tuning.health > 0 && tuning.damage > 0 && tuning.attackTicks > 0, "content_tuning");
            var itemIds = Ids(items, x => x.id); var skillIds = Ids(skills, x => x.id);
            var targetIds = Ids(targets, x => x.id); var actionIds = Ids(actions, x => x.id);
            var questIds = Ids(quests, x => x.id); var enemyIds=Ids(enemies, x => x.id);
            var flockIds=Ids(flocks,f=>f.id);Ids(presentationEvents,p=>p.id);Ids(respawnRegions,r=>r.id);
            Ids(gates,g=>g.id);var trapIds=Ids(traps,t=>t.id);Ids(arenas,a=>a.id);
            foreach(var item in items) Need(item.tags!=null && item.tags.Distinct().Count()==item.tags.Length && item.tags.All(t=>!string.IsNullOrWhiteSpace(t)),"item_tags");
            Need(exclusiveFlags != null && exclusiveFlags.All(g=>g != null && g.flags != null && g.flags.Length>=2 && g.flags.Distinct().Count()==g.flags.Length), "exclusive_flags");
            foreach (var s in skills) Need(s.thresholds != null && s.thresholds.Length == 99 && s.thresholds[0] == 0 &&
                s.thresholds.Last() == 5000000 && s.thresholds.Skip(1).Zip(s.thresholds, (a,b) => a > b).All(x => x), "skill_thresholds");
            foreach (var t in targets) Need(Finite(t.x) && Finite(t.y) && Finite(t.z) && Math.Abs(t.x) <= 1000 && Math.Abs(t.z) <= 1000 && t.all != null && t.none != null, "target_position");
            foreach (var q in quests) { Need(q.all != null && q.startAll != null && q.stages != null && q.stages.Length > 0, "quest_stages"); Ids(q.stages, x => x.id); foreach (var s in q.stages) Conditions(s.all, Array.Empty<string>(), s.any, s.anyCount); }
            Need(actions.All(a=>a.counterEffects!=null),"counter_effects_array");
            var producedCounters=new HashSet<string>(actions.SelectMany(a=>a.counterEffects).Where(c=>c!=null).Select(c=>c.id),StringComparer.Ordinal);
            foreach(var effect in actions.SelectMany(a=>a.counterEffects)) Need(effect!=null && !string.IsNullOrWhiteSpace(effect.id) && effect.amount>0,"counter_effect");
            foreach(var stage in quests.SelectMany(q=>q.stages)) Need(stage.counterRequirements!=null && stage.counterRequirements.All(c=>c!=null && c.min>0 && producedCounters.Contains(c.id)),"counter_requirement");
            foreach (var a in actions)
            {
                Need(targetIds.Contains(a.target) && a.ticks >= 0 && a.cooldown >= 0 && a.xp >= 0, "action_target_or_timing");
                Need(new[]{"enter","dialogue","inspect","channel","gather","craft","lift","deliver","consume"}.Contains(a.kind), "action_kind");
                Need(string.IsNullOrEmpty(a.quest) || questIds.Contains(a.quest), "action_quest");
                if (!string.IsNullOrEmpty(a.quest)) { var q = quests.First(x=>x.id==a.quest); Need(a.minStage >= 0 && a.minStage <= q.stages.Length && (a.maxStage == -1 || a.maxStage >= a.minStage && a.maxStage < q.stages.Length), "action_stage_range"); }
                Need(string.IsNullOrEmpty(a.tool) || itemIds.Contains(a.tool), "action_tool");
                Need(a.xp == 0 || skillIds.Contains(a.skill), "action_skill");
                Need(a.flags != null && a.inputs != null && a.outputs != null && a.removeItems != null && a.conditionalOutputs != null, "action_arrays");
                Need(a.tagInputs!=null && a.tagInputs.All(t=>t!=null && t.count>0 && items.Any(i=>i.tags.Contains(t.tag))),"action_tag_inputs");
                Need(new[]{"","prepare","resolve","recover"}.Contains(a.flockOperation) && (string.IsNullOrEmpty(a.flock)?a.flockOperation=="":flockIds.Contains(a.flock) && a.flockOperation!=""),"action_flock");
                Need(new[]{"","inspect","disarm"}.Contains(a.trapOperation) && (string.IsNullOrEmpty(a.trap)?a.trapOperation=="":trapIds.Contains(a.trap)&&a.trapOperation!=""),"action_trap");
                if(a.flockOperation=="resolve") Need(a.xp==0 && a.inputs.Length==0 && a.tagInputs.Length==0 && a.outputs.Length==0 && a.conditionalOutputs.Length==0,"resolve_has_no_reward");
                if(a.flockOperation=="recover") Need(a.kind=="gather","recovery_is_gathering");
                Conditions(a.all, a.none, a.any, a.anyCount);
                foreach (var i in a.inputs.Concat(a.outputs)) Need(itemIds.Contains(i.id) && i.count > 0, "action_item");
                foreach (var i in a.removeItems) Need(itemIds.Contains(i), "action_remove_item");
                foreach (var i in a.conditionalOutputs) Need(itemIds.Contains(i.id) && i.count>0 && i.all!=null && i.none!=null,"conditional_output");
                if(a.kind=="gather") Need(targets.First(t=>t.id==a.target).nodeInstanceId>0 && skillIds.Contains(a.skill),"gather_placement");
                if(a.kind=="craft") Need(a.removeItems.Length==0,"craft_has_transfer_effect");
            }
            Need(targets.Where(t=>t.nodeInstanceId>0).Select(t=>t.nodeInstanceId).Distinct().Count()==targets.Count(t=>t.nodeInstanceId>0),"duplicate_node_placement");
            foreach (var e in enemies) Need(targetIds.Contains(e.target) && e.health > 0 && e.damage > 0 && e.windup > 0 && e.cooldown > 0 && e.range > 0 && e.leash >= e.range && e.respawn >= 0 && !string.IsNullOrEmpty(e.killFlag) && (string.IsNullOrEmpty(e.lootAction) || actionIds.Contains(e.lootAction)) && (string.IsNullOrEmpty(e.boundaryTarget) || targetIds.Contains(e.boundaryTarget) && e.boundaryRadius>0), "enemy_contract");
            foreach(var e in enemies) Need((string.IsNullOrEmpty(e.spawnFrom)||enemyIds.Contains(e.spawnFrom)&&e.spawnFrom!=e.id) && e.spawnHealthPercent>=0 && e.spawnHealthPercent<=100 && e.spawnWindupTicks>=0 && Finite(e.moveSpeed) && e.moveSpeed>=0,"enemy_spawn");
            Ids(hazards,h=>h.id);
            foreach(var h in hazards) Need(targetIds.Contains(h.target) && h.all!=null && h.none!=null && !string.IsNullOrEmpty(h.once) && h.windup>0 && h.damage>0 && h.radius>0 && h.pushDistance>=0,"hazard_contract");
            foreach(var f in flocks) Need(new[]{f.target,f.alternateTarget,f.coverTarget,f.recoveryTarget,f.closedTarget}.All(targetIds.Contains) && f.all!=null && f.none!=null && f.alertRadius>0 && f.coverRadius>0 && f.closedRadius>0 && f.warningTicks>0,"flock_contract");
            foreach(var p in presentationEvents) Need(targetIds.Contains(p.target) && !string.IsNullOrEmpty(p.triggerFlag) && (p.kind=="waterRise"&&p.rise>0 || p.kind=="quiet"&&p.rise==0&&!p.persistRise) && p.ticks>0 && Finite(p.rise),"presentation_contract");
            foreach(var r in respawnRegions) Need(targetIds.Contains(r.target) && Finite(r.x) && Finite(r.y) && Finite(r.z) && r.radius>0 && r.all!=null && r.none!=null,"respawn_region");
            foreach(var g in gates) Need(targetIds.Contains(g.target)&&Finite(g.yaw)&&g.width>0&&g.height>0&&g.depth>0&&g.openAll!=null&&g.openNone!=null,"gate_contract");
            foreach(var t in traps) Need(targetIds.Contains(t.target)&&Finite(t.yaw)&&t.width>0&&t.depth>0&&t.all!=null&&t.none!=null&&t.warningTicks>=0&&t.damage>=0&&t.staggerTicks>=0&&t.rearmTicks>=0&&t.activeTicks>0&&t.slowPermille>0&&t.slowPermille<=1000&&(string.IsNullOrEmpty(t.rearmEnemy)||enemyIds.Contains(t.rearmEnemy))&&(string.IsNullOrEmpty(t.disableEnemy)||enemyIds.Contains(t.disableEnemy))&&(string.IsNullOrEmpty(t.triggerEnemy)||enemyIds.Contains(t.triggerEnemy))&&t.triggerHealthPercent>=0&&t.triggerHealthPercent<=100,"trap_contract");
            foreach(var a in arenas) Need(targetIds.Contains(a.target)&&a.radius>0&&enemyIds.Contains(a.boss)&&a.enemies!=null&&a.enemies.Contains(a.boss)&&a.enemies.All(enemyIds.Contains)&&a.enemies.Distinct().Count()==a.enemies.Length&&a.all!=null&&a.none!=null,"arena_contract");
        }
        static HashSet<string> Ids<T>(T[] values, Func<T,string> key) { Need(values != null, "missing_array"); var ids=new HashSet<string>(StringComparer.Ordinal); foreach(var v in values) Need(v != null && !string.IsNullOrWhiteSpace(key(v)) && ids.Add(key(v)), "duplicate_or_empty_id"); return ids; }
        static void Conditions(string[] all, string[] none, string[] any, int count) { Need(all != null && none != null && any != null && count >= 0 && count <= any.Distinct().Count(), "conditions"); }
        internal static void Need(bool ok, string message) { if (!ok) throw new InvalidOperationException("GAMEPLAY_"+message); }
        internal static bool Finite(float n) => !float.IsNaN(n) && !float.IsInfinity(n);
    }
    [Serializable] public sealed class GameplayTuning { public int health, damage, attackTicks; public float respawnX, respawnZ; }
    [Serializable] public sealed class FlagGroup { public string[] flags; }
    [Serializable] public sealed class ItemDefinition { public string id, name; public int heal; public bool quest; public string[] tags; }
    [Serializable] public sealed class SkillDefinition { public string id, name; public int[] thresholds; }
    [Serializable] public sealed class ItemAmount { public string id; public int count; public ItemAmount(){} public ItemAmount(string id,int count){this.id=id;this.count=count;} }
    [Serializable] public sealed class TargetDefinition { public string id, name, kind; public float x,y,z; public int nodeInstanceId; public string[] all,none; }
    [Serializable] public sealed class ConditionalAmount { public string id; public int count; public string[] all,none; }
    [Serializable] public sealed class ActionDefinition
    {
        public string id,target,label,text,kind,quest,once,tool,skill,carry,requiresCarry;
        public int minStage,maxStage,anyCount,ticks,cooldown,xp;
        public string[] all,none,any,flags,removeItems; public ItemAmount[] inputs,outputs;
        public ConditionalAmount[] conditionalOutputs;
        public TagAmount[] tagInputs; public string flock,flockOperation,trap,trapOperation;
        public CounterEffect[] counterEffects;
    }
    [Serializable] public sealed class StageDefinition { public string id,objective; public string[] all,any; public int anyCount; public CounterRequirement[] counterRequirements; }
    [Serializable] public sealed class CounterEffect { public string id; public int amount; }
    [Serializable] public sealed class CounterRequirement { public string id; public int min; }
    [Serializable] public sealed class QuestDefinition { public string id,name; public string[] all,startAll; public StageDefinition[] stages; }
    [Serializable] public sealed class EnemyDefinition { public string id,target,killFlag,lootAction,boundaryTarget,spawnFrom; public string[] all,none; public int health,damage,windup,cooldown,respawn,spawnHealthPercent,spawnWindupTicks; public float range,leash,boundaryRadius,moveSpeed; }
    [Serializable] public sealed class TagAmount { public string tag; public int count; }
    [Serializable] public sealed class FlockDefinition { public string id,target,alternateTarget,coverTarget,recoveryTarget,closedTarget; public string[] all,none; public float alertRadius,coverRadius,closedRadius; public int warningTicks; }
    [Serializable] public sealed class PresentationDefinition { public string id,target,triggerFlag,kind; public int ticks; public float rise; public bool persistRise; }
    [Serializable] public sealed class RespawnRegion { public string id,target; public float x,y,z,radius; public string[] all,none; }
    [Serializable] public sealed class FlockProgress { public string id; public int positionIndex,warning; public bool prepared,recoveryPending; }
    [Serializable] public sealed class PresentationProgress { public string id; public bool seen; public int remaining; }
    public readonly struct GameplayPoint { public readonly float X,Y,Z; public GameplayPoint(float x,float z):this(x,0,z){} public GameplayPoint(float x,float y,float z){X=x;Y=y;Z=z;} }
    [Serializable] public sealed class GateDefinition { public string id,target;public float yaw,width,height,depth;public string[] openAll,openNone; }
    [Serializable] public sealed class TrapDefinition { public string id,target,alarmFlag,rearmEnemy,disableEnemy,triggerEnemy;public float yaw,width,depth;public string[] all,none;public int warningTicks,damage,staggerTicks,rearmTicks,activeTicks,slowPermille,triggerHealthPercent;public bool nonlethal; }
    [Serializable] public sealed class ArenaDefinition {public string id,target,boss;public float radius;public string[] enemies,all,none;}
    [Serializable] public sealed class TrapProgress {public string id;public bool revealed,disarmed,triggered;public int warning,cooldown,active;}
    [Serializable] public sealed class ArenaProgress {public string id;public bool engaged;}
    [Serializable] public sealed class HazardDefinition { public string id,target,once; public string[] all,none; public int windup,damage; public float radius,pushDistance; }
    [Serializable] public sealed class HazardProgress { public string id; public int remaining; }
    [Serializable] public sealed class QuestProgress { public string id; public int stage; }
    [Serializable] public sealed class EnemyProgress { public string id; public int health,windup,cooldown,respawn,spawnWarning; public bool loot,activated; public float aimX,aimY,aimZ,x,y,z; }
    [Serializable] public sealed class ActionProgress { public string id; public int cooldown; }
    [Serializable] public sealed class GameplaySave
    {
        public int version; public string contentId; public long tick; public int health;
        public string[] flags; public ItemAmount[] items,xp; public QuestProgress[] quests;
        public EnemyProgress[] enemies; public ActionProgress[] actions;
        public HazardProgress[] hazards;
        public FlockProgress[] flocks; public PresentationProgress[] presentations;
        public ItemAmount[] counters;
        public TrapProgress[] traps;public ArenaProgress[] arenas;
    }
}

