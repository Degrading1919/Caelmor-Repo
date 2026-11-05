using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEditor.Build.Reporting;
using UnityEngine;
using UnityEngine.SceneManagement;
using Object = UnityEngine.Object;

namespace Caelmor.Unity.Editor
{
    /// <summary>Executed Editor/asset tests. No map authorship or gameplay interpretation.</summary>
    public static class ArchitectureValidation
    {
        const string Floor = "CODE/Scripts/architectural_generator/dist/floor_visibility_demo.glb";
        const string Gate = "CODE/Scripts/architectural_generator/evidence/benchmarks_v08/gatehouse.glb";
        const string ScratchKey = "_architecture_validation";
        static int checks;
        static string ScratchDirectory => Path.Combine(Application.dataPath, "../Obj/ArchitectureValidation");
        static string BindingsPath => ArchitectureImport.Root + "/Bindings/floor_visibility_demo.asset";

        [MenuItem("Caelmor/Architecture/Validate pipeline")]
        public static void Run()
        {
            checks = 0;
            CaelmorSceneOwnership.RequireCleanScenes();
            Check(!Directory.Exists(ScratchDirectory) && !Directory.Exists(ArchitectureImport.Root + "/Generated/" + ScratchKey) && !File.Exists(ArchitectureImport.Root + "/Prefabs/" + ScratchKey + ".prefab") && !File.Exists("Assets/_Project/World/" + ScratchKey + ".unity"), "Reserved validation paths must be absent; no pre-existing content is deleted.");
            var sceneHashes = SceneHashes();
            var originalScenes = Enumerable.Range(0, SceneManager.sceneCount).Select(SceneManager.GetSceneAt).Select(s => (s.path, s.isDirty)).ToArray();
            var floorBindings = GetFixtureBindings();
            var floor = ArchitectureImport.Import(Path.Combine(ArchitectureImport.Repository, Floor), "floor_visibility_demo", floorBindings);
            var gate = ArchitectureImport.Import(Path.Combine(ArchitectureImport.Repository, Gate), "thornfell_gatehouse");
            ValidateFixture(floor, true);
            ValidateFixture(gate, false);
            var assetHashes = AssetHashes();
            Check(ReferenceEquals(floor, ArchitectureImport.Import(Path.Combine(ArchitectureImport.Repository, Floor), "floor_visibility_demo", floorBindings)), "Identical import returns the existing asset.");
            ArchitectureImport.Import(Path.Combine(ArchitectureImport.Repository, Gate), "thornfell_gatehouse");
            Check(Equal(assetHashes, AssetHashes()), "Repeated import creates no files and modifies no saved assets.");
            ValidateAuthoredAndUpdates();
            ValidateConflictAndRollback();
            Check(Equal(sceneHashes, SceneHashes()), "Every pre-existing saved Unity scene is byte/content unchanged.");
            foreach (var scene in originalScenes)
                Check(Enumerable.Range(0, SceneManager.sceneCount).Select(SceneManager.GetSceneAt).Single(s => s.path == scene.path).isDirty == scene.isDirty, "Existing open scene dirty state preserved.");
            Check(SceneManager.sceneCount == originalScenes.Length, "All temporary scenes closed without changing original scene setup.");
            WriteReport(floor, gate);
            Debug.Log("CAELMOR_ARCHITECTURE_VALIDATION_PASSED checks=" + checks);
        }

        public static void ValidateSavedAssets()
        {
            checks = 0;
            foreach (string key in new[] { "floor_visibility_demo", "thornfell_gatehouse" })
            {
                var record = AssetDatabase.LoadAssetAtPath<ArchitectureImportRecord>(ArchitectureImport.Root + "/Generated/" + key + "/ImportRecord.asset");
                Check(record != null, "Import record persisted across Editor processes.");
                ArchitectureImport.VerifyOwned(record);
                ValidateFixture(record, key == "floor_visibility_demo");
                var placement = AssetDatabase.LoadAssetAtPath<GameObject>(record.placementPrefab);
                Check(placement != null && PrefabUtility.GetPrefabAssetType(placement) == PrefabAssetType.Variant, "Hand-authorable prefab variant persisted.");
                Check(AssetDatabase.AssetPathToGUID(record.placementPrefab) == record.placementGuid, "Placement prefab GUID persisted.");
            }
            Debug.Log("CAELMOR_ARCHITECTURE_PERSISTENCE_PASSED checks=" + checks);
        }

