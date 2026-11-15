using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using Unity.Profiling;
using Unity.Profiling.LowLevel.Unsafe;
using UnityEngine;
using UnityEngine.Profiling;
using UnityEngine.Rendering;

namespace Caelmor.Unity
{
    // Entry point only in the generated benchmark scene.
    public sealed class LowmarkPerformance : MonoBehaviour
    {
        public Camera inspection;
        public Transform[] views;
        public GameObject[] roofVariants;
        public string configuration;
        public int commonMaterials;
        public bool releaseVisualMeshCpuCopy;
        public TextAsset scatter;
        public Mesh[] plants;
        public int[] farSpecimens;
        public Material[] foliage;
        struct Cluster
        {
            public int specimen;
            public Matrix4x4[] matrices;
            public Matrix4x4[] half;
            public Bounds bounds;
        }

        readonly List<Cluster> clusters = new List<Cluster>();
        string foliageMode = "off";
        Material[] opaque;
        Material[] uninstanced;
        Matrix4x4[][] mergedMatrices;
        int[] mergedCounts;
        readonly FrameTiming[] timings = new FrameTiming[1];
        static string N(double value) => value.ToString("0.####", CultureInfo.InvariantCulture);

        void LoadScatter()
        {
            if (scatter == null) return;
            using var reader = new BinaryReader(new MemoryStream(scatter.bytes));
            int count = reader.ReadInt32();
            for (int group = 0; group < count; group++)
            {
                int specimen = reader.ReadInt32();
                int length = reader.ReadInt32();
                var matrices = new Matrix4x4[length];
                var bounds = new Bounds();
                for (int i = 0; i < length; i++)
                {
                    var matrix = Matrix4x4.zero;
                    for (int row = 0; row < 4; row++)
                        for (int column = 0; column < 4; column++)
                            matrix[row,column] = reader.ReadSingle();
                    matrices[i] = matrix;
                    var point = (Vector3)matrix.GetColumn(3);
                    if (i == 0) bounds = new Bounds(point, Vector3.one * 4);
                    else bounds.Encapsulate(new Bounds(point, Vector3.one * 4));
                }
                clusters.Add(new Cluster { specimen = specimen, matrices = matrices,
                    half = matrices.Where((_, i) => i % 2 == 0).ToArray(), bounds = bounds });
            }
            opaque = CopyFoliageMaterials(material => material.SetFloat("_Cutoff", 0));
            uninstanced = CopyFoliageMaterials(material => material.enableInstancing = false);
            mergedMatrices = plants.Select(_=>new Matrix4x4[1023]).ToArray();
            mergedCounts = new int[plants.Length];
        }

        Material[] CopyFoliageMaterials(Action<Material> configure)
        {
            var copies = new Dictionary<Material,Material>();
            return foliage.Select(source =>
            {
                if (copies.TryGetValue(source,out var existing)) return existing;
                var material = new Material(source);
                configure(material);
                copies.Add(source,material);
                return material;
            }).ToArray();
        }

        void Submit(int specimen, Material material, Matrix4x4[] matrices, int count) =>
            Graphics.DrawMeshInstanced(plants[specimen],0,material,matrices,count,null,
                ShadowCastingMode.Off,false,0,inspection);

        void MergeVisible(int specimen, Matrix4x4[] matrices)
        {
            var buffer = mergedMatrices[specimen];
            int count = mergedCounts[specimen];
            int offset = 0;
            while (offset < matrices.Length)
            {
                int copy = Math.Min(buffer.Length-count,matrices.Length-offset);
                Array.Copy(matrices,offset,buffer,count,copy);
                offset += copy;
                count += copy;
                if (count == buffer.Length)
                {
                    Submit(specimen,foliage[specimen],buffer,count);
                    count = 0;
                }
            }
            mergedCounts[specimen] = count;
        }

