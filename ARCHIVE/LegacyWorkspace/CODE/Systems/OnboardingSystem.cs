using System;
using System.Collections.Concurrent;

namespace Caelmor.Runtime.Onboarding
{
    /// <summary>
    /// Server-side onboarding runtime system.
    /// Transitions a connecting client session into a valid, tick-eligible player entity.
    /// Pure runtime infrastructure: identity binding, runtime instance creation, initial zone assignment,
    /// zone attachment, tick eligibility registration, and atomic completion signaling.
    /// </summary>
    public sealed class OnboardingSystem
    {
        private readonly IPlayerIdentitySystem _playerIdentitySystem;
        private readonly IPlayerLifecycleSystem _playerLifecycleSystem;
        private readonly IWorldManager _worldManager;
        private readonly IZoneManager _zoneManager;
        private readonly ITickEligibilityRegistry _tickEligibility;
        private readonly IOnboardingEvents _events;

        // Guards against duplicate onboarding calls for the same session.
        private readonly ConcurrentDictionary<SessionId, byte> _inFlight = new();

        public OnboardingSystem(
            IPlayerIdentitySystem playerIdentitySystem,
            IPlayerLifecycleSystem playerLifecycleSystem,
            IWorldManager worldManager,
            IZoneManager zoneManager,
            ITickEligibilityRegistry tickEligibility,
            IOnboardingEvents events)
        {
            _playerIdentitySystem = playerIdentitySystem ?? throw new ArgumentNullException(nameof(playerIdentitySystem));
            _playerLifecycleSystem = playerLifecycleSystem ?? throw new ArgumentNullException(nameof(playerLifecycleSystem));
            _worldManager = worldManager ?? throw new ArgumentNullException(nameof(worldManager));
            _zoneManager = zoneManager ?? throw new ArgumentNullException(nameof(zoneManager));
            _tickEligibility = tickEligibility ?? throw new ArgumentNullException(nameof(tickEligibility));
            _events = events ?? throw new ArgumentNullException(nameof(events));
        }

        /// <summary>
        /// Accepts a server-validated session join event and onboards the player atomically.
        /// Client identifiers are not trusted; identity is bound/created server-side only.
        /// </summary>
        public void HandleClientJoin(IServerSession session)
        {
            if (session is null) throw new ArgumentNullException(nameof(session));
            if (!session.IsServerAuthoritative)
            {
                // Defensive: onboarding must only occur on the host-authoritative server.
                _events.OnboardingFailed(session, OnboardingFailureReason.NotServerAuthority, "Onboarding invoked without server authority.");
                return;
            }

            if (!_inFlight.TryAdd(session.Id, 0))
            {
                _events.OnboardingFailed(session, OnboardingFailureReason.DuplicateSession, "Duplicate onboarding request for session.");
                return;
            }

            var txn = new OnboardingTransaction(session);

            try
            {
                // 1) Accept connection/session event (already server-side).
                //    Do NOT trust client identifiers. Only use server-issued SessionId.

                // 2) Bind or create Player Identity (server-side PlayerId generation).
                txn.PlayerId = _playerIdentitySystem.BindOrCreateIdentity(session);

                if (!txn.PlayerId.HasValue)
                {
                    Fail(txn, OnboardingFailureReason.IdentityBindingFailed, "Player identity binding failed.");
                    return;
                }

                // 3) Create Player Runtime Instance (inactive until fully attached).
                txn.PlayerHandle = _playerLifecycleSystem.CreateRuntimePlayer(txn.PlayerId.Value);

                if (!txn.PlayerHandle.HasValue)
                {
                    Fail(txn, OnboardingFailureReason.RuntimeCreationFailed, "Runtime player instance creation failed.");
                    return;
                }

                _playerLifecycleSystem.SetActive(txn.PlayerHandle.Value, isActive: false);

                // 4) Assign Initial Zone (deterministic + placeholder-safe).
                //    No lore assumptions. Determinism is delegated to World/Zone managers.
                txn.ZoneId = DetermineInitialZoneId(txn);

                if (!txn.ZoneId.HasValue)
                {
                    Fail(txn, OnboardingFailureReason.ZoneAssignmentFailed, "Initial zone assignment failed.");
                    return;
                }

                // 5) Attach Player to Zone (register residency; enforce zone authority boundaries).
                if (!_zoneManager.AttachPlayerToZone(txn.PlayerHandle.Value, txn.ZoneId.Value))
                {
                    Fail(txn, OnboardingFailureReason.ZoneAttachmentFailed, "Failed to attach player to initial zone.");
                    return;
                }

                txn.AttachedToZone = true;

                // 6) Register Tick Eligibility ONLY after identity binding + zone attachment.
                if (!_tickEligibility.TrySetTickEligible(txn.PlayerHandle.Value, isEligible: true))
                {
                    Fail(txn, OnboardingFailureReason.TickEligibilityFailed, "Failed to register tick eligibility.");
                    return;
                }

                txn.TickEligible = true;

                // Final control handoff: now safe to activate runtime player.
                _playerLifecycleSystem.SetActive(txn.PlayerHandle.Value, isActive: true);

                // 7) Emit completion signal (success).
                _events.OnboardingCompleted(session, txn.PlayerId.Value, txn.PlayerHandle.Value, txn.ZoneId.Value);
            }
            catch (Exception ex)
            {
                // Fail atomically; no residual state allowed.
                Fail(txn, OnboardingFailureReason.Exception, ex.Message);
            }
            finally
            {
                // Always cleanup in-flight guard.
                _inFlight.TryRemove(session.Id, out _);

                // Ensure rollback on any failure path.
                if (!txn.Succeeded)
                {
                    Rollback(txn);
                }
            }
        }

