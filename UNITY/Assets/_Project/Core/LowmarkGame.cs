using System;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using Caelmor.Runtime.Gameplay;
using UnityEngine;

namespace Caelmor.Unity.Playable
{
    /// <summary>Unity composition/presentation only. UI submits numeric intentions through
    /// the existing authoritative command queue. All state decisions belong to GameplaySession.</summary>
    public sealed class LowmarkGame : MonoBehaviour
    {
        public PlayableBootstrap Game { get; private set; }
        public GameplayContent Content { get; private set; }
        public GameplaySession Session { get; private set; }
        public string ContentIdentity { get; private set; }
        public int Selected { get; private set; } = -1;
        public string CheckpointStatus { get; private set; } = "F5: save checkpoint. F9: reload checkpoint (restarts at road head).";
        readonly List<GameplayRequest> requests = new List<GameplayRequest>();
        readonly List<GameObject> views = new List<GameObject>();
        readonly List<GameObject> warnings = new List<GameObject>();
        readonly List<TextMesh> labels = new List<TextMesh>();
        readonly List<Material> materials = new List<Material>();
        readonly List<GameObject> hazardViews = new List<GameObject>();
        int pendingAction=-1, pendingEnemy=-1;
        AtomicTextCheckpoint checkpoint;
        Vector3 preparingPosition;
        long discoveryStarted=-1;
        bool hadDiscovery;
        GameObject water;
        public bool DiscoveryQuiet => discoveryStarted>=0 && Game.Host.Snapshot.Tick-discoveryStarted<100;
        public string Dialogue { get; private set; } = "";
        public static string CheckpointPath => Path.Combine(Application.persistentDataPath,"lowmark-gameplay.checkpoint.json");
        public static GameplayContent LoadContent(out string identity)
        {
            var asset=Resources.Load<TextAsset>("LowmarkGameplay");
            if(asset==null)throw new InvalidOperationException("Lowmark gameplay content was not staged. Run UNITY/Build.ps1.");
            using(var hash=SHA256.Create()) identity="lowmark_playable:"+BitConverter.ToString(hash.ComputeHash(Encoding.UTF8.GetBytes(asset.text))).Replace("-","");
            var content=JsonUtility.FromJson<GameplayContent>(asset.text);content.Validate();return content;
        }
        public void Initialize(PlayableBootstrap game)
        {
            Game=game;Content=LoadContent(out var identity);ContentIdentity=identity;
            checkpoint=new AtomicTextCheckpoint(CheckpointPath);
            Session=NewSession();
            game.Host.GameplayCommandConsumed+=Consume;
            game.Host.GameplayPreparing+=Prepare;
            game.Host.GameplayCommitting+=Commit;
            game.Host.GameplayAborted+=Abort;
            game.Host.InputCleared+=Clear;
            CreateViews();
            foreach(var renderer in game.interactionAnchor.GetComponentsInChildren<Renderer>())renderer.enabled=false;
        }
        GameplaySession NewSession()=>new GameplaySession(Content,ContentIdentity,Game.Host.GameplayPlayer,()=>Game.Host.IsReady);
        void Consume(int action,int target,int option)
        {
            if(action>=0 && action<=3)requests.Add(new GameplayRequest((GameplayRequestKind)action,target));
        }
        void Prepare(long tick,Vector3 position)
        {
            preparingPosition=position;
            Session.PrepareTick(tick,position.x,position.z,requests,HasSight);requests.Clear();
            if(Session.PendingPushX!=0 || Session.PendingPushZ!=0)Game.Host.DisplaceDuringExecution(new Vector3(Session.PendingPushX,0,Session.PendingPushZ));
            if(Session.PendingRespawn)Game.Host.RespawnDuringExecution(new Vector3(Content.tuning.respawnX,0,Content.tuning.respawnZ));
        }
        bool HasSight(int ti)
        {
            var t=Content.targets[ti];
            return !Physics.Linecast(preparingPosition+Vector3.up,new Vector3(t.x,1,t.z),Game.solidLayerMask,QueryTriggerInteraction.Ignore);
        }
        void Commit(long tick)
        {
            Session.CommitTick(tick);
            if(!string.IsNullOrEmpty(Session.Feedback)) Dialogue=Session.Feedback;
            // Discovery presentation is triggered only by the committed edge, never hydration.
            if(!hadDiscovery && Session.Has("discovery"))discoveryStarted=tick;
            hadDiscovery=Session.Has("discovery");
        }
        void Abort(){requests.Clear();Session.AbortTick();}
        void Clear(){requests.Clear();pendingAction=-1;pendingEnemy=-1;Session?.ClearTransient();}
        public void ChooseAction(int index)
        {
            if(Game.HelpOpen || DiscoveryQuiet || !Session.Available(index))return;
            pendingEnemy=-1;pendingAction=index;
            Approach(Array.FindIndex(Content.targets,t=>t.id==Content.actions[index].target));
        }
        public void Attack(int index)
        {
            if(Game.HelpOpen || DiscoveryQuiet)return;
            pendingAction=-1;pendingEnemy=index;
            Approach(Array.FindIndex(Content.targets,t=>t.id==Content.enemies[index].target));
        }
        void Approach(int target)
        {
            var t=Content.targets[target];var position=Game.Host.Snapshot.Position;var center=new Vector3(t.x,0,t.z);
            if(Vector3.Distance(position,center)>1.5f)
            {
                var point=center+(position-center).normalized*1.15f;
                Game.Host.SubmitDestination(point);
            }
            else if(Game.Host.Snapshot.HasDestination)Game.Host.SubmitDestination(position);
        }
        public void InteractNearest()
        {
            float best=2.5f;int index=-1;
            for(int i=0;i<Content.targets.Length;i++)
            {
                if(!Session.TargetVisible(i))continue;
                var t=Content.targets[i];float d=Vector3.Distance(Game.Host.Snapshot.Position,new Vector3(t.x,0,t.z));
                if(d<best && Array.Exists(Content.actions,a=>a.target==t.id && a.kind!="enter" && Session.Available(Array.IndexOf(Content.actions,a)))){best=d;index=i;}
            }
            if(index>=0)Selected=index;
        }
        public bool TrySelect(Ray ray)
        {
            if(!Physics.Raycast(ray,out var hit,250,1<<9,QueryTriggerInteraction.Collide))return false;
            var selection=hit.collider.GetComponent<LowmarkSelection>();
            if(selection==null)return false;
            Selected=selection.Index;pendingAction=-1;pendingEnemy=-1;return true;
        }
        public void CancelApproach(){pendingAction=-1;pendingEnemy=-1;}
        void Update()
        {
            if(Session==null)return;
            if(Input.GetKeyDown(KeyCode.F5))SaveCheckpoint();
            if(Input.GetKeyDown(KeyCode.F9))ReloadCheckpoint();
            if(Game.HelpOpen || DiscoveryQuiet || !Game.Host.IsReady)return;
            int ti=-1;
            if(pendingAction>=0)ti=Array.FindIndex(Content.targets,t=>t.id==Content.actions[pendingAction].target);
            if(pendingEnemy>=0)ti=Array.FindIndex(Content.targets,t=>t.id==Content.enemies[pendingEnemy].target);
            if(ti>=0)
            {
                var t=Content.targets[ti];var p=Game.Host.Snapshot.Position;
                if(Vector3.Distance(p,new Vector3(t.x,0,t.z))<=2.2f && !Game.Host.Snapshot.HasDestination)
                {
                    Game.Host.SubmitGameplayAction(pendingAction>=0?0:1,pendingAction>=0?pendingAction:pendingEnemy);
                    pendingAction=pendingEnemy=-1;
                }
            }
        }
        public void SaveCheckpoint()
        {
            try
            {
                if(!Game.Host.IsReady)throw new InvalidOperationException("Host is not ready.");
                var text=JsonUtility.ToJson(Session.Capture(),true);
                checkpoint.Write(text,ValidateCheckpoint);CheckpointStatus="Checkpoint saved: "+CheckpointPath;
            }
            catch(Exception e){CheckpointStatus="Save failed: "+e.Message;Debug.LogError(CheckpointStatus);}
        }
        void ValidateCheckpoint(string text)=>Session.ValidateSave(JsonUtility.FromJson<GameplaySave>(text));
        public void ReloadCheckpoint()
        {
            try
            {
                if(!checkpoint.Exists)throw new InvalidOperationException("No checkpoint exists.");
                var text=checkpoint.Read(ValidateCheckpoint);
                // A fresh runtime composition prevents stale coarse quest states or commands.
                PlayerPrefs.SetInt("Caelmor.LoadGameplayCheckpoint",1);PlayerPrefs.Save();
                Game.Host.ClearPendingInput();UnityEngine.SceneManagement.SceneManager.LoadScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene().buildIndex);
            }
            catch(Exception e){CheckpointStatus="Load failed; current game retained: "+e.Message;Debug.LogError(CheckpointStatus);}
        }
        public void ApplyRequestedCheckpoint()
        {
            if(PlayerPrefs.GetInt("Caelmor.LoadGameplayCheckpoint",0)!=1)return;
            PlayerPrefs.DeleteKey("Caelmor.LoadGameplayCheckpoint");
            try {var text=checkpoint.Read(ValidateCheckpoint);Session.Restore(JsonUtility.FromJson<GameplaySave>(text));hadDiscovery=Session.Has("discovery");Dialogue=Session.Feedback;CheckpointStatus="Checkpoint restored at road head.";}
            catch(Exception e){CheckpointStatus="Checkpoint rejected; fresh game started: "+e.Message;Debug.LogError(CheckpointStatus);}
        }
        void CreateViews()
        {
            foreach(var t in Content.targets)
            {
                var go=GameObject.CreatePrimitive(t.kind=="npc"?PrimitiveType.Capsule:t.kind=="enemy"?PrimitiveType.Sphere:PrimitiveType.Cube);
                go.name=t.name;go.layer=9;go.transform.position=new Vector3(t.x,t.kind=="npc"?.85f:.45f,t.z);
                go.transform.localScale=t.kind=="npc"?new Vector3(.6f,.85f,.6f):t.kind=="tree"?new Vector3(.6f,2,.6f):new Vector3(.7f,.7f,.7f);
                go.GetComponent<Collider>().isTrigger=true;go.AddComponent<LowmarkSelection>().Index=views.Count;
                var mat=new Material(Shader.Find("Standard"));materials.Add(mat);mat.color=t.kind=="enemy"?new Color(.52f,.27f,.2f):t.kind=="npc"?new Color(.48f,.57f,.48f):t.kind=="tree"?new Color(.27f,.45f,.23f):new Color(.60f,.51f,.31f);go.GetComponent<Renderer>().sharedMaterial=mat;
                views.Add(go);
                var label=new GameObject("Name").AddComponent<TextMesh>();label.transform.position=new Vector3(t.x,2.1f,t.z);label.text=t.name;label.fontSize=48;label.characterSize=.14f;label.anchor=TextAnchor.MiddleCenter;label.color=new Color(.95f,.91f,.75f);labels.Add(label);
                var warning=GameObject.CreatePrimitive(PrimitiveType.Cylinder);warning.name="Host attack ground tell";Destroy(warning.GetComponent<Collider>());warning.transform.localScale=new Vector3(1.5f,.015f,1.5f);var wm=new Material(Shader.Find("Standard"));materials.Add(wm);wm.color=new Color(.9f,.25f,.12f);warning.GetComponent<Renderer>().sharedMaterial=wm;warning.SetActive(false);warnings.Add(warning);
            }
            water=GameObject.CreatePrimitive(PrimitiveType.Cube);water.name="Discovery / water rises along the old mark";Destroy(water.GetComponent<Collider>());water.transform.localScale=new Vector3(.08f,.01f,.65f);var waterMat=new Material(Shader.Find("Standard"));materials.Add(waterMat);waterMat.color=new Color(.45f,.8f,.84f);water.GetComponent<Renderer>().sharedMaterial=waterMat;water.SetActive(false);
            foreach(var h in Content.hazards)
            {
                var t=Array.Find(Content.targets,v=>v.id==h.target);var tell=GameObject.CreatePrimitive(PrimitiveType.Cylinder);tell.name=h.id+" / environmental ground tell";
                Destroy(tell.GetComponent<Collider>());tell.transform.position=new Vector3(t.x,.03f,t.z);tell.transform.localScale=new Vector3(h.radius*2,.015f,h.radius*2);
                var mat=new Material(Shader.Find("Standard"));materials.Add(mat);mat.color=new Color(.95f,.62f,.13f);tell.GetComponent<Renderer>().sharedMaterial=mat;tell.SetActive(false);hazardViews.Add(tell);
            }
        }
        void LateUpdate()
        {
            if(Session==null)return;
            for(int i=0;i<views.Count;i++)
            {
                bool active=Session.TargetVisible(i) && Content.targets[i].kind!="area";views[i].SetActive(active);
                var labelDistance=Vector3.Distance(Game.Host.Snapshot.Position,new Vector3(Content.targets[i].x,0,Content.targets[i].z));
                labels[i].gameObject.SetActive(active && !DiscoveryQuiet && (labelDistance<8 || Selected==i));
                labels[i].transform.rotation=Game.playerCamera.transform.rotation;
                var t=Content.targets[i];int ei=Array.FindIndex(Content.enemies,e=>e.target==t.id);
                if(ei>=0)
                {
                    var e=Session.Enemy(ei);var d=Content.enemies[ei];
                    views[i].transform.localScale=e.health==0?new Vector3(.8f,.18f,.8f):Vector3.one*.8f;
                    views[i].GetComponent<Renderer>().sharedMaterial.color=e.health==0?new Color(.25f,.22f,.19f):e.windup>0?new Color(.95f,.45f,.14f):new Color(.52f,.27f,.2f);
                    labels[i].text=t.name+"  "+e.health+"/"+d.health+(e.windup>0?"  WINDUP":"");
                    warnings[i].SetActive(active && e.windup>0);warnings[i].transform.position=new Vector3(e.aimX,.025f,e.aimZ);
                }
            }
            water.SetActive(DiscoveryQuiet);
            for(int i=0;i<hazardViews.Count;i++)hazardViews[i].SetActive(Session.HazardRemaining(i)>0);
            if(DiscoveryQuiet)
            {
                float seconds=(Game.Host.Snapshot.Tick-discoveryStarted)/10f;
                float height=seconds<2?0:seconds<4?(seconds-2)*.5f:seconds<8?1:Mathf.Max(0,1-(seconds-8)*.5f);
                water.transform.localScale=new Vector3(.08f,.01f+height,.65f);water.transform.position=new Vector3(-9,.5f*height,10);
            }
        }
        void OnDestroy()
        {
            if(Game!=null && Game.Host!=null){Game.Host.GameplayCommandConsumed-=Consume;Game.Host.GameplayPreparing-=Prepare;Game.Host.GameplayCommitting-=Commit;Game.Host.GameplayAborted-=Abort;Game.Host.InputCleared-=Clear;}
            foreach(var mat in materials)if(mat!=null)Destroy(mat);
            for(int i=0;i<views.Count;i++){if(views[i]!=null)Destroy(views[i]);if(warnings[i]!=null)Destroy(warnings[i]);if(labels[i]!=null)Destroy(labels[i].gameObject);}
            if(water!=null)Destroy(water);
            foreach(var view in hazardViews)if(view!=null)Destroy(view);
        }
    }
    public sealed class LowmarkSelection : MonoBehaviour {public int Index;}
}