        public static void BuildValidationPlayer()
        {
            CaelmorSceneOwnership.RequireCleanScenes();
            string output = Environment.GetEnvironmentVariable("CAELMOR_ARCHITECTURE_BUILD_OUTPUT") ?? Path.Combine(Application.dataPath, "../Builds/ArchitectureValidation/CaelmorArchitectureValidation.exe");
            output = Path.GetFullPath(output);
            Check(output.StartsWith(ArchitectureImport.Repository + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase), "Validation build stays in designated checkout.");
            const string scenePath = "Assets/_Project/World/_architecture_player_validation.unity";
            Check(!File.Exists(scenePath), "Disposable player verification scene does not overwrite authored content.");
            var setup = EditorSceneManager.GetSceneManagerSetup();
            Scene test = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            try
            {
                SceneManager.SetActiveScene(test);
                var root = new GameObject("Architecture validation only");
                var validation = root.AddComponent<ArchitecturePlayerValidation>();
                var floor = AssetDatabase.LoadAssetAtPath<GameObject>(ArchitectureImport.Root + "/Prefabs/floor_visibility_demo.prefab");
                var gate = AssetDatabase.LoadAssetAtPath<GameObject>(ArchitectureImport.Root + "/Prefabs/thornfell_gatehouse.prefab");
                Check(floor != null && gate != null, "Import real fixtures before building the verification player.");
                validation.floorA = (GameObject)PrefabUtility.InstantiatePrefab(floor, test);
                validation.floorB = (GameObject)PrefabUtility.InstantiatePrefab(floor, test);
                validation.gatehouse = (GameObject)PrefabUtility.InstantiatePrefab(gate, test);
                validation.floorB.transform.position = new Vector3(40, 0, 0);
                validation.gatehouse.transform.position = new Vector3(-40, 0, 0);
                EditorSceneManager.SaveScene(test, scenePath);
                Directory.CreateDirectory(Path.GetDirectoryName(output));
                var report = BuildPipeline.BuildPlayer(new BuildPlayerOptions { scenes = new[] { scenePath }, target = BuildTarget.StandaloneWindows64, locationPathName = output, options = BuildOptions.StrictMode });
                Check(report.summary.result == BuildResult.Succeeded, "Architecture native Windows build including PBR shaders succeeded.");
                Debug.Log("CAELMOR_ARCHITECTURE_PLAYER_BUILT bytes=" + report.summary.totalSize + " seconds=" + report.summary.totalTime.TotalSeconds.ToString("F3"));
            }
            finally
            {
                EditorSceneManager.CloseScene(test, true);
                CaelmorSceneOwnership.RestoreSetup(setup);
                AssetDatabase.DeleteAsset(scenePath);
            }
        }

        static ArchitectureMaterialBindings GetFixtureBindings()
        {
            var existing = AssetDatabase.LoadAssetAtPath<ArchitectureMaterialBindings>(BindingsPath);
            if (existing != null) return existing;
            var source = JObject.Parse(File.ReadAllText(Path.Combine(ArchitectureImport.Repository, Path.ChangeExtension(Floor, ".caelmor.json"))));
            var objects = source["objects"];
            string roof = objects.Select(o => (string)o["name"]).First(n => n.Contains("Split oak shingle courses::covering"));
            string iron = (string)objects.First(o => (string)o["material"] == "iron")["name"];
            var bindings = ScriptableObject.CreateInstance<ArchitectureMaterialBindings>();
            bindings.bindings = new[]
            {
                new ArchitectureMaterialBindings.Binding { bufferId = roof, materialId = "split_oak_shingle", metricUv0Verified = true },
                new ArchitectureMaterialBindings.Binding { bufferId = iron, materialId = "forged_iron", metricUv0Verified = true }
            };
            Directory.CreateDirectory(Path.GetDirectoryName(BindingsPath));
            AssetDatabase.CreateAsset(bindings, BindingsPath);
            return bindings;
        }

