using System;
using System.Buffers;
using System.Collections.Generic;
using System.Text;
using System.Threading;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Persistence;
using Caelmor.Runtime.Replication;
using Caelmor.Runtime.Sessions;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.WorldSimulation;

namespace Caelmor.Runtime.Integration
{
    /// <summary>
    /// Allocation-free transport router and message dispatcher.
    /// Frames are stored in a fixed ring buffer; payload byte arrays are rented
    /// from ArrayPool and must be returned by the consumer via ReturnPayload.
    /// </summary>
    public sealed class PooledTransportRouter : ITransportRouter
    {
        private readonly TransportFrame[] _outgoing;
        private readonly ArrayPool<byte> _payloadPool;
        private int _head;
        private int _tail;

#if DEBUG
        private long _framesEnqueued;
        private long _framesDequeued;
        private long _bytesRented;
        private long _bytesReturned;
        private int _maxQueueDepth;
#endif

        public PooledTransportRouter(int capacity, ArrayPool<byte>? payloadPool = null)
        {
            if (capacity <= 0) throw new ArgumentOutOfRangeException(nameof(capacity));

            _outgoing = new TransportFrame[capacity];
            _payloadPool = payloadPool ?? ArrayPool<byte>.Shared;
        }

        public bool EnqueueOutgoing(SessionId sessionId, int messageType, ReadOnlySpan<byte> payload)
        {
            var nextTail = (_tail + 1) % _outgoing.Length;
            if (nextTail == _head)
                return false; // full

            byte[] payloadBuffer;
            if (payload.Length == 0)
            {
                payloadBuffer = Array.Empty<byte>();
            }
            else
            {
                payloadBuffer = _payloadPool.Rent(payload.Length);
                payload.CopyTo(new Span<byte>(payloadBuffer, 0, payload.Length));
#if DEBUG
                Interlocked.Add(ref _bytesRented, payload.Length);
#endif
            }

            _outgoing[_tail] = new TransportFrame(sessionId, messageType, payloadBuffer, payload.Length);
            _tail = nextTail;

#if DEBUG
            var depth = (_tail - _head + _outgoing.Length) % _outgoing.Length;
            if (depth > _maxQueueDepth)
                _maxQueueDepth = depth;
            Interlocked.Increment(ref _framesEnqueued);
#endif

            return true;
        }

        public bool TryDequeueOutgoing(out TransportFrame frame)
        {
            if (_head == _tail)
            {
                frame = default;
                return false;
            }

            frame = _outgoing[_head];
            _outgoing[_head] = default;
            _head = (_head + 1) % _outgoing.Length;

#if DEBUG
            Interlocked.Increment(ref _framesDequeued);
#endif
            return true;
        }

        public void ReturnPayload(in TransportFrame frame)
        {
            if (frame.Payload is null || frame.Payload.Length == 0)
                return;

            _payloadPool.Return(frame.Payload, clearArray: false);

#if DEBUG
            Interlocked.Add(ref _bytesReturned, frame.PayloadLength);
#endif
        }
    }

    public readonly struct TransportFrame
    {
        public readonly SessionId SessionId;
        public readonly int MessageType;
        public readonly byte[] Payload;
        public readonly int PayloadLength;

        public TransportFrame(SessionId sessionId, int messageType, byte[] payload, int payloadLength)
        {
            SessionId = sessionId;
            MessageType = messageType;
            Payload = payload;
            PayloadLength = payloadLength;
        }
    }

    public interface ITransportRouter
    {
        bool EnqueueOutgoing(SessionId sessionId, int messageType, ReadOnlySpan<byte> payload);
        bool TryDequeueOutgoing(out TransportFrame frame);
        void ReturnPayload(in TransportFrame frame);
    }

    /// <summary>
    /// Connection/session handshake ring-buffer. Avoids per-request allocations.
    /// </summary>
    public sealed class SessionHandshakePipeline
    {
        private readonly HandshakeRequest[] _requests;
        private readonly IPlayerSessionSystem _sessions;
        private readonly IOnboardingHandoffService _handoff;
        private int _head;
        private int _tail;

#if DEBUG
        private int _maxQueueDepth;
#endif

