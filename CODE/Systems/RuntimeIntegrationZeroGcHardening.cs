using System;
using System.Buffers;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Threading;
using System.Buffers.Binary;
using Caelmor.Runtime;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.InterestManagement;
using Caelmor.Runtime.Persistence;
using Caelmor.Runtime.Replication;
using Caelmor.Runtime.Sessions;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.WorldSimulation;
using Caelmor.Runtime.Transport;

namespace Caelmor.Runtime.Integration
{
    /// <summary>
    /// Authoritative input ingestion with fixed per-session command rings.
    /// - Transport thread enqueues only.
    /// - Tick thread freezes deterministically at the start of each authoritative tick.
    /// - No per-tick allocations after warm-up; arrays are rented once per session and reused.
    /// </summary>
    public sealed class AuthoritativeCommandIngestor : IAuthoritativeCommandIngestor
    {
        private readonly RuntimeBackpressureConfig _config;
        private readonly ArrayPool<AuthoritativeCommand> _commandPool;
        private readonly Dictionary<SessionId, SessionCommandState> _perSession;
        private readonly Dictionary<SessionId, SessionCommandMetrics> _metrics;
        private readonly object _gate = new object();

        private SessionId[] _sessionKeySnapshot = Array.Empty<SessionId>();
        private SessionCommandMetricsSnapshot[] _metricsBuffer = Array.Empty<SessionCommandMetricsSnapshot>();
        private long _commandRingGrows;
        private long _prewarmCompleted;
        private long _dropPathInvocations;
#if DEBUG
        private int _maxCommandsPerSession;
#endif

        public AuthoritativeCommandIngestor(RuntimeBackpressureConfig? config = null, ArrayPool<AuthoritativeCommand>? commandPool = null)
        {
            _config = config ?? RuntimeBackpressureConfig.Default;
            _commandPool = commandPool ?? ArrayPool<AuthoritativeCommand>.Shared;
            _perSession = new Dictionary<SessionId, SessionCommandState>(Math.Max(1, _config.ExpectedMaxSessions));
            _metrics = new Dictionary<SessionId, SessionCommandMetrics>(Math.Max(1, _config.ExpectedMaxSessions));
        }

        public bool TryEnqueue(SessionId sessionId, in AuthoritativeCommand command)
        {
            if (!sessionId.IsValid)
                return false;

            lock (_gate)
            {
                if (!_perSession.TryGetValue(sessionId, out var state))
                {
                    state = SessionCommandState.Create(_config.MaxInboundCommandsPerSession, _commandPool);
                    _commandRingGrows++;
                }

                if (command.AuthoritativeTick < state.LastFrozenTick)
                {
                    state.Metrics.DroppedStale++;
                    _dropPathInvocations++;
                    _perSession[sessionId] = state;
                    _metrics[sessionId] = state.Metrics;
                    return false;
                }

                // Deterministic overflow policy: reject the newest command when the ring is full.
                var success = state.Ring.TryPush(command);

                if (!success)
                {
                    state.Metrics.DroppedOverflow++;
                    _dropPathInvocations++;
                    _perSession[sessionId] = state;
                    _metrics[sessionId] = state.Metrics;
                    return false;
                }

                state.Metrics.Accepted++;
                state.Metrics.PeakBuffered = Math.Max(state.Metrics.PeakBuffered, state.Ring.Count);
                _perSession[sessionId] = state;
                _metrics[sessionId] = state.Metrics;

#if DEBUG
                if (state.Ring.Count > _maxCommandsPerSession)
                    _maxCommandsPerSession = state.Ring.Count;
#endif

                return true;
            }
        }

        public void FreezeAllSessions(long authoritativeTick)
        {
            lock (_gate)
            {
                int count = _perSession.Count;
                EnsureCapacity(ref _sessionKeySnapshot, count);

                int index = 0;
                foreach (var kvp in _perSession)
                    _sessionKeySnapshot[index++] = kvp.Key;

                Array.Sort(_sessionKeySnapshot, 0, index, Caelmor.Runtime.Transport.SessionIdValueComparer.Instance);

                for (int i = 0; i < index; i++)
                    FreezeSessionLocked(_sessionKeySnapshot[i], authoritativeTick);
            }
        }

