using System;
using System.IO;
using System.Collections.Generic;
using UnityEngine.AI;
using Caelmor.Unity.Playable;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;

namespace Caelmor.Unity.Editor
{
    public static class CaelmorBuild
    {
        public const string ScenePath = "Assets/_Project/World/PlayableFoundation.unity";
        [MenuItem("Caelmor/Technical fixture/Regenerate owned playable scene")]
        public static void CreateScene()
        {
            CaelmorSceneOwnership.RequireCleanScenes();
            CaelmorSceneOwnership.RequireUnmodifiedFixture();
            var setup = EditorSceneManager.GetSceneManagerSetup();
            try { GenerateOwnedScene(); }
            finally { CaelmorSceneOwnership.RestoreSetup(setup); }
        }
        static void GenerateOwnedScene()
        {
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            Directory.CreateDirectory("Assets/_Project/World/Materials");
            AssetDatabase.Refresh();
            var ground = Material("Ground", new Color(.21f, .27f, .25f));
            var stone = Material("Stone", new Color(.34f, .40f, .40f));
            var path = Material("Path", new Color(.40f, .39f, .32f));
            var wood = Material("FixtureAmber", new Color(.85f, .65f, .28f));
            var playerMat = Material("Player", new Color(.29f, .49f, .57f));
            var trim = Material("Trim", new Color(.65f, .60f, .45f));
            Cube("Ground / technical 28m square", new Vector3(0, -.25f, 0), new Vector3(28, .5f, 28), ground, true).AddComponent<NavigableTerrain>();
            Cube("Shelter and margin / connected technical hub", new Vector3(26, -.25f, 0), new Vector3(24, .5f, 28), ground, true).AddComponent<NavigableTerrain>();
            Cube("Central route", new Vector3(0, .006f, 0), new Vector3(3, .01f, 26), path, false);
            Cube("Cross route", new Vector3(0, .008f, 1), new Vector3(26, .01f, 2.2f), path, false);
            Cube("North bound", new Vector3(0, .75f, 13.75f), new Vector3(28, 1.5f, .5f), stone, true);
            Cube("South bound", new Vector3(0, .75f, -13.75f), new Vector3(28, 1.5f, .5f), stone, true);
            Cube("East bound / north of connecting road", new Vector3(13.75f, .75f, 8.5f), new Vector3(.5f, 1.5f, 11), stone, true);
            Cube("East bound / south of connecting road", new Vector3(13.75f, .75f, -8.5f), new Vector3(.5f, 1.5f, 11), stone, true);
            Cube("West bound", new Vector3(-13.75f, .75f, 0), new Vector3(.5f, 1.5f, 28), stone, true);
            Cube("Shelter hub north bound", new Vector3(26, .75f, 13.75f), new Vector3(24, 1.5f, .5f), stone, true);
            Cube("Shelter hub south bound", new Vector3(26, .75f, -13.75f), new Vector3(24, 1.5f, .5f), stone, true);
            Cube("Shelter hub east bound", new Vector3(37.75f, .75f, 0), new Vector3(.5f, 1.5f, 28), stone, true);
            Cube("Connecting shelter road", new Vector3(18, .008f, 0), new Vector3(22, .01f, 3), path, false);
            AddSign("Shelter and reed margin →", new Vector3(11.7f, 2.2f, 1.8f));
            AddSign("← Landing and bank", new Vector3(17, 2.2f, 1.8f));
            Cube("Collision test wall", new Vector3(-5, 1, 1), new Vector3(5, 2, .8f), stone, true);
            Cube("Collision test block", new Vector3(6, .9f, 5), new Vector3(2.5f, 1.8f, 2.5f), stone, true);
            for (int z = -10; z <= 10; z += 5)
            {
                Cube("Route edge left", new Vector3(-1.65f, .05f, z), new Vector3(.2f, .1f, 1f), trim, false);
                Cube("Route edge right", new Vector3(1.65f, .05f, z), new Vector3(.2f, .1f, 1f), trim, false);
            }
            var target = new GameObject("Interaction fixture / narrative adapter anchor (no content)");
            target.transform.position = new Vector3(0, 0, 2);
            var anchor = target.AddComponent<InteractionAnchor>();
            var pedestal = Cube("Marker plinth", new Vector3(0, .25f, 2), new Vector3(1.3f, .5f, 1.3f), stone, false);
            pedestal.transform.SetParent(target.transform, true);
            var marker = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            marker.name = "Server state marker"; marker.transform.position = new Vector3(0, 1.15f, 2);
            marker.transform.localScale = Vector3.one * .85f;
            UnityEngine.Object.DestroyImmediate(marker.GetComponent<Collider>());
            marker.transform.SetParent(target.transform, true);
            marker.GetComponent<Renderer>().sharedMaterial = wood;
            anchor.markerRenderer = marker.GetComponent<Renderer>();
            var spawn = new GameObject("Player spawn / technical fixture"); spawn.transform.position = new Vector3(0, 0, -4);
            var avatar = new GameObject("Local view / snapshot interpolation only");
            var body = GameObject.CreatePrimitive(PrimitiveType.Capsule);
            body.name = "Greybox player"; body.transform.SetParent(avatar.transform, false);
            body.transform.localPosition = Vector3.up * .9f; body.transform.localScale = new Vector3(.7f, .9f, .7f);
            UnityEngine.Object.DestroyImmediate(body.GetComponent<Collider>()); body.GetComponent<Renderer>().sharedMaterial = playerMat;
            var nose = Cube("Facing indicator", new Vector3(0, 1.35f, .4f), new Vector3(.25f, .15f, .25f), trim, false);
            nose.transform.SetParent(avatar.transform, false);
            var cameraObject = new GameObject("Player camera"); cameraObject.tag = "MainCamera";
            var camera = cameraObject.AddComponent<Camera>(); camera.fieldOfView = 58; camera.nearClipPlane = .1f;
            camera.clearFlags = CameraClearFlags.SolidColor; camera.backgroundColor = new Color(.18f, .24f, .28f);
            cameraObject.transform.SetPositionAndRotation(new Vector3(0, 5, -10), Quaternion.Euler(32, 0, 0));
            var sun = new GameObject("Daylight").AddComponent<Light>(); sun.type = LightType.Directional;
            sun.intensity = 1.3f; sun.shadows = LightShadows.Soft; sun.transform.rotation = Quaternion.Euler(45, -32, 0);
            RenderSettings.ambientLight = new Color(.55f, .60f, .64f);
            RenderSettings.fog = true; RenderSettings.fogColor = camera.backgroundColor; RenderSettings.fogMode = FogMode.Linear;
            RenderSettings.fogStartDistance = 24; RenderSettings.fogEndDistance = 65;
            var nav = new GameObject("Host navigation / baked terrain mesh").AddComponent<TerrainNavigation>();
            nav.data = BakeNavigation(); nav.Bind();
            var destinationView = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            destinationView.name = "Destination / committed host presentation";
            destinationView.transform.localScale = new Vector3(.65f, .012f, .65f);
            UnityEngine.Object.DestroyImmediate(destinationView.GetComponent<Collider>());
            destinationView.GetComponent<Renderer>().sharedMaterial = trim;
            destinationView.SetActive(false);
            var game = new GameObject("Caelmor / playable composition").AddComponent<PlayableBootstrap>();
            game.navigation = nav; game.destinationView = destinationView.transform;
            game.spawn = spawn.transform; game.playerView = avatar.transform; game.playerCamera = camera; game.interactionAnchor = anchor;
            game.gameObject.AddComponent<PlayableHud>().game = game;
            EditorSceneManager.SaveScene(EditorSceneManager.GetActiveScene(), ScenePath);
            CaelmorSceneOwnership.SaveOwnedAssetsAndRecordHashes();
            Debug.Log("CAELMOR_SCENE_READY: " + ScenePath);
        }
        [MenuItem("Caelmor/Validate playable scene")]
        public static void Validate()
        {
            CaelmorSceneOwnership.RequireCleanScenes();
            if (!File.Exists(ScenePath))
                throw new InvalidOperationException("CAELMOR_FIXTURE_MISSING: explicitly regenerate the owned technical fixture before validation.");
            var setup = EditorSceneManager.GetSceneManagerSetup();
            try
            {
                // Global Physics/NavMesh checks require isolation from unrelated authored scene geometry.
                // Open only after refusing unsaved changes, and never persist validation mutations.
                EditorSceneManager.OpenScene(ScenePath);
                var anchor = UnityEngine.Object.FindAnyObjectByType<InteractionAnchor>();
                PlayableValidation.Run(anchor, 1 << 8, UnityEngine.Object.FindAnyObjectByType<TerrainNavigation>());
            }
            finally { CaelmorSceneOwnership.RestoreSetup(setup); }
        }
        public static void BuildWindows()
        {
            CaelmorSceneOwnership.RequireCleanScenes();
            var scenes = GetBuildScenePaths();
            Validate();
            string output = Environment.GetEnvironmentVariable("CAELMOR_BUILD_OUTPUT");
            if (string.IsNullOrWhiteSpace(output)) output = Path.Combine(Directory.GetCurrentDirectory(), "Builds", "Windows", "Caelmor.exe");
            Directory.CreateDirectory(Path.GetDirectoryName(output));
            var report = BuildPipeline.BuildPlayer(new BuildPlayerOptions
            {
                scenes = scenes, locationPathName = output,
                target = BuildTarget.StandaloneWindows64, options = BuildOptions.Development
            });
            if (report.summary.result != BuildResult.Succeeded)
                throw new InvalidOperationException("CAELMOR_BUILD_FAILED: " + report.summary.result + " errors=" + report.summary.totalErrors);
            Debug.Log("CAELMOR_BUILD_SUCCEEDED: " + output);
        }
        public static string[] GetBuildScenePaths()
        {
            var result = new List<string>();
            foreach (var scene in EditorBuildSettings.scenes)
            {
                if (!scene.enabled) continue;
                if (string.IsNullOrWhiteSpace(scene.path) || !File.Exists(scene.path))
                    throw new InvalidOperationException("CAELMOR_BUILD_SCENE_MISSING: " + scene.path);
                if (result.Contains(scene.path))
                    throw new InvalidOperationException("CAELMOR_BUILD_SCENE_DUPLICATE: " + scene.path);
                result.Add(scene.path);
            }
            if (result.Count == 0)
                throw new InvalidOperationException("CAELMOR_BUILD_SCENES_EMPTY: select saved scenes in Build Settings; builds do not generate or replace scenes.");
            return result.ToArray();
        }
        static NavMeshData BakeNavigation()
        {
            Physics.SyncTransforms();
            var settings = NavMesh.GetSettingsCount() > 0 ? NavMesh.GetSettingsByIndex(0) : NavMesh.CreateSettings();
            settings.agentRadius = .43f; settings.agentHeight = 1.8f; settings.agentClimb = .2f; settings.agentSlope = 40f;
            settings.overrideVoxelSize = true; settings.voxelSize = .08f; settings.minRegionArea = .1f;
            var sources = new List<NavMeshBuildSource>();
            var navigationBounds=new Bounds(new Vector3(12,1,0),new Vector3(56,6,30));
            UnityEngine.AI.NavMeshBuilder.CollectSources(navigationBounds,
                1 << 8, NavMeshCollectGeometry.PhysicsColliders, 0, new List<NavMeshBuildMarkup>(), sources);
            var baked = UnityEngine.AI.NavMeshBuilder.BuildNavMeshData(settings, sources,
                navigationBounds, Vector3.zero, Quaternion.identity);
            if (baked == null) throw new InvalidOperationException("CAELMOR_NAVIGATION_BAKE_FAILED");
            const string assetPath = "Assets/_Project/World/PlayableNavigation.asset";
            var existing = AssetDatabase.LoadAssetAtPath<NavMeshData>(assetPath);
            if (existing == null) { AssetDatabase.CreateAsset(baked, assetPath); return baked; }
            EditorUtility.CopySerialized(baked, existing); UnityEngine.Object.DestroyImmediate(baked);
            EditorUtility.SetDirty(existing); return existing;
        }
        static Material Material(string name, Color color)
        {
            string path = "Assets/_Project/World/Materials/" + name + ".mat";
            var material = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (material == null) { material = new Material(Shader.Find("Standard")); AssetDatabase.CreateAsset(material, path); }
            material.color = color; return material;
        }
        static void AddSign(string text,Vector3 position)
        {
            var sign=new GameObject(text).AddComponent<TextMesh>();sign.text=text;sign.transform.position=position;
            sign.fontSize=48;sign.characterSize=.12f;sign.anchor=TextAnchor.MiddleCenter;sign.color=new Color(.92f,.86f,.7f);
            sign.transform.rotation=Quaternion.Euler(0,0,0);
        }
        static GameObject Cube(string name, Vector3 position, Vector3 scale, Material material, bool solid)
        {
            var go = GameObject.CreatePrimitive(PrimitiveType.Cube); go.name = name;
            go.transform.position = position; go.transform.localScale = scale; go.GetComponent<Renderer>().sharedMaterial = material;
            if (solid) go.layer = 8; else UnityEngine.Object.DestroyImmediate(go.GetComponent<Collider>());
            return go;
        }
    }
}
