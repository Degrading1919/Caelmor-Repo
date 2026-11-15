using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using Object = UnityEngine.Object;

namespace Caelmor.Unity.Editor
{
    public static partial class ArchitectureImport
    {
        const string CollisionPrefix = "Collision | ";
        const string GuidedSignatureTag = "guided:";
        const string GuidedPrefix = "world_lowmark.lowmark_main_hall.guide.";
        static readonly Regex GuidePart = new Regex(@"^world_lowmark\.lowmark_main_hall\.guide\.([0-9a-f]{32})\.[a-z0-9_]+$", RegexOptions.CultureInvariant);
        static readonly Regex CollisionName = new Regex(@"^(Collider (?:Wall|Floor) \d{2}-\d{2}|Collider Approach [0-9a-f]{32})(?:\.\d{3,})?$", RegexOptions.CultureInvariant);
        static readonly Regex BuildingId = new Regex(@"^[0-9a-f]{32}$", RegexOptions.CultureInvariant);
        const string Reconcile = " Keep the existing placement and reconcile the source/overrides, or import using a new key.";

        static string Text(JToken token, string key) => (string)token?[key];
        static string VisualKey(JToken extras, string name)
        {
            if ((bool?)extras?["caelm_anchor"] == true) return "anchor";
            if (Text(extras, "caelm_floor_group") is string floor) return "floor:" + floor;
            if (Text(extras, "caelm_buffer_id") is string buffer) return "section:" + buffer;
            return "node:" + name;
        }

        static string CollisionKey(string name, JToken extras = null)
        {
            if ((bool?)extras?["caelm_anchor"] == true) return "anchor";
            var match = CollisionName.Match(name);
            string stableName = match.Success ? match.Groups[1].Value : name;
            string authored = Text(extras, "caelm_collider_id");
            Require(authored == null || (match.Success && authored == stableName), "Collision stable identity disagrees with " + name + "." + Reconcile);
            return stableName;
        }

        static string GuideId(JToken extras)
        {
            string source = Text(extras, "caelm_source_buffer_id") ?? Text(extras, "caelm_buffer_id")?.Split(new[] { "::" }, StringSplitOptions.None)[0];
            return source != null && GuidePart.Match(source) is Match { Success: true } match ? match.Groups[1].Value : null;
        }

        static GuidedUpdate PlanGuidedUpdate(ArchitectureImportRecord previous, Container visual, Container collision, JObject sidecar, string directory)
        {
            var priorVisual = Container.Read(directory + "/visual.glb");
            // Once a placement has been reconciled, its saved names remain authoritative even after the last guide is removed.
            if (previous.compatibilitySignature?.StartsWith(GuidedSignatureTag, StringComparison.Ordinal) != true &&
                !priorVisual.Json["nodes"].Concat(visual.Json["nodes"]).Any(n => GuideId(n["extras"]) != null)) return null;
            var priorCollision = Container.Read(directory + "/collision.glb");
            var priorSidecar = JObject.Parse(File.ReadAllText(directory + "/source.caelmor.json"));
            string building = Text(sidecar["floor_presentation"], "building_id");
            Require(building != null && BuildingId.IsMatch(building) && building == previous.buildingId &&
                building == Text(priorSidecar["floor_presentation"], "building_id"),
                "Guided update changed the source building ID." + Reconcile);
            Require(Text(sidecar, "architecture") == "WORLD" && Text(sidecar["settings"], "region") == "LOWMARK" &&
                (bool?)sidecar["settings"]?["floor_separation"] == true &&
                sidecar["construction_zones"] is JArray zones && zones.Any(z => Text(z, "key") == "lowmark_main_hall"),
                "Guided update requires the exported Lowmark main hall and its authored floor separation." + Reconcile);
            foreach (string field in new[] { "architecture", "functional_program", "floor_presentation", "units", "up_axis" })
                Require(JToken.DeepEquals(priorSidecar[field], sidecar[field]), "Guided update changed " + field + "." + Reconcile);
            Require(JToken.DeepEquals(Without(priorSidecar["anchor"], "name"), Without(sidecar["anchor"], "name")), "Guided update moved or changed the building anchor." + Reconcile);
            JArray ZoneLayout(JToken values) => new JArray(values.Select(z => Without(z, "triangles", "vertices")));
            Require(JToken.DeepEquals(ZoneLayout(priorSidecar["construction_zones"]), ZoneLayout(sidecar["construction_zones"])),
                "Guided update changed the construction-zone layout." + Reconcile);
            var before = new GuidedShape(priorVisual.Json, priorCollision.Json, priorSidecar, building);
            var after = new GuidedShape(visual.Json, collision.Json, sidecar, building);
            var retiredComponents = before.Visual.Values.Where(s => s.Guide != null).Select(s => s.Guide)
                .Except(after.Visual.Values.Select(s => s.Guide)).SelectMany(id => new[] { "frame", "leaf", "shutters" }
                    .Select(part => "lowmark_main_hall/guide." + id + "." + part)).ToHashSet();
            var priorSettings = (JObject)priorSidecar["settings"].DeepClone();
            if (priorSettings["construction_overrides"] is JObject overrides && overrides["by_component"] is JObject components)
            {
                foreach (string component in retiredComponents) components.Remove(component);
                if (!components.Properties().Any()) overrides.Remove("by_component");
            }
            Require(JToken.DeepEquals(priorSettings, sidecar["settings"]), "Guided update changed the exported generation settings." + Reconcile);
            CompareSections(before.Visual, after.Visual);
            CompareSections(before.Collision, after.Collision);
            return new GuidedUpdate(previous, directory, before, after);
        }

