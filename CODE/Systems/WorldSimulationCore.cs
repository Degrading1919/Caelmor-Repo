using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Tick;

namespace Caelmor.Runtime.WorldSimulation
{
    /// <summary>
    /// Server-authoritative world simulation core (Stage 28.B).
    /// Owns the fixed-rate simulation tick driver and orchestrates deterministic
    /// pre-tick eligibility gating, simulation execution, and post-tick finalization.
    /// No gameplay logic is implemented here.
    /// </summary>
    public sealed class WorldSimulationCore : IDisposable
    {
        public const int TickRateHz = 10;
        public static readonly TimeSpan TickInterval = TimeSpan.FromMilliseconds(100);
        private const int MaxCatchUpTicksPerLoop = 3;

        private readonly ISimulationEntityIndex _entities;
        private readonly List<ISimulationEligibilityGate> _eligibilityGates = new List<ISimulationEligibilityGate>();
        private readonly List<ParticipantEntry> _participants = new List<ParticipantEntry>();
        private readonly List<PhaseHookEntry> _phaseHooks = new List<PhaseHookEntry>();

        private ParticipantEntry[] _participantSnapshot = Array.Empty<ParticipantEntry>();
        private PhaseHookEntry[] _phaseHooksSnapshot = Array.Empty<PhaseHookEntry>();
        private ISimulationEligibilityGate[] _eligibilityGatesSnapshot = Array.Empty<ISimulationEligibilityGate>();

        private readonly List<EntityHandle> _eligibleBuffer = new List<EntityHandle>(128);
        private readonly Dictionary<EntityHandle, bool> _eligibilityMap = new Dictionary<EntityHandle, bool>(128);
        private EntityHandle[] _eligibleArray = Array.Empty<EntityHandle>();
        private readonly PooledArrayReadOnlyList<EntityHandle> _eligibleView = new PooledArrayReadOnlyList<EntityHandle>();

        private readonly SimulationEffectBuffer _effectBuffer = new SimulationEffectBuffer();

        private readonly object _gate = new object();
        private readonly TickDiagnostics _diagnostics = new TickDiagnostics();

        private long _participantSeq;
        private long _hookSeq;
        private long _tickIndex;
        private Thread? _thread;
        private CancellationTokenSource? _cts;
        private volatile bool _running;

#if DEBUG
        private int _maxEligibleEntities;
        private int _maxParticipants;
        private int _maxHooks;
#endif

        public WorldSimulationCore(ISimulationEntityIndex entities)
        {
            _entities = entities ?? throw new ArgumentNullException(nameof(entities));
        }

        /// <summary>
        /// Registers a gate evaluated during pre-tick eligibility determination.
        /// Registration order is deterministic.
        /// </summary>
        public void RegisterEligibilityGate(ISimulationEligibilityGate gate)
        {
            if (gate is null) throw new ArgumentNullException(nameof(gate));

            lock (_gate)
            {
                _eligibilityGates.Add(gate);
            }
        }

        /// <summary>
        /// Registers a simulation participant invoked for each eligible entity.
        /// Deterministic ordering: OrderKey ascending then registration sequence.
        /// </summary>
        public void RegisterParticipant(ISimulationParticipant participant, int orderKey)
        {
            if (participant is null) throw new ArgumentNullException(nameof(participant));

            lock (_gate)
            {
                _participants.Add(new ParticipantEntry(participant, orderKey, ++_participantSeq));
                _participants.Sort(ParticipantEntryComparer.Instance);
            }
        }

        /// <summary>
        /// Registers a phase hook invoked before and after simulation each tick.
        /// Deterministic ordering: OrderKey ascending then registration sequence.
        /// </summary>
        public void RegisterPhaseHook(ITickPhaseHook hook, int orderKey)
        {
            if (hook is null) throw new ArgumentNullException(nameof(hook));

            lock (_gate)
            {
                _phaseHooks.Add(new PhaseHookEntry(hook, orderKey, ++_hookSeq));
                _phaseHooks.Sort(PhaseHookEntryComparer.Instance);
            }
        }

