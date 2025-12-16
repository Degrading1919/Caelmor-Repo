using System;
using System.Collections.Concurrent;

namespace Caelmor.Runtime.PlayerLifecycle
{
    /// <summary>
    /// Server-side player lifecycle runtime.
    /// Governs post-onboarding activation/deactivation and safe disconnect handling.
    /// Runtime infrastructure only: no saves, no gameplay logic, no zone transfers.
    /// </summary>
    public sealed class PlayerLifecycleSystem : IPlayerLifecycleSystem
    {
        private readonly IPlayerIdentitySystem _identity;
        private readonly IZoneManager _zones;
        private readonly ITickEligibilityRegistry _tick;
        private readonly IPlayerLifecycleEvents _events;

        // Keyed by runtime player handle.
        private readonly ConcurrentDictionary<PlayerHandle, PlayerLifecycleState> _stateByPlayer = new();

        // Keyed by server session id to runtime player handle.
        private readonly ConcurrentDictionary<SessionId, PlayerHandle> _playerBySession = new();

        public PlayerLifecycleSystem(
            IPlayerIdentitySystem identity,
            IZoneManager zones,
            ITickEligibilityRegistry tick,
            IPlayerLifecycleEvents events)
        {
            _identity = identity ?? throw new ArgumentNullException(nameof(identity));
            _zones = zones ?? throw new ArgumentNullException(nameof(zones));
            _tick = tick ?? throw new ArgumentNullException(nameof(tick));
            _events = events ?? throw new ArgumentNullException(nameof(events));
        }

        /// <summary>
        /// Registers a post-onboarding runtime player with a server session and identity.
        /// Player is created inactive and not tick-eligible until ActivatePlayer is called.
        /// </summary>
        public bool RegisterOnboardedPlayer(IServerSession session, PlayerId playerId, PlayerHandle player)
        {
            if (session is null) throw new ArgumentNullException(nameof(session));

            if (!session.IsServerAuthoritative)
                return false;

            if (!playerId.HasValue)
                return false;

            if (player.Value <= 0)
                return false;

            // Reject duplicate or malformed sessions.
            if (_playerBySession.ContainsKey(session.Id))
                return false;

            // Identity must be known server-side.
            if (!_identity.IsValidPlayerId(playerId))
                return false;

            var st = new PlayerLifecycleState
            {
                SessionId = session.Id,
                PlayerId = playerId,
                Player = player,
                IsActive = false,
                IsTickEligible = false
            };

            if (!_stateByPlayer.TryAdd(player, st))
                return false;

            if (!_playerBySession.TryAdd(session.Id, player))
            {
                _stateByPlayer.TryRemove(player, out _);
                return false;
            }

            return true;
        }

        /// <summary>
        /// Activates a player (onboarded → active).
        /// Grants tick eligibility. Idempotent.
        /// Activation is rejected if identity is invalid or zone attachment is missing.
        /// </summary>
        public bool ActivatePlayer(PlayerHandle player)
        {
            if (player.Value <= 0)
                return false;

            if (!_stateByPlayer.TryGetValue(player, out var st))
                return false;

            // Already active: idempotent success.
            if (st.IsActive)
                return true;

            // Identity must remain valid.
            if (!_identity.IsValidPlayerId(st.PlayerId))
                return false;

            // Must be attached to a zone before activation.
            if (!_zones.IsPlayerAttachedToAnyZone(player))
                return false;

            // Safe ordering: grant tick eligibility first, then mark active.
            if (!_tick.TrySetTickEligible(player, isEligible: true))
                return false;

            st.IsTickEligible = true;
            st.IsActive = true;
            _stateByPlayer[player] = st;

            _events.OnPlayerActivated(st.SessionId, st.PlayerId, player);
            return true;
        }