        static JObject Without(JToken token, params string[] keys) =>
            token is JObject obj ? new JObject(obj.Properties().Where(p => !keys.Contains(p.Name)).Select(p => p.DeepClone())) : null;

        sealed class GuidedSection
        {
            public string Key, Name, Parent, Guide;
            public JToken Contract;
            public bool HasMesh;
        }

        sealed class GuidedShape
        {
            public readonly Dictionary<string, GuidedSection> Visual, Collision;

            public GuidedShape(JObject visual, JObject collision, JObject sidecar, string building)
            {
                var objects = ((JArray)sidecar["objects"]).ToDictionary(o => Text(o, "name"));
                Visual = Read(visual, objects, building);
                Collision = Read(collision, null, building);
                var guides = Visual.Values.Where(s => s.Guide != null).Select(s => s.Guide).ToHashSet();
                Require(Collision.Values.All(s => s.Guide == null || guides.Contains(s.Guide)), "An approach collider does not match an exported opening guide." + Reconcile);
                Require(Visual.Values.Count(s => s.HasMesh) == objects.Count && Collision.Values.Count(s => s.HasMesh) == (int)sidecar["collision"]["object_count"],
                    "Guided update GLBs and sidecar section counts disagree." + Reconcile);
            }

            static Dictionary<string, GuidedSection> Read(JObject glb, Dictionary<string, JToken> objects, string building)
            {
                bool visual = objects != null;
                var nodes = (JArray)glb["nodes"];
                int root = (int)glb["scenes"][0]["nodes"][0];
                string Key(JToken n) => visual ? VisualKey(n["extras"], Text(n, "name")) :
                    (n == nodes[root] ? "anchor" : CollisionKey(Text(n, "name"), n["extras"]));
                var parents = new Dictionary<int, string>();
                foreach (var node in nodes)
                    foreach (int child in node["children"] ?? new JArray())
                    {
                        Require(child >= 0 && child < nodes.Count && !parents.ContainsKey(child), "Guided GLB hierarchy is ambiguous." + Reconcile);
                        parents.Add(child, Key(node));
                    }
                Require(Key(nodes[root]) == "anchor" && Text(nodes[root]["extras"], "caelm_building_id") == building &&
                    parents.Count == nodes.Count - 1 && !parents.ContainsKey(root),
                    "Guided GLB does not have one authored building root." + Reconcile);
                var sections = new Dictionary<string, GuidedSection>();
                for (int i = 0; i < nodes.Count; i++)
                {
                    var node = nodes[i];
                    var extras = node["extras"];
                    string name = Text(node, "name"), key = Key(node);
                    bool hasMesh = node["mesh"] != null;
                    string guide = visual ? GuideId(extras) :
                        key.StartsWith("Collider Approach ", StringComparison.Ordinal) && CollisionName.IsMatch(key) ? key.Substring("Collider Approach ".Length) : null;
                    Require(!sections.ContainsKey(key), "Guided update cannot match duplicate stable section " + key + "." + Reconcile);
                    Require(!visual || !hasMesh || key.StartsWith("section:", StringComparison.Ordinal) && objects.ContainsKey(name),
                        "Guided update needs stable visual buffer metadata for " + name + "." + Reconcile);
                    Require(!visual || Text(extras, "caelm_building_id") == building, "Visual section " + key + " belongs to a different building." + Reconcile);
                    Require(!visual || !(Text(extras, "caelm_source_buffer_id") ?? name).StartsWith(GuidedPrefix, StringComparison.Ordinal) || guide != null,
                        "Guided section " + key + " has no stable guide ID." + Reconcile);
                    var contract = new JObject
                    {
                        ["metadata"] = Without(extras, "caelm_floor_min", "caelm_floor_max", "caelm_collider_id",
                            "caelm_build_id", "caelm_component_source_hash", "caelm_surface_material", "caelm_surface_fingerprint"),
                        ["transform"] = guide != null && visual ? null : new JObject(new[] { "translation", "rotation", "scale", "matrix" }
                            .Where(k => node[k] != null).Select(k => new JProperty(k, node[k]))),
                        ["slots"] = hasMesh ? MeshSlots(glb, node, visual) : null
                    };
                    if (visual && hasMesh)
                    {
                        var obj = Without(objects[name], "name", "component_source_hash", "surface_material", "surface_fingerprint");
                        if (obj["floor_section"] != null) obj["floor_section"] = Without(obj["floor_section"], "floor_min", "floor_max");
                        contract["object"] = obj;
                        if (guide != null)
                        {
                            string volume = Text(extras, "caelm_floor_volume"), visibility = Text(extras, "caelm_visibility");
                            int? floor = (int?)extras["caelm_floor_index"];
                            string suffix = visibility == "FLOOR" ? $"::floor:{volume}:{floor}" : "::" + visibility?.ToLowerInvariant();
                            Require(volume == "lowmark_main_hall" && floor.HasValue && !string.IsNullOrEmpty(visibility) &&
                                Text(extras, "caelm_buffer_id") == Text(extras, "caelm_source_buffer_id") + suffix &&
                                parents.GetValueOrDefault(i) == $"floor:{volume}/{visibility}/{floor}" && (bool?)obj["protected"] != true,
                                "Guided section " + key + " is outside the supported host or is protected in Blender." + Reconcile);
                        }
                    }
                    sections.Add(key, new GuidedSection { Key = key, Name = name, HasMesh = hasMesh, Parent = parents.GetValueOrDefault(i), Guide = guide, Contract = contract });
                }
                return sections;
            }

