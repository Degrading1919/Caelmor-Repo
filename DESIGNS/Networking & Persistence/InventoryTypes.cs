// File: Economy/Inventory/InventoryTypes.cs

using System;
using System.Collections.Generic;

namespace Caelmor.Economy.Inventory
{
    public readonly struct ResourceGrant
    {
        public readonly string ResourceItemKey;
        public readonly int Count;

        public ResourceGrant(string resourceItemKey, int count)
        {
            if (string.IsNullOrWhiteSpace(resourceItemKey))
                throw new ArgumentException("ResourceItemKey must be non-empty.", nameof(resourceItemKey));
            if (count <= 0)
                throw new ArgumentOutOfRangeException(nameof(count), "Count must be > 0.");

            ResourceItemKey = resourceItemKey;
            Count = count;
        }
    }

    public readonly struct ResourceGrantedEvent
    {
        public readonly int PlayerId;
        public readonly int SourceNodeInstanceId;
        public readonly IReadOnlyList<ResourceGrant> Grants;

        public ResourceGrantedEvent(int playerId, int sourceNodeInstanceId, IReadOnlyList<ResourceGrant> grants)
        {
            PlayerId = playerId;
            SourceNodeInstanceId = sourceNodeInstanceId;
            Grants = grants ?? throw new ArgumentNullException(nameof(grants));
        }
    }

    public enum GrantProcessStatus : byte
    {
        Applied = 0,
        NoOp = 1,
        Failed = 2
    }

    public readonly struct GrantProcessResult
    {
        public readonly GrantProcessStatus Status;
        public readonly string? FailureReason;

        public GrantProcessResult(GrantProcessStatus status, string? failureReason)
        {
            Status = status;
            FailureReason = failureReason;
        }

        public static GrantProcessResult Applied => new GrantProcessResult(GrantProcessStatus.Applied, null);
        public static GrantProcessResult NoOp(string reason) => new GrantProcessResult(GrantProcessStatus.NoOp, reason);
        public static GrantProcessResult Failed(string reason) => new GrantProcessResult(GrantProcessStatus.Failed, reason);
    }
}
