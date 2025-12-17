using System;
using Caelmor.Runtime.Onboarding;

namespace Caelmor.Runtime.Persistence
{
    /// <summary>
    /// Hard server-side guardrails that deterministically reject any client-provided identifiers.
    /// Client may request "join" only; identity and save binding are server-authoritative only.
    /// No persistence IO, no networking implementation, no exceptions as control flow.
    /// </summary>
    public static class ClientIdentifierRejectionGuards
    {
        /// <summary>
        /// Defines whether an incoming join/request payload contains prohibited client-authored identifiers.
        /// Any non-empty PlayerId / SaveId / binding token is considered client-provided and must be rejected.
        /// </summary>
        public static GuardResult RejectIfClientProvidedIdentifiersPresent(in ClientJoinRequest request)
        {
            if (request.ClientProvidedPlayerId.IsValid)
                return GuardResult.Rejected(GuardFailureReason.ClientProvidedPlayerId);

            if (request.ClientProvidedSaveId.IsValid)
                return GuardResult.Rejected(GuardFailureReason.ClientProvidedSaveId);

            if (request.ClientProvidedBindingToken.IsPresent)
                return GuardResult.Rejected(GuardFailureReason.ClientProvidedBindingToken);

            return GuardResult.Accepted();
        }

        /// <summary>
        /// Ensures server-authoritative binding flow by rejecting any attempt to supply a SaveId
        /// when requesting a save binding. The server must allocate/validate the SaveId internally.
        /// </summary>
        public static GuardResult RejectIfClientProvidedSaveSelection(SaveId clientSuppliedSaveId, BindingToken clientSuppliedBindingToken)
        {
            if (clientSuppliedSaveId.IsValid)
                return GuardResult.Rejected(GuardFailureReason.ClientProvidedSaveId);

            if (clientSuppliedBindingToken.IsPresent)
                return GuardResult.Rejected(GuardFailureReason.ClientProvidedBindingToken);

            return GuardResult.Accepted();
        }

        /// <summary>
        /// Rejects any explicit PlayerId supplied by a client on any server entry path.
        /// The server must generate PlayerId and bind it to the session internally.
        /// </summary>
        public static GuardResult RejectIfClientProvidedPlayerId(PlayerId clientSuppliedPlayerId)
        {
            if (clientSuppliedPlayerId.IsValid)
                return GuardResult.Rejected(GuardFailureReason.ClientProvidedPlayerId);

            return GuardResult.Accepted();
        }
    }

    /// <summary>
    /// Minimal DTO shape representing a client join/request payload.
    /// This is a shape only (no networking implementation).
    /// Any populated identifier fields are prohibited.
    /// </summary>
    public readonly struct ClientJoinRequest
    {
        public readonly PlayerId ClientProvidedPlayerId;
        public readonly SaveId ClientProvidedSaveId;
        public readonly BindingToken ClientProvidedBindingToken;

        public ClientJoinRequest(PlayerId clientProvidedPlayerId, SaveId clientProvidedSaveId, BindingToken clientProvidedBindingToken)
        {
            ClientProvidedPlayerId = clientProvidedPlayerId;
            ClientProvidedSaveId = clientProvidedSaveId;
            ClientProvidedBindingToken = clientProvidedBindingToken;
        }
    }

    /// <summary>
    /// Opaque binding token that could imply client-side save selection. Any presence is rejected.
    /// </summary>
    public readonly struct BindingToken : IEquatable<BindingToken>
    {
        public readonly Guid Value;

        public BindingToken(Guid value)
        {
            Value = value;
        }

        public bool IsPresent => Value != Guid.Empty;

        public bool Equals(BindingToken other) => Value.Equals(other.Value);
        public override bool Equals(object obj) => obj is BindingToken other && Equals(other);
        public override int GetHashCode() => Value.GetHashCode();
        public override string ToString() => Value.ToString();
    }

    public readonly struct GuardResult
    {
        public readonly bool Ok;
        public readonly GuardFailureReason FailureReason;

        private GuardResult(bool ok, GuardFailureReason failureReason)
        {
            Ok = ok;
            FailureReason = failureReason;
        }

        public static GuardResult Accepted() => new GuardResult(true, GuardFailureReason.None);
        public static GuardResult Rejected(GuardFailureReason reason) => new GuardResult(false, reason);
    }

    public enum GuardFailureReason
    {
        None = 0,
        ClientProvidedPlayerId = 1,
        ClientProvidedSaveId = 2,
        ClientProvidedBindingToken = 3
    }

}