            static JArray MeshSlots(JObject glb, JToken node, bool visual)
            {
                var primitives = (JArray)glb["meshes"][(int)node["mesh"]]["primitives"];
                return new JArray(primitives.Select(p => new JObject
                {
                    ["attributes"] = new JObject(((JObject)p["attributes"]).Properties().Select(a =>
                    {
                        JToken accessor = glb["accessors"][(int)a.Value];
                        return new JProperty(a.Name, new JArray(accessor["type"], accessor["componentType"], (bool?)accessor["normalized"] ?? false));
                    })),
                    // Blender exports one generated palette slot per section. Numeric material/texture indices and baked maps are allowed to change.
                    ["material"] = visual && primitives.Count > 1 && p["material"] != null ? Text(glb["materials"][(int)p["material"]], "name") : null
                }));
            }
        }

        static void CompareSections(Dictionary<string, GuidedSection> before, Dictionary<string, GuidedSection> after)
        {
            foreach (string key in before.Keys.Union(after.Keys))
            {
                before.TryGetValue(key, out var old);
                after.TryGetValue(key, out var updated);
                if (old == null || updated == null)
                {
                    var section = old ?? updated;
                    Require(section.HasMesh && section.Guide != null, "Guided update added, removed, or renamed a section outside the guides: " + key + "." + Reconcile);
                    continue;
                }
                Require(old.Parent == updated.Parent && old.Guide == updated.Guide && old.HasMesh == updated.HasMesh,
                    "Guided update changed hierarchy or ownership of " + key + "." + Reconcile);
                Require(JToken.DeepEquals(old.Contract, updated.Contract),
                    "Guided update changed the section/material slot contract of " + key + "." + Reconcile);
            }
        }

        static readonly Regex UnityAssetReference = new Regex(@"\{\s*fileID:\s*(-?\d+),\s*guid:\s*([0-9a-f]{32})\b", RegexOptions.CultureInvariant);
        static readonly HashSet<string> UnityLinks = new HashSet<string>
        {
            "m_CorrespondingSourceObject", "m_PrefabInstance", "m_PrefabAsset", "m_GameObject", "m_Component", "m_Father", "m_Children"
        };

