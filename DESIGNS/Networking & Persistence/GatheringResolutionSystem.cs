// File: Economy/Gathering/GatheringResolutionSystem.cs

using System;
using System.Collections.Generic;

namespace Caelmor.Economy.Gathering
{
    /// <summary>
    /// Stage 7.2 / Stage 8.4:
    /// Deterministic server-authoritative resolution for a gather attempt.
    ///
    /// Responsibilities:
    /// - Validate node exists + is available
    /// - Validate gathering skill is allowed for node AND player possesses it
    /// - Apply optional tool policy
    /// - Surface triggered risk (descriptive only)
    /// - Return GatheringResolutionResult for downstream systems
    ///
    /// Non-goals:
    /// - No node depletion (Stage 8.3 handles state; Stage 8.5 will coordinate)
    /// - No inventory grants
    /// - No XP, tuning, RNG, persistence, UI
    /// </summary>
    public sealed class GatheringResolutionSystem
    {
        private readonly IGatheringNodeQuery _nodeQuery;
        private readonly IPlayerGatheringSkillProvider _playerSkills;
        private readonly IGatheringToolPolicyProvider _toolPolicy;
        private readonly IGatheringRiskPolicy _riskPolicy;

        public GatheringResolutionSystem(
            IGatheringNodeQuery nodeQuery,
            IPlayerGatheringSkillProvider playerSkills,
            IGatheringToolPolicyProvider? toolPolicyProvider = null,
            IGatheringRiskPolicy? riskPolicy = null)
        {
            _nodeQuery = nodeQuery ?? throw new ArgumentNullException(nameof(nodeQuery));
            _playerSkills = playerSkills ?? throw new ArgumentNullException(nameof(playerSkills));
            _toolPolicy = toolPolicyProvider ?? NoToolPolicyProvider.Instance;
            _riskPolicy = riskPolicy ?? NoRiskPolicy.Instance;
        }

        public GatheringResolutionResult ResolveAttempt(
            int playerId,
            int nodeInstanceId,
            string gatheringSkillKey,
            ToolContext toolContext)
        {
            if (string.IsNullOrWhiteSpace(gatheringSkillKey))
            {
                return HardFail(playerId, nodeInstanceId, gatheringSkillKey,
                    failureReason: "invalid_gathering_skill_key");
            }

            // ---- Validation: node existence + availability + definition facts ----
            if (!_nodeQuery.TryGetNodeContext(
                    nodeInstanceId,
                    out var nodeTypeKey,
                    out var availability,
                    out var allowedSkills,
                    out var riskFlags))
            {
                return HardFail(playerId, nodeInstanceId, gatheringSkillKey,
                    failureReason: "node_not_found");
            }

            if (availability != NodeAvailability.Available)
            {
                return HardFail(playerId, nodeInstanceId, gatheringSkillKey,
                    failureReason: "node_not_available");
            }

            // ---- Validation: gathering skill allowed for this node ----
            if (!ContainsString(allowedSkills, gatheringSkillKey))
            {
                return HardFail(playerId, nodeInstanceId, gatheringSkillKey,
                    failureReason: "skill_not_allowed_for_node");
            }

            // ---- Validation: player possesses the gathering skill (boolean-only) ----
            if (!_playerSkills.PlayerHasGatheringSkill(playerId, gatheringSkillKey))
            {
                return HardFail(playerId, nodeInstanceId, gatheringSkillKey,
                    failureReason: "player_missing_required_skill");
            }

            // ---- Tool policy (optional, policy-level) ----
            var toolCheck = EvaluateToolPolicy(nodeTypeKey, gatheringSkillKey, toolContext);
            if (toolCheck.outcome == GatheringOutcome.FailureHard)
            {
                return HardFail(playerId, nodeInstanceId, gatheringSkillKey, toolCheck.failureReason!);
            }
            if (toolCheck.outcome == GatheringOutcome.FailureSoft)
            {
                return SoftFail(playerId, nodeInstanceId, gatheringSkillKey, toolCheck.failureReason!);
            }

            // ---- Risk surfacing (deterministic; descriptive) ----
            // Stage 7.2 allows provisional mapping: if risk triggers => hard failure.
            // Triggering rules are NOT defined in Stage 7.2, so policy provides the deterministic trigger.
            string? triggeredRisk = _riskPolicy.DetermineTriggeredRisk(
                playerId, nodeInstanceId, nodeTypeKey, gatheringSkillKey, riskFlags, toolContext);

            if (!string.IsNullOrEmpty(triggeredRisk))
            {
                // Provisional coupling per Stage 7.2: triggered risk => hard failure
                return new GatheringResolutionResult(
                    outcome: GatheringOutcome.FailureHard,
                    playerId: playerId,
                    nodeInstanceId: nodeInstanceId,
                    gatheringSkillKey: gatheringSkillKey,
                    resourceGrantAllowed: false,
                    nodeDepletionAllowed: false,
                    riskTriggered: true,
                    triggeredRiskKey: triggeredRisk,
                    failureReason: "risk_triggered");
            }

            // ---- Success ----
            return new GatheringResolutionResult(
                outcome: GatheringOutcome.Success,
                playerId: playerId,
                nodeInstanceId: nodeInstanceId,
                gatheringSkillKey: gatheringSkillKey,
                resourceGrantAllowed: true,
                nodeDepletionAllowed: true,
                riskTriggered: false,
                triggeredRiskKey: null,
                failureReason: null);
        }