        static void ValidateFixture(ArchitectureImportRecord record, bool separated)
        {
            string original = Path.Combine(ArchitectureImport.Repository, record.sourcePath);
            var raw = ArchitectureImport.Container.Read(original);
            var sidecar = JObject.Parse(File.ReadAllText(Path.ChangeExtension(original, ".caelmor.json")));
            var prefab = AssetDatabase.LoadAssetAtPath<GameObject>(record.generatedPrefab);
            Check(prefab != null, "Native generated prefab saved.");
            var identities = prefab.GetComponentsInChildren<ArchitectureIdentity>(true);
            Check(identities.Length == raw.Json["nodes"].Count(), "Every original node retains semantic metadata.");
            Check(identities.All(i => i.buildingId == record.buildingId), "Persistent source building identity retained.");
            Check(prefab.GetComponentsInChildren<MeshRenderer>(true).Length == sidecar["objects"].Count(), "All visual sections preserved separately.");
            Check(prefab.GetComponentsInChildren<MeshCollider>(true).Length == (int)sidecar["collision"]["object_count"], "Separate collision proxy count preserved.");
            Check(prefab.GetComponentsInChildren<MeshCollider>(true).All(c => c.GetComponent<Renderer>() == null && !c.convex), "Collision proxies are invisible static MeshColliders.");
            Check(!prefab.GetComponentsInChildren<MonoBehaviour>(true).Any(c => c.GetType().Name == "FloorVisibilityBuilding"), "No interior occupancy/gameplay floor adapter inferred.");
            var byName = identities.ToDictionary(i => i.gameObject.name);
            for (int n = 0; n < raw.Json["nodes"].Count(); n++)
            {
                var node = raw.Json["nodes"][n];
                var identity = byName[(string)node["name"]];
                foreach (int child in node["children"] ?? new JArray())
                    Check(byName[(string)raw.Json["nodes"][child]["name"]].transform.parent == identity.transform, "Original local hierarchy retained.");
                var translation = node["translation"];
                Vector3 expected = translation == null ? Vector3.zero : new Vector3(-(float)translation[0], (float)translation[1], (float)translation[2]);
                Check(Vector3.Distance(identity.transform.localPosition, expected) < 0.0001f, "glTF right-handed -> Unity X-reflection translation preserved.");
                var scale = node["scale"];
                Vector3 expectedScale = scale == null ? Vector3.one : new Vector3((float)scale[0], (float)scale[1], (float)scale[2]);
                Check(Vector3.Distance(identity.transform.localScale, expectedScale) < 0.0001f, "Metre scale preserved without implicit scaling.");
                var rotation = node["rotation"];
                Quaternion expectedRotation = rotation == null ? Quaternion.identity : new Quaternion((float)rotation[0], -(float)rotation[1], -(float)rotation[2], (float)rotation[3]);
                Check(Quaternion.Angle(identity.transform.localRotation, expectedRotation) < 0.001f, "glTF right-handed -> Unity reflected local rotation preserved.");
                var extras = node["extras"];
                if (extras?["caelm_visibility"] != null)
                {
                    Check(identity.volumeId == (string)extras["caelm_floor_volume"] && identity.visibility == (string)extras["caelm_visibility"] && identity.floorIndex == (int)extras["caelm_floor_index"], "Exact optional floor visibility identity preserved.");
                    if (extras["caelm_floor_min"] != null)
                        Check(identity.floorMin == (float)extras["caelm_floor_min"] && identity.floorMax == (float)extras["caelm_floor_max"], "Exact source-local visual height bounds preserved.");
                }
                if (node["mesh"] == null) continue;
                var meshSpec = raw.Json["meshes"][(int)node["mesh"]];
                Check(meshSpec["primitives"].Count() == 1, "Fixture source has one primitive per semantic section.");
                var primitive = meshSpec["primitives"][0];
                var mesh = identity.GetComponent<MeshFilter>().sharedMesh;
                Check(AssetDatabase.GetAssetPath(mesh).EndsWith(".asset"), "Prepared mesh uses native reusable Unity persistence.");
                Check(mesh.vertexCount == (int)raw.Json["accessors"][(int)primitive["attributes"]["POSITION"]]["count"], "Original vertex count retained.");
                foreach (var attr in ((JObject)primitive["attributes"]).Properties().Where(p => p.Name.StartsWith("TEXCOORD_")))
                {
                    int channel = int.Parse(attr.Name.Substring(9));
                    var uvs = new List<Vector2>(); mesh.GetUVs(channel, uvs);
                    Check(uvs.Count == mesh.vertexCount, "Every original UV channel retained.");
                    foreach (int vertex in Sentinels(mesh.vertexCount))
                    {
                        float[] source = FloatAccessor(raw, (int)attr.Value, vertex, 2);
                        Check(Vector2.Distance(uvs[vertex], new Vector2(source[0], 1 - source[1])) < 0.0001f, "Independent original GLB UV sentinel, including Unity V conversion.");
                    }
                }
                foreach (int vertex in Sentinels(mesh.vertexCount))
                {
                    float[] source = FloatAccessor(raw, (int)primitive["attributes"]["POSITION"], vertex, 3);
                    Check(Vector3.Distance(mesh.vertices[vertex], new Vector3(-source[0], source[1], source[2])) < 0.0001f, "Independent original GLB metre/orientation position sentinel.");
                    Vector4 tangent = mesh.tangents[vertex];
                    Check(!float.IsNaN(tangent.x) && Mathf.Abs(tangent.w) == 1 && Mathf.Abs(Vector3.Dot(mesh.normals[vertex], new Vector3(tangent.x, tangent.y, tangent.z))) < 0.01f, "Prepared normal-UV tangent frame finite and orthogonal.");
                }
                if (primitive["attributes"]["COLOR_0"] != null) Check(mesh.colors.Length == mesh.vertexCount, "Source vertex weathering colors retained.");
                var material = identity.GetComponent<MeshRenderer>().sharedMaterial;
                var sourceMaterial = raw.Json["materials"][(int)primitive["material"]];
                if (material.shader.name == "Caelmor/Architecture PBR")
                {
                    Check(material.GetFloat("_BaseUv") == ((int?)sourceMaterial["pbrMetallicRoughness"]?["baseColorTexture"]?["texCoord"] ?? 0), "Original albedo UV selection retained.");
                    Check(material.GetFloat("_NormalUv") == ((int?)sourceMaterial["normalTexture"]?["texCoord"] ?? 0), "Original detail normal UV selection retained.");
                    Check(material.GetFloat("_OrmUv") == ((int?)sourceMaterial["pbrMetallicRoughness"]?["metallicRoughnessTexture"]?["texCoord"] ?? 0), "Original ORM UV selection retained.");
                    Check(material.GetFloat("_Roughness") == ((float?)sourceMaterial["pbrMetallicRoughness"]?["roughnessFactor"] ?? 1), "PBR roughness factor preserved.");
                    Check(material.GetFloat("_Metallic") == ((float?)sourceMaterial["pbrMetallicRoughness"]?["metallicFactor"] ?? 1), "PBR metallic factor preserved.");
                    var sourceColor = sourceMaterial["pbrMetallicRoughness"]?["baseColorFactor"];
                    Color expectedColor = sourceColor == null ? Color.white : new Color((float)sourceColor[0], (float)sourceColor[1], (float)sourceColor[2], (float)sourceColor[3]).gamma;
                    Check(Vector4.Distance(material.GetColor("_Color"), expectedColor) < 0.0001f, "Linear glTF factor converted to Unity Color property convention.");
                    Check(material.GetFloat("_VertexColor") == 1, "PBR shader consumes original vertex color.");
                    foreach (string prop in new[] { "_MainTex", "_NormalTex", "_OrmTex" })
                    {
                        var texture = material.GetTexture(prop);
                        if (texture == null || string.IsNullOrEmpty(AssetDatabase.GetAssetPath(texture))) continue;
                        var importer = (TextureImporter)AssetImporter.GetAtPath(AssetDatabase.GetAssetPath(texture));
                        Check(importer.sRGBTexture == (prop == "_MainTex"), "sRGB color and linear normal/ORM import roles preserved.");
                        if (prop == "_NormalTex") Check(importer.textureType == TextureImporterType.NormalMap && !importer.flipGreenChannel, "+Y tangent normal preserved.");
                    }
                }
                else Check(material.shader.name == "Standard" && separated, "Only explicitly bound baseline uses Standard.");
            }
            if (separated)
            {
                Check(identities.Any(i => i.visibility == "FLOOR" && i.floorIndex == 1) && identities.Any(i => i.visibility == "COVERING"), "Independently hideable storeys and roof sections retained.");
                Check(identities.Select(i => i.volumeId).Distinct().Count() >= 3, "Distinct construction volumes retained.");
                foreach (var binding in GetFixtureBindings().bindings)
                {
                    var material = byName[binding.bufferId].GetComponent<MeshRenderer>().sharedMaterial;
                    var descriptor = JObject.Parse(File.ReadAllText(ArchitectureImport.Root + "/Materials/" + binding.materialId + "/material.json"));
                    Check(material.name.EndsWith(binding.materialId), "Exact stable painting-library ID assigned explicitly.");
                    Check(Vector2.Distance(material.GetTextureScale("_MainTex"), new Vector2(1 / (float)descriptor["scale_m"][0], 1 / (float)descriptor["scale_m"][1])) < 0.0001f, "Physical repeat in metres retained.");
                    Check(material.IsKeywordEnabled("_NORMALMAP") && material.IsKeywordEnabled("_METALLICGLOSSMAP"), "Baseline normal and metallic/smoothness PBR channels active.");
                }
            }
            var shader = Shader.Find("Caelmor/Architecture PBR");
            Check(shader != null && !ShaderUtil.GetShaderMessages(shader).Any(m => m.severity.ToString() == "Error"), "PBR shader imported without compiler errors.");
        }

