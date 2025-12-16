// File: Economy/Inventory/InventoryInterfaces.cs

using System;
using System.Collections.Generic;

namespace Caelmor.Economy.Inventory
{
    /// <summary>
    /// Minimal authoritative inventory store.
    /// Keyed by ResourceItemKey with integer counts.
    /// Serializable by upstream persistence layer (not implemented here).
    /// </summary>
    public interface IPlayerInventoryStore
    {
        /// <summary>True only if the player's inventory is loaded/writable for this session.</summary>
        bool IsInventoryWritable(int playerId);

        /// <summary>
        /// Applies deltas atomically for a single player.
        /// Positive counts add; negative counts subtract.
        /// Must fail without mutation if it cannot apply.
        /// </summary>
        bool TryApplyDeltasAtomic(int playerId, IReadOnlyList<(string key, int delta)> deltas, out string? failureReason);
    }

    /// <summary>
    /// Resolves node instance id -> node type key (ResourceNode key) without mutating runtime.
    /// Source is world/zone placement content or an engine-owned registry.
    /// </summary>
    public interface INodeInstanceTypeResolver
    {
        bool TryGetNodeTypeKey(int nodeInstanceId, out string nodeTypeKey);
    }

    /// <summary>
    /// Placeholder resource mapping. Deterministic only.
    /// Must return stable ordering for multiple grants.
    /// </summary>
    public interface IResourceGrantMapping
    {
        bool TryResolve(string nodeTypeKey, string gatheringSkillKey, out IReadOnlyList<ResourceGrant> grants);
    }

    /// <summary>
    /// Respawn ticks are policy/tuning-provided upstream.
    /// This system never hardcodes respawn durations.
    /// </summary>
    public interface INodeRespawnTicksProvider
    {
        int GetRespawnTicksRemaining(string nodeTypeKey);
    }

    /// <summary>
    /// Server-side diagnostics sink (logs/event bus).
    /// Informational only.
    /// </summary>
    public interface IServerDiagnosticsSink
    {
        void Emit(string code, string message);
    }

    /// <summary>
    /// Informational event sink (no UI/networking here).
    /// </summary>
    public interface IResourceGrantEventSink
    {
        void Emit(ResourceGrantedEvent evt);
    }
}