        /// <summary>
        /// Starts the fixed-rate simulation tick loop on a dedicated background thread.
        /// Idempotent; multiple calls beyond the first successful start are ignored.
        /// </summary>
        public void Start()
        {
            if (_running)
                return;

            lock (_gate)
            {
                if (_running)
                    return;

                _cts = new CancellationTokenSource();
                _thread = new Thread(() => RunLoop(_cts.Token))
                {
                    IsBackground = true,
                    Name = "Caelmor.WorldSimulationCore"
                };
                _running = true;
                _thread.Start();
            }
        }

        /// <summary>
        /// Stops the simulation loop between tick boundaries.
        /// Idempotent and safe to call multiple times.
        /// </summary>
        public void Stop()
        {
            if (!_running)
                return;

            Thread? thread;
            CancellationTokenSource? cts;

            lock (_gate)
            {
                if (!_running)
                    return;

                thread = _thread;
                cts = _cts;
                _running = false;
            }

            try { cts?.Cancel(); } catch { /* no-op */ }

            try
            {
                if (thread != null && Thread.CurrentThread != thread)
                    thread.Join();
            }
            catch { /* no-op */ }
        }

        public bool IsRunning => _running;

        /// <summary>
        /// Executes exactly one simulation tick synchronously.
        /// Intended for deterministic validation harnesses; identical logic to the background loop.
        /// </summary>
        public void ExecuteSingleTick()
        {
            ExecuteOneTick(TickInterval);
        }

        public void Dispose()
        {
            Stop();
            lock (_gate)
            {
                _cts?.Dispose();
                _cts = null;
                _thread = null;
            }
        }

        public TickDiagnosticsSnapshot Diagnostics => _diagnostics.Snapshot();

        private void RunLoop(CancellationToken token)
        {
            var stopwatch = Stopwatch.StartNew();
            long tickCounter = 0;
            var nextTickAt = TickInterval;
            var tickStopwatch = new Stopwatch();

            TickThreadAssert.CaptureTickThread(Thread.CurrentThread);

            try
            {
                while (!token.IsCancellationRequested)
                {
                    var now = stopwatch.Elapsed;
                    if (now < nextTickAt)
                    {
                        var remaining = nextTickAt - now;
                        if (remaining > TimeSpan.FromMilliseconds(2))
                        {
                            try { Thread.Sleep(remaining - TimeSpan.FromMilliseconds(1)); }
                            catch { /* no-op */ }
                        }
                        else
                        {
                            Thread.SpinWait(64);
                        }

                        continue;
                    }

                    var catchUpExecuted = 0;
                    bool clamped = false;

                    while (now >= nextTickAt && !token.IsCancellationRequested && catchUpExecuted < MaxCatchUpTicksPerLoop)
                    {
                        tickStopwatch.Restart();
                        ExecuteOneTick(TickInterval);
                        tickStopwatch.Stop();

                        var duration = tickStopwatch.Elapsed;
                        var overrun = duration > TickInterval;
                        _diagnostics.RecordTick(duration, overrun, catchUpClamped: false);

                        tickCounter++;
                        catchUpExecuted++;
                        nextTickAt = TimeSpan.FromTicks(TickInterval.Ticks * (tickCounter + 1));
                        now = stopwatch.Elapsed;
                    }

                    if (now >= nextTickAt && catchUpExecuted >= MaxCatchUpTicksPerLoop)
                    {
                        var ticksBehind = (long)((now - nextTickAt).Ticks / TickInterval.Ticks) + 1;
                        tickCounter += ticksBehind;
                        nextTickAt = TimeSpan.FromTicks(TickInterval.Ticks * (tickCounter + 1));
                        clamped = true;
                    }

                    if (clamped)
                    {
                        _diagnostics.RecordTick(TimeSpan.Zero, overrun: true, catchUpClamped: true);
                    }
                }
            }
            finally
            {
                TickThreadAssert.ClearTickThread();
            }
        }

