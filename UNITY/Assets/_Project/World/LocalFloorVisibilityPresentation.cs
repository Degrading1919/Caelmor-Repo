using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

namespace Caelmor.Unity.Playable
{
    /// <summary>
    /// Optional client presentation adapter for one local camera. It consumes explicit occupancy
    /// and floor section data, never changes simulation state, and restores renderer states after
    /// each render and when disabled.
    /// </summary>
    [DisallowMultipleComponent]
    public sealed class LocalFloorVisibilityPresentation : MonoBehaviour
    {
        const float CutoffEpsilon = .00001f;

        public Camera targetCamera;
        public Transform occupancyProbe;
        public FloorVisibilityBuilding[] volumes = Array.Empty<FloorVisibilityBuilding>();
        [Min(0f)] public float transitionDwellSeconds = .15f;
        [Min(0f)] public float floorBoundaryHysteresis = .12f;

        readonly Dictionary<Renderer, bool> originalEnabled = new Dictionary<Renderer, bool>();
        readonly Dictionary<Renderer, bool> renderBaselineEnabled = new Dictionary<Renderer, bool>();
        readonly Dictionary<Renderer, bool> renderedEnabled = new Dictionary<Renderer, bool>();
        readonly Stack<NestedCameraState> nestedCameraStates = new Stack<NestedCameraState>();
        FloorVisibilityBuilding activeVolume;
        int currentFloor = -1;
        int candidateFloor = -1;
        float candidateSince;
        bool candidateActive;
        bool rendering;
        bool usesScriptablePipeline;

        internal int CurrentFloorForValidation => currentFloor;
        internal bool HasRendererBaselineForValidation(Renderer renderer) => renderBaselineEnabled.ContainsKey(renderer);

        sealed class NestedCameraState
        {
            public Camera camera;
            public readonly Dictionary<Renderer, bool> priorEnabled = new Dictionary<Renderer, bool>();
        }

        void OnEnable()
        {
            if (targetCamera == null) targetCamera = GetComponent<Camera>();
            CaptureOriginalRendererStates();
            usesScriptablePipeline = GraphicsSettings.currentRenderPipeline != null;
            if (usesScriptablePipeline)
            {
                RenderPipelineManager.beginCameraRendering += BeginScriptableCamera;
                RenderPipelineManager.endCameraRendering += EndScriptableCamera;
            }
            else
            {
                Camera.onPreCull += BeginBuiltInCamera;
                Camera.onPostRender += EndBuiltInCamera;
            }
        }

        void OnDisable()
        {
            if (usesScriptablePipeline)
            {
                RenderPipelineManager.beginCameraRendering -= BeginScriptableCamera;
                RenderPipelineManager.endCameraRendering -= EndScriptableCamera;
            }
            else
            {
                Camera.onPreCull -= BeginBuiltInCamera;
                Camera.onPostRender -= EndBuiltInCamera;
            }
            if (rendering) SetOriginalRendererEnabled();
            nestedCameraStates.Clear();
            renderedEnabled.Clear();
            renderBaselineEnabled.Clear();
            rendering = false;
            ResetSelection();
        }

        void CaptureOriginalRendererStates()
        {
            originalEnabled.Clear();
            if (volumes == null) return;
            for (int v = 0; v < volumes.Length; v++)
            {
                var volume = volumes[v];
                if (volume == null || volume.sections == null) continue;
                for (int s = 0; s < volume.sections.Length; s++)
                {
                    var section = volume.sections[s];
                    if (section == null || section.renderers == null) continue;
                    for (int r = 0; r < section.renderers.Length; r++)
                    {
                        var renderer = section.renderers[r];
                        if (renderer != null && !originalEnabled.ContainsKey(renderer))
                            originalEnabled.Add(renderer, renderer.enabled);
                    }
                }
            }
        }

        internal void BeginBuiltInCamera(Camera camera)
        {
            if (camera == targetCamera) BeginPresentation();
            else if (rendering) SuspendForNestedCamera(camera);
        }

        internal void EndBuiltInCamera(Camera camera)
        {
            if (camera == targetCamera) EndPresentation();
            else ResumeAfterNestedCamera(camera);
        }

        internal void BeginScriptableCamera(ScriptableRenderContext context, Camera camera)
        {
            if (camera == targetCamera) BeginPresentation();
            else if (rendering) SuspendForNestedCamera(camera);
        }

        internal void EndScriptableCamera(ScriptableRenderContext context, Camera camera)
        {
            if (camera == targetCamera) EndPresentation();
            else ResumeAfterNestedCamera(camera);
        }

        void SuspendForNestedCamera(Camera camera)
        {
            var state = new NestedCameraState { camera = camera };
            foreach (var pair in originalEnabled)
                if (pair.Key != null) state.priorEnabled.Add(pair.Key, pair.Key.enabled);
            nestedCameraStates.Push(state);
            SetOriginalRendererEnabled();
        }

        void ResumeAfterNestedCamera(Camera camera)
        {
            if (nestedCameraStates.Count == 0 || nestedCameraStates.Peek().camera != camera) return;
            var state = nestedCameraStates.Pop();
            foreach (var pair in state.priorEnabled)
                if (pair.Key != null) pair.Key.enabled = pair.Value;
        }

