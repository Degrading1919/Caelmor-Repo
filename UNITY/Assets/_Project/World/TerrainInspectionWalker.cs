using System;
using System.Collections;
using UnityEngine;

namespace Caelmor.Unity.Inspection
{
    /// <summary>Inspection-only movement. No gameplay/save/network composition.</summary>
    [DefaultExecutionOrder(-100)]
    [RequireComponent(typeof(CharacterController))]
    public sealed class TerrainInspectionWalker : MonoBehaviour
    {
        public TerrainInspectionSurface surface;
        public Camera eye;
        public float walkSpeed=3f,sprintSpeed=5.5f;
        CharacterController controller;
        float verticalSpeed,yaw,pitch;
        bool smoke;
        void Awake()
        {
            controller=GetComponent<CharacterController>();surface.BuildGeometry();SpawnAt(0);
            smoke=Array.IndexOf(Environment.GetCommandLineArgs(),"--caelmor-terrain-smoke")>=0;
        }
        void Start(){if(smoke)StartCoroutine(Smoke());}
        public void SpawnAt(int index)
        {
            if(controller==null)controller=GetComponent<CharacterController>();surface.ReadPayload();
            index=Mathf.Clamp(index,0,surface.spawns.Count-1);var spawn=surface.spawns[index];
            controller.enabled=false;transform.position=new Vector3(spawn.point.x,surface.HeightAt(spawn.point.x,spawn.point.y)+.05f,spawn.point.y);controller.enabled=true;
            Vector2 direction=spawn.target-spawn.point;yaw=Mathf.Atan2(direction.x,direction.y)*Mathf.Rad2Deg;pitch=0;verticalSpeed=0;
            transform.rotation=Quaternion.Euler(0,yaw,0);if(eye!=null)eye.transform.localRotation=Quaternion.identity;
        }
        public void Step(Vector2 input,float delta,bool sprint)
        {
            if(controller==null)controller=GetComponent<CharacterController>();
            input=Vector2.ClampMagnitude(input,1);Vector3 horizontal=(transform.right*input.x+transform.forward*input.y)*(sprint?sprintSpeed:walkSpeed);
            if(controller.isGrounded&&verticalSpeed<0)verticalSpeed=-2;
            verticalSpeed-=9.81f*delta;controller.Move((horizontal+Vector3.up*verticalSpeed)*delta);
        }
        public void AdvanceFrame(Vector2 input,float delta,bool sprint)
        {
            float remaining=Mathf.Min(delta,1f);
            while(remaining>0){float step=Mathf.Min(.05f,remaining);Step(input,step,sprint);remaining-=step;}
        }
        void Update()
        {
            if(Application.isBatchMode)return;
            for(int i=0;i<4;i++)if(Input.GetKeyDown((KeyCode)((int)KeyCode.Alpha1+i)))SpawnAt(i);
            if(Input.GetKeyDown(KeyCode.Home))SpawnAt(0);
            if(Input.GetKeyDown(KeyCode.Alpha5)&&surface.bridges.Count>0)
            {
                var bridge=surface.bridges[0];var point=(bridge.a+bridge.b)*.5f;controller.enabled=false;transform.position=new Vector3(point.x,bridge.top+.05f,point.y);controller.enabled=true;verticalSpeed=0;
            }
            if(Input.GetMouseButtonDown(1))Cursor.lockState=CursorLockMode.Locked;
            if(Input.GetMouseButtonUp(1)||Input.GetKeyDown(KeyCode.Escape))Cursor.lockState=CursorLockMode.None;
            if(Input.GetMouseButton(1))
            {
                yaw+=Input.GetAxis("Mouse X")*2;pitch=Mathf.Clamp(pitch-Input.GetAxis("Mouse Y")*2,-75,80);
                transform.rotation=Quaternion.Euler(0,yaw,0);eye.transform.localRotation=Quaternion.Euler(pitch,0,0);
            }
            Vector2 input=new Vector2(Input.GetAxisRaw("Horizontal"),Input.GetAxisRaw("Vertical"));
            AdvanceFrame(input,Time.deltaTime,Input.GetKey(KeyCode.LeftShift));
            if(transform.position.y<10)SpawnAt(0);
        }
        void OnGUI()
        {
            if(Application.isBatchMode)return;
            GUI.Box(new Rect(10,10,740,142),"Lowmark terrain walking inspection — technical scene");
            GUI.Label(new Rect(22,35,715,23),"WASD: 3 m/s  •  Shift: 5.5 m/s  •  Hold RMB: look  •  Home: approach  •  5: proxy bridge deck");
            GUI.Label(new Rect(22,58,715,23),"1 Crestbridge approach   2 Greyharrow   3 Reedmere   4 Drowsebank Mill");
            GUI.Label(new Rect(22,81,715,23),"E "+transform.position.x.ToString("F1")+"m   N "+transform.position.z.ToString("F1")+"m   elevation "+transform.position.y.ToString("F2")+"m  •  baked terrain, no gameplay");
            GUI.Label(new Rect(22,104,715,23),"Bridge proxy approach gap "+surface.bridgeApproachGap.ToString("F2")+"m: no ramps certified. Water is a stage cue; use 5 for deck inspection.");
            GUI.Label(new Rect(22,125,715,23),"Tan marks technical graded corridors. Hall/Depot labels are fixed anchors, not completed buildings.");
        }
        IEnumerator Smoke()
        {
            yield return null;yield return new WaitForFixedUpdate();
            try
            {
                for(int i=0;i<4;i++)
                {
                    SpawnAt(i);Physics.SyncTransforms();
                    if(!Physics.Raycast(transform.position+Vector3.up*10,Vector3.down,out var hit,30,1<<TerrainInspectionSurface.TerrainLayer))throw new InvalidOperationException("Missing spawn terrain collider "+i);
                    if(Mathf.Abs(hit.point.y-surface.HeightAt(transform.position.x,transform.position.z))>.03f)throw new InvalidOperationException("Spawn geometry differs from baked terrain "+i);
                }
                SpawnAt(0);for(int i=0;i<30;i++)Step(Vector2.zero,1f/60,false);
                Vector3 start=transform.position;for(int i=0;i<60;i++)Step(Vector2.up,1f/60,false);
                float distance=Vector2.Distance(new Vector2(start.x,start.z),new Vector2(transform.position.x,transform.position.z));
                if(Mathf.Abs(distance-3)>.04f)throw new InvalidOperationException("Walk displacement "+distance+" expected 3m");
                Debug.Log("CAELMOR_TERRAIN_WALK_SMOKE_PASSED: four real terrain spawns, collision, one-second 3m movement, source="+surface.sourceHash);
                Application.Quit(0);
            }
            catch(Exception error){Debug.LogError(error);Application.Quit(1);}
        }
    }
}