        /// <summary>
        /// Deactivates a player (active → inactive).
        /// Revokes tick eligibility. Idempotent.
        /// Does not save or destroy; preserves runtime state for explicit persistence elsewhere.
        /// </summary>
        public bool DeactivatePlayer(PlayerHandle player, DeactivationReason reason)
        {
            if (player.Value <= 0)
                return false;

            if (!_stateByPlayer.TryGetValue(player, out var st))
                return false;

            // Idempotent: if already inactive, ensure tick is not eligible and return success.
            if (!st.IsActive)
            {
                if (st.IsTickEligible)
                {
                    _tick.TrySetTickEligible(player, isEligible: false);
                    st.IsTickEligible = false;
                    _stateByPlayer[player] = st;
                }

                _events.OnPlayerDeactivated(st.SessionId, st.PlayerId, player, reason);
                return true;
            }

            // Safe ordering: revoke tick eligibility first, then mark inactive.
            if (st.IsTickEligible)
            {
                _tick.TrySetTickEligible(player, isEligible: false);
                st.IsTickEligible = false;
            }

            st.IsActive = false;
            _stateByPlayer[player] = st;

            _events.OnPlayerDeactivated(st.SessionId, st.PlayerId, player, reason);
            return true;
        }

        /// <summary>
        /// Handles session loss/disconnect. Must be safe to call multiple times.
        /// Ensures no lingering tick participation and no partial lifecycle state.
        /// </summary>
        public void HandleDisconnect(IServerSession session)
        {
            if (session is null) throw new ArgumentNullException(nameof(session));

            if (!_playerBySession.TryGetValue(session.Id, out var player))
            {
                // No registered player for this session: idempotent no-op.
                return;
            }

            // Deactivate is idempotent; ensures tick is revoked.
            DeactivatePlayer(player, DeactivationReason.Disconnect);
        }

        /// <summary>
        /// Unregisters a player mapping from session. Intended for higher-level teardown.
        /// Does not destroy runtime entities; only removes lifecycle tracking.
        /// Call DeactivatePlayer before calling this method.
        /// </summary>
        public bool UnregisterPlayer(IServerSession session)
        {
            if (session is null) throw new ArgumentNullException(nameof(session));

            if (!_playerBySession.TryRemove(session.Id, out var player))
                return false;

            _stateByPlayer.TryRemove(player, out _);
            return true;
        }

        /// <summary>
        /// Legacy hook used by other runtime systems to flip active state.
        /// This method enforces lifecycle rules and tick eligibility transitions.
        /// </summary>
        bool IPlayerLifecycleSystem.SetActive(PlayerHandle player, bool isActive)
        {
            return isActive
                ? ActivatePlayer(player)
                : DeactivatePlayer(player, DeactivationReason.Explicit);
        }

        private struct PlayerLifecycleState
        {
            public SessionId SessionId;
            public PlayerId PlayerId;
            public PlayerHandle Player;
            public bool IsActive;
            public bool IsTickEligible;
        }
    }

    /// <summary>Minimal server session abstraction for lifecycle hooks.</summary>
    public interface IServerSession
    {
        SessionId Id { get; }
        bool IsServerAuthoritative { get; }
    }

    /// <summary>Identity validation (server-side only).</summary>
    public interface IPlayerIdentitySystem
    {
        bool IsValidPlayerId(PlayerId playerId);
    }

    /// <summary>Zone residency checks only (no transfers).</summary>
    public interface IZoneManager
    {
        bool IsPlayerAttachedToAnyZone(PlayerHandle player);
    }

    /// <summary>Controls whether an entity participates in server ticks (10 Hz).</summary>
    public interface ITickEligibilityRegistry
    {
        bool TrySetTickEligible(PlayerHandle player, bool isEligible);
    }

    /// <summary>Lifecycle event sink (server-side only).</summary>
    public interface IPlayerLifecycleEvents
    {
        void OnPlayerActivated(SessionId sessionId, PlayerId playerId, PlayerHandle player);
        void OnPlayerDeactivated(SessionId sessionId, PlayerId playerId, PlayerHandle player, DeactivationReason reason);
    }

    /// <summary>Contract expected by other runtime systems.</summary>
    public interface IPlayerLifecycleSystem
    {
        bool SetActive(PlayerHandle player, bool isActive);
    }

    public enum DeactivationReason
    {
        Explicit = 1,
        Disconnect = 2
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
        public bool HasValue => Value != Guid.Empty;
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
}
