using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;

namespace Caelmor.Runtime.Tick
{
    /// <summary>
    /// Server-side authoritative tick system.
    /// Owns the fixed 10 Hz (100ms) tick loop and invokes tick participants in deterministic order.
    /// No gameplay logic, no networking, no persistence, no Unity Update()/FixedUpdate() coupling.
    /// </summary>
    public sealed class TickSystem : IDisposable
    {
        public const int TickRateHz = 10;
        public static readonly TimeSpan TickInterval = TimeSpan.FromMilliseconds(100);

        private readonly ITickEligibilityRegistry _eligibility;
        private readonly IEntityRegistry _entities;

        private readonly object _gate = new object();
        private readonly List<ParticipantEntry> _participants = new List<ParticipantEntry>();

        private Thread _thread;
        private CancellationTokenSource _cts;
        private volatile bool _running;
        private long _registrationSeq;

        public TickSystem(ITickEligibilityRegistry eligibility, IEntityRegistry entities)
        {
            _eligibility = eligibility ?? throw new ArgumentNullException(nameof(eligibility));
            _entities = entities ?? throw new ArgumentNullException(nameof(entities));
        }

        /// <summary>
        /// Registers an entity-tick participant invoked once per eligible entity each tick.
        /// Deterministic order is (orderKey asc) then (registration order asc).
        /// </summary>
        public void RegisterParticipant(ITickEntityParticipant participant, int orderKey)
        {
            if (participant is null) throw new ArgumentNullException(nameof(participant));

            lock (_gate)
            {
                _participants.Add(new ParticipantEntry(
                    participant,
                    orderKey,
                    Interlocked.Increment(ref _registrationSeq)));

                _participants.Sort(ParticipantEntryComparer.Instance);
            }
        }

        /// <summary>
        /// Starts the authoritative tick loop on a dedicated server thread.
        /// Idempotent: calling Start multiple times has no effect after the first successful start.
        /// </summary>
        public void Start()
        {
            if (_running) return;

            lock (_gate)
            {
                if (_running) return;

                _cts = new CancellationTokenSource();
                _thread = new Thread(() => RunLoop(_cts.Token))
                {
                    IsBackground = true,
                    Name = "Caelmor.TickSystem"
                };
                _running = true;
                _thread.Start();
            }
        }

        /// <summary>
        /// Requests a controlled stop. No partial tick execution occurs:
        /// the tick loop stops only between full tick boundaries.
        /// Idempotent.
        /// </summary>
        public void Stop()
        {
            if (!_running) return;

            CancellationTokenSource cts;
            Thread thread;

            lock (_gate)
            {
                if (!_running) return;
                cts = _cts;
                thread = _thread;
                _running = false;
            }

            try { cts?.Cancel(); } catch { /* no-op */ }

            try
            {
                // Wait for loop exit; if Stop is called from within the tick thread, do not Join self.
                if (thread != null && Thread.CurrentThread != thread)
                    thread.Join();
            }
            catch { /* no-op */ }
        }

        /// <summary>
        /// Returns true if the tick loop is currently running.
        /// </summary>
        public bool IsRunning => _running;

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

            // Schedule based on absolute time to avoid drift accumulation.
            long tickIndex = 0;
            var nextTickAt = TickInterval;

            while (!token.IsCancellationRequested)
            {
                var now = stopwatch.Elapsed;

                if (now < nextTickAt)
                {
                    var remaining = nextTickAt - now;

                    // Sleep most of the remaining time; spin the last tiny slice for tighter cadence.
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

                // Execute ticks for each elapsed interval, preserving deterministic ordering.
                while (now >= nextTickAt && !token.IsCancellationRequested)
                {
                    tickIndex++;
                    ExecuteOneTick(tickIndex, TickInterval);

                    nextTickAt = TimeSpan.FromTicks(TickInterval.Ticks * (tickIndex + 1));
                    now = stopwatch.Elapsed;
                }
            }
        }

        private void ExecuteOneTick(long tickIndex, TimeSpan fixedDelta)
        {
            // Snapshot participants deterministically.
            ITickEntityParticipant[] participantsSnapshot;
            lock (_gate)
            {
                var count = _participants.Count;
                participantsSnapshot = new ITickEntityParticipant[count];
                for (int i = 0; i < count; i++)
                    participantsSnapshot[i] = _participants[i].Participant;
            }

            // Snapshot entities deterministically.
            var entitiesSnapshot = _entities.SnapshotEntitiesDeterministic();

            var ctx = new TickContext(tickIndex, fixedDelta);

            // Deterministic invocation:
            // For each participant (ordered), tick each eligible entity (deterministic entity order).
            for (int p = 0; p < participantsSnapshot.Length; p++)
            {
                var participant = participantsSnapshot[p];
                for (int e = 0; e < entitiesSnapshot.Length; e++)
                {
                    var entity = entitiesSnapshot[e];

                    if (!_eligibility.IsTickEligible(entity))
                        continue;

                    participant.TickEntity(entity, ctx);
                }
            }
        }

        private readonly struct ParticipantEntry
        {
            public readonly ITickEntityParticipant Participant;
            public readonly int OrderKey;
            public readonly long RegistrationSeq;

            public ParticipantEntry(ITickEntityParticipant participant, int orderKey, long registrationSeq)
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
    }

    /// <summary>
    /// Tick context provided to participants. FixedDelta is always 100ms.
    /// </summary>
    public readonly struct TickContext
    {
        public readonly long TickIndex;
        public readonly TimeSpan FixedDelta;

        public TickContext(long tickIndex, TimeSpan fixedDelta)
        {
            TickIndex = tickIndex;
            FixedDelta = fixedDelta;
        }
    }

    /// <summary>
    /// Participant invoked once per eligible entity each tick.
    /// Implementations must be deterministic and server-authoritative.
    /// </summary>
    public interface ITickEntityParticipant
    {
        void TickEntity(EntityHandle entity, TickContext context);
    }

    /// <summary>
    /// Entity registry providing a deterministic snapshot of active runtime entities.
    /// No side effects; ordering must be stable/deterministic across calls within a tick.
    /// </summary>
    public interface IEntityRegistry
    {
        EntityHandle[] SnapshotEntitiesDeterministic();
    }

    /// <summary>
    /// Tick eligibility registry queried by the tick system.
    /// </summary>
    public interface ITickEligibilityRegistry
    {
        bool IsTickEligible(EntityHandle entity);
    }

    /// <summary>
    /// Opaque runtime entity handle. No gameplay assumptions permitted.
    /// </summary>
    public readonly struct EntityHandle : IEquatable<EntityHandle>
    {
        public readonly int Value;

        public EntityHandle(int value)
        {
            Value = value;
        }

        public bool IsValid => Value > 0;

        public bool Equals(EntityHandle other) => Value == other.Value;
        public override bool Equals(object obj) => obj is EntityHandle other && Equals(other);
        public override int GetHashCode() => Value;
        public override string ToString() => Value.ToString();
    }
}
