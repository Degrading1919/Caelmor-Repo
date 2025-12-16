// File: Economy/Crafting/CraftingExecutionTypes.cs

using System;
using System.Collections.Generic;

namespace Caelmor.Economy.Crafting
{
    public readonly struct CraftItemDelta
    {
        public readonly string ResourceItemKey;
        public readonly int Count;

        public CraftItemDelta(string resourceItemKey, int count)
        {
            if (string.IsNullOrWhiteSpace(resourceItemKey))
                throw new ArgumentException("ResourceItemKey must be non-empty.", nameof(resourceItemKey));
            if (count <= 0)
                throw new ArgumentOutOfRangeException(nameof(count), "Count must be > 0.");

            ResourceItemKey = resourceItemKey;
            Count = count;
        }
    }

    public readonly struct CraftingRequest
    {
        public readonly int PlayerId;
        public readonly string RecipeKey;
        public readonly string CraftingStationKey;

        public CraftingRequest(int playerId, string recipeKey, string craftingStationKey)
        {
            PlayerId = playerId;
            RecipeKey = recipeKey ?? throw new ArgumentNullException(nameof(recipeKey));
            CraftingStationKey = craftingStationKey ?? throw new ArgumentNullException(nameof(craftingStationKey));
        }
    }

    public readonly struct CraftingExecutionResult
    {
        public readonly int PlayerId;
        public readonly string RecipeKey;
        public readonly bool Success;

        public readonly IReadOnlyList<CraftItemDelta> InputsConsumed;
        public readonly IReadOnlyList<CraftItemDelta> OutputsProduced;

        public readonly string? FailureReason; // null on success

        public CraftingExecutionResult(
            int playerId,
            string recipeKey,
            bool success,
            IReadOnlyList<CraftItemDelta> inputsConsumed,
            IReadOnlyList<CraftItemDelta> outputsProduced,
            string? failureReason)
        {
            PlayerId = playerId;
            RecipeKey = recipeKey;
            Success = success;

            InputsConsumed = inputsConsumed ?? throw new ArgumentNullException(nameof(inputsConsumed));
            OutputsProduced = outputsProduced ?? throw new ArgumentNullException(nameof(outputsProduced));

            FailureReason = failureReason;
        }

        public static CraftingExecutionResult Fail(int playerId, string recipeKey, string reason) =>
            new CraftingExecutionResult(
                playerId, recipeKey, success: false,
                inputsConsumed: Array.Empty<CraftItemDelta>(),
                outputsProduced: Array.Empty<CraftItemDelta>(),
                failureReason: reason);

        public static CraftingExecutionResult Ok(int playerId, string recipeKey, IReadOnlyList<CraftItemDelta> inputs, IReadOnlyList<CraftItemDelta> outputs) =>
            new CraftingExecutionResult(playerId, recipeKey, success: true, inputs, outputs, failureReason: null);
    }
}
