using UnityEngine;

namespace Caelmor.Unity.Playable
{
    /// <summary>Scene-authored technical target. Not an NPC, quest, or production content definition.</summary>
    public sealed class InteractionAnchor : MonoBehaviour
    {
        public int fixtureId = 9001;
        public int zoneId = 1;
        public string displayName = "Interaction fixture";
        public float interactionRange = 2.4f;
        public Renderer markerRenderer;
    }
}
