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
        readonly List<GameObject> presentationViews = new List<GameObject>();
        readonly List<GameObject> boundaryViews = new List<GameObject>();
        int pendingAction=-1, pendingEnemy=-1;
        Vector3 pendingApproachTarget;
        AtomicTextCheckpoint checkpoint;
        Vector3 preparingPosition;
        public bool QuietPresentation
        {
            get
            {
                if(Session==null || Content==null)return false;
                for(int i=0;i<Content.presentationEvents.Length;i++)if(Session.Presentation(i).remaining>0)return true;
                return false;
            }
        }
        public string Dialogue { get; private set; } = "";
        public string LocationLabel
        {
            get
            {
                if(Session==null)return "Lowmark";
                var position=Game.Host.Snapshot.Position;
                foreach(var region in Content.respawnRegions)
                {
                    if(!Array.TrueForAll(region.all,Session.Has) || Array.Exists(region.none,Session.Has))continue;
                    int target=Array.FindIndex(Content.targets,t=>t.id==region.target);var center=Session.CurrentTargetPosition(target);
                    if(Vector3.Distance(position,new Vector3(center.X,0,center.Z))<=region.radius)return Content.targets[target].name;
                }
                return Content.title;
            }
        }
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
        void Prepare(long tick,Vector3 position,bool rushing)
        {
            preparingPosition=position;
            Session.PrepareTick(tick,position.x,position.z,requests,HasSight,rushing);requests.Clear();
            if(Session.PendingPushX!=0 || Session.PendingPushZ!=0)Game.Host.DisplaceDuringExecution(new Vector3(Session.PendingPushX,0,Session.PendingPushZ));
            if(Session.PendingRespawn)Game.Host.RespawnDuringExecution(new Vector3(Session.PendingRespawnX,0,Session.PendingRespawnZ));
        }
        bool HasSight(int ti)
        {
            var t=Session.CurrentTargetPosition(ti);
            return !Physics.Linecast(preparingPosition+Vector3.up,new Vector3(t.X,1,t.Z),Game.solidLayerMask,QueryTriggerInteraction.Ignore);
        }
        void Commit(long tick)
        {
            Session.CommitTick(tick);
            if(!string.IsNullOrEmpty(Session.Feedback)) Dialogue=Session.Feedback;
        }
        void Abort(){requests.Clear();Session.AbortTick();}
        void Clear(){requests.Clear();pendingAction=-1;pendingEnemy=-1;Session?.ClearTransient();}
        public void ChooseAction(int index)
        {
            if(Game.HelpOpen || QuietPresentation || !Session.Available(index))return;
            pendingEnemy=-1;pendingAction=index;
            Approach(Array.FindIndex(Content.targets,t=>t.id==Content.actions[index].target),Content.actions[index].flockOperation=="prepare"?0:1.15f);
        }
        public void Attack(int index)
        {
            if(Game.HelpOpen || QuietPresentation)return;
            pendingAction=-1;pendingEnemy=index;
            Approach(Array.FindIndex(Content.targets,t=>t.id==Content.enemies[index].target));
        }
        void Approach(int target,float standOff=1.15f)
        {
            var t=Session.CurrentTargetPosition(target);var position=Game.Host.Snapshot.Position;var center=new Vector3(t.X,0,t.Z);
            pendingApproachTarget=center;
            if(Vector3.Distance(position,center)>Mathf.Max(.1f,standOff+.35f))
            {
                var point=center+(position-center).normalized*standOff;
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
                var t=Session.CurrentTargetPosition(i);float d=Vector3.Distance(Game.Host.Snapshot.Position,new Vector3(t.X,0,t.Z));
                if(d<best && Array.Exists(Content.actions,a=>a.target==Content.targets[i].id && a.kind!="enter" && Session.Available(Array.IndexOf(Content.actions,a)))){best=d;index=i;}
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
            if(Session==null || Application.isBatchMode)return;
            if(Input.GetKeyDown(KeyCode.F5))SaveCheckpoint();
            if(Input.GetKeyDown(KeyCode.F9))ReloadCheckpoint();
            if(Game.HelpOpen || QuietPresentation || !Game.Host.IsReady)return;
            int ti=-1;
            if(pendingAction>=0)ti=Array.FindIndex(Content.targets,t=>t.id==Content.actions[pendingAction].target);
            if(pendingEnemy>=0)ti=Array.FindIndex(Content.targets,t=>t.id==Content.enemies[pendingEnemy].target);
            if(ti>=0)
            {
                var t=Session.CurrentTargetPosition(ti);var p=Game.Host.Snapshot.Position;
                var currentTarget=new Vector3(t.X,0,t.Z);
                bool preparing=pendingAction>=0 && Content.actions[pendingAction].flockOperation=="prepare";
                if(Vector3.Distance(currentTarget,pendingApproachTarget)>.1f)Approach(ti,preparing?0:1.15f);
                if(Vector3.Distance(p,currentTarget)<=(preparing?.15f:2.2f) && !Game.Host.Snapshot.HasDestination)
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
            try {var text=checkpoint.Read(ValidateCheckpoint);Session.Restore(JsonUtility.FromJson<GameplaySave>(text));Dialogue=Session.Feedback;CheckpointStatus="Checkpoint restored at road head.";}
            catch(Exception e){CheckpointStatus="Checkpoint rejected; fresh game started: "+e.Message;Debug.LogError(CheckpointStatus);}
        }
        void CreateViews()
        {
            foreach(var t in Content.targets)
            {
                var go=GameObject.CreatePrimitive(t.kind=="npc"?PrimitiveType.Capsule:t.kind=="enemy"||t.kind=="flock"?PrimitiveType.Sphere:PrimitiveType.Cube);
                go.name=t.name;go.layer=9;go.transform.position=new Vector3(t.x,t.kind=="npc"?.85f:.45f,t.z);
                go.transform.localScale=t.kind=="npc"?new Vector3(.6f,.85f,.6f):t.kind=="tree"?new Vector3(.6f,2,.6f):new Vector3(.7f,.7f,.7f);
                go.GetComponent<Collider>().isTrigger=true;go.AddComponent<LowmarkSelection>().Index=views.Count;
                var mat=new Material(Shader.Find("Standard"));materials.Add(mat);mat.color=t.kind=="enemy"?new Color(.52f,.27f,.2f):t.kind=="npc"?new Color(.48f,.57f,.48f):t.kind=="tree"?new Color(.27f,.45f,.23f):new Color(.60f,.51f,.31f);go.GetComponent<Renderer>().sharedMaterial=mat;
                views.Add(go);
                var label=new GameObject("Name").AddComponent<TextMesh>();label.transform.position=new Vector3(t.x,2.1f,t.z);label.text=t.name;label.fontSize=48;label.characterSize=.14f;label.anchor=TextAnchor.MiddleCenter;label.color=new Color(.95f,.91f,.75f);labels.Add(label);
                var warning=GameObject.CreatePrimitive(PrimitiveType.Cylinder);warning.name="Host attack ground tell";Destroy(warning.GetComponent<Collider>());warning.transform.localScale=new Vector3(1.5f,.015f,1.5f);var wm=new Material(Shader.Find("Standard"));materials.Add(wm);wm.color=new Color(.9f,.25f,.12f);warning.GetComponent<Renderer>().sharedMaterial=wm;warning.SetActive(false);warnings.Add(warning);
            }
            foreach(var presentation in Content.presentationEvents)
            {
                var water=GameObject.CreatePrimitive(PrimitiveType.Cube);water.name=presentation.id+" / committed water presentation";Destroy(water.GetComponent<Collider>());
                var waterMat=new Material(Shader.Find("Standard"));materials.Add(waterMat);waterMat.color=new Color(.45f,.8f,.84f);water.GetComponent<Renderer>().sharedMaterial=waterMat;water.SetActive(false);presentationViews.Add(water);
            }
            foreach(var h in Content.hazards)
            {
                var t=Array.Find(Content.targets,v=>v.id==h.target);var tell=GameObject.CreatePrimitive(PrimitiveType.Cylinder);tell.name=h.id+" / environmental ground tell";
                Destroy(tell.GetComponent<Collider>());tell.transform.position=new Vector3(t.x,.03f,t.z);tell.transform.localScale=new Vector3(h.radius*2,.015f,h.radius*2);
                var mat=new Material(Shader.Find("Standard"));materials.Add(mat);mat.color=new Color(.95f,.62f,.13f);tell.GetComponent<Renderer>().sharedMaterial=mat;tell.SetActive(false);hazardViews.Add(tell);
            }
            foreach(var flock in Content.flocks)
            {
                var center=Content.targets[Array.FindIndex(Content.targets,t=>t.id==flock.closedTarget)];
                var line=new GameObject(flock.id+" / closed nesting stakes").AddComponent<LineRenderer>();
                line.positionCount=33;line.startWidth=line.endWidth=.07f;line.useWorldSpace=true;
                var mat=new Material(Shader.Find("Sprites/Default"));materials.Add(mat);line.sharedMaterial=mat;line.startColor=line.endColor=new Color(.85f,.58f,.36f);
                for(int n=0;n<=32;n++){float a=n*Mathf.PI*2/32;line.SetPosition(n,new Vector3(center.x+Mathf.Cos(a)*flock.closedRadius,.06f,center.z+Mathf.Sin(a)*flock.closedRadius));}
                boundaryViews.Add(line.gameObject);
            }
        }
        void LateUpdate()
        {
            if(Session==null)return;
            for(int i=0;i<views.Count;i++)
            {
                bool active=Session.TargetVisible(i) && Content.targets[i].kind!="area";views[i].SetActive(active);
                var committed=Session.CurrentTargetPosition(i);
                var viewPosition=views[i].transform.position;viewPosition.x=committed.X;viewPosition.z=committed.Z;
                int flockIndex=Array.FindIndex(Content.flocks,f=>f.target==Content.targets[i].id);
                views[i].transform.position=flockIndex>=0?Vector3.MoveTowards(views[i].transform.position,viewPosition,Time.unscaledDeltaTime*9f):viewPosition;
                labels[i].transform.position=new Vector3(committed.X,2.1f,committed.Z);
                var labelDistance=Vector3.Distance(Game.Host.Snapshot.Position,new Vector3(committed.X,0,committed.Z));
                labels[i].gameObject.SetActive(active && !QuietPresentation && (labelDistance<8 || Selected==i));
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
                if(flockIndex>=0)
                {
                    var flock=Session.Flock(flockIndex);
                    views[i].GetComponent<Renderer>().sharedMaterial.color=flock.warning>0?new Color(.98f,.65f,.25f):new Color(.78f,.80f,.72f);
                    labels[i].text=t.name+(flock.warning>0?" / HEADS UP":flock.prepared?" / CALM APPROACH":" / FEEDING");
                }
            }
            for(int i=0;i<boundaryViews.Count;i++)boundaryViews[i].SetActive(Session.TargetVisible(Array.FindIndex(Content.targets,t=>t.id==Content.flocks[i].closedTarget)));
            for(int i=0;i<hazardViews.Count;i++)hazardViews[i].SetActive(Session.HazardRemaining(i)>0);
            for(int i=0;i<presentationViews.Count;i++)
            {
                var definition=Content.presentationEvents[i];var state=Session.Presentation(i);var water=presentationViews[i];
                water.SetActive(state.seen && (state.remaining>0 || definition.persistRise));
                float progress=Mathf.Clamp01(1-state.remaining/(float)definition.ticks);
                float shape=definition.persistRise?Mathf.Clamp01(progress/.375f):progress<.2f?0:progress<.4f?(progress-.2f)/.2f:progress<.8f?1:Mathf.Max(0,(1-progress)/.2f);
                float height=definition.rise*shape;var target=Session.CurrentTargetPosition(Array.FindIndex(Content.targets,t=>t.id==definition.target));
                water.transform.localScale=new Vector3(definition.persistRise?1.7f:.08f,.01f+height,.65f);water.transform.position=new Vector3(target.X,.5f*height,target.Z);
            }
        }
        void OnDestroy()
        {
            if(Game!=null && Game.Host!=null){Game.Host.GameplayCommandConsumed-=Consume;Game.Host.GameplayPreparing-=Prepare;Game.Host.GameplayCommitting-=Commit;Game.Host.GameplayAborted-=Abort;Game.Host.InputCleared-=Clear;}
            foreach(var mat in materials)if(mat!=null)Destroy(mat);
            for(int i=0;i<views.Count;i++){if(views[i]!=null)Destroy(views[i]);if(warnings[i]!=null)Destroy(warnings[i]);if(labels[i]!=null)Destroy(labels[i].gameObject);}
            foreach(var water in presentationViews)if(water!=null)Destroy(water);
            foreach(var view in hazardViews)if(view!=null)Destroy(view);
            foreach(var view in boundaryViews)if(view!=null)Destroy(view);
        }
    }
    public sealed class LowmarkSelection : MonoBehaviour {public int Index;}
}