        void LateUpdate()
        {
            FrameTimingManager.CaptureFrameTimings();
            if (foliageMode != "off")
            {
                var planes = GeometryUtility.CalculateFrustumPlanes(inspection);
                bool merge = foliageMode == "merged";
                if (merge) Array.Clear(mergedCounts,0,mergedCounts.Length);
                foreach (var cluster in clusters)
                {
                    if (!GeometryUtility.TestPlanesAABB(planes, cluster.bounds)) continue;
                    int specimen = foliageMode == "lod" && (cluster.bounds.center-inspection.transform.position).sqrMagnitude > 18*18 ? farSpecimens[cluster.specimen] : cluster.specimen;
                    var mesh = plants[specimen];
                    var material = (foliageMode == "opaque" ? opaque : foliage)[specimen];
                    if (foliageMode == "individual")
                    {
                        foreach (var matrix in cluster.half)
                            Graphics.DrawMesh(mesh,matrix,uninstanced[specimen],0,inspection,0,null,ShadowCastingMode.Off,false);
                    }
                    else
                    {
                        var matrices = foliageMode == "half" ? cluster.half : cluster.matrices;
                        if (merge) MergeVisible(specimen,matrices);
                        else Submit(specimen,material,matrices,matrices.Length);
                    }
                }
                if (merge)
                    for (int i = 0; i < mergedCounts.Length; i++)
                        if (mergedCounts[i] > 0) Submit(i,foliage[i],mergedMatrices[i],mergedCounts[i]);
            }
            // Explicit submission also renders when the player window is hidden.
            if (inspection.targetTexture != null) inspection.Render();
        }

