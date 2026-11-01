using System;
using UnityEngine;

namespace Caelmor.Unity.Playable
{
    /// <summary>Executable checks against real host ticks and scene collision geometry.</summary>
    public static class PlayableValidation
    {
        public static void Run(InteractionAnchor anchor, int mask)
        {
            Physics.SyncTransforms();
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
            Debug.Log("CAELMOR_GAMEPLAY_CHECKS_PASSED: authority, normalized movement, walk/sprint, lifecycle, residency, reach, target, LOS, collision, committed events");
        }
        static void Check(bool condition, string reason) { if (!condition) throw new InvalidOperationException("PLAYABLE_ASSERT: " + reason); }
        static void Near(float actual, float expected, string reason) { Check(Mathf.Abs(actual - expected) < .006f, reason + " actual=" + actual + " expected=" + expected); }
    }
}
