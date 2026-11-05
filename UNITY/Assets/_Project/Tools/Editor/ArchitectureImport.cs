using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using Debug = UnityEngine.Debug;
using Object = UnityEngine.Object;

namespace Caelmor.Unity.Editor
{
    /// <summary>Offline GLB adaptation around Unity's glTFast. Never opens or saves a world scene.</summary>
    public static class ArchitectureImport
    {
        public const string Root = "Assets/_Project/World/Architecture";
        public const string ImporterVersion = "CaelmorArchitectureImport/1";
        public static string Repository => Path.GetFullPath(Path.Combine(Application.dataPath, "../.."));
        static readonly HashSet<string> AllowedAlpha = new HashSet<string> { "OPAQUE", "MASK" };

        [MenuItem("Caelmor/Architecture/Import exported GLB")]
        public static void ImportDialog()
        {
            string file = EditorUtility.OpenFilePanel("Caelmor exported building", Path.Combine(Repository, "CODE/Scripts/architectural_generator/dist"), "glb");
            if (string.IsNullOrEmpty(file)) return;
            Import(file, Path.GetFileNameWithoutExtension(file));
        }

        public static void ImportFromEnvironment()
        {
            string source = Environment.GetEnvironmentVariable("CAELMOR_ARCHITECTURE_SOURCE");
            string key = Environment.GetEnvironmentVariable("CAELMOR_ARCHITECTURE_KEY");
            string bindingsPath = Environment.GetEnvironmentVariable("CAELMOR_ARCHITECTURE_BINDINGS");
            var bindings = string.IsNullOrEmpty(bindingsPath) ? null : AssetDatabase.LoadAssetAtPath<ArchitectureMaterialBindings>(bindingsPath);
            Require(string.IsNullOrEmpty(bindingsPath) || bindings != null, "Explicit binding asset was not found: " + bindingsPath);
            Import(source, key, bindings);
            Debug.Log("CAELMOR_ARCHITECTURE_IMPORTED");
        }

