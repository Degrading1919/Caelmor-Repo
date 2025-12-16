using System;
using System.Collections.Generic;
using Caelmor.Runtime.Players;
using Caelmor.Systems;

namespace Caelmor.Runtime.Quests
{
    /// <summary>
    /// Server-authoritative quest runtime (Stage 27.B).
    /// Manages quest instances as deterministic state machines, enforces explicit transitions,
    /// and processes progression outside simulation ticks without mutating other systems.
    /// </summary>
    public sealed class QuestRuntimeSystem : IQuestRuntimeSystem
    {
        private readonly IServerAuthority _authority;
        private readonly IQuestMutationGate _mutationGate;
        private readonly IPlayerLifecycleQuery _lifecycle;
        private readonly IQuestProgressionEvaluator _progressionEvaluator;

        private readonly object _gate = new object();
        private readonly Dictionary<QuestInstanceId, QuestRecord> _records = new Dictionary<QuestInstanceId, QuestRecord>();

        public QuestRuntimeSystem(
            IServerAuthority authority,
            IQuestMutationGate mutationGate,
            IPlayerLifecycleQuery lifecycle,
            IQuestProgressionEvaluator progressionEvaluator)
        {
            _authority = authority ?? throw new ArgumentNullException(nameof(authority));
            _mutationGate = mutationGate ?? throw new ArgumentNullException(nameof(mutationGate));
            _lifecycle = lifecycle ?? throw new ArgumentNullException(nameof(lifecycle));
            _progressionEvaluator = progressionEvaluator ?? throw new ArgumentNullException(nameof(progressionEvaluator));
        }

        /// <summary>
        /// Registers a quest instance for a player. Deterministic and idempotent for matching inputs.
        /// Does not mutate player lifecycle, inventory, or world state.
        /// </summary>
        public QuestRegistrationResult RegisterQuest(QuestInstanceId questId, PlayerHandle owner, string questDefinitionId)
        {
            if (!_authority.IsServerAuthoritative)
                return QuestRegistrationResult.Failed(QuestRegistrationFailureReason.NotServerAuthority);

            if (!questId.IsValid)
                return QuestRegistrationResult.Failed(QuestRegistrationFailureReason.InvalidQuestInstanceId);

            if (!owner.IsValid)
                return QuestRegistrationResult.Failed(QuestRegistrationFailureReason.InvalidPlayerHandle);

            if (string.IsNullOrWhiteSpace(questDefinitionId))
                return QuestRegistrationResult.Failed(QuestRegistrationFailureReason.InvalidQuestDefinitionId);

            lock (_gate)
            {
                if (_records.TryGetValue(questId, out var existing))
                {
                    if (existing.Owner.Equals(owner) && existing.QuestDefinitionId.Equals(questDefinitionId, StringComparison.Ordinal))
                        return QuestRegistrationResult.Success(existing.QuestId, false);

                    return QuestRegistrationResult.Failed(QuestRegistrationFailureReason.AlreadyRegistered);
                }

                var record = new QuestRecord(questId, owner, questDefinitionId, QuestState.Inactive);
                _records.Add(questId, record);

                return QuestRegistrationResult.Success(questId, true);
            }
        }

        /// <summary>
        /// Explicitly activates a quest instance. Requires lifecycle eligibility and mid-tick mutation clearance.
        /// </summary>
        public QuestStateTransitionResult ActivateQuest(QuestInstanceId questId)
        {
            return Transition(questId, QuestState.Active);
        }

        /// <summary>
        /// Explicitly marks a quest instance as completed.
        /// </summary>
        public QuestStateTransitionResult CompleteQuest(QuestInstanceId questId)
        {
            return Transition(questId, QuestState.Completed);
        }

        /// <summary>
        /// Explicitly marks a quest instance as failed.
        /// </summary>
        public QuestStateTransitionResult FailQuest(QuestInstanceId questId)
        {
            return Transition(questId, QuestState.Failed);
        }

