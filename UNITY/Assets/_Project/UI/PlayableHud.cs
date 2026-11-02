using System;
using UnityEngine;

namespace Caelmor.Unity.Playable
{
    public sealed class PlayableHud : MonoBehaviour
    {
        public PlayableBootstrap game;
        GUIStyle title,label,small;
        bool inventory;
        Vector2 dialogueScroll,actionScroll,inventoryScroll,journalScroll;
        internal static bool BlocksPointer(PlayableBootstrap game,Vector2 screen)
        {
            if(game.HelpOpen)return true;
            if(game.Lowmark!=null && game.Lowmark.QuietPresentation)return false;
            float scale=Mathf.Min(Screen.width/1280f,Screen.height/720f);
            var p=new Vector2((screen.x-(Screen.width-1280*scale)/2)/scale,(Screen.height-screen.y-(Screen.height-720*scale)/2)/scale);
            return new Rect(24,24,405,108).Contains(p)||new Rect(946,24,310,648).Contains(p)||new Rect(24,480,902,192).Contains(p)||new Rect(24,680,1232,32).Contains(p);
        }
        void Update(){if(!Application.isBatchMode && Input.GetKeyDown(KeyCode.I))inventory=!inventory;}
        void OnGUI()
        {
            if(game?.Lowmark!=null && game.Lowmark.QuietPresentation)return;
            Styles();float scale=Mathf.Min(Screen.width/1280f,Screen.height/720f);
            GUI.matrix=Matrix4x4.TRS(new Vector3((Screen.width-1280*scale)/2,(Screen.height-720*scale)/2),Quaternion.identity,Vector3.one*scale);
            if(game?.Host==null || game.StartupFailure!=null || game.Lowmark?.Session==null){GUI.Label(new Rect(30,30,1200,600),"Could not start Caelmor.\n"+game?.StartupFailure,label);return;}
            var rpg=game.Lowmark;var session=rpg.Session;var content=rpg.Content;
            GUI.Box(new Rect(24,24,405,108),"");
            GUI.Label(new Rect(38,31,380,30),"CAELMOR  /  LOWMARK",title);
            GUI.Label(new Rect(38,65,380,24),"Health "+session.Health+" / "+content.tuning.health+(session.Carry.Length>0?"    Carrying: "+session.Carry:""),label);
            GUI.Label(new Rect(38,95,380,24),session.ChannelAction>=0?content.actions[session.ChannelAction].label+"  "+(session.ChannelRemaining/10f).ToString("F1")+"s":rpg.LocationLabel,small);
            GUI.Box(new Rect(946,24,310,210),"");
            GUI.Label(new Rect(962,38,280,30),inventory?"PACK & SKILLS":"JOURNAL",title);
            if(GUI.Button(new Rect(962,190,135,30),inventory?"Journal [I]":"Pack [I]"))inventory=!inventory;
            if(GUI.Button(new Rect(1104,190,132,30),"Controls")){game.Host.ClearPendingInput();ToggleHelp();}
            if(!inventory)
            {
                GUILayout.BeginArea(new Rect(962,75,278,110));journalScroll=GUILayout.BeginScrollView(journalScroll);
                for(int pass=0;pass<2;pass++)for(int i=0;i<content.quests.Length;i++)
                {
                    if(!session.QuestAvailable(i))continue;
                    int stage=session.Stage(i);bool completed=stage>=content.quests[i].stages.Length;
                    if(completed!=(pass==1))continue;
                    GUILayout.Label(content.quests[i].name,label);
                    GUILayout.Label(completed?"Completed.":content.quests[i].stages[stage].objective,small);
                    if(!completed)foreach(var requirement in content.quests[i].stages[stage].counterRequirements)GUILayout.Label(Mathf.Min(session.Counter(requirement.id),requirement.min)+" / "+requirement.min,small);
                    GUILayout.Space(5);
                }
                GUILayout.EndScrollView();GUILayout.EndArea();
            }
            else GUI.Label(new Rect(962,80,278,95),"Gather, hunt and cook useful supplies. Prepare in reed cover, then walk toward the flock. Recover downed fowl separately. Eat cooked food from your pack to restore health.",small);
            GUI.Box(new Rect(946,244,310,428),"");
            GUILayout.BeginArea(new Rect(960,255,282,404));
            if(inventory)
            {
                inventoryScroll=GUILayout.BeginScrollView(inventoryScroll);
                foreach(var item in content.items)
                {
                    int count=session.Quantity(item.id);if(count==0)continue;
                    GUILayout.Label(item.name+"  ×"+count,label);
                    if(item.heal>0 && GUILayout.Button("Eat (+"+item.heal+" health)"))game.Host.SubmitGameplayAction(2,Array.IndexOf(content.items,item));
                }
                var save=session.Capture();GUILayout.Space(12);
                for(int i=0;i<content.skills.Length;i++)GUILayout.Label(content.skills[i].name+"  Lv "+session.Level(i)+"  /  "+save.xp[i].count+" XP",small);
                GUILayout.Space(12);GUILayout.Label(rpg.CheckpointStatus,small);
                if(GUILayout.Button("Save checkpoint [F5]"))rpg.SaveCheckpoint();
                if(GUILayout.Button("Reload checkpoint [F9]"))rpg.ReloadCheckpoint();
                GUILayout.EndScrollView();
            }
            else
            {
                int selected=rpg.Selected;
                if(selected<0)GUILayout.Label("Click a person or object to see interactions. E selects something within reach.",label);
                else
                {
                    var target=content.targets[selected];GUILayout.Label(target.name,title);
                    actionScroll=GUILayout.BeginScrollView(actionScroll);
                    int flock=Array.FindIndex(content.flocks,f=>f.target==target.id||f.coverTarget==target.id||f.recoveryTarget==target.id);
                    if(flock>=0)
                    {
                        var state=session.Flock(flock);
                        GUILayout.Label(state.recoveryPending?"A bird is down. Recovery gives food and Hunting XP.":state.warning>0?"Heads up! Withdraw from the flock to avoid scattering it.":state.prepared?"Prepared. Walk calmly toward the feeding flock.":"Prepare in reed cover. Walking keeps the approach quiet; sprinting alarms the sentinel.",small);
                    }
                    int enemy=Array.FindIndex(content.enemies,e=>e.target==target.id);
                    if(enemy>=0 && session.TargetVisible(selected) && session.Enemy(enemy).health>0 && GUILayout.Button("Attack"))rpg.Attack(enemy);
                    bool any=false;
                    for(int i=0;i<content.actions.Length;i++)
                    {
                        var action=content.actions[i];if(action.target!=target.id||action.kind=="enter"||!session.Available(i))continue;
                        any=true;if(GUILayout.Button(action.label,GUILayout.MinHeight(38)))rpg.ChooseAction(i);
                    }
                    if(!any && enemy<0)GUILayout.Label("No action available. Follow the journal or investigate elsewhere.",small);
                    GUILayout.EndScrollView();
                }
            }
            GUILayout.EndArea();
            GUI.Box(new Rect(24,480,902,192),"");
            GUILayout.BeginArea(new Rect(40,492,870,165));dialogueScroll=GUILayout.BeginScrollView(dialogueScroll);GUILayout.Label(rpg.Dialogue.Length>0?rpg.Dialogue:session.Feedback,label);GUILayout.EndScrollView();GUILayout.EndArea();
            GUI.Label(new Rect(24,680,1230,30),"LMB: move / select    E: nearby interaction    Shift: sprint    RMB: orbit    Wheel: zoom    I: pack    F5/F9: checkpoint    Esc: stop / help",small);
            if(game.HelpOpen)
            {
                GUI.Box(new Rect(280,150,650,310),"");GUI.Label(new Rect(300,170,610,34),"Whisperflow Landing",title);
                GUI.Label(new Rect(300,215,610,180),"Click terrain to walk around obstacles. Click an actor or prop, then choose an action; you approach automatically.\nMove away from orange ground tells to dodge attacks. Move during a channel to cancel it without spending resources.\nUse your pack to eat. F5 saves an explicit checkpoint; F9 reloads at the road head. Channels and carries are cleared.\nF3 enables optional WASD debugging. Host simulation: 10 Hz.",label);
                if(GUI.Button(new Rect(300,410,180,32),"Quit application"))Application.Quit();
            }
        }
        void ToggleHelp(){game.SendMessage("ToggleHelpFromHud",SendMessageOptions.RequireReceiver);}
        void Styles()
        {
            if(title!=null)return;
            title=new GUIStyle(GUI.skin.label){fontSize=20,fontStyle=FontStyle.Bold,wordWrap=true,normal={textColor=new Color(.92f,.86f,.7f)}};
            label=new GUIStyle(GUI.skin.label){fontSize=16,wordWrap=true,normal={textColor=new Color(.94f,.94f,.9f)}};
            small=new GUIStyle(label){fontSize=13,normal={textColor=new Color(.74f,.8f,.78f)}};
            GUI.skin.button.wordWrap=true;GUI.skin.button.fontSize=14;
        }
    }
}
