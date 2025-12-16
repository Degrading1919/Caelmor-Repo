using System;
using System.Collections.Generic;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Players;
using Caelmor.Runtime.ZoneResidency;
using Caelmor.Systems;

namespace Caelmor.Runtime.PlayerLifecycle
{
    /// <summary>
    /// Server-authoritative player lifecycle runtime (Stage 23.4.B).
    /// Explicit state machine that gates simulation eligibility by lifecycle state
    /// and enforces ordering with sessions, zone residency, and mid-tick mutation rules.
    /// </summary>
    public sealed class PlayerLifecycleSystem : IPlayerLifecycleSystem
    {
        private readonly IServerAuthority _authority;
        private readonly IPlayerZoneResidencyQuery _residency;
        private readonly IPlayerSimulationEligibility _simulation;
        private readonly ILifecycleMutationGate _mutationGate;
        private readonly IPlayerLifecycleEvents _events;

        private readonly object _gate = new object();
        private readonly Dictionary<PlayerHandle, LifecycleRecord> _records = new Dictionary<PlayerHandle, LifecycleRecord>();
        private readonly Dictionary<SessionId, PlayerHandle> _playerBySession = new Dictionary<SessionId, PlayerHandle>();

        public PlayerLifecycleSystem(
            IServerAuthority authority,
            IPlayerZoneResidencyQuery residency,
            IPlayerSimulationEligibility simulation,
            ILifecycleMutationGate mutationGate,
            IPlayerLifecycleEvents events)
        {
            _authority = authority ?? throw new ArgumentNullException(nameof(authority));
            _residency = residency ?? throw new ArgumentNullException(nameof(residency));
            _simulation = simulation ?? throw new ArgumentNullException(nameof(simulation));
            _mutationGate = mutationGate ?? throw new ArgumentNullException(nameof(mutationGate));
            _events = events ?? throw new ArgumentNullException(nameof(events));
        }

        /// <summary>
        /// Registers a session-bound runtime player for lifecycle tracking.
        /// Does not create runtime instances or assign zones; idempotent for matching inputs.
        /// </summary>
        public RegisterLifecycleResult Register(SessionId sessionId, PlayerId playerId, PlayerHandle player)
        {
            if (!_authority.IsServerAuthoritative)
                return RegisterLifecycleResult.Failed(RegisterLifecycleFailureReason.NotServerAuthority);

            if (!IsValid(sessionId))
                return RegisterLifecycleResult.Failed(RegisterLifecycleFailureReason.InvalidSessionId);

            if (!playerId.IsValid)
                return RegisterLifecycleResult.Failed(RegisterLifecycleFailureReason.InvalidPlayerId);

            if (!player.IsValid)
                return RegisterLifecycleResult.Failed(RegisterLifecycleFailureReason.InvalidPlayerHandle);

            lock (_gate)
            {
                if (_playerBySession.TryGetValue(sessionId, out var existingPlayer))
                {
                    if (_records.TryGetValue(existingPlayer, out var existing) &&
                        existing.PlayerId.Equals(playerId) &&
                        existing.Player.Equals(player))
                    {
                        return RegisterLifecycleResult.Success(existing.Player, false);
                    }

                    return RegisterLifecycleResult.Failed(RegisterLifecycleFailureReason.SessionAlreadyRegistered);
                }

                if (_records.TryGetValue(player, out var existingRecord))
                {
                    if (existingRecord.PlayerId.Equals(playerId) && existingRecord.SessionId.Equals(sessionId))
                        return RegisterLifecycleResult.Success(existingRecord.Player, false);

                    return RegisterLifecycleResult.Failed(RegisterLifecycleFailureReason.PlayerAlreadyRegistered);
                }

                var record = new LifecycleRecord(sessionId, playerId, player, PlayerLifecycleState.Inactive, isSimulationEligible: false);
                _records.Add(player, record);
                _playerBySession.Add(sessionId, player);

                return RegisterLifecycleResult.Success(player, true);
            }
        }

        /// <summary>
        /// Activates an inactive or suspended player.
        /// Requires residency and mutation gate clearance.
        /// Grants simulation eligibility before marking the state active.
        /// </summary>
        public LifecycleTransitionResult Activate(PlayerHandle player)
        {
            return Transition(player, PlayerLifecycleState.Active);
        }

        /// <summary>
        /// Suspends an active player. Revokes simulation eligibility before state change.
        /// </summary>
        public LifecycleTransitionResult Suspend(PlayerHandle player)
        {
            return Transition(player, PlayerLifecycleState.Suspended);
        }

        /// <summary>
        /// Deactivates an active or suspended player. Revokes simulation eligibility before state change.
        /// </summary>
        public LifecycleTransitionResult Deactivate(PlayerHandle player, LifecycleTerminationReason reason)
        {
            return Transition(player, PlayerLifecycleState.Inactive, reason);
        }

