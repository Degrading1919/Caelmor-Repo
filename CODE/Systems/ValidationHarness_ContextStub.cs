using System;
using System.Collections.Generic;
using Caelmor.Economy.Inventory;
using Caelmor.Economy.ResourceNodes;

namespace Caelmor.Systems
{
    /// <summary>
    /// Stage 9.2: A minimal scenario context implementation that adapts to existing systems.
    /// This is scaffolding only; it does not modify gameplay behavior.
    ///
    /// IMPORTANT:
    /// - EnqueueSerializedAction MUST enqueue into your existing action serialization queue.
    /// - State capture MUST be read-only and must not emit gameplay events.
    /// - Save/Restore invokers MUST call existing persistence wiring (Stage 8.7).
    /// </summary>
    public sealed class ValidationScenarioContext : IScenarioContext
    {
        public IAuthoritativeTickSource TickSource { get; }
        public IAuthoritativeStateCapture State { get; }
        public ISaveCheckpointInvoker Save { get; }
        public IRestoreInvoker Restore { get; }
        public IValidationLogger Log { get; }

        private readonly Action<string, Action> _enqueueSerializedAction;

        public ValidationScenarioContext(
            IAuthoritativeTickSource tickSource,
            IAuthoritativeStateCapture stateCapture,
            ISaveCheckpointInvoker saveInvoker,
            IRestoreInvoker restoreInvoker,
            IValidationLogger logger,
            Action<string, Action> enqueueSerializedAction)
        {
            TickSource = tickSource ?? throw new ArgumentNullException(nameof(tickSource));
            State = stateCapture ?? throw new ArgumentNullException(nameof(stateCapture));
            Save = saveInvoker ?? throw new ArgumentNullException(nameof(saveInvoker));
            Restore = restoreInvoker ?? throw new ArgumentNullException(nameof(restoreInvoker));
            Log = logger ?? throw new ArgumentNullException(nameof(logger));

            _enqueueSerializedAction = enqueueSerializedAction ?? throw new ArgumentNullException(nameof(enqueueSerializedAction));
        }

        public void EnqueueSerializedAction(string actionLabel, Action action)
        {
            // Determinism requirement: all scenario actions must pass through the same serialized action path as gameplay.
            _enqueueSerializedAction(actionLabel ?? "validation_action", action ?? throw new ArgumentNullException(nameof(action)));
        }
    }

    /// <summary>
    /// Stage 9.2: Minimal read-only state capture adapter.
    /// Implemented against existing runtime systems without modifying them.
    /// </summary>
    public sealed class AuthoritativeStateCapture : IAuthoritativeStateCapture
    {
        private readonly SimplePlayerInventoryStore _inventory;          // Stage 8.5 store (authoritative)
        private readonly ResourceNodeRuntimeSystem _nodeRuntime;          // Stage 8.3 runtime

        // Scratch reused; safe because harness is single-threaded/tick-driven.
        private readonly List<(string key, int count)> _scratchInv = new List<(string key, int count)>(64);

        public AuthoritativeStateCapture(SimplePlayerInventoryStore inventory, ResourceNodeRuntimeSystem nodeRuntime)
        {
            _inventory = inventory ?? throw new ArgumentNullException(nameof(inventory));
            _nodeRuntime = nodeRuntime ?? throw new ArgumentNullException(nameof(nodeRuntime));
        }

        public InventorySnapshot CaptureInventory(int playerId)
        {
            _scratchInv.Clear();

            foreach (var kv in _inventory.DebugEnumerate(playerId))
                _scratchInv.Add((kv.Key, kv.Value));

            return new InventorySnapshot(playerId, _scratchInv.ToArray());
        }

        public NodeSnapshot CaptureNode(int nodeInstanceId)
        {
            bool exists = _nodeRuntime.TryGetNodeAvailability(nodeInstanceId, out var availability);
            if (!exists)
                return new NodeSnapshot(nodeInstanceId, exists: false, available: false, respawnTicksRemaining: 0);

            // Stage 8.3 does not expose ticks remaining directly via query API.
            // For validation, we rely on save snapshot visibility (which includes ticks-remaining for depleted nodes).
            // Scenarios that need exact ticks remaining should compare via WorldSave snapshot in Stage 9.3.
            bool available = (availability == ResourceNodeAvailability.Available);
            return new NodeSnapshot(nodeInstanceId, exists: true, available: available, respawnTicksRemaining: -1);
        }
    }
}
