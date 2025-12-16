// File: Economy/Gathering/GatheringResolutionInterfaces.cs

using System;
using System.Collections.Generic;

namespace Caelmor.Economy.Gathering
{
    public enum NodeAvailability : byte
    {
        Available = 0,
        Depleted = 1
    }

    /// <summary>
    /// A small query surface that composes:
    /// - Stage 8.3 ResourceNodeRuntimeSystem facts (existence + availability + node type key)
    /// - Canonical ResourceNode definition facts (allowed skills, risk flags)
    ///
    /// This adapter prevents Stage 8.4 from reaching into runtime internals or schemas directly.
    /// </summary>
    public interface IGatheringNodeQuery
    {
        bool TryGetNodeContext(
            int nodeInstanceId,
            out string nodeTypeKey,
            out NodeAvailability availability,
            out IReadOnlyList<string> allowedGatheringSkills,
            out IReadOnlyList<string> nodeRiskFlags);
    }

    /// <summary>
    /// Skill possession check (boolean only).
    /// No numeric levels in Stage 7.2.
    /// </summary>
    public interface IPlayerGatheringSkillProvider
    {
        bool PlayerHasGatheringSkill(int playerId, string gatheringSkillKey);
    }

    public enum ToolPolicyKind : byte
    {
        NotApplicable = 0,
        Recommended = 1,
        Required = 2
    }

    public readonly struct ToolPolicy
    {
        public readonly ToolPolicyKind Kind;
        public readonly string? RequiredToolClassKey; // only meaningful for Recommended/Required

        public ToolPolicy(ToolPolicyKind kind, string? requiredToolClassKey)
        {
            Kind = kind;
            RequiredToolClassKey = requiredToolClassKey;
        }

        public static ToolPolicy NotApplicable => new ToolPolicy(ToolPolicyKind.NotApplicable, null);
    }

    /// <summary>
    /// Tool handling is policy-level and optional (Stage 7.2).
    /// Implementations must gracefully handle absence of a tool system.
    /// </summary>
    public interface IGatheringToolPolicyProvider
    {
        ToolPolicy GetToolPolicy(string nodeTypeKey, string gatheringSkillKey);
    }

    /// <summary>
    /// Deterministic risk trigger policy.
    /// Stage 7.2 requires risk surfacing but defines no triggering rules;
    /// therefore, triggering is delegated to an explicit policy.
    /// </summary>
    public interface IGatheringRiskPolicy
    {
        /// <returns>
        /// A triggered risk key (must be one of nodeRiskFlags) or null if no risk is triggered.
        /// Deterministic only.
        /// </returns>
        string? DetermineTriggeredRisk(
            int playerId,
            int nodeInstanceId,
            string nodeTypeKey,
            string gatheringSkillKey,
            IReadOnlyList<string> nodeRiskFlags,
            ToolContext toolContext);
    }

    /// <summary>
    /// Safe default: never triggers risk (deterministic).
    /// </summary>
    public sealed class NoRiskPolicy : IGatheringRiskPolicy
    {
        public static readonly NoRiskPolicy Instance = new NoRiskPolicy();
        private NoRiskPolicy() { }

        public string? DetermineTriggeredRisk(
            int playerId,
            int nodeInstanceId,
            string nodeTypeKey,
            string gatheringSkillKey,
            IReadOnlyList<string> nodeRiskFlags,
            ToolContext toolContext)
        {
            return null;
        }
    }

    /// <summary>
    /// Safe default: tools irrelevant unless another system provides policy.
    /// </summary>
    public sealed class NoToolPolicyProvider : IGatheringToolPolicyProvider
    {
        public static readonly NoToolPolicyProvider Instance = new NoToolPolicyProvider();
        private NoToolPolicyProvider() { }

        public ToolPolicy GetToolPolicy(string nodeTypeKey, string gatheringSkillKey)
        {
            return ToolPolicy.NotApplicable;
        }
    }
}