        public void FreezeSessions(long authoritativeTick, IReadOnlyList<SessionId> activeSessions)
        {
            if (activeSessions is null) throw new ArgumentNullException(nameof(activeSessions));

            lock (_gate)
            {
                EnsureCapacity(ref _sessionKeySnapshot, activeSessions.Count);

                for (int i = 0; i < activeSessions.Count; i++)
                    _sessionKeySnapshot[i] = activeSessions[i];

                Array.Sort(_sessionKeySnapshot, 0, activeSessions.Count, Caelmor.Runtime.Transport.SessionIdValueComparer.Instance);

                for (int i = 0; i < activeSessions.Count; i++)
                    FreezeSessionLocked(_sessionKeySnapshot[i], authoritativeTick);
            }
        }

        public FrozenCommandBatch GetFrozenBatch(SessionId sessionId)
        {
            lock (_gate)
            {
                if (_perSession.TryGetValue(sessionId, out var state))
                    return state.Frozen;
            }

            return FrozenCommandBatch.Empty(sessionId);
        }

        /// <summary>
        /// Drops all buffered commands for a session (disconnect/unload) and returns pooled buffers.
        /// </summary>
        public bool DropSession(SessionId sessionId)
        {
            lock (_gate)
            {
                if (!_perSession.TryGetValue(sessionId, out var state))
                    return false;

                state.ReturnBuffer(_commandPool);
                _perSession.Remove(sessionId);
                _metrics.Remove(sessionId);
                _dropPathInvocations++;
                return true;
            }
        }

        /// <summary>
        /// Clears all session buffers. Invoked during server shutdown to avoid retention leaks.
        /// </summary>
        public void Clear()
        {
            lock (_gate)
            {
                foreach (var kvp in _perSession)
                    kvp.Value.ReturnBuffer(_commandPool);

                _perSession.Clear();
                _metrics.Clear();
            }
        }

        /// <summary>
        /// Pre-allocates pools and diagnostic buffers. Call once during runtime startup to avoid
        /// allocating in tick-thread hot paths after warm-up.
        /// </summary>
        public void Prewarm()
        {
            lock (_gate)
            {
                if (_prewarmCompleted > 0)
                    return;

                int expectedSessions = Math.Max(1, _config.ExpectedMaxSessions);
                EnsureCapacity(ref _sessionKeySnapshot, expectedSessions);
                EnsureCapacity(ref _metricsBuffer, expectedSessions);

                int ringStride = Math.Max(1, _config.MaxInboundCommandsPerSession) + 1;
                int scratchSize = Math.Max(1, _config.ExpectedMaxCommandsPerSessionPerTick);

                for (int i = 0; i < expectedSessions; i++)
                {
                    var ringBuffer = _commandPool.Rent(ringStride);
                    _commandPool.Return(ringBuffer, clearArray: false);

                    var scratchBuffer = _commandPool.Rent(scratchSize);
                    _commandPool.Return(scratchBuffer, clearArray: false);
                }

                _prewarmCompleted++;
            }
        }

        public CommandIngestorDiagnostics SnapshotMetrics()
        {
            lock (_gate)
            {
                int count = _metrics.Count;
                if (count == 0)
                    return CommandIngestorDiagnostics.Empty;

                EnsureCapacity(ref _sessionKeySnapshot, count);
                EnsureCapacity(ref _metricsBuffer, count);

                int index = 0;
                foreach (var kvp in _metrics)
                    _sessionKeySnapshot[index++] = kvp.Key;

                Array.Sort(_sessionKeySnapshot, 0, index, Caelmor.Runtime.Transport.SessionIdValueComparer.Instance);

                int totalDroppedOverflow = 0;
                int totalDroppedStale = 0;
                int totalAccepted = 0;
                int totalFrozen = 0;
                int maxBuffered = 0;

                for (int i = 0; i < index; i++)
                {
                    var sessionId = _sessionKeySnapshot[i];
                    var metrics = _metrics[sessionId];
                    _metricsBuffer[i] = new SessionCommandMetricsSnapshot(sessionId, metrics);

                    totalDroppedOverflow += metrics.DroppedOverflow;
                    totalDroppedStale += metrics.DroppedStale;
                    totalAccepted += metrics.Accepted;
                    totalFrozen += metrics.LastFrozenCount;
                    if (metrics.PeakBuffered > maxBuffered)
                        maxBuffered = metrics.PeakBuffered;
                }

                var totals = new CommandIngestorTotals(
                    totalAccepted,
                    totalDroppedOverflow,
                    totalDroppedStale,
                    totalFrozen,
                    maxBuffered,
                    _commandRingGrows,
                    _prewarmCompleted,
                    _dropPathInvocations);
                return new CommandIngestorDiagnostics(_metricsBuffer, index, totals);
            }
        }