        public SessionHandshakePipeline(int capacity, IPlayerSessionSystem sessions, IOnboardingHandoffService handoff)
        {
            if (capacity <= 0) throw new ArgumentOutOfRangeException(nameof(capacity));
            _sessions = sessions ?? throw new ArgumentNullException(nameof(sessions));
            _handoff = handoff ?? throw new ArgumentNullException(nameof(handoff));
            _requests = new HandshakeRequest[capacity];
        }

        public bool TrySubmit(in HandshakeRequest request)
        {
            var nextTail = (_tail + 1) % _requests.Length;
            if (nextTail == _head)
                return false;

            _requests[_tail] = request;
            _tail = nextTail;

#if DEBUG
            var depth = (_tail - _head + _requests.Length) % _requests.Length;
            if (depth > _maxQueueDepth)
                _maxQueueDepth = depth;
#endif
            return true;
        }

        public bool TryProcessNext(Func<HandshakeRequest, SessionActivationResult> activation)
        {
            if (_head == _tail)
                return false;

            ref var request = ref _requests[_head];
            var result = activation != null
                ? activation(request)
                : _sessions.ActivateSession(request.SessionId, request.PlayerId);

            if (result.Ok)
            {
                _handoff.NotifyOnboardingSuccess(new HandshakeSessionAdapter(result.SessionId));
            }
            else
            {
                _handoff.NotifyOnboardingFailure(new HandshakeSessionAdapter(request.SessionId));
            }

            _requests[_head] = default;
            _head = (_head + 1) % _requests.Length;
            return true;
        }
    }