        // ----------------- Boundaries (helpers) -----------------

        private (GatheringOutcome outcome, string? failureReason) EvaluateToolPolicy(
            string nodeTypeKey,
            string gatheringSkillKey,
            ToolContext toolContext)
        {
            // Tool system absent => graceful no-op (Stage 7.2 tool logic is optional).
            if (!toolContext.HasToolSystem)
                return (GatheringOutcome.Success, null);

            ToolPolicy policy = _toolPolicy.GetToolPolicy(nodeTypeKey, gatheringSkillKey);

            if (policy.Kind == ToolPolicyKind.NotApplicable)
                return (GatheringOutcome.Success, null);

            // If a policy specifies a required tool class, compare logically.
            string requiredClass = policy.RequiredToolClassKey ?? string.Empty;
            string providedClass = toolContext.ToolClassKey ?? string.Empty;

            bool hasRequired = !string.IsNullOrEmpty(requiredClass) &&
                               string.Equals(requiredClass, providedClass, StringComparison.Ordinal);

            // If required tool class key is empty, policy is ill-defined; treat as hard fail
            // (don’t invent behavior; fail clearly).
            if ((policy.Kind == ToolPolicyKind.Required || policy.Kind == ToolPolicyKind.Recommended) &&
                string.IsNullOrEmpty(requiredClass))
            {
                return (GatheringOutcome.FailureHard, "tool_policy_invalid_missing_required_class");
            }

            if (policy.Kind == ToolPolicyKind.Required)
            {
                return hasRequired
                    ? (GatheringOutcome.Success, null)
                    : (GatheringOutcome.FailureHard, "missing_required_tool");
            }

            if (policy.Kind == ToolPolicyKind.Recommended)
            {
                return hasRequired
                    ? (GatheringOutcome.Success, null)
                    : (GatheringOutcome.FailureSoft, "missing_recommended_tool");
            }

            return (GatheringOutcome.Success, null);
        }

        private static bool ContainsString(IReadOnlyList<string> list, string value)
        {
            if (list == null) return false;
            for (int i = 0; i < list.Count; i++)
            {
                if (string.Equals(list[i], value, StringComparison.Ordinal))
                    return true;
            }
            return false;
        }

        private static GatheringResolutionResult HardFail(
            int playerId,
            int nodeInstanceId,
            string gatheringSkillKey,
            string failureReason)
        {
            return new GatheringResolutionResult(
                outcome: GatheringOutcome.FailureHard,
                playerId: playerId,
                nodeInstanceId: nodeInstanceId,
                gatheringSkillKey: gatheringSkillKey ?? string.Empty,
                resourceGrantAllowed: false,
                nodeDepletionAllowed: false,
                riskTriggered: false,
                triggeredRiskKey: null,
                failureReason: failureReason);
        }

        private static GatheringResolutionResult SoftFail(
            int playerId,
            int nodeInstanceId,
            string gatheringSkillKey,
            string failureReason)
        {
            return new GatheringResolutionResult(
                outcome: GatheringOutcome.FailureSoft,
                playerId: playerId,
                nodeInstanceId: nodeInstanceId,
                gatheringSkillKey: gatheringSkillKey ?? string.Empty,
                resourceGrantAllowed: false,
                nodeDepletionAllowed: false,
                riskTriggered: false,
                triggeredRiskKey: null,
                failureReason: failureReason);
        }
    }
}
