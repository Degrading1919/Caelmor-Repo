// - Active runtime code only.
// - Fixed 10 Hz authoritative tick. No tick-thread blocking I/O.
// - Zero/low GC steady state after warm-up: no per-tick allocations in hot paths (do not introduce any).
// - Bounded growth/backpressure with deterministic overflow + metrics.
// - Deterministic ordering. No Dictionary iteration order reliance.
// - Thread ownership must be explicit and enforced: tick-thread asserts OR mailbox marshalling.
// - Deterministic cleanup on disconnect/shutdown; no leaks.
// - AOT/IL2CPP safe patterns only.
// CombatReplicationSystem.cs
// NOTE: Save location must follow existing project structure.
// Implements CombatReplicationSystem only.
// No combat logic, no state mutation, no persistence, no prediction.

using System;
using System.Collections.Generic;
using System.Threading;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Tick;

namespace Caelmor.Combat
{
    /// <summary>
    /// CombatReplicationSystem
    ///
    /// Responsibilities:
    /// - Consume authoritative CombatEvents emitted after application (Stage 12.4)
    /// - Replicate events to clients in deterministic, emission order
    /// - Enforce observability timing and visibility guarantees
    /// - Ensure exactly-once delivery per event per client PER TICK
    ///
    /// Restore-safety guarantee:
    /// - Delivery guards are scoped per session and cleared per authoritative tick
    /// - No cross-tick event ids are retained
    /// </summary>
    public sealed class CombatReplicationSystem
    {
        private readonly IClientRegistry _clientRegistry;
        private readonly IVisibilityPolicy _visibilityPolicy;
        private readonly INetworkSender _networkSender;
        private readonly IReplicationValidationSink _validationSink;

        // Delivery guard is reused; no per-tick allocations.
        private readonly Dictionary<SessionId, DeliveryGuard> _deliveryGuards =
            new Dictionary<SessionId, DeliveryGuard>();

        private int? _currentTick;
        private long _combatEventsReplicated;
        private long _deliveryGuardHits;
        private long _deliveryGuardMisses;
        private long _deliveryGuardOverflow;
        private long _combatReplicationTickCalls;
        private long _combatClientsReleased;
        private long _combatReleaseUnknownClientCount;
        private readonly int _deliveryGuardInitialCapacity;
        private readonly int _deliveryGuardMaxCount;

        public CombatReplicationSystem(
            IClientRegistry clientRegistry,
            IVisibilityPolicy visibilityPolicy,
            INetworkSender networkSender,
            IReplicationValidationSink validationSink,
            int deliveryGuardInitialCapacity = 256,
            int deliveryGuardMaxCount = 512)
        {
            _clientRegistry = clientRegistry ?? throw new ArgumentNullException(nameof(clientRegistry));
            _visibilityPolicy = visibilityPolicy ?? throw new ArgumentNullException(nameof(visibilityPolicy));
            _networkSender = networkSender ?? throw new ArgumentNullException(nameof(networkSender));
            _validationSink = validationSink ?? throw new ArgumentNullException(nameof(validationSink));
            if (deliveryGuardInitialCapacity <= 0) throw new ArgumentOutOfRangeException(nameof(deliveryGuardInitialCapacity));
            if (deliveryGuardMaxCount <= 0) throw new ArgumentOutOfRangeException(nameof(deliveryGuardMaxCount));
            if (deliveryGuardMaxCount < deliveryGuardInitialCapacity)
                throw new ArgumentOutOfRangeException(nameof(deliveryGuardMaxCount));
            _deliveryGuardInitialCapacity = deliveryGuardInitialCapacity;
            _deliveryGuardMaxCount = deliveryGuardMaxCount;
        }

