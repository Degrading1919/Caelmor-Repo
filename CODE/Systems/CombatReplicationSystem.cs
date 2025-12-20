// CombatReplicationSystem.cs
// NOTE: Save location must follow existing project structure.
// Implements CombatReplicationSystem only.
// No combat logic, no state mutation, no persistence, no prediction.

using System;
using System.Collections.Generic;
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
        private readonly Dictionary<ClientId, DeliveryGuard> _deliveryGuards =
            new Dictionary<ClientId, DeliveryGuard>();

        private int? _currentTick;
        private long _combatEventsReplicated;
        private long _deliveryGuardHits;
        private long _deliveryGuardMisses;
        private long _deliveryGuardOverflow;
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
        public void Replicate(CombatEventBatch batch)
        {
            if (batch == null) throw new ArgumentNullException(nameof(batch));

            BeginTick(batch.AuthoritativeTick);

            for (int i = 0; i < batch.EventsInOrder.Count; i++)
            {
                var combatEvent = batch.EventsInOrder[i];
                ReplicateSingleEvent(batch.AuthoritativeTick, combatEvent);
            }
        }

        private void BeginTick(int authoritativeTick)
        {
            if (_currentTick == authoritativeTick)
                return;

            _currentTick = authoritativeTick;

            // Delivery guards are reused per session; tick reset is per-client on first use.
        }

        private void ReplicateSingleEvent(int authoritativeTick, CombatEvent combatEvent)
        {
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

        private bool TryMarkDelivered(int tick, ClientId clientId, ulong eventId)
        {
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

        public void ReleaseClient(ClientId clientId)
        {
            if (_deliveryGuards.TryGetValue(clientId, out var guard))
            {
                guard.ClearAll();
                _deliveryGuards.Remove(clientId);
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

    public sealed class CombatEventBatch
    {
        public int AuthoritativeTick { get; }
        public IReadOnlyList<CombatEvent> EventsInOrder { get; }

        public CombatEventBatch(int authoritativeTick, IReadOnlyList<CombatEvent> eventsInOrder)
        {
            AuthoritativeTick = authoritativeTick;
            EventsInOrder = eventsInOrder ?? throw new ArgumentNullException(nameof(eventsInOrder));
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

    public readonly struct ClientId
    {
        public readonly string Value;
        public ClientId(string value) { Value = value; }
    }

    public interface IClientRegistry
    {
        IReadOnlyList<ClientId> GetSubscribers(string combatContextId);
    }

    public interface IVisibilityPolicy
    {
        bool IsEventVisibleToClient(CombatEvent combatEvent, ClientId clientId);
    }

    public interface INetworkSender
    {
        void SendReliable(ClientId clientId, CombatEventPayload payload, int authoritativeTick);
    }

    public interface IReplicationValidationSink
    {
        void RecordReplicatedPayload(ClientId clientId, int authoritativeTick, CombatEventPayload payload);
    }
}
