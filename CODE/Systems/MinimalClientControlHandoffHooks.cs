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
        /// Records a successful onboarding completion and emits a client-consumable
        /// authorization signal. Idempotent.
        /// </summary>
        public void NotifyOnboardingSuccess(IServerSession session)
        {
            if (session is null) throw new ArgumentNullException(nameof(session));
            if (!session.IsServerAuthoritative) return;

            var result = _results.GetOrAdd(session.Id, OnboardingResult.Success);

            if (result == OnboardingResult.Success)
            {
                // Idempotent: repeated calls re-emit the same authorization safely.
                _clientChannel.AuthorizeClientControl(session.Id);
            }
        }

        /// <summary>
        /// Records an onboarding failure. Client control remains disabled.
        /// Idempotent.
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

    /// <summary>
    /// Minimal server session abstraction.
    /// </summary>
    public interface IServerSession
    {
        SessionId Id { get; }
        bool IsServerAuthoritative { get; }
    }

    /// <summary>
    /// Opaque server-issued session identifier.
    /// </summary>
    public readonly struct SessionId : IEquatable<SessionId>
    {
        public readonly Guid Value;

        public SessionId(Guid value)
        {
            Value = value;
        }

        public bool Equals(SessionId other) => Value.Equals(other.Value);
        public override bool Equals(object obj) => obj is SessionId other && Equals(other);
        public override int GetHashCode() => Value.GetHashCode();
        public override string ToString() => Value.ToString();
    }
}
