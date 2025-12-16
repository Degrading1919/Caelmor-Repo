using System;
using System.Collections.Generic;
using Caelmor.Runtime.Players;
using Caelmor.Runtime.Onboarding;
using Caelmor.Systems;

namespace Caelmor.Runtime.ZoneResidency
{
    /// <summary>
    /// Server-side runtime system enforcing single-zone residency per player.
    /// Explicit attach/detach operations only; no lifecycle, tick, or simulation ownership.
    /// Deterministic, idempotent where applicable, and constant-time queries.
    /// </summary>
    public sealed class PlayerZoneResidencySystem : IPlayerZoneResidencySystem
    {
        private readonly IServerAuthority _authority;
        private readonly object _gate = new object();
        private readonly Dictionary<PlayerHandle, ZoneId> _zoneByPlayer = new Dictionary<PlayerHandle, ZoneId>();

        public PlayerZoneResidencySystem(IServerAuthority authority)
        {
            _authority = authority ?? throw new ArgumentNullException(nameof(authority));
        }

        /// <summary>
        /// Attaches a player to a zone if and only if the player is not already resident.
        /// Rejected deterministically when server authority is missing, identifiers are invalid, or residency already exists.
        /// </summary>
        public AttachPlayerToZoneResult AttachPlayerToZone(PlayerHandle player, ZoneId zone)
        {
            if (!_authority.IsServerAuthoritative)
                return AttachPlayerToZoneResult.Failed(AttachPlayerToZoneFailureReason.NotServerAuthority);

            if (!player.IsValid)
                return AttachPlayerToZoneResult.Failed(AttachPlayerToZoneFailureReason.InvalidPlayerHandle);

            if (zone.Value <= 0)
                return AttachPlayerToZoneResult.Failed(AttachPlayerToZoneFailureReason.InvalidZoneId);

            lock (_gate)
            {
                if (_zoneByPlayer.TryGetValue(player, out var existingZone))
                    return AttachPlayerToZoneResult.Failed(AttachPlayerToZoneFailureReason.AlreadyResident, existingZone);

                _zoneByPlayer[player] = zone;
                return AttachPlayerToZoneResult.Success(zone);
            }
        }

        /// <summary>
        /// Detaches a player from the specified zone. Idempotent and deterministic: returns failure without mutation when the player
        /// is not resident or is resident elsewhere.
        /// </summary>
        public DetachPlayerFromZoneResult DetachPlayerFromZone(PlayerHandle player, ZoneId zone)
        {
            if (!_authority.IsServerAuthoritative)
                return DetachPlayerFromZoneResult.Failed(DetachPlayerFromZoneFailureReason.NotServerAuthority);

            if (!player.IsValid)
                return DetachPlayerFromZoneResult.Failed(DetachPlayerFromZoneFailureReason.InvalidPlayerHandle);

            if (zone.Value <= 0)
                return DetachPlayerFromZoneResult.Failed(DetachPlayerFromZoneFailureReason.InvalidZoneId);

            lock (_gate)
            {
                if (!_zoneByPlayer.TryGetValue(player, out var existingZone))
                    return DetachPlayerFromZoneResult.Failed(DetachPlayerFromZoneFailureReason.NotResident);

                if (!existingZone.Equals(zone))
                    return DetachPlayerFromZoneResult.Failed(DetachPlayerFromZoneFailureReason.ResidentInDifferentZone, existingZone);

                _zoneByPlayer.Remove(player);
                return DetachPlayerFromZoneResult.Success(existingZone);
            }
        }

        /// <summary>
        /// True if the player is currently resident in any zone.
        /// </summary>
        public bool IsResident(PlayerHandle player)
        {
            if (!player.IsValid)
                return false;

            lock (_gate)
            {
                return _zoneByPlayer.ContainsKey(player);
            }
        }

        /// <summary>
        /// Returns true if the player is resident in the specified zone.
        /// </summary>
        public bool IsResident(PlayerHandle player, ZoneId zone)
        {
            if (!player.IsValid || zone.Value <= 0)
                return false;

            lock (_gate)
            {
                return _zoneByPlayer.TryGetValue(player, out var existing) && existing.Equals(zone);
            }
        }

        /// <summary>
        /// Attempts to get the resident zone for the player. Bounded-time constant lookup.
        /// </summary>
        public bool TryGetResidentZone(PlayerHandle player, out ZoneId zone)
        {
            zone = default;
            if (!player.IsValid)
                return false;

            lock (_gate)
            {
                return _zoneByPlayer.TryGetValue(player, out zone);
            }
        }
    }

    public interface IPlayerZoneResidencySystem
    {
        AttachPlayerToZoneResult AttachPlayerToZone(PlayerHandle player, ZoneId zone);
        DetachPlayerFromZoneResult DetachPlayerFromZone(PlayerHandle player, ZoneId zone);
        bool IsResident(PlayerHandle player);
        bool IsResident(PlayerHandle player, ZoneId zone);
        bool TryGetResidentZone(PlayerHandle player, out ZoneId zone);
    }

    public readonly struct AttachPlayerToZoneResult
    {
        private AttachPlayerToZoneResult(bool ok, AttachPlayerToZoneFailureReason failureReason, ZoneId? existingZone)
        {
            Ok = ok;
            FailureReason = failureReason;
            ExistingZone = existingZone;
        }

        public bool Ok { get; }
        public AttachPlayerToZoneFailureReason FailureReason { get; }
        public ZoneId? ExistingZone { get; }

        public static AttachPlayerToZoneResult Success(ZoneId zone) => new AttachPlayerToZoneResult(true, AttachPlayerToZoneFailureReason.None, zone);

        public static AttachPlayerToZoneResult Failed(AttachPlayerToZoneFailureReason reason, ZoneId? existingZone = null) => new AttachPlayerToZoneResult(false, reason, existingZone);
    }

    public enum AttachPlayerToZoneFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidPlayerHandle = 2,
        InvalidZoneId = 3,
        AlreadyResident = 4
    }

    public readonly struct DetachPlayerFromZoneResult
    {
        private DetachPlayerFromZoneResult(bool ok, DetachPlayerFromZoneFailureReason failureReason, ZoneId? previousZone)
        {
            Ok = ok;
            FailureReason = failureReason;
            PreviousZone = previousZone;
        }

        public bool Ok { get; }
        public DetachPlayerFromZoneFailureReason FailureReason { get; }
        public ZoneId? PreviousZone { get; }

        public static DetachPlayerFromZoneResult Success(ZoneId previousZone) => new DetachPlayerFromZoneResult(true, DetachPlayerFromZoneFailureReason.None, previousZone);

        public static DetachPlayerFromZoneResult Failed(DetachPlayerFromZoneFailureReason reason, ZoneId? previousZone = null) => new DetachPlayerFromZoneResult(false, reason, previousZone);
    }

    public enum DetachPlayerFromZoneFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidPlayerHandle = 2,
        InvalidZoneId = 3,
        NotResident = 4,
        ResidentInDifferentZone = 5
    }
}