        static void ValidateAuthoredAndUpdates()
        {
            string source = CopyFixture();
            var setup = EditorSceneManager.GetSceneManagerSetup();
            Scene test = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            try
            {
                SceneManager.SetActiveScene(test);
                var record = ArchitectureImport.Import(source, ScratchKey);
                var variantMaterial = AssetDatabase.LoadAssetAtPath<Material>(ArchitectureImport.Root + "/Materials/forged_iron/forged_iron.mat");
                var variantContents = PrefabUtility.LoadPrefabContents(record.placementPrefab);
                try
                {
                    var artistRenderer = variantContents.GetComponentsInChildren<MeshRenderer>(true).First();
                    artistRenderer.sharedMaterial = variantMaterial;
                    PrefabUtility.RecordPrefabInstancePropertyModifications(artistRenderer);
                    var artistAddition = new GameObject("Director variant fixture");
                    SceneManager.MoveGameObjectToScene(artistAddition, variantContents.scene);
                    artistAddition.transform.SetParent(variantContents.transform, false);
                    artistAddition.transform.localPosition = new Vector3(3, 2, 1);
                    PrefabUtility.SaveAsPrefabAsset(variantContents, record.placementPrefab);
                }
                finally { PrefabUtility.UnloadPrefabContents(variantContents); }
                var asset = AssetDatabase.LoadAssetAtPath<GameObject>(record.placementPrefab);
                var a = (GameObject)PrefabUtility.InstantiatePrefab(asset, test);
                var b = (GameObject)PrefabUtility.InstantiatePrefab(asset, test);
                a.name = "Manually placed A"; a.transform.position = new Vector3(30, 5, -20);
                b.name = "Manually placed B"; b.transform.position = new Vector3(-30, 2, 40);
                var rendererA = a.GetComponentsInChildren<MeshRenderer>(true).First();
                var rendererB = b.GetComponentsInChildren<MeshRenderer>(true).First();
                Check(ReferenceEquals(rendererA.sharedMaterial, rendererB.sharedMaterial), "Instances share materials rather than instantiate duplicates.");
                Check(ReferenceEquals(rendererA.GetComponent<MeshFilter>().sharedMesh, rendererB.GetComponent<MeshFilter>().sharedMesh), "Instances share prepared native meshes.");
                Check(rendererA.sharedMaterial == variantMaterial && a.GetComponentsInChildren<Transform>(true).Any(t => t.name == "Director variant fixture"), "Artist variant child material override/addition inherited by placements.");
                var overrideMaterial = AssetDatabase.LoadAssetAtPath<Material>(ArchitectureImport.Root + "/Materials/split_oak_shingle/split_oak_shingle.mat");
                rendererA.sharedMaterial = overrideMaterial;
                PrefabUtility.RecordPrefabInstancePropertyModifications(rendererA);
                PrefabUtility.RecordPrefabInstancePropertyModifications(a.transform);
                var personalObject = new GameObject("Director-authored content"); personalObject.transform.SetParent(a.transform, false);
                personalObject.transform.localPosition = new Vector3(1, 2, 3);
                string scenePath = "Assets/_Project/World/" + ScratchKey + ".unity";
                EditorSceneManager.SaveScene(test, scenePath);
                string authoredHash = ArchitectureImport.FileHash(scenePath);
                string variantHash = ArchitectureImport.FileHash(record.placementPrefab);
                string prefabGuid = AssetDatabase.AssetPathToGUID(record.generatedPrefab);
                var raw = ArchitectureImport.Container.Read(source);
                string previousSourceHash = record.sourceHash;
                var meshNode = raw.Json["nodes"].First(n => n["mesh"] != null);
                var positionAccessor = raw.Json["accessors"][(int)raw.Json["meshes"][(int)meshNode["mesh"]]["primitives"][0]["attributes"]["POSITION"]];
                var positionView = raw.Json["bufferViews"][(int)positionAccessor["bufferView"]];
                int changedVertex = (int)positionAccessor["count"] / 2;
                int vertexOffset = ((int?)positionView["byteOffset"] ?? 0) + ((int?)positionAccessor["byteOffset"] ?? 0) + changedVertex * ((int?)positionView["byteStride"] ?? 12);
                float changedX = BitConverter.ToSingle(raw.Bin, vertexOffset) + 0.03125f;
                Buffer.BlockCopy(BitConverter.GetBytes(changedX), 0, raw.Bin, vertexOffset, 4);
                if (positionAccessor["min"] != null) positionAccessor["min"][0] = Math.Min((float)positionAccessor["min"][0], changedX);
                if (positionAccessor["max"] != null) positionAccessor["max"][0] = Math.Max((float)positionAccessor["max"][0], changedX);
                meshNode["translation"] = new JArray(0.125, 0.0, 0.0);
                float sine = Mathf.Sin(Mathf.PI / 8), cosine = Mathf.Cos(Mathf.PI / 8);
                meshNode["rotation"] = new JArray(0, sine, 0, cosine);
                meshNode["scale"] = new JArray(1.25, 0.75, 1.5);
                File.WriteAllBytes(source, raw.Write(raw.Json));
                var updated = ArchitectureImport.Import(source, ScratchKey);
                Check(updated.sourceHash != previousSourceHash && ReferenceEquals(updated, record), "Changed source processed on the existing record.");
                Check(AssetDatabase.AssetPathToGUID(updated.generatedPrefab) == prefabGuid, "Source geometry update preserves generated prefab GUID.");
                Check(ArchitectureImport.FileHash(scenePath) == authoredHash && ArchitectureImport.FileHash(updated.placementPrefab) == variantHash, "Source update never rewrites authored scene or variant files.");
                Check(a.transform.position == new Vector3(30, 5, -20) && personalObject != null && personalObject.transform.localPosition == new Vector3(1, 2, 3), "Open authored placement/additions survive update.");
                Check(rendererA.sharedMaterial == overrideMaterial, "Open child material override survives update.");
                Check(rendererB.sharedMaterial == variantMaterial && b.GetComponentsInChildren<Transform>(true).Any(t => t.name == "Director variant fixture"), "Artist variant child override/addition survives source update independently of scene override.");
                var updatedPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(updated.generatedPrefab);
                var changedNode = updatedPrefab.GetComponentsInChildren<ArchitectureIdentity>(true).Single(i => i.name == (string)meshNode["name"]);
                Check(Mathf.Abs(changedNode.transform.localPosition.x + 0.125f) < 0.0001f, "Source transform update reaches reusable generated content.");
                Check(Mathf.Abs(changedNode.GetComponent<MeshFilter>().sharedMesh.vertices[changedVertex].x + changedX) < 0.0001f, "Changed original GLB vertex reaches the existing native prepared mesh.");
                Check(Quaternion.Angle(changedNode.transform.localRotation, new Quaternion(0, -sine, 0, cosine)) < 0.001f && changedNode.transform.localScale == new Vector3(1.25f, 0.75f, 1.5f), "Changed source rotation and nonuniform local scale persist with correct handedness.");
                var unsaved = new GameObject("Unsaved Director work"); unsaved.transform.position = new Vector3(17, 6, 21);
                EditorSceneManager.MarkSceneDirty(test);
                ArchitectureImport.Import(source, ScratchKey);
                Check(test.isDirty && unsaved != null && unsaved.transform.position == new Vector3(17, 6, 21) && ArchitectureImport.FileHash(scenePath) == authoredHash, "Repeated import retains unsaved authored objects and never saves their scene.");
                test = EditorSceneManager.OpenScene(scenePath, OpenSceneMode.Single);
                var reloadedA = test.GetRootGameObjects().Single(o => o.name == "Manually placed A");
                Check(reloadedA.transform.position == new Vector3(30, 5, -20) && reloadedA.GetComponentsInChildren<Transform>(true).Any(t => t.name == "Director-authored content"), "Saved authored placements/additions survive scene reload.");
                Check(reloadedA.GetComponentsInChildren<MeshRenderer>(true).First().sharedMaterial == overrideMaterial, "Saved child material override survives source update and reload.");
                var reloadedB = test.GetRootGameObjects().Single(o => o.name == "Manually placed B");
                Check(reloadedB.GetComponentsInChildren<MeshRenderer>(true).First().sharedMaterial == variantMaterial && reloadedB.GetComponentsInChildren<Transform>(true).Any(t => t.name == "Director variant fixture"), "Artist variant override/addition persists after scene reload.");
                var beforeConflict = AssetHashes();
                meshNode["name"] = "incompatible renamed section";
                File.WriteAllBytes(source, raw.Write(raw.Json));
                Reject(() => ArchitectureImport.Import(source, ScratchKey), "Removed/renamed semantic identity rejected before publishing.");
                Check(Equal(beforeConflict, AssetHashes()), "Identity conflict changes no Unity asset files.");
            }
            finally
            {
                if (test.IsValid()) EditorSceneManager.CloseScene(test, true);
                CaelmorSceneOwnership.RestoreSetup(setup);
                AssetDatabase.DeleteAsset("Assets/_Project/World/" + ScratchKey + ".unity");
                CleanScratch();
            }
        }

