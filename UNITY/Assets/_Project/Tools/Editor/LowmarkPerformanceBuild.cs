using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using Object = UnityEngine.Object;

namespace Caelmor.Unity.Editor
{
    internal static class LowmarkPerformanceBuild
    {
        const string Scratch = "Assets/__LowmarkPerformance";
        static readonly string[] Buildings = { "farmhouse", "cottage", "workshop" };

        public static void Build()
        {
            CaelmorSceneOwnership.RequireCleanScenes();
            if (GraphicsSettings.defaultRenderPipeline != null)
                throw new InvalidOperationException("This benchmark requires Built-in rendering.");
            string source = Environment.GetEnvironmentVariable("CAELMOR_PERF_SOURCE");
            string output = Environment.GetEnvironmentVariable("CAELMOR_PERF_BUILDS");
            if (!File.Exists(Path.Combine(source,"export.json")) || string.IsNullOrWhiteSpace(output))
                throw new InvalidOperationException("Set the exported input and build directories.");
            string mode = Environment.GetEnvironmentVariable("CAELMOR_PERF_COMPRESSED");
            bool compressed = mode == "1";
            bool noMips = mode == "2";
            var setup = EditorSceneManager.GetSceneManagerSetup();
            string previousRoot = ArchitectureImport.Root;
            try
            {
                string marker = Scratch + "/caelmor-perf-owner.txt";
                if (Directory.Exists(Scratch) && !File.Exists(marker))
                    throw new InvalidOperationException("Reserved benchmark directory already exists.");
                if (File.Exists(marker))
                {
                    string[] owner = File.ReadAllLines(marker);
                    if (owner.Length == 0 || owner[0] != "Disposable Lowmark benchmark assets")
                        throw new InvalidOperationException("The benchmark directory has an invalid ownership marker.");
                    if (owner.Length == 2 && owner[1] != source && !AssetDatabase.DeleteAsset(Scratch))
                        throw new IOException("Could not replace disposable benchmark inputs.");
                }
                Directory.CreateDirectory(Scratch);
                File.WriteAllLines(marker,new[] {"Disposable Lowmark benchmark assets",source});
                ArchitectureImport.Root = Scratch + "/Architecture";
                JObject export = JObject.Parse(File.ReadAllText(Path.Combine(source,"export.json")));
                var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
                var harness = new GameObject("Lowmark standalone benchmark").AddComponent<LowmarkPerformance>();
                harness.inspection = new GameObject("Fixed camera").AddComponent<Camera>();
                harness.inspection.renderingPath = RenderingPath.Forward;
                harness.inspection.clearFlags = CameraClearFlags.SolidColor;
                harness.inspection.backgroundColor = new Color(.38f,.47f,.56f);
                harness.inspection.farClipPlane = 200;
                harness.views = new[] { "Settlement","Materials" }.Select(name => MakeView(name,export["cameras"][name])).ToArray();
                var light = new GameObject("Fixed sun").AddComponent<Light>();
                light.type = LightType.Directional;
                light.transform.rotation = Quaternion.Euler(48,-32,0);
                light.intensity = 1.1f;
                light.shadows = LightShadows.Hard;
                RenderSettings.ambientMode = AmbientMode.Flat;
                RenderSettings.ambientLight = new Color(.47f,.47f,.47f);
                AddGround(source, scene);

                var roots = new List<GameObject>();
                var approvedRoofMaterials = new Dictionary<string, Material[]>();
                foreach (string variant in new[] {"showcase","0","50","100"})
                {
                    var root = new GameObject(variant);
                    var materialSets = new List<HashSet<Material>>();
                    foreach (string building in Buildings)
                    {
                        string detail = variant == "showcase" ? export[building]["detail"].ToString() : variant;
                        string key = building + "_" + detail;
                        var record = LoadOrImport(source,key);
                        Debug.Log($"CAELMOR_PERF_IMPORT {key} triangles={record.triangles} renderers={record.rendererCount} textures={record.textureCount}");
                        var asset = AssetDatabase.LoadAssetAtPath<GameObject>(record.placementPrefab);
                        var placed = (GameObject)PrefabUtility.InstantiatePrefab(asset,scene);
                        placed.transform.SetParent(root.transform,false);
                        // The roof generator's default trim materials differ from
                        // the showcase bindings. Keep trim constant across detail runs.
                        foreach (var renderer in placed.GetComponentsInChildren<MeshRenderer>())
                        {
                            var identity = renderer.GetComponent<ArchitectureIdentity>();
                            if (identity == null) continue;
                            string name = System.Text.RegularExpressions.Regex.Replace(renderer.name, @"\.\d{3}$", "");
                            string materialKey = building + "/" + name;
                            if (variant == "showcase") approvedRoofMaterials[materialKey] = renderer.sharedMaterials;
                            else if (approvedRoofMaterials.TryGetValue(materialKey,out var approved) &&
                                     approved.Length == renderer.sharedMaterials.Length) renderer.sharedMaterials = approved;
                        }
                        materialSets.Add(placed.GetComponentsInChildren<MeshRenderer>()
                            .SelectMany(r=>r.sharedMaterials).ToHashSet());
                    }
                    if (variant == "showcase")
                    {
                        var shared = materialSets[0].Where(m => materialSets.Skip(1).All(s => s.Contains(m))).ToArray();
                        harness.commonMaterials = shared.Length;
                        Debug.Log("CAELMOR_PERF_SHARED " + string.Join(" | ",shared.Select(m=>m.name)));
                        if (shared.Length == 0) throw new InvalidOperationException("Expected common material assets.");
                    }
                    root.SetActive(roots.Count == 0);
                    roots.Add(root);
                }
                harness.roofVariants = roots.ToArray();
                AddFoliage(source,harness);
                harness.configuration = compressed ? "compressed_streaming_nonreadable" : noMips ? "uncompressed_nomips" : "baseline";
                if (compressed || noMips) ConfigureTextures(harness,compressed);
                string path = Scratch + "/LowmarkPerformance.unity";
                if (!EditorSceneManager.SaveScene(scene,path)) throw new IOException("Cannot save benchmark scene.");
                Directory.CreateDirectory(output);
                var result = BuildPipeline.BuildPlayer(new BuildPlayerOptions {
                    scenes = new[] { path },
                    locationPathName = Path.Combine(output,harness.configuration,"LowmarkPerformance.exe"),
                    target = BuildTarget.StandaloneWindows64, options = BuildOptions.Development
                });
                if (result.summary.result != BuildResult.Succeeded) throw new InvalidOperationException("Benchmark build failed.");
                Debug.Log("CAELMOR_PERF_BUILT " + harness.configuration);
            }
            finally
            {
                ArchitectureImport.Root = previousRoot;
                CaelmorSceneOwnership.RestoreSetup(setup);
            }
        }

