using System;
using System.Collections;
using Caelmor.Runtime.WorldSimulation;
using UnityEngine;

namespace Caelmor.Unity.Playable
{
    public sealed class PlayableBootstrap : MonoBehaviour
    {
        public Transform playerView;
        public Camera playerCamera;
        public InteractionAnchor interactionAnchor;
        public Transform spawn;
        public TerrainNavigation navigation;
        public Transform destinationView;
        public bool DebugMovementEnabled { get; private set; }
        public int solidLayerMask = 1 << 8;
        public PlayableHost Host { get; private set; }
        public LowmarkGame Lowmark { get; private set; }
        public bool HelpOpen { get; private set; }
        public string StartupFailure { get; private set; }
        internal bool PersistenceWriteBlocked { get; private set; }
        public event Action<PlayableHost> HostInitialized;
        double accumulator;
        double lastSnapshotTime;
        PlayableSnapshot previous;
        float yaw, pitch = 32f, zoom = 7.5f;
        bool smoke;

        void Start()
        {
            try
            {
                Application.targetFrameRate = 120;
                QualitySettings.vSyncCount = 1;
                smoke = Array.IndexOf(Environment.GetCommandLineArgs(), "--caelmor-smoke") >= 0;
                Physics.SyncTransforms();
                Host = new PlayableHost(spawn.position, interactionAnchor, solidLayerMask, navigation);
                Lowmark = gameObject.AddComponent<LowmarkGame>();
                Lowmark.Initialize(this);
                if(!Application.isBatchMode)Lowmark.ApplyRequestedCheckpoint();
                previous = Host.Snapshot;
                lastSnapshotTime = Time.realtimeSinceStartupAsDouble;
                Host.SnapshotCommitted += OnSnapshot;
                playerView.position = Host.Snapshot.Position;
                HostInitialized?.Invoke(Host);
                if (smoke) StartCoroutine(RunSmoke());
            }
            catch (Exception error)
            {
                StartupFailure = error.ToString();
                Debug.LogException(error);
                if (Array.IndexOf(Environment.GetCommandLineArgs(), "--caelmor-smoke") >= 0) Application.Quit(1);
            }
        }
        void OnSnapshot(PlayableSnapshot snapshot)
        {
            lastSnapshotTime = Time.realtimeSinceStartupAsDouble;
        }
        internal void BlockForPersistenceError(string message)
        {
            PersistenceWriteBlocked=true;StartupFailure="Progress could not be saved. Gameplay stopped to preserve your active quests.\n"+message;
            Host?.ClearPendingInput();accumulator=0;
        }
        internal void ClearPersistenceError()
        {
            if(!PersistenceWriteBlocked)return;
            PersistenceWriteBlocked=false;StartupFailure=null;Host?.ClearPendingInput();accumulator=0;
        }
        void Update()
        {
            if (Host == null || StartupFailure != null) return;
            if (!Application.isBatchMode && Input.GetKeyDown(KeyCode.Escape))
            {
                HelpOpen = !HelpOpen;
                Host.ClearPendingInput(); accumulator = 0;
            }
            if (!smoke && !HelpOpen && Application.isFocused)
            {
                if (Input.GetKeyDown(KeyCode.F3)) { DebugMovementEnabled = !DebugMovementEnabled; Host.ClearPendingInput(); }
                if (Input.GetKeyDown(KeyCode.E)) Lowmark.InteractNearest();
                if (Input.GetMouseButtonDown(0)) TryClickDestination(Input.mousePosition);
            }
            accumulator += Math.Min(Time.unscaledDeltaTime, .3f);
            int catchUp = 0;
            while (accumulator >= WorldTickSeconds && catchUp++ < 3)
            {
                Vector2 direction = Vector2.zero;
                bool sprint = false;
                if (!smoke && !HelpOpen && Application.isFocused)
                {
                    float x = DebugMovementEnabled ? (Input.GetKey(KeyCode.D) ? 1 : 0) - (Input.GetKey(KeyCode.A) ? 1 : 0) : 0;
                    float z = DebugMovementEnabled ? (Input.GetKey(KeyCode.W) ? 1 : 0) - (Input.GetKey(KeyCode.S) ? 1 : 0) : 0;
                    var local = new Vector3(x, 0, z);
                    var world = Quaternion.Euler(0, yaw, 0) * local;
                    direction = new Vector2(world.x, world.z);
                    sprint = Input.GetKey(KeyCode.LeftShift) || Input.GetKey(KeyCode.RightShift);
                }
                if (direction.sqrMagnitude > .0001f) Host.SubmitMove(direction, sprint);
                else Host.SubmitSprint(sprint);
                previous = Host.Snapshot;
                Host.Step();
                accumulator -= WorldTickSeconds;
            }
            // Drop excessive accumulated wall time instead of speeding up the simulation after a stall.
            if (catchUp >= 3 && accumulator >= WorldTickSeconds) accumulator = 0;
        }
        internal bool TryClickDestination(Vector2 screenPoint)
        {
            if (Host == null || HelpOpen || !Application.isFocused || PlayableHud.BlocksPointer(this, screenPoint)) return false;
            var ray = playerCamera.ScreenPointToRay(screenPoint);
            if (Lowmark != null && Lowmark.TrySelect(ray)) return true;
            if (!Physics.Raycast(ray, out var hit, 250f, solidLayerMask, QueryTriggerInteraction.Ignore) ||
                hit.collider.GetComponent<NavigableTerrain>() == null || hit.normal.y < .7f) return false;
            Lowmark?.CancelApproach();
            return Host.SubmitDestination(hit.point);
        }
        static readonly double WorldTickSeconds = WorldSimulationCore.TickInterval.TotalSeconds;
        void ToggleHelpFromHud(){HelpOpen=!HelpOpen;Host.ClearPendingInput();accumulator=0;}
        void OnApplicationFocus(bool focused)
        { if (Host != null) { Host.ClearPendingInput(); accumulator = 0; } }
        void OnApplicationPause(bool paused)
        { if (Host != null) { Host.ClearPendingInput(); accumulator = 0; } }
        void LateUpdate()
        {
            if (Host == null || StartupFailure != null) return;
            var state = Host.Snapshot;
            if (destinationView != null)
            {
                destinationView.gameObject.SetActive(state.HasDestination);
                destinationView.position = state.Destination+Vector3.up*.025f;
            }
            float alpha = Mathf.Clamp01((float)((Time.realtimeSinceStartupAsDouble - lastSnapshotTime) / WorldTickSeconds));
            playerView.position = Vector3.Lerp(previous.Position, state.Position, alpha);
            if (state.Facing.sqrMagnitude > .001f)
                playerView.rotation = Quaternion.Slerp(playerView.rotation, Quaternion.LookRotation(state.Facing), Time.unscaledDeltaTime * 14f);
            if (!HelpOpen && Input.GetMouseButton(1))
            {
                yaw += Input.GetAxis("Mouse X") * 3f;
                pitch = Mathf.Clamp(pitch - Input.GetAxis("Mouse Y") * 2.5f, 15, 70);
            }
            zoom = Mathf.Clamp(zoom - Input.mouseScrollDelta.y * .7f, 3f, 12f);
            var focus = playerView.position + Vector3.up * 1.25f;
            var rotation = Quaternion.Euler(pitch, yaw, 0);
            var offset = rotation * Vector3.back;
            float distance = zoom;
            if (Physics.SphereCast(focus, .2f, offset, out var hit, zoom, solidLayerMask, QueryTriggerInteraction.Ignore))
                distance = Mathf.Max(.3f, hit.distance - .15f);
            playerCamera.transform.SetPositionAndRotation(focus + offset * distance, rotation);
            if (interactionAnchor.markerRenderer != null)
                interactionAnchor.markerRenderer.material.color = state.MarkerActive ? new Color(.27f, .85f, .68f) : new Color(.85f, .65f, .28f);
        }
        IEnumerator RunSmoke()
        {
            yield return null;
            try
            {
                PlayableValidation.Run(interactionAnchor, solidLayerMask, navigation);
                LowmarkValidation.Run(interactionAnchor, solidLayerMask, navigation);
            }
            catch (Exception error)
            {
                Debug.LogError("CAELMOR_SMOKE_FAILED: " + error);
                Application.Quit(1);
                yield break;
            }
            // Synchronous validation can stall one frame. Drain that frame before sampling
            // the live scheduler so its legitimate catch-up is not charged to this interval.
            accumulator=0;
            yield return null;
            accumulator=0;
            long before = Host.Snapshot.Tick;
            double sampleStart=Time.realtimeSinceStartupAsDouble;
            yield return new WaitForSecondsRealtime(1.15f);
            long ticks = Host.Snapshot.Tick - before;
            double elapsed=Time.realtimeSinceStartupAsDouble-sampleStart;
            if (ticks < Math.Floor(elapsed/WorldTickSeconds)-1 || ticks > Math.Ceiling(elapsed/WorldTickSeconds)+1)
            {
                Debug.LogError("CAELMOR_SMOKE_FAILED: live 10Hz scheduler advanced " + ticks + " ticks in " + elapsed.ToString("F3") + " seconds");
                Application.Quit(1); yield break;
            }
            Debug.Log("CAELMOR_SMOKE_PASSED: deterministic gameplay assertions and live 10Hz scheduler (" + ticks + " ticks in " + elapsed.ToString("F3") + " seconds)");
            Application.Quit(0);
        }
        void OnDestroy()
        {
            if (Host != null) { Host.SnapshotCommitted -= OnSnapshot; Host.Dispose(); Host = null; }
        }
    }
}