        static void VerifyAuthorReferences(ArchitectureImportRecord previous, GameObject[] retired, string[] meshes, string directory)
        {
            var retiredObjects = retired.SelectMany(obj => new[] { (Object)obj }.Concat(obj.GetComponents<Component>())).ToHashSet();
            var meshPaths = meshes.ToHashSet();
            var privateSources = new[] { directory + "/visual.glb", directory + "/collision.glb" }.ToHashSet();
            var watchedGuids = privateSources.Select(AssetDatabase.AssetPathToGUID).Concat(meshes.Select(AssetDatabase.AssetPathToGUID)).ToHashSet();
            var watchedIds = new HashSet<(string guid, string id)>();
            void WatchId(Object obj)
            {
                if (AssetDatabase.TryGetGUIDAndLocalFileIdentifier(obj, out string guid, out long id) && id != 0)
                    watchedIds.Add((guid, id.ToString(System.Globalization.CultureInfo.InvariantCulture)));
                else if (retiredObjects.Contains(obj))
                    Require(false, "Cannot guard references to retired guided section " + obj.name + "." + Reconcile);
            }
            foreach (var obj in retiredObjects) WatchId(obj);

            // Inherited child IDs may be serialized against a derived variant rather than the source prefab.
            var owned = previous.ownedFiles.Where(f => f.path.StartsWith(directory + "/", StringComparison.Ordinal)).Select(f => f.path).ToHashSet();
            var dependents = new Dictionary<string, string[]>();
            foreach (string path in AssetDatabase.GetAllAssetPaths())
            {
                if (!path.StartsWith("Assets/", StringComparison.Ordinal) || owned.Contains(path) || !File.Exists(path)) continue;
                var direct = AssetDatabase.GetDependencies(path, false);
                if (direct.Length > 0) dependents.Add(path, direct);
            }
            var relevant = new HashSet<string>(meshPaths.Concat(privateSources)) { previous.generatedPrefab };
            bool expanded;
            do
            {
                expanded = false;
                foreach (var pair in dependents)
                    if (!relevant.Contains(pair.Key) && pair.Value.Any(relevant.Contains)) expanded |= relevant.Add(pair.Key);
            }
            while (expanded);

            bool Retired(Object obj) => obj != null && (retiredObjects.Contains(obj)
                || retiredObjects.Contains(PrefabUtility.GetCorrespondingObjectFromSourceAtPath(obj, previous.generatedPrefab)));
            bool Referenced(Object obj)
            {
                if (obj == null) return false;
                string path = AssetDatabase.GetAssetPath(obj);
                return meshPaths.Contains(path) || privateSources.Contains(path) || Retired(obj);
            }
            string Help(string location, string detail) => "Guided update would invalidate " + detail + " in " + location +
                ". Move or clear the authored reference/override and retry, or keep this import under a separate key.";

            if (retiredObjects.Count > 0)
                foreach (string path in relevant.Where(p => p.EndsWith(".prefab", StringComparison.OrdinalIgnoreCase) && p != previous.generatedPrefab))
                {
                    var asset = AssetDatabase.LoadAssetAtPath<GameObject>(path);
                    if (asset == null) continue;
                    foreach (var t in asset.GetComponentsInChildren<Transform>(true))
                        foreach (var obj in new[] { (Object)t.gameObject }.Concat(t.GetComponents<Component>()))
                            if (Retired(obj)) WatchId(obj);
                }

            foreach (string path in relevant.Where(dependents.ContainsKey))
            {
                var direct = dependents[path];
                Require(!direct.Any(privateSources.Contains), Help(path, "a reference to a private generated GLB"));
                Require(!direct.Any(meshPaths.Contains), Help(path, "a reference to a removed guided mesh"));
                if (retiredObjects.Count == 0) continue;
                using var reader = new StreamReader(path);
                var header = new char[5];
                bool yaml = reader.ReadBlock(header, 0, header.Length) == header.Length && new string(header) == "%YAML";
                Require(yaml || !direct.Any(p => relevant.Contains(p) && p.EndsWith(".prefab", StringComparison.OrdinalIgnoreCase)),
                    Help(path, "a non-text prefab dependency that cannot be checked for removed guide references"));
                if (!yaml) continue;
                foreach (Match reference in UnityAssetReference.Matches(reader.ReadToEnd()))
                    Require(!watchedGuids.Contains(reference.Groups[2].Value) && !watchedIds.Contains((reference.Groups[2].Value, reference.Groups[1].Value)),
                        Help(path, "a saved reference or override to a removed guided section"));
            }

            void CheckProperties(Object obj, string label)
            {
                var serialized = new SerializedObject(obj);
                var current = serialized.GetIterator();
                bool enter = true;
                while (current.Next(enter))
                {
                    enter = !UnityLinks.Contains(current.name);
                    if (enter && current.propertyType == SerializedPropertyType.ObjectReference)
                        Require(!Referenced(current.objectReferenceValue), Help(label, "a live object reference (" + obj.name + "." + current.propertyPath + ")"));
                }
            }

            void CheckScene(Scene scene, GameObject[] roots)
            {
                string label = string.IsNullOrEmpty(scene.path) ? scene.name + " (unsaved scene)" : scene.path;
                foreach (var transform in roots.SelectMany(root => root.GetComponentsInChildren<Transform>(true)))
                {
                    var obj = transform.gameObject;
                    if (PrefabUtility.IsAnyPrefabInstanceRoot(obj) && retiredObjects.Count > 0)
                    {
                        foreach (var mod in PrefabUtility.GetPropertyModifications(obj) ?? Array.Empty<PropertyModification>())
                            Require(!Referenced(mod.target) && !Referenced(mod.objectReference), Help(label, "a live prefab override (" + mod.propertyPath + ")"));
                        foreach (var added in PrefabUtility.GetAddedGameObjects(obj))
                            Require(!Retired(added.instanceGameObject.transform.parent), Help(label, "a child added to a removed guided section"));
                        foreach (var added in PrefabUtility.GetAddedComponents(obj))
                            Require(!Retired(added.instanceComponent.gameObject), Help(label, "a component added to a removed guided section"));
                        foreach (var removed in PrefabUtility.GetRemovedGameObjects(obj))
                            Require(!Retired(removed.assetGameObject), Help(label, "a removed-object override on a guided section"));
                        foreach (var removed in PrefabUtility.GetRemovedComponents(obj))
                            Require(!Retired(removed.assetComponent), Help(label, "a removed-component override on a guided section"));
                    }
                    if (!Retired(obj))
                        foreach (var component in obj.GetComponents<Component>().Where(c => c != null))
                            CheckProperties(component, label);
                }
            }

            for (int i = 0; i < SceneManager.sceneCount; i++)
            {
                var scene = SceneManager.GetSceneAt(i);
                if (scene.isLoaded) CheckScene(scene, scene.GetRootGameObjects());
            }
            var stage = PrefabStageUtility.GetCurrentPrefabStage();
            if (stage != null)
            {
                Require(retiredObjects.Count == 0 || !stage.scene.isDirty || !relevant.Contains(stage.assetPath),
                    "An affected prefab is open with unsaved changes in Prefab Mode: " + stage.assetPath + ". Save it or close Prefab Mode before removing a guided section.");
                CheckScene(stage.scene, new[] { stage.prefabContentsRoot });
            }
            foreach (var asset in Resources.FindObjectsOfTypeAll<ScriptableObject>())
            {
                string path = AssetDatabase.GetAssetPath(asset);
                if (EditorUtility.IsDirty(asset) && path.StartsWith("Assets/", StringComparison.Ordinal) && !owned.Contains(path)) CheckProperties(asset, path);
            }
        }