        /// <summary>
        /// Replicates a batch of CombatEvents for a single authoritative tick.
        /// Events MUST be provided in the exact emission order.
        /// </summary>
        public void Replicate(in CombatEventBatch batch)
        {
            TickThreadAssert.AssertTickThread();
            Interlocked.Increment(ref _combatReplicationTickCalls);

            BeginTick(batch.AuthoritativeTick);

            for (int i = 0; i < batch.Count; i++)
            {
                var combatEvent = batch[i];
                ReplicateSingleEvent(batch.AuthoritativeTick, combatEvent);
            }
        }

        private void BeginTick(int authoritativeTick)
        {
            TickThreadAssert.AssertTickThread();
            if (_currentTick == authoritativeTick)
                return;

            _currentTick = authoritativeTick;

            // Delivery guards are reused per session; tick reset is per-client on first use.
        }

        private void ReplicateSingleEvent(int authoritativeTick, CombatEvent combatEvent)
        {
            TickThreadAssert.AssertTickThread();
            var subscribers = _clientRegistry.GetSubscribers(combatEvent.CombatContextId);

            for (int i = 0; i < subscribers.Count; i++)
            {
                var clientId = subscribers[i];

                if (!_visibilityPolicy.IsEventVisibleToClient(combatEvent, clientId))
                    continue;

                if (TryMarkDelivered(authoritativeTick, clientId, combatEvent.EventId))
                    continue;

                var payload = CombatEventPayload.FromCombatEvent(combatEvent);

                _networkSender.SendReliable(
                    clientId,
                    payload,
                    authoritativeTick);

                System.Threading.Interlocked.Increment(ref _combatEventsReplicated);
                _validationSink.RecordReplicatedPayload(
                    clientId,
                    authoritativeTick,
                    payload);
            }
        }

        private bool TryMarkDelivered(int tick, SessionId clientId, ulong eventId)
        {
            TickThreadAssert.AssertTickThread();
            if (!_deliveryGuards.TryGetValue(clientId, out var guard))
            {
                guard = new DeliveryGuard(_deliveryGuardInitialCapacity, _deliveryGuardMaxCount);
                _deliveryGuards.Add(clientId, guard);
            }

            return guard.TryMarkDelivered(
                tick,
                eventId,
                ref _deliveryGuardHits,
                ref _deliveryGuardMisses,
                ref _deliveryGuardOverflow);
        }

        public long CombatEventsReplicated => System.Threading.Interlocked.Read(ref _combatEventsReplicated);
        public long CombatDeliveryGuardHits => System.Threading.Interlocked.Read(ref _deliveryGuardHits);
        public long CombatDeliveryGuardMisses => System.Threading.Interlocked.Read(ref _deliveryGuardMisses);
        public long CombatDeliveryGuardOverflow => System.Threading.Interlocked.Read(ref _deliveryGuardOverflow);
        public long CombatReplicationTickCalls => System.Threading.Interlocked.Read(ref _combatReplicationTickCalls);
        public long CombatClientsReleased => System.Threading.Interlocked.Read(ref _combatClientsReleased);
        public long CombatReleaseUnknownClientCount => System.Threading.Interlocked.Read(ref _combatReleaseUnknownClientCount);

        public void ReleaseClient(SessionId clientId)
        {
            TickThreadAssert.AssertTickThread();
            if (_deliveryGuards.TryGetValue(clientId, out var guard))
            {
                guard.ClearAll();
                _deliveryGuards.Remove(clientId);
                System.Threading.Interlocked.Increment(ref _combatClientsReleased);
            }
            else
            {
                System.Threading.Interlocked.Increment(ref _combatReleaseUnknownClientCount);
            }
        }

        private sealed class DeliveryGuard
        {
            private readonly HashSet<ulong> _deliveredThisWindow;
            private readonly int _maxCount;
            private int _tick;
            private bool _hasTick;

            public DeliveryGuard(int initialCapacity, int maxCount)
            {
                _deliveredThisWindow = new HashSet<ulong>(initialCapacity);
                _maxCount = maxCount;
            }

