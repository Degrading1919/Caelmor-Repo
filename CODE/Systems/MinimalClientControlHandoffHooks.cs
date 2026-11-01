using Caelmor.Runtime.Onboarding;
using System;
using System.Collections.Concurrent;

namespace Caelmor.Runtime.Onboarding
{
    /// <summary>
    /// Minimal server-authoritative handoff service that exposes onboarding completion
    /// and authorizes client control. Pure signal bridge; no gameplay, UI, or input logic.
    /// </summary>
    public sealed class OnboardingHandoffService : IOnboardingHandoffService
    {
        // Server-authoritative onboarding results keyed by session.
        private readonly ConcurrentDictionary<SessionId, OnboardingResult> _results = new();

        private readonly IClientControlChannel _clientChannel;

        public OnboardingHandoffService(IClientControlChannel clientChannel)
        {
            _clientChannel = clientChannel ?? throw new ArgumentNullException(nameof(clientChannel));
        }

        /// <summary>
        /// Records authoritative completion, superseding any earlier failed attempt,
        /// and emits authorization only for the caller that wins that transition.
        /// </summary>
        public void NotifyOnboardingSuccess(IServerSession session)
        {
            if (session is null) throw new ArgumentNullException(nameof(session));
            if (!session.IsServerAuthoritative) return;

            // A rejected duplicate or an earlier failed attempt must not suppress
            // the authoritative completion of the successful attempt. Only the
            // caller that wins the transition emits the authorization signal.
            while (true)
            {
                if (_results.TryGetValue(session.Id, out var result))
                {
                    if (result == OnboardingResult.Success)
                        return;
                    if (!_results.TryUpdate(session.Id, OnboardingResult.Success, result))
                        continue;
                }
                else if (!_results.TryAdd(session.Id, OnboardingResult.Success))
                {
                    continue;
                }

                _clientChannel.AuthorizeClientControl(session.Id);
                return;
            }
        }

        /// <summary>
        /// Records an attempt failure while no successful completion exists.
        /// A rejected duplicate cannot overwrite successful authorization.
        /// </summary>
        public void NotifyOnboardingFailure(IServerSession session)
        {
            if (session is null) throw new ArgumentNullException(nameof(session));
            if (!session.IsServerAuthoritative) return;

            _results.TryAdd(session.Id, OnboardingResult.Failure);
        }

        /// <summary>
        /// Server-side query for onboarding completion state.
        /// Returns false if onboarding has not succeeded.
        /// </summary>
        public bool IsClientAuthorized(SessionId sessionId)
        {
            return _results.TryGetValue(sessionId, out var result)
                   && result == OnboardingResult.Success;
        }
    }

    /// <summary>
    /// Minimal contract for server-to-client control authorization signaling.
    /// Transport and replication are intentionally abstracted.
    /// </summary>
    public interface IClientControlChannel
    {
        /// <summary>
        /// Emits an authoritative signal enabling client control for the session.
        /// Must be safe to call multiple times.
        /// </summary>
        void AuthorizeClientControl(SessionId sessionId);
    }

    /// <summary>
    /// Minimal onboarding handoff surface used by onboarding runtime.
    /// </summary>
    public interface IOnboardingHandoffService
    {
        void NotifyOnboardingSuccess(IServerSession session);
        void NotifyOnboardingFailure(IServerSession session);
        bool IsClientAuthorized(SessionId sessionId);
    }

    /// <summary>
    /// Onboarding completion state.
    /// </summary>
    public enum OnboardingResult
    {
        Failure = 0,
        Success = 1
    }

}
