// File: Economy/Inventory/InventoryAndResourceGrantSystem.cs
// Stage 8.5.1 — Hardening pass (comments/guards only; no behavior changes)
//
// IMPORTANT EXECUTION CONTRACT
// - This system is SINGLE-THREADED.
// - It MUST be called only via the authoritative action-serialization queue.
// - Concurrent calls (including re-entrant calls via event handlers) are UNDEFINED BEHAVIOR.
// - No locks are used by design; serialization is the contract.

using System;
using System.Collections.Generic;
using Caelmor.Economy.Gathering;
using Caelmor.Economy.ResourceNodes;

namespace Caelmor.Economy.Inventory
{
    public sealed class InventoryAndResourceGrantSystem
    {
        private readonly IPlayerInventoryStore _inventory;
        private readonly INodeInstanceTypeResolver _nodeTypeResolver;
        private readonly IResourceGrantMapping _grantMapping;
        private readonly INodeRespawnTicksProvider _respawnTicksProvider;
        private readonly ResourceNodeRuntimeSystem _nodeRuntime;
        private readonly IResourceGrantEventSink _eventSink;
        private readonly IServerDiagnosticsSink _diagnostics;

        // _scratchDeltas is intentionally reused to avoid per-action allocations.
        // This is SAFE only because this system is single-threaded and non-re-entrant
        // under the action-serialization queue contract (see header).
        private readonly List<(string key, int delta)> _scratchDeltas = new List<(string key, int delta)>(8);

        public InventoryAndResourceGrantSystem(
            IPlayerInventoryStore inventory,
            INodeInstanceTypeResolver nodeTypeResolver,
            IResourceGrantMapping grantMapping,
            INodeRespawnTicksProvider respawnTicksProvider,
            ResourceNodeRuntimeSystem nodeRuntime,
            IResourceGrantEventSink eventSink,
            IServerDiagnosticsSink diagnostics)
        {
            _inventory = inventory ?? throw new ArgumentNullException(nameof(inventory));
            _nodeTypeResolver = nodeTypeResolver ?? throw new ArgumentNullException(nameof(nodeTypeResolver));
            _grantMapping = grantMapping ?? throw new ArgumentNullException(nameof(grantMapping));
            _respawnTicksProvider = respawnTicksProvider ?? throw new ArgumentNullException(nameof(respawnTicksProvider));
            _nodeRuntime = nodeRuntime ?? throw new ArgumentNullException(nameof(nodeRuntime));
            _eventSink = eventSink ?? throw new ArgumentNullException(nameof(eventSink));
            _diagnostics = diagnostics ?? throw new ArgumentNullException(nameof(diagnostics));
        }

