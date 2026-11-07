using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Caelmor.Unity.Inspection;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Caelmor.Unity.Editor
{
    /// <summary>Explicit generated inspector; standard project builds never call this.</summary>
    public static class TerrainInspectionEditor
    {
        public const string DirectoryPath="Assets/_Project/World/TerrainInspection";
        public const string ScenePath=DirectoryPath+"/LowmarkTerrainInspection.unity";
        const string PayloadPath=DirectoryPath+"/LowmarkTerrain.bytes";
        const string OwnershipPath=DirectoryPath+"/SceneOwnership.txt";

        [MenuItem("Caelmor/Terrain inspection/Generate and validate scene")]
        public static void GenerateAndValidate()
        {
            CaelmorSceneOwnership.RequireCleanScenes();
            RequireSceneOwnership();
            if(!File.Exists(PayloadPath))throw new InvalidOperationException("Bake the verified terrain inspection payload first.");
            var setup=EditorSceneManager.GetSceneManagerSetup();
            var fixtureHashes=FixtureHashes();
            string buildSettings=File.ReadAllText("ProjectSettings/EditorBuildSettings.asset");
            try
            {
                AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
                var scene=EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
                var surface=new GameObject("Baked Lowmark terrain / inspection only").AddComponent<TerrainInspectionSurface>();
                surface.payload=AssetDatabase.LoadAssetAtPath<TextAsset>(PayloadPath);surface.ReadPayload();
                surface.groundMaterial=Material("InspectionGround",new Color(.38f,.44f,.34f));
                surface.roadMaterial=Material("InspectionCorridor",new Color(.48f,.43f,.34f));
                surface.waterMaterial=Material("InspectionWater",new Color(.15f,.37f,.46f));
                surface.proxyMaterial=Material("InspectionProxy",new Color(.56f,.48f,.34f));
                var player=new GameObject("Inspector / 3 metres per second");
                var capsule=player.AddComponent<CharacterController>();capsule.height=1.8f;capsule.radius=.3f;capsule.center=new Vector3(0,.9f,0);capsule.stepOffset=.3f;capsule.slopeLimit=48;capsule.skinWidth=.03f;capsule.minMoveDistance=0;
                var cameraObject=new GameObject("Inspector camera");cameraObject.tag="MainCamera";cameraObject.transform.SetParent(player.transform,false);cameraObject.transform.localPosition=new Vector3(0,1.62f,0);
                var camera=cameraObject.AddComponent<Camera>();camera.fieldOfView=70;camera.nearClipPlane=.06f;camera.farClipPlane=8000;camera.backgroundColor=new Color(.55f,.67f,.73f);camera.clearFlags=CameraClearFlags.SolidColor;
                cameraObject.AddComponent<AudioListener>();
                var walker=player.AddComponent<TerrainInspectionWalker>();walker.surface=surface;walker.eye=camera;walker.walkSpeed=3;walker.sprintSpeed=5.5f;walker.SpawnAt(0);
                var sun=new GameObject("Inspection daylight").AddComponent<Light>();sun.type=LightType.Directional;sun.intensity=1.25f;sun.shadows=LightShadows.Soft;sun.transform.rotation=Quaternion.Euler(40,-35,0);
                RenderSettings.ambientLight=new Color(.55f,.58f,.60f);RenderSettings.fog=true;RenderSettings.fogMode=FogMode.Linear;RenderSettings.fogStartDistance=1500;RenderSettings.fogEndDistance=7000;RenderSettings.fogColor=camera.backgroundColor;
                if(!EditorSceneManager.SaveScene(scene,ScenePath))throw new InvalidOperationException("Could not save generated terrain inspection scene.");
                File.WriteAllLines(OwnershipPath,new[]{CaelmorSceneOwnership.Hash(ScenePath),CaelmorSceneOwnership.Hash(ScenePath+".meta")});
                AssetDatabase.ImportAsset(OwnershipPath);
                ValidateLoaded(surface,walker);
            }
            finally
            {
                CaelmorSceneOwnership.RestoreSetup(setup);
                foreach(var pair in fixtureHashes)Check(CaelmorSceneOwnership.Hash(pair.Key)==pair.Value,"Existing technical fixture unchanged: "+pair.Key);
                Check(File.ReadAllText("ProjectSettings/EditorBuildSettings.asset")==buildSettings,"Configured build scenes unchanged");
            }
            ValidateSaved();
            Debug.Log("CAELMOR_TERRAIN_INSPECTION_SCENE_READY: "+ScenePath);
        }

        [MenuItem("Caelmor/Terrain inspection/Validate saved scene")]
        public static void ValidateSaved()
        {
            CaelmorSceneOwnership.RequireCleanScenes();
            RequireSceneOwnership();
            var setup=EditorSceneManager.GetSceneManagerSetup();
            string before=CaelmorSceneOwnership.Hash(ScenePath);
            try
            {
                EditorSceneManager.OpenScene(ScenePath);
                var surface=UnityEngine.Object.FindAnyObjectByType<TerrainInspectionSurface>();
                var walker=UnityEngine.Object.FindAnyObjectByType<TerrainInspectionWalker>();
                Check(surface!=null&&surface.payload!=null&&walker!=null,"Saved native scene retains payload/player references");
                ValidateLoaded(surface,walker);
            }
            finally{CaelmorSceneOwnership.RestoreSetup(setup);}
            Check(CaelmorSceneOwnership.Hash(ScenePath)==before,"Native validation never persists runtime geometry into scene");
            Debug.Log("CAELMOR_TERRAIN_INSPECTION_PERSISTENCE_PASSED");
        }

        static void ValidateLoaded(TerrainInspectionSurface surface,TerrainInspectionWalker walker)
        {
            surface.BuildGeometry();Physics.SyncTransforms();
            Check(surface.grids.Count==4&&surface.spawns.Count==4,"Regional and three local grids / four spawns loaded");
            Check(walker.walkSpeed==3&&walker.sprintSpeed==5.5f,"Serialized movement speed is exactly 3 / 5.5m per second");
            for(int i=0;i<surface.spawns.Count;i++)
            {
                walker.SpawnAt(i);Physics.SyncTransforms();
                var point=walker.transform.position;
                Check(Physics.Raycast(point+Vector3.up*20,Vector3.down,out var hit,50,1<<TerrainInspectionSurface.TerrainLayer),"Real terrain collider at spawn "+i);
                Check(Mathf.Abs(hit.point.y-surface.HeightAt(point.x,point.z))<.03f,"Native mesh elevation matches exact source triangles at spawn "+i);
            }
            // Raycast both sides of every local/regional interface, including T junctions.
            for(int gridIndex=1;gridIndex<surface.grids.Count;gridIndex++)
            {
                var grid=surface.grids[gridIndex];float east=grid.east,north=grid.north,maxEast=east+(grid.nx-1)*grid.step,maxNorth=north+(grid.ny-1)*grid.step;
                for(int i=1;i<8;i++)
                {
                    float fraction=i/8f;
                    foreach(var point in new[]{new Vector2(east-.1f,Mathf.Lerp(north,maxNorth,fraction)),new Vector2(east+.1f,Mathf.Lerp(north,maxNorth,fraction)),new Vector2(maxEast-.1f,Mathf.Lerp(north,maxNorth,fraction)),new Vector2(maxEast+.1f,Mathf.Lerp(north,maxNorth,fraction)),new Vector2(Mathf.Lerp(east,maxEast,fraction),north-.1f),new Vector2(Mathf.Lerp(east,maxEast,fraction),north+.1f),new Vector2(Mathf.Lerp(east,maxEast,fraction),maxNorth-.1f),new Vector2(Mathf.Lerp(east,maxEast,fraction),maxNorth+.1f)})
                    {
                        float expected=surface.HeightAt(point.x,point.y);
                        Check(Physics.Raycast(new Vector3(point.x,expected+20,point.y),Vector3.down,out var hit,40,1<<TerrainInspectionSurface.TerrainLayer),"No collision hole at terrain interface");
                        Check(Mathf.Abs(hit.point.y-expected)<.04f,"Interface collider matches source");
                    }
                }
            }
            walker.SpawnAt(0);Physics.SyncTransforms();for(int i=0;i<30;i++)walker.Step(Vector2.zero,1f/60,false);
            Vector3 start=walker.transform.position;for(int i=0;i<60;i++)walker.Step(Vector2.up,1f/60,false);
            float distance=Vector2.Distance(new Vector2(start.x,start.z),new Vector2(walker.transform.position.x,walker.transform.position.z));
            Check(Mathf.Abs(distance-3)<.04f,"Actual CharacterController one-second displacement is 3m; measured "+distance);
            walker.SpawnAt(0);for(int i=0;i<30;i++)walker.Step(Vector2.zero,1f/60,false);start=walker.transform.position;
            for(int i=0;i<10;i++)walker.AdvanceFrame(Vector2.up,.1f,false);
            float lowFpsDistance=Vector2.Distance(new Vector2(start.x,start.z),new Vector2(walker.transform.position.x,walker.transform.position.z));
            Check(Mathf.Abs(lowFpsDistance-3)<.04f,"Ten FPS frame consumption retains 3m/s; measured "+lowFpsDistance);
            Check(surface.groundMaterial!=null&&surface.waterMaterial!=null,"Serialized native materials retain shaders in standalone builds");
            Debug.Log("CAELMOR_TERRAIN_INSPECTION_CHECKS_PASSED: native chunk meshes/collision, four spawn raycasts, 168 interface probes, serialized 3m/s, actual 1s displacement="+distance+", 10FPS displacement="+lowFpsDistance+", bridge approach maximum gap="+surface.bridgeApproachGap);
        }

        [MenuItem("Caelmor/Terrain inspection/Build standalone inspector")]
        public static void BuildWindows()
        {
            ValidateSaved();
            string output=Environment.GetEnvironmentVariable("CAELMOR_TERRAIN_INSPECTION_OUTPUT");
            if(string.IsNullOrWhiteSpace(output))output=Path.GetFullPath("Builds/TerrainInspection/CaelmorTerrainInspector.exe");
            Directory.CreateDirectory(Path.GetDirectoryName(output));
            var report=BuildPipeline.BuildPlayer(new BuildPlayerOptions{scenes=new[]{ScenePath},locationPathName=output,target=BuildTarget.StandaloneWindows64,options=BuildOptions.Development});
            Check(report.summary.result==BuildResult.Succeeded,"Inspection standalone build succeeds");
            Debug.Log("CAELMOR_TERRAIN_INSPECTION_BUILD_PASSED: "+output);
        }
        static Dictionary<string,string> FixtureHashes()=>CaelmorSceneOwnership.OwnedPaths.SelectMany(path=>new[]{path,path+".meta"}).ToDictionary(path=>path,CaelmorSceneOwnership.Hash);
        static Material Material(string name,Color color)
        {
            string path=DirectoryPath+"/"+name+".mat";
            var existing=AssetDatabase.LoadAssetAtPath<Material>(path);if(existing!=null)return existing;
            var material=new Material(Shader.Find("Standard")){name=name,color=color};material.SetFloat("_Glossiness",.08f);
            AssetDatabase.CreateAsset(material,path);AssetDatabase.SaveAssetIfDirty(material);return material;
        }
        static void RequireSceneOwnership()
        {
            if(!File.Exists(ScenePath))return;
            Check(File.Exists(OwnershipPath),"Existing inspection scene has no ownership stamp; do not overwrite authored content");
            var lines=File.ReadAllLines(OwnershipPath);
            Check(lines.Length==2&&lines[0]==CaelmorSceneOwnership.Hash(ScenePath)&&File.Exists(ScenePath+".meta")&&lines[1]==CaelmorSceneOwnership.Hash(ScenePath+".meta"),"Changed inspection scene preserved; reconcile authored edits before explicit regeneration");
        }
        static void Check(bool condition,string detail){if(!condition)throw new InvalidOperationException("TERRAIN_INSPECTION_ASSERT: "+detail);}
    }
}