        static void ValidateConflictAndRollback()
        {
            string source = CopyFixture();
            try
            {
                string sidecarPath = Path.ChangeExtension(source, ".caelmor.json");
                byte[] sidecarBytes = File.ReadAllBytes(sidecarPath);
                var sidecar = JObject.Parse(File.ReadAllText(sidecarPath));
                sidecar["collision"]["object_count"] = 999;
                File.WriteAllText(sidecarPath, sidecar.ToString(Formatting.Indented));
                var before = AssetHashes();
                Reject(() => ArchitectureImport.Import(source, ScratchKey), "Late collision mismatch rolls back first import.");
                Check(!Directory.Exists(ArchitectureImport.Root + "/Generated/" + ScratchKey), "Failed first-import destination fully removed for retry.");
                Check(Equal(before, AssetHashes()), "Late failure restores complete asset tree.");
                File.WriteAllBytes(sidecarPath, sidecarBytes);
                var record = ArchitectureImport.Import(source, ScratchKey);
                ArchitectureImport.VerifyOwned(record);
                var beforeUpdateFailure = AssetHashes();
                var raw = ArchitectureImport.Container.Read(source);
                raw.Json["nodes"].First(n => n["mesh"] != null)["translation"] = new JArray(0.5, 0, 0);
                File.WriteAllBytes(source, raw.Write(raw.Json));
                File.WriteAllText(sidecarPath, sidecar.ToString(Formatting.Indented));
                Reject(() => ArchitectureImport.Import(source, ScratchKey), "Late collision mismatch rolls back existing-mesh updates.");
                Check(Equal(beforeUpdateFailure, AssetHashes()), "Existing generated files byte/content restored after late update failure.");
                ArchitectureImport.VerifyOwned(record);
                File.WriteAllBytes(sidecarPath, sidecarBytes);
                ArchitectureImport.Import(source, ScratchKey);
                ArchitectureImport.VerifyOwned(record);
                Check(true, "Corrected same-key import succeeds after both rollback paths.");
                var generatedMaterial = AssetDatabase.LoadAssetAtPath<GameObject>(record.generatedPrefab).GetComponentsInChildren<MeshRenderer>(true).First().sharedMaterial;
                float original = generatedMaterial.GetFloat("_Roughness");
                generatedMaterial.SetFloat("_Roughness", 0.123f); EditorUtility.SetDirty(generatedMaterial);
                Reject(() => ArchitectureImport.Import(source, ScratchKey), "Unsaved shared material edit rejected.");
                generatedMaterial.SetFloat("_Roughness", original); EditorUtility.ClearDirty(generatedMaterial);
                string materialPath = AssetDatabase.GetAssetPath(generatedMaterial);
                byte[] bytes = File.ReadAllBytes(materialPath);
                try
                {
                    File.AppendAllText(materialPath, "\n# Artist-edited generated resource\n");
                    Reject(() => ArchitectureImport.Import(source, ScratchKey + "_new"), "Shared-resource edits rejected even for a new key.");
                }
                finally { File.WriteAllBytes(materialPath, bytes); AssetDatabase.ImportAsset(materialPath, ImportAssetOptions.ForceSynchronousImport); }
            }
            finally { CleanScratch(); }
        }