        /// <summary>
        /// Processes a GatheringResolutionResult and applies inventory grant + node depletion atomically.
        ///
        /// EXECUTION CONTRACT:
        /// - Must be invoked ONLY from the authoritative action serialization queue.
        /// - This method is NOT thread-safe and NOT re-entrant.
        ///
        /// LIFECYCLE CONTRACT:
        /// - PlayerSessionManager must mark inventory writable before this is called.
        /// - If inventory is not writable, this indicates a lifecycle/ordering error (not a gameplay failure).
        /// </summary>
        public GrantProcessResult ProcessGatheringResult(int playerId, GatheringResolutionResult result)
        {
            // Validate caller consistency.
            if (playerId != result.PlayerId)
                return Fail("player_id_mismatch");

            // Inventory writability is a session lifecycle contract.
            // If this fails, higher-level systems should investigate PlayerSessionManager ordering.
            if (!_inventory.IsInventoryWritable(playerId))
            {
                EmitDiag(
                    "InventoryNotWritable",
                    $"Inventory not writable for PlayerId={playerId}. This is a session lifecycle error (PlayerSessionManager ordering), not gameplay.");
                return Fail("inventory_not_writable");
            }

            // 1) Confirm grant allowed.
            if (!result.ResourceGrantAllowed)
                return GrantProcessResult.NoOp("resource_grant_not_allowed");

            // 2) Determine node type for mapping.
            if (!_nodeTypeResolver.TryGetNodeTypeKey(result.NodeInstanceId, out var nodeTypeKey) ||
                string.IsNullOrWhiteSpace(nodeTypeKey))
            {
                EmitDiag("MissingNodeType",
                    $"No node type for NodeInstanceId={result.NodeInstanceId}, PlayerId={playerId}");
                return Fail("node_type_missing");
            }

            // 2) Determine grants (node type + skill key).
            if (!_grantMapping.TryResolve(nodeTypeKey, result.GatheringSkillKey, out var grants) || grants.Count == 0)
            {
                // Missing mapping is allowed to be NoOp, but must never be silent.
                EmitDiag("MissingResourceGrantMapping",
                    $"No mapping for NodeTypeKey='{nodeTypeKey}', SkillKey='{result.GatheringSkillKey}', NodeInstanceId={result.NodeInstanceId}, PlayerId={playerId}");
                return GrantProcessResult.NoOp("missing_resource_grant_mapping");
            }

            // 3) Apply inventory mutation atomically.
            // _scratchDeltas reuse is safe under the serialization/non-reentrancy contract.
            _scratchDeltas.Clear();
            for (int i = 0; i < grants.Count; i++)
            {
                var g = grants[i];
                _scratchDeltas.Add((g.ResourceItemKey, g.Count)); // positive delta adds
            }

            if (!_inventory.TryApplyDeltasAtomic(playerId, _scratchDeltas, out var invFail))
            {
                EmitDiag("InventoryGrantFailed",
                    $"Inventory mutation failed. Reason='{invFail}', PlayerId={playerId}, NodeInstanceId={result.NodeInstanceId}");
                return Fail(invFail ?? "inventory_grant_failed");
            }

            // 4) If and only if inventory mutation succeeded, attempt depletion if allowed.
            //
            // Node depletion may fail if another serialized action depleted the node after resolution but before grant.
            // In that case, rollback is INTENTIONAL and REQUIRED to prevent partial application.
            // This is why resolution + grant must be serialized; it is not a bug.
            if (result.NodeDepletionAllowed)
            {
                int respawnTicksRemaining = _respawnTicksProvider.GetRespawnTicksRemaining(nodeTypeKey);
                if (respawnTicksRemaining <= 0)
                {
                    RollbackInventoryOrThrow(playerId, grants,
                        context: $"Invalid respawn ticks from provider for NodeTypeKey='{nodeTypeKey}'.");
                    EmitDiag("InvalidRespawnTicks",
                        $"Respawn ticks provider returned <=0 for NodeTypeKey='{nodeTypeKey}'. PlayerId={playerId}, NodeInstanceId={result.NodeInstanceId}");
                    return Fail("invalid_respawn_ticks");
                }

                bool depleted = _nodeRuntime.TryDepleteNode(result.NodeInstanceId, respawnTicksRemaining);
                if (!depleted)
                {
                    // Roll back inventory to enforce atomicity across inventory + node state.
                    RollbackInventoryOrThrow(playerId, grants,
                        context: $"Node depletion failed for NodeInstanceId={result.NodeInstanceId} after inventory grant.");
                    EmitDiag("NodeDepleteFailed",
                        $"Node depletion failed after inventory mutation; rolled back. PlayerId={playerId}, NodeInstanceId={result.NodeInstanceId}");
                    return Fail("node_depletion_failed");
                }
            }

            // 5) Emit informational event.
            // WARNING: Event sinks must not call back into this system (no re-entrancy).
            _eventSink.Emit(new ResourceGrantedEvent(
                playerId: playerId,
                sourceNodeInstanceId: result.NodeInstanceId,
                grants: grants));

            return GrantProcessResult.Applied;
        }

        private void RollbackInventoryOrThrow(int playerId, IReadOnlyList<ResourceGrant> grants, string context)
        {
            _scratchDeltas.Clear();
            for (int i = 0; i < grants.Count; i++)
            {
                var g = grants[i];
                _scratchDeltas.Add((g.ResourceItemKey, -g.Count)); // negative delta subtracts
            }

            if (!_inventory.TryApplyDeltasAtomic(playerId, _scratchDeltas, out var rollbackFail))
            {
                // FATAL INVARIANT BREACH:
                // At this point we have observed a partial application that cannot be repaired in-process.
                // Higher-level systems are expected to catch/log/quarantine (e.g., disconnect player, halt zone, etc.).
                throw new InvalidOperationException(
                    $"FATAL invariant breach: rollback failed after partial economy mutation. " +
                    $"This indicates a severe lifecycle/concurrency/storage defect. " +
                    $"Context='{context}', PlayerId={playerId}, RollbackFailReason='{rollbackFail}'.");
            }
        }

        private GrantProcessResult Fail(string reason) => GrantProcessResult.Failed(reason);

        private void EmitDiag(string code, string message) => _diagnostics.Emit(code, message);
    }
}