        public static ArchitectureImportRecord Import(string source, string key, ArchitectureMaterialBindings bindings = null)
        {
            var watch = Stopwatch.StartNew();
            Require(!string.IsNullOrWhiteSpace(key) && key.All(c => char.IsLetterOrDigit(c) || c == '_' || c == '-'), "Use a stable letters/digits/_/- asset key.");
            Require(!string.IsNullOrEmpty(source) && File.Exists(source) && Path.GetExtension(source).ToLowerInvariant() == ".glb", "A real exported .glb is required.");
            source = Path.GetFullPath(source);
            Require(source.StartsWith(Repository + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase), "Keep source exports in the designated checkout before importing.");
            string sidecarPath = Path.ChangeExtension(source, ".caelmor.json");
            Require(File.Exists(sidecarPath), "Missing format-1 .caelmor.json sidecar.");
            var sidecar = JObject.Parse(File.ReadAllText(sidecarPath));
            Require((string)sidecar["format"] == "CaelmorBuildingExport" && (int?)sidecar["version"] == 1, "Unsupported architecture export contract.");
            Require((string)sidecar["units"] == "metres" && (string)sidecar["up_axis"] == "Y", "Expected metre, Y-up glTF export.");
            Require((bool?)sidecar["source_validation"]?["valid"] == true, "Generator source validation is not valid.");
            string collisionName = (string)sidecar["collision"]?["file"];
            Require(!string.IsNullOrEmpty(collisionName) && Path.GetFileName(collisionName) == collisionName, "A local separate collision GLB is required.");
            string collisionPath = Path.Combine(Path.GetDirectoryName(source), collisionName);
            Require(File.Exists(collisionPath), "Missing separate collision geometry: " + collisionPath);
            var visual = Container.Read(source);
            var collision = Container.Read(collisionPath);
            ValidateContainer(visual, true);
            ValidateContainer(collision, false);
            var sourceObjects = (JArray)sidecar["objects"];
            Require(sourceObjects != null && sourceObjects.Count > 0, "No exported construction objects.");
            var visualNames = new HashSet<string>(visual.Json["nodes"].Select(n => (string)n["name"]));
            Require(sourceObjects.All(o => visualNames.Contains((string)o["name"])), "Sidecar identities do not match GLB nodes.");
            string directory = Root + "/Generated/" + key;
            string recordPath = directory + "/ImportRecord.asset";
            string prefabPath = directory + "/" + key + ".prefab";
            string placementPath = Root + "/Prefabs/" + key + ".prefab";
            string signature = Hash(Encoding.UTF8.GetBytes(Signature(visual.Json, collision.Json, sidecar)));
            string bindingSignature = bindings == null ? "none" : Hash(Encoding.UTF8.GetBytes(JsonUtility.ToJson(bindings)));
            string sourceHash = Hash(File.ReadAllBytes(source)), colliderHash = Hash(File.ReadAllBytes(collisionPath)), sidecarHash = Hash(File.ReadAllBytes(sidecarPath));
            var previous = AssetDatabase.LoadAssetAtPath<ArchitectureImportRecord>(recordPath);
            foreach (string guid in AssetDatabase.FindAssets("t:ArchitectureImportRecord", new[] { Root }))
                VerifyOwned(AssetDatabase.LoadAssetAtPath<ArchitectureImportRecord>(AssetDatabase.GUIDToAssetPath(guid)));
            if (previous != null)
            {
                VerifyOwned(previous);
                Require(previous.importerVersion == ImporterVersion, "Importer adapter version changed; migrate this generated asset explicitly after reviewing artist overrides.");
                Require(File.Exists(placementPath) && File.Exists(placementPath + ".meta") && AssetDatabase.AssetPathToGUID(placementPath) == previous.placementGuid, "Artist placement prefab/GUID is missing or changed; recover/reconcile it before reimport.");
                Require(previous.compatibilitySignature == signature, "Source identities/hierarchy/section contract changed. Preserve this asset and reconcile overrides explicitly, or import using a new key.");
                Require(previous.bindingsSignature == bindingSignature, "Explicit binding configuration changed. Use an authored variant for new overrides, or reconcile under a new asset key.");
                Require(previous.sourcePath == Relative(source), "This key belongs to a different source path.");
                if (previous.sourceHash == sourceHash && previous.collisionHash == colliderHash && previous.sidecarHash == sidecarHash)
                {
                    Require(File.Exists(placementPath), "Placement prefab is missing; recover it from Git rather than overwriting authored content.");
                    return previous;
                }
            }
            else Require(!Directory.Exists(directory) && !File.Exists(placementPath), "Unowned content already occupies the requested key.");

            ValidateBindings(bindings, sourceObjects);
            var owned = new HashSet<string>(StringComparer.Ordinal);
            var transaction = new FileTransaction();
            Scene preview = default;
            try
            {
                Directory.CreateDirectory(directory); Directory.CreateDirectory(Root + "/Prefabs");
                string visualPath = directory + "/visual.glb", colliderPath = directory + "/collision.glb";
                var texturePaths = PrepareTextures(visual, directory, transaction, owned);
                // glTFast shaders accept UV0/1 only. Its transient source materials are unused;
                // the saved generated prefab uses the original-channel PBR adapter below.
                var normalized = (JObject)visual.Json.DeepClone();
                normalized["images"] = new JArray(texturePaths.Select(p => new JObject { ["uri"] = RelativeUri(directory, p) }));
                for (int i = 0; i < texturePaths.Length; i++) normalized["textures"][i]["source"] = i;
                foreach (var token in normalized["materials"]?.SelectTokens("$..texCoord").ToArray() ?? Array.Empty<JToken>()) token.Replace(new JValue(0));
                transaction.Write(visualPath, visual.Write(normalized), true); owned.Add(visualPath);
                transaction.Write(colliderPath, File.ReadAllBytes(collisionPath), true); owned.Add(colliderPath);
                string metadataPath = directory + "/source.caelmor.json";
                transaction.Write(metadataPath, File.ReadAllBytes(sidecarPath), true); owned.Add(metadataPath);
                AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
                foreach (string glbPath in new[] { visualPath, colliderPath })
                {
                    transaction.Track(glbPath + ".meta");
                    var importer = AssetImporter.GetAtPath(glbPath);
                    var serialized = new SerializedObject(importer);
                    var creation = serialized.FindProperty("instantiationSettings")?.FindPropertyRelative("sceneObjectCreation");
                    Require(creation != null, "Pinned glTFast importer settings are incompatible.");
                    creation.intValue = 1; // GLTFast.SceneObjectCreation.Always
                    serialized.ApplyModifiedPropertiesWithoutUndo();
                    importer.SaveAndReimport();
                }
                var sourceAsset = AssetDatabase.LoadAssetAtPath<GameObject>(visualPath);
                var collisionAsset = AssetDatabase.LoadAssetAtPath<GameObject>(colliderPath);
                Require(sourceAsset != null && collisionAsset != null, "Unity glTFast import failed; inspect the Editor log.");
                var sourceMaterials = BuildMaterials(visual.Json, texturePaths, transaction, owned);
                preview = EditorSceneManager.NewPreviewScene();
                var generated = new GameObject(key);
                SceneManager.MoveGameObjectToScene(generated, preview);
                var imported = (GameObject)PrefabUtility.InstantiatePrefab(sourceAsset, preview);
                PrefabUtility.UnpackPrefabInstance(imported, PrefabUnpackMode.Completely, InteractionMode.AutomatedAction);
                imported.transform.SetParent(generated.transform, false);
                var nodes = imported.GetComponentsInChildren<Transform>(true).ToDictionary(t => t.name);
                string buildingId = (string)sidecar["floor_presentation"]?["building_id"] ?? "asset:" + key;
                foreach (var node in visual.Json["nodes"])
                {
                    string name = (string)node["name"];
                    Require(nodes.ContainsKey(name), "Imported node name changed: " + name);
                    var metadata = nodes[name].gameObject.AddComponent<ArchitectureIdentity>();
                    var extras = node["extras"];
                    metadata.buildingId = buildingId;
                    metadata.bufferId = (string)extras?["caelm_buffer_id"] ?? name;
                    metadata.volumeId = (string)extras?["caelm_floor_volume"] ?? (string)extras?["caelm_world_zone"] ?? "main";
                    metadata.semanticRole = (string)extras?["caelm_semantic"];
                    metadata.constructionRole = (string)extras?["caelm_component_role"] ?? (string)extras?["caelm_structural_role"];
                    metadata.sourceBufferId = (string)extras?["caelm_source_buffer_id"];
                    metadata.visibility = (string)extras?["caelm_visibility"];
                    metadata.floorIndex = (int?)extras?["caelm_floor_index"] ?? -1;
                    metadata.floorMin = (float?)extras?["caelm_floor_min"] ?? 0;
                    metadata.floorMax = (float?)extras?["caelm_floor_max"] ?? 0;
                    metadata.sourceMetadata = extras?.ToString(Formatting.None) ?? "{}";
                    if (node["mesh"] == null) continue;
                    var meshSpec = visual.Json["meshes"][(int)node["mesh"]];
                    var renderer = nodes[name].GetComponent<MeshRenderer>();
                    var meshFilter = nodes[name].GetComponent<MeshFilter>();
                    Require(renderer != null && meshFilter != null, "Expected static mesh section " + name);
                    var primitives = (JArray)meshSpec["primitives"];
                    Require(primitives.Count == renderer.sharedMaterials.Length, "Submesh/material assignment mismatch.");
                    var mats = primitives.Select(p => sourceMaterials[(int)p["material"]]).ToArray();
                    var explicitBinding = bindings?.bindings.SingleOrDefault(b => b.bufferId == name);
                    if (explicitBinding != null) mats = Enumerable.Repeat(BuildLibraryMaterial(explicitBinding.materialId, transaction, owned), mats.Length).ToArray();
                    renderer.sharedMaterials = mats;
                    // Tangents must follow the actual selected normal UV, not glTFast's temporary UV0 material.
                    int[] normalChannels = primitives.Select(p => explicitBinding != null ? 0 : (int?)visual.Json["materials"][(int)p["material"]]?["normalTexture"]?["texCoord"] ?? 0).Distinct().ToArray();
                    Require(normalChannels.Length == 1, "A mesh with normals on differing UV sets needs an explicit split in Blender.");
                    meshFilter.sharedMesh = SaveMesh(meshFilter.sharedMesh, directory + "/Meshes/" + Hash(Encoding.UTF8.GetBytes(name)).Substring(0, 20) + ".asset", normalChannels[0], transaction, owned);
                }
                var colliders = (GameObject)PrefabUtility.InstantiatePrefab(collisionAsset, preview);
                PrefabUtility.UnpackPrefabInstance(colliders, PrefabUnpackMode.Completely, InteractionMode.AutomatedAction);
                colliders.name = "Collision (generated)";
                colliders.transform.SetParent(generated.transform, false);
                // SaveAsPrefabAsset matches existing GameObjects by name. Collision exports
                // repeat the visual anchor name, so namespace all collision nodes explicitly.
                foreach (var transform in colliders.GetComponentsInChildren<Transform>(true))
                    transform.name = "Collision | " + transform.name;
                foreach (var mf in colliders.GetComponentsInChildren<MeshFilter>(true))
                {
                    var mc = mf.gameObject.AddComponent<MeshCollider>();
                    mc.sharedMesh = SaveMesh(mf.sharedMesh, directory + "/Meshes/collision_" + Hash(Encoding.UTF8.GetBytes(mf.name)).Substring(0, 20) + ".asset", -1, transaction, owned);
                    mc.convex = false;
                    Object.DestroyImmediate(mf.GetComponent<MeshRenderer>());
                    Object.DestroyImmediate(mf);
                }
                Require(colliders.GetComponentsInChildren<MeshCollider>(true).Length == (int)sidecar["collision"]["object_count"], "Collision count differs from export metadata.");
                transaction.Track(prefabPath);
                PrefabUtility.SaveAsPrefabAsset(generated, prefabPath);
                owned.Add(prefabPath);
                var saved = AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath);
                Require(saved != null, "Generated prefab failed to save.");
                if (!File.Exists(placementPath))
                {
                    transaction.Track(placementPath);
                    var variant = (GameObject)PrefabUtility.InstantiatePrefab(saved, preview);
                    PrefabUtility.SaveAsPrefabAsset(variant, placementPath);
                }
                transaction.Track(recordPath);
                var record = previous ?? ScriptableObject.CreateInstance<ArchitectureImportRecord>();
                record.sourcePath = Relative(source); record.sourceHash = sourceHash; record.collisionHash = colliderHash; record.sidecarHash = sidecarHash;
                record.importerVersion = ImporterVersion;
                record.compatibilitySignature = signature; record.bindingsSignature = bindingSignature; record.buildingId = buildingId;
                record.generatedPrefab = prefabPath; record.placementPrefab = placementPath;
                record.placementGuid = AssetDatabase.AssetPathToGUID(placementPath);
                record.sourceBytes = new FileInfo(source).Length + new FileInfo(collisionPath).Length + new FileInfo(sidecarPath).Length;
                var renderers = saved.GetComponentsInChildren<MeshRenderer>(true);
                var meshes = saved.GetComponentsInChildren<MeshFilter>(true).Select(m => m.sharedMesh).Distinct().ToArray();
                record.rendererCount = renderers.Length; record.meshCount = meshes.Length;
                record.colliderCount = saved.GetComponentsInChildren<MeshCollider>(true).Length;
                var materials = renderers.SelectMany(r => r.sharedMaterials).Distinct().ToArray();
                record.materialCount = materials.Length; record.textureCount = materials.SelectMany(m => m.GetTexturePropertyNames().Select(m.GetTexture)).Where(t => t != null).Distinct().Count();
                record.vertices = meshes.Sum(m => (long)m.vertexCount); record.triangles = meshes.Sum(m => (long)m.triangles.Length / 3);
                record.unresolvedLibraryMappings = string.Join("\n", sourceObjects.Where(o => bindings == null || !bindings.bindings.Any(b => b.bufferId == (string)o["name"])).Select(o => (string)o["name"] + " => generator " + (string)o["material"]));
                foreach (string path in owned)
                    if (AssetDatabase.LoadMainAssetAtPath(path) is Object asset && EditorUtility.IsDirty(asset)) AssetDatabase.SaveAssetIfDirty(asset);
                var files = owned.SelectMany(p => new[] { p, p + ".meta" }).Where(File.Exists).Distinct().OrderBy(p => p).ToArray();
                record.ownedFiles = files.Select(p => new ArchitectureImportRecord.OwnedFile { path = p, sha256 = FileHash(p) }).ToArray();
                record.generatedBytes = files.Sum(p => new FileInfo(p).Length);
                record.importSeconds = watch.Elapsed.TotalSeconds;
                if (previous == null) AssetDatabase.CreateAsset(record, recordPath); else EditorUtility.SetDirty(record);
                AssetDatabase.SaveAssetIfDirty(record);
                transaction.Commit();
                Debug.Log($"CAELMOR_ARCHITECTURE_READY {key}: {record.rendererCount} renderers, {record.colliderCount} colliders, {record.materialCount} shared materials, {record.generatedBytes} bytes, {record.importSeconds:F3}s");
                return record;
            }
            catch { transaction.Rollback(); AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport); throw; }
            finally { if (preview.IsValid()) EditorSceneManager.ClosePreviewScene(preview); }
        }

        public static void VerifyOwned(ArchitectureImportRecord record)
        {
            Require(record.ownedFiles != null && record.ownedFiles.Length > 0, "Missing ownership ledger.");
            foreach (var file in record.ownedFiles)
            {
                Require(File.Exists(file.path) && FileHash(file.path) == file.sha256, "Generated-content conflict: " + file.path + ". Recover/reconcile it; authored overrides belong in the placement variant or scene.");
                if (new[] { ".asset", ".mat", ".prefab" }.Contains(Path.GetExtension(file.path).ToLowerInvariant()) && AssetDatabase.LoadMainAssetAtPath(file.path) is Object asset)
                    Require(!EditorUtility.IsDirty(asset), "Unsaved generated asset conflict: " + file.path);
                if (!file.path.EndsWith(".meta") && AssetImporter.GetAtPath(file.path) is AssetImporter importer)
                    Require(!EditorUtility.IsDirty(importer), "Unsaved generated importer settings conflict: " + file.path);
            }
        }

        static void ValidateBindings(ArchitectureMaterialBindings bindings, JArray objects)
        {
            if (bindings == null) return;
            Require(bindings.bindings != null && bindings.bindings.Select(b => b.bufferId).Distinct().Count() == bindings.bindings.Length, "Duplicate explicit bindings.");
            foreach (var binding in bindings.bindings)
            {
                Require(binding.metricUv0Verified && objects.Any(o => (string)o["name"] == binding.bufferId), "A binding requires exact exported buffer identity and verified metric UV0.");
                Require(!string.IsNullOrWhiteSpace(binding.materialId) && binding.materialId.All(c => char.IsLetterOrDigit(c) || c == '_'), "Invalid library ID.");
                Require(File.Exists(Root + "/Materials/" + binding.materialId + "/material.json"), "Stage the exact baseline material first: " + binding.materialId);
            }
        }

        static string Signature(JObject visual, JObject collision, JObject sidecar)
        {
            JObject Shape(JObject glb) => new JObject
            {
                ["nodes"] = new JArray(glb["nodes"].Select(n => new JObject { ["name"] = n["name"], ["children"] = n["children"], ["mesh"] = n["mesh"] })),
                ["meshes"] = new JArray(glb["meshes"].Select(m => new JObject { ["name"] = m["name"], ["primitives"] = new JArray(m["primitives"].Select(p => new JObject { ["attributes"] = p["attributes"], ["material"] = p["material"] })) }))
            };
            return new JObject { ["visual"] = Shape(visual), ["collision"] = Shape(collision), ["objects"] = sidecar["objects"], ["floor_presentation"] = sidecar["floor_presentation"] }.ToString(Formatting.None);
        }

        static void ValidateContainer(Container data, bool visual)
        {
            var json = data.Json;
            Require((string)json["asset"]?["version"] == "2.0", "Only glTF 2.0 is supported.");
            Require(json["extensionsUsed"] == null || !json["extensionsUsed"].Any(), "Resolve glTF extensions (including texture transforms) before this bounded architecture import.");
            Require(json["skins"] == null && json["animations"] == null, "Static architectural exports only.");
            Require(json["scenes"]?.Count() == 1 && json["scenes"][0]["nodes"]?.Count() == 1, "One building root in one exported scene is required.");
            string[] names = json["nodes"].Select(n => (string)n["name"]).ToArray();
            Require(names.All(n => !string.IsNullOrWhiteSpace(n)) && names.Distinct().Count() == names.Length, "Unique meaningful node names are required for safe prefab updates.");
            foreach (var mesh in json["meshes"])
                foreach (var primitive in mesh["primitives"])
                    Require(primitive["mode"] == null || (int)primitive["mode"] == 4, "Triangle static meshes only.");
            if (!visual) return;
            foreach (var material in json["materials"] ?? new JArray())
            {
                Require(AllowedAlpha.Contains((string)material["alphaMode"] ?? "OPAQUE"), "Transparent architecture needs an explicit shader-compatible pipeline; not silently approximated.");
                Require(material["extensions"] == null, "Unsupported material extensions.");
                Require(material["emissiveTexture"] == null && (material["emissiveFactor"] == null || material["emissiveFactor"].All(v => (float)v == 0)), "Emission requires explicit adapter support.");
                Require(material["occlusionTexture"] == null || (int?)material["occlusionTexture"]?["index"] == (int?)material["pbrMetallicRoughness"]?["metallicRoughnessTexture"]?["index"], "Separate occlusion texture requires explicit adapter support.");
                Require(material["occlusionTexture"] == null || ((int?)material["occlusionTexture"]?["texCoord"] ?? 0) == ((int?)material["pbrMetallicRoughness"]?["metallicRoughnessTexture"]?["texCoord"] ?? 0), "Independent occlusion UV requires explicit adapter support.");
                foreach (var uv in material.SelectTokens("$..texCoord")) Require((int)uv >= 0 && (int)uv <= 3, "PBR adapter supports original UV0 through UV3.");
            }
        }

        static string[] PrepareTextures(Container data, string directory, FileTransaction transaction, HashSet<string> owned)
        {
            var textures = (JArray)data.Json["textures"] ?? new JArray();
            var paths = new string[textures.Count];
            for (int index = 0; index < textures.Count; index++)
            {
                var roles = new HashSet<string>();
                foreach (var material in data.Json["materials"] ?? new JArray())
                {
                    if ((int?)material["pbrMetallicRoughness"]?["baseColorTexture"]?["index"] == index) roles.Add("color");
                    if ((int?)material["pbrMetallicRoughness"]?["metallicRoughnessTexture"]?["index"] == index || (int?)material["occlusionTexture"]?["index"] == index) roles.Add("data");
                    if ((int?)material["normalTexture"]?["index"] == index) roles.Add("normal");
                }
                Require(roles.Count == 1, "Texture usage must have one unambiguous color/data/normal import role.");
                string role = roles.Single();
                var texture = textures[index];
                var image = data.Json["images"][(int)texture["source"]];
                Require(image["bufferView"] != null && ((string)image["mimeType"] == "image/png" || (string)image["mimeType"] == "image/jpeg"), "Use embedded PNG/JPEG textures in the GLB.");
                var view = data.Json["bufferViews"][(int)image["bufferView"]];
                byte[] bytes = data.Bin.Skip((int?)view["byteOffset"] ?? 0).Take((int)view["byteLength"]).ToArray();
                var sampler = texture["sampler"] == null ? new JObject() : data.Json["samplers"][(int)texture["sampler"]];
                Require(((int?)sampler["magFilter"] ?? 9729) == 9729 && ((int?)sampler["minFilter"] ?? 9987) == 9987, "This adapter accepts linear magnification and trilinear mipmapped minification; export that sampler explicitly.");
                string digest = Hash(bytes.Concat(Encoding.UTF8.GetBytes(role + sampler.ToString(Formatting.None))).ToArray());
                string path = Root + "/Shared/Textures/" + digest + ((string)image["mimeType"] == "image/png" ? ".png" : ".jpg");
                transaction.Write(path, bytes); owned.Add(path);
                AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceSynchronousImport);
                var importer = (TextureImporter)AssetImporter.GetAtPath(path);
                Require(importer != null, "Texture importer unavailable.");
                transaction.Track(path + ".meta");
                importer.textureType = role == "normal" ? TextureImporterType.NormalMap : TextureImporterType.Default;
                importer.sRGBTexture = role == "color";
                importer.flipGreenChannel = false;
                importer.textureCompression = TextureImporterCompression.Uncompressed;
                importer.maxTextureSize = 8192;
                importer.mipmapEnabled = true;
                importer.wrapModeU = Wrap((int?)sampler["wrapS"] ?? 10497);
                importer.wrapModeV = Wrap((int?)sampler["wrapT"] ?? 10497);
                importer.filterMode = ((int?)sampler["magFilter"] ?? 9729) == 9728 ? FilterMode.Point : FilterMode.Trilinear;
                importer.SaveAndReimport();
                paths[index] = path;
            }
            return paths;
        }

        static TextureWrapMode Wrap(int value) => value == 10497 ? TextureWrapMode.Repeat : value == 33071 ? TextureWrapMode.Clamp : value == 33648 ? TextureWrapMode.Mirror : throw new InvalidOperationException("Unsupported glTF wrap mode.");

        static Material[] BuildMaterials(JObject json, string[] textures, FileTransaction transaction, HashSet<string> owned)
        {
            var list = new List<Material>();
            foreach (var source in json["materials"])
            {
                var spec = (JObject)source.DeepClone();
                foreach (var index in spec.SelectTokens("$..index").ToArray()) index.Replace(new JValue(textures[(int)index]));
                string path = Root + "/Shared/Materials/" + Hash(Encoding.UTF8.GetBytes(ImporterVersion + spec.ToString(Formatting.None))) + ".mat";
                var material = new Material(Shader.Find("Caelmor/Architecture PBR")) { name = (string)source["name"] };
                var pbr = source["pbrMetallicRoughness"];
                var color = pbr?["baseColorFactor"];
                // Match Unity glTFast's Color-property convention in both Gamma and Linear projects.
                material.SetColor("_Color", color == null ? Color.white : new Color((float)color[0], (float)color[1], (float)color[2], (float)color[3]).gamma);
                material.SetFloat("_Metallic", (float?)pbr?["metallicFactor"] ?? 1);
                material.SetFloat("_Roughness", (float?)pbr?["roughnessFactor"] ?? 1);
                material.SetFloat("_Cull", (bool?)source["doubleSided"] == true ? 0 : 2);
                material.SetFloat("_Cutoff", (string)source["alphaMode"] == "MASK" ? (float?)source["alphaCutoff"] ?? 0.5f : -1);
                void Bind(JToken texture, string prop, string uvProp)
                {
                    if (texture == null) return;
                    material.SetTexture(prop, AssetDatabase.LoadAssetAtPath<Texture2D>(textures[(int)texture["index"]]));
                    material.SetFloat(uvProp, (int?)texture["texCoord"] ?? 0);
                }
                Bind(pbr?["baseColorTexture"], "_MainTex", "_BaseUv");
                Bind(pbr?["metallicRoughnessTexture"], "_OrmTex", "_OrmUv");
                Bind(source["normalTexture"], "_NormalTex", "_NormalUv");
                material.SetFloat("_HasOrm", pbr?["metallicRoughnessTexture"] != null ? 1 : 0);
                material.SetFloat("_HasNormal", source["normalTexture"] != null ? 1 : 0);
                material.SetFloat("_NormalScale", (float?)source["normalTexture"]?["scale"] ?? 1);
                material.SetFloat("_OcclusionStrength", source["occlusionTexture"] != null ? (float?)source["occlusionTexture"]?["strength"] ?? 1 : 0);
                list.Add(SaveMaterial(material, path, transaction, owned));
            }
            return list.ToArray();
        }

        static Material BuildLibraryMaterial(string id, FileTransaction transaction, HashSet<string> owned)
        {
            string directory = Root + "/Materials/" + id;
            var descriptor = JObject.Parse(File.ReadAllText(directory + "/material.json"));
            Require((string)descriptor["id"] == id, "Baseline descriptor identity mismatch.");
            Vector2 repeat = new Vector2(1 / (float)descriptor["scale_m"][0], 1 / (float)descriptor["scale_m"][1]);
            Require(repeat.x > 0 && repeat.y > 0 && !float.IsInfinity(repeat.x) && !float.IsInfinity(repeat.y), "Invalid physical repeat scale.");
            foreach (var pair in new[] { ("color.png", true, false), ("normal.png", false, true), ("metallic_smoothness.png", false, false) })
            {
                string texturePath = directory + "/" + pair.Item1;
                Require(File.Exists(texturePath), "Missing explicit baseline map: " + texturePath);
                AssetDatabase.ImportAsset(texturePath, ImportAssetOptions.ForceSynchronousImport);
                transaction.Track(texturePath + ".meta");
                var importer = (TextureImporter)AssetImporter.GetAtPath(texturePath);
                importer.textureType = pair.Item3 ? TextureImporterType.NormalMap : TextureImporterType.Default;
                importer.sRGBTexture = pair.Item2; importer.flipGreenChannel = false;
                importer.textureCompression = TextureImporterCompression.Uncompressed;
                importer.wrapMode = TextureWrapMode.Repeat; importer.mipmapEnabled = true;
                importer.SaveAndReimport(); owned.Add(texturePath);
            }
            owned.Add(directory + "/material.json");
            var material = new Material(Shader.Find("Standard")) { name = "Caelmor baseline | " + id };
            material.SetTexture("_MainTex", AssetDatabase.LoadAssetAtPath<Texture2D>(directory + "/color.png"));
            material.SetTexture("_BumpMap", AssetDatabase.LoadAssetAtPath<Texture2D>(directory + "/normal.png"));
            material.SetTexture("_MetallicGlossMap", AssetDatabase.LoadAssetAtPath<Texture2D>(directory + "/metallic_smoothness.png"));
            material.SetFloat("_Metallic", 1); material.SetFloat("_GlossMapScale", 1);
            material.EnableKeyword("_NORMALMAP"); material.EnableKeyword("_METALLICGLOSSMAP");
            foreach (string prop in new[] { "_MainTex", "_BumpMap", "_MetallicGlossMap" }) material.SetTextureScale(prop, repeat);
            return SaveMaterial(material, directory + "/" + id + ".mat", transaction, owned);
        }

        static Material SaveMaterial(Material material, string path, FileTransaction transaction, HashSet<string> owned)
        {
            Directory.CreateDirectory(Path.GetDirectoryName(path));
            var existing = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (existing != null) { Object.DestroyImmediate(material); owned.Add(path); return existing; }
            transaction.Track(path); AssetDatabase.CreateAsset(material, path); owned.Add(path); return material;
        }

        static Mesh SaveMesh(Mesh source, string path, int normalUv, FileTransaction transaction, HashSet<string> owned)
        {
            Require(source.isReadable, "Imported mesh must be readable for collision/tangent preparation.");
            var mesh = Object.Instantiate(source);
            if (normalUv >= 0)
            {
                var metric = new List<Vector2>(); var normal = new List<Vector2>();
                mesh.GetUVs(0, metric); mesh.GetUVs(normalUv, normal);
                Require(normal.Count == mesh.vertexCount, "Selected normal texture UV channel is missing.");
                mesh.SetUVs(0, normal); mesh.RecalculateTangents(); mesh.SetUVs(0, metric);
            }
            Directory.CreateDirectory(Path.GetDirectoryName(path));
            transaction.Track(path);
            var existing = AssetDatabase.LoadAssetAtPath<Mesh>(path);
            if (existing == null) AssetDatabase.CreateAsset(mesh, path);
            else { EditorUtility.CopySerialized(mesh, existing); EditorUtility.SetDirty(existing); Object.DestroyImmediate(mesh); mesh = existing; }
            owned.Add(path); return mesh;
        }

        internal static string Relative(string path) => Path.GetRelativePath(Repository, path).Replace('\\', '/');
        static string RelativeUri(string directory, string path) => Path.GetRelativePath(Path.GetFullPath(directory), Path.GetFullPath(path)).Replace('\\', '/');
        public static string Hash(byte[] data) { using var sha = SHA256.Create(); return string.Concat(sha.ComputeHash(data).Select(b => b.ToString("x2"))); }
        public static string FileHash(string path)
        {
            byte[] bytes = File.ReadAllBytes(path);
            string extension = Path.GetExtension(path).ToLowerInvariant();
            if (new[] { ".meta", ".prefab", ".mat", ".json" }.Contains(extension) || extension == ".asset" && Encoding.UTF8.GetString(bytes.Take(10).ToArray()).Contains("%YAML"))
                bytes = Encoding.UTF8.GetBytes(Encoding.UTF8.GetString(bytes).Replace("\r\n", "\n"));
            return Hash(bytes);
        }
        internal static void Require(bool value, string message) { if (!value) throw new InvalidOperationException(message); }

        internal sealed class Container
        {
            public JObject Json;
            public byte[] Bin;
            public static Container Read(string file)
            {
                using var reader = new BinaryReader(File.OpenRead(file));
                Require(reader.ReadUInt32() == 0x46546c67 && reader.ReadUInt32() == 2, "Invalid GLB 2 header.");
                Require(reader.ReadUInt32() == reader.BaseStream.Length, "GLB length mismatch.");
                int length = reader.ReadInt32(); Require(reader.ReadUInt32() == 0x4e4f534a, "Missing GLB JSON chunk.");
                var json = JObject.Parse(Encoding.UTF8.GetString(reader.ReadBytes(length)));
                int binLength = reader.ReadInt32(); Require(reader.ReadUInt32() == 0x004e4942, "Missing GLB BIN chunk.");
                byte[] bin = reader.ReadBytes(binLength); Require(bin.Length == binLength, "Truncated GLB BIN chunk.");
                return new Container { Json = json, Bin = bin };
            }
            public byte[] Write(JObject json)
            {
                byte[] utf8 = Encoding.UTF8.GetBytes(json.ToString(Formatting.None));
                int padded = (utf8.Length + 3) & ~3;
                using var stream = new MemoryStream(); using var writer = new BinaryWriter(stream);
                writer.Write(0x46546c67u); writer.Write(2u); writer.Write((uint)(28 + padded + Bin.Length));
                writer.Write(padded); writer.Write(0x4e4f534au); writer.Write(utf8);
                for (int i = utf8.Length; i < padded; i++) writer.Write((byte)' ');
                writer.Write(Bin.Length); writer.Write(0x004e4942u); writer.Write(Bin);
                return stream.ToArray();
            }
        }

        sealed class FileTransaction
        {
            readonly Dictionary<string, byte[]> originals = new Dictionary<string, byte[]>();
            readonly HashSet<string> originalFolders = new HashSet<string>(Directory.Exists(Root) ? Directory.GetDirectories(Root, "*", SearchOption.AllDirectories).Select(Path.GetFullPath).Append(Path.GetFullPath(Root)) : Array.Empty<string>(), StringComparer.OrdinalIgnoreCase);
            bool committed;
            public void Track(string path)
            {
                if (!originals.ContainsKey(path)) originals[path] = File.Exists(path) ? File.ReadAllBytes(path) : null;
                if (!path.EndsWith(".meta") && !originals.ContainsKey(path + ".meta")) originals[path + ".meta"] = File.Exists(path + ".meta") ? File.ReadAllBytes(path + ".meta") : null;
            }
            public void Write(string path, byte[] data, bool replaceOwned = false)
            {
                if (File.Exists(path))
                {
                    if (File.ReadAllBytes(path).SequenceEqual(data)) return;
                    Require(replaceOwned, "Generated resource conflict at " + path);
                }
                Track(path); Directory.CreateDirectory(Path.GetDirectoryName(path)); File.WriteAllBytes(path, data);
            }
            public void Commit() => committed = true;
            public void Rollback()
            {
                if (committed) return;
                foreach (string path in originals.Keys.Where(p => !p.EndsWith(".meta")))
                    if (AssetDatabase.LoadMainAssetAtPath(path) is Object asset) EditorUtility.ClearDirty(asset);
                foreach (var pair in originals)
                    if (pair.Value == null) { if (File.Exists(pair.Key)) File.Delete(pair.Key); }
                    else File.WriteAllBytes(pair.Key, pair.Value);
                if (Directory.Exists(Root))
                    foreach (string directory in Directory.GetDirectories(Root, "*", SearchOption.AllDirectories).OrderByDescending(p => p.Length))
                        if (!originalFolders.Contains(Path.GetFullPath(directory)) && !Directory.EnumerateFileSystemEntries(directory).Any())
                        {
                            Directory.Delete(directory);
                            if (File.Exists(directory + ".meta")) File.Delete(directory + ".meta");
                        }
                foreach (string path in originals.Keys.Where(p => !p.EndsWith(".meta") && File.Exists(p)))
                    AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate | ImportAssetOptions.ForceSynchronousImport);
            }
        }
    }
}
