// File: Economy/Crafting/CraftingExecutionSystem.cs
//
// Stage 8.6 — Crafting Execution (Stage 7.4)
//
// IMPORTANT EXECUTION CONTRACT
// - Single-threaded.
// - Must be called only via the authoritative action serialization queue.
// - Concurrent calls (including re-entrancy) are undefined behavior.
// - No timers, no RNG, no persistence I/O.
//
// Atomicity rule:
// - Input consumption and output production MUST occur in ONE atomic inventory mutation.
// - If this is not possible, the craft MUST fail with inventory unchanged.
// :contentReference[oaicite:3]{index=3}

using System;
using System.Collections.Generic;
using Caelmor.Economy.Inventory;

namespace Caelmor.Economy.Crafting
{
    public sealed class CraftingExecutionSystem
    {
        private readonly IPlayerInventoryStore _inventory;
        private readonly IRecipeRepository _recipes;
        private readonly IPlayerRecipeKnowledge _recipeKnowledge;
        private readonly ICraftingStationContext _stations;
        private readonly IPlayerSkillFlags _skillFlags;
        private readonly ICraftingExecutionEventSink _eventSink;
        private readonly IServerDiagnosticsSink _diagnostics;

        // Reused scratch list; safe only under action-serialization single-threaded contract.
        private readonly List<(string key, int delta)> _scratchDeltas = new List<(string key, int delta)>(16);

        public CraftingExecutionSystem(
            IPlayerInventoryStore inventory,
            IRecipeRepository recipes,
            IPlayerRecipeKnowledge recipeKnowledge,
            ICraftingStationContext stations,
            IPlayerSkillFlags skillFlags,
            ICraftingExecutionEventSink eventSink,
            IServerDiagnosticsSink diagnostics)
        {
            _inventory = inventory ?? throw new ArgumentNullException(nameof(inventory));
            _recipes = recipes ?? throw new ArgumentNullException(nameof(recipes));
            _recipeKnowledge = recipeKnowledge ?? throw new ArgumentNullException(nameof(recipeKnowledge));
            _stations = stations ?? throw new ArgumentNullException(nameof(stations));
            _skillFlags = skillFlags ?? throw new ArgumentNullException(nameof(skillFlags));
            _eventSink = eventSink ?? throw new ArgumentNullException(nameof(eventSink));
            _diagnostics = diagnostics ?? throw new ArgumentNullException(nameof(diagnostics));
        }

        public CraftingExecutionResult ExecuteCraft(CraftingRequest request)
        {
            // Lifecycle contract: inventory must be writable before crafting.
            if (!_inventory.IsInventoryWritable(request.PlayerId))
            {
                EmitDiag("InventoryNotWritable",
                    $"Inventory not writable for PlayerId={request.PlayerId}. This is a session lifecycle error (PlayerSessionManager ordering), not gameplay.");
                return FailAndEmit(request, "inventory_not_writable");
            }

            // 1) Validate recipe exists.
            if (!_recipes.TryGetRecipe(request.RecipeKey, out var recipe))
            {
                return FailAndEmit(request, "recipe_missing");
            }

            // 2) Validate recipe known.
            if (!_recipeKnowledge.PlayerKnowsRecipe(request.PlayerId, request.RecipeKey))
            {
                return FailAndEmit(request, "recipe_not_known");
            }

            // 3) Validate station presence/usability and station requirement match.
            if (!_stations.IsStationUsable(request.PlayerId, request.CraftingStationKey, out var stationFail))
            {
                EmitDiag("StationUnusable",
                    $"Station unusable. PlayerId={request.PlayerId}, StationKey='{request.CraftingStationKey}', Reason='{stationFail}'.");
                return FailAndEmit(request, stationFail ?? "station_unusable");
            }

            // Required station type/key must match recipe requirement.
            if (!string.Equals(recipe.RequiredCraftingStationKey, request.CraftingStationKey, StringComparison.Ordinal))
            {
                return FailAndEmit(request, "wrong_station_type");
            }

            // 4) Validate skill requirements (boolean only).
            if (!string.IsNullOrWhiteSpace(recipe.RequiredSkillFlagKey))
            {
                if (!_skillFlags.PlayerHasSkillFlag(request.PlayerId, recipe.RequiredSkillFlagKey!))
                {
                    return FailAndEmit(request, "missing_required_skill");
                }
            }

            // 5) Prepare atomic inventory deltas: inputs negative, outputs positive.
            // This single delta list is the ONLY inventory mutation performed.
            _scratchDeltas.Clear();

            // Inputs (consume)
            var inputs = recipe.Inputs ?? Array.Empty<CraftItemDelta>();
            for (int i = 0; i < inputs.Count; i++)
            {
                var line = inputs[i];
                _scratchDeltas.Add((line.ResourceItemKey, -line.Count));
            }

            // Outputs (produce)
            var outputs = recipe.Outputs ?? Array.Empty<CraftItemDelta>();
            for (int i = 0; i < outputs.Count; i++)
            {
                var line = outputs[i];
                _scratchDeltas.Add((line.ResourceItemKey, line.Count));
            }

            // Guard: A recipe with no deltas is invalid at this stage; fail explicitly.
            if (_scratchDeltas.Count == 0)
            {
                EmitDiag("InvalidRecipeNoDeltas",
                    $"Recipe has no inputs/outputs. RecipeKey='{request.RecipeKey}'.");
                return FailAndEmit(request, "invalid_recipe_no_deltas");
            }

            // 6) Atomic mutation via inventory system (no partial consumption allowed).
            if (!_inventory.TryApplyDeltasAtomic(request.PlayerId, _scratchDeltas, out var invFail))
            {
                // Inventory layer is authoritative for “missing inputs” and mid-exec changes.
                // We translate to a Stage 7.4-aligned failure reason when possible.
                string reason = invFail switch
                {
                    "insufficient_items" => "missing_required_inputs",
                    _ => invFail ?? "inventory_atomic_failure"
                };

                EmitDiag("CraftInventoryAtomicFailed",
                    $"Craft atomic mutation failed. PlayerId={request.PlayerId}, RecipeKey='{request.RecipeKey}', Reason='{invFail}'.");
                return FailAndEmit(request, reason);
            }

            // Success result includes exact recipe lines as the “consumed/produced” report.
            var success = CraftingExecutionResult.Ok(
                playerId: request.PlayerId,
                recipeKey: request.RecipeKey,
                inputs: inputs,
                outputs: outputs);

            _eventSink.Emit(success);
            return success;
        }

        private CraftingExecutionResult FailAndEmit(CraftingRequest request, string reason)
        {
            var fail = CraftingExecutionResult.Fail(request.PlayerId, request.RecipeKey, reason);
            _eventSink.Emit(fail);
            return fail;
        }

        private void EmitDiag(string code, string message) => _diagnostics.Emit(code, message);
    }
}
