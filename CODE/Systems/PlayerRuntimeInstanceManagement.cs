using System;
using System.Collections.Generic;

namespace Caelmor.Runtime.Players
{
    /// <summary>
    /// Server-side runtime player instance manager.
    /// Creates, tracks, and destroys Player runtime instances independent of sessions.
    /// Foundational infrastructure only: no zones, ticks, lifecycle, sessions, saves, or world logic.
    /// </summary>
    public sealed class PlayerRuntimeInstanceManager : IPlayerRuntimeInstanceManager
    {
        private readonly IServerAuthority _authority;

        private readonly object _gate = new object();

        // One instance per PlayerId.
        private readonly Dictionary<PlayerId, PlayerHandle> _handleByPlayerId = new Dictionary<PlayerId, PlayerHandle>();
        private readonly Dictionary<PlayerHandle, PlayerRuntimeInstance> _instanceByHandle = new Dictionary<PlayerHandle, PlayerRuntimeInstance>();

        // Deterministic handle allocation within this server process.
        private int _nextHandle = 1;

        public PlayerRuntimeInstanceManager(IServerAuthority authority)
        {
            _authority = authority ?? throw new ArgumentNullException(nameof(authority));
        }

        /// <summary>
        /// Creates (or returns) a runtime instance for the given PlayerId.
        /// Server-authoritative and idempotent: repeated calls return the same instance and handle.
        /// </summary>
        public CreatePlayerResult CreatePlayer(PlayerId playerId)
        {
            if (!_authority.IsServerAuthoritative)
                return CreatePlayerResult.Failed(CreatePlayerFailureReason.NotServerAuthority);

            if (!playerId.IsValid)
                return CreatePlayerResult.Failed(CreatePlayerFailureReason.InvalidPlayerId);

            lock (_gate)
            {
                if (_handleByPlayerId.TryGetValue(playerId, out var existingHandle))
                {
                    if (_instanceByHandle.TryGetValue(existingHandle, out var existingInstance))
                        return CreatePlayerResult.Success(existingHandle, existingInstance, wasCreated: false);

                    // Defensive: reconcile inconsistent state deterministically by recreating instance from known mapping.
                    var reconstructed = new PlayerRuntimeInstance(playerId, existingHandle);
                    _instanceByHandle[existingHandle] = reconstructed;
                    return CreatePlayerResult.Success(existingHandle, reconstructed, wasCreated: false);
                }

                var handle = AllocateHandle();
                var instance = new PlayerRuntimeInstance(playerId, handle);

                _handleByPlayerId.Add(playerId, handle);
                _instanceByHandle.Add(handle, instance);

                return CreatePlayerResult.Success(handle, instance, wasCreated: true);
            }
        }

        /// <summary>
        /// Returns true if a runtime instance exists for the PlayerId.
        /// </summary>
        public bool Exists(PlayerId playerId)
        {
            if (!playerId.IsValid)
                return false;

            lock (_gate)
            {
                return _handleByPlayerId.ContainsKey(playerId);
            }
        }

        /// <summary>
        /// Tries to get the runtime instance handle for a PlayerId.
        /// </summary>
        public bool TryGetHandle(PlayerId playerId, out PlayerHandle handle)
        {
            handle = default;

            if (!playerId.IsValid)
                return false;

            lock (_gate)
            {
                return _handleByPlayerId.TryGetValue(playerId, out handle);
            }
        }

        /// <summary>
        /// Tries to get the runtime instance by PlayerId.
        /// </summary>
        public bool TryGetInstance(PlayerId playerId, out PlayerRuntimeInstance instance)
        {
            instance = default;

            if (!playerId.IsValid)
                return false;

            lock (_gate)
            {
                if (!_handleByPlayerId.TryGetValue(playerId, out var handle))
                    return false;

                return _instanceByHandle.TryGetValue(handle, out instance);
            }
        }

        /// <summary>
        /// Tries to get the runtime instance by handle.
        /// </summary>
        public bool TryGetInstance(PlayerHandle handle, out PlayerRuntimeInstance instance)
        {
            instance = default;

            if (!handle.IsValid)
                return false;

            lock (_gate)
            {
                return _instanceByHandle.TryGetValue(handle, out instance);
            }
        }

        /// <summary>
        /// Destroys the runtime instance for a PlayerId.
        /// Deterministic cleanup with no side effects beyond runtime state removal.
        /// Idempotent: returns false if no instance exists.
        /// </summary>
        public bool DestroyPlayer(PlayerId playerId)
        {
            if (!_authority.IsServerAuthoritative)
                return false;

            if (!playerId.IsValid)
                return false;

            lock (_gate)
            {
                if (!_handleByPlayerId.TryGetValue(playerId, out var handle))
                    return false;

                _handleByPlayerId.Remove(playerId);
                _instanceByHandle.Remove(handle);
                return true;
            }
        }

