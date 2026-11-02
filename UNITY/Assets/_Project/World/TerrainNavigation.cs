using System;
using System.Collections.Generic;
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
        NavMeshData runtimeData;

        void OnEnable() => Bind();
        void OnDisable() { if (instance.valid) instance.Remove();if(runtimeData!=null)DestroyImmediate(runtimeData);runtimeData=null; }

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
            for(int i=0;i<corners.Length;i++)
            {
                if(!TryGroundPoint(corners[i],solidMask,out var groundPoint)){corners=null;return false;}
                corners[i]=groundPoint;
            }
            return corners.Length > 0;
        }
        public bool TryGroundPoint(Vector3 point,int solidMask,out Vector3 groundPoint)
        {
            groundPoint=point;
            if(!Finite(point) || !Physics.Raycast(point+Vector3.up*.3f,Vector3.down,out var hit,.6f,solidMask,QueryTriggerInteraction.Ignore) ||
                hit.collider.GetComponent<NavigableTerrain>()==null || hit.normal.y<.7f || Mathf.Abs(hit.point.y-point.y)>.2f)return false;
            groundPoint=hit.point;return true;
        }
        // Rare persistent gate transitions rebuild synchronously at finalization. There
        // is no frame-delayed carving state that could disagree with authoritative tests.
        public void RefreshWorldGeometry(int solidMask)
        {
            Physics.SyncTransforms();
            var settings=NavMesh.GetSettingsByIndex(0);settings.agentRadius=.43f;settings.agentHeight=1.8f;settings.agentClimb=.2f;settings.agentSlope=40;
            settings.overrideVoxelSize=true;settings.voxelSize=.08f;settings.minRegionArea=.1f;
            var bounds=new Bounds(new Vector3(46,0,0),new Vector3(124,24,42));
            var sources=new List<NavMeshBuildSource>();
            NavMeshBuilder.CollectSources(bounds,solidMask,NavMeshCollectGeometry.PhysicsColliders,0,new List<NavMeshBuildMarkup>(),sources);
            var rebuilt=NavMeshBuilder.BuildNavMeshData(settings,sources,bounds,Vector3.zero,Quaternion.identity);
            if(rebuilt==null)throw new InvalidOperationException("World navigation rebuild failed.");
            if(instance.valid)instance.Remove();if(runtimeData!=null)DestroyImmediate(runtimeData);
            runtimeData=rebuilt;instance=NavMesh.AddNavMeshData(runtimeData);
        }

        static bool Finite(Vector3 point) => Finite(point.x) && Finite(point.y) && Finite(point.z);
        static bool Finite(float value) => !float.IsNaN(value) && !float.IsInfinity(value);
    }
}