        /// <summary>
        /// Processes progression for an active quest using read-only gameplay signals.
        /// Execution is deterministic, occurs outside simulation ticks, and never mutates other systems.
        /// </summary>
        public QuestProgressionResult ProcessProgression(QuestInstanceId questId, QuestProgressionEvents eventsSnapshot)
        {
            if (!_authority.IsServerAuthoritative)
                return QuestProgressionResult.Failed(QuestProgressionFailureReason.NotServerAuthority);

            if (!_mutationGate.CanMutateQuestsNow())
                return QuestProgressionResult.Failed(QuestProgressionFailureReason.MidTickMutationForbidden);

            if (!questId.IsValid)
                return QuestProgressionResult.Failed(QuestProgressionFailureReason.InvalidQuestInstanceId);

            lock (_gate)
            {
                if (!_records.TryGetValue(questId, out var record))
                    return QuestProgressionResult.Failed(QuestProgressionFailureReason.QuestNotRegistered);

                if (record.State != QuestState.Active)
                    return QuestProgressionResult.Failed(QuestProgressionFailureReason.InvalidState);

                if (!_lifecycle.IsPlayerActive(record.Owner))
                    return QuestProgressionResult.Failed(QuestProgressionFailureReason.LifecycleNotEligible);

                var context = new QuestProgressionContext(record.QuestId, record.Owner, record.State, eventsSnapshot);
                var decision = _progressionEvaluator.Evaluate(context);

                if (decision == QuestProgressionDecision.NoChange)
                    return QuestProgressionResult.Success(record.State, wasStateChanged: false);

                var targetState = decision == QuestProgressionDecision.Complete ? QuestState.Completed : QuestState.Failed;

                if (!IsTransitionAllowed(record.State, targetState))
                    return QuestProgressionResult.Failed(QuestProgressionFailureReason.InvalidTransition);

                record = record.WithState(targetState);
                _records[questId] = record;

                return QuestProgressionResult.Success(record.State, wasStateChanged: true);
            }
        }

        /// <summary>
        /// Returns true if the quest is tracked and outputs its current state.
        /// Read-only and deterministic.
        /// </summary>
        public bool TryGetState(QuestInstanceId questId, out QuestState state)
        {
            lock (_gate)
            {
                if (_records.TryGetValue(questId, out var record))
                {
                    state = record.State;
                    return true;
                }
            }

            state = default;
            return false;
        }

        /// <summary>
        /// Returns true if the quest is tracked and outputs its owner handle.
        /// </summary>
        public bool TryGetOwner(QuestInstanceId questId, out PlayerHandle owner)
        {
            lock (_gate)
            {
                if (_records.TryGetValue(questId, out var record))
                {
                    owner = record.Owner;
                    return true;
                }
            }

            owner = default;
            return false;
        }

        private QuestStateTransitionResult Transition(QuestInstanceId questId, QuestState targetState)
        {
            if (!_authority.IsServerAuthoritative)
                return QuestStateTransitionResult.Failed(QuestStateTransitionFailureReason.NotServerAuthority);

            if (!_mutationGate.CanMutateQuestsNow())
                return QuestStateTransitionResult.Failed(QuestStateTransitionFailureReason.MidTickMutationForbidden);

            if (!questId.IsValid)
                return QuestStateTransitionResult.Failed(QuestStateTransitionFailureReason.InvalidQuestInstanceId);

            lock (_gate)
            {
                if (!_records.TryGetValue(questId, out var record))
                    return QuestStateTransitionResult.Failed(QuestStateTransitionFailureReason.QuestNotRegistered);

                if (!_lifecycle.IsPlayerActive(record.Owner))
                    return QuestStateTransitionResult.Failed(QuestStateTransitionFailureReason.LifecycleNotEligible);

                if (!IsTransitionAllowed(record.State, targetState))
                    return QuestStateTransitionResult.Failed(QuestStateTransitionFailureReason.InvalidTransition);

                if (record.State == targetState)
                    return QuestStateTransitionResult.Success(record.State, wasStateChanged: false);

                record = record.WithState(targetState);
                _records[questId] = record;

                return QuestStateTransitionResult.Success(record.State, wasStateChanged: true);
            }
        }

