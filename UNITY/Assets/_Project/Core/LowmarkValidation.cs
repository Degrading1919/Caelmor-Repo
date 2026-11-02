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
                var save=test.Session.Capture();var path=Path.Combine(Path.GetTempPath(),"Caelmor-Unity-Checkpoint-"+Guid.NewGuid().ToString("N")+".json");
                var disk=new AtomicTextCheckpoint(path);
                disk.Write(JsonUtility.ToJson(save),raw=>test.Session.ValidateSave(JsonUtility.FromJson<GameplaySave>(raw)));
                using(var restored=new Harness(content,identity,anchor,mask,navigation))
                {
                    restored.Session.Restore(JsonUtility.FromJson<GameplaySave>(disk.Read(raw=>restored.Session.ValidateSave(JsonUtility.FromJson<GameplaySave>(raw)))));
                    restored.Check(restored.Session.Stage(0)==11 && restored.Session.Stage(1)==6 && restored.Session.Quantity("payment")==12 && restored.Session.Quantity("dried_game_strips")==1,"actual JsonUtility and disk checkpoint restore");
                    restored.Act("marker_read");
                    restored.Host.SuspendForValidation(true);long before=restored.Session.Capture().tick;restored.Step();
                    restored.Check(restored.Session.Capture().tick==before,"suspended lifecycle blocks gameplay execution and publication");
                }
            }
            Debug.Log("CAELMOR_LOWMARK_PASSED: real host commands, NavMesh movement, dialogue, True Line and Bank Walk completion, melee retaliation/dodge, interruption, hazards/validated push, inventory, repeatable economy, disk save/restore and lifecycle gates");
        }
        sealed class Harness : IDisposable
        {
            public readonly PlayableHost Host;public readonly GameplaySession Session;
            readonly GameplayContent content;readonly int mask;readonly List<GameplayRequest> requests=new List<GameplayRequest>();Vector3 position;
            public Harness(GameplayContent content,string identity,InteractionAnchor anchor,int mask,TerrainNavigation navigation)
            {
                this.content=content;this.mask=mask;Host=new PlayableHost(new Vector3(0,0,-4),anchor,mask,navigation);
                Session=new GameplaySession(content,identity,Host.GameplayPlayer,()=>Host.IsReady);
                Host.GameplayCommandConsumed+=(kind,index,option)=>requests.Add(new GameplayRequest((GameplayRequestKind)kind,index));
                Host.GameplayPreparing+=(tick,p)=>{position=p;Session.PrepareTick(tick,p.x,p.z,requests,Sight);requests.Clear();if(Session.PendingPushX!=0 || Session.PendingPushZ!=0)Host.DisplaceDuringExecution(new Vector3(Session.PendingPushX,0,Session.PendingPushZ));if(Session.PendingRespawn)Host.RespawnDuringExecution(new Vector3(content.tuning.respawnX,0,content.tuning.respawnZ));};
                Host.GameplayCommitting+=Session.CommitTick;Host.GameplayAborted+=Session.AbortTick;
                Host.SnapshotCommitted+=snapshot=>Check(Session.Capture().tick==snapshot.Tick,"gameplay committed before movement snapshot publishes");
            }
            bool Sight(int ti){var t=content.targets[ti];return !Physics.Linecast(position+Vector3.up,new Vector3(t.x,1,t.z),mask,QueryTriggerInteraction.Ignore);}
            public void Step()=>Host.Step();
            public void Check(bool ok,string message){if(!ok)throw new InvalidOperationException("LOWMARK: "+message+"; stage="+Session.Stage(0)+" hp="+Session.Health+" position="+Host.Snapshot.Position+" feedback="+Session.Feedback);}
            public void Go(string target)=>Move(content.targets[Array.FindIndex(content.targets,t=>t.id==target)]);
            void Move(TargetDefinition t,float offset=0)
            {
                var point=new Vector3(t.x+offset,0,t.z);
                Check(Host.SubmitDestination(point),"destination enqueued "+t.id);Step();
                for(int i=0;i<1500 && Host.Snapshot.HasDestination;i++)Step();
                Check(Vector3.Distance(Host.Snapshot.Position,point)<.1f,"reached navigable target "+t.id);
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
