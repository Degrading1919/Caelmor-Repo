using System;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Persistence;

namespace Caelmor.Runtime.Sessions
{
    /// <summary>
    /// Session system wrapper that keeps a deterministic active session index in sync with mutations.
    /// </summary>
    public sealed class ActiveSessionIndexedPlayerSessionSystem : IPlayerSessionSystem
    {
        private readonly PlayerSessionSystem _inner;
        private readonly DeterministicActiveSessionIndex _activeSessions;

        public ActiveSessionIndexedPlayerSessionSystem(
            IServerAuthority authority,
            IPlayerSaveBindingQuery saveBinding,
            IPersistenceRestoreQuery restore,
            ISnapshotEligibilityRegistry snapshotEligibility,
            ISessionMutationGate mutationGate,
            ISessionEvents sessionEvents,
            DeterministicActiveSessionIndex activeSessions)
        {
            if (activeSessions == null) throw new ArgumentNullException(nameof(activeSessions));
            _activeSessions = activeSessions;
            _inner = new PlayerSessionSystem(authority, saveBinding, restore, snapshotEligibility, mutationGate, sessionEvents);
        }

        public PlayerSessionSystem Inner => _inner;

        public SessionActivationResult ActivateSession(SessionId sessionId, PlayerId serverResolvedPlayerId, ClientJoinRequest? clientRequest = null)
        {
            var result = _inner.ActivateSession(sessionId, serverResolvedPlayerId, clientRequest);
            if (result.Ok)
                _activeSessions.TryAdd(result.SessionId);

            return result;
        }

        public SessionDeactivationResult DeactivateSession(SessionId sessionId)
        {
            var result = _inner.DeactivateSession(sessionId);
            if (result.Ok && result.WasRemoved)
                _activeSessions.TryRemove(sessionId);

            return result;
        }

        public SessionActivationResult TryRebindForReconnect(PlayerId serverResolvedPlayerId, SessionId newSessionId, ClientJoinRequest? clientRequest = null)
        {
            var result = _inner.TryRebindForReconnect(serverResolvedPlayerId, newSessionId, clientRequest);
            if (result.Ok)
                _activeSessions.TryAdd(result.SessionId);

            return result;
        }

        public bool TryGetPlayerForSession(SessionId sessionId, out PlayerId playerId)
            => _inner.TryGetPlayerForSession(sessionId, out playerId);

        public bool TryGetSessionForPlayer(PlayerId playerId, out SessionId sessionId)
            => _inner.TryGetSessionForPlayer(playerId, out sessionId);

        public bool IsSessionActive(SessionId sessionId)
            => _inner.IsSessionActive(sessionId);
    }
}
