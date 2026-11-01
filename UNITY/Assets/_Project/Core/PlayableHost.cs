using System;
using System.Collections.Generic;
using System.Threading;
using Caelmor.Runtime.Integration;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Persistence;
using Caelmor.Runtime.Players;
using Caelmor.Runtime.PlayerLifecycle;
using Caelmor.Runtime.Sessions;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.WorldSimulation;
using Caelmor.Runtime.WorldState;
using Caelmor.Runtime.ZoneResidency;
using UnityEngine;
using PlayerHandle = Caelmor.Runtime.Players.PlayerHandle;

namespace Caelmor.Unity.Playable
{
    public readonly struct PlayableSnapshot
    {
        public readonly long Tick;
        public readonly Vector3 Position;
        public readonly Vector3 Facing;
        public readonly bool Sprinting;
        public readonly bool MarkerActive;
        public readonly int InteractionCount;
        public readonly string Feedback;
        public readonly bool HasDestination;
        public readonly Vector3 Destination;
        public PlayableSnapshot(long tick, Vector3 position, Vector3 facing, bool sprinting,
            bool markerActive, int interactionCount, string feedback, bool hasDestination = false, Vector3 destination = default)
        {
            Tick = tick; Position = position; Facing = facing; Sprinting = sprinting;
            MarkerActive = markerActive; InteractionCount = interactionCount; Feedback = feedback;
            HasDestination = hasDestination; Destination = destination;
        }
    }

