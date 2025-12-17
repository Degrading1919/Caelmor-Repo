using System;
using System.Collections.Generic;
using Caelmor.Runtime.Onboarding;

namespace Caelmor.Runtime.Persistence
{
    /// <summary>
    /// Server-side runtime system that binds a server-authoritative PlayerId to exactly one SaveId.
    /// Binding only: no disk IO, no serialization, no world loading, and no client-authored identifiers.
    /// </summary>
    public sealed class PlayerSaveBindingSystem : IPlayerSaveBindingSystem
    {
        private readonly IServerAuthority _authority;
        private readonly ISaveIdAllocator _saveAllocator;

        // Two-way map must remain consistent; guarded by a single gate for atomicity/determinism.
        private readonly object _gate = new object();
        private readonly Dictionary<PlayerId, SaveId> _saveByPlayer = new Dictionary<PlayerId, SaveId>();
        private readonly Dictionary<SaveId, PlayerId> _playerBySave = new Dictionary<SaveId, PlayerId>();

        public PlayerSaveBindingSystem(IServerAuthority authority, ISaveIdAllocator saveAllocator)
        {
            _authority = authority ?? throw new ArgumentNullException(nameof(authority));
            _saveAllocator = saveAllocator ?? throw new ArgumentNullException(nameof(saveAllocator));
        }

        /// <summary>
        /// Returns the SaveId bound to the given PlayerId.
        /// If none exists, allocates a new SaveId server-side and binds it atomically.
        /// Idempotent: repeated calls return the same SaveId.
        /// Rejects invalid PlayerId and any attempt to rebind to a different save.
        /// </summary>
        public BindSaveResult BindOrGetSaveForPlayer(PlayerId playerId)
        {
            if (!_authority.IsServerAuthoritative)
                return BindSaveResult.Failed(BindSaveFailureReason.NotServerAuthority);

            if (!playerId.IsValid)
                return BindSaveResult.Failed(BindSaveFailureReason.InvalidPlayerId);

            lock (_gate)
            {
                if (_saveByPlayer.TryGetValue(playerId, out var existing))
                    return BindSaveResult.Success(existing, wasCreated: false);

                // Allocate new SaveId via server-only allocator (no client input).
                var newSaveId = _saveAllocator.AllocateForPlayer(playerId);
                if (!newSaveId.IsValid)
                    return BindSaveResult.Failed(BindSaveFailureReason.SaveAllocationFailed);

                // Enforce one-save-to-one-player uniqueness.
                if (_playerBySave.TryGetValue(newSaveId, out var otherPlayer))
                {
                    if (!otherPlayer.Equals(playerId))
                        return BindSaveResult.Failed(BindSaveFailureReason.SaveAlreadyBoundToDifferentPlayer);

                    // If allocator returned a SaveId already bound to this player, just ensure the forward map.
                    _saveByPlayer[playerId] = newSaveId;
                    return BindSaveResult.Success(newSaveId, wasCreated: false);
                }

                _saveByPlayer.Add(playerId, newSaveId);
                _playerBySave.Add(newSaveId, playerId);
                return BindSaveResult.Success(newSaveId, wasCreated: true);
            }
        }

        /// <summary>
        /// Attempts to retrieve an existing binding without allocating.
        /// </summary>
        public bool TryGetSaveForPlayer(PlayerId playerId, out SaveId saveId)
        {
            saveId = default;

            if (!playerId.IsValid)
                return false;

            lock (_gate)
            {
                return _saveByPlayer.TryGetValue(playerId, out saveId);
            }
        }

        /// <summary>
        /// Returns true if the player has an existing save binding.
        /// </summary>
        public bool HasBinding(PlayerId playerId)
        {
            if (!playerId.IsValid)
                return false;

            lock (_gate)
            {
                return _saveByPlayer.ContainsKey(playerId);
            }
        }

