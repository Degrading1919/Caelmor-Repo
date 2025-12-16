using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
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

        private readonly ISimulationEntityIndex _entities;
        private readonly List<ISimulationEligibilityGate> _eligibilityGates = new List<ISimulationEligibilityGate>();
        private readonly List<ParticipantEntry> _participants = new List<ParticipantEntry>();
        private readonly List<PhaseHookEntry> _phaseHooks = new List<PhaseHookEntry>();

        private readonly object _gate = new object();

        private long _participantSeq;
        private long _hookSeq;
        private long _tickIndex;
        private Thread? _thread;
        private CancellationTokenSource? _cts;
        private volatile bool _running;

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

        private void RunLoop(CancellationToken token)
        {
            var stopwatch = Stopwatch.StartNew();
            long tickCounter = 0;
            var nextTickAt = TickInterval;

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

                while (now >= nextTickAt && !token.IsCancellationRequested)
                {
                    ExecuteOneTick(TickInterval);
                    tickCounter++;
                    nextTickAt = TimeSpan.FromTicks(TickInterval.Ticks * (tickCounter + 1));
                    now = stopwatch.Elapsed;
                }
            }
        }

        private void ExecuteOneTick(TimeSpan fixedDelta)
        {
            ParticipantEntry[] participants;
            PhaseHookEntry[] hooks;
            ISimulationEligibilityGate[] gates;
            EntityHandle[] entities;

            lock (_gate)
            {
                participants = _participants.ToArray();
                hooks = _phaseHooks.ToArray();
                gates = _eligibilityGates.ToArray();
            }

            entities = _entities.SnapshotEntitiesDeterministic();

            var tickIndex = Interlocked.Increment(ref _tickIndex);
            var effectBuffer = new SimulationEffectBuffer();
            var tickContext = new SimulationTickContext(tickIndex, fixedDelta, effectBuffer);

            var eligibilitySnapshot = EvaluateEligibility(entities, gates);

            // Phase 1: Pre-Tick Gate Evaluation completed by EvaluateEligibility above.
            for (int i = 0; i < hooks.Length; i++)
                hooks[i].Hook.OnPreTick(tickContext, eligibilitySnapshot.EligibleEntities);

            // Phase 2: Simulation Execution.
            for (int p = 0; p < participants.Length; p++)
            {
                var participant = participants[p].Participant;
                for (int e = 0; e < eligibilitySnapshot.EligibleEntities.Length; e++)
                {
                    participant.Execute(eligibilitySnapshot.EligibleEntities[e], tickContext);
                }
            }

            // Phase 3: Post-Tick Finalization.
            EnsureEligibilityStable(entities, gates, eligibilitySnapshot);
            effectBuffer.Commit();

            for (int i = 0; i < hooks.Length; i++)
                hooks[i].Hook.OnPostTick(tickContext, eligibilitySnapshot.EligibleEntities);
        }

        private EligibilitySnapshot EvaluateEligibility(EntityHandle[] entities, ISimulationEligibilityGate[] gates)
        {
            var eligible = new List<EntityHandle>(entities.Length);
            var map = new Dictionary<EntityHandle, bool>(entities.Length);

            for (int i = 0; i < entities.Length; i++)
            {
                var entity = entities[i];
                bool allowed = true;
                for (int g = 0; g < gates.Length; g++)
                {
                    if (!gates[g].IsEligible(entity))
                    {
                        allowed = false;
                        break;
                    }
                }

                map[entity] = allowed;
                if (allowed)
                    eligible.Add(entity);
            }

            return new EligibilitySnapshot(entities, eligible.ToArray(), map);
        }

        private void EnsureEligibilityStable(EntityHandle[] entities, ISimulationEligibilityGate[] gates, EligibilitySnapshot snapshot)
        {
            for (int i = 0; i < entities.Length; i++)
            {
                var entity = entities[i];
                bool expected = snapshot.EligibilityMap[entity];
                bool current = true;
                for (int g = 0; g < gates.Length; g++)
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
            public readonly IReadOnlyDictionary<EntityHandle, bool> EligibilityMap;

            public EligibilitySnapshot(EntityHandle[] entities, EntityHandle[] eligibleEntities, IReadOnlyDictionary<EntityHandle, bool> map)
            {
                Entities = entities;
                EligibleEntities = eligibleEntities;
                EligibilityMap = map;
            }
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

        public void BufferEffect(string label, Action commit)
        {
            _buffer.Buffer(label, commit);
        }
    }

    internal sealed class SimulationEffectBuffer
    {
        private readonly List<(string label, Action commit)> _effects = new List<(string label, Action commit)>();

        public void Buffer(string label, Action commit)
        {
            if (commit is null) throw new ArgumentNullException(nameof(commit));
            _effects.Add((label ?? string.Empty, commit));
        }

        public void Commit()
        {
            for (int i = 0; i < _effects.Count; i++)
            {
                _effects[i].commit();
            }
            _effects.Clear();
        }
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