        private static bool IsTransitionAllowed(QuestState current, QuestState target)
        {
            if (current == QuestState.Inactive)
                return target == QuestState.Active;

            if (current == QuestState.Active)
                return target == QuestState.Completed || target == QuestState.Failed;

            return false;
        }

        private readonly struct QuestRecord
        {
            public QuestRecord(QuestInstanceId questId, PlayerHandle owner, string questDefinitionId, QuestState state)
            {
                QuestId = questId;
                Owner = owner;
                QuestDefinitionId = questDefinitionId;
                State = state;
            }

            public QuestInstanceId QuestId { get; }
            public PlayerHandle Owner { get; }
            public string QuestDefinitionId { get; }
            public QuestState State { get; }

            public QuestRecord WithState(QuestState state) => new QuestRecord(QuestId, Owner, QuestDefinitionId, state);
        }
    }

    public interface IQuestRuntimeSystem
    {
        QuestRegistrationResult RegisterQuest(QuestInstanceId questId, PlayerHandle owner, string questDefinitionId);

        QuestStateTransitionResult ActivateQuest(QuestInstanceId questId);
        QuestStateTransitionResult CompleteQuest(QuestInstanceId questId);
        QuestStateTransitionResult FailQuest(QuestInstanceId questId);

        QuestProgressionResult ProcessProgression(QuestInstanceId questId, QuestProgressionEvents eventsSnapshot);

        bool TryGetState(QuestInstanceId questId, out QuestState state);
        bool TryGetOwner(QuestInstanceId questId, out PlayerHandle owner);
    }

    public interface IQuestMutationGate
    {
        bool CanMutateQuestsNow();
    }

    public interface IQuestProgressionEvaluator
    {
        QuestProgressionDecision Evaluate(QuestProgressionContext context);
    }

    public interface IPlayerLifecycleQuery
    {
        bool IsPlayerActive(PlayerHandle player);
    }

    public readonly struct QuestInstanceId : IEquatable<QuestInstanceId>
    {
        public readonly Guid Value;

        public QuestInstanceId(Guid value)
        {
            Value = value;
        }

        public bool IsValid => Value != Guid.Empty;

        public bool Equals(QuestInstanceId other) => Value.Equals(other.Value);
        public override bool Equals(object obj) => obj is QuestInstanceId other && Equals(other);
        public override int GetHashCode() => Value.GetHashCode();
        public override string ToString() => Value.ToString();
    }

    public readonly struct QuestProgressionEvents
    {
        public QuestProgressionEvents(
            IReadOnlyList<WorldEvent> worldEvents,
            IReadOnlyList<CombatEvent> combatEvents,
            IReadOnlyList<InventoryEvent> inventoryEvents)
        {
            WorldEvents = CopyOrEmpty(worldEvents);
            CombatEvents = CopyOrEmpty(combatEvents);
            InventoryEvents = CopyOrEmpty(inventoryEvents);
        }

        public IReadOnlyList<WorldEvent> WorldEvents { get; }
        public IReadOnlyList<CombatEvent> CombatEvents { get; }
        public IReadOnlyList<InventoryEvent> InventoryEvents { get; }

        private static T[] CopyOrEmpty<T>(IReadOnlyList<T> source)
        {
            if (source == null || source.Count == 0)
                return Array.Empty<T>();

            var copy = new T[source.Count];
            for (int i = 0; i < source.Count; i++)
                copy[i] = source[i];

            return copy;
        }
    }

    public readonly struct QuestProgressionContext
    {
        public QuestProgressionContext(QuestInstanceId questId, PlayerHandle owner, QuestState currentState, QuestProgressionEvents eventsSnapshot)
        {
            QuestId = questId;
            Owner = owner;
            CurrentState = currentState;
            Events = eventsSnapshot;
        }

        public QuestInstanceId QuestId { get; }
        public PlayerHandle Owner { get; }
        public QuestState CurrentState { get; }
        public QuestProgressionEvents Events { get; }
    }