        static string CopyFixture()
        {
            Directory.CreateDirectory(ScratchDirectory);
            string source = Path.Combine(ArchitectureImport.Repository, Floor);
            foreach (string extension in new[] { ".glb", ".collision.glb", ".caelmor.json" })
                File.Copy(Path.ChangeExtension(source, extension), Path.Combine(ScratchDirectory, "floor_visibility_demo" + extension), true);
            return Path.Combine(ScratchDirectory, "floor_visibility_demo.glb");
        }

        static void CleanScratch()
        {
            AssetDatabase.DeleteAsset(ArchitectureImport.Root + "/Generated/" + ScratchKey);
            AssetDatabase.DeleteAsset(ArchitectureImport.Root + "/Prefabs/" + ScratchKey + ".prefab");
            if (Directory.Exists(ScratchDirectory)) Directory.Delete(ScratchDirectory, true);
        }

        static IEnumerable<int> Sentinels(int count) => new[] { 0, count / 3, count / 2, count - 1 }.Distinct();
        static float[] FloatAccessor(ArchitectureImport.Container raw, int index, int vertex, int dimensions)
        {
            var accessor = raw.Json["accessors"][index];
            Check((int)accessor["componentType"] == 5126, "Fixture oracle uses original float accessor.");
            var view = raw.Json["bufferViews"][(int)accessor["bufferView"]];
            int start = ((int?)view["byteOffset"] ?? 0) + ((int?)accessor["byteOffset"] ?? 0) + vertex * ((int?)view["byteStride"] ?? dimensions * 4);
            return Enumerable.Range(0, dimensions).Select(i => BitConverter.ToSingle(raw.Bin, start + i * 4)).ToArray();
        }
        static Dictionary<string, string> AssetHashes() => Directory.GetFiles(ArchitectureImport.Root, "*", SearchOption.AllDirectories).Where(p => !p.EndsWith(".meta") || !Directory.Exists(p.Substring(0, p.Length - 5))).ToDictionary(p => p.Replace('\\', '/'), ArchitectureImport.FileHash);
        static Dictionary<string, string> SceneHashes() => Directory.GetFiles("Assets", "*.unity", SearchOption.AllDirectories).ToDictionary(p => p, ArchitectureImport.FileHash);
        static bool Equal(Dictionary<string, string> a, Dictionary<string, string> b) => a.Count == b.Count && a.All(p => b.TryGetValue(p.Key, out string hash) && hash == p.Value);
        static void Reject(Action action, string assertion)
        {
            bool rejected = false;
            try { action(); } catch (InvalidOperationException) { rejected = true; }
            Check(rejected, assertion);
        }
        static void Check(bool value, string message) { checks++; ArchitectureImport.Require(value, "Architecture validation failed: " + message); }

