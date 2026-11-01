using System;
using UnityEngine;
using UnityEngine.AI;

namespace Caelmor.Unity.Playable
{
    /// <summary>Host-side path queries over a scene-baked mesh. This component never moves actors.</summary>
    [ExecuteAlways]
    public sealed class TerrainNavigation : MonoBehaviour
    {
        public NavMeshData data;
        NavMeshDataInstance instance;
        NavMeshPath query;

        void OnEnable() => Bind();
        void OnDisable() { if (instance.valid) instance.Remove(); }

        public void Bind()
        {
            if (query == null) query = new NavMeshPath();
            if (instance.valid) return;
            if (data != null) instance = NavMesh.AddNavMeshData(data);
        }

        public bool TryPath(Vector3 start, Vector3 destination, int solidMask, out Vector3[] corners)
        {
            corners = null;
            if (!Finite(start) || !Finite(destination) || !instance.valid) return false;
            // Ground designation and height are checked on the host as well as in the input adapter.
            if (!Physics.Raycast(destination + Vector3.up * .25f, Vector3.down, out var ground,
                .5f, solidMask, QueryTriggerInteraction.Ignore) ||
                ground.collider.GetComponent<NavigableTerrain>() == null ||
                Mathf.Abs(ground.point.y - destination.y) > .08f) return false;
            if (!NavMesh.SamplePosition(destination, out var end, .12f, NavMesh.AllAreas) ||
                Vector3.Distance(end.position, destination) > .12f ||
                !NavMesh.SamplePosition(start, out var begin, .25f, NavMesh.AllAreas)) return false;
            if (!NavMesh.CalculatePath(begin.position, end.position, NavMesh.AllAreas, query) ||
                query.status != NavMeshPathStatus.PathComplete) return false;
            corners = query.corners;
            return corners.Length > 0;
        }

        static bool Finite(Vector3 point) => Finite(point.x) && Finite(point.y) && Finite(point.z);
        static bool Finite(float value) => !float.IsNaN(value) && !float.IsInfinity(value);
    }
}
