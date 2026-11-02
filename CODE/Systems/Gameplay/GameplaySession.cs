#nullable disable
using System;
using System.Collections.Generic;
using System.Linq;
using Caelmor.Economy.Inventory;
using Caelmor.Persistence;
using Caelmor.Runtime.Players;
using Caelmor.Runtime.Quests;
using Caelmor.Systems;

namespace Caelmor.Runtime.Gameplay
{
    /// <summary>Content-driven authoritative activity composition. No Unity, disk, UI, quest IDs,
    /// or client positions. Drafts are private until CommitTick at host finalization.</summary>
    public sealed partial class GameplaySession
    {
        readonly GameplayContent content;
        readonly string identity;
        readonly Func<bool> participating;
        readonly QuestBridge bridge;
        readonly QuestRuntimeSystem quests;
        readonly QuestInstanceId[] questIds;
        readonly string[] counterIds;
        State current, draft;
        long preparedTick, lastHostTick;
        bool restored;
        public string Feedback { get; private set; } = "Explore the landing. Select a person or object, then approach to interact.";
        string draftFeedback;
        public string Carry => current.carry;
        public int ChannelAction => current.channel;
        public int ChannelRemaining => current.remaining;
        public bool PendingRespawn { get; private set; }
        public float PendingPushX { get; private set; }
        public float PendingPushZ { get; private set; }
        public float PendingRespawnX { get; private set; }
        public float PendingRespawnZ { get; private set; }
        public bool Has(string flag) => current.flags.Contains(flag);
        public int Quantity(string item) => Count(current,item);
        public int Health => current.data.health;
        public int Counter(string key)=>current.data.counters.FirstOrDefault(c=>c.id==key)?.count??0;
        public int Level(int skill) => content.skills[skill].thresholds.Count(t => t <= current.data.xp[skill].count);
        public int Stage(int quest) => current.data.quests[quest].stage;
        public QuestState CoarseState(int quest) { quests.TryGetState(questIds[quest],out var state); return state; }
        public GameplaySession(GameplayContent content, string contentIdentity, PlayerHandle owner, Func<bool> participating)
        {
            this.content=content ?? throw new ArgumentNullException(nameof(content)); content.Validate();
            identity=contentIdentity ?? throw new ArgumentNullException(nameof(contentIdentity)); this.participating=participating ?? throw new ArgumentNullException(nameof(participating));
            counterIds=content.actions.SelectMany(a=>a.counterEffects).Select(c=>c.id).Concat(content.quests.SelectMany(q=>q.stages).SelectMany(s=>s.counterRequirements).Select(c=>c.id)).Distinct(StringComparer.Ordinal).OrderBy(c=>c,StringComparer.Ordinal).ToArray();
            bridge=new QuestBridge(owner, participating); quests=new QuestRuntimeSystem(bridge,bridge,bridge,bridge);
            questIds=content.quests.Select(q=>new QuestInstanceId(Guid.NewGuid())).ToArray();
            for(int i=0;i<questIds.Length;i++) GameplayContent.Need(quests.RegisterQuest(questIds[i],owner,content.quests[i].id).Ok,"quest_register");
            current=NewState();
        }
        State NewState()
        {
            var save=new GameplaySave { version=1,contentId=identity,tick=0,health=content.tuning.health,flags=Array.Empty<string>(),items=Array.Empty<ItemAmount>(),
                xp=content.skills.Select(s=>new ItemAmount(s.id,0)).ToArray(),quests=content.quests.Select(q=>new QuestProgress{id=q.id,stage=0}).ToArray(),
                enemies=content.enemies.Select(e=>new EnemyProgress{id=e.id,health=e.health}).ToArray(),actions=content.actions.Select(a=>new ActionProgress{id=a.id}).ToArray(),hazards=content.hazards.Select(h=>new HazardProgress{id=h.id}).ToArray(),
                flocks=content.flocks.Select(f=>new FlockProgress{id=f.id}).ToArray(),presentations=content.presentationEvents.Select(p=>new PresentationProgress{id=p.id}).ToArray(),counters=counterIds.Select(id=>new ItemAmount(id,0)).ToArray() };
            return new State(save);
        }
        public GameplaySave Capture() { GameplayContent.Need(draft==null,"save_during_prepare"); return Copy(current); }
        public void Restore(GameplaySave save)
        {
            GameplayContent.Need(draft==null && lastHostTick==0 && !this.restored && participating(),"restore_requires_fresh_session");
            ValidateSave(save); var restored=new State(Clone(save));
            foreach(var presentation in restored.data.presentations)presentation.remaining=0;
            current=restored; this.restored=true; Feedback="Checkpoint restored. Interrupted channels, combat and carries were cleared.";
            SynchronizeQuests();
        }
        public void ValidateSave(GameplaySave s)
        {
            GameplayContent.Need(s!=null && s.version==1 && s.contentId==identity && s.tick>=0 && s.health>0 && s.health<=content.tuning.health,"save_header");
            GameplayContent.Need(s.items!=null && s.xp!=null && s.flags!=null && s.quests!=null && s.enemies!=null && s.actions!=null && s.hazards!=null && s.flocks!=null && s.presentations!=null && s.counters!=null,"save_arrays");
            GameplayContent.Need(s.counters.Length==counterIds.Length,"save_counter_shape");
            for(int i=0;i<s.counters.Length;i++) GameplayContent.Need(s.counters[i]!=null && s.counters[i].id==counterIds[i] && s.counters[i].count>=0,"save_counter");
            var knownItems=new HashSet<string>(content.items.Select(i=>i.id)); var seen=new HashSet<string>();
            foreach(var i in s.items) GameplayContent.Need(i!=null && knownItems.Contains(i.id) && i.count>0 && seen.Add(i.id),"save_inventory");
            var knownFlags=new HashSet<string>(content.actions.SelectMany(a=>a.flags).Concat(content.actions.Select(a=>a.once).Where(x=>!string.IsNullOrEmpty(x))).Concat(content.enemies.Select(e=>e.killFlag)).Concat(content.hazards.Select(h=>h.once)));
            GameplayContent.Need(s.flags.Distinct().Count()==s.flags.Length && s.flags.All(knownFlags.Contains),"save_flags");
            GameplayContent.Need(s.xp.Length==content.skills.Length && s.quests.Length==content.quests.Length && s.enemies.Length==content.enemies.Length && s.actions.Length==content.actions.Length && s.hazards.Length==content.hazards.Length && s.flocks.Length==content.flocks.Length && s.presentations.Length==content.presentationEvents.Length,"save_shape");
            for(int i=0;i<s.xp.Length;i++) GameplayContent.Need(s.xp[i]!=null && s.xp[i].id==content.skills[i].id && s.xp[i].count>=0 && s.xp[i].count<=5000000,"save_xp");
            var flags=new HashSet<string>(s.flags);
            foreach(var group in content.exclusiveFlags) GameplayContent.Need(group.flags.Count(flags.Contains)<=1,"save_choice_conflict");
            for(int i=0;i<s.quests.Length;i++)
            {
                var q=s.quests[i]; var def=content.quests[i]; GameplayContent.Need(q!=null && q.id==def.id && q.stage>=0 && q.stage<=def.stages.Length,"save_quest");
                GameplayContent.Need(q.stage==0 || def.all.All(flags.Contains),"save_quest_prerequisite");
                for(int j=0;j<q.stage;j++) GameplayContent.Need(StageSatisfied(flags,s.counters,def.stages[j]),"save_quest_history");
            }
            for(int i=0;i<s.enemies.Length;i++) { var e=s.enemies[i]; var d=content.enemies[i]; GameplayContent.Need(e!=null && e.id==d.id && e.health>=0 && e.health<=d.health && e.windup>=0 && e.windup<=d.windup && e.cooldown>=0 && e.cooldown<=d.cooldown && e.respawn>=0 && e.respawn<=d.respawn && GameplayContent.Finite(e.aimX) && GameplayContent.Finite(e.aimZ) && (!e.loot || e.health==0) && (e.health!=0 || flags.Contains(d.killFlag)),"save_enemy"); }
            for(int i=0;i<s.actions.Length;i++) GameplayContent.Need(s.actions[i]!=null && s.actions[i].id==content.actions[i].id && s.actions[i].cooldown>=0 && s.actions[i].cooldown<=content.actions[i].cooldown,"save_action");
            for(int i=0;i<s.hazards.Length;i++) GameplayContent.Need(s.hazards[i]!=null && s.hazards[i].id==content.hazards[i].id && s.hazards[i].remaining>=0 && s.hazards[i].remaining<=content.hazards[i].windup && (!flags.Contains(content.hazards[i].once) || s.hazards[i].remaining==0),"save_hazard");
            ValidateOpportunitySave(s,flags);
        }
        public void PrepareTick(long tick,float x,float z,IReadOnlyList<GameplayRequest> requests,Func<int,bool> visible,bool rushing=false)
        {
            GameplayContent.Need(draft==null && tick>lastHostTick && GameplayContent.Finite(x) && GameplayContent.Finite(z),"tick_boundary");
            GameplayContent.Need(participating(),"not_participating");
            draft=new State(Copy(current)){carry=current.carry,channel=current.channel,remaining=current.remaining,attack=current.attack,attackWait=current.attackWait,originX=current.originX,originZ=current.originZ};
            preparedTick=tick; draft.data.tick=tick; draftFeedback=Feedback; PendingRespawn=false;PendingPushX=PendingPushZ=0;
            PendingRespawnX=content.tuning.respawnX;PendingRespawnZ=content.tuning.respawnZ;
            foreach(var a in draft.data.actions) if(a.cooldown>0)a.cooldown--;
            for(int i=0;i<draft.data.enemies.Length;i++)
            {
                var e=draft.data.enemies[i]; var d=content.enemies[i];
                if(e.health==0 && d.respawn>0 && --e.respawn<=0) { e.health=d.health;e.loot=false;e.cooldown=0;e.windup=0; }
            }
            TickFlocks(x,z,rushing);
            // One actionable request per tick; duplicates cannot multiply zero-duration rewards.
            if(requests!=null && requests.Count>0)
            {
                var r=requests[requests.Count-1];
                if(r.Kind==GameplayRequestKind.Cancel) { draft.channel=-1;draft.attack=-1;draft.carry=""; Say("Activity cancelled. Carried loads can be collected again."); }
                else if(r.Kind==GameplayRequestKind.Attack) { if(r.Index>=0 && r.Index<content.enemies.Length && EnemyActive(draft,r.Index) && draft.data.enemies[r.Index].health>0) { draft.channel=-1;draft.attack=r.Index; } else Say("That target cannot be attacked."); }
                else if(r.Kind==GameplayRequestKind.Consume) Consume(r.Index);
                else if(r.Kind==GameplayRequestKind.Action) StartAction(r.Index,x,z,visible);
            }
            // Incoming combat resolves before a channel's final tick so a hit cannot
            // both interrupt the action and let its resource/XP transaction escape.
            Combat(x,z,visible);
            Hazards(x,z);
            if(draft.channel>=0)
            {
                int i=draft.channel;
                if(Distance(x,z,draft.originX,draft.originZ)>.15f || !CanUse(draft,i,x,z,visible)) {draft.channel=-1;Say("Action interrupted. No resources consumed.");}
                else if(--draft.remaining<=0) { draft.channel=-1;Apply(i); }
            }
            // Content-authored enter volumes use the same condition and finalization path.
            if(draft.channel<0) for(int i=0;i<content.actions.Length;i++) if(content.actions[i].kind=="enter" && CanUse(draft,i,x,z,visible)) { StartAction(i,x,z,visible); break; }
            if(draft.data.health<=0)
            {
                draft.data.health=content.tuning.health;draft.channel=-1;draft.attack=-1;draft.carry="";PendingRespawn=true;
                foreach(var e in draft.data.enemies){e.windup=0;e.cooldown=0;}
                Say("You recovered at the crew fire. Quest progress and inventory retained.");
                foreach(var region in content.respawnRegions)
                {
                    var center=content.targets.First(t=>t.id==region.target);
                    if(Meets(draft.flags,region.all,region.none,Array.Empty<string>(),0) && Distance(x,z,center.x,center.z)<=region.radius)
                    {PendingRespawnX=region.x;PendingRespawnZ=region.z;Say("You recovered at "+center.name+". Quest progress and inventory retained.");break;}
                }
            }
            TickPresentations();
            for(int i=0;i<content.quests.Length;i++)
            {
                var def=content.quests[i];var q=draft.data.quests[i];
                if(!def.all.All(draft.flags.Contains))continue;
                while(q.stage<def.stages.Length && StageSatisfied(draft.flags,draft.data.counters,def.stages[q.stage])) q.stage++;
            }
        }
        public void CommitTick(long tick)
        {
            GameplayContent.Need(draft!=null && preparedTick==tick && participating(),"commit_boundary");
            current=draft;draft=null;lastHostTick=tick;Feedback=draftFeedback;SynchronizeQuests();
        }
        public void AbortTick(){draft=null;PendingRespawn=false;PendingPushX=PendingPushZ=0;}
        public void ClearTransient(){ GameplayContent.Need(draft==null,"clear_mid_tick"); current.channel=-1;current.attack=-1; }
        void SynchronizeQuests()
        {
            bridge.committing=true;
            try { for(int i=0;i<questIds.Length;i++) { if(!content.quests[i].all.All(current.flags.Contains))continue; quests.TryGetState(questIds[i],out var state); if(state==QuestState.Inactive) GameplayContent.Need(quests.ActivateQuest(questIds[i]).Ok,"quest_activate"); if(current.data.quests[i].stage==content.quests[i].stages.Length) GameplayContent.Need(quests.CompleteQuest(questIds[i]).Ok,"quest_complete"); } }
            finally {bridge.committing=false;}
        }
        public bool Available(int action) => action>=0 && action<content.actions.Length && Enabled(current,action);
        public bool QuestAvailable(int quest)=>content.quests[quest].all.All(current.flags.Contains);
        public int HazardRemaining(int hazard)=>current.data.hazards[hazard].remaining;
        public bool TargetVisible(int target) => target>=0 && target<content.targets.Length && Meets(current.flags,content.targets[target].all,content.targets[target].none,Array.Empty<string>(),0) && OpportunityTargetVisible(current,target);
        public EnemyProgress Enemy(int i) => CloneEnemy(current.data.enemies[i]);
        bool Enabled(State s,int i)
        {
            var a=content.actions[i]; if(!string.IsNullOrEmpty(a.once)&&s.flags.Contains(a.once) || s.data.actions[i].cooldown>0 || !Meets(s.flags,a.all,a.none,a.any,a.anyCount))return false;
            foreach(var group in content.exclusiveFlags) if(a.flags.Any(group.flags.Contains) && group.flags.Any(s.flags.Contains))return false;
            int qi=Array.FindIndex(content.quests,q=>q.id==a.quest);
            if(qi>=0 && !content.quests[qi].all.All(s.flags.Contains))return false;
            if(qi>=0 && (s.data.quests[qi].stage<a.minStage || a.maxStage>=0 && s.data.quests[qi].stage>a.maxStage))return false;
            if(!string.IsNullOrEmpty(a.requiresCarry) && (a.requiresCarry=="-" ? s.carry.Length>0 : s.carry!=a.requiresCarry))return false;
            int ei=Array.FindIndex(content.enemies,e=>e.lootAction==a.id);
            return (ei<0 || s.data.enemies[ei].health==0 && s.data.enemies[ei].loot) && OpportunityEnabled(s,a) && (a.tagInputs.Length==0 || TryInputs(s,a,out _));
        }
        bool CanUse(State s,int i,float x,float z,Func<int,bool> visible)
        {
            if(i<0||i>=content.actions.Length||!Enabled(s,i))return false;
            var a=content.actions[i]; int ti=Array.FindIndex(content.targets,t=>t.id==a.target); var t=content.targets[ti];var point=TargetPoint(s,ti);
            return Meets(s.flags,t.all,t.none,Array.Empty<string>(),0) && OpportunityTargetVisible(s,ti) && Distance(x,z,point.X,point.Z)<=2.3f && (visible==null||visible(ti)) &&
                (string.IsNullOrEmpty(a.tool)||Count(s,a.tool)>0) && TryInputs(s,a,out _) && OpportunityCanUse(s,a,x,z);
        }
        void StartAction(int i,float x,float z,Func<int,bool> visible)
        {
            if(!CanUse(draft,i,x,z,visible)) {Say("Cannot do that here yet. Check the objective, reach, tool and materials.");return;}
            var a=content.actions[i];draft.attack=-1;
            if(a.ticks==0) {draft.channel=-1;Apply(i);} else {draft.channel=i;draft.remaining=a.ticks;draft.originX=x;draft.originZ=z; if(a.kind!="enter")Say(a.label+"...");}
        }
        void Apply(int i)
        {
            var a=content.actions[i];
            if(!TryInputs(draft,a,out var inputs)){Say("Action rejected: missing required inputs.");return;}
            var counterChanges=new Dictionary<string,int>(StringComparer.Ordinal);
            foreach(var effect in a.counterEffects)
            {
                if(!counterChanges.TryGetValue(effect.id,out int prior))prior=draft.data.counters.First(c=>c.id==effect.id).count;
                long next=(long)prior+effect.amount;
                if(next>int.MaxValue){Say("Action rejected: counter overflow.");return;}
                counterChanges[effect.id]=(int)next;
            }
            var outputs=a.outputs.Concat(a.conditionalOutputs.Where(v=>Meets(draft.flags,v.all,v.none,Array.Empty<string>(),0)).Select(v=>new ItemAmount(v.id,v.count))).ToArray();
            var deltas=new List<(string key,int delta)>();
            deltas.AddRange(inputs.Select(v=>(v.id,-v.count))); deltas.AddRange(outputs.Select(v=>(v.id,v.count)));
            foreach(var item in a.removeItems) {int n=Count(draft,item);if(n>0)deltas.Add((item,-n));}
            string reason;
            if(a.kind=="gather")
            {
                int node=content.targets.First(t=>t.id==a.target).nodeInstanceId;
                if(!GameplayEconomyAdapter.TryGather(a,content,draft.inventory,node,true,out reason)){Say("Gather rejected: "+reason);return;}
            }
            bool changed=a.kind=="craft" ? GameplayEconomyAdapter.TryCraft(a,content,draft.inventory,outputs,true,out reason,inputs) : draft.inventory.TryApplyDeltasAtomic(1,deltas,out reason);
            if(!changed) {Say("Action rejected: "+reason);return;}
            foreach(var change in counterChanges)draft.data.counters.First(c=>c.id==change.Key).count=change.Value;
            ApplyOpportunity(a);
            foreach(var f in a.flags)draft.flags.Add(f);if(!string.IsNullOrEmpty(a.once))draft.flags.Add(a.once);
            if(!string.IsNullOrEmpty(a.carry))draft.carry=a.carry=="-"?"":a.carry;
            if(a.xp>0){var xp=draft.data.xp.First(v=>v.id==a.skill);xp.count=(int)Math.Min(5000000L,(long)xp.count+a.xp);}
            int ei=Array.FindIndex(content.enemies,e=>e.lootAction==a.id);if(ei>=0)draft.data.enemies[ei].loot=false;
            if(a.kind=="consume") foreach(var v in a.inputs) draft.data.health=Math.Min(content.tuning.health,draft.data.health+content.items.First(d=>d.id==v.id).heal);
            draft.data.actions[i].cooldown=a.cooldown; if(!string.IsNullOrEmpty(a.text))Say(a.text);
        }
        void Consume(int i)
        {
            if(i<0||i>=content.items.Length)return;var item=content.items[i];
            if(item.heal<=0||draft.data.health>=content.tuning.health||Count(draft,item.id)<=0) {Say("No healing food needed or available.");return;}
            if(draft.inventory.TryApplyDeltasAtomic(1,new[]{(item.id,-1)},out _)) {draft.data.health=Math.Min(content.tuning.health,draft.data.health+item.heal);Say("Ate "+item.name+".");}
        }
        void Combat(float x,float z,Func<int,bool> visible)
        {
            if(draft.attackWait>0)draft.attackWait--;
            if(draft.attack>=0)
            {
                int i=draft.attack;var e=draft.data.enemies[i];var def=content.enemies[i];int ti=Array.FindIndex(content.targets,t=>t.id==def.target);var target=content.targets[ti];
                if(e.health<=0||!EnemyActive(draft,i))draft.attack=-1;
                // Attack reach must stay inside enemy initiation range: an anchored
                // encounter must never expose a safe player-only damage annulus.
                else if(draft.attackWait<=0 && EnemyWithinBoundary(def,x,z) && Distance(x,z,target.x,target.z)<=Math.Min(1.65f,def.range) && (visible==null||visible(ti)) && GameplayCombatAdapter.ResolveAttack(preparedTick,1,i+2))
                {
                    int damage=Math.Min(e.health,content.tuning.damage);e.health-=damage;draft.attackWait=content.tuning.attackTicks;
                    var xp=draft.data.xp.FirstOrDefault(v=>v.id=="melee");if(xp!=null)xp.count=Math.Min(5000000,xp.count+damage);
                    Say(target.name+" takes "+damage+" damage.");
                    if(e.health==0) {e.windup=0;e.loot=!string.IsNullOrEmpty(def.lootAction);e.respawn=def.respawn;draft.flags.Add(def.killFlag);draft.attack=-1;Say(target.name+" defeated.");}
                }
            }
            for(int i=0;i<content.enemies.Length;i++)
            {
                var def=content.enemies[i];var e=draft.data.enemies[i];if(e.health<=0||!EnemyActive(draft,i))continue;
                if(!EnemyWithinBoundary(def,x,z)){e.windup=0;continue;}
                int ti=Array.FindIndex(content.targets,t=>t.id==def.target);var t=content.targets[ti];float distance=Distance(x,z,t.x,t.z);
                if(distance>def.leash){e.windup=0;continue;}
                if(e.cooldown>0)e.cooldown--;
                if(e.windup>0)
                {
                    if(--e.windup==0)
                    {
                        bool hit=Distance(x,z,e.aimX,e.aimZ)<=.75f && distance<=def.range+.8f && (visible==null||visible(ti));
                        if(hit && GameplayCombatAdapter.ResolveAttack(preparedTick,i+2,1)){draft.data.health-=def.damage;draft.channel=-1;Say(t.name+" hits for "+def.damage+".");} else Say(t.name+" misses. The ground strike is exposed.");
                        e.cooldown=def.cooldown;
                    }
                }
                else if(e.cooldown==0 && distance<=def.range && (visible==null||visible(ti))) {e.windup=def.windup;e.aimX=x;e.aimZ=z;}
            }
        }
        void Hazards(float x,float z)
        {
            for(int i=0;i<content.hazards.Length;i++)
            {
                var h=content.hazards[i];var state=draft.data.hazards[i];if(draft.flags.Contains(h.once))continue;
                var t=content.targets.First(target=>target.id==h.target);
                if(state.remaining>0)
                {
                    if(--state.remaining==0)
                    {
                        draft.flags.Add(h.once);
                        if(Distance(x,z,t.x,t.z)<=h.radius)
                        {
                            draft.data.health-=h.damage;draft.channel=-1;
                            float dx=x-t.x,dz=z-t.z;float length=Distance(x,z,t.x,t.z);
                            if(length<.001f){dx=1;dz=0;length=1;}
                            PendingPushX+=dx/length*h.pushDistance;PendingPushZ+=dz/length*h.pushDistance;
                            Say(t.name+" swings through the marked ground. You take "+h.damage+" damage.");
                        }
                        else Say(t.name+" falls clear of you.");
                    }
                }
                else if(Meets(draft.flags,h.all,h.none,Array.Empty<string>(),0))state.remaining=h.windup;
            }
        }
        bool EnemyActive(State s,int i)=>Meets(s.flags,content.enemies[i].all,content.enemies[i].none,Array.Empty<string>(),0);
        static bool Meets(HashSet<string> flags,string[] all,string[] none,string[] any,int count)=>all.All(flags.Contains)&&!none.Any(flags.Contains)&&any.Count(flags.Contains)>=count;
        static bool StageSatisfied(HashSet<string> flags,ItemAmount[] counters,StageDefinition stage)=>Meets(flags,stage.all,Array.Empty<string>(),stage.any,stage.anyCount) && stage.counterRequirements.All(r=>counters.First(c=>c.id==r.id).count>=r.min);
        static float Distance(float x,float z,float xx,float zz)=>(float)Math.Sqrt((x-xx)*(x-xx)+(z-zz)*(z-zz));
        static int Count(State s,string id) {foreach(var i in s.inventory.DebugEnumerate(1))if(i.Key==id)return i.Value;return 0;}
        void Say(string text){draftFeedback=text;}
        GameplaySave Copy(State s) {var copy=Clone(s.data);copy.flags=s.flags.OrderBy(f=>f,StringComparer.Ordinal).ToArray();copy.items=s.inventory.DebugEnumerate(1).OrderBy(v=>v.Key,StringComparer.Ordinal).Select(v=>new ItemAmount(v.Key,v.Value)).ToArray();return copy;}
        static EnemyProgress CloneEnemy(EnemyProgress e)=>new EnemyProgress{id=e.id,health=e.health,windup=e.windup,cooldown=e.cooldown,respawn=e.respawn,loot=e.loot,aimX=e.aimX,aimZ=e.aimZ};
        static GameplaySave Clone(GameplaySave s)=>new GameplaySave {version=s.version,contentId=s.contentId,tick=s.tick,health=s.health,flags=(string[])s.flags.Clone(),items=s.items.Select(v=>new ItemAmount(v.id,v.count)).ToArray(),xp=s.xp.Select(v=>new ItemAmount(v.id,v.count)).ToArray(),quests=s.quests.Select(q=>new QuestProgress{id=q.id,stage=q.stage}).ToArray(),enemies=s.enemies.Select(CloneEnemy).ToArray(),actions=s.actions.Select(a=>new ActionProgress{id=a.id,cooldown=a.cooldown}).ToArray(),hazards=s.hazards.Select(h=>new HazardProgress{id=h.id,remaining=h.remaining}).ToArray(),flocks=s.flocks.Select(CloneFlock).ToArray(),presentations=s.presentations.Select(ClonePresentation).ToArray(),counters=s.counters.Select(c=>new ItemAmount(c.id,c.count)).ToArray()};
        sealed class State
        {
            public GameplaySave data; public HashSet<string> flags; public SimplePlayerInventoryStore inventory=new SimplePlayerInventoryStore();
            public string carry=""; public int channel=-1,remaining,attack=-1,attackWait;public float originX,originZ;
            public State(GameplaySave data) {this.data=data;flags=new HashSet<string>(data.flags,StringComparer.Ordinal);inventory.MarkWritable(1);inventory.DebugSetExact(1,data.items.Select(v=>new PersistedInventoryEntry(v.id,v.count)).ToList());}
        }
        sealed class QuestBridge : IServerAuthority,IQuestMutationGate,IPlayerLifecycleQuery,IQuestProgressionEvaluator
        {
            readonly PlayerHandle owner;readonly Func<bool> active;public bool committing;
            public QuestBridge(PlayerHandle owner,Func<bool> active){this.owner=owner;this.active=active;}
            public bool IsServerAuthoritative=>true;
            public bool CanMutateQuestsNow()=>committing;
            public bool IsPlayerActive(PlayerHandle player)=>player.Equals(owner)&&active();
            public QuestProgressionDecision Evaluate(QuestProgressionContext context)=>QuestProgressionDecision.NoChange;
        }
    }
    public enum GameplayRequestKind { Action,Attack,Consume,Cancel }
    public readonly struct GameplayRequest
    {
        public readonly GameplayRequestKind Kind; public readonly int Index;
        public GameplayRequest(GameplayRequestKind kind,int index){Kind=kind;Index=index;}
    }
}

