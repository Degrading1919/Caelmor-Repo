using System;
using UnityEngine;
using UnityEngine.Rendering;

namespace Caelmor.Unity.Playable
{
    /// <summary>Isolated Unity object checks for authored floor presentation and camera restoration.</summary>
    public static class FloorVisibilityPresentationValidation
    {
        public static void Run()
        {
            var root = new GameObject("Floor visibility validation");
            root.SetActive(false);
            var probeObject = new GameObject("Explicit occupancy probe");
            try
            {
                var camera = root.AddComponent<Camera>();
                var low = root.AddComponent<FloorVisibilityBuilding>();
                low.buildingId = "validation-building";
                low.volumeId = "lower-wing";
                low.heightAxis = FloorVisibilityBuilding.HeightAxis.LocalY;
                low.occupancyVolume = AddOccupancyBox(root.transform, "Lower occupancy", new Vector3(0, 2, 0));
                low.floorBands = new[] { Band(0, 0, 2), Band(1, 2, 4) };

                var lowFloor = AddRenderer(root.transform, "Lower floor", true);
                var upperFloor = AddRenderer(root.transform, "Upper floor", true);
                var lowCover = AddRenderer(root.transform, "Cover below cutoff", true);
                var highCover = AddRenderer(root.transform, "Cover above cutoff", true);
                var always = AddRenderer(root.transform, "Continuous chimney", true);
                var originallyDisabled = AddRenderer(root.transform, "Originally disabled detail", false);
                low.sections = new[]
                {
                    Section(FloorVisibilityBuilding.SectionVisibility.Floor, 0, 0, 2, lowFloor),
                    Section(FloorVisibilityBuilding.SectionVisibility.Floor, 1, 2, 4, upperFloor),
                    Section(FloorVisibilityBuilding.SectionVisibility.Covering, -1, 0, 1, lowCover),
                    Section(FloorVisibilityBuilding.SectionVisibility.Covering, -1, 4, 5, highCover),
                    Section(FloorVisibilityBuilding.SectionVisibility.Always, -1, 0, 8, always, originallyDisabled)
                };

                var high = root.AddComponent<FloorVisibilityBuilding>();
                high.buildingId = low.buildingId;
                high.volumeId = "raised-wing";
                high.heightAxis = FloorVisibilityBuilding.HeightAxis.LocalY;
                high.occupancyVolume = AddOccupancyBox(root.transform, "Raised occupancy", new Vector3(10, 5, 0));
                high.occupancyVolume.size = new Vector3(4, 8, 4);
                high.floorBands = new[] { Band(0, 5, 7), Band(1, 7, 9) };
                var raisedFloor = AddRenderer(root.transform, "Raised floor", true);
                var raisedCover = AddRenderer(root.transform, "Raised roof", true);
                high.sections = new[]
                {
                    Section(FloorVisibilityBuilding.SectionVisibility.Floor, 0, 5, 7, raisedFloor),
                    Section(FloorVisibilityBuilding.SectionVisibility.Covering, -1, 7, 8, raisedCover)
                };

                var controller = root.AddComponent<LocalFloorVisibilityPresentation>();
                controller.targetCamera = camera;
                controller.occupancyProbe = probeObject.transform;
                controller.volumes = new[] { low, high };
                controller.transitionDwellSeconds = 0f;
                controller.floorBoundaryHysteresis = .12f;
                bool lowColliderEnabled = low.occupancyVolume.enabled;
                bool lowColliderTrigger = low.occupancyVolume.isTrigger;
                bool highColliderEnabled = high.occupancyVolume.enabled;
                bool highColliderTrigger = high.occupancyVolume.isTrigger;

                root.SetActive(true);
                probeObject.transform.position = new Vector3(0, 1, 0);
                Check(low.ContainsOccupant(probeObject.transform.position), "explicit lower occupancy box contains its probe");
                Check(low.TryGetFloor(1f, out int expectedFloor, out _, out _) && expectedFloor == 0,
                    "authored local-height band maps the probe to floor zero");
                Check(!LocalFloorVisibilityPresentation.IsVisible(FloorVisibilityBuilding.SectionVisibility.Floor, 2, 4, 2),
                    "floor section at the cutoff is hidden by the authored elevation rule");
                BuiltInFrame(controller, camera);
                controller.BeginBuiltInCamera(camera);
                Check(lowFloor.enabled && !upperFloor.enabled,
                    "lower authored floor selected after dwell (selected=" + controller.CurrentFloorForValidation +
                    ", lower=" + lowFloor.enabled + ", upper=" + upperFloor.enabled +
                    ", baseline=" + controller.HasRendererBaselineForValidation(upperFloor) +
                    ", mapped=" + (low.sections[1].renderers[0] == upperFloor) + ")");
                Check(lowCover.enabled && !highCover.enabled && always.enabled, "lower cutoff hides only above-floor covering");
                Check(!originallyDisabled.enabled, "presentation preserves initially disabled renderers");
                End(controller, camera);
                Check(lowFloor.enabled && upperFloor.enabled && highCover.enabled && !originallyDisabled.enabled,
                    "built-in camera post-render restores baseline states");
                lowCover.enabled = false;
                controller.BeginBuiltInCamera(camera);
                Check(!lowCover.enabled, "external renderer disable is respected during the next filtered render");
                End(controller, camera);
                Check(!lowCover.enabled, "post-render restores the latest external renderer state");
                lowCover.enabled = true;

                probeObject.transform.position = new Vector3(0, 2.05f, 0);
                BuiltInFrame(controller, camera);
                controller.BeginBuiltInCamera(camera);
                Check(!upperFloor.enabled, "boundary hysteresis prevents a floor flap");
                End(controller, camera);
                probeObject.transform.position = new Vector3(0, 2.5f, 0);
                BuiltInFrame(controller, camera);
                controller.BeginBuiltInCamera(camera);
                Check(lowFloor.enabled && upperFloor.enabled && !highCover.enabled,
                    "stable elevation transition reveals the upper floor while keeping above-floor covering hidden");
                var nestedCamera = new GameObject("Nested validation camera").AddComponent<Camera>();
                controller.BeginBuiltInCamera(nestedCamera);
                Check(lowFloor.enabled && upperFloor.enabled && highCover.enabled && !originallyDisabled.enabled,
                    "nested camera receives the original unfiltered renderer state");
                controller.EndBuiltInCamera(nestedCamera);
                Check(lowFloor.enabled && upperFloor.enabled && !highCover.enabled,
                    "nested camera end restores the active local view");
                End(controller, camera);

                probeObject.transform.position = new Vector3(3, 2.5f, 0);
                BuiltInFrame(controller, camera);
                Check(lowFloor.enabled && upperFloor.enabled && highCover.enabled,
                    "outside the explicit occupancy volume restores full visibility");
                End(controller, camera);

                probeObject.transform.position = new Vector3(10, 5.5f, 0);
                BuiltInFrame(controller, camera);
                controller.BeginBuiltInCamera(camera);
                Check(raisedFloor.enabled && !raisedCover.enabled && lowCover.enabled,
                    "raised volume uses its own elevation schedule and shared building cutoff");
                End(controller, camera);

                probeObject.transform.position = new Vector3(10, 7.5f, 0);
                BuiltInFrame(controller, camera);
                controller.BeginBuiltInCamera(camera);
                Check(raisedFloor.enabled && raisedCover.enabled,
                    "raised volume floor transition restores its covering at its independent height");
                End(controller, camera);

                controller.BeginScriptableCamera(default(ScriptableRenderContext), camera);
                Check(raisedFloor.enabled && raisedCover.enabled, "scriptable camera begin applies selected view");
                controller.EndScriptableCamera(default(ScriptableRenderContext), camera);
                Check(raisedFloor.enabled && raisedCover.enabled,
                    "scriptable camera end restores renderer baseline");

                controller.BeginBuiltInCamera(camera);
                controller.enabled = false;
                Check(raisedFloor.enabled && raisedCover.enabled && !originallyDisabled.enabled,
                    "disable during an active render restores original renderer states");
                Check(low.occupancyVolume.enabled == lowColliderEnabled && low.occupancyVolume.isTrigger == lowColliderTrigger &&
                    high.occupancyVolume.enabled == highColliderEnabled && high.occupancyVolume.isTrigger == highColliderTrigger,
                    "occupancy collider state remains unchanged");
            }
            finally
            {
                UnityEngine.Object.DestroyImmediate(probeObject);
                UnityEngine.Object.DestroyImmediate(root);
                var nested = GameObject.Find("Nested validation camera");
                if (nested != null) UnityEngine.Object.DestroyImmediate(nested);
            }
        }

