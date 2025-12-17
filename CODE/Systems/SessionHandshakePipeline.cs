using System;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Persistence;
using Caelmor.Runtime.Sessions;

namespace Caelmor.Runtime.Integration
{
    /// <summary>
    /// Bounded handshake pipeline that stages connection activation for processing on the tick thread.
    /// Ensures session activation and onboarding notifications run in a deterministic order without
    /// mutating gameplay state off-thread.
    /// </summary>
    public sealed class SessionHandshakePipeline
    {
        private readonly HandshakeWorkItem[] _requests;
        private readonly HandshakeWorkItem[] _scratch;
        private readonly object _gate = new object();

        private readonly IPlayerSessionSystem _sessions;
        private readonly IOnboardingHandoffService _handoff;

        private int _head;
        private int _tail;

        public SessionHandshakePipeline(int capacity, IPlayerSessionSystem sessions, IOnboardingHandoffService handoff)
        {
            if (capacity <= 0) throw new ArgumentOutOfRangeException(nameof(capacity));
            _sessions = sessions ?? throw new ArgumentNullException(nameof(sessions));
            _handoff = handoff ?? throw new ArgumentNullException(nameof(handoff));
            _requests = new HandshakeWorkItem[capacity];
            _scratch = new HandshakeWorkItem[capacity];
        }

        public HandshakeEnqueueResult TryEnqueue(PlayerId playerId, ClientJoinRequest? clientRequest = null, SessionId sessionId = default)
        {
            if (!playerId.IsValid)
                return HandshakeEnqueueResult.Rejected(HandshakeRejectionReason.InvalidPlayerId);

            var resolvedSessionId = sessionId.IsValid ? sessionId : new SessionId(Guid.NewGuid());

            lock (_gate)
            {
                var nextTail = (_tail + 1) % _requests.Length;
                if (nextTail == _head)
                    return HandshakeEnqueueResult.Rejected(HandshakeRejectionReason.QueueFull);

                _requests[_tail] = new HandshakeWorkItem(resolvedSessionId, playerId, clientRequest);
                _tail = nextTail;
                return HandshakeEnqueueResult.Accepted(resolvedSessionId);
            }
        }

        public bool TryProcessNext(out SessionActivationResult activationResult)
        {
            activationResult = default;
            HandshakeWorkItem request;

            lock (_gate)
            {
                if (_head == _tail)
                    return false;

                request = _requests[_head];
                _requests[_head] = default;
                _head = (_head + 1) % _requests.Length;
            }

            if (!request.PlayerId.IsValid)
            {
                activationResult = SessionActivationResult.Failed(SessionActivationFailureReason.InvalidPlayerId);
                _handoff.NotifyOnboardingFailure(new HandshakeSessionAdapter(request.SessionId));
                return true;
            }

            activationResult = _sessions.ActivateSession(request.SessionId, request.PlayerId, request.ClientRequest);
            if (activationResult.Ok)
            {
                _handoff.NotifyOnboardingSuccess(new HandshakeSessionAdapter(activationResult.SessionId));
            }
            else
            {
                _handoff.NotifyOnboardingFailure(new HandshakeSessionAdapter(request.SessionId));
            }

            return true;
        }

        public void Drop(SessionId sessionId)
        {
            lock (_gate)
            {
                if (_head == _tail)
                    return;

                int write = 0;
                int count = (_tail - _head + _requests.Length) % _requests.Length;
                int readIndex = _head;

                for (int i = 0; i < count; i++)
                {
                    var item = _requests[readIndex];
                    _requests[readIndex] = default;

                    if (!item.SessionId.Equals(sessionId))
                    {
                        _scratch[write++] = item;
                    }

                    readIndex = (readIndex + 1) % _requests.Length;
                }

                _head = 0;
                _tail = write;

                for (int i = 0; i < write; i++)
                {
                    _requests[i] = _scratch[i];
                    _scratch[i] = default;
                }
            }
        }

        public void Reset()
        {
            lock (_gate)
            {
                while (_head != _tail)
                {
                    _requests[_head] = default;
                    _head = (_head + 1) % _requests.Length;
                }

                _head = 0;
                _tail = 0;
            }
        }

        private readonly struct HandshakeWorkItem
        {
            public readonly SessionId SessionId;
            public readonly PlayerId PlayerId;
            public readonly ClientJoinRequest? ClientRequest;

            public HandshakeWorkItem(SessionId sessionId, PlayerId playerId, ClientJoinRequest? clientRequest)
            {
                SessionId = sessionId;
                PlayerId = playerId;
                ClientRequest = clientRequest;
            }
        }
    }

    public readonly struct HandshakeEnqueueResult
    {
        private HandshakeEnqueueResult(bool ok, SessionId sessionId, HandshakeRejectionReason reason)
        {
            Ok = ok;
            SessionId = sessionId;
            RejectionReason = reason;
        }

        public bool Ok { get; }
        public SessionId SessionId { get; }
        public HandshakeRejectionReason RejectionReason { get; }

        public static HandshakeEnqueueResult Accepted(SessionId sessionId)
            => new HandshakeEnqueueResult(true, sessionId, HandshakeRejectionReason.None);

        public static HandshakeEnqueueResult Rejected(HandshakeRejectionReason reason)
            => new HandshakeEnqueueResult(false, default, reason);
    }

    public enum HandshakeRejectionReason
    {
        None = 0,
        InvalidPlayerId = 1,
        QueueFull = 2
    }

    /// <summary>Lightweight IServerSession adapter to avoid allocations.</summary>
    internal readonly struct HandshakeSessionAdapter : IServerSession
    {
        public SessionId Id { get; }
        public bool IsServerAuthoritative => true;

        public HandshakeSessionAdapter(SessionId id)
        {
            Id = id;
        }
    }
}