        static void WriteReport(params ArchitectureImportRecord[] records)
        {
            var report = new JObject
            {
                ["unity"] = Application.unityVersion, ["gltfast"] = "6.14.1", ["checks"] = checks,
                ["fixtures"] = new JArray(records.Select(FixtureReport)),
                ["unique_asset_files"] = Directory.GetFiles(ArchitectureImport.Root, "*", SearchOption.AllDirectories).Count(p => !p.EndsWith(".meta")),
                ["unique_asset_bytes"] = Directory.GetFiles(ArchitectureImport.Root, "*", SearchOption.AllDirectories).Sum(p => new FileInfo(p).Length),
                ["native_material_asset_files"] = Directory.GetFiles(ArchitectureImport.Root, "*.mat", SearchOption.AllDirectories).Length,
                ["editor_source_material_subassets"] = Directory.GetFiles(ArchitectureImport.Root + "/Generated", "*.glb", SearchOption.AllDirectories).Sum(p => AssetDatabase.LoadAllAssetsAtPath(p).OfType<Material>().Count()),
                ["limits"] = "Batch asset/physics/shader compilation evidence; no rendered artistic review, occupancy authoring, traversal or gameplay floor hiding."
            };
            string path = Path.Combine(Application.dataPath, "../Logs/architecture-validation.json");
            Directory.CreateDirectory(Path.GetDirectoryName(path)); File.WriteAllText(path, report.ToString(Formatting.Indented) + "\n");
        }

