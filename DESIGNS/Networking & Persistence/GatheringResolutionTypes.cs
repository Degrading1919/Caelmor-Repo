// File: Economy/Gathering/GatheringResolutionTypes.cs

using System;

namespace Caelmor.Economy.Gathering
{
    public enum GatheringOutcome : byte
    {
        Success = 0,
        FailureSoft = 1,
        FailureHard = 2
    }

    /// <summary>
    /// Optional tool context (policy-level only).
    /// No dependency on a tool schema.
    /// </summary>
    public readonly struct ToolContext
    {
        public readonly bool HasToolSystem;     // false => tool logic must be a no-op
        public readonly string? ToolClassKey;   // null/empty => no tool equipped / unknown

        public ToolContext(bool hasToolSystem, string? toolClassKey)
        {
            HasToolSystem = hasToolSystem;
            ToolClassKey = toolClassKey;
        }

        public static ToolContext None => new ToolContext(hasToolSystem: false, toolClassKey: null);
    }

    /// <summary>
    /// Output contract consumed by Stage 8.5.
    /// </summary>
    public readonly struct GatheringResolutionResult
    {
        public readonly GatheringOutcome Outcome;

        public readonly int PlayerId;
        public readonly int NodeInstanceId;
        public readonly string GatheringSkillKey;

        public readonly bool ResourceGrantAllowed;
        public readonly bool NodeDepletionAllowed;

        public readonly bool RiskTriggered;
        public readonly string? TriggeredRiskKey; // descriptive only

        public readonly string? FailureReason;    // null on success

        public GatheringResolutionResult(
            GatheringOutcome outcome,
            int playerId,
            int nodeInstanceId,
            string gatheringSkillKey,
            bool resourceGrantAllowed,
            bool nodeDepletionAllowed,
            bool riskTriggered,
            string? triggeredRiskKey,
            string? failureReason)
        {
            Outcome = outcome;
            PlayerId = playerId;
            NodeInstanceId = nodeInstanceId;
            GatheringSkillKey = gatheringSkillKey;

            ResourceGrantAllowed = resourceGrantAllowed;
            NodeDepletionAllowed = nodeDepletionAllowed;

            RiskTriggered = riskTriggered;
            TriggeredRiskKey = triggeredRiskKey;

            FailureReason = failureReason;
        }
    }
}