        static ArchitectureImportRecord LoadOrImport(string directory, string key)
        {
            string source = Path.Combine(directory,key + ".glb");
            var record = AssetDatabase.LoadAssetAtPath<ArchitectureImportRecord>(
                ArchitectureImport.Root + "/Generated/" + key + "/ImportRecord.asset");
            if (record != null && record.sourcePath == ArchitectureImport.Relative(source) &&
                record.sourceHash == ArchitectureImport.FileHash(source) &&
                record.collisionHash == ArchitectureImport.FileHash(Path.ChangeExtension(source,".collision.glb")) &&
                record.sidecarHash == ArchitectureImport.Hash(File.ReadAllBytes(Path.ChangeExtension(source,".caelmor.json"))))
            {
                ArchitectureImport.VerifyOwned(record);
                return record;
            }
            return ArchitectureImport.Import(source,key);
        }

        static Vector3 Basis(JToken value) => new Vector3(-(float)value[0],(float)value[2],-(float)value[1]);

        static Transform MakeView(string name,JToken camera)
        {
            var view = new GameObject(name).transform;
            view.position = Basis(camera["position"]);
            view.rotation = Quaternion.LookRotation(Basis(camera["forward"]),Vector3.up);
            view.localScale = new Vector3(Camera.HorizontalToVerticalFieldOfView((float)camera["horizontal_fov"],16f/9),1,1);
            return view;
        }

        static void AddGround(string source, UnityEngine.SceneManagement.Scene scene)
        {
            string path = Scratch + "/Ground.mat";
            var material = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (material == null)
            {
                material = new Material(Shader.Find("Standard")) { color = new Color(.30f,.32f,.21f) };
                AssetDatabase.CreateAsset(material,path);
            }
            string meshPath = Scratch + "/ground.glb";
            if (!File.Exists(meshPath)) File.Copy(Path.Combine(source,"ground.glb"),meshPath);
            AssetDatabase.ImportAsset(meshPath,ImportAssetOptions.ForceSynchronousImport);
            var asset = AssetDatabase.LoadAssetAtPath<GameObject>(meshPath);
            if (asset == null) throw new IOException("Showcase ground did not import.");
            var ground = (GameObject)PrefabUtility.InstantiatePrefab(asset,scene);
            ground.name = "Showcase ground geometry, neutral finish";
            foreach (var renderer in ground.GetComponentsInChildren<MeshRenderer>())
                renderer.sharedMaterials = renderer.sharedMaterials.Select(_=>material).ToArray();
        }