        static void BuiltInFrame(LocalFloorVisibilityPresentation controller, Camera camera)
        { controller.BeginBuiltInCamera(camera); controller.EndBuiltInCamera(camera); }

        static void End(LocalFloorVisibilityPresentation controller, Camera camera)
        { controller.EndBuiltInCamera(camera); }

        static BoxCollider AddOccupancyBox(Transform parent, string name, Vector3 position)
        {
            var boxObject = new GameObject(name);
            boxObject.transform.SetParent(parent, false);
            boxObject.transform.position = position;
            var box = boxObject.AddComponent<BoxCollider>();
            box.size = new Vector3(4, 4, 4);
            return box;
        }

        static Renderer AddRenderer(Transform parent, string name, bool enabled)
        {
            var obj = GameObject.CreatePrimitive(PrimitiveType.Cube);
            obj.name = name;
            obj.transform.SetParent(parent, false);
            var renderer = obj.GetComponent<Renderer>();
            renderer.enabled = enabled;
            return renderer;
        }

        static FloorVisibilityBuilding.FloorBand Band(int index, float minimum, float maximum) =>
            new FloorVisibilityBuilding.FloorBand { floorIndex = index, minimumLocalHeight = minimum, maximumLocalHeight = maximum };

        static FloorVisibilityBuilding.Section Section(FloorVisibilityBuilding.SectionVisibility visibility,
            int index, float minimum, float maximum, params Renderer[] renderers) =>
            new FloorVisibilityBuilding.Section
            {
                visibility = visibility, floorIndex = index,
                minimumLocalHeight = minimum, maximumLocalHeight = maximum, renderers = renderers
            };

        static void Check(bool condition, string message)
        {
            if (!condition) throw new InvalidOperationException("FLOOR_VISIBILITY_CHECK_FAILED: " + message);
        }
    }
}
