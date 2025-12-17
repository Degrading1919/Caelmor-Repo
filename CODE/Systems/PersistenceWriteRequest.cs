using System;
using Caelmor.Runtime.Onboarding;

namespace Caelmor.Runtime.Persistence
{
    /// <summary>
    /// Persistence write request descriptor. Payload data is treated as opaque by the runtime;
    /// only deterministic metadata and size accounting are tracked for backpressure enforcement.
    /// </summary>
    public readonly struct PersistenceWriteRequest : IEquatable<PersistenceWriteRequest>
    {
        public PersistenceWriteRequest(SaveId saveId, PlayerId playerId, int estimatedBytes, string operationLabel)
        {
            if (estimatedBytes < 0) throw new ArgumentOutOfRangeException(nameof(estimatedBytes));
            SaveId = saveId;
            PlayerId = playerId;
            EstimatedBytes = estimatedBytes;
            OperationLabel = operationLabel ?? string.Empty;
        }

        public SaveId SaveId { get; }
        public PlayerId PlayerId { get; }
        public int EstimatedBytes { get; }
        public string OperationLabel { get; }

        public bool Equals(PersistenceWriteRequest other)
        {
            return SaveId.Equals(other.SaveId)
                && PlayerId.Equals(other.PlayerId)
                && EstimatedBytes == other.EstimatedBytes
                && string.Equals(OperationLabel, other.OperationLabel, StringComparison.Ordinal);
        }

        public override bool Equals(object obj) => obj is PersistenceWriteRequest other && Equals(other);
        public override int GetHashCode() => HashCode.Combine(SaveId, PlayerId, EstimatedBytes, OperationLabel);
    }
}