        static JObject FixtureReport(ArchitectureImportRecord r)
        {
            var prefab = AssetDatabase.LoadAssetAtPath<GameObject>(r.generatedPrefab);
            var materials = prefab.GetComponentsInChildren<MeshRenderer>(true).SelectMany(m => m.sharedMaterials).Distinct().ToArray();
            var textures = materials.SelectMany(m => m.GetTexturePropertyNames().Select(m.GetTexture)).Where(t => t != null).Distinct().ToArray();
            var visual = prefab.GetComponentsInChildren<MeshFilter>(true).Select(m => m.sharedMesh).Distinct().ToArray();
            var collision = prefab.GetComponentsInChildren<MeshCollider>(true).Select(c => c.sharedMesh).Distinct().ToArray();
            return new JObject
            {
                ["source"] = r.sourcePath, ["sha256"] = r.sourceHash, ["building_id"] = r.buildingId,
                ["renderers"] = r.rendererCount, ["visual_meshes"] = r.meshCount, ["colliders"] = r.colliderCount,
                ["materials"] = r.materialCount, ["textures"] = r.textureCount, ["vertices"] = r.vertices, ["triangles"] = r.triangles,
                ["input_bytes"] = r.sourceBytes, ["owned_generated_bytes"] = r.generatedBytes, ["first_import_seconds"] = r.importSeconds,
                ["owned_asset_files"] = r.ownedFiles.Count(f => !f.path.EndsWith(".meta")),
                ["editor_texture_native_estimate_bytes"] = textures.Sum(UnityEngine.Profiling.Profiler.GetRuntimeMemorySizeLong),
                ["editor_visual_mesh_native_estimate_bytes"] = visual.Sum(UnityEngine.Profiling.Profiler.GetRuntimeMemorySizeLong),
                ["editor_collision_mesh_native_estimate_bytes"] = collision.Sum(UnityEngine.Profiling.Profiler.GetRuntimeMemorySizeLong),
                ["editor_material_native_estimate_bytes"] = materials.Sum(UnityEngine.Profiling.Profiler.GetRuntimeMemorySizeLong),
                ["unresolved_library_mapping_count"] = r.unresolvedLibraryMappings.Split('\n').Length,
                ["memory_note"] = "Editor native estimates for unique referenced resources; not process RSS or a player/GPU benchmark."
            };
        }
    }
}
