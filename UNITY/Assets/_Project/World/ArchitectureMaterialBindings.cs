using System;
using UnityEngine;

namespace Caelmor.Unity
{
    [CreateAssetMenu(menuName = "Caelmor/Architecture material bindings")]
    public sealed class ArchitectureMaterialBindings : ScriptableObject
    {
        [Tooltip("Exact stable caelm_buffer_id / sidecar object.name; no inferred surface replacement.")]
        public Binding[] bindings = Array.Empty<Binding>();
        [Serializable] public sealed class Binding
        {
            public string bufferId;
            public string materialId;
            [Tooltip("Explicit assertion that original GLB UV0 is metric, with authored grain/course orientation.")]
            public bool metricUv0Verified;
        }
    }
}