        /// <summary>
        /// Returns the lifecycle state for the player if registered.
        /// </summary>
        public bool TryGetState(PlayerHandle player, out PlayerLifecycleState state)
        {
            lock (_gate)
            {
                if (_records.TryGetValue(player, out var record))
                {
                    state = record.State;
                    return true;
                }
            }

            state = default;
            return false;
        }

        /// <summary>
        /// Returns true if the player currently has simulation eligibility granted by this lifecycle system.
        /// </summary>
        public bool IsSimulationEligible(PlayerHandle player)
        {
            lock (_gate)
            {
                if (_records.TryGetValue(player, out var record))
                    return record.IsSimulationEligible;
            }

            return false;
        }

        private LifecycleTransitionResult Transition(PlayerHandle player, PlayerLifecycleState targetState, LifecycleTerminationReason terminationReason = LifecycleTerminationReason.None)
        {
            if (!_authority.IsServerAuthoritative)
                return LifecycleTransitionResult.Failed(PlayerLifecycleFailureReason.NotServerAuthority);

            if (!_mutationGate.CanMutateLifecycleNow())
                return LifecycleTransitionResult.Failed(PlayerLifecycleFailureReason.MidTickMutationForbidden);

            if (!player.IsValid)
                return LifecycleTransitionResult.Failed(PlayerLifecycleFailureReason.InvalidPlayerHandle);

            lock (_gate)
            {
                if (!_records.TryGetValue(player, out var record))
                    return LifecycleTransitionResult.Failed(PlayerLifecycleFailureReason.NotRegistered);

                if (targetState == PlayerLifecycleState.Active && !_residency.IsResident(player))
                    return LifecycleTransitionResult.Failed(PlayerLifecycleFailureReason.MissingZoneResidency);

                if (record.State == targetState)
                {
                    // Idempotent: ensure simulation eligibility matches state invariants.
                    if (targetState == PlayerLifecycleState.Active && !record.IsSimulationEligible)
                    {
                        if (!_simulation.TrySetSimulationEligible(player, isEligible: true))
                            return LifecycleTransitionResult.Failed(PlayerLifecycleFailureReason.SimulationEligibilityMutationFailed);

                        record = record.WithSimulationEligibility(true);
                        _records[player] = record;
                    }

                    if (targetState != PlayerLifecycleState.Active && record.IsSimulationEligible)
                    {
                        if (!_simulation.TrySetSimulationEligible(player, isEligible: false))
                            return LifecycleTransitionResult.Failed(PlayerLifecycleFailureReason.SimulationEligibilityMutationFailed);

                        record = record.WithSimulationEligibility(false);
                        _records[player] = record;
                    }

                    return LifecycleTransitionResult.Success(record.State, wasStateChanged: false);
                }

                if (!IsTransitionAllowed(record.State, targetState))
                    return LifecycleTransitionResult.Failed(PlayerLifecycleFailureReason.InvalidTransition);

                // Enforce ordering: adjust simulation eligibility before state changes.
                if (targetState == PlayerLifecycleState.Active)
                {
                    if (!_simulation.TrySetSimulationEligible(player, isEligible: true))
                        return LifecycleTransitionResult.Failed(PlayerLifecycleFailureReason.SimulationEligibilityMutationFailed);

                    record = record.WithSimulationEligibility(true);
                }
                else if (record.IsSimulationEligible)
                {
                    if (!_simulation.TrySetSimulationEligible(player, isEligible: false))
                        return LifecycleTransitionResult.Failed(PlayerLifecycleFailureReason.SimulationEligibilityMutationFailed);

                    record = record.WithSimulationEligibility(false);
                }

                var previousState = record.State;
                record = record.WithState(targetState);
                _records[player] = record;

                if (targetState == PlayerLifecycleState.Active)
                {
                    _events.OnPlayerActivated(record.SessionId, record.PlayerId, record.Player);
                }
                else if (targetState == PlayerLifecycleState.Suspended)
                {
                    _events.OnPlayerSuspended(record.SessionId, record.PlayerId, record.Player);
                }
                else
                {
                    _events.OnPlayerDeactivated(record.SessionId, record.PlayerId, record.Player, terminationReason);
                }

                return LifecycleTransitionResult.Success(record.State, wasStateChanged: !previousState.Equals(record.State));
            }
        }

        private static bool IsTransitionAllowed(PlayerLifecycleState current, PlayerLifecycleState target)
        {
            if (current == PlayerLifecycleState.Inactive)
                return target == PlayerLifecycleState.Active;

            if (current == PlayerLifecycleState.Active)
                return target == PlayerLifecycleState.Suspended || target == PlayerLifecycleState.Inactive;

            if (current == PlayerLifecycleState.Suspended)
                return target == PlayerLifecycleState.Active || target == PlayerLifecycleState.Inactive;

            return false;
        }