        private void FreezeSessionLocked(SessionId sessionId, long authoritativeTick)
        {
            if (!_perSession.TryGetValue(sessionId, out var state))
                return;

            state.LastFrozenTick = authoritativeTick;

            if (state.Scratch == null || state.Scratch.Length == 0)
                state.Scratch = _commandPool.Rent(_config.MaxInboundCommandsPerSession);

            var destination = state.Scratch.AsSpan();
            int drained = state.Ring.TryPopAll(destination);

            if (drained > 1)
                Array.Sort(state.Scratch, 0, drained, AuthoritativeCommandComparer.Instance);

            state.Frozen = new FrozenCommandBatch(sessionId, authoritativeTick, state.Scratch, drained);
            state.Metrics.LastFrozenCount = drained;
            _perSession[sessionId] = state;
            _metrics[sessionId] = state.Metrics;
        }

        private static void EnsureCapacity<T>(ref T[] buffer, int required)
        {
            if (buffer.Length >= required)
                return;

            var next = buffer.Length == 0 ? required : buffer.Length;
            while (next < required)
                next <<= 1;
            buffer = new T[next];
        }

        private struct SessionCommandState
        {
            public CommandRing Ring;
            public AuthoritativeCommand[] Scratch;
            public FrozenCommandBatch Frozen;
            public SessionCommandMetrics Metrics;
            public long LastFrozenTick;

            public static SessionCommandState Create(int capacity, ArrayPool<AuthoritativeCommand> pool)
            {
                var buffer = pool.Rent(Math.Max(1, capacity));
                return new SessionCommandState
                {
                    Ring = new CommandRing(capacity, pool),
                    Scratch = buffer,
                    Frozen = FrozenCommandBatch.Empty(default),
                    Metrics = default,
                    LastFrozenTick = 0
                };
            }

            public void ReturnBuffer(ArrayPool<AuthoritativeCommand> pool)
            {
                if (Scratch != null && Scratch.Length > 0)
                    pool.Return(Scratch, clearArray: false);

                Scratch = Array.Empty<AuthoritativeCommand>();
                Ring.ReturnBuffer(pool);
                Frozen = FrozenCommandBatch.Empty(default);
                Metrics = default;
                LastFrozenTick = 0;
            }
        }

        private struct CommandRing
        {
            private AuthoritativeCommand[] _commands;
            private int _capacity;
            private int _stride;
            private int _head;
            private int _tail;

            public int Count { get; private set; }
            public int Capacity => _capacity;

            public CommandRing(int capacity, ArrayPool<AuthoritativeCommand> pool)
            {
                _capacity = Math.Max(1, capacity);
                _stride = _capacity + 1;
                _commands = pool.Rent(_stride);
                _head = 0;
                _tail = 0;
                Count = 0;
            }

            public bool TryPush(in AuthoritativeCommand command)
            {
                if (_stride <= 0)
                    return false;

                var nextTail = (_tail + 1) % _stride;
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
                    _head = (_head + 1) % _stride;
                    written++;
                    Count--;
                }
                return written;
            }

