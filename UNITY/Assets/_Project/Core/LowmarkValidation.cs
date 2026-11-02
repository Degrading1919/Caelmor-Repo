using System;
using System.Collections.Generic;
using System.IO;
using Caelmor.Runtime.Gameplay;
using UnityEngine;

namespace Caelmor.Unity.Playable
{
    /// <summary>Actual Unity physics/NavMesh + real host queue tests. No position writes,
    /// granted test items, synthetic quest flags, or accelerated gameplay clocks.</summary>
    public static class LowmarkValidation
    {
        public static void Run(InteractionAnchor anchor,int mask,TerrainNavigation navigation)
        {
            var content=LowmarkGame.LoadContent(out var identity);
            using(var test=new Harness(content,identity,anchor,mask,navigation))
            {
                test.Act("hear_order");test.Act("hear_river");test.Act("settle");
                test.Check(test.Session.Stage(0)==2,"real NPC dialogue advances after queue consumption");
                test.Act("notch");test.Act("earth");test.Act("drag");test.Act("post_found");
                test.Go("footing");
                foreach(var id in new[]{"silt1","silt2","silt3","leech"})test.Fight(id);
                test.Act("clear");test.Act("hatchet");
                // Start a real channel, redirect movement, verify no award before retry.
                test.Go("coppice");test.Submit("stem");test.Step();
                test.Check(test.Session.ChannelAction>=0,"woodcutting starts on tick");
                var p=test.Host.Snapshot.Position;test.Host.SubmitDestination(p+Vector3.right);test.Step();
                test.Check(test.Session.ChannelAction<0 && test.Session.Quantity("marker_stem")==0,"validated movement interrupts channel without reward");
                test.Act("stem");test.Act("notch_cut");test.Act("seat");
                test.Go("footing");for(int i=0;i<105;i++)test.Step();test.Act("maelin_after");
                test.Act("proof_notches");test.Act("proof_walk");test.Act("close_crossing");
                for(int i=1;i<=3;i++){test.Act("lift"+i);test.Act("deliver"+i);}
                test.Act("trunk_lift");test.Act("trunk_set");test.Fight("boar");test.Act("uphill_done");
                test.Act("TL_EVIDENCE_PLAYER");test.Act("TL_STONE_KEPT");test.Act("quest_finish");
                test.Check(test.Session.Stage(0)==11 && test.Session.Quantity("payment")==8,"complete quest and reward through real authority bridge");
                test.Act("timber_cut");test.Fight("wild_boar");test.Act("wild_boar_harvest");test.Act("cook_meat");
                test.Check(test.Session.Quantity("dried_game_strips")==1 && test.Session.Quantity("game_meat")==0,"connected repeatable gathering hunting crafting loop");
                test.Act("BW_start");test.Act("BW_measure1");test.Act("BW_measure2");test.Act("BW_measure3");test.Act("BW_wrack");test.Go("bw_jam");
                for(int i=1;i<=5;i++)test.Fight("BW_skitter"+i);
                test.Act("BW_cut_jam");var jamPosition=test.Host.Snapshot.Position;int jamHealth=test.Session.Health;
                for(int i=0;i<18;i++)test.Step();
                test.Check(test.Session.Has("BW_JAM_SWUNG") && test.Session.Health<jamHealth && Vector3.Distance(jamPosition,test.Host.Snapshot.Position)>.4f,"authored jam hazard applies damage and collision-validated push");
                test.Act("BW_cord");test.Act("BW_repair");test.Act("BW_leaner_read");test.Act("BW_holder_read");test.Act("BW_old_read");test.Act("BW_leaner_notch");test.Act("BW_leaner_back");
                test.Host.SubmitDestination(test.Host.Snapshot.Position+Vector3.forward*2);for(int i=0;i<25;i++)test.Step();
                test.Check(test.Session.Has("BW_LEANER_FALLEN"),"felling resolves into persistent world state");
                test.Act("BW_build");test.Act("BW_give_wood");test.Act("BW_stage1");test.Act("BW_stage2");test.Act("BW_finish");
                test.Check(test.Session.Stage(1)==6 && test.Session.Quantity("payment")==12,"second authored quest completes through reusable runtime");
                test.Kitchen();
                var save=test.Session.Capture();var path=Path.Combine(Path.GetTempPath(),"Caelmor-Unity-Checkpoint-"+Guid.NewGuid().ToString("N")+".json");
                var disk=new AtomicTextCheckpoint(path);
                disk.Write(JsonUtility.ToJson(save),raw=>test.Session.ValidateSave(JsonUtility.FromJson<GameplaySave>(raw)));
                using(var restored=new Harness(content,identity,anchor,mask,navigation))
                {
                    restored.Session.Restore(JsonUtility.FromJson<GameplaySave>(disk.Read(raw=>restored.Session.ValidateSave(JsonUtility.FromJson<GameplaySave>(raw)))));
                    restored.Check(restored.Session.Stage(0)==11 && restored.Session.Stage(1)==6 && restored.Session.Stage(2)==7 && restored.Session.Quantity("payment")==16 && restored.Session.Quantity("fowl_stew")==3,"actual JsonUtility and disk checkpoint restore for three connected quests");
                    for(int i=0;i<content.presentationEvents.Length;i++)restored.Check(restored.Session.Presentation(i).remaining==0,"restoration never replays a quiet presentation");
                    restored.Act("marker_read");
                    restored.Host.SuspendForValidation(true);long before=restored.Session.Capture().tick;restored.Step();
                    restored.Check(restored.Session.Capture().tick==before,"suspended lifecycle blocks gameplay execution and publication");
                }
            }
            Debug.Log("CAELMOR_LOWMARK_PASSED: real host commands, connected NavMesh hubs, True Line, Bank Walk and Flood Kitchen completion, melee/dodge, flock scatter/noncombat recovery, closed nesting ground, tagged meals, quiet water state, hazards/validated push, repeatable economy, disk restore and lifecycle gates");
        }
        sealed class Harness : IDisposable
        {
            public readonly PlayableHost Host;public readonly GameplaySession Session;
            readonly GameplayContent content;readonly int mask;readonly InteractionAnchor anchorForRestore;readonly TerrainNavigation navigationForRestore;readonly List<GameplayRequest> requests=new List<GameplayRequest>();Vector3 position;
            public Harness(GameplayContent content,string identity,InteractionAnchor anchor,int mask,TerrainNavigation navigation)
            {
                this.content=content;this.mask=mask;anchorForRestore=anchor;navigationForRestore=navigation;Host=new PlayableHost(new Vector3(0,0,-4),anchor,mask,navigation);
                Session=new GameplaySession(content,identity,Host.GameplayPlayer,()=>Host.IsReady);
                Host.GameplayCommandConsumed+=(kind,index,option)=>requests.Add(new GameplayRequest((GameplayRequestKind)kind,index));
                Host.GameplayPreparing+=(tick,p,sprint)=>{position=p;Session.PrepareTick(tick,p.x,p.z,requests,Sight,sprint);requests.Clear();if(Session.PendingPushX!=0 || Session.PendingPushZ!=0)Host.DisplaceDuringExecution(new Vector3(Session.PendingPushX,0,Session.PendingPushZ));if(Session.PendingRespawn)Host.RespawnDuringExecution(new Vector3(Session.PendingRespawnX,0,Session.PendingRespawnZ));};
                Host.GameplayCommitting+=Session.CommitTick;Host.GameplayAborted+=Session.AbortTick;
                Host.SnapshotCommitted+=snapshot=>Check(Session.Capture().tick==snapshot.Tick,"gameplay committed before movement snapshot publishes");
            }
            bool Sight(int ti){var t=Session.CurrentTargetPosition(ti);return !Physics.Linecast(position+Vector3.up,new Vector3(t.X,1,t.Z),mask,QueryTriggerInteraction.Ignore);}
            public void Step()=>Host.Step();
            public void Check(bool ok,string message){if(!ok)throw new InvalidOperationException("LOWMARK: "+message+"; stage="+Session.Stage(0)+" hp="+Session.Health+" position="+Host.Snapshot.Position+" feedback="+Session.Feedback);}
            public void Go(string target)=>Move(content.targets[Array.FindIndex(content.targets,t=>t.id==target)]);
            void Move(TargetDefinition t,float offset=0)
            {
                var target=Session.CurrentTargetPosition(Array.IndexOf(content.targets,t));
                var point=new Vector3(target.X+offset,0,target.Z);
                MovePoint(point);
            }
            void MovePoint(Vector3 point,bool sprint=false)
            {
                Check(Host.SubmitDestination(point),"destination enqueued "+point);Host.SubmitSprint(sprint);Step();
                for(int i=0;i<1500 && Host.Snapshot.HasDestination;i++){Host.SubmitSprint(sprint);Step();}
                Check(Vector3.Distance(Host.Snapshot.Position,point)<.1f,"reached navigable destination "+point);
            }
            public void Kitchen()
            {
                Go("fk_shelter");Act("FK_start");
                for(int i=1;i<=2;i++){Act("FK_lift"+i);Act("FK_deposit"+i);}
                Act("FK_light_fire");Check(Session.Stage(2)==2,"crate fuel enables the shelter hearth");
                var definition=content.flocks[0];int ti=Array.FindIndex(content.targets,t=>t.id==definition.target);
                var home=Session.CurrentTargetPosition(ti);
                MovePoint(new Vector3(home.X,0,home.Z),true);
                for(int i=0;i<18;i++)Step();
                var alternate=Session.CurrentTargetPosition(ti);
                Check(Session.Flock(0).positionIndex==1 && Vector3.Distance(new Vector3(home.X,0,home.Z),new Vector3(alternate.X,0,alternate.Z))>3,"rushing/unprepared approach scatters the flock to another navigable point");
                Act("FK_prepare");MovePoint(new Vector3(alternate.X-2.6f,0,alternate.Z));
                Host.SubmitDestination(Host.Snapshot.Position+Vector3.right*.2f);Host.SubmitSprint(true);Step();
                Check(!Host.Snapshot.HasDestination && !Host.Snapshot.Sprinting && Session.Flock(0).warning>0,"a sprint arrival still carries authoritative movement noise after presentation becomes idle");
                Act("FK_prepare");Go(definition.closedTarget);int before=Session.Quantity("raw_fowl");Submit("FK_resolve");Step();
                Check(Session.Quantity("raw_fowl")==before && !Session.Flock(0).recoveryPending,"closed nesting ground cannot produce Hunting rewards");
                Go(definition.coverTarget);int health=Session.Health;for(int i=0;i<35;i++)Step();Check(Session.Health==health,"nesting defenders stop after leaving their boundary");
                Recover("FK_recover1");Recover("FK_recover2");
                Check(Session.Stage(2)==3 && Session.Quantity("raw_fowl")==2,"only two recoveries complete Hunting objective");
                using(var alternative=new Harness(content,Session.Capture().contentId,anchorForRestore,mask,navigationForRestore))
                {
                    alternative.Session.Restore(JsonUtility.FromJson<GameplaySave>(JsonUtility.ToJson(Session.Capture())));
                    alternative.Act("FK_cook_repeat");
                    alternative.Check(alternative.Session.Counter("fk_portions_cooked")==2 && alternative.Session.Stage(2)==3,"public Cooking contributes actual portions to generic objective progress");
                    alternative.Act("timber_cut");alternative.Act("FK_cook_repeat");
                    alternative.Check(alternative.Session.Counter("fk_portions_cooked")==4 && alternative.Session.Stage(2)==4 && !alternative.Session.Has("FK_cook_batch"),"two public cooks complete the same objective without Nan's fixed batch");
                }
                Act("FK_cook_batch");int hush=Array.FindIndex(content.presentationEvents,p=>p.triggerFlag=="FK_HUSH_SEEN");
                Check(Session.Presentation(hush).seen && Session.Presentation(hush).remaining>0,"first pot starts committed generic hush");
                using(var restored=new Harness(content,Session.Capture().contentId,anchorForRestore,mask,navigationForRestore))
                {
                    restored.Session.Restore(JsonUtility.FromJson<GameplaySave>(JsonUtility.ToJson(Session.Capture())));
                    restored.Check(restored.Session.Presentation(hush).seen && restored.Session.Presentation(hush).remaining==0,"mid-hush restoration preserves risen water without replay");
                }
                for(int i=0;i<85;i++)Step();
                Act("FK_bottom_step");Check(Session.Feedback.Contains("No rain fell"),"latest authored early-world-state bottom-step inspect is bound");
                for(int i=1;i<=4;i++)Act("FK_feed"+i);
                Check(Session.Quantity("dried_game_strips")==0 && Session.Quantity("fowl_stew")==1,"households accept food from the earlier hunting/cooking loop");
                Act("FK_own");Act("FK_tune");Act("FK_finish_own");
                Check(Session.Stage(2)==7 && Session.Quantity("payment")==16,"third authored quest completes once with the own-food choice");
                Recover("FK_recover_repeat");Act("timber_cut");Act("FK_cook_repeat");
                Check(Session.Quantity("fowl_stew")==3 && Session.Presentation(hush).remaining==0,"public cooking and hunting remain useful without repeating the hush");
                Go("fk_deep_water");var region=content.respawnRegions[0];var safe=new Vector3(region.x,0,region.z);
                for(int i=0;i<6000 && Vector3.Distance(Host.Snapshot.Position,safe)>.1f;i++)Step();
                Check(Vector3.Distance(Host.Snapshot.Position,safe)<.1f && Session.Health==content.tuning.health && Session.Stage(2)==7 && Session.Quantity("fowl_stew")==3,"actual damage/death returns to shelter with quest and inventory retained");
            }
            void Recover(string action)
            {
                Act("FK_prepare");int before=Session.Quantity("raw_fowl");int xp=Session.Capture().xp[Array.FindIndex(content.skills,s=>s.id=="hunting")].count;
                Act("FK_resolve");Check(Session.Flock(0).recoveryPending && Session.Quantity("raw_fowl")==before,"taking is not a combat kill or inventory grant");
                Act(action);Check(!Session.Flock(0).recoveryPending && Session.Quantity("raw_fowl")==before+1 && Session.Capture().xp[Array.FindIndex(content.skills,s=>s.id=="hunting")].count==xp+28,"separate recovery grants exactly one food-only fowl and Hunting XP");
            }
            public void Submit(string id){int i=Array.FindIndex(content.actions,a=>a.id==id);Check(Host.SubmitGameplayAction(0,i),"action enqueued "+id);}
            public void Act(string id)
            {
                int i=Array.FindIndex(content.actions,a=>a.id==id);var a=content.actions[i];Go(a.target);
                Check(Session.Available(i),"action ready "+id);Submit(id);Step();
                for(int n=0;n<1000 && Session.ChannelAction>=0;n++)Step();
                Check(string.IsNullOrEmpty(a.once)||Session.Has(a.once),"action committed "+id);
            }
            public void Fight(string id)
            {
                int i=Array.FindIndex(content.enemies,e=>e.id==id);var t=content.targets[Array.FindIndex(content.targets,v=>v.id==content.enemies[i].target)];
                float side=t.x>10?-1:1;float offset=side*1.55f;
                if(id=="boar")
                {
                    Move(t,side*2.15f);int hp=Session.Enemy(i).health;
                    Host.SubmitGameplayAction(1,i);Step();for(int n=0;n<25;n++)Step();
                    Check(Session.Enemy(i).health==hp,"old safe annulus cannot deal melee damage");
                }
                Move(t,offset);int before=Session.Health;bool damaged=false,dodged=false;
                Host.SubmitGameplayAction(1,i);Step();
                for(int n=0;n<1800 && Session.Enemy(i).health>0;n++)
                {
                    if(Session.Health<before)damaged=true;
                    var enemy=Session.Enemy(i);
                    if(enemy.windup>0 && (id!="boar" || damaged))
                    {
                        int health=Session.Health;
                        // A real destination command moves the capsule off the telegraph.
                        // No test position writes or client-side combat decisions.
                        Move(t,offset+side*1.05f);
                        while(Session.Enemy(i).windup>0)Step();
                        if(id=="boar" && !dodged)
                        {
                            Check(Session.Health==health,"real navigation dodges committed boar tell");
                            Check(Session.Enemy(i).cooldown>0,"missed boar attack has recovery");dodged=true;
                        }
                        Move(t,offset);
                    }
                    Step();
                }
                if(id=="boar")Check(damaged && dodged,"required boar combat proved damage and movement dodge");
                Check(Session.Enemy(i).health==0,"enemy defeated "+id);
            }
            public void Dispose()=>Host.Dispose();
        }
    }
}