        sealed class GuidedUpdate
        {
            readonly ArchitectureImportRecord previous;
            readonly string directory;
            readonly Dictionary<string, GuidedSection> visualByName, collisionByName;
            readonly Dictionary<string, GameObject> oldPrefab;
            readonly Dictionary<string, string> meshPaths = new Dictionary<string, string>();
            readonly Dictionary<string, string[]> stableIds = new Dictionary<string, string[]>();
            readonly string[] retiredMeshPaths;
            public IEnumerable<string> PreviousSharedPaths => previous.ownedFiles.Select(f => f.path)
                .Where(p => !p.EndsWith(".meta", StringComparison.Ordinal) && !p.StartsWith(directory + "/", StringComparison.Ordinal));

            public GuidedUpdate(ArchitectureImportRecord previous, string directory, GuidedShape before, GuidedShape after)
            {
                this.previous = previous;
                this.directory = directory;
                var old = AssetDatabase.LoadAssetAtPath<GameObject>(previous.generatedPrefab);
                Require(old != null, "The generated prefab is missing. Recover it before reimport.");
                oldPrefab = PrefabSections(old);
                visualByName = after.Visual.Values.ToDictionary(s => s.Name);
                collisionByName = after.Collision.Values.ToDictionary(s => s.Name);
                var beforeKeys = PrefabKeys(before).ToHashSet();
                var afterKeys = PrefabKeys(after).ToHashSet();
                Require(beforeKeys.SetEquals(oldPrefab.Keys), "The owned prefab hierarchy does not match the previously imported source." + Reconcile);
                Require(oldPrefab.Values.Select(o => o.name).Distinct().Count() == oldPrefab.Count, "The owned prefab contains duplicate object names; safe Unity fileID matching is not possible." + Reconcile);
                foreach (var pair in oldPrefab.Where(p => afterKeys.Contains(p.Key)))
                    stableIds.Add(pair.Key, ObjectIds(pair.Value));
                var retired = oldPrefab.Where(p => !afterKeys.Contains(p.Key)).Select(p => p.Value).ToArray();
                retiredMeshPaths = retired.Select(MeshInSection).Select(AssetDatabase.GetAssetPath).Distinct().ToArray();
                foreach (var section in after.Visual.Values.Where(s => s.HasMesh)) PlanMesh("visual:", section);
                foreach (var section in after.Collision.Values.Where(s => s.HasMesh)) PlanMesh("collision:", section);
                Require(!meshPaths.Values.Intersect(retiredMeshPaths).Any(), "A retired guided section unexpectedly shares a retained prepared mesh." + Reconcile);
                foreach (string path in retiredMeshPaths) RequireOwnedMesh(path);
                VerifyAuthorReferences(previous, retired, retiredMeshPaths, directory);
            }

