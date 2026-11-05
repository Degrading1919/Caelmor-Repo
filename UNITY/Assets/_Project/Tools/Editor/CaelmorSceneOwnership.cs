using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine.SceneManagement;

namespace Caelmor.Unity.Editor
{
    /// <summary>Fixed technical-fixture ownership. World scenes have no generation entry point.</summary>
    public static class CaelmorSceneOwnership
    {
        public const string RecordPath = "Assets/_Project/World/PlayableFixtureOwnership.txt";
        public static readonly string[] OwnedPaths =
        {
            CaelmorBuild.ScenePath,
            "Assets/_Project/World/PlayableNavigation.asset",
            "Assets/_Project/World/Materials/Ground.mat",
            "Assets/_Project/World/Materials/Stone.mat",
            "Assets/_Project/World/Materials/Path.mat",
            "Assets/_Project/World/Materials/FixtureAmber.mat",
            "Assets/_Project/World/Materials/Player.mat",
            "Assets/_Project/World/Materials/Trim.mat"
        };

        public static void RequireCleanScenes()
        {
            if (PrefabStageUtility.GetCurrentPrefabStage() != null)
                throw new InvalidOperationException("CAELMOR_PREFAB_STAGE_OPEN: finish or close Prefab Mode before technical validation, generation, or building.");
            bool hasUntitled = false, hasSaved = false;
            for (int index = 0; index < SceneManager.sceneCount; index++)
            {
                var scene = SceneManager.GetSceneAt(index);
                if (scene.isDirty)
                    throw new InvalidOperationException("CAELMOR_UNSAVED_SCENE: save or close your changes before technical validation, generation, or building: " + scene.name);
                if (string.IsNullOrEmpty(scene.path) && scene.rootCount > 0)
                    throw new InvalidOperationException("CAELMOR_UNSAVED_SCENE: save or close the untitled scene containing objects before technical validation, generation, or building.");
                hasUntitled |= string.IsNullOrEmpty(scene.path);
                hasSaved |= !string.IsNullOrEmpty(scene.path);
            }
            if (hasUntitled && hasSaved)
                throw new InvalidOperationException("CAELMOR_UNTITLED_SCENE_SETUP: save or close the untitled scene before changing the loaded scene setup.");
        }

        public static void RestoreSetup(SceneSetup[] setup)
        {
            // An untouched untitled empty scene has no disk path to restore.
            if (setup.Length == 0 || setup.All(scene => string.IsNullOrEmpty(scene.path)))
                EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            else EditorSceneManager.RestoreSceneManagerSetup(setup);
        }

        public static string Hash(string path)
        {
            byte[] bytes = File.ReadAllBytes(path);
            string extension = Path.GetExtension(path).ToLowerInvariant();
            if (extension == ".unity" || extension == ".mat" || extension == ".meta")
                bytes = Encoding.UTF8.GetBytes(File.ReadAllText(path).Replace("\r\n", "\n"));
            using (var algorithm = SHA256.Create())
                return BitConverter.ToString(algorithm.ComputeHash(bytes)).Replace("-", "").ToLowerInvariant();
        }

        public static void RequireUnmodifiedFixture()
        {
            if (!File.Exists(RecordPath))
                throw new InvalidOperationException("CAELMOR_FIXTURE_OWNERSHIP_MISSING: restore the tracked ownership record; generation cannot claim existing content.");
            var entries = File.ReadAllLines(RecordPath).Where(line => !string.IsNullOrWhiteSpace(line) && !line.StartsWith("#")).ToArray();
            var expected = OwnedPaths.SelectMany(path => new[] { path, path + ".meta" }).ToArray();
            if (entries.Length != expected.Length)
                throw new InvalidOperationException("CAELMOR_FIXTURE_OWNERSHIP_INVALID: expected the exact reserved fixture asset and GUID set.");
            foreach (string path in expected)
            {
                var matching = entries.Where(line => line.Length > 66 && line.Substring(66) == path).ToArray();
                if (matching.Length != 1)
                    throw new InvalidOperationException("CAELMOR_FIXTURE_OWNERSHIP_INVALID: " + path);
                if (path.EndsWith(".meta", StringComparison.Ordinal) && !File.Exists(path))
                    throw new InvalidOperationException("CAELMOR_FIXTURE_GUID_MISSING: restore the tracked meta file before regenerating: " + path);
                if (File.Exists(path) && Hash(path) != matching[0].Substring(0, 64))
                    throw new InvalidOperationException("CAELMOR_FIXTURE_CONFLICT: changed generated content is preserved. Move authored work to a separate scene/material, or reconcile this file deliberately before regeneration: " + path);
                if (!path.EndsWith(".meta", StringComparison.Ordinal))
                {
                    var asset = AssetDatabase.LoadMainAssetAtPath(path);
                    if (asset != null && EditorUtility.IsDirty(asset))
                        throw new InvalidOperationException("CAELMOR_FIXTURE_CONFLICT: unsaved asset edits are preserved: " + path);
                }
            }
        }

        public static void SaveOwnedAssetsAndRecordHashes()
        {
            foreach (string path in OwnedPaths)
            {
                var asset = AssetDatabase.LoadMainAssetAtPath(path);
                if (asset != null) AssetDatabase.SaveAssetIfDirty(asset);
            }
            AssetDatabase.Refresh();
            var lines = new[] { "# Generated technical fixture only. Text hashes normalize CRLF to LF; binary assets use raw bytes.", "# Never place authored world layouts or artist material edits in these reserved resources." }
                .Concat(OwnedPaths.SelectMany(path => new[] { path, path + ".meta" }).Select(path => Hash(path) + "  " + path));
            File.WriteAllLines(RecordPath, lines);
            AssetDatabase.ImportAsset(RecordPath);
        }
    }
}
