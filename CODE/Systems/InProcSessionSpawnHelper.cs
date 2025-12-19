using System;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Sessions;

namespace Caelmor.Runtime.Integration
{
    /// <summary>
    /// In-process helper that enqueues session activation through the handshake pipeline.
    /// </summary>
    public sealed class InProcSessionSpawnHelper
    {
        private readonly SessionHandshakePipeline _handshakes;
        private readonly IPlayerSessionSystem _sessions;

        public InProcSessionSpawnHelper(SessionHandshakePipeline handshakes, IPlayerSessionSystem sessions)
        {
            _handshakes = handshakes ?? throw new ArgumentNullException(nameof(handshakes));
            _sessions = sessions ?? throw new ArgumentNullException(nameof(sessions));
        }

        public bool TryEnqueueSpawn(PlayerId playerId, out SessionId sessionId)
        {
            var result = _handshakes.TryEnqueue(playerId);
            sessionId = result.SessionId;
            return result.Ok;
        }

        public bool IsSessionActive(SessionId sessionId)
        {
            return _sessions.IsSessionActive(sessionId);
        }
    }
}