        private void ExecuteOneTick(TimeSpan fixedDelta)
        {
            TickThreadAssert.AssertTickThread();

            ParticipantEntry[] participants;
            int participantCount;
            PhaseHookEntry[] hooks;
            int hookCount;
            ISimulationEligibilityGate[] gates;
            int gateCount;
            EntityHandle[] entities;

            lock (_gate)
            {
                participantCount = _participants.Count;
                EnsureCapacity(ref _participantSnapshot, participantCount);
                _participants.CopyTo(_participantSnapshot, 0);
                participants = _participantSnapshot;

                hookCount = _phaseHooks.Count;
                EnsureCapacity(ref _phaseHooksSnapshot, hookCount);
                _phaseHooks.CopyTo(_phaseHooksSnapshot, 0);
                hooks = _phaseHooksSnapshot;

                gateCount = _eligibilityGates.Count;
                EnsureCapacity(ref _eligibilityGatesSnapshot, gateCount);
                _eligibilityGates.CopyTo(_eligibilityGatesSnapshot, 0);
                gates = _eligibilityGatesSnapshot;
            }

#if DEBUG
            if (participantCount > _maxParticipants)
                _maxParticipants = participantCount;
            if (hookCount > _maxHooks)
                _maxHooks = hookCount;
#endif

            entities = _entities.SnapshotEntitiesDeterministic();

            var tickIndex = Interlocked.Increment(ref _tickIndex);
            var tickContext = new SimulationTickContext(tickIndex, fixedDelta, _effectBuffer);

            _effectBuffer.BeginTick(tickIndex);
            try
            {
                var eligibilitySnapshot = EvaluateEligibility(entities, gateCount);

                // Phase 1: Pre-Tick Gate Evaluation completed by EvaluateEligibility above.
                for (int i = 0; i < hookCount; i++)
                    hooks[i].Hook.OnPreTick(tickContext, eligibilitySnapshot.EligibleView);

                // Phase 2: Simulation Execution.
                for (int p = 0; p < participantCount; p++)
                {
                    var participant = participants[p].Participant;
                    for (int e = 0; e < eligibilitySnapshot.EligibleCount; e++)
                    {
                        participant.Execute(eligibilitySnapshot.EligibleEntities[e], tickContext);
                    }
                }

                // Phase 3: Post-Tick Finalization.
                EnsureEligibilityStable(entities, gates, gateCount, eligibilitySnapshot);
                _effectBuffer.Commit();

                for (int i = 0; i < hookCount; i++)
                    hooks[i].Hook.OnPostTick(tickContext, eligibilitySnapshot.EligibleView);
            }
            finally
            {
                _effectBuffer.EndTick();
            }
        }

        private EligibilitySnapshot EvaluateEligibility(EntityHandle[] entities, int gateCount)
        {
            _eligibleBuffer.Clear();
            _eligibilityMap.Clear();

            for (int i = 0; i < entities.Length; i++)
            {
                var entity = entities[i];
                bool allowed = true;
                for (int g = 0; g < gateCount; g++)
                {
                    if (!_eligibilityGatesSnapshot[g].IsEligible(entity))
                    {
                        allowed = false;
                        break;
                    }
                }

                _eligibilityMap[entity] = allowed;
                if (allowed)
                    _eligibleBuffer.Add(entity);
            }

            EnsureCapacity(ref _eligibleArray, _eligibleBuffer.Count);
            for (int i = 0; i < _eligibleBuffer.Count; i++)
                _eligibleArray[i] = _eligibleBuffer[i];

#if DEBUG
            if (_eligibleBuffer.Count > _maxEligibleEntities)
                _maxEligibleEntities = _eligibleBuffer.Count;
#endif
            _eligibleView.Set(_eligibleArray, _eligibleBuffer.Count);

            return new EligibilitySnapshot(entities, _eligibleArray, _eligibleBuffer.Count, _eligibilityMap, _eligibleView);
        }

