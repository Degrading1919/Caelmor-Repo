using System;
using System.Buffers;
using System.Collections.Generic;
using System.Text;
using System.Threading;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.InterestManagement;
using Caelmor.Runtime.Persistence;
using Caelmor.Runtime.Replication;
using Caelmor.Runtime.Sessions;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.WorldSimulation;

namespace Caelmor.Runtime.Integration
{
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

        /// <summary>
        /// Drops all buffered commands for a session (disconnect/unload).
        /// </summary>
        public bool DropSession(SessionId sessionId)
        {
            return _perSession.Remove(sessionId);
        }

        /// <summary>
        /// Clears all session buffers. Invoked during server shutdown to avoid retention leaks.
        /// </summary>
        public void Clear()
        {
            _perSession.Clear();
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
        bool DropSession(SessionId sessionId);
        void Clear();
    }

    /// <summary>
    /// Interest management implementation using per-session visibility caches backed by a spatial index.
    /// </summary>
    public sealed class VisibilityCullingService : IReplicationEligibilityGate, IDisposable
    {
        private readonly ZoneSpatialIndex _spatialIndex;
        private readonly ArrayPool<EntityHandle> _entityPool;
        private readonly Dictionary<SessionId, VisibilityBucket> _visibility = new Dictionary<SessionId, VisibilityBucket>(64);
        private readonly List<EntityHandle> _queryBuffer;

        public VisibilityCullingService(ZoneSpatialIndex spatialIndex, ArrayPool<EntityHandle>? entityPool = null, int initialQueryCapacity = 64)
        {
            _spatialIndex = spatialIndex ?? throw new ArgumentNullException(nameof(spatialIndex));
            _entityPool = entityPool ?? ArrayPool<EntityHandle>.Shared;
            _queryBuffer = new List<EntityHandle>(Math.Max(4, initialQueryCapacity));
        }

        /// <summary>
        /// Tracks or moves an entity within the zone spatial index without allocations.
        /// </summary>
        public void Track(EntityHandle entity, ZoneId zone, ZonePosition position)
        {
            _spatialIndex.Upsert(entity, zone, position);
        }

        /// <summary>
        /// Removes an entity from the spatial index. Safe to call when already absent.
        /// </summary>
        public void Remove(EntityHandle entity)
        {
            _spatialIndex.Remove(entity);
        }

        /// <summary>
        /// Rebuilds the deterministic visibility set for a session using the spatial index.
        /// </summary>
        public int RefreshVisibility(SessionId session, ZoneInterestQuery query)
        {
            _queryBuffer.Clear();
            _spatialIndex.Query(query, _queryBuffer);
            _queryBuffer.Sort(EntityHandleComparer.Instance);

            var bucket = _visibility.TryGetValue(session, out var existing)
                ? existing
                : new VisibilityBucket(_entityPool.Rent(_queryBuffer.Count == 0 ? 4 : _queryBuffer.Count));

            bucket.SetSorted(_queryBuffer, _entityPool);
            _visibility[session] = bucket;
            return bucket.Count;
        }

        /// <summary>
        /// Provides nearby entities for AI/target-selection surfaces using the same spatial index.
        /// Results are sorted deterministically by EntityHandle value.
        /// </summary>
        public int QueryNearbyTargets(ZoneInterestQuery query, List<EntityHandle> destination)
        {
            if (destination is null) throw new ArgumentNullException(nameof(destination));

            destination.Clear();
            _spatialIndex.Query(query, destination);
            destination.Sort(EntityHandleComparer.Instance);
            return destination.Count;
        }

        public bool IsEntityReplicationEligible(SessionId sessionId, EntityHandle entity)
        {
            if (!_visibility.TryGetValue(sessionId, out var bucket))
                return false;

            return bucket.Contains(entity);
        }

        /// <summary>
        /// Removes cached visibility for a disconnected session and returns rented buffers.
        /// </summary>
        public void RemoveSession(SessionId sessionId)
        {
            if (!_visibility.TryGetValue(sessionId, out var bucket))
                return;

            bucket.Release(_entityPool);
            _visibility.Remove(sessionId);
        }

        /// <summary>
        /// Drops spatial and visibility state for a zone unload.
        /// </summary>
        public void RemoveZone(ZoneId zone)
        {
            _spatialIndex.RemoveZone(zone);

            var sessionsToDrop = new List<SessionId>();
            foreach (var kvp in _visibility)
            {
                sessionsToDrop.Add(kvp.Key);
            }

            for (int i = 0; i < sessionsToDrop.Count; i++)
                RemoveSession(sessionsToDrop[i]);
        }

        /// <summary>
        /// Clears all cached visibility and spatial index state for shutdown.
        /// </summary>
        public void Clear()
        {
            foreach (var kvp in _visibility)
            {
                kvp.Value.Release(_entityPool);
            }

            _visibility.Clear();
            _spatialIndex.Clear();
        }

        public void Dispose()
        {
            Clear();
        }

        private struct VisibilityBucket
        {
            private EntityHandle[] _entities;
            private int _count;

            public VisibilityBucket(EntityHandle[] rented)
            {
                _entities = rented;
                _count = 0;
            }

            public int Count => _count;

            public void SetSorted(List<EntityHandle> source, ArrayPool<EntityHandle> pool)
            {
                EnsureCapacity(source.Count, pool);

                for (int i = 0; i < source.Count; i++)
                    _entities[i] = source[i];

                _count = source.Count;
            }

            public void Release(ArrayPool<EntityHandle> pool)
            {
                if (_entities != null && _entities.Length > 0)
                    pool.Return(_entities, clearArray: false);

                _entities = Array.Empty<EntityHandle>();
                _count = 0;
            }

            public bool Contains(EntityHandle entity)
            {
                int low = 0;
                int high = _count - 1;

                while (low <= high)
                {
                    var mid = low + ((high - low) >> 1);
                    var current = _entities[mid].Value;
                    var target = entity.Value;

                    if (current == target)
                        return true;

                    if (current < target)
                        low = mid + 1;
                    else
                        high = mid - 1;
                }

                return false;
            }

            private void EnsureCapacity(int required, ArrayPool<EntityHandle> pool)
            {
                if (_entities != null && _entities.Length >= required)
                {
                    return;
                }

                var next = _entities == null || _entities.Length == 0 ? Math.Max(4, required) : _entities.Length;
                while (next < required)
                    next *= 2;

                var rented = pool.Rent(next);
                if (_entities != null && _entities.Length > 0)
                    pool.Return(_entities, clearArray: false);

                _entities = rented;
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

        public ServerRuntimeHost(TickSystem tickSystem, WorldSimulationCore worldSimulation)
        {
            _tickSystem = tickSystem ?? throw new ArgumentNullException(nameof(tickSystem));
            _worldSimulation = worldSimulation ?? throw new ArgumentNullException(nameof(worldSimulation));
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
