using System;
using System.Collections.Generic;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Persistence;

namespace Caelmor.Runtime.Sessions
{
    /// <summary>
    /// Server-side runtime wiring for Session activation and deactivation.
    /// Owns session records keyed by SessionId and binds/unbinds SessionId ↔ PlayerId.
    /// Enforces authority boundaries, activation gates, one-active-session-per-player, and reconnect semantics.
    /// No lifecycle transitions, no tick eligibility, no zones/world logic, no saves/IO, no networking implementation.
    /// </summary>
    public sealed class PlayerSessionSystem : IPlayerSessionSystem
    {
        private readonly IServerAuthority _authority;
        private readonly IPlayerSaveBindingQuery _saveBinding;
        private readonly IPersistenceRestoreQuery _restore;
        private readonly ISnapshotEligibilityRegistry _snapshotEligibility;
        private readonly ISessionMutationGate _mutationGate;
        private readonly ISessionEvents _events;
        private readonly SessionConflictPolicy _conflictPolicy;

        private readonly object _gate = new object();
        private readonly Dictionary<SessionId, SessionRecord> _sessionsById = new Dictionary<SessionId, SessionRecord>();
        private readonly Dictionary<PlayerId, SessionId> _activeSessionByPlayer = new Dictionary<PlayerId, SessionId>();

        public PlayerSessionSystem(
            IServerAuthority authority,
            IPlayerSaveBindingQuery saveBinding,
            IPersistenceRestoreQuery restore,
            ISnapshotEligibilityRegistry snapshotEligibility,
            ISessionMutationGate mutationGate,
            ISessionEvents events,
            SessionConflictPolicy conflictPolicy = SessionConflictPolicy.Replace)
        {
            _authority = authority ?? throw new ArgumentNullException(nameof(authority));
            _saveBinding = saveBinding ?? throw new ArgumentNullException(nameof(saveBinding));
            _restore = restore ?? throw new ArgumentNullException(nameof(restore));
            _snapshotEligibility = snapshotEligibility ?? throw new ArgumentNullException(nameof(snapshotEligibility));
            _mutationGate = mutationGate ?? throw new ArgumentNullException(nameof(mutationGate));
            _events = events ?? throw new ArgumentNullException(nameof(events));
            _conflictPolicy = conflictPolicy;
        }

        /// <summary>
        /// Activates a session and binds it to a server-authoritative PlayerId.
        /// Enforces Stage 23.2 gates:
        /// - mid-tick mutation forbidden
        /// - save binding must exist
        /// - persistence restore must be completed
        /// - snapshot eligibility granted on activation
        /// Also rejects any client-provided identifiers if a request shape is provided.
        /// </summary>
        public SessionActivationResult ActivateSession(SessionId sessionId, PlayerId serverResolvedPlayerId, ClientJoinRequest? clientRequest = null)
        {
            if (!_authority.IsServerAuthoritative)
                return SessionActivationResult.Failed(SessionActivationFailureReason.NotServerAuthority);

            if (!sessionId.IsValid)
                return SessionActivationResult.Failed(SessionActivationFailureReason.InvalidSessionId);

            if (!serverResolvedPlayerId.IsValid)
                return SessionActivationResult.Failed(SessionActivationFailureReason.InvalidPlayerId);

            if (!_mutationGate.CanMutateSessionsNow())
                return SessionActivationResult.Failed(SessionActivationFailureReason.MidTickMutationForbidden);

            if (clientRequest.HasValue)
            {
                var guard = ClientIdentifierRejectionGuards.RejectIfClientProvidedIdentifiersPresent(in clientRequest.Value);
                if (!guard.Ok)
                    return SessionActivationResult.Failed(SessionActivationFailureReason.ClientProvidedIdentifiersRejected);
            }

            if (!_saveBinding.TryGetSaveForPlayer(serverResolvedPlayerId, out var saveId))
                return SessionActivationResult.Failed(SessionActivationFailureReason.MissingSaveBinding);

            if (!_restore.IsRestoreCompleted(saveId))
                return SessionActivationResult.Failed(SessionActivationFailureReason.PersistenceRestoreIncomplete);

            lock (_gate)
            {
                if (_sessionsById.TryGetValue(sessionId, out var existing))
                {
                    if (existing.IsActive &&
                        existing.PlayerId.Equals(serverResolvedPlayerId) &&
                        existing.SaveId.Equals(saveId))
                    {
                        return SessionActivationResult.Success(sessionId, serverResolvedPlayerId, saveId, wasCreated: false);
                    }

                    return SessionActivationResult.Failed(SessionActivationFailureReason.SessionIdAlreadyInUse);
                }

                if (_activeSessionByPlayer.TryGetValue(serverResolvedPlayerId, out var otherSession))
                {
                    if (_conflictPolicy == SessionConflictPolicy.Reject)
                        return SessionActivationResult.Failed(SessionActivationFailureReason.PlayerAlreadyHasActiveSession);

                    InternalDeactivateLocked(otherSession, DeactivationReason.ReplacedByReconnect);
                }

                var record = new SessionRecord(sessionId, serverResolvedPlayerId, saveId, isActive: true);
                _sessionsById.Add(sessionId, record);
                _activeSessionByPlayer[serverResolvedPlayerId] = sessionId;

                _snapshotEligibility.TrySetSnapshotEligible(sessionId, isEligible: true);

                _events.OnSessionActivated(sessionId, serverResolvedPlayerId, saveId);

                return SessionActivationResult.Success(sessionId, serverResolvedPlayerId, saveId, wasCreated: true);
            }
        }