        /// <summary>
        /// Validation hook: asserts one-to-one invariant across both maps.
        /// Deterministic and side-effect free.
        /// </summary>
        public bool ValidateOneToOneBinding(out string error)
        {
            error = string.Empty;

            lock (_gate)
            {
                if (_saveByPlayer.Count != _playerBySave.Count)
                {
                    error = "Binding maps have mismatched counts.";
                    return false;
                }

                foreach (var kvp in _saveByPlayer)
                {
                    var player = kvp.Key;
                    var save = kvp.Value;

                    if (!player.IsValid || !save.IsValid)
                    {
                        error = "Invalid PlayerId or SaveId exists in binding map.";
                        return false;
                    }

                    if (!_playerBySave.TryGetValue(save, out var backPlayer))
                    {
                        error = "Forward binding missing reverse entry.";
                        return false;
                    }

                    if (!backPlayer.Equals(player))
                    {
                        error = "Forward and reverse bindings disagree.";
                        return false;
                    }
                }

                foreach (var kvp in _playerBySave)
                {
                    var save = kvp.Key;
                    var player = kvp.Value;

                    if (!_saveByPlayer.TryGetValue(player, out var backSave))
                    {
                        error = "Reverse binding missing forward entry.";
                        return false;
                    }

                    if (!backSave.Equals(save))
                    {
                        error = "Reverse and forward bindings disagree.";
                        return false;
                    }
                }

                return true;
            }
        }

        /// <summary>
        /// Validation hook: rejects any attempt to bind a player to an explicit SaveId.
        /// This method exists to make the prohibition explicit in the API surface.
        /// </summary>
        public BindSaveResult RejectClientSuppliedSaveId(PlayerId playerId, SaveId clientSuppliedSaveId)
        {
            _ = playerId;
            _ = clientSuppliedSaveId;
            return BindSaveResult.Failed(BindSaveFailureReason.ClientSuppliedSaveIdRejected);
        }
    }

    public interface IPlayerSaveBindingSystem
    {
        BindSaveResult BindOrGetSaveForPlayer(PlayerId playerId);
        bool TryGetSaveForPlayer(PlayerId playerId, out SaveId saveId);
        bool HasBinding(PlayerId playerId);
        bool ValidateOneToOneBinding(out string error);
        BindSaveResult RejectClientSuppliedSaveId(PlayerId playerId, SaveId clientSuppliedSaveId);
    }

    /// <summary>
    /// Server-only SaveId allocation source (binding only; no IO).
    /// Implementations may consult an in-memory index, reserved ids, or a later SaveSystem.
    /// </summary>
    public interface ISaveIdAllocator
    {
        SaveId AllocateForPlayer(PlayerId playerId);
    }

    public readonly struct BindSaveResult
    {
        public readonly bool Ok;
        public readonly SaveId SaveId;
        public readonly bool WasCreated;
        public readonly BindSaveFailureReason FailureReason;

        private BindSaveResult(bool ok, SaveId saveId, bool wasCreated, BindSaveFailureReason failureReason)
        {
            Ok = ok;
            SaveId = saveId;
            WasCreated = wasCreated;
            FailureReason = failureReason;
        }

        public static BindSaveResult Success(SaveId saveId, bool wasCreated)
            => new BindSaveResult(true, saveId, wasCreated, BindSaveFailureReason.None);

        public static BindSaveResult Failed(BindSaveFailureReason reason)
            => new BindSaveResult(false, default, false, reason);
    }

    public enum BindSaveFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidPlayerId = 2,
        SaveAllocationFailed = 3,
        SaveAlreadyBoundToDifferentPlayer = 4,
        ClientSuppliedSaveIdRejected = 5
    }

    /// <summary>
    /// Opaque persisted SaveId reference.
    /// </summary>
    public readonly struct SaveId : IEquatable<SaveId>
    {
        public readonly Guid Value;

        public SaveId(Guid value)
        {
            Value = value;
        }

        public bool IsValid => Value != Guid.Empty;

        public bool Equals(SaveId other) => Value.Equals(other.Value);
        public override bool Equals(object obj) => obj is SaveId other && Equals(other);
        public override int GetHashCode() => Value.GetHashCode();
        public override string ToString() => Value.ToString();
    }
}
