using System;
using System.Collections.Generic;
using Caelmor.Systems;

namespace Caelmor.Runtime.Persistence
{
    /// <summary>
    /// Server-authoritative runtime for persistence restore sequencing (Stage 23.5.B).
    /// Tracks restore requests per SaveId, enforces mid-tick gating, and exposes
    /// deterministic completion status for lifecycle, residency, and simulation gating.
    /// No disk IO, serialization, or zone/world mutation is performed here.
    /// </summary>
    public sealed class PlayerSaveRestoreSystem : IPlayerSaveRestoreSystem
    {
        private readonly IServerAuthority _authority;
        private readonly IRestoreMutationGate _mutationGate;
        private readonly IPersistenceRehydration _rehydration;

        private readonly object _gate = new object();
        private readonly Dictionary<SaveId, RestoreRecord> _records = new Dictionary<SaveId, RestoreRecord>();

        public PlayerSaveRestoreSystem(IServerAuthority authority, IRestoreMutationGate mutationGate, IPersistenceRehydration rehydration)
        {
            _authority = authority ?? throw new ArgumentNullException(nameof(authority));
            _mutationGate = mutationGate ?? throw new ArgumentNullException(nameof(mutationGate));
            _rehydration = rehydration ?? throw new ArgumentNullException(nameof(rehydration));
        }

        /// <summary>
        /// Requests restore for the given SaveId. Deterministic ordering:
        /// Requested → InProgress → Completed | Failed.
        /// Idempotent when restore already completed; rejected when mid-tick or already running.
        /// </summary>
        public RestoreRequestResult RequestRestore(SaveId saveId)
        {
            if (!_authority.IsServerAuthoritative)
                return RestoreRequestResult.Failed(RestoreRequestFailureReason.NotServerAuthority, RestoreStatus.None);

            if (!saveId.IsValid)
                return RestoreRequestResult.Failed(RestoreRequestFailureReason.InvalidSaveId, RestoreStatus.None);

            if (!_mutationGate.CanRestoreNow())
                return RestoreRequestResult.Failed(RestoreRequestFailureReason.MidTickRestoreForbidden, RestoreStatus.None);

            lock (_gate)
            {
                if (_records.TryGetValue(saveId, out var existing))
                {
                    if (existing.Status == RestoreStatus.Completed)
                        return RestoreRequestResult.Success(existing.Status, wasStateChanged: false);

                    if (existing.Status == RestoreStatus.InProgress || existing.Status == RestoreStatus.Requested)
                        return RestoreRequestResult.Failed(RestoreRequestFailureReason.AlreadyInProgress, existing.Status);

                    if (existing.Status == RestoreStatus.Failed)
                        return RestoreRequestResult.Failed(RestoreRequestFailureReason.PreviousRestoreFailed, existing.Status);
                }

                _records[saveId] = new RestoreRecord(RestoreStatus.Requested);
                _records[saveId] = new RestoreRecord(RestoreStatus.InProgress);
            }

            if (!_mutationGate.CanRestoreNow())
            {
                Fail(saveId);
                return RestoreRequestResult.Failed(RestoreRequestFailureReason.MidTickRestoreForbidden, RestoreStatus.InProgress);
            }

            var operation = _rehydration.PerformRestore(saveId);
            if (!operation.Ok)
            {
                Fail(saveId);
                return RestoreRequestResult.Failed(
                    RestoreRequestFailureReason.RestoreExecutionFailed,
                    RestoreStatus.Failed,
                    operation.FailureReason);
            }

            lock (_gate)
            {
                _records[saveId] = new RestoreRecord(RestoreStatus.Completed);
            }

            return RestoreRequestResult.Success(RestoreStatus.Completed, wasStateChanged: true);
        }