        static void AddFoliage(string source,LowmarkPerformance harness)
        {
            string glb = Scratch + "/plants.glb";
            string points = Scratch + "/scatter.bytes";
            if (!File.Exists(glb)) File.Copy(Path.Combine(source,"plants.glb"),glb);
            if (!File.Exists(points)) File.Copy(Path.Combine(source,"scatter.bytes"),points);
            AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
            var asset = AssetDatabase.LoadAssetAtPath<GameObject>(glb);
            if (asset == null) throw new InvalidOperationException("Approved vegetation GLB failed to import.");
            var specimens = asset.GetComponentsInChildren<MeshFilter>()
                .Where(f=>f.name.StartsWith("specimen_",StringComparison.Ordinal))
                .OrderBy(f=>int.Parse(f.name.Substring(9))).ToArray();
            if (specimens.Length == 0 || specimens.Any(f=>f.sharedMesh.subMeshCount != 1))
                throw new InvalidOperationException("Expected one mesh/material per specimen.");
            harness.plants = specimens.Select(f=>f.sharedMesh).ToArray();
            harness.farSpecimens = JArray.Parse(File.ReadAllText(Path.Combine(source,"lod.json"))).ToObject<int[]>();
            harness.foliage = specimens.Select(filter => {
                var sourceMaterial = filter.GetComponent<MeshRenderer>().sharedMaterial;
                Texture texture = sourceMaterial.GetTexturePropertyNames()
                    .Where(n=>n=="_MainTex" || n=="_BaseColorTexture" || n=="baseColorTexture")
                    .Select(sourceMaterial.GetTexture).FirstOrDefault(t=>t!=null);
                if (texture==null) throw new InvalidOperationException("Missing source vegetation atlas " + sourceMaterial.name);
                string path = Scratch + "/" + sourceMaterial.name.Replace(" ","_") + ".mat";
                var material = AssetDatabase.LoadAssetAtPath<Material>(path);
                if (material == null)
                {
                    material = new Material(Shader.Find("Caelmor/Architecture PBR"));
                    material.SetTexture("_MainTex",texture);
                    material.SetFloat("_Cutoff",.45f);
                    material.SetFloat("_Cull",0);
                    material.SetFloat("_VertexColor",0);
                    material.enableInstancing=true;
                    AssetDatabase.CreateAsset(material,path);
                }
                return material;
            }).ToArray();
            harness.scatter = AssetDatabase.LoadAssetAtPath<TextAsset>(points);
        }

        static void ConfigureTextures(LowmarkPerformance harness, bool compress)
        {
            string directory = Scratch + (compress ? "/Compressed" : "/NoMips");
            Directory.CreateDirectory(directory);
            var materialCopies = new Dictionary<Material,Material>();
            var textureCopies = new Dictionary<Texture,Texture>();
            foreach (var renderer in harness.roofVariants.SelectMany(root=>root.GetComponentsInChildren<MeshRenderer>(true)))
            {
                renderer.sharedMaterials = renderer.sharedMaterials.Select(source => {
                    if (materialCopies.TryGetValue(source,out var material)) return material;
                    var path = directory + "/material-" + materialCopies.Count + ".mat";
                    material = new Material(source);
                    foreach (string property in source.GetTexturePropertyNames())
                    {
                        var texture = source.GetTexture(property);
                        if (texture == null) continue;
                        string original = AssetDatabase.GetAssetPath(texture);
                        if (!(AssetImporter.GetAtPath(original) is TextureImporter old)) continue;
                        if (!textureCopies.TryGetValue(texture,out var compressed))
                        {
                            string copy = directory + "/" + Path.GetFileName(original);
                            if (!File.Exists(copy) && !AssetDatabase.CopyAsset(original,copy)) throw new IOException(copy);
                            var importer = (TextureImporter)AssetImporter.GetAtPath(copy);
                            importer.textureCompression = compress ? TextureImporterCompression.CompressedHQ : TextureImporterCompression.Uncompressed;
                            importer.mipmapEnabled = compress;
                            importer.streamingMipmaps = compress;
                            importer.isReadable = false;
                            var platform = importer.GetPlatformTextureSettings("Standalone");
                            platform.overridden = compress;
                            platform.maxTextureSize = old.maxTextureSize;
                            platform.format = old.textureType == TextureImporterType.NormalMap ? TextureImporterFormat.BC5 : TextureImporterFormat.BC7;
                            importer.SetPlatformTextureSettings(platform);
                            importer.SaveAndReimport();
                            compressed = AssetDatabase.LoadAssetAtPath<Texture2D>(copy);
                            textureCopies.Add(texture,compressed);
                        }
                        material.SetTexture(property,compressed);
                    }
                    if (File.Exists(path)) AssetDatabase.DeleteAsset(path);
                    AssetDatabase.CreateAsset(material,path);
                    materialCopies.Add(source,material);
                    return material;
                }).ToArray();
            }
            harness.releaseVisualMeshCpuCopy = compress;
        }
    }
}