        private ZoneId? DetermineInitialZoneId(OnboardingTransaction txn)
        {
            // Deterministic, placeholder-safe selection.
            // Delegates selection to authoritative systems; this class does not hardcode lore.
            // The WorldManager may consult server config, region routing, or deterministic defaults.
            var worldId = _worldManager.GetActiveWorldId();
            if (!worldId.HasValue) return null;

            var zoneId = _worldManager.GetDefaultInitialZone(worldId.Value);
            if (!zoneId.HasValue) return null;

            // Optional: validate zone exists and is hosted by this server.
            if (!_zoneManager.IsZoneKnown(zoneId.Value)) return null;
            if (!_zoneManager.IsZoneAuthoritativeHere(zoneId.Value)) return null;

            return zoneId.Value;
        }

        private void Fail(OnboardingTransaction txn, OnboardingFailureReason reason, string message)
        {
            txn.Succeeded = false;
            _events.OnboardingFailed(txn.Session, reason, message);
        }

        private void Rollback(OnboardingTransaction txn)
        {
            // Reverse order of creation/registration.
            try
            {
                if (txn.TickEligible && txn.PlayerHandle.HasValue)
                {
                    _tickEligibility.TrySetTickEligible(txn.PlayerHandle.Value, isEligible: false);
                    txn.TickEligible = false;
                }
            }
            catch { /* best-effort rollback */ }

            try
            {
                if (txn.AttachedToZone && txn.PlayerHandle.HasValue && txn.ZoneId.HasValue)
                {
                    _zoneManager.DetachPlayerFromZone(txn.PlayerHandle.Value, txn.ZoneId.Value);
                    txn.AttachedToZone = false;
                }
            }
            catch { /* best-effort rollback */ }

            try
            {
                if (txn.PlayerHandle.HasValue)
                {
                    _playerLifecycleSystem.DestroyRuntimePlayer(txn.PlayerHandle.Value);
                    txn.PlayerHandle = null;
                }
            }
            catch { /* best-effort rollback */ }

            try
            {
                if (txn.PlayerId.HasValue)
                {
                    _playerIdentitySystem.UnbindIdentity(txn.Session);
                    txn.PlayerId = null;
                }
            }
            catch { /* best-effort rollback */ }
        }

        private sealed class OnboardingTransaction
        {
            public OnboardingTransaction(IServerSession session)
            {
                Session = session;
            }

            public IServerSession Session { get; }
            public PlayerId? PlayerId { get; set; }
            public PlayerHandle? PlayerHandle { get; set; }
            public ZoneId? ZoneId { get; set; }
            public bool AttachedToZone { get; set; }
            public bool TickEligible { get; set; }
            public bool Succeeded { get; set; } = true;
        }
    }

    /// <summary>Server session abstraction (server-issued identifiers only).</summary>
    public interface IServerSession
    {
        SessionId Id { get; }
        bool IsServerAuthoritative { get; }
    }

    /// <summary>Responsible for server-side identity binding and authoritative PlayerId generation.</summary>
    public interface IPlayerIdentitySystem
    {
        /// <summary>Bind an existing identity or create a new one for the session; returns null on failure.</summary>
        PlayerId? BindOrCreateIdentity(IServerSession session);

        /// <summary>Unbind identity from the session; used for rollback on failure.</summary>
        void UnbindIdentity(IServerSession session);
    }

    /// <summary>Responsible for runtime player instance lifecycle (create/activate/destroy).</summary>
    public interface IPlayerLifecycleSystem
    {
        /// <summary>Create a runtime player instance for a known PlayerId; returns null on failure.</summary>
        PlayerHandle? CreateRuntimePlayer(PlayerId playerId);

