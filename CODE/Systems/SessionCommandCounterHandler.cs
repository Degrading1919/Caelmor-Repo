using System;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Integration;
using Caelmor.Runtime.WorldSimulation;

namespace Caelmor.Runtime.Sessions
{
    /// <summary>
    /// Minimal authoritative command handler that mutates per-session command counters.
    /// Proof-of-life only; no gameplay logic.
    /// </summary>
    public sealed class SessionCommandCounterHandler : IAuthoritativeCommandHandler
    {
        private readonly PlayerSessionSystem _sessions;
        private long _mutationsObserved;

        public SessionCommandCounterHandler(PlayerSessionSystem sessions)
        {
            _sessions = sessions ?? throw new ArgumentNullException(nameof(sessions));
        }

        public long MutationsObserved => _mutationsObserved;

        public void Handle(in AuthoritativeCommand command, SessionId sessionId, SimulationTickContext context)
        {
            TickThreadAssert.AssertTickThread();

            if (_sessions.TryRecordCommandHandled(sessionId, command.DeterministicSequence))
                _mutationsObserved++;
        }
    }
}