        /// <summary>
        /// Deactivates a session (disconnect event) and unbinds SessionId ↔ PlayerId mapping.
        /// Stage 23.2 strict ordering:
        /// 1) Snapshot eligibility revoked
        /// 2) World/zone participation ended (hook)
        /// 3) Session marked inactive (record removed)
        /// 4) Persistence save permitted (outside this system; implied by ordering + hook completion)
        /// Idempotent and deterministic.
        /// </summary>
        public SessionDeactivationResult DeactivateSession(SessionId sessionId)
        {
            if (!_authority.IsServerAuthoritative)
                return SessionDeactivationResult.Failed(SessionDeactivationFailureReason.NotServerAuthority);

            if (!sessionId.IsValid)
                return SessionDeactivationResult.Failed(SessionDeactivationFailureReason.InvalidSessionId);

            if (!_mutationGate.CanMutateSessionsNow())
                return SessionDeactivationResult.Failed(SessionDeactivationFailureReason.MidTickMutationForbidden);

            lock (_gate)
            {
                if (!_sessionsById.ContainsKey(sessionId))
                    return SessionDeactivationResult.Success(wasRemoved: false);

                InternalDeactivateLocked(sessionId, DeactivationReason.Disconnect);
                return SessionDeactivationResult.Success(wasRemoved: true);
            }
        }

        /// <summary>
        /// Reconnect support at the session layer only.
        /// Deterministic behavior matches constructor policy:
        /// - Reject: fails if Player already has an active session
        /// - Replace: deactivates old session then activates new session
        /// </summary>
        public SessionActivationResult TryRebindForReconnect(PlayerId serverResolvedPlayerId, SessionId newSessionId, ClientJoinRequest? clientRequest = null)
        {
            return ActivateSession(newSessionId, serverResolvedPlayerId, clientRequest);
        }

        /// <summary>
        /// Returns the PlayerId bound to a SessionId, if any (active sessions only).
        /// </summary>
        public bool TryGetPlayerForSession(SessionId sessionId, out PlayerId playerId)
        {
            playerId = default;

            if (!sessionId.IsValid)
                return false;

            lock (_gate)
            {
                if (_sessionsById.TryGetValue(sessionId, out var rec) && rec.IsActive)
                {
                    playerId = rec.PlayerId;
                    return true;
                }

                return false;
            }
        }

        /// <summary>
        /// Returns the active SessionId for a PlayerId, if any.
        /// </summary>
        public bool TryGetSessionForPlayer(PlayerId playerId, out SessionId sessionId)
        {
            sessionId = default;

            if (!playerId.IsValid)
                return false;

            lock (_gate)
            {
                return _activeSessionByPlayer.TryGetValue(playerId, out sessionId);
            }
        }

        /// <summary>
        /// Returns true if a session record exists and is active.
        /// </summary>
        public bool IsSessionActive(SessionId sessionId)
        {
            if (!sessionId.IsValid)
                return false;

            lock (_gate)
            {
                return _sessionsById.TryGetValue(sessionId, out var rec) && rec.IsActive;
            }
        }

        private void InternalDeactivateLocked(SessionId sessionId, DeactivationReason reason)
        {
            _snapshotEligibility.TrySetSnapshotEligible(sessionId, isEligible: false);

            if (!_sessionsById.TryGetValue(sessionId, out var rec))
                return;

            _events.OnSessionParticipationEnded(sessionId, rec.PlayerId, rec.SaveId, reason);

            _sessionsById.Remove(sessionId);

            if (rec.PlayerId.IsValid &&
                _activeSessionByPlayer.TryGetValue(rec.PlayerId, out var mapped) &&
                mapped.Equals(sessionId))
            {
                _activeSessionByPlayer.Remove(rec.PlayerId);
            }

            _events.OnSessionDeactivated(sessionId, rec.PlayerId, rec.SaveId, reason);
        }