        private static bool IsValid(SessionId sessionId) => sessionId.Value != Guid.Empty;

        private readonly struct LifecycleRecord
        {
            public LifecycleRecord(SessionId sessionId, PlayerId playerId, PlayerHandle player, PlayerLifecycleState state, bool isSimulationEligible)
            {
                SessionId = sessionId;
                PlayerId = playerId;
                Player = player;
                State = state;
                IsSimulationEligible = isSimulationEligible;
            }

            public SessionId SessionId { get; }
            public PlayerId PlayerId { get; }
            public PlayerHandle Player { get; }
            public PlayerLifecycleState State { get; }
            public bool IsSimulationEligible { get; }

            public LifecycleRecord WithState(PlayerLifecycleState state) => new LifecycleRecord(SessionId, PlayerId, Player, state, IsSimulationEligible);

            public LifecycleRecord WithSimulationEligibility(bool isEligible) => new LifecycleRecord(SessionId, PlayerId, Player, State, isEligible);
        }
    }

    public interface IPlayerLifecycleSystem
    {
        RegisterLifecycleResult Register(SessionId sessionId, PlayerId playerId, PlayerHandle player);
        LifecycleTransitionResult Activate(PlayerHandle player);
        LifecycleTransitionResult Suspend(PlayerHandle player);
        LifecycleTransitionResult Deactivate(PlayerHandle player, LifecycleTerminationReason reason);
        bool TryGetState(PlayerHandle player, out PlayerLifecycleState state);
        bool IsSimulationEligible(PlayerHandle player);
    }

    public interface IPlayerZoneResidencyQuery
    {
        bool IsResident(PlayerHandle player);
    }

    public interface IPlayerSimulationEligibility
    {
        bool TrySetSimulationEligible(PlayerHandle player, bool isEligible);
    }

    public interface ILifecycleMutationGate
    {
        bool CanMutateLifecycleNow();
    }

    public interface IPlayerLifecycleEvents
    {
        void OnPlayerActivated(SessionId sessionId, PlayerId playerId, PlayerHandle player);
        void OnPlayerSuspended(SessionId sessionId, PlayerId playerId, PlayerHandle player);
        void OnPlayerDeactivated(SessionId sessionId, PlayerId playerId, PlayerHandle player, LifecycleTerminationReason reason);
    }

    public readonly struct RegisterLifecycleResult
    {
        private RegisterLifecycleResult(bool ok, RegisterLifecycleFailureReason failureReason, PlayerHandle? player, bool wasCreated)
        {
            Ok = ok;
            FailureReason = failureReason;
            Player = player;
            WasCreated = wasCreated;
        }

        public bool Ok { get; }
        public RegisterLifecycleFailureReason FailureReason { get; }
        public PlayerHandle? Player { get; }
        public bool WasCreated { get; }

        public static RegisterLifecycleResult Success(PlayerHandle player, bool wasCreated) => new RegisterLifecycleResult(true, RegisterLifecycleFailureReason.None, player, wasCreated);

        public static RegisterLifecycleResult Failed(RegisterLifecycleFailureReason reason) => new RegisterLifecycleResult(false, reason, null, wasCreated: false);
    }

    public readonly struct LifecycleTransitionResult
    {
        private LifecycleTransitionResult(bool ok, PlayerLifecycleFailureReason failureReason, PlayerLifecycleState? state, bool wasStateChanged)
        {
            Ok = ok;
            FailureReason = failureReason;
            State = state;
            WasStateChanged = wasStateChanged;
        }

        public bool Ok { get; }
        public PlayerLifecycleFailureReason FailureReason { get; }
        public PlayerLifecycleState? State { get; }
        public bool WasStateChanged { get; }

        public static LifecycleTransitionResult Success(PlayerLifecycleState state, bool wasStateChanged) => new LifecycleTransitionResult(true, PlayerLifecycleFailureReason.None, state, wasStateChanged);

        public static LifecycleTransitionResult Failed(PlayerLifecycleFailureReason reason) => new LifecycleTransitionResult(false, reason, null, wasStateChanged: false);
    }

    public enum PlayerLifecycleState
    {
        Inactive = 0,
        Active = 1,
        Suspended = 2
    }

    public enum PlayerLifecycleFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        MidTickMutationForbidden = 2,
        InvalidPlayerHandle = 3,
        NotRegistered = 4,
        MissingZoneResidency = 5,
        InvalidTransition = 6,
        SimulationEligibilityMutationFailed = 7
    }

    public enum RegisterLifecycleFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidSessionId = 2,
        InvalidPlayerId = 3,
        InvalidPlayerHandle = 4,
        SessionAlreadyRegistered = 5,
        PlayerAlreadyRegistered = 6
    }

    public enum LifecycleTerminationReason
    {
        None = 0,
        Explicit = 1,
        Disconnect = 2,
        PersistenceWindow = 3
    }
}