            public bool TryMarkDelivered(
                int tick,
                ulong eventId,
                ref long hits,
                ref long misses,
                ref long overflow)
            {
                if (!_hasTick || _tick != tick)
                {
                    _deliveredThisWindow.Clear();
                    _tick = tick;
                    _hasTick = true;
                }

                if (_deliveredThisWindow.Contains(eventId))
                {
                    System.Threading.Interlocked.Increment(ref hits);
                    return true;
                }

                System.Threading.Interlocked.Increment(ref misses);
                if (_deliveredThisWindow.Count >= _maxCount)
                {
                    _deliveredThisWindow.Clear();
                    System.Threading.Interlocked.Increment(ref overflow);
                }

                _deliveredThisWindow.Add(eventId);
                return false;
            }

            public void ClearAll()
            {
                _deliveredThisWindow.Clear();
                _hasTick = false;
                _tick = 0;
            }
        }
    }

    // --------------------------------------------------------------------
    // Batch Input
    // --------------------------------------------------------------------

    public readonly struct CombatEventBatch
    {
        private readonly CombatEvent[] _events;
        private readonly int _count;
        public int AuthoritativeTick { get; }

        public CombatEventBatch(int authoritativeTick, CombatEvent[] eventsInOrder, int count)
        {
            AuthoritativeTick = authoritativeTick;
            _events = eventsInOrder ?? throw new ArgumentNullException(nameof(eventsInOrder));
            if (count < 0 || count > eventsInOrder.Length)
                throw new ArgumentOutOfRangeException(nameof(count));
            _count = count;
        }

        public int Count => _count;

        public CombatEvent this[int index]
        {
            get
            {
                if ((uint)index >= (uint)_count)
                    throw new ArgumentOutOfRangeException(nameof(index));
                return _events[index];
            }
        }
    }

    // --------------------------------------------------------------------
    // Payload (schema-only, no enrichment)
    // --------------------------------------------------------------------

    public sealed class CombatEventPayload
    {
        public ulong EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public CombatEventType EventType { get; }

        public EntityHandle SubjectEntity { get; }

        public IntentResult? IntentResult { get; }
        public DamageOutcome? DamageOutcome { get; }
        public MitigationOutcome? MitigationOutcome { get; }
        public CombatEntityState? StateSnapshot { get; }

        private CombatEventPayload(
            ulong eventId,
            int authoritativeTick,
            string combatContextId,
            CombatEventType eventType,
            EntityHandle subjectEntity,
            IntentResult? intentResult,
            DamageOutcome? damageOutcome,
            MitigationOutcome? mitigationOutcome,
            CombatEntityState? stateSnapshot)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            EventType = eventType;
            SubjectEntity = subjectEntity;
            IntentResult = intentResult;
            DamageOutcome = damageOutcome;
            MitigationOutcome = mitigationOutcome;
            StateSnapshot = stateSnapshot;
        }

        public static CombatEventPayload FromCombatEvent(CombatEvent e)
        {
            if (e == null) throw new ArgumentNullException(nameof(e));

            return new CombatEventPayload(
                e.EventId,
                e.AuthoritativeTick,
                e.CombatContextId,
                e.EventType,
                e.SubjectEntity,
                e.IntentResult,
                e.DamageOutcome,
                e.MitigationOutcome,
                e.StateSnapshot
            );
        }
    }

    // --------------------------------------------------------------------
    // Dependencies / Interfaces
    // --------------------------------------------------------------------

    public interface IClientRegistry
    {
        IReadOnlyList<SessionId> GetSubscribers(string combatContextId);
    }

    public interface IVisibilityPolicy
    {
        bool IsEventVisibleToClient(CombatEvent combatEvent, SessionId clientId);
    }

    public interface INetworkSender
    {
        void SendReliable(SessionId clientId, CombatEventPayload payload, int authoritativeTick);
    }

    public interface IReplicationValidationSink
    {
        void RecordReplicatedPayload(SessionId clientId, int authoritativeTick, CombatEventPayload payload);
    }
}