        private void EnsureEligibilityStable(EntityHandle[] entities, ISimulationEligibilityGate[] gates, int gateCount, EligibilitySnapshot snapshot)
        {
            for (int i = 0; i < entities.Length; i++)
            {
                var entity = entities[i];
                bool expected = snapshot.EligibilityMap[entity];
                bool current = true;
                for (int g = 0; g < gateCount; g++)
                {
                    if (!gates[g].IsEligible(entity))
                    {
                        current = false;
                        break;
                    }
                }

                if (current != expected)
                {
                    throw new InvalidOperationException(
                        $"SIMULATION_INVARIANT_VIOLATION: eligibility_mutated_mid_tick entity={entity}");
                }
            }
        }

        private readonly struct EligibilitySnapshot
        {
            public readonly EntityHandle[] Entities;
            public readonly EntityHandle[] EligibleEntities;
            public readonly int EligibleCount;
            public readonly IReadOnlyDictionary<EntityHandle, bool> EligibilityMap;
            public readonly IReadOnlyList<EntityHandle> EligibleView;

            public EligibilitySnapshot(EntityHandle[] entities, EntityHandle[] eligibleEntities, int eligibleCount, IReadOnlyDictionary<EntityHandle, bool> map, IReadOnlyList<EntityHandle> eligibleView)
            {
                Entities = entities;
                EligibleEntities = eligibleEntities;
                EligibleCount = eligibleCount;
                EligibilityMap = map;
                EligibleView = eligibleView;
            }
        }

        private static void EnsureCapacity<T>(ref T[] array, int required)
        {
            if (required <= array.Length)
                return;

            var nextSize = array.Length == 0 ? required : array.Length;
            while (nextSize < required)
                nextSize *= 2;

            array = new T[nextSize];
        }

        private readonly struct ParticipantEntry
        {
            public readonly ISimulationParticipant Participant;
            public readonly int OrderKey;
            public readonly long RegistrationSeq;

            public ParticipantEntry(ISimulationParticipant participant, int orderKey, long registrationSeq)
            {
                Participant = participant;
                OrderKey = orderKey;
                RegistrationSeq = registrationSeq;
            }
        }

        private sealed class ParticipantEntryComparer : IComparer<ParticipantEntry>
        {
            public static readonly ParticipantEntryComparer Instance = new ParticipantEntryComparer();

            public int Compare(ParticipantEntry x, ParticipantEntry y)
            {
                var c = x.OrderKey.CompareTo(y.OrderKey);
                if (c != 0) return c;
                return x.RegistrationSeq.CompareTo(y.RegistrationSeq);
            }
        }

        private readonly struct PhaseHookEntry
        {
            public readonly ITickPhaseHook Hook;
            public readonly int OrderKey;
            public readonly long RegistrationSeq;

            public PhaseHookEntry(ITickPhaseHook hook, int orderKey, long registrationSeq)
            {
                Hook = hook;
                OrderKey = orderKey;
                RegistrationSeq = registrationSeq;
            }
        }

        private sealed class PhaseHookEntryComparer : IComparer<PhaseHookEntry>
        {
            public static readonly PhaseHookEntryComparer Instance = new PhaseHookEntryComparer();

            public int Compare(PhaseHookEntry x, PhaseHookEntry y)
            {
                var c = x.OrderKey.CompareTo(y.OrderKey);
                if (c != 0) return c;
                return x.RegistrationSeq.CompareTo(y.RegistrationSeq);
            }
        }
    }

    internal sealed class PooledArrayReadOnlyList<T> : IReadOnlyList<T>
    {
        private T[] _buffer = Array.Empty<T>();
        private int _count;

        public void Set(T[] buffer, int count)
        {
            _buffer = buffer ?? Array.Empty<T>();
            _count = count;
        }

        public int Count => _count;

        public T this[int index]
        {
            get
            {
                if ((uint)index >= (uint)_count)
                    throw new ArgumentOutOfRangeException(nameof(index));
                return _buffer[index];
            }
        }

        public Enumerator GetEnumerator() => new Enumerator(_buffer, _count);

