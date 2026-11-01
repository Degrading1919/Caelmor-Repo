using System;
using System.Collections.Generic;
using UnityEngine.AI;
using UnityEngine;

namespace Caelmor.Unity.Playable
{
    /// <summary>Executable checks against real host ticks and scene collision geometry.</summary>
    public static class PlayableValidation
    {
        public static void Run(InteractionAnchor anchor, int mask, TerrainNavigation navigation)
        {
            Physics.SyncTransforms();
            Check(navigation != null && navigation.data != null, "persisted navigation asset must survive scene/player load");
            navigation.Bind();
            using (var host = new PlayableHost(new Vector3(0, 0, -4), anchor, mask))
            {
                Check(host.IsReady, "fresh restore/session/lifecycle/residency must complete");
                var initial = host.Snapshot;
                host.SubmitMove(Vector2.up, false);
                Check(host.Snapshot.Position == initial.Position && host.Snapshot.Tick == 0, "input must not mutate state before tick");
                int publishedSnapshots = 0;
                host.SnapshotCommitted += snapshot => { Check(snapshot.Tick == host.Simulation.CurrentTickIndex, "snapshot publication tick"); publishedSnapshots++; };
                host.Step();
                Check(publishedSnapshots == 1 && host.Snapshot.Tick == 1, "single tick commit");
                Near(host.Snapshot.Position.z, -3.7f, "walk displacement uses 100ms");
                host.SubmitMove(Vector2.up, true); host.Step();
                Near(host.Snapshot.Position.z, -3.15f, "sprint displacement uses 100ms");
                var before = host.Snapshot.Position;
                host.SubmitMove(Vector2.one, false); host.Step();
                Near(Vector3.Distance(host.Snapshot.Position, before), .3f, "diagonal speed normalized");
                before = host.Snapshot.Position; host.Step();
                Check(host.Snapshot.Position == before && host.Snapshot.InteractionCount == 0, "idle stays still");
                before = host.Snapshot.Position; host.Step();
                Check(host.Snapshot.Position == before, "missing commands stop movement");
                host.SubmitInteraction(anchor.fixtureId); host.Step();
                Check(host.Snapshot.InteractionCount == 0 && host.Snapshot.Feedback.Contains("Out of reach"), "out of range rejected");
                Check(!host.SubmitMove(new Vector2(float.NaN, 0), false), "non-finite input rejected");
                host.SuspendForValidation(true);
                Check(!host.IsReady && !host.SubmitMove(Vector2.up, false), "inactive lifecycle blocks input");
                int beforeSuspendedSnapshots = publishedSnapshots;
                host.Step(); Check(host.Snapshot.Position == before, "inactive lifecycle blocks simulation");
                Check(publishedSnapshots == beforeSuspendedSnapshots, "inactive lifecycle suppresses client snapshots");
                host.SuspendForValidation(false); Check(host.IsReady, "reactivation restores eligibility");
                host.DetachForValidation();
                Check(!host.IsReady && !host.SubmitInteraction(anchor.fixtureId), "missing residency blocks input and interaction");
                host.Step(); Check(publishedSnapshots == beforeSuspendedSnapshots && host.Snapshot.Position == before,
                    "missing residency suppresses client snapshots and movement");
            }
            using (var host = new PlayableHost(anchor.transform.position + Vector3.back * 1.7f, anchor, mask))
            {
                int events = 0;
                host.InteractionCommitted += (session, id, tick) =>
                { Check(id == anchor.fixtureId && tick == host.Snapshot.Tick, "event emitted only after committed snapshot"); events++; };
                host.SubmitInteraction(-1); host.Step(); Check(host.Snapshot.InteractionCount == 0, "unknown target rejected");
                host.SubmitInteraction(anchor.fixtureId); host.ClearPendingInput(); host.Step();
                Check(host.Snapshot.InteractionCount == 0 && events == 0, "focus/help boundary cancels queued interactions");
                host.SubmitInteraction(anchor.fixtureId);
                Check(!host.Snapshot.MarkerActive, "interaction not predicted");
                host.Step(); Check(host.Snapshot.MarkerActive && events == 1 && host.Snapshot.InteractionCount == 1, "legal interaction visibly committed");
                host.SubmitInteraction(anchor.fixtureId); host.Step();
                Check(!host.Snapshot.MarkerActive && events == 2, "second legal interaction updates state");
                anchor.zoneId++;
                try { host.SubmitInteraction(anchor.fixtureId); host.Step(); Check(events == 2, "cross-zone target rejected"); }
                finally { anchor.zoneId--; }
            }
            using (var host = new PlayableHost(new Vector3(0, 0, -4), anchor, mask))
            {
                for (int i = 0; i < 70; i++) { host.SubmitMove(Vector2.right, true); host.Step(); }
                Check(host.Snapshot.Position.x < 13.2f && host.Snapshot.Position.x > 12f, "swept collision respects east bound at sprint speed");
            }
            // A real temporary scene collider separates a nearby target from the authoritative player.
            var blocker = GameObject.CreatePrimitive(PrimitiveType.Cube);
            blocker.name = "Validation line of sight blocker"; blocker.layer = 8;
            blocker.transform.position = anchor.transform.position + new Vector3(0, 1, -.8f);
            blocker.transform.localScale = new Vector3(3, 2, .2f);
            Physics.SyncTransforms();
            try
            {
                using (var host = new PlayableHost(anchor.transform.position + Vector3.back * 1.7f, anchor, mask))
                { host.SubmitInteraction(anchor.fixtureId); host.Step(); Check(host.Snapshot.InteractionCount == 0 && host.Snapshot.Feedback.Contains("blocked"), "solid geometry rejects interaction"); }
            }
            finally { blocker.SetActive(false); UnityEngine.Object.DestroyImmediate(blocker); Physics.SyncTransforms(); }
            ValidateNavigation(anchor, mask, navigation);
            Debug.Log("CAELMOR_GAMEPLAY_CHECKS_PASSED: authority, click paths, obstacle avoidance, retarget, invalid/unreachable destinations, cancellation, normalized movement, walk/sprint, lifecycle, residency, reach, target, LOS, collision, committed events");
        }
        static void ValidateNavigation(InteractionAnchor anchor, int mask, TerrainNavigation navigation)
        {
            using (var host = new PlayableHost(new Vector3(-5, 0, -2), anchor, mask, navigation))
            {
                var start = host.Snapshot.Position;
                Check(host.SubmitDestination(new Vector3(-5, 0, 4)), "destination intent accepted");
                Check(host.Snapshot.Position == start && !host.Snapshot.HasDestination, "click cannot mutate state before authoritative tick");
                float furthestSide = 0;
                bool arrived = false;
                for (int i = 0; i < 160; i++)
                {
                    var previous = host.Snapshot.Position; host.Step();
                    Check(Vector3.Distance(previous, host.Snapshot.Position) <= .305f, "path obeys walk speed on every100ms tick");
                    furthestSide = Mathf.Max(furthestSide, Mathf.Abs(host.Snapshot.Position.x + 5));
                    if (!host.Snapshot.HasDestination) { arrived = true; break; }
                }
                Check(arrived && Vector3.Distance(host.Snapshot.Position, new Vector3(-5, 0, 4)) < .06f, "route reaches exact ground destination around wall");
                Check(furthestSide > 2.8f, "route must actually travel around the real wall, not through it");
                var stopped = host.Snapshot.Position; host.Step(); host.Step();
                Check(host.Snapshot.Position == stopped, "arrival stops without oscillation");
            }
            using (var host = new PlayableHost(new Vector3(0, 0, -4), anchor, mask, navigation))
            {
                host.SubmitDestination(new Vector3(0, 0, 8)); host.Step();
                Check(host.Snapshot.HasDestination, "route persists without held input");
                var before = host.Snapshot.Position;
                host.SubmitDestination(new Vector3(6, 0, -4)); host.Step();
                Check(Vector3.Distance(before, host.Snapshot.Position) > .29f && host.Snapshot.HasDestination,
                    "retarget moves on same tick without idle interruption");
                Near(host.Snapshot.Destination.x, 6, "replacement destination selected");
                host.SubmitDestination(new Vector3(6, 0, 5)); host.Step();
                Check(host.Snapshot.HasDestination && host.Snapshot.Destination.x > 5.9f && host.Snapshot.Destination.z < -3.9f,
                    "obstacle destination rejected while valid existing route continues");
                host.SubmitDestination(new Vector3(25, 0, 0)); host.Step();
                Check(host.Snapshot.HasDestination && host.Snapshot.Destination.x > 5.9f, "off-terrain destination cannot replace valid route");
                Check(!host.SubmitDestination(new Vector3(float.NaN, 0, 0)) && !host.SubmitDestination(new Vector3(0, 2, 0)),
                    "nonfinite and elevated forged destinations rejected");
                host.ClearPendingInput(); before = host.Snapshot.Position; host.Step();
                Check(host.Snapshot.Position == before && !host.Snapshot.HasDestination, "focus/help cancellation stops committed route");
                host.SubmitDestination(new Vector3(0, 0, 8)); host.Step();
                host.SuspendForValidation(true); before = host.Snapshot.Position; host.Step();
                host.SuspendForValidation(false); host.Step();
                Check(!host.Snapshot.HasDestination && host.Snapshot.Position == before, "suspended route never silently resumes");
            }
            using (var host = new PlayableHost(new Vector3(0, 0, -4), anchor, mask, navigation))
            {
                host.SubmitDestination(anchor.transform.position + Vector3.back * 1.6f);
                for (int i = 0; i < 60; i++) { host.Step(); if (!host.Snapshot.HasDestination) break; }
                Check(Vector3.Distance(host.Snapshot.Position, anchor.transform.position) < 1.7f, "path approaches interaction fixture");
                host.SubmitInteraction(anchor.fixtureId); host.Step();
                Check(host.Snapshot.InteractionCount == 1, "interaction still succeeds after click route arrival");
            }
            var obstruction = GameObject.CreatePrimitive(PrimitiveType.Cube);
            obstruction.name = "Validation dynamic obstruction"; obstruction.layer = 8;
            obstruction.transform.position = new Vector3(0, 1, -2); obstruction.transform.localScale = new Vector3(3, 2, .3f);
            Physics.SyncTransforms();
            try
            {
                using (var host = new PlayableHost(new Vector3(0, 0, -4), anchor, mask, navigation))
                {
                    host.SubmitDestination(new Vector3(0, 0, 2));
                    for (int i = 0; i < 30; i++) { host.Step(); if (!host.Snapshot.HasDestination) break; }
                    Check(!host.Snapshot.HasDestination && host.Snapshot.Position.z < -2.4f && host.Snapshot.Feedback.Contains("blocked"),
                        "new collider invalidating baked path stops safely rather than tunnelling or spinning");
                }
            }
            finally { obstruction.SetActive(false); UnityEngine.Object.DestroyImmediate(obstruction); Physics.SyncTransforms(); }
            // A separate native NavMesh island is navigable but cannot be reached from the player mesh.
            var island = GameObject.CreatePrimitive(PrimitiveType.Cube); island.layer = 8;
            island.transform.position = new Vector3(40, -.25f, 0); island.transform.localScale = new Vector3(4, .5f, 4);
            island.AddComponent<NavigableTerrain>(); Physics.SyncTransforms();
            var sources = new List<NavMeshBuildSource>();
            NavMeshBuilder.CollectSources(new Bounds(new Vector3(40, 0, 0), new Vector3(5, 3, 5)), mask,
                NavMeshCollectGeometry.PhysicsColliders, 0, new List<NavMeshBuildMarkup>(), sources);
            var islandData = NavMeshBuilder.BuildNavMeshData(NavMesh.GetSettingsByIndex(0), sources,
                new Bounds(new Vector3(40, 0, 0), new Vector3(5, 3, 5)), Vector3.zero, Quaternion.identity);
            var islandInstance = NavMesh.AddNavMeshData(islandData);
            try
            {
                using (var host = new PlayableHost(new Vector3(0, 0, -4), anchor, mask, navigation))
                {
                    host.SubmitDestination(new Vector3(40, 0, 0)); host.Step();
                    Check(!host.Snapshot.HasDestination && host.Snapshot.Position == new Vector3(0, 0, -4),
                        "complete path required; unreachable navigable island rejected");
                }
            }
            finally { islandInstance.Remove(); UnityEngine.Object.DestroyImmediate(islandData); island.SetActive(false); UnityEngine.Object.DestroyImmediate(island); }
        }
        static void Check(bool condition, string reason) { if (!condition) throw new InvalidOperationException("PLAYABLE_ASSERT: " + reason); }
        static void Near(float actual, float expected, string reason) { Check(Mathf.Abs(actual - expected) < .006f, reason + " actual=" + actual + " expected=" + expected); }
    }
}

