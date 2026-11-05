using System;
using System.Linq;
using UnityEngine;

namespace Caelmor.Unity
{
    /// <summary>Only attached to the disposable architecture verification build.</summary>
    public sealed class ArchitecturePlayerValidation : MonoBehaviour
    {
        public GameObject floorA;
        public GameObject floorB;
        public GameObject gatehouse;
        void Start()
        {
            try
            {
                Require(floorA != null && floorB != null && gatehouse != null, "Native prefab instances persisted into player.");
                var a = floorA.GetComponentsInChildren<MeshRenderer>(true);
                var b = floorB.GetComponentsInChildren<MeshRenderer>(true);
                Require(a.Length == 79 && b.Length == 79 && gatehouse.GetComponentsInChildren<MeshRenderer>(true).Length == 149, "Actual exported section counts.");
                for (int i = 0; i < a.Length; i++)
                {
                    Require(a[i].sharedMaterial == b[i].sharedMaterial, "Instances share material resources.");
                    Require(a[i].GetComponent<MeshFilter>().sharedMesh == b[i].GetComponent<MeshFilter>().sharedMesh, "Instances share mesh resources.");
                    Require(a[i].sharedMaterial.shader != null, "PBR shader retained in player build.");
                }
                // Built-in shader fallback textures such as "bump" become non-null in
                // players even when no authored normal map is enabled on that material.
                var atlas = a.FirstOrDefault(r => r.sharedMaterial.shader.name == "Caelmor/Architecture PBR" && r.sharedMaterial.GetFloat("_HasNormal") > 0.5f);
                Require(atlas != null, "An actual enabled atlas/detail normal material persists.");
                var atlasMaterial = atlas.sharedMaterial;
                Require(atlasMaterial.GetFloat("_BaseUv") == 2 && atlasMaterial.GetFloat("_NormalUv") == 3,
                    $"Atlas/detail UV channel properties persist: material={atlasMaterial.name} base={atlasMaterial.GetFloat("_BaseUv")} normal={atlasMaterial.GetFloat("_NormalUv")} enabled={atlasMaterial.GetFloat("_HasNormal")}");
                Require(atlas.GetComponent<MeshFilter>().sharedMesh.uv3.Length == atlas.GetComponent<MeshFilter>().sharedMesh.vertexCount, "Third UV channel persisted.");
                Require(floorA.GetComponentsInChildren<ArchitectureIdentity>(true).Any(i => i.visibility == "FLOOR" && i.floorIndex == 1), "Storey identities persist.");
                Require(a.Count(r => r.sharedMaterial.shader.name == "Standard") == 2, "Two explicit original grayscale painting baselines persist.");
                Physics.SyncTransforms();
                foreach (GameObject building in new[] { floorA, floorB, gatehouse })
                {
                    var colliders = building.GetComponentsInChildren<MeshCollider>(true);
                    Require(colliders.Length == 15 && colliders.All(c => c.GetComponent<Renderer>() == null), "Separate invisible collision persists.");
                    var floor = colliders.First(c => c.name.IndexOf("floor", StringComparison.OrdinalIgnoreCase) >= 0);
                    Bounds bounds = floor.bounds;
                    Require(floor.Raycast(new Ray(new Vector3(bounds.center.x, bounds.max.y + 2, bounds.center.z), Vector3.down), out _, bounds.size.y + 4), "Native physics ray hits exported floor collision.");
                }
                Debug.Log("CAELMOR_ARCHITECTURE_PLAYER_PASSED renderers=307 colliders=45 shared_instances=2");
                Application.Quit(0);
            }
            catch (Exception exception)
            {
                Debug.LogError("CAELMOR_ARCHITECTURE_PLAYER_FAILED " + exception);
                Application.Quit(1);
            }
        }
        static void Require(bool condition, string message) { if (!condition) throw new InvalidOperationException(message); }
    }
}