    public readonly struct HandshakeRequest
    {
        public readonly SessionId SessionId;
        public readonly PlayerId PlayerId;

        public HandshakeRequest(SessionId sessionId, PlayerId playerId)
        {
            SessionId = sessionId;
            PlayerId = playerId;
        }
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

    /// <summary>
    /// Authoritative input ingestion with fixed per-session command rings.
    /// </summary>
    public sealed class AuthoritativeCommandIngestor : IAuthoritativeCommandIngestor
    {
        private readonly Dictionary<SessionId, CommandRing> _perSession = new Dictionary<SessionId, CommandRing>(64);

#if DEBUG
        private int _maxCommandsPerSession;
#endif

        public bool TryEnqueue(SessionId sessionId, in AuthoritativeCommand command)
        {
            if (!_perSession.TryGetValue(sessionId, out var ring))
            {
                ring = new CommandRing(32);
            }

            var success = ring.TryPush(command);
            _perSession[sessionId] = ring;

#if DEBUG
            if (ring.Count > _maxCommandsPerSession)
                _maxCommandsPerSession = ring.Count;
#endif

            return success;
        }

        public int TryDrain(SessionId sessionId, Span<AuthoritativeCommand> destination)
        {
            if (!_perSession.TryGetValue(sessionId, out var ring) || ring.Count == 0)
                return 0;

            var drained = ring.TryPopAll(destination);
            _perSession[sessionId] = ring;
            return drained;
        }

        private struct CommandRing
        {
            private AuthoritativeCommand[] _commands;
            private int _head;
            private int _tail;

            public int Count { get; private set; }

            public CommandRing(int capacity)
            {
                _commands = new AuthoritativeCommand[capacity];
                _head = 0;
                _tail = 0;
                Count = 0;
            }

            public bool TryPush(in AuthoritativeCommand command)
            {
                var nextTail = (_tail + 1) % _commands.Length;
                if (nextTail == _head)
                    return false;

                _commands[_tail] = command;
                _tail = nextTail;
                Count++;
                return true;
            }

            public int TryPopAll(Span<AuthoritativeCommand> destination)
            {
                var written = 0;
                while (_head != _tail && written < destination.Length)
                {
                    destination[written] = _commands[_head];
                    _commands[_head] = default;
                    _head = (_head + 1) % _commands.Length;
                    written++;
                    Count--;
                }
                return written;
            }
        }
    }

    public readonly struct AuthoritativeCommand
    {
        public readonly long AuthoritativeTick;
        public readonly int CommandType;
        public readonly int PayloadA;
        public readonly int PayloadB;

        public AuthoritativeCommand(long authoritativeTick, int commandType, int payloadA, int payloadB)
        {
            AuthoritativeTick = authoritativeTick;
            CommandType = commandType;
            PayloadA = payloadA;
            PayloadB = payloadB;
        }
    }

    public interface IAuthoritativeCommandIngestor
    {
        bool TryEnqueue(SessionId sessionId, in AuthoritativeCommand command);
        int TryDrain(SessionId sessionId, Span<AuthoritativeCommand> destination);
    }

    /// <summary>
    /// Interest management implementation using per-session visibility caches.
    /// </summary>
    public sealed class VisibilityCullingService : IReplicationEligibilityGate
    {
        private readonly Dictionary<SessionId, VisibilityBucket> _visibility = new Dictionary<SessionId, VisibilityBucket>(64);

        public void SetVisibleEntities(SessionId session, EntityHandle[] entities, int count)
        {
            if (!_visibility.TryGetValue(session, out var bucket))
            {
                bucket = new VisibilityBucket(entities.Length);
            }

            bucket.Set(entities, count);
            _visibility[session] = bucket;
        }

        public bool IsEntityReplicationEligible(SessionId sessionId, EntityHandle entity)
        {
            if (!_visibility.TryGetValue(sessionId, out var bucket))
                return false;

            return bucket.Contains(entity);
        }

        private struct VisibilityBucket
        {
            private EntityHandle[] _entities;
            private int _count;

            public VisibilityBucket(int capacity)
            {
                _entities = new EntityHandle[capacity];
                _count = 0;
            }

            public void Set(EntityHandle[] source, int count)
            {
                EnsureCapacity(count);
                Array.Copy(source, _entities, count);
                _count = count;
            }

            public bool Contains(EntityHandle entity)
            {
                for (int i = 0; i < _count; i++)
                {
                    if (_entities[i].Equals(entity))
                        return true;
                }

                return false;
            }

            private void EnsureCapacity(int required)
            {
                if (_entities.Length >= required)
                    return;

                var next = _entities.Length == 0 ? required : _entities.Length;
                while (next < required)
                    next *= 2;
                Array.Resize(ref _entities, next);
            }
        }
    }

    /// <summary>
    /// Snapshot serializer using pooled byte buffers. Ownership of the rented buffer
    /// stays with the returned payload and must be disposed by the transport.
    /// </summary>
    public sealed class SnapshotSerializer
    {
        private readonly ArrayPool<byte> _pool;

        private long _bytesRented;
        private long _bytesReturned;

        public SnapshotSerializer(ArrayPool<byte>? pool = null)
        {
            _pool = pool ?? ArrayPool<byte>.Shared;
        }

        public PooledTransportPayload Serialize(in ClientReplicationSnapshot snapshot)
        {
            var estimated = 32 + snapshot.EntityCount * 32;
            var buffer = _pool.Rent(estimated);
            var span = buffer.AsSpan();
            var offset = 0;

            WriteInt64(snapshot.AuthoritativeTick, span, ref offset);
            WriteGuid(snapshot.SessionId.Value, span, ref offset);

            WriteInt32(snapshot.EntityCount, span, ref offset);
            var entities = snapshot.EntitiesSpan;
            for (int i = 0; i < snapshot.EntityCount; i++)
            {
                WriteInt32(entities[i].Entity.Value, span, ref offset);
                EnsureCapacity(ref buffer, ref span, offset, entities[i].State.Fingerprint.Length * 4 + offset + 1);
                offset += Encoding.UTF8.GetBytes(entities[i].State.Fingerprint.AsSpan(), span.Slice(offset));
                span[offset++] = 0; // delimiter
            }

            Interlocked.Add(ref _bytesRented, buffer.Length);

            return new PooledTransportPayload(buffer, offset, _pool, OnPayloadReturned);
        }

        private static void WriteInt32(int value, Span<byte> destination, ref int offset)
        {
            System.Buffers.Binary.BinaryPrimitives.WriteInt32LittleEndian(destination.Slice(offset, sizeof(int)), value);
            offset += sizeof(int);
        }

        private static void WriteInt64(long value, Span<byte> destination, ref int offset)
        {
            System.Buffers.Binary.BinaryPrimitives.WriteInt64LittleEndian(destination.Slice(offset, sizeof(long)), value);
            offset += sizeof(long);
        }

        private static void WriteGuid(Guid value, Span<byte> destination, ref int offset)
        {
            Span<byte> guidBytes = stackalloc byte[16];
            value.TryWriteBytes(guidBytes);
            guidBytes.CopyTo(destination.Slice(offset, guidBytes.Length));
            offset += guidBytes.Length;
        }

        private void EnsureCapacity(ref byte[] buffer, ref Span<byte> span, int used, int required)
        {
            if (required <= buffer.Length)
                return;

            var newBuffer = _pool.Rent(required);
            new Span<byte>(buffer, 0, used).CopyTo(newBuffer);
            _pool.Return(buffer, clearArray: false);
            Interlocked.Add(ref _bytesReturned, buffer.Length);
            Interlocked.Add(ref _bytesRented, newBuffer.Length);
            buffer = newBuffer;
            span = buffer.AsSpan();
        }

        private void OnPayloadReturned(int length)
        {
            Interlocked.Add(ref _bytesReturned, length);
        }
    }

    public readonly struct PooledTransportPayload : IDisposable
    {
        public readonly byte[] Buffer;
        public readonly int Length;
        private readonly ArrayPool<byte> _pool;
        private readonly Action<int> _onReturn;

        public PooledTransportPayload(byte[] buffer, int length, ArrayPool<byte> pool, Action<int> onReturn)
        {
            Buffer = buffer;
            Length = length;
            _pool = pool ?? ArrayPool<byte>.Shared;
            _onReturn = onReturn ?? (_ => { });
        }

        public void Dispose()
        {
            if (Buffer != null && Buffer.Length > 0)
            {
                _pool.Return(Buffer, clearArray: false);
                _onReturn(Length);
            }
        }
    }

    /// <summary>
    /// Persistence I/O hook using a fixed request buffer. Actual I/O must run off-thread.
    /// </summary>
    public sealed class PersistenceIoQueue
    {
        private readonly PersistenceRequest[] _requests;
        private int _head;
        private int _tail;

        public PersistenceIoQueue(int capacity)
        {
            if (capacity <= 0) throw new ArgumentOutOfRangeException(nameof(capacity));
            _requests = new PersistenceRequest[capacity];
        }

        public bool TryEnqueue(PersistenceRequest request)
        {
            var nextTail = (_tail + 1) % _requests.Length;
            if (nextTail == _head)
                return false;

            _requests[_tail] = request;
            _tail = nextTail;
            return true;
        }

        public bool TryDequeue(out PersistenceRequest request)
        {
            if (_head == _tail)
            {
                request = default;
                return false;
            }

            request = _requests[_head];
            _requests[_head] = default;
            _head = (_head + 1) % _requests.Length;
            return true;
        }
    }

    public readonly struct PersistenceRequest
    {
        public readonly SaveId SaveId;
        public readonly int Operation;

        public PersistenceRequest(SaveId saveId, int operation)
        {
            SaveId = saveId;
            Operation = operation;
        }
    }

    /// <summary>
    /// Lightweight diagnostics accumulator (thread-safe via Interlocked) without allocations in hot paths.
    /// </summary>
    public sealed class ServerDiagnostics
    {
        private long _errors;
        private long _warnings;
        private long _invariants;

        public void RegisterError() => Interlocked.Increment(ref _errors);
        public void RegisterWarning() => Interlocked.Increment(ref _warnings);
        public void RegisterInvariantViolation() => Interlocked.Increment(ref _invariants);

        public (long errors, long warnings, long invariants) Snapshot()
        {
            return (
                Interlocked.Read(ref _errors),
                Interlocked.Read(ref _warnings),
                Interlocked.Read(ref _invariants));
        }
    }

    /// <summary>
    /// Runtime host entrypoint that wires the tick and world simulation cores without blocking the tick thread.
    /// </summary>
    public sealed class ServerRuntimeHost : IDisposable
    {
        private readonly TickSystem _tickSystem;
        private readonly WorldSimulationCore _worldSimulation;
        private readonly ITransportRouter _transport;

        public ServerRuntimeHost(TickSystem tickSystem, WorldSimulationCore worldSimulation, ITransportRouter transport)
        {
            _tickSystem = tickSystem ?? throw new ArgumentNullException(nameof(tickSystem));
            _worldSimulation = worldSimulation ?? throw new ArgumentNullException(nameof(worldSimulation));
            _transport = transport ?? throw new ArgumentNullException(nameof(transport));
        }

        public void Start()
        {
            _worldSimulation.Start();
            _tickSystem.Start();
        }

        public void Stop()
        {
            _tickSystem.Stop();
            _worldSimulation.Stop();
        }

        public void Dispose()
        {
            Stop();
        }
    }
}
