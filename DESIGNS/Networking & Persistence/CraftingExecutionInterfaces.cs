// File: Economy/Crafting/CraftingExecutionInterfaces.cs

using System;
using System.Collections.Generic;

namespace Caelmor.Economy.Crafting
{
    /// <summary>
    /// Minimal recipe definition surface required by Stage 7.4.
    /// This is NOT schema; it's a runtime view over canonical recipe data.
    /// </summary>
    public interface IRecipeDefinition
    {
        string RecipeKey { get; }

        /// <summary>Required station type/key for this recipe.</summary>
        string RequiredCraftingStationKey { get; }

        /// <summary>Optional boolean skill flag required to craft. Null/empty means none.</summary>
        string? RequiredSkillFlagKey { get; }

        IReadOnlyList<CraftItemDelta> Inputs { get; }
        IReadOnlyList<CraftItemDelta> Outputs { get; }
    }

    public interface IRecipeRepository
    {
        bool TryGetRecipe(string recipeKey, out IRecipeDefinition recipe);
    }

    /// <summary>
    /// Stage 7.4 requires "recipe is known by the player".
    /// This is a boolean check only.
    /// </summary>
    public interface IPlayerRecipeKnowledge
    {
        bool PlayerKnowsRecipe(int playerId, string recipeKey);
    }

    /// <summary>
    /// Boolean-only skill requirement check (no numeric tuning).
    /// </summary>
    public interface IPlayerSkillFlags
    {
        bool PlayerHasSkillFlag(int playerId, string skillFlagKey);
    }

    /// <summary>
    /// Station presence/usability query.
    /// No ownership rules at this stage.
    /// </summary>
    public interface ICraftingStationContext
    {
        bool IsStationUsable(int playerId, string craftingStationKey, out string? failureReason);
    }

    /// <summary>
    /// Informational event sink (no UI/networking/persistence here).
    /// </summary>
    public interface ICraftingExecutionEventSink
    {
        void Emit(CraftingExecutionResult evt);
    }

    public interface IServerDiagnosticsSink
    {
        void Emit(string code, string message);
    }
}