            static IEnumerable<string> PrefabKeys(GuidedShape shape) => new[] { "prefab", "visual", "collision" }
                .Concat(shape.Visual.Keys.Select(k => "visual:" + k)).Concat(shape.Collision.Keys.Select(k => "collision:" + k));

            static Dictionary<string, GameObject> PrefabSections(GameObject root)
            {
                Require(root.transform.childCount == 2, "Expected the generated visual and collision branches." + Reconcile);
                var collision = root.transform.Cast<Transform>().SingleOrDefault(t => t.name == CollisionPrefix + "Collision (generated)");
                Require(collision != null, "Generated collision branch is missing." + Reconcile);
                var visual = root.transform.Cast<Transform>().Single(t => t != collision);
                var result = new Dictionary<string, GameObject> { ["prefab"] = root, ["visual"] = visual.gameObject, ["collision"] = collision.gameObject };
                void Add(string key, GameObject obj)
                {
                    Require(!result.ContainsKey(key), "Generated prefab has duplicate stable identity " + key + "." + Reconcile);
                    result.Add(key, obj);
                }
                foreach (var id in visual.GetComponentsInChildren<ArchitectureIdentity>(true))
                    Add("visual:" + VisualKey(JObject.Parse(id.sourceMetadata), id.name), id.gameObject);
                Require(collision.childCount == 1, "Generated collision root no longer matches the source hierarchy." + Reconcile);
                foreach (var t in collision.GetComponentsInChildren<Transform>(true).Where(t => t != collision))
                {
                    Require(t.name.StartsWith(CollisionPrefix, StringComparison.Ordinal), "Owned collision name cannot be matched: " + t.name + "." + Reconcile);
                    Add(t == collision.GetChild(0) ? "collision:anchor" : "collision:" + CollisionKey(t.name.Substring(CollisionPrefix.Length)), t.gameObject);
                }
                return result;
            }

            static Mesh MeshInSection(GameObject obj)
            {
                var filter = obj.GetComponent<MeshFilter>();
                if (filter != null) return filter.sharedMesh;
                var collider = obj.GetComponent<MeshCollider>();
                return collider != null ? collider.sharedMesh : null;
            }

            void RequireOwnedMesh(string path) =>
                Require(!string.IsNullOrEmpty(path) && path.StartsWith(directory + "/Meshes/", StringComparison.Ordinal) &&
                    previous.ownedFiles.Any(f => f.path == path) && previous.ownedFiles.Any(f => f.path == path + ".meta"),
                    "Expected an owned, per-building prepared mesh at " + path + "." + Reconcile);