        void BeginPresentation()
        {
            if (!isActiveAndEnabled || rendering) return;
            try
            {
                CaptureCurrentRendererStates();
                UpdateFloorSelection();
                ApplyPresentation();
                rendering = true;
            }
            catch
            {
                RestoreOriginalRendererStates();
                ResetSelection();
                throw;
            }
        }

        void EndPresentation()
        {
            if (!rendering) return;
            RestoreOriginalRendererStates();
        }

        void UpdateFloorSelection()
        {
            FloorVisibilityBuilding found = null;
            if (occupancyProbe != null && volumes != null)
            {
                for (int i = 0; i < volumes.Length; i++)
                {
                    var candidate = volumes[i];
                    if (candidate != null && candidate.isActiveAndEnabled && candidate.ContainsOccupant(occupancyProbe.position))
                    { found = candidate; break; }
                }
            }

            if (found != activeVolume)
            {
                activeVolume = found;
                currentFloor = -1;
                ClearCandidate();
            }
            if (activeVolume == null) return;

            float localHeight = activeVolume.LocalHeight(occupancyProbe.position);
            if (currentFloor >= 0 && TryGetCurrentBand(out float low, out float high) &&
                localHeight >= low - floorBoundaryHysteresis && localHeight <= high + floorBoundaryHysteresis)
            {
                ClearCandidate();
                return;
            }
            if (!activeVolume.TryGetFloor(localHeight, out int desiredFloor, out _, out _) || desiredFloor == currentFloor)
            { ClearCandidate(); return; }

            if (!candidateActive || candidateFloor != desiredFloor)
            {
                candidateFloor = desiredFloor;
                candidateSince = Time.unscaledTime;
                candidateActive = true;
                return;
            }
            if (Time.unscaledTime - candidateSince >= transitionDwellSeconds)
            {
                currentFloor = candidateFloor;
                ClearCandidate();
            }
        }

        bool TryGetCurrentBand(out float minimum, out float maximum)
        {
            if (activeVolume != null && activeVolume.floorBands != null)
            {
                for (int i = 0; i < activeVolume.floorBands.Length; i++)
                {
                    var band = activeVolume.floorBands[i];
                    if (band != null && band.floorIndex == currentFloor && band.maximumLocalHeight > band.minimumLocalHeight)
                    { minimum = band.minimumLocalHeight; maximum = band.maximumLocalHeight; return true; }
                }
            }
            minimum = maximum = 0f;
            return false;
        }

        void ApplyPresentation()
        {
            renderedEnabled.Clear();
            foreach (var pair in renderBaselineEnabled) renderedEnabled[pair.Key] = pair.Value;
            if (activeVolume != null && currentFloor >= 0 && TryGetCurrentBand(out _, out float cutoff) && volumes != null)
            {
                for (int v = 0; v < volumes.Length; v++)
                {
                    var volume = volumes[v];
                    if (volume == null || !SharesBuilding(volume, activeVolume) || volume.sections == null) continue;
                    for (int i = 0; i < volume.sections.Length; i++)
                    {
                        var section = volume.sections[i];
                        if (section == null || section.renderers == null) continue;
                        bool visible = IsVisible(section.visibility, section.minimumLocalHeight, section.maximumLocalHeight, cutoff);
                        for (int r = 0; r < section.renderers.Length; r++)
                        {
                            var renderer = section.renderers[r];
                            if (renderer != null && renderBaselineEnabled.TryGetValue(renderer, out bool wasEnabled))
                                renderedEnabled[renderer] = wasEnabled && visible;
                        }
                    }
                }
            }
            foreach (var pair in renderedEnabled)
                if (pair.Key != null) pair.Key.enabled = pair.Value;
        }

        internal static bool IsVisible(FloorVisibilityBuilding.SectionVisibility visibility, float lower, float upper, float cutoff)
        {
            switch (visibility)
            {
                case FloorVisibilityBuilding.SectionVisibility.Floor: return lower < cutoff - CutoffEpsilon;
                case FloorVisibilityBuilding.SectionVisibility.Covering: return upper <= cutoff - CutoffEpsilon;
                default: return true;
            }
        }

        static bool SharesBuilding(FloorVisibilityBuilding a, FloorVisibilityBuilding b)
        {
            if (ReferenceEquals(a, b)) return true;
            if (string.IsNullOrEmpty(a.buildingId) || string.IsNullOrEmpty(b.buildingId)) return false;
            return string.Equals(a.buildingId, b.buildingId, StringComparison.Ordinal);
        }

        void RestoreOriginalRendererStates()
        {
            SetOriginalRendererEnabled();
            nestedCameraStates.Clear();
            renderedEnabled.Clear();
            renderBaselineEnabled.Clear();
            rendering = false;
        }

        void CaptureCurrentRendererStates()
        {
            CaptureOriginalRendererStates();
            renderBaselineEnabled.Clear();
            foreach (var pair in originalEnabled)
                if (pair.Key != null) renderBaselineEnabled.Add(pair.Key, pair.Key.enabled);
        }

        void SetOriginalRendererEnabled()
        {
            foreach (var pair in renderBaselineEnabled)
                if (pair.Key != null) pair.Key.enabled = pair.Value;
        }

        void ClearCandidate() { candidateFloor = -1; candidateActive = false; }

        void ResetSelection()
        {
            activeVolume = null;
            currentFloor = -1;
            ClearCandidate();
        }
    }
}