        /// <summary>
        /// Returns true when restore reached Completed state for the SaveId.
        /// </summary>
        public bool IsRestoreCompleted(SaveId saveId)
        {
            if (!saveId.IsValid)
                return false;

            lock (_gate)
            {
                return _records.TryGetValue(saveId, out var record) && record.Status == RestoreStatus.Completed;
            }
        }

        /// <summary>
        /// Exposes restore status for validation and diagnostics. No partial restore data is exposed.
        /// </summary>
        public bool TryGetStatus(SaveId saveId, out RestoreStatus status)
        {
            status = RestoreStatus.None;
            if (!saveId.IsValid)
                return false;

            lock (_gate)
            {
                if (_records.TryGetValue(saveId, out var record))
                {
                    status = record.Status;
                    return true;
                }
            }

            return false;
        }

        private void Fail(SaveId saveId)
        {
            lock (_gate)
            {
                _records[saveId] = new RestoreRecord(RestoreStatus.Failed);
            }
        }

        private readonly struct RestoreRecord
        {
            public RestoreRecord(RestoreStatus status)
            {
                Status = status;
            }

            public RestoreStatus Status { get; }
        }
    }

    public interface IPlayerSaveRestoreSystem : IPersistenceRestoreQuery
    {
        RestoreRequestResult RequestRestore(SaveId saveId);
        bool TryGetStatus(SaveId saveId, out RestoreStatus status);
    }

    public interface IRestoreMutationGate
    {
        bool CanRestoreNow();
    }

    public interface IPersistenceRehydration
    {
        RestoreOperationResult PerformRestore(SaveId saveId);
    }

    public readonly struct RestoreOperationResult
    {
        private RestoreOperationResult(bool ok, RestoreOperationFailureReason failureReason)
        {
            Ok = ok;
            FailureReason = failureReason;
        }

        public bool Ok { get; }
        public RestoreOperationFailureReason FailureReason { get; }

        public static RestoreOperationResult Success() => new RestoreOperationResult(true, RestoreOperationFailureReason.None);

        public static RestoreOperationResult Failed(RestoreOperationFailureReason reason) => new RestoreOperationResult(false, reason);
    }

    public readonly struct RestoreRequestResult
    {
        private RestoreRequestResult(
            bool ok,
            RestoreRequestFailureReason failureReason,
            RestoreStatus status,
            bool wasStateChanged,
            RestoreOperationFailureReason operationFailureReason)
        {
            Ok = ok;
            FailureReason = failureReason;
            Status = status;
            WasStateChanged = wasStateChanged;
            OperationFailureReason = operationFailureReason;
        }

        public bool Ok { get; }
        public RestoreRequestFailureReason FailureReason { get; }
        public RestoreStatus Status { get; }
        public bool WasStateChanged { get; }
        public RestoreOperationFailureReason OperationFailureReason { get; }

        public static RestoreRequestResult Success(RestoreStatus status, bool wasStateChanged)
            => new RestoreRequestResult(true, RestoreRequestFailureReason.None, status, wasStateChanged, RestoreOperationFailureReason.None);

        public static RestoreRequestResult Failed(
            RestoreRequestFailureReason reason,
            RestoreStatus status,
            RestoreOperationFailureReason operationFailureReason = RestoreOperationFailureReason.None)
            => new RestoreRequestResult(false, reason, status, wasStateChanged: false, operationFailureReason);
    }

    public enum RestoreRequestFailureReason
    {
        None = 0,
        NotServerAuthority = 1,
        InvalidSaveId = 2,
        MidTickRestoreForbidden = 3,
        AlreadyInProgress = 4,
        PreviousRestoreFailed = 5,
        RestoreExecutionFailed = 6
    }

    public enum RestoreOperationFailureReason
    {
        None = 0,
        PersistenceUnavailable = 1,
        ValidationFailed = 2,
        Unknown = 3
    }

    public enum RestoreStatus
    {
        None = 0,
        Requested = 1,
        InProgress = 2,
        Completed = 3,
        Failed = 4
    }
}
