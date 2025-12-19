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
    /// - Delivery guards are scoped per authoritative tick
    /// - No cross-session or cross-tick memory is retained
    /// </summary>
    public sealed class CombatReplicationSystem
    {
        private readonly IClientRegistry _clientRegistry;
        private readonly IVisibilityPolicy _visibilityPolicy;
        private readonly INetworkSender _networkSender;
        private readonly IReplicationValidationSink _validationSink;

        // Delivery guard scoped PER TICK:
        // authoritativeTick -> (client -> delivered event ids)
        private readonly Dictionary<int, Dictionary<ClientId, HashSet<string>>> _deliveredByTick =
            new Dictionary<int, Dictionary<ClientId, HashSet<string>>>();

        private int? _currentTick;

        public CombatReplicationSystem(
            IClientRegistry clientRegistry,
            IVisibilityPolicy visibilityPolicy,
            INetworkSender networkSender,
            IReplicationValidationSink validationSink)
        {
            _clientRegistry = clientRegistry ?? throw new ArgumentNullException(nameof(clientRegistry));
            _visibilityPolicy = visibilityPolicy ?? throw new ArgumentNullException(nameof(visibilityPolicy));
            _networkSender = networkSender ?? throw new ArgumentNullException(nameof(networkSender));
            _validationSink = validationSink ?? throw new ArgumentNullException(nameof(validationSink));
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

            // Hard reset delivery guards for new tick
            _deliveredByTick.Clear();
            _deliveredByTick[authoritativeTick] =
                new Dictionary<ClientId, HashSet<string>>();
        }

        private void ReplicateSingleEvent(int authoritativeTick, CombatEvent combatEvent)
        {
            var subscribers = _clientRegistry.GetSubscribers(combatEvent.CombatContextId);

            for (int i = 0; i < subscribers.Count; i++)
            {
                var clientId = subscribers[i];

                if (!_visibilityPolicy.IsEventVisibleToClient(combatEvent, clientId))
                    continue;

                if (AlreadyDelivered(authoritativeTick, clientId, combatEvent.EventId))
                    continue;

                var payload = CombatEventPayload.FromCombatEvent(combatEvent);

                _networkSender.SendReliable(
                    clientId,
                    payload,
                    authoritativeTick);

                MarkDelivered(authoritativeTick, clientId, combatEvent.EventId);

                _validationSink.RecordReplicatedPayload(
                    clientId,
                    authoritativeTick,
                    payload);
            }
        }

        private bool AlreadyDelivered(int tick, ClientId clientId, string eventId)
        {
            var perTick = _deliveredByTick[tick];

            if (!perTick.TryGetValue(clientId, out var set))
                return false;

            return set.Contains(eventId);
        }

        private void MarkDelivered(int tick, ClientId clientId, string eventId)
        {
            var perTick = _deliveredByTick[tick];

            if (!perTick.TryGetValue(clientId, out var set))
            {
                set = new HashSet<string>(StringComparer.Ordinal);
                perTick.Add(clientId, set);
            }

            set.Add(eventId);
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
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public CombatEventType EventType { get; }

        public EntityHandle SubjectEntity { get; }

        public IntentResult? IntentResult { get; }
        public DamageOutcome? DamageOutcome { get; }
        public MitigationOutcome? MitigationOutcome { get; }
        public CombatEntityState? StateSnapshot { get; }

        private CombatEventPayload(
            string eventId,
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