        /// <summary>
        /// Destroys the runtime instance by handle.
        /// Deterministic cleanup with no side effects beyond runtime state removal.
        /// Idempotent: returns false if no instance exists.
        /// </summary>
        public bool DestroyPlayer(PlayerHandle handle)
        {
            if (!_authority.IsServerAuthoritative)
                return false;

            if (!handle.IsValid)
                return false;

            lock (_gate)
            {
                if (!_instanceByHandle.TryGetValue(handle, out var inst))
                    return false;

                _instanceByHandle.Remove(handle);
                _handleByPlayerId.Remove(inst.PlayerId);
                return true;
            }
        }

        private PlayerHandle AllocateHandle()
        {
            var value = _nextHandle++;
            if (value <= 0) value = 1;
            return new PlayerHandle(value);
        }
    }

    public interface IPlayerRuntimeInstanceManager
    {
        CreatePlayerResult CreatePlayer(PlayerId playerId);

        bool Exists(PlayerId playerId);

        bool TryGetHandle(PlayerId playerId, out PlayerHandle handle);

        bool TryGetInstance(PlayerId playerId, out PlayerRuntimeInstance instance);

        bool TryGetInstance(PlayerHandle handle, out PlayerRuntimeInstance instance);

        bool DestroyPlayer(PlayerId playerId);

        bool DestroyPlayer(PlayerHandle handle);
    }

    public readonly struct CreatePlayerResult
    {
        public readonly bool Ok;
        public readonly PlayerHandle Handle;
        public readonly PlayerRuntimeInstance Instance;
        public readonly bool WasCreated;
        public readonly CreatePlayerFailureReason FailureReason;

        private CreatePlayerResult(bool ok, PlayerHandle handle, PlayerRuntimeInstance instance, bool wasCreated, CreatePlayerFailureReason failureReason)
        {
            Ok = ok;
            Handle = handle;
            Instance = instance;
            WasCreated = wasCreated;
            FailureReason = failureReason;
        }

        public static CreatePlayerResult Success(PlayerHandle handle, PlayerRuntimeInstance instance, bool wasCreated)
            => new CreatePlayerResult(true, handle, instance, wasCreated, CreatePlayerFailureReason.None);

        public static CreatePlayerResult Failed(CreatePlayerFailureReason reason)
            => new CreatePlayerResult(false, default, default, false, reason);
    }

    public enum CreatePlayerFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidPlayerId = 2
    }

    /// <summary>
    /// Minimal runtime definition of a Player instance.
    /// Defines identity and opaque runtime handle only.
    /// </summary>
    public readonly struct PlayerRuntimeInstance : IEquatable<PlayerRuntimeInstance>
    {
        public readonly PlayerId PlayerId;
        public readonly PlayerHandle Handle;

        public PlayerRuntimeInstance(PlayerId playerId, PlayerHandle handle)
        {
            PlayerId = playerId;
            Handle = handle;
        }

        public bool Equals(PlayerRuntimeInstance other) => PlayerId.Equals(other.PlayerId) && Handle.Equals(other.Handle);
        public override bool Equals(object obj) => obj is PlayerRuntimeInstance other && Equals(other);
        public override int GetHashCode() => HashCode.Combine(PlayerId, Handle);
        public override string ToString() => $"PlayerRuntimeInstance(PlayerId={PlayerId}, Handle={Handle})";
    }

    /// <summary>
    /// Opaque server-issued PlayerId.
    /// </summary>
    public readonly struct PlayerId : IEquatable<PlayerId>
    {
        public readonly Guid Value;

        public PlayerId(Guid value)
        {
            Value = value;
        }

        public bool IsValid => Value != Guid.Empty;

        public bool Equals(PlayerId other) => Value.Equals(other.Value);
        public override bool Equals(object obj) => obj is PlayerId other && Equals(other);
        public override int GetHashCode() => Value.GetHashCode();
        public override string ToString() => Value.ToString();
    }

    /// <summary>
    /// Opaque runtime handle for the Player instance.
    /// </summary>
    public readonly struct PlayerHandle : IEquatable<PlayerHandle>
    {
        public readonly int Value;

        public PlayerHandle(int value)
        {
            Value = value;
        }

        public bool IsValid => Value > 0;

        public bool Equals(PlayerHandle other) => Value == other.Value;
        public override bool Equals(object obj) => obj is PlayerHandle other && Equals(other);
        public override int GetHashCode() => Value;
        public override string ToString() => Value.ToString();
    }
}