        /// <summary>Activates/deactivates the runtime player (inactive until zone-attached + tick-eligible).</summary>
        void SetActive(PlayerHandle handle, bool isActive);

        /// <summary>Destroy runtime player instance; used for rollback or disconnect handling elsewhere.</summary>
        void DestroyRuntimePlayer(PlayerHandle handle);
    }

    /// <summary>World authority and initial spawn routing.</summary>
    public interface IWorldManager
    {
        WorldId? GetActiveWorldId();

        /// <summary>Deterministic default initial zone for a world (placeholder-safe; no lore assumptions here).</summary>
        ZoneId? GetDefaultInitialZone(WorldId worldId);
    }

    /// <summary>Zone authority and residency attachment boundaries.</summary>
    public interface IZoneManager
    {
        bool IsZoneKnown(ZoneId zoneId);
        bool IsZoneAuthoritativeHere(ZoneId zoneId);

        /// <summary>Registers player residency in the zone; returns false on failure.</summary>
        bool AttachPlayerToZone(PlayerHandle player, ZoneId zoneId);

        /// <summary>Removes residency registration; best-effort rollback.</summary>
        void DetachPlayerFromZone(PlayerHandle player, ZoneId zoneId);
    }

    /// <summary>Controls whether an entity participates in server ticks (10 Hz).</summary>
    public interface ITickEligibilityRegistry
    {
        /// <summary>Set tick eligibility; returns false if the registry rejects the change.</summary>
        bool TrySetTickEligible(PlayerHandle player, bool isEligible);
    }

    /// <summary>Onboarding completion/failure signaling (server-side only).</summary>
    public interface IOnboardingEvents
    {
        void OnboardingCompleted(IServerSession session, PlayerId playerId, PlayerHandle playerHandle, ZoneId zoneId);
        void OnboardingFailed(IServerSession session, OnboardingFailureReason reason, string message);
    }

    public enum OnboardingFailureReason
    {
        NotServerAuthority = 1,
        DuplicateSession = 2,
        IdentityBindingFailed = 3,
        RuntimeCreationFailed = 4,
        ZoneAssignmentFailed = 5,
        ZoneAttachmentFailed = 6,
        TickEligibilityFailed = 7,
        Exception = 8
    }

    /// <summary>Opaque server-issued session identifier.</summary>
    public readonly struct SessionId : IEquatable<SessionId>
    {
        public readonly Guid Value;
        public SessionId(Guid value) => Value = value;
        public bool Equals(SessionId other) => Value.Equals(other.Value);
        public override bool Equals(object obj) => obj is SessionId other && Equals(other);
        public override int GetHashCode() => Value.GetHashCode();
        public override string ToString() => Value.ToString();
    }

    /// <summary>Opaque server-issued player identifier.</summary>
    public readonly struct PlayerId : IEquatable<PlayerId>
    {
        public readonly Guid Value;
        public PlayerId(Guid value) => Value = value;
        public bool Equals(PlayerId other) => Value.Equals(other.Value);
        public override bool Equals(object obj) => obj is PlayerId other && Equals(other);
        public override int GetHashCode() => Value.GetHashCode();
        public override string ToString() => Value.ToString();
    }

    /// <summary>Opaque handle for the runtime player entity instance.</summary>
    public readonly struct PlayerHandle : IEquatable<PlayerHandle>
    {
        public readonly int Value;
        public PlayerHandle(int value) => Value = value;
        public bool Equals(PlayerHandle other) => Value == other.Value;
        public override bool Equals(object obj) => obj is PlayerHandle other && Equals(other);
        public override int GetHashCode() => Value;
        public override string ToString() => Value.ToString();
    }

    /// <summary>Opaque identifier for a zone instance.</summary>
    public readonly struct ZoneId : IEquatable<ZoneId>
    {
        public readonly int Value;
        public ZoneId(int value) => Value = value;
        public bool Equals(ZoneId other) => Value == other.Value;
        public override bool Equals(object obj) => obj is ZoneId other && Equals(other);
        public override int GetHashCode() => Value;
        public override string ToString() => Value.ToString();
    }

    /// <summary>Opaque identifier for the active world instance.</summary>
    public readonly struct WorldId : IEquatable<WorldId>
    {
        public readonly int Value;
        public WorldId(int value) => Value = value;
        public bool Equals(WorldId other) => Value == other.Value;
        public override bool Equals(object obj) => obj is WorldId other && Equals(other);
        public override int GetHashCode() => Value;
        public override string ToString() => Value.ToString();
    }
}