        IEnumerator<T> IEnumerable<T>.GetEnumerator() => GetEnumerator();

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        public struct Enumerator : IEnumerator<T>
        {
            private readonly T[] _array;
            private readonly int _count;
            private int _index;

            public Enumerator(T[] array, int count)
            {
                _array = array;
                _count = count;
                _index = -1;
            }

            public T Current => _array[_index];

            object IEnumerator.Current => Current!;

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
    /// Simulation tick context passed to participants and hooks.
    /// Effects buffered through this context are committed only at Post-Tick Finalization.
    /// </summary>
    public readonly struct SimulationTickContext
    {
        private readonly SimulationEffectBuffer _buffer;

        public readonly long TickIndex;
        public readonly TimeSpan FixedDelta;

        internal SimulationTickContext(long tickIndex, TimeSpan fixedDelta, SimulationEffectBuffer buffer)
        {
            TickIndex = tickIndex;
            FixedDelta = fixedDelta;
            _buffer = buffer;
        }

        public void BufferEffect(in SimulationEffectCommand command) => _buffer.Buffer(command);
    }

    internal enum SimulationEffectCommandType : byte
    {
        None = 0,
        CombatOutcomeCommit = 1,
        FlagSignal = 2,
        AppendLog = 3
    }

    /// <summary>
    /// Effect command recorded during tick execution.
    /// </summary>
    public readonly struct SimulationEffectCommand
    {
        private readonly SimulationEffectCommandType _type;
        private readonly string _label;
        private readonly EntityHandle _entity;
        private readonly CombatResolutionResult? _combatResolution;
        private readonly ICombatOutcomeCommitSink? _combatCommitSink;
        private readonly EffectFlagMarker? _flagMarker;
        private readonly IList<string>? _logTarget;
        private readonly string? _logEntry;

        private SimulationEffectCommand(
            SimulationEffectCommandType type,
            string label,
            EntityHandle entity,
            CombatResolutionResult? combatResolution,
            ICombatOutcomeCommitSink? combatCommitSink,
            EffectFlagMarker? flagMarker,
            IList<string>? logTarget,
            string? logEntry)
        {
            _type = type;
            _label = label ?? string.Empty;
            _entity = entity;
            _combatResolution = combatResolution;
            _combatCommitSink = combatCommitSink;
            _flagMarker = flagMarker;
            _logTarget = logTarget;
            _logEntry = logEntry;
        }

        internal SimulationEffectCommandType Type => _type;
        internal string Label => _label;
        internal EntityHandle Entity => _entity;
        internal CombatResolutionResult? CombatResolution => _combatResolution;
        internal ICombatOutcomeCommitSink? CombatCommitSink => _combatCommitSink;
        internal EffectFlagMarker? FlagMarker => _flagMarker;
        internal IList<string>? LogTarget => _logTarget;
        internal string? LogEntry => _logEntry;

        public static SimulationEffectCommand CombatOutcomeCommit(
            EntityHandle entity,
            ICombatOutcomeCommitSink commitSink,
            CombatResolutionResult resolution,
            string label = "combat_outcome")
        {
            if (commitSink is null) throw new ArgumentNullException(nameof(commitSink));
            if (resolution is null) throw new ArgumentNullException(nameof(resolution));
            return new SimulationEffectCommand(
                SimulationEffectCommandType.CombatOutcomeCommit,
                label,
                entity,
                resolution,
                commitSink,
                null,
                null,
                null);
        }

        public static SimulationEffectCommand FlagSignal(EffectFlagMarker marker, string label = "flag_signal")
        {
            if (marker is null) throw new ArgumentNullException(nameof(marker));
            return new SimulationEffectCommand(
                SimulationEffectCommandType.FlagSignal,
                label,
                default,
                null,
                null,
                marker,
                null,
                null);
        }

        public static SimulationEffectCommand AppendLog(IList<string> target, string entry, string label = "append_log")
        {
            if (target is null) throw new ArgumentNullException(nameof(target));
            if (entry is null) throw new ArgumentNullException(nameof(entry));
            return new SimulationEffectCommand(
                SimulationEffectCommandType.AppendLog,
                label,
                default,
                null,
                null,
                null,
                target,
                entry);
        }
    }

    /// <summary>
    /// Effect buffer optimized for zero-allocation steady state usage.
    /// </summary>
    internal sealed class SimulationEffectBuffer
    {
        private const int MaxBufferedEffects = 512;
        private readonly List<SimulationEffectCommand> _effects = new List<SimulationEffectCommand>(MaxBufferedEffects);
        private bool _tickWindowOpen;
        private long _tickIndex;

        public void BeginTick(long tickIndex)
        {
            if (_tickWindowOpen)
                throw new InvalidOperationException("Effect buffering tick window already open.");

#if DEBUG
            if (_effects.Count != 0)
                throw new InvalidOperationException("Effect buffer must be empty at tick start.");
#endif

            _tickWindowOpen = true;
            _tickIndex = tickIndex;
        }

        public void Buffer(in SimulationEffectCommand command)
        {
            if (!_tickWindowOpen)
                throw new InvalidOperationException("Effects can only be buffered during tick execution.");

            var nextIndex = _effects.Count + 1;
#if DEBUG
            if (nextIndex > MaxBufferedEffects)
                throw new InvalidOperationException($"Buffered effects exceeded budget ({MaxBufferedEffects}).");
#endif
            if (nextIndex > _effects.Capacity)
                throw new InvalidOperationException("Effect buffer capacity exhausted.");

            _effects.Add(command);
        }

        public void Commit()
        {
            if (!_tickWindowOpen)
                throw new InvalidOperationException("Commit can only execute during an open tick window.");

#if DEBUG
            if (_tickIndex == 0)
                throw new InvalidOperationException("Tick index was not initialized for effect buffer.");
#endif

            for (int i = 0; i < _effects.Count; i++)
            {
                Apply(in _effects[i]);
            }

            _effects.Clear();
        }

        public void EndTick()
        {
            if (!_tickWindowOpen)
                throw new InvalidOperationException("Effect buffering tick window was not open.");

            _effects.Clear();
            _tickWindowOpen = false;
            _tickIndex = 0;
        }

        private static void Apply(in SimulationEffectCommand command)
        {
            switch (command.Type)
            {
                case SimulationEffectCommandType.CombatOutcomeCommit:
                    Debug.Assert(command.CombatCommitSink != null, "CombatOutcomeCommit requires sink.");
                    Debug.Assert(command.CombatResolution != null, "CombatOutcomeCommit requires resolution.");
                    command.CombatCommitSink!.Commit(command.Entity, command.CombatResolution!);
                    break;
                case SimulationEffectCommandType.FlagSignal:
                    Debug.Assert(command.FlagMarker != null, "FlagSignal requires marker.");
                    command.FlagMarker!.Mark();
                    break;
                case SimulationEffectCommandType.AppendLog:
                    Debug.Assert(command.LogTarget != null, "AppendLog requires target.");
                    Debug.Assert(command.LogEntry != null, "AppendLog requires entry.");
                    command.LogTarget!.Add(command.LogEntry!);
                    break;
                default:
                    throw new InvalidOperationException($"Unknown effect command type {command.Type}.");
            }
        }
    }

    /// <summary>
    /// Marker used by validation helpers and diagnostics to record effect commits without allocations.
    /// </summary>
    public sealed class EffectFlagMarker
    {
        public bool IsMarked { get; private set; }

        public void Mark() => IsMarked = true;
    }

    /// <summary>
    /// Minimal eligibility gate contract used by the world simulation core.
    /// </summary>
    public interface ISimulationEligibilityGate
    {
        string Name { get; }
        bool IsEligible(EntityHandle entity);
    }

    /// <summary>
    /// Simulation participant invoked during the Simulation Execution phase.
    /// </summary>
    public interface ISimulationParticipant
    {
        void Execute(EntityHandle entity, SimulationTickContext context);
    }

    /// <summary>
    /// Phase hooks invoked during Pre-Tick Gate Evaluation and Post-Tick Finalization.
    /// </summary>
    public interface ITickPhaseHook
    {
        void OnPreTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities);
        void OnPostTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities);
    }

    /// <summary>
    /// Deterministic entity index supplying the world simulation core with runtime entities.
    /// </summary>
    public interface ISimulationEntityIndex
    {
        EntityHandle[] SnapshotEntitiesDeterministic();
    }
}
