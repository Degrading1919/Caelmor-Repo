using System;
using UnityEngine;

namespace Caelmor.Unity.Playable
{
    /// <summary>
    /// Authored presentation data for one enterable volume within a building. The occupancy box
    /// is explicit scene data; it is never inferred from exterior geometry or floor metadata.
    /// </summary>
    public sealed class FloorVisibilityBuilding : MonoBehaviour
    {
        public enum HeightAxis { LocalX, LocalY, LocalZ }
        public enum SectionVisibility { Floor, Covering, Always }

        [Serializable]
        public sealed class FloorBand
        {
            public int floorIndex;
            public float minimumLocalHeight;
            public float maximumLocalHeight;
        }

        [Serializable]
        public sealed class Section
        {
            public SectionVisibility visibility;
            public int floorIndex;
            public float minimumLocalHeight;
            public float maximumLocalHeight;
            public Renderer[] renderers = Array.Empty<Renderer>();
        }

        [Tooltip("Persistent generator id shared by this building's independent volumes.")]
        public string buildingId;
        [Tooltip("Stable schedule key for this independently elevated floor volume.")]
        public string volumeId;
        [Tooltip("Explicit enterable volume. Only its box bounds are read; collider state is preserved.")]
        public BoxCollider occupancyVolume;
        [Tooltip("Axis mapping for generator local-Z metres after import. Unity glTF Y-up imports normally map source Z to local Y.")]
        public HeightAxis heightAxis = HeightAxis.LocalY;
        [Tooltip("Authored occupiable bands for this volume. Do not include attic/roof bands.")]
        public FloorBand[] floorBands = Array.Empty<FloorBand>();
        [Tooltip("Renderer groups from this volume's floor-section manifest entries.")]
        public Section[] sections = Array.Empty<Section>();

        public bool ContainsOccupant(Vector3 worldPosition)
        {
            if (occupancyVolume == null) return false;
            var local = occupancyVolume.transform.InverseTransformPoint(worldPosition) - occupancyVolume.center;
            var half = occupancyVolume.size * .5f;
            return Mathf.Abs(local.x) <= half.x && Mathf.Abs(local.y) <= half.y && Mathf.Abs(local.z) <= half.z;
        }

        public float LocalHeight(Vector3 worldPosition)
        {
            var local = transform.InverseTransformPoint(worldPosition);
            switch (heightAxis)
            {
                case HeightAxis.LocalX: return local.x;
                case HeightAxis.LocalZ: return local.z;
                default: return local.y;
            }
        }

        public bool TryGetFloor(float localHeight, out int index, out float minimum, out float maximum)
        {
            if (floorBands != null)
            {
                for (int i = 0; i < floorBands.Length; i++)
                {
                    var band = floorBands[i];
                    if (band == null || band.maximumLocalHeight <= band.minimumLocalHeight) continue;
                    if (localHeight < band.minimumLocalHeight || localHeight > band.maximumLocalHeight) continue;
                    index = band.floorIndex;
                    minimum = band.minimumLocalHeight;
                    maximum = band.maximumLocalHeight;
                    return true;
                }
            }
            index = -1; minimum = maximum = 0f;
            return false;
        }
    }
}