            public void ReturnBuffer(ArrayPool<AuthoritativeCommand> pool)
            {
                if (_commands != null && _commands.Length > 0)
                    pool.Return(_commands, clearArray: false);

                _commands = Array.Empty<AuthoritativeCommand>();
                _capacity = 0;
                _stride = 0;
                _head = 0;
                _tail = 0;
                Count = 0;
            }
        }
    }

    /// <summary>
    /// Read-only frozen batch for a session within a single authoritative tick.
    /// Backed by a pooled buffer owned by the ingestor; callers must not mutate or retain past the tick.
    /// </summary>
    public readonly struct FrozenCommandBatch
    {
        public readonly SessionId SessionId;
        public readonly long AuthoritativeTick;
        public readonly AuthoritativeCommand[] Buffer;
        public readonly int Count;

        public FrozenCommandBatch(SessionId sessionId, long authoritativeTick, AuthoritativeCommand[] buffer, int count)
        {
            SessionId = sessionId;
            AuthoritativeTick = authoritativeTick;
            Buffer = buffer ?? Array.Empty<AuthoritativeCommand>();
            Count = Math.Max(0, count);
        }

        public static FrozenCommandBatch Empty(SessionId sessionId) => new FrozenCommandBatch(sessionId, authoritativeTick: 0, Array.Empty<AuthoritativeCommand>(), count: 0);

        public ReadOnlySpan<AuthoritativeCommand> AsSpan()
        {
            return Buffer.AsSpan(0, Count);
        }
    }

    public readonly struct AuthoritativeCommand
    {
        public readonly long AuthoritativeTick;
        public readonly int CommandType;
        public readonly int PayloadA;
        public readonly int PayloadB;
        public readonly long DeterministicSequence;

        public AuthoritativeCommand(long authoritativeTick, int commandType, int payloadA, int payloadB, long deterministicSequence = 0)
        {
            AuthoritativeTick = authoritativeTick;
            CommandType = commandType;
            PayloadA = payloadA;
            PayloadB = payloadB;
            DeterministicSequence = deterministicSequence;
        }

        public AuthoritativeCommand WithSequence(long sequence)
        {
            return new AuthoritativeCommand(AuthoritativeTick, CommandType, PayloadA, PayloadB, sequence);
        }
    }

    public sealed class AuthoritativeCommandComparer : IComparer<AuthoritativeCommand>
    {
        public static readonly AuthoritativeCommandComparer Instance = new AuthoritativeCommandComparer();

        public int Compare(AuthoritativeCommand x, AuthoritativeCommand y)
        {
            var c = x.AuthoritativeTick.CompareTo(y.AuthoritativeTick);
            if (c != 0) return c;

            c = x.DeterministicSequence.CompareTo(y.DeterministicSequence);
            if (c != 0) return c;

            c = x.CommandType.CompareTo(y.CommandType);
            if (c != 0) return c;

            c = x.PayloadA.CompareTo(y.PayloadA);
            if (c != 0) return c;

            return x.PayloadB.CompareTo(y.PayloadB);
        }
    }

    public interface IAuthoritativeCommandIngestor
    {
        bool TryEnqueue(SessionId sessionId, in AuthoritativeCommand command);
        void FreezeAllSessions(long authoritativeTick);
        void FreezeSessions(long authoritativeTick, IReadOnlyList<SessionId> activeSessions);
        FrozenCommandBatch GetFrozenBatch(SessionId sessionId);
        bool DropSession(SessionId sessionId);
        void Clear();
        CommandIngestorDiagnostics SnapshotMetrics();
    }

    /// <summary>
    /// Tick-phase hook that freezes authoritative command ingestion at the start of each authoritative tick.
    /// Thread contract: invoked on the tick thread only. Transport/network threads enqueue only.
    /// </summary>
    public sealed class AuthoritativeCommandFreezeHook : ITickPhaseHook
    {
        private readonly IAuthoritativeCommandIngestor _ingestor;
        private readonly IActiveSessionIndex? _activeSessions;

        public AuthoritativeCommandFreezeHook(IAuthoritativeCommandIngestor ingestor, IActiveSessionIndex? activeSessions = null)
        {
            _ingestor = ingestor ?? throw new ArgumentNullException(nameof(ingestor));
            _activeSessions = activeSessions;
        }

        public void OnPreTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            if (_activeSessions != null)
            {
                _ingestor.FreezeSessions(context.TickIndex, _activeSessions.SnapshotSessionsDeterministic());
            }
            else
            {
                _ingestor.FreezeAllSessions(context.TickIndex);
            }
        }

        public void OnPostTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            // No post-tick work required; freeze occurs at tick start.
        }
    }

    public interface IAuthoritativeCommandHandler
    {
        void Handle(in AuthoritativeCommand command, SessionId sessionId, SimulationTickContext context);
    }

    public interface ICommandHandlerRegistry
    {
        bool TryGetHandler(int commandType, out IAuthoritativeCommandHandler handler);
        int HandlerCount { get; }
    }

    public sealed class CommandHandlerRegistry : ICommandHandlerRegistry
    {
        private readonly Dictionary<int, IAuthoritativeCommandHandler> _handlers = new Dictionary<int, IAuthoritativeCommandHandler>(16);

        public int HandlerCount => _handlers.Count;

        public void Register(int commandType, IAuthoritativeCommandHandler handler)
        {
            if (commandType == 0)
                throw new ArgumentOutOfRangeException(nameof(commandType));
            if (handler is null)
                throw new ArgumentNullException(nameof(handler));

            if (_handlers.ContainsKey(commandType))
                throw new InvalidOperationException($"Command handler already registered for type {commandType}.");

            _handlers.Add(commandType, handler);
        }

        public bool TryGetHandler(int commandType, out IAuthoritativeCommandHandler handler)
            => _handlers.TryGetValue(commandType, out handler);
    }

    /// <summary>
    /// TODO: Replace with real gameplay handlers once authoritative command surfaces are defined.
    /// No-op handler used for validation and proof-of-life counters only.
    /// </summary>
    public sealed class NoOpCommandHandler : IAuthoritativeCommandHandler
    {
        private long _handledCount;
        private long _lastSequence;

        public long HandledCount => _handledCount;
        public long LastSequence => _lastSequence;

        public void Handle(in AuthoritativeCommand command, SessionId sessionId, SimulationTickContext context)
        {
            _handledCount++;
            _lastSequence = command.DeterministicSequence;
        }
    }

    /// <summary>
    /// Tick-phase hook that consumes frozen authoritative command batches deterministically.
    /// Runs after the freeze hook and before simulation commit. Tick thread only.
    /// </summary>
    public sealed class AuthoritativeCommandConsumeTickHook : ITickPhaseHook
    {
        private readonly IAuthoritativeCommandIngestor _ingestor;
        private readonly ICommandHandlerRegistry _registry;
        private readonly IActiveSessionIndex _activeSessions;

        private long _frozenBatchesConsumed;
        private long _commandsDispatched;
        private long _unknownCommandTypeRejected;
        private long _handlerErrors;

        public AuthoritativeCommandConsumeTickHook(
            IAuthoritativeCommandIngestor ingestor,
            ICommandHandlerRegistry registry,
            IActiveSessionIndex activeSessions)
        {
            _ingestor = ingestor ?? throw new ArgumentNullException(nameof(ingestor));
            _registry = registry ?? throw new ArgumentNullException(nameof(registry));
            _activeSessions = activeSessions ?? throw new ArgumentNullException(nameof(activeSessions));
        }

        public CommandConsumeDiagnostics Diagnostics => new CommandConsumeDiagnostics(
            _frozenBatchesConsumed,
            _commandsDispatched,
            _unknownCommandTypeRejected,
            _handlerErrors);

        public int HandlerCount => _registry.HandlerCount;

        public void OnPreTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            TickThreadAssert.AssertTickThread();

            // Deterministic ordering:
            // - Sessions: active session snapshot order.
            // - Commands: frozen batch order (sorted by server receive sequence).
            var sessions = _activeSessions.SnapshotSessionsDeterministic();
            for (int s = 0; s < sessions.Count; s++)
            {
                var sessionId = sessions[s];
                var batch = _ingestor.GetFrozenBatch(sessionId);
                if (batch.AuthoritativeTick != context.TickIndex)
                    continue;

                _frozenBatchesConsumed++;

                var commands = batch.AsSpan();
                for (int i = 0; i < commands.Length; i++)
                {
                    ref readonly var command = ref commands[i];
                    if (_registry.TryGetHandler(command.CommandType, out var handler))
                    {
                        try
                        {
                            handler.Handle(in command, sessionId, context);
                        }
                        catch
                        {
                            _handlerErrors++;
                        }

                        _commandsDispatched++;
                    }
                    else
                    {
                        _unknownCommandTypeRejected++;
                    }
                }
            }
        }

        public void OnPostTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
        }
    }

    public readonly struct CommandConsumeDiagnostics
    {
        public CommandConsumeDiagnostics(
            long frozenBatchesConsumed,
            long commandsDispatched,
            long unknownCommandTypeRejected,
            long handlerErrors)
        {
            FrozenBatchesConsumed = frozenBatchesConsumed;
            CommandsDispatched = commandsDispatched;
            UnknownCommandTypeRejected = unknownCommandTypeRejected;
            HandlerErrors = handlerErrors;
        }

        public long FrozenBatchesConsumed { get; }
        public long CommandsDispatched { get; }
        public long UnknownCommandTypeRejected { get; }
        public long HandlerErrors { get; }
    }

    /// <summary>
    /// Deterministic inbound transport pump that bridges transport ingress into the authoritative command ingestor
    /// and freezes per-session command batches at tick start.
    /// </summary>
    public sealed class InboundPumpTickHook : ITickPhaseHook
    {
        private readonly PooledTransportRouter _transport;
        private readonly AuthoritativeCommandIngestor _ingestor;
        private readonly IActiveSessionIndex? _activeSessions;
        private readonly ServerStampedInboundCommand[] _ingressBuffer;
        private readonly int _maxFramesPerTick;
        private readonly int _maxCommandsPerTick;

        private long _ticksExecuted;
        private long _framesRouted;
        private long _commandsEnqueued;
        private long _commandsRejected;
        private long _rejectedClientTickProvided;
        private long _rejectedTooOld;
        private long _rejectedTooFarFuture;
        private long _acceptedStampedInbound;
        private readonly int _maxInboundAgeTicks;
        private readonly int _maxInboundLeadTicks;

        public InboundPumpTickHook(
            PooledTransportRouter transport,
            AuthoritativeCommandIngestor ingestor,
            IActiveSessionIndex? activeSessions = null,
            int maxFramesPerTick = 0,
            int maxCommandsPerTick = 0)
        {
            _transport = transport ?? throw new ArgumentNullException(nameof(transport));
            _ingestor = ingestor ?? throw new ArgumentNullException(nameof(ingestor));
            _activeSessions = activeSessions;

            var config = _transport.Config;
            _maxFramesPerTick = maxFramesPerTick > 0 ? maxFramesPerTick : config.MaxInboundCommandsPerSession;
            _maxCommandsPerTick = maxCommandsPerTick > 0 ? maxCommandsPerTick : config.MaxInboundCommandsPerSession;
            _maxInboundAgeTicks = Math.Max(0, config.MaxInboundCommandAgeTicks);
            _maxInboundLeadTicks = Math.Max(0, config.MaxInboundCommandLeadTicks);

            if (_maxCommandsPerTick <= 0)
                _maxCommandsPerTick = 1;

            _ingressBuffer = new ServerStampedInboundCommand[_maxCommandsPerTick];
        }

        public InboundPumpDiagnostics Diagnostics => new InboundPumpDiagnostics(
            _ticksExecuted,
            _framesRouted,
            _commandsEnqueued,
            _commandsRejected,
            _acceptedStampedInbound,
            _rejectedClientTickProvided,
            _rejectedTooOld,
            _rejectedTooFarFuture);

        public void OnPreTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            TickThreadAssert.AssertTickThread();

            _ticksExecuted++;
            _framesRouted += _transport.RouteQueuedInbound(context.TickIndex, _maxFramesPerTick);

            int drained = _transport.DeterministicRouter.DrainIngressDeterministic(_ingressBuffer, _maxCommandsPerTick);
            for (int i = 0; i < drained; i++)
            {
                var envelope = _ingressBuffer[i];

                Debug.Assert(envelope.ServerReceiveSeq > 0, "Inbound commands must be stamped with a server receive sequence.");
                Debug.Assert(envelope.ServerReceiveTick >= 0, "Inbound commands must be stamped with a valid server receive tick.");

                if (envelope.ClientSubmitTick > 0)
                {
                    _rejectedClientTickProvided++;
                    envelope.Dispose();
                    _ingressBuffer[i] = default;
                    continue;
                }

                if (IsTooOld(envelope.ServerReceiveTick, context.TickIndex))
                {
                    _rejectedTooOld++;
                    envelope.Dispose();
                    _ingressBuffer[i] = default;
                    continue;
                }

                if (IsTooFarFuture(envelope.ServerReceiveTick, context.TickIndex))
                {
                    _rejectedTooFarFuture++;
                    envelope.Dispose();
                    _ingressBuffer[i] = default;
                    continue;
                }

                _acceptedStampedInbound++;

                var command = DecodeCommand(envelope);
                if (_ingestor.TryEnqueue(envelope.SessionId, command))
                    _commandsEnqueued++;
                else
                    _commandsRejected++;

                envelope.Dispose();
                _ingressBuffer[i] = default;
            }

            FreezeCommands(context.TickIndex);
        }

        public void OnPostTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
        }

        public FrozenCommandBatch GetFrozenBatch(SessionId sessionId)
        {
            return _ingestor.GetFrozenBatch(sessionId);
        }

        private void FreezeCommands(long tickIndex)
        {
            if (_activeSessions != null)
            {
                _ingestor.FreezeSessions(tickIndex, _activeSessions.SnapshotSessionsDeterministic());
            }
            else
            {
                _ingestor.FreezeAllSessions(tickIndex);
            }
        }

        private static AuthoritativeCommand DecodeCommand(in ServerStampedInboundCommand envelope)
        {
            var payloadLength = envelope.Payload.Length;
            var payloadSpan = envelope.Payload.Buffer.AsSpan(0, payloadLength);

            int payloadA = payloadLength >= sizeof(int)
                ? BinaryPrimitives.ReadInt32LittleEndian(payloadSpan)
                : payloadLength;

            int payloadB = payloadLength >= sizeof(int) * 2
                ? BinaryPrimitives.ReadInt32LittleEndian(payloadSpan.Slice(sizeof(int)))
                : payloadLength;

            return new AuthoritativeCommand(envelope.ServerReceiveTick, envelope.CommandType, payloadA, payloadB, envelope.ServerReceiveSeq);
        }

        private bool IsTooOld(long serverReceiveTick, long currentTick)
        {
            if (_maxInboundAgeTicks <= 0)
                return false;

            return serverReceiveTick < currentTick - _maxInboundAgeTicks;
        }

        private bool IsTooFarFuture(long serverReceiveTick, long currentTick)
        {
            if (_maxInboundLeadTicks <= 0)
                return serverReceiveTick > currentTick;

            return serverReceiveTick > currentTick + _maxInboundLeadTicks;
        }
    }

    public readonly struct InboundPumpDiagnostics
    {
        public InboundPumpDiagnostics(
            long ticksExecuted,
            long framesRouted,
            long commandsEnqueued,
            long commandsRejected,
            long acceptedStampedInbound,
            long rejectedClientTickProvided,
            long rejectedTooOld,
            long rejectedTooFarFuture)
        {
            InboundPumpTicksExecuted = ticksExecuted;
            InboundFramesRouted = framesRouted;
            CommandsEnqueuedToIngestor = commandsEnqueued;
            CommandsRejectedByIngestor = commandsRejected;
            AcceptedStampedInbound = acceptedStampedInbound;
            RejectedClientTickProvided = rejectedClientTickProvided;
            RejectedTooOld = rejectedTooOld;
            RejectedTooFarFuture = rejectedTooFarFuture;
        }

        public long InboundPumpTicksExecuted { get; }
        public long InboundFramesRouted { get; }
        public long CommandsEnqueuedToIngestor { get; }
        public long CommandsRejectedByIngestor { get; }
        public long AcceptedStampedInbound { get; }
        public long RejectedClientTickProvided { get; }
        public long RejectedTooOld { get; }
        public long RejectedTooFarFuture { get; }
    }

    public readonly struct CommandIngestorDiagnostics
    {
        public static readonly CommandIngestorDiagnostics Empty = new CommandIngestorDiagnostics(Array.Empty<SessionCommandMetricsSnapshot>(), 0, default);

        private readonly SessionCommandMetricsSnapshot[] _buffer;
        private readonly SessionCommandMetricsReadOnlyList _view;

        public CommandIngestorDiagnostics(SessionCommandMetricsSnapshot[] buffer, int count, CommandIngestorTotals totals)
        {
            _buffer = buffer ?? Array.Empty<SessionCommandMetricsSnapshot>();
            Count = Math.Max(0, count);
            _view = new SessionCommandMetricsReadOnlyList(_buffer, Count);
            Totals = totals;
        }

        public int Count { get; }
        public CommandIngestorTotals Totals { get; }
        public IReadOnlyList<SessionCommandMetricsSnapshot> PerSession => _view;
    }

    public readonly struct CommandIngestorTotals
    {
        public CommandIngestorTotals(
            int accepted,
            int droppedOverflow,
            int droppedStale,
            int frozenLastTick,
            int peakBuffered,
            long commandRingGrows,
            long prewarmCompleted,
            long dropPathInvocations)
        {
            Accepted = accepted;
            DroppedOverflow = droppedOverflow;
            DroppedStale = droppedStale;
            FrozenLastTick = frozenLastTick;
            PeakBuffered = peakBuffered;
            CommandRingGrows = commandRingGrows;
            PrewarmCompleted = prewarmCompleted;
            DropPathInvocations = dropPathInvocations;
        }

        public int Accepted { get; }
        public int DroppedOverflow { get; }
        public int DroppedStale { get; }
        public int FrozenLastTick { get; }
        public int PeakBuffered { get; }
        public long CommandRingGrows { get; }
        public long PrewarmCompleted { get; }
        public long DropPathInvocations { get; }
    }

    public struct SessionCommandMetrics
    {
        public int Accepted;
        public int DroppedOverflow;
        public int DroppedStale;
        public int LastFrozenCount;
        public int PeakBuffered;
    }

    public readonly struct SessionCommandMetricsSnapshot
    {
        public SessionCommandMetricsSnapshot(SessionId sessionId, SessionCommandMetrics metrics)
        {
            SessionId = sessionId;
            Metrics = metrics;
        }

        public SessionId SessionId { get; }
        public SessionCommandMetrics Metrics { get; }
    }

    internal readonly struct SessionCommandMetricsReadOnlyList : IReadOnlyList<SessionCommandMetricsSnapshot>
    {
        private readonly SessionCommandMetricsSnapshot[] _buffer;
        private readonly int _count;

        public SessionCommandMetricsReadOnlyList(SessionCommandMetricsSnapshot[] buffer, int count)
        {
            _buffer = buffer ?? Array.Empty<SessionCommandMetricsSnapshot>();
            _count = count;
        }

        public SessionCommandMetricsSnapshot this[int index]
        {
            get
            {
                if ((uint)index >= (uint)_count)
                    throw new ArgumentOutOfRangeException(nameof(index));
                return _buffer[index];
            }
        }

        public int Count => _count;

        public Enumerator GetEnumerator() => new Enumerator(_buffer, _count);

        IEnumerator<SessionCommandMetricsSnapshot> IEnumerable<SessionCommandMetricsSnapshot>.GetEnumerator() => GetEnumerator();

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        internal struct Enumerator : IEnumerator<SessionCommandMetricsSnapshot>
        {
            private readonly SessionCommandMetricsSnapshot[] _buffer;
            private readonly int _count;
            private int _index;

            public Enumerator(SessionCommandMetricsSnapshot[] buffer, int count)
            {
                _buffer = buffer;
                _count = count;
                _index = -1;
            }

            public SessionCommandMetricsSnapshot Current => _buffer[_index];

            object IEnumerator.Current => Current;

            public bool MoveNext()
            {
                var next = _index + 1;
                if (next >= _count)
                    return false;
                _index = next;
                return true;
            }

            public void Reset() => _index = -1;

            public void Dispose()
            {
            }
        }
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
            TickThreadAssert.AssertTickThread();
            _spatialIndex.Upsert(entity, zone, position);
        }

        /// <summary>
        /// Removes an entity from the spatial index. Safe to call when already absent.
        /// </summary>
        public void Remove(EntityHandle entity)
        {
            TickThreadAssert.AssertTickThread();
            _spatialIndex.Remove(entity);
        }

        /// <summary>
        /// Rebuilds the deterministic visibility set for a session using the spatial index.
        /// </summary>
        public int RefreshVisibility(SessionId session, ZoneInterestQuery query)
        {
            TickThreadAssert.AssertTickThread();
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

            TickThreadAssert.AssertTickThread();
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
            TickThreadAssert.AssertTickThread();
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
            TickThreadAssert.AssertTickThread();
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
            TickThreadAssert.AssertTickThread();
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