        IEnumerator Start()
        {
            if (GraphicsSettings.currentRenderPipeline != null || SystemInfo.graphicsDeviceType == GraphicsDeviceType.Null)
                throw new InvalidOperationException("Benchmark requires real Built-in rendering.");
            string output = Environment.GetEnvironmentVariable("CAELMOR_PERF_OUTPUT");
            if (string.IsNullOrEmpty(output)) { Application.Quit(2); yield break; }
            Directory.CreateDirectory(output);
            QualitySettings.vSyncCount = 0;
            Application.targetFrameRate = -1;
            Application.runInBackground = true;
            // A fixed render target makes the workload independent of desktop size.
            inspection.targetTexture = new RenderTexture(1920,1080,24);
            inspection.enabled = false;
            LoadScatter();
            bool forceResident = Environment.GetEnvironmentVariable("CAELMOR_PERF_FORCE_RESIDENT") == "1";
            QualitySettings.streamingMipmapsActive = releaseVisualMeshCpuCopy && !forceResident;
            if (forceResident) configuration = "compressed_resident_nonreadable";
            if (releaseVisualMeshCpuCopy)
                foreach (var mesh in roofVariants.SelectMany(r => r.GetComponentsInChildren<MeshFilter>(true)).Select(f=>f.sharedMesh).Distinct())
                    if (mesh != null && mesh.isReadable) mesh.UploadMeshData(true);
            File.WriteAllText(Path.Combine(output,"device.txt"),
                $"{SystemInfo.graphicsDeviceName}\n{SystemInfo.graphicsDeviceType}\n{SystemInfo.processorType}\n{SystemInfo.graphicsMemorySize} MiB reported VRAM\n1920x1080 render target\n");
            var handles = new List<ProfilerRecorderHandle>();
            ProfilerRecorderHandle.GetAvailable(handles);
            var renderCounters = handles.Select(ProfilerRecorderHandle.GetDescription)
                .Where(d => d.Category == ProfilerCategory.Render).Select(d=>d.Name).OrderBy(n=>n).ToArray();
            File.WriteAllLines(Path.Combine(output,"render-counters.txt"),renderCounters);
            string batchCounter = renderCounters.Contains("Total Batches Count") ? "Total Batches Count" : "Batches Count";
            using var batches = ProfilerRecorder.StartNew(ProfilerCategory.Render,batchCounter);
            using var draws = ProfilerRecorder.StartNew(ProfilerCategory.Render,"Draw Calls Count");
            using var standard = ProfilerRecorder.StartNew(ProfilerCategory.Render,"Standard Draw Calls Count");
            using var instanced = ProfilerRecorder.StartNew(ProfilerCategory.Render,"Standard Instanced Draw Calls Count");
            using var setPass = ProfilerRecorder.StartNew(ProfilerCategory.Render,"SetPass Calls Count");
            using var triangles = ProfilerRecorder.StartNew(ProfilerCategory.Render,"Triangles Count");
            using var writer = new StreamWriter(Path.Combine(output,"frames.csv"));
            writer.WriteLine("configuration,view,roof_case,foliage,frame_ms,cpu_ms,gpu_ms,batches,draw_calls,standard_draw_calls,instanced_draw_calls,setpass,triangles,allocated_bytes,scene_texture_bytes,scene_mesh_bytes,streaming_current_bytes,material_count,common_material_count");
            for (int variant = 0; variant < roofVariants.Length; variant++)
            {
                if (variant > 0 && configuration != "baseline") break;
                for (int other = 0; other < roofVariants.Length; other++) roofVariants[other].SetActive(other == variant);
                for (int view = 0; view < views.Length; view++)
                {
                    inspection.transform.SetPositionAndRotation(views[view].position,views[view].rotation);
                    inspection.fieldOfView = views[view].localScale.x;
                    var modes = new[] {"off"};
                    if (variant == 0 && clusters.Count > 0)
                        modes = configuration == "baseline"
                            ? new[] {"off","full","merged","half","lod","opaque","individual"}
                            : new[] {"off","merged"};
                    foreach (string mode in modes)
                    {
                        foliageMode = mode;
                        for (int i = 0; i < 64; i++) yield return null;
                        if (!triangles.Valid || triangles.LastValue == 0)
                        {
                            Debug.LogError("Benchmark fixture did not submit render geometry.");
                            Application.Quit(3);
                            yield break;
                        }
                        var root = roofVariants[variant];
                        var materials = root.GetComponentsInChildren<Renderer>().SelectMany(r => r.sharedMaterials)
                            .Concat(mode == "off" ? Array.Empty<Material>() : foliage).Distinct().ToArray();
                        var textures = materials.SelectMany(m => m.GetTexturePropertyNames().Select(m.GetTexture))
                            .Where(t => t != null).Distinct();
                        var meshes = root.GetComponentsInChildren<MeshFilter>().Select(f => f.sharedMesh)
                            .Concat(mode == "off" ? Array.Empty<Mesh>() : plants).Where(m => m != null).Distinct();
                        long textureBytes = textures.Sum(t => Profiler.GetRuntimeMemorySizeLong(t));
                        long meshBytes = meshes.Sum(m => Profiler.GetRuntimeMemorySizeLong(m));
                        for (int i = 0; i < 96; i++)
                        {
                            yield return null;
                            bool has = FrameTimingManager.GetLatestTimings(1,timings) > 0;
                            writer.WriteLine(string.Join(",",configuration,views[view].name,root.name,mode,
                                N(Time.unscaledDeltaTime*1000),has ? N(timings[0].cpuFrameTime) : "",
                                has && timings[0].gpuFrameTime > 0 ? N(timings[0].gpuFrameTime) : "",
                                batches.Valid ? batches.LastValue.ToString() : "", draws.Valid ? draws.LastValue.ToString() : "",
                                standard.Valid ? standard.LastValue.ToString() : "",
                                instanced.Valid ? instanced.LastValue.ToString() : "", setPass.Valid ? setPass.LastValue.ToString() : "",
                                triangles.Valid ? triangles.LastValue.ToString() : "",Profiler.GetTotalAllocatedMemoryLong(),
                                textureBytes,meshBytes,Texture.currentTextureMemory,materials.Length,commonMaterials));
                        }
                        if (mode != "individual")
                        {
                            var prior = RenderTexture.active;
                            RenderTexture.active = inspection.targetTexture;
                            var image = new Texture2D(1920,1080,TextureFormat.RGB24,false);
                            image.ReadPixels(new Rect(0,0,1920,1080),0,0);
                            image.Apply();
                            File.WriteAllBytes(Path.Combine(output,$"{views[view].name}-{root.name}-{mode}.jpg"),image.EncodeToJPG(91));
                            Destroy(image);
                            RenderTexture.active = prior;
                        }
                    }
                }
            }
            writer.Flush();
            File.AppendAllText(Path.Combine(output,"device.txt"),$"Streaming enabled: {QualitySettings.streamingMipmapsActive}; streaming textures: {Texture.streamingTextureCount}; instancing supported: {SystemInfo.supportsInstancing}\n");
            Debug.Log("CAELMOR_PERFORMANCE_COMPLETE");
            Application.Quit();
        }
    }
}