    /// <summary>
    /// Unity host adapter, with one authoritative WorldSimulationCore clock. All methods belong to
    /// the creating Unity thread. Inputs contain direction/intent only; clients cannot supply position.
    /// Geometry, speeds, and marker behavior are technical fixture tuning, not production balance.
    /// </summary>
    public sealed class PlayableHost : IDisposable, ITickPhaseHook, ISimulationParticipant,
        ISimulationEligibilityGate, IAuthoritativeStateMutatingCommandHandler
    {
        const int MoveCommand = 101, SprintCommand = 102, InteractCommand = 103, DestinationCommand = 104;
        const float ArrivalTolerance = .025f;
        const float WalkSpeed = 3f, SprintSpeed = 5.5f, Radius = .38f, Skin = .025f;
        readonly int ownerThread = Thread.CurrentThread.ManagedThreadId;
        readonly DeterministicEntityRegistry entities = new DeterministicEntityRegistry();
        readonly AuthoritativeCommandIngestor commands = new AuthoritativeCommandIngestor();
        readonly SceneSessionContext context;
        readonly PlayerRuntimeInstanceManager players;
        readonly PlayerSessionSystem sessions;
        readonly PlayerZoneResidencySystem residency;
        readonly Caelmor.Runtime.PlayerLifecycle.PlayerLifecycleSystem lifecycle;
        readonly PlayerSaveRestoreSystem restore;
        readonly PlayerSaveBindingSystem bindings;
        readonly PlayerId playerId;
        readonly PlayerHandle player;
        readonly EntityHandle entity = new EntityHandle(1);
        readonly ZoneId zone;
        readonly InteractionAnchor anchor;
        readonly int collisionMask;
        readonly TerrainNavigation navigation;
        Vector3[] route = Array.Empty<Vector3>();
        int routeIndex;
        Vector3 destination;
        bool hasDestination, destinationRequested, debugMoveRequested;
        Vector3 requestedDestination;
        long inputSequence, lastConsumedSequence;
        Vector2 input;
        bool sprint, interact, inTick, disposed;
        int requestedTarget;
        Vector3 pendingPosition, pendingFacing;
        bool pendingMarker, pendingSprint;
        int pendingCount;
        string pendingFeedback;
        public readonly SessionId Session;
        internal WorldSimulationCore Simulation { get; }
        public PlayableSnapshot Snapshot { get; private set; }
        public bool IsReady => !disposed && IsEligible(entity);
        public string Name => "Playable session / restore / lifecycle / zone gate";

        /// <summary>
        /// Narrative systems may subscribe to committed intent acknowledgments. No dialogue,
        /// objectives, rewards or quest progression is inferred by this bridge.
        /// </summary>
        public event Action<SessionId, int, long> InteractionCommitted;
        public event Action<PlayableSnapshot> SnapshotCommitted;

        public PlayableHost(Vector3 spawn, InteractionAnchor interactionAnchor, int solidMask, TerrainNavigation terrainNavigation = null)
        {
            anchor = interactionAnchor ?? throw new ArgumentNullException(nameof(interactionAnchor));
            collisionMask = solidMask;
            navigation = terrainNavigation;
            navigation?.Bind();
            zone = new ZoneId(anchor.zoneId);
            Session = new SessionId(Guid.NewGuid());
            playerId = new PlayerId(Guid.NewGuid());
            context = new SceneSessionContext(this, spawn);
            bindings = new PlayerSaveBindingSystem(context, context);
            context.Bindings = bindings;
            restore = new PlayerSaveRestoreSystem(context, context, context);
            var binding = bindings.BindOrGetSaveForPlayer(playerId);
            Require(binding.Ok, "save_binding_failed");
            // This executable intentionally starts a fresh ephemeral fixture session. The real
            // restore state machine must complete its initialization before activation is permitted.
            Require(restore.RequestRestore(binding.SaveId).Ok, "fresh_session_restore_failed");
            players = new PlayerRuntimeInstanceManager(context);
            var created = players.CreatePlayer(playerId);
            Require(created.Ok, "player_creation_failed");
            player = created.Handle;
            residency = new PlayerZoneResidencySystem(context);
            lifecycle = new Caelmor.Runtime.PlayerLifecycle.PlayerLifecycleSystem(context, context, context, context, context);
            sessions = new PlayerSessionSystem(context, context, restore, context, context, context);
            Require(sessions.ActivateSession(Session, playerId).Ok, "session_activation_failed");
            Require(lifecycle.Register(Session, playerId, player).Ok, "lifecycle_registration_failed");
            Require(residency.AttachPlayerToZone(player, zone).Ok, "zone_attach_failed");
            Require(lifecycle.Activate(player).Ok, "lifecycle_activation_failed");
            Require(entities.Register(entity, zone), "entity_registration_failed");
            Snapshot = new PlayableSnapshot(0, context.RestoredSpawn, Vector3.forward, false, false, 0,
                "Host ready. Approach the marker and press E.");
            Simulation = new WorldSimulationCore(entities);
            Simulation.RegisterEligibilityGate(this);
            var registry = new CommandHandlerRegistry();
            registry.Register(MoveCommand, this); registry.Register(SprintCommand, this); registry.Register(InteractCommand, this);
            registry.Register(DestinationCommand, this);
            Simulation.RegisterPhaseHook(this, -100);
            Simulation.RegisterPhaseHook(new AuthoritativeCommandFreezeHook(commands, sessions), -90);
            Simulation.RegisterPhaseHook(new AuthoritativeCommandConsumeTickHook(commands, registry, sessions), -80);
            Simulation.RegisterParticipant(this, 0);
        }

        public bool IsEligible(EntityHandle candidate)
        {
            return candidate.Equals(entity) && sessions != null && sessions.IsSessionActive(Session) &&
                context.SnapshotEligible && context.SimulationEligible &&
                bindings.TryGetSaveForPlayer(playerId, out var save) && restore.IsRestoreCompleted(save) &&
                players.Exists(playerId) && residency.IsResident(player, zone) && lifecycle.IsSimulationEligible(player);
        }

        /// <summary>Server stamps tick and receive sequence; no client identity or position is accepted.</summary>
        public bool SubmitMove(Vector2 direction, bool wantsSprint)
        {
            AssertOwner();
            if (!IsReady || !Finite(direction.x) || !Finite(direction.y)) return false;
            direction = Vector2.ClampMagnitude(direction, 1f);
            bool a = Enqueue(MoveCommand, Mathf.RoundToInt(direction.x * 10000f), Mathf.RoundToInt(direction.y * 10000f));
            bool b = Enqueue(SprintCommand, wantsSprint ? 1 : 0, 0);
            return a && b;
        }
        /// <summary>Destination intent only: reachability is evaluated by the host during simulation.</summary>
        public bool SubmitDestination(Vector3 point)
        {
            AssertOwner();
            if (!IsReady || !Finite(point.x) || !Finite(point.y) || !Finite(point.z) ||
                Mathf.Abs(point.y - Snapshot.Position.y) > .08f || Mathf.Abs(point.x) > 1000 || Mathf.Abs(point.z) > 1000) return false;
            return Enqueue(DestinationCommand, Mathf.RoundToInt(point.x * 1000f), Mathf.RoundToInt(point.z * 1000f));
        }
        public bool SubmitSprint(bool wantsSprint)
        {
            AssertOwner(); return IsReady && Enqueue(SprintCommand, wantsSprint ? 1 : 0, 0);
        }
        public bool SubmitInteraction(int targetId)
        {
            AssertOwner();
            return IsReady && Enqueue(InteractCommand, targetId, 0);
        }
        public void ClearPendingInput()
        {
            AssertOwner(); Require(!inTick, "input_clear_mid_tick");
            commands.DropSession(Session); input = Vector2.zero; sprint = false; interact = false;
            destinationRequested = false; debugMoveRequested = false;
            hasDestination = false; route = Array.Empty<Vector3>(); routeIndex = 0;
        }
        bool Enqueue(int type, int a, int b) => commands.TryEnqueue(Session,
            new AuthoritativeCommand(Simulation.CurrentTickIndex + 1, type, a, b, ++inputSequence));

        public void Step()
        {
            AssertOwner();
            if (disposed) throw new ObjectDisposedException(nameof(PlayableHost));
            Require(!inTick, "reentrant_tick_forbidden");
            inTick = true;
            try { Simulation.ExecuteSingleTick(); }
            finally { inTick = false; }
        }
        public void OnPreTick(SimulationTickContext tick, IReadOnlyList<EntityHandle> eligible)
        {
            AssertOwner();
            pendingPosition = Snapshot.Position; pendingFacing = Snapshot.Facing;
            pendingMarker = Snapshot.MarkerActive; pendingCount = Snapshot.InteractionCount;
            pendingFeedback = Snapshot.Feedback; pendingSprint = false;
            // Debug direction is per-tick input; a validated destination persists until arrival or explicit cancellation.
            input = Vector2.zero; sprint = false; interact = false;
            destinationRequested = false; debugMoveRequested = false;
        }
        public void Handle(in AuthoritativeCommand command, SessionId session, SimulationTickContext tick)
        {
            AssertOwner();
            if (!inTick || !session.Equals(Session) || !IsReady || command.AuthoritativeTick > tick.TickIndex ||
                command.DeterministicSequence <= lastConsumedSequence) return;
            lastConsumedSequence = command.DeterministicSequence;
            if (command.CommandType == MoveCommand)
            {
                input = Vector2.ClampMagnitude(new Vector2(command.PayloadA / 10000f, command.PayloadB / 10000f), 1f);
                debugMoveRequested = input.sqrMagnitude > .0001f;
                if (debugMoveRequested) destinationRequested = false;
            }
            else if (command.CommandType == DestinationCommand)
            {
                requestedDestination = new Vector3(command.PayloadA / 1000f, Snapshot.Position.y, command.PayloadB / 1000f);
                destinationRequested = true; debugMoveRequested = false;
            }
            else if (command.CommandType == SprintCommand) sprint = command.PayloadA == 1;
            else if (command.CommandType == InteractCommand) { interact = true; requestedTarget = command.PayloadA; }
        }
        public void Execute(EntityHandle candidate, SimulationTickContext tick)
        {
            AssertOwner();
            if (!inTick || !IsEligible(candidate)) return;
            if (destinationRequested)
            {
                if (navigation != null && navigation.TryPath(Snapshot.Position, requestedDestination, collisionMask, out var nextRoute))
                {
                    route = nextRoute; routeIndex = 0; destination = route[route.Length - 1]; hasDestination = true;
                    pendingFeedback = "Following host-validated path.";
                }
                else pendingFeedback = "That destination is not reachable. Existing route retained.";
            }
            if (debugMoveRequested)
            {
                hasDestination = false; route = Array.Empty<Vector3>();
                var direction = new Vector3(input.x, 0, input.y);
                pendingSprint = sprint;
                pendingFacing = direction.normalized;
                pendingPosition = MoveWithCollision(Snapshot.Position,
                    direction * (sprint ? SprintSpeed : WalkSpeed) * (float)tick.FixedDelta.TotalSeconds);
            }
            else if (hasDestination)
            {
                float remaining = (sprint ? SprintSpeed : WalkSpeed) * (float)tick.FixedDelta.TotalSeconds;
                pendingSprint = sprint;
                // Consume the same tick's distance across corners; retargeting never inserts an idle tick.
                while (hasDestination && remaining > .0001f)
                {
                    if (routeIndex >= route.Length)
                    { hasDestination = false; pendingFeedback = "Destination reached."; break; }
                    var delta = route[routeIndex] - pendingPosition; delta.y = 0;
                    float distance = delta.magnitude;
                    if (distance <= ArrivalTolerance) { routeIndex++; continue; }
                    var direction = delta / distance;
                    float travel = Mathf.Min(remaining, distance);
                    var moved = MoveWithCollision(pendingPosition, direction * travel);
                    float actual = Vector3.Distance(moved, pendingPosition);
                    pendingFacing = direction; pendingPosition = moved; remaining -= travel;
                    if (actual + .004f < travel)
                    {
                        hasDestination = false; route = Array.Empty<Vector3>();
                        pendingFeedback = "Path blocked. Choose a new destination."; break;
                    }
                    if (distance - travel <= ArrivalTolerance) routeIndex++;
                    if (routeIndex >= route.Length)
                    { hasDestination = false; pendingFeedback = "Destination reached."; }
                }
                if (!hasDestination) pendingSprint = false;
            }
            if (!interact) return;
            if (anchor == null || !anchor.isActiveAndEnabled || requestedTarget != anchor.fixtureId)
                pendingFeedback = "Interaction rejected: target is unavailable.";
            else if (anchor.zoneId != zone.Value || !residency.IsResident(player, new ZoneId(anchor.zoneId)))
                pendingFeedback = "Interaction rejected: target is outside your resident zone.";
            else if (Vector3.Distance(pendingPosition, anchor.transform.position) > anchor.interactionRange)
                pendingFeedback = "Out of reach. Move closer to the marker.";
            else if (Physics.Linecast(pendingPosition + Vector3.up, anchor.transform.position + Vector3.up,
                collisionMask, QueryTriggerInteraction.Ignore))
                pendingFeedback = "Interaction blocked by solid geometry.";
            else
            {
                pendingMarker = !pendingMarker; pendingCount++;
                pendingFeedback = "Host acknowledged interaction at tick " + tick.TickIndex + ".";
            }
        }
        Vector3 MoveWithCollision(Vector3 start, Vector3 displacement)
        {
            // Swept capsule prevents tunnelling at sprint speed. A second sweep slides along walls.
            var position = start;
            for (int iteration = 0; iteration < 2 && displacement.sqrMagnitude > .000001f; iteration++)
            {
                float distance = displacement.magnitude;
                var direction = displacement / distance;
                if (!Physics.CapsuleCast(position + Vector3.up * .45f, position + Vector3.up * 1.4f,
                    Radius, direction, out var hit, distance + Skin, collisionMask, QueryTriggerInteraction.Ignore))
                { position += displacement; break; }
                float travelled = Mathf.Max(0, hit.distance - Skin);
                position += direction * travelled;
                displacement = Vector3.ProjectOnPlane(displacement - direction * travelled, hit.normal);
                displacement.y = 0;
            }
            position.y = start.y;
            return position;
        }
        public void OnPostTick(SimulationTickContext tick, IReadOnlyList<EntityHandle> eligible)
        {
            AssertOwner();
            bool committedInteraction = pendingCount > Snapshot.InteractionCount;
            // Single finalization boundary: presentation never reads partially simulated state.
            Snapshot = new PlayableSnapshot(tick.TickIndex, pendingPosition, pendingFacing, pendingSprint,
                pendingMarker, pendingCount, pendingFeedback, hasDestination, destination);
            if (!IsReady) return;
            SnapshotCommitted?.Invoke(Snapshot);
            if (committedInteraction) InteractionCommitted?.Invoke(Session, anchor.fixtureId, tick.TickIndex);
        }

        internal void SuspendForValidation(bool suspend)
        {
            AssertOwner();
            Require(!inTick, "lifecycle_mutation_mid_tick");
            if (suspend) { ClearPendingInput(); Require(lifecycle.Suspend(player).Ok, "suspend_failed"); }
            else Require(lifecycle.Activate(player).Ok, "resume_failed");
        }
        internal void DetachForValidation() { AssertOwner(); Require(!inTick, "detach_mid_tick"); ClearPendingInput(); residency.DetachPlayerFromZone(player, zone); }
        public void Dispose()
        {
            AssertOwner();
            if (disposed) return;
            Require(!inTick, "dispose_mid_tick");
            lifecycle.Deactivate(player, LifecycleTerminationReason.Explicit);
            residency.DetachPlayerFromZone(player, zone);
            sessions.DeactivateSession(Session);
            commands.Clear(); entities.ClearAll(); players.DestroyPlayer(playerId);
            Simulation.Dispose(); entities.Dispose(); disposed = true;
        }
        void AssertOwner()
        {
            if (Thread.CurrentThread.ManagedThreadId != ownerThread) throw new InvalidOperationException("PLAYABLE_HOST_THREAD_ONLY");
        }
        static bool Finite(float value) => !float.IsNaN(value) && !float.IsInfinity(value);
        static void Require(bool ok, string reason) { if (!ok) throw new InvalidOperationException(reason); }

        sealed class SceneSessionContext : Caelmor.Systems.IServerAuthority,
            ISaveIdAllocator, IPlayerSaveBindingQuery, IRestoreMutationGate, IPersistenceRehydration,
            ISnapshotEligibilityRegistry, ISessionMutationGate, ISessionEvents, IPlayerZoneResidencyQuery,
            IPlayerSimulationEligibility, ILifecycleMutationGate, IPlayerLifecycleEvents
        {
            readonly PlayableHost host;
            readonly Vector3 initialSpawn;
            public PlayerSaveBindingSystem Bindings;
            public Vector3 RestoredSpawn { get; private set; }
            public bool SnapshotEligible { get; private set; }
            public bool SimulationEligible { get; private set; }
            public bool IsServerAuthoritative => !host.disposed;
            public SceneSessionContext(PlayableHost host, Vector3 spawn) { this.host = host; initialSpawn = spawn; }
            public SaveId AllocateForPlayer(PlayerId id) => id.IsValid ? new SaveId(Guid.NewGuid()) : default;
            public bool TryGetSaveForPlayer(PlayerId id, out SaveId save) => Bindings.TryGetSaveForPlayer(id, out save);
            public bool CanRestoreNow() => !host.inTick && !host.disposed;
            public RestoreOperationResult PerformRestore(SaveId save)
            {
                if (!Bindings.TryGetSaveForPlayer(host.playerId, out var bound) || !save.Equals(bound))
                    return RestoreOperationResult.Failed(RestoreOperationFailureReason.Unknown);
                RestoredSpawn = initialSpawn;
                return RestoreOperationResult.Success();
            }
            public bool TrySetSnapshotEligible(SessionId id, bool enabled)
            { if (!id.Equals(host.Session)) return false; SnapshotEligible = enabled; return true; }
            public bool CanMutateSessionsNow() => !host.inTick;
            public void OnSessionActivated(SessionId session, PlayerId id, SaveId save) { }
            public void OnSessionParticipationEnded(SessionId session, PlayerId id, SaveId save, DeactivationReason reason)
            { SimulationEligible = false; }
            public void OnSessionDeactivated(SessionId session, PlayerId id, SaveId save, DeactivationReason reason) { }
            public bool IsResident(PlayerHandle handle) => host.residency != null && host.residency.IsResident(handle);
            public bool TrySetSimulationEligible(PlayerHandle handle, bool enabled)
            { if (!handle.Equals(host.player)) return false; SimulationEligible = enabled; return true; }
            public bool CanMutateLifecycleNow() => !host.inTick;
            public void OnPlayerActivated(SessionId session, PlayerId id, PlayerHandle handle) { }
            public void OnPlayerSuspended(SessionId session, PlayerId id, PlayerHandle handle) { }
            public void OnPlayerDeactivated(SessionId session, PlayerId id, PlayerHandle handle, LifecycleTerminationReason reason) { }
        }
    }
}
