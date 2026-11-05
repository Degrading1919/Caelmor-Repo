using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Caelmor.Unity.Editor
{
    /// <summary>Batch evidence for ownership conflicts and saved/unsaved authored-scene preservation.</summary>
    public static class SceneOwnershipValidation
    {
        const string Scratch = "Assets/_Project/World/SceneOwnershipValidationScratch";

        [MenuItem("Caelmor/Validate scene ownership safeguards")]
        public static void Run()
        {
            CaelmorSceneOwnership.RequireCleanScenes();
            if (Directory.Exists(Scratch)) throw new InvalidOperationException("Scene ownership test scratch already exists; inspect it before removing.");
            CaelmorSceneOwnership.RequireUnmodifiedFixture();
            var originalSetup = EditorSceneManager.GetSceneManagerSetup();
            var originalBuildScenes = EditorBuildSettings.scenes.Select(value => new EditorBuildSettingsScene(value.path, value.enabled)).ToArray();
            const string buildSettingsPath = "ProjectSettings/EditorBuildSettings.asset";
            byte[] originalBuildSettings = File.ReadAllBytes(buildSettingsPath);
            var hashes = CaelmorSceneOwnership.OwnedPaths.SelectMany(path => new[] { path, path + ".meta" })
                .ToDictionary(path => path, CaelmorSceneOwnership.Hash);
            var fixtureSnapshot = hashes.Keys.Concat(new[] { CaelmorSceneOwnership.RecordPath })
                .ToDictionary(path => path, File.ReadAllBytes);
            string first = Scratch + "/AuthoredFirst.unity", second = Scratch + "/AuthoredSecond.unity";
            byte[] originalFixture = File.ReadAllBytes(CaelmorBuild.ScenePath);
            try
            {
                AssetDatabase.CreateFolder("Assets/_Project/World", "SceneOwnershipValidationScratch");
                var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
                var material = new Material(Shader.Find("Standard")) { color = Color.magenta };
                AssetDatabase.CreateAsset(material, Scratch + "/ArtistOverride.mat");
                var authored = GameObject.CreatePrimitive(PrimitiveType.Cube);
                authored.name = "Manually placed object with artist override";
                authored.transform.SetPositionAndRotation(new Vector3(7, 2, -3), Quaternion.Euler(0, 31, 0));
                authored.transform.localScale = new Vector3(2, 3, 4);
                authored.GetComponent<Renderer>().sharedMaterial = material;
                var terrainData = new TerrainData { heightmapResolution = 33, size = new Vector3(8, 2, 8) };
                AssetDatabase.CreateAsset(terrainData, Scratch + "/AuthoredTerrain.asset");
                Terrain.CreateTerrainGameObject(terrainData).name = "Authored terrain";
                Check(EditorSceneManager.SaveScene(scene, first), "save first authored scene");
                var scene2 = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
                new GameObject("Independent authored content").transform.position = new Vector3(-12, 1, 4);
                Check(EditorSceneManager.SaveScene(scene2, second), "save second authored scene");
                SceneManager.SetActiveScene(scene2);
                var authoredHashes = Directory.GetFiles(Scratch, "*", SearchOption.AllDirectories)
                    .ToDictionary(path => path, CaelmorSceneOwnership.Hash);
                var authoredSetup = EditorSceneManager.GetSceneManagerSetup();
                EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(first, true), new EditorBuildSettingsScene(second, true) };
                Check(CaelmorBuild.GetBuildScenePaths().SequenceEqual(new[] { first, second }), "build selects configured authored scenes without substituting fixture");

                CaelmorBuild.Validate();
                AssertSetup(authoredSetup);
                Check(EditorBuildSettings.scenes.Select(value => value.path).SequenceEqual(new[] { first, second }), "validation preserves build list");
                foreach (var pair in authoredHashes) Check(CaelmorSceneOwnership.Hash(pair.Key) == pair.Value, "validation preserves authored bytes " + pair.Key);
                authored = GameObject.Find("Manually placed object with artist override");
                Check(authored != null && authored.transform.position == new Vector3(7, 2, -3) && authored.transform.localScale == new Vector3(2, 3, 4), "saved authored transform survives validation");
                Check(authored.GetComponent<Renderer>().sharedMaterial == AssetDatabase.LoadAssetAtPath<Material>(Scratch + "/ArtistOverride.mat"), "artist material override survives validation");
                Check(GameObject.Find("Authored terrain") != null && GameObject.Find("Independent authored content") != null, "terrain and additive scene objects survive validation");

                // Exercise the explicit generator, while retaining the exact tracked fixture baseline.
                // Its only writable resources are the reserved fixture scene/nav/material/GUID set.
                CaelmorBuild.CreateScene();
                CaelmorSceneOwnership.RequireUnmodifiedFixture();
                AssertSetup(authoredSetup);
                Check(EditorBuildSettings.scenes.Select(value => value.path).SequenceEqual(new[] { first, second }), "explicit generation preserves authored build list");
                foreach (var pair in authoredHashes) Check(CaelmorSceneOwnership.Hash(pair.Key) == pair.Value, "explicit generation preserves authored bytes " + pair.Key);
                CaelmorBuild.Validate();
                RestoreFixture(fixtureSnapshot);
                AssertSetup(authoredSetup);

                string materialPath = "Assets/_Project/World/Materials/FixtureAmber.mat";
                var fixtureMaterial = AssetDatabase.LoadAssetAtPath<Material>(materialPath);
                var baselineColor = fixtureMaterial.color;
                fixtureMaterial.color = Color.cyan;
                EditorUtility.SetDirty(fixtureMaterial);
                try
                {
                    ExpectConflict(CaelmorBuild.CreateScene, "CAELMOR_FIXTURE_CONFLICT");
                    Check(fixtureMaterial.color == Color.cyan && EditorUtility.IsDirty(fixtureMaterial), "unsaved fixture material override survives generation refusal");
                }
                finally
                {
                    fixtureMaterial.color = baselineColor;
                    AssetDatabase.ImportAsset(materialPath, ImportAssetOptions.ForceUpdate);
                    // ImportAsset retains native Material dirty flags even after restoring its value.
                    // This test owns that one temporary in-memory edit and has restored its baseline.
                    EditorUtility.ClearDirty(fixtureMaterial);
                }

                string guidPath = materialPath + ".meta";
                var originalGuidBytes = File.ReadAllBytes(guidPath);
                WithPausedAssetImport(() =>
                {
                    try
                    {
                        File.Delete(guidPath);
                        ExpectConflict(CaelmorBuild.CreateScene, "CAELMOR_FIXTURE_GUID_MISSING");
                    }
                    finally { File.WriteAllBytes(guidPath, originalGuidBytes); }
                });

                authored = GameObject.Find("Manually placed object with artist override");
                authored.transform.position = new Vector3(15, 6, 9);
                EditorSceneManager.MarkSceneDirty(authored.scene);
                ExpectConflict(CaelmorBuild.Validate, "CAELMOR_UNSAVED_SCENE");
                ExpectConflict(CaelmorBuild.CreateScene, "CAELMOR_UNSAVED_SCENE");
                ExpectConflict(CaelmorBuild.BuildWindows, "CAELMOR_UNSAVED_SCENE");
                Check(authored != null && authored.transform.position == new Vector3(15, 6, 9) && authored.scene.isDirty, "all standard paths retain dirty in-memory authored work");
                foreach (var pair in authoredHashes) Check(CaelmorSceneOwnership.Hash(pair.Key) == pair.Value, "dirty refusal preserves saved bytes " + pair.Key);
                EditorSceneManager.OpenScene(first, OpenSceneMode.Single); // Only discard this test's own unsaved mutation.

                WithPausedAssetImport(() =>
                {
                    // Same-size in-place mutation avoids truncating a scene that Windows may map.
                    // The watcher must never import this deliberately invalid temporary YAML.
                    var editedFixture = (byte[])originalFixture.Clone();
                    editedFixture[0] ^= 1;
                    try
                    {
                        WriteSameSize(CaelmorBuild.ScenePath, editedFixture);
                        string editedHash = CaelmorSceneOwnership.Hash(CaelmorBuild.ScenePath);
                        ExpectConflict(CaelmorBuild.CreateScene, "CAELMOR_FIXTURE_CONFLICT");
                        Check(CaelmorSceneOwnership.Hash(CaelmorBuild.ScenePath) == editedHash, "explicit generation preserves modified fixture bytes");
                    }
                    finally { WriteSameSize(CaelmorBuild.ScenePath, originalFixture); }
                });

                EditorBuildSettings.scenes = Array.Empty<EditorBuildSettingsScene>();
                ExpectConflict(() => CaelmorBuild.GetBuildScenePaths(), "CAELMOR_BUILD_SCENES_EMPTY");
                EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(first, true), new EditorBuildSettingsScene(first, true) };
                ExpectConflict(() => CaelmorBuild.GetBuildScenePaths(), "CAELMOR_BUILD_SCENE_DUPLICATE");
                foreach (var pair in hashes) Check(CaelmorSceneOwnership.Hash(pair.Key) == pair.Value, "fixture source unchanged " + pair.Key);
                Debug.Log("CAELMOR_SCENE_OWNERSHIP_CHECKS_PASSED: configured scene selection, saved additive scenes/terrain/artist material/transform preservation, executed explicit owned regeneration and native fixture validation, dirty validation/generation/build refusal, modified fixture and unsaved material/GUID conflicts, unchanged tracked technical fixture");
            }
            finally
            {
                try
                {
                    RestoreFixture(fixtureSnapshot);
                    CaelmorSceneOwnership.RestoreSetup(originalSetup);
                    AssetDatabase.DeleteAsset(Scratch);
                    AssetDatabase.ImportAsset(CaelmorBuild.ScenePath, ImportAssetOptions.ForceUpdate);
                }
                finally
                {
                    EditorBuildSettings.scenes = originalBuildScenes;
                    File.WriteAllBytes(buildSettingsPath, originalBuildSettings);
                }
            }
        }

        static void RestoreFixture(Dictionary<string, byte[]> snapshot)
        {
            WithPausedAssetImport(() =>
            {
                foreach (var pair in snapshot) File.WriteAllBytes(pair.Key, pair.Value);
            });
            foreach (string path in CaelmorSceneOwnership.OwnedPaths.Concat(new[] { CaelmorSceneOwnership.RecordPath }))
            {
                AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);
                var asset = AssetDatabase.LoadMainAssetAtPath(path);
                if (asset != null) EditorUtility.ClearDirty(asset);
            }
        }

        static void WithPausedAssetImport(Action action)
        {
            AssetDatabase.DisallowAutoRefresh();
            try
            {
                AssetDatabase.StartAssetEditing();
                try
                {
                    AssetDatabase.ReleaseCachedFileHandles();
                    action();
                }
                finally { AssetDatabase.StopAssetEditing(); }
            }
            finally { AssetDatabase.AllowAutoRefresh(); }
        }

        static void WriteSameSize(string path, byte[] bytes)
        {
            using (var stream = new FileStream(path, FileMode.Open, FileAccess.Write, FileShare.ReadWrite | FileShare.Delete))
            {
                Check(stream.Length == bytes.Length, "same-size test fixture mutation");
                stream.Write(bytes, 0, bytes.Length);
                stream.Flush();
            }
        }

        static void AssertSetup(SceneSetup[] expected)
        {
            var actual = EditorSceneManager.GetSceneManagerSetup();
            Check(actual.Length == expected.Length, "scene setup count restored");
            for (int index = 0; index < expected.Length; index++)
                Check(actual[index].path == expected[index].path && actual[index].isActive == expected[index].isActive && actual[index].isLoaded == expected[index].isLoaded, "scene setup restored " + index);
        }
        static void ExpectConflict(Action action, string prefix)
        {
            try { action(); }
            catch (InvalidOperationException error) when (error.Message.StartsWith(prefix, StringComparison.Ordinal)) { return; }
            throw new InvalidOperationException("SCENE_OWNERSHIP_ASSERT: expected " + prefix);
        }
        static void Check(bool condition, string detail)
        {
            if (!condition) throw new InvalidOperationException("SCENE_OWNERSHIP_ASSERT: " + detail);
        }
    }
}