    public readonly struct QuestRegistrationResult
    {
        private QuestRegistrationResult(bool ok, QuestRegistrationFailureReason failureReason, QuestInstanceId questId, bool wasCreated)
        {
            Ok = ok;
            FailureReason = failureReason;
            QuestId = questId;
            WasCreated = wasCreated;
        }

        public bool Ok { get; }
        public QuestRegistrationFailureReason FailureReason { get; }
        public QuestInstanceId QuestId { get; }
        public bool WasCreated { get; }

        public static QuestRegistrationResult Success(QuestInstanceId questId, bool wasCreated)
            => new QuestRegistrationResult(true, QuestRegistrationFailureReason.None, questId, wasCreated);

        public static QuestRegistrationResult Failed(QuestRegistrationFailureReason reason)
            => new QuestRegistrationResult(false, reason, default, wasCreated: false);
    }

    public readonly struct QuestStateTransitionResult
    {
        private QuestStateTransitionResult(bool ok, QuestStateTransitionFailureReason failureReason, QuestState? state, bool wasStateChanged)
        {
            Ok = ok;
            FailureReason = failureReason;
            State = state;
            WasStateChanged = wasStateChanged;
        }

        public bool Ok { get; }
        public QuestStateTransitionFailureReason FailureReason { get; }
        public QuestState? State { get; }
        public bool WasStateChanged { get; }

        public static QuestStateTransitionResult Success(QuestState state, bool wasStateChanged)
            => new QuestStateTransitionResult(true, QuestStateTransitionFailureReason.None, state, wasStateChanged);

        public static QuestStateTransitionResult Failed(QuestStateTransitionFailureReason reason)
            => new QuestStateTransitionResult(false, reason, null, wasStateChanged: false);
    }

    public readonly struct QuestProgressionResult
    {
        private QuestProgressionResult(bool ok, QuestProgressionFailureReason failureReason, QuestState? state, bool wasStateChanged)
        {
            Ok = ok;
            FailureReason = failureReason;
            State = state;
            WasStateChanged = wasStateChanged;
        }

        public bool Ok { get; }
        public QuestProgressionFailureReason FailureReason { get; }
        public QuestState? State { get; }
        public bool WasStateChanged { get; }

        public static QuestProgressionResult Success(QuestState state, bool wasStateChanged)
            => new QuestProgressionResult(true, QuestProgressionFailureReason.None, state, wasStateChanged);

        public static QuestProgressionResult Failed(QuestProgressionFailureReason reason)
            => new QuestProgressionResult(false, reason, null, wasStateChanged: false);
    }

    public readonly struct WorldEvent
    {
        public WorldEvent(string name)
        {
            Name = name ?? string.Empty;
        }

        public string Name { get; }
    }

    public readonly struct CombatEvent
    {
        public CombatEvent(string outcome)
        {
            Outcome = outcome ?? string.Empty;
        }

        public string Outcome { get; }
    }

    public readonly struct InventoryEvent
    {
        public InventoryEvent(string resource, int delta)
        {
            Resource = resource ?? string.Empty;
            Delta = delta;
        }

        public string Resource { get; }
        public int Delta { get; }
    }

    public enum QuestProgressionDecision
    {
        NoChange = 0,
        Complete = 1,
        Fail = 2
    }

    public enum QuestState
    {
        Inactive = 0,
        Active = 1,
        Completed = 2,
        Failed = 3
    }

    public enum QuestRegistrationFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidQuestInstanceId = 2,
        InvalidPlayerHandle = 3,
        InvalidQuestDefinitionId = 4,
        AlreadyRegistered = 5
    }

    public enum QuestStateTransitionFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        MidTickMutationForbidden = 2,
        InvalidQuestInstanceId = 3,
        QuestNotRegistered = 4,
        LifecycleNotEligible = 5,
        InvalidTransition = 6
    }

    public enum QuestProgressionFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        MidTickMutationForbidden = 2,
        InvalidQuestInstanceId = 3,
        QuestNotRegistered = 4,
        InvalidState = 5,
        LifecycleNotEligible = 6,
        InvalidTransition = 7
    }
}