            void PlanMesh(string branch, GuidedSection section)
            {
                string logicalId = branch + section.Key;
                string path;
                if (oldPrefab.TryGetValue(logicalId, out var prior))
                {
                    path = AssetDatabase.GetAssetPath(MeshInSection(prior));
                    RequireOwnedMesh(path);
                }
                else
                {
                    path = directory + "/Meshes/guide_" + Hash(Encoding.UTF8.GetBytes(logicalId)).Substring(0, 20) + ".asset";
                    Require(!File.Exists(path) && !File.Exists(path + ".meta"), "Unowned geometry occupies the new guided mesh path " + path + "." + Reconcile);
                }
                Require(!meshPaths.Values.Contains(path), "Guided sections must use separate prepared meshes at " + path + "." + Reconcile);
                meshPaths.Add(logicalId, path);
            }

            public string VisualBindingName(string name) => oldPrefab.TryGetValue("visual:" + visualByName[name].Key, out var prior) ? prior.name : name;
            public string MeshPath(string name, bool collision) => collision ?
                meshPaths["collision:" + collisionByName[name].Key] : meshPaths["visual:" + visualByName[name].Key];

            public void ReusePrefabNames(GameObject generated, GameObject visual, GameObject collision, Dictionary<string, Transform> visuals)
            {
                var expected = new Dictionary<string, GameObject> { ["prefab"] = generated, ["visual"] = visual, ["collision"] = collision };
                foreach (var part in visualByName.Values) expected.Add("visual:" + part.Key, visuals[part.Name].gameObject);
                var collisionNames = collision.GetComponentsInChildren<Transform>(true).ToDictionary(t => t.name);
                foreach (var part in collisionByName.Values) expected.Add("collision:" + part.Key, collisionNames[CollisionPrefix + part.Name].gameObject);
                Require(expected.Count == generated.GetComponentsInChildren<Transform>(true).Length, "Imported guided prefab contains unexpected scene objects." + Reconcile);
                var reserved = oldPrefab.Values.Select(o => o.name).ToHashSet();
                foreach (var pair in expected.OrderBy(p => p.Key, StringComparer.Ordinal))
                {
                    if (oldPrefab.TryGetValue(pair.Key, out var prior)) pair.Value.name = prior.name;
                    else Require(reserved.Add(pair.Value.name), "New guided object " + pair.Value.name + " conflicts with an existing generated object name." + Reconcile);
                }
            }

            public void VerifySavedPrefab(GameObject saved)
            {
                var actual = PrefabSections(saved);
                Require(actual.Count == 3 + visualByName.Count + collisionByName.Count, "Saved prefab has an unexpected number of guided sections. Import rolled back.");
                foreach (var pair in stableIds)
                    Require(actual.TryGetValue(pair.Key, out var section) && pair.Value.SequenceEqual(ObjectIds(section)),
                        "Unity changed an existing GUID/fileID for " + pair.Key + ". Import rolled back." + Reconcile);
                foreach (var pair in meshPaths)
                    Require(actual.TryGetValue(pair.Key, out var section) && AssetDatabase.GetAssetPath(MeshInSection(section)) == pair.Value,
                        "Saved guided geometry did not bind to its expected mesh for " + pair.Key + ". Import rolled back.");
            }

            static string[] ObjectIds(GameObject obj) => new[] { (Object)obj }.Concat(obj.GetComponents<Component>())
                .Concat(MeshInSection(obj) is Mesh mesh ? new Object[] { mesh } : Array.Empty<Object>())
                .Select(o =>
                {
                    Require(AssetDatabase.TryGetGUIDAndLocalFileIdentifier(o, out string guid, out long id) && id != 0,
                        "Cannot verify Unity fileID for " + obj.name + "." + Reconcile);
                    return o.GetType().FullName + ":" + guid + ":" + id;
                }).OrderBy(id => id, StringComparer.Ordinal).ToArray();

            public void RetireMeshes(FileTransaction transaction)
            {
                foreach (string path in retiredMeshPaths)
                {
                    transaction.Track(path);
                    Require(AssetDatabase.DeleteAsset(path), "Unity could not retire the unreferenced guided mesh " + path + ". Import rolled back.");
                }
            }
        }
    }
}