        private readonly struct SessionRecord
        {
            public readonly SessionId SessionId;
            public readonly PlayerId PlayerId;
            public readonly SaveId SaveId;
            public readonly bool IsActive;

            public SessionRecord(SessionId sessionId, PlayerId playerId, SaveId saveId, bool isActive)
            {
                SessionId = sessionId;
                PlayerId = playerId;
                SaveId = saveId;
                IsActive = isActive;
            }
        }
    }

    public interface IPlayerSessionSystem
    {
        SessionActivationResult ActivateSession(SessionId sessionId, PlayerId serverResolvedPlayerId, ClientJoinRequest? clientRequest = null);
        SessionDeactivationResult DeactivateSession(SessionId sessionId);
        SessionActivationResult TryRebindForReconnect(PlayerId serverResolvedPlayerId, SessionId newSessionId, ClientJoinRequest? clientRequest = null);

        bool TryGetPlayerForSession(SessionId sessionId, out PlayerId playerId);
        bool TryGetSessionForPlayer(PlayerId playerId, out SessionId sessionId);
        bool IsSessionActive(SessionId sessionId);
    }

    public enum SessionConflictPolicy
    {
        Reject = 0,
        Replace = 1
    }

    public readonly struct SessionActivationResult
    {
        public readonly bool Ok;
        public readonly SessionId SessionId;
        public readonly PlayerId PlayerId;
        public readonly SaveId SaveId;
        public readonly bool WasCreated;
        public readonly SessionActivationFailureReason FailureReason;

        private SessionActivationResult(bool ok, SessionId sessionId, PlayerId playerId, SaveId saveId, bool wasCreated, SessionActivationFailureReason failureReason)
        {
            Ok = ok;
            SessionId = sessionId;
            PlayerId = playerId;
            SaveId = saveId;
            WasCreated = wasCreated;
            FailureReason = failureReason;
        }

        public static SessionActivationResult Success(SessionId sessionId, PlayerId playerId, SaveId saveId, bool wasCreated)
            => new SessionActivationResult(true, sessionId, playerId, saveId, wasCreated, SessionActivationFailureReason.None);

        public static SessionActivationResult Failed(SessionActivationFailureReason reason)
            => new SessionActivationResult(false, default, default, default, false, reason);
    }

    public enum SessionActivationFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidSessionId = 2,
        InvalidPlayerId = 3,
        ClientProvidedIdentifiersRejected = 4,
        MissingSaveBinding = 5,
        PersistenceRestoreIncomplete = 6,
        SessionIdAlreadyInUse = 7,
        PlayerAlreadyHasActiveSession = 8,
        MidTickMutationForbidden = 9
    }

    public readonly struct SessionDeactivationResult
    {
        public readonly bool Ok;
        public readonly bool WasRemoved;
        public readonly SessionDeactivationFailureReason FailureReason;

        private SessionDeactivationResult(bool ok, bool wasRemoved, SessionDeactivationFailureReason failureReason)
        {
            Ok = ok;
            WasRemoved = wasRemoved;
            FailureReason = failureReason;
        }

        public static SessionDeactivationResult Success(bool wasRemoved)
            => new SessionDeactivationResult(true, wasRemoved, SessionDeactivationFailureReason.None);

        public static SessionDeactivationResult Failed(SessionDeactivationFailureReason reason)
            => new SessionDeactivationResult(false, false, reason);
    }

    public enum SessionDeactivationFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidSessionId = 2,
        MidTickMutationForbidden = 3
    }

    public enum DeactivationReason
    {
        Disconnect = 1,
        ReplacedByReconnect = 2
    }

    public interface IPlayerSaveBindingQuery
    {
        bool TryGetSaveForPlayer(PlayerId playerId, out SaveId saveId);
    }

    public interface IPersistenceRestoreQuery
    {
        bool IsRestoreCompleted(SaveId saveId);
    }

    public interface ISnapshotEligibilityRegistry
    {
        bool TrySetSnapshotEligible(SessionId sessionId, bool isEligible);
    }

    public interface ISessionMutationGate
    {
        bool CanMutateSessionsNow();
    }

    public interface ISessionEvents
    {
        void OnSessionActivated(SessionId sessionId, PlayerId playerId, SaveId saveId);

        /// <summary>
        /// Must synchronously end world/zone participation for this session before the session is marked inactive.
        /// No world/zone logic is implemented here; this hook exists only to enforce ordering.
        /// </summary>
        void OnSessionParticipationEnded(SessionId sessionId, PlayerId playerId, SaveId saveId, DeactivationReason reason);

        void OnSessionDeactivated(SessionId sessionId, PlayerId playerId, SaveId saveId, DeactivationReason reason);
    }
}
