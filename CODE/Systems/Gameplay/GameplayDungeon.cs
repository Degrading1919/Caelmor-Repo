#nullable disable
using System;
using System.Linq;

namespace Caelmor.Runtime.Gameplay
{
    public sealed partial class GameplaySession
    {
        public bool GateIsOpen(int index)=>Meets(current.flags,content.gates[index].openAll,content.gates[index].openNone,Array.Empty<string>(),0);
        public TrapProgress Trap(int index)=>CloneTrap(current.data.traps[index]);
        public ArenaProgress Arena(int index)=>new ArenaProgress{id=current.data.arenas[index].id,engaged=current.data.arenas[index].engaged};
        static TrapProgress CloneTrap(TrapProgress p)=>new TrapProgress{id=p.id,revealed=p.revealed,disarmed=p.disarmed,triggered=p.triggered,warning=p.warning,cooldown=p.cooldown,active=p.active};
        EnemyProgress NewEnemy(EnemyDefinition definition)
        {
            var target=content.targets.First(t=>t.id==definition.target);
            return new EnemyProgress{id=definition.id,health=definition.health,x=target.x,y=target.y,z=target.z,activated=string.IsNullOrEmpty(definition.spawnFrom)};
        }
        static float Distance3(float x,float y,float z,float xx,float yy,float zz)=>(float)Math.Sqrt((x-xx)*(x-xx)+(y-yy)*(y-yy)+(z-zz)*(z-zz));
        bool CombatVisible(float x,float z,EnemyProgress enemy,int target,Func<int,bool> visible)=>executingSight!=null?executingSight(new GameplayPoint(x,executingY,z),new GameplayPoint(enemy.x,enemy.y,enemy.z)):(visible==null||visible(target));
        bool DungeonTargetVisible(State state,int target)
        {
            int enemy=Array.FindIndex(content.enemies,e=>e.target==content.targets[target].id);
            return enemy<0 || state.data.enemies[enemy].activated;
        }
        bool TrapActionEnabled(State state,ActionDefinition action)
        {
            if(string.IsNullOrEmpty(action.trap))return true;
            var trap=state.data.traps[Array.FindIndex(content.traps,t=>t.id==action.trap)];
            return action.trapOperation=="inspect" || trap.revealed && !trap.disarmed && trap.active==0;
        }
        void ApplyTrapAction(ActionDefinition action)
        {
            if(string.IsNullOrEmpty(action.trap))return;
            int index=Array.FindIndex(content.traps,t=>t.id==action.trap);var trap=draft.data.traps[index];var definition=content.traps[index];
            trap.revealed=true;
            if(action.trapOperation=="disarm")
            {
                trap.disarmed=true;trap.triggered=false;trap.warning=0;trap.active=0;
                trap.cooldown=!string.IsNullOrEmpty(definition.rearmEnemy)&&EnemyAlive(definition.rearmEnemy)?definition.rearmTicks:0;
            }
        }
        bool EnemyAlive(string id)
        {
            int index=Array.FindIndex(content.enemies,e=>e.id==id);
            return index>=0 && draft.data.enemies[index].health>0 && EnemyActive(draft,index);
        }
        bool TrapEnabled(TrapDefinition definition)=>Meets(draft.flags,definition.all,definition.none,Array.Empty<string>(),0);
        bool InTrap(TrapDefinition definition,float x,float y,float z)
        {
            var t=content.targets.First(target=>target.id==definition.target);if(Math.Abs(y-t.y)>.65f)return false;
            double radians=definition.yaw*Math.PI/180d;float dx=x-t.x,dz=z-t.z;
            double localX=dx*Math.Cos(radians)-dz*Math.Sin(radians),localZ=dx*Math.Sin(radians)+dz*Math.Cos(radians);
            return Math.Abs(localX)<=definition.width*.5 && Math.Abs(localZ)<=definition.depth*.5;
        }
        void FireTrap(TrapDefinition definition,TrapProgress state)
        {
            state.triggered=true;state.active=definition.activeTicks;state.cooldown=definition.rearmTicks;
            if(!string.IsNullOrEmpty(definition.alarmFlag))draft.flags.Add(definition.alarmFlag);
        }
        void TickTraps(float x,float y,float z)
        {
            draft.movement=1000;
            for(int i=0;i<content.traps.Length;i++)
            {
                var d=content.traps[i];var t=draft.data.traps[i];
                if(!TrapEnabled(d)){t.warning=0;continue;}
                if(!string.IsNullOrEmpty(d.disableEnemy)&&draft.data.enemies[Array.FindIndex(content.enemies,e=>e.id==d.disableEnemy)].health<=0){t.disarmed=true;t.warning=0;t.active=0;t.cooldown=0;continue;}
                if(t.disarmed)
                {
                    if(t.cooldown>0 && !string.IsNullOrEmpty(d.rearmEnemy))
                    {
                        if(!EnemyAlive(d.rearmEnemy))t.cooldown=0;
                        else if(--t.cooldown==0){t.disarmed=false;t.triggered=false;}
                    }
                    continue;
                }
                bool inside=InTrap(d,x,y,z);
                if(t.warning>0){if(--t.warning==0)FireTrap(d,t);}
                else if(t.active==0 && !t.triggered && t.cooldown==0)
                {
                    bool trigger=inside;
                    if(!string.IsNullOrEmpty(d.triggerEnemy))
                    {
                        int enemy=Array.FindIndex(content.enemies,e=>e.id==d.triggerEnemy);
                        trigger=EnemyAlive(d.triggerEnemy) && draft.data.enemies[enemy].health*100L<=content.enemies[enemy].health*(long)d.triggerHealthPercent;
                    }
                    if(trigger){t.warning=d.warningTicks;if(t.warning==0)FireTrap(d,t);}
                }
                if(t.active>0)
                {
                    if(inside && draft.data.health>0)
                    {
                        draft.movement=Math.Min(draft.movement,d.slowPermille);
                        // A timed floor payload pulses once per second; single-tick traps
                        // apply once. No frame-rate-dependent damage is introduced.
                        if(t.active==d.activeTicks || t.active%10==0)
                        {
                            int next=draft.data.health-d.damage;
                            draft.data.health=d.nonlethal?Math.Max(1,next):next;
                            draft.stagger=Math.Max(draft.stagger,d.staggerTicks);draft.channel=-1;
                        }
                    }
                    t.active--;
                }
                // HP-triggered room spills retain slow ground after their damage window.
                if(t.triggered && !string.IsNullOrEmpty(d.triggerEnemy) && inside)draft.movement=Math.Min(draft.movement,d.slowPermille);
                if(t.triggered && t.active==0 && t.warning==0 && t.cooldown>0)
                {
                    if(--t.cooldown==0 && string.IsNullOrEmpty(d.triggerEnemy))t.triggered=false;
                }
            }
        }
        void BeginDungeon(float x,float y,float z,Func<GameplayPoint,GameplayPoint,float,GameplayPoint> moveEnemy)
        {
            for(int i=0;i<content.arenas.Length;i++)
            {
                var definition=content.arenas[i];var state=draft.data.arenas[i];var center=content.targets.First(t=>t.id==definition.target);
                int boss=Array.FindIndex(content.enemies,e=>e.id==definition.boss);
                if(draft.data.enemies[boss].health<=0)continue;
                bool enabled=Meets(draft.flags,definition.all,definition.none,Array.Empty<string>(),0);
                bool inside=Distance3(x,y,z,center.x,center.y,center.z)<=definition.radius;
                if(state.engaged && (!inside||!enabled))ResetArena(i);
                else if(enabled && inside)state.engaged=true;
            }
            for(int i=0;i<content.enemies.Length;i++)
            {
                var d=content.enemies[i];var e=draft.data.enemies[i];
                if(!string.IsNullOrEmpty(d.spawnFrom) && !e.activated)
                {
                    int parent=Array.FindIndex(content.enemies,p=>p.id==d.spawnFrom);
                    if(e.spawnWarning>0){if(--e.spawnWarning==0)e.activated=true;}
                    else if(EnemyActive(draft,parent) && draft.data.enemies[parent].health>0 && draft.data.enemies[parent].health*100L<=content.enemies[parent].health*(long)d.spawnHealthPercent)
                    {e.spawnWarning=d.spawnWindupTicks;if(e.spawnWarning==0)e.activated=true;}
                }
                if(!EnemyActive(draft,i)||e.health<=0||e.windup>0||d.moveSpeed<=0||moveEnemy==null)continue;
                var origin=content.targets.First(t=>t.id==d.target);float distance=Distance3(x,y,z,e.x,e.y,e.z);
                if(distance<=d.range*.85f || Distance3(x,y,z,origin.x,origin.y,origin.z)>d.leash || !EnemyWithinBoundary(d,x,z))continue;
                float budget=d.moveSpeed*.1f;var moved=moveEnemy(new GameplayPoint(e.x,e.y,e.z),new GameplayPoint(x,y,z),budget);
                if(!GameplayContent.Finite(moved.X)||!GameplayContent.Finite(moved.Y)||!GameplayContent.Finite(moved.Z)||Distance3(e.x,e.y,e.z,moved.X,moved.Y,moved.Z)>budget+.01f||Distance3(origin.x,origin.y,origin.z,moved.X,moved.Y,moved.Z)>d.leash)continue;
                e.x=moved.X;e.y=moved.Y;e.z=moved.Z;
            }
        }
        void FinishDefeatedArenas()
        {
            for(int i=0;i<content.arenas.Length;i++)
            {
                int boss=Array.FindIndex(content.enemies,e=>e.id==content.arenas[i].boss);
                if(draft.data.enemies[boss].health<=0){draft.data.arenas[i].engaged=false;ClearArenaTraps(content.arenas[i]);}
            }
        }
        void ResetActiveArenas(){for(int i=0;i<content.arenas.Length;i++)if(draft.data.arenas[i].engaged)ResetArena(i);}
        void ResetArena(int index)
        {
            var definition=content.arenas[index];var state=draft.data.arenas[index];
            int boss=Array.FindIndex(content.enemies,e=>e.id==definition.boss);if(draft.data.enemies[boss].health<=0){state.engaged=false;return;}
            foreach(var id in definition.enemies)
            {
                int i=Array.FindIndex(content.enemies,e=>e.id==id);draft.data.enemies[i]=NewEnemy(content.enemies[i]);draft.flags.Remove(content.enemies[i].killFlag);
                if(draft.attack==i)draft.attack=-1;
            }
            ClearArenaTraps(definition);state.engaged=false;
        }
        void ClearArenaTraps(ArenaDefinition arena)
        {
            for(int i=0;i<content.traps.Length;i++)
            {
                var d=content.traps[i];if(!arena.enemies.Contains(d.triggerEnemy))continue;
                var t=draft.data.traps[i];t.warning=0;t.active=0;t.cooldown=0;t.triggered=false;
            }
        }
        void ValidateDungeonSave(GameplaySave save)
        {
            GameplayContent.Need(save.traps!=null&&save.arenas!=null&&save.traps.Length==content.traps.Length&&save.arenas.Length==content.arenas.Length,"save_dungeon_shape");
            for(int i=0;i<save.traps.Length;i++)
            {
                var p=save.traps[i];var d=content.traps[i];GameplayContent.Need(p!=null&&p.id==d.id&&p.warning>=0&&p.warning<=d.warningTicks&&p.cooldown>=0&&p.cooldown<=d.rearmTicks&&p.active>=0&&p.active<=d.activeTicks&&(!p.disarmed||p.warning==0&&p.active==0)&& (p.active==0||p.triggered),"save_trap");
            }
            for(int i=0;i<save.arenas.Length;i++)GameplayContent.Need(save.arenas[i]!=null&&save.arenas[i].id==content.arenas[i].id,"save_arena");
            for(int i=0;i<save.enemies.Length;i++)
            {
                var e=save.enemies[i];var d=content.enemies[i];var origin=content.targets.First(t=>t.id==d.target);
                GameplayContent.Need(GameplayContent.Finite(e.x)&&GameplayContent.Finite(e.y)&&GameplayContent.Finite(e.z)&&GameplayContent.Finite(e.aimY)&&e.spawnWarning>=0&&e.spawnWarning<=d.spawnWindupTicks&&(!string.IsNullOrEmpty(d.spawnFrom)||e.activated)&&(!e.activated||e.spawnWarning==0)&& (e.activated||e.health==d.health)&&Distance3(e.x,e.y,e.z,origin.x,origin.y,origin.z)<=d.leash+.01f,"save_enemy_pose");
            }
        }
        static bool DurableChanged(State before,State after)
        {
            if(!before.flags.SetEquals(after.flags)||before.data.quests.Where((q,i)=>q.stage!=after.data.quests[i].stage).Any()||before.data.xp.Where((v,i)=>v.count!=after.data.xp[i].count).Any()||before.data.counters.Where((v,i)=>v.count!=after.data.counters[i].count).Any())return true;
            var oldItems=before.inventory.DebugEnumerate(1).ToDictionary(v=>v.Key,v=>v.Value,StringComparer.Ordinal);var newItems=after.inventory.DebugEnumerate(1).ToDictionary(v=>v.Key,v=>v.Value,StringComparer.Ordinal);
            if(oldItems.Count!=newItems.Count||oldItems.Any(v=>!newItems.TryGetValue(v.Key,out int n)||n!=v.Value))return true;
            if(before.data.traps.Where((t,i)=>t.disarmed!=after.data.traps[i].disarmed||t.revealed!=after.data.traps[i].revealed).Any())return true;
            return before.data.flocks.Where((f,i)=>f.recoveryPending!=after.data.flocks[i].recoveryPending||f.positionIndex!=after.data.flocks[i].positionIndex).Any();
        }
    }
}
