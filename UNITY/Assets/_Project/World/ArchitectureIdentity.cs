using UnityEngine;

namespace Caelmor.Unity
{
    /// <summary>Offline construction metadata only; never infers occupancy or controls visibility.</summary>
    public sealed class ArchitectureIdentity : MonoBehaviour
    {
        public string buildingId;
        public string bufferId;
        public string volumeId;
        public string semanticRole;
        public string constructionRole;
        public string sourceBufferId;
        public string visibility;
        public int floorIndex = -1;
        public float floorMin;
        public float floorMax;
        [TextArea] public string sourceMetadata;
    }
}
