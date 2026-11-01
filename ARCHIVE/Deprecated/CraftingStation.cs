// CraftingStation.cs
using System;
using System.Collections.Generic;
using UnityEngine;

namespace Caelmor.VS
{
    /// <summary>
    /// Core, non-MonoBehaviour logic for a server-authoritative crafting station.
    /// 
    /// Responsibilities:
    ///  - Recipe lookup by station type
    ///  - Validate skill level + ingredients
    ///  - Consume ingredients
    ///  - Award results + XP
    ///  - Expose hooks for animation / VFX / UI
    ///
    /// Notes:
    ///  - StationType examples: "forge", "campfire", "fletching_bench"
    ///  - InventorySystem performs actual item stack mutations
    ///  - SkillSystem integration is stubbed for VS
    /// </summary>
    public class CraftingStation
    {
        // --------------------------------------------------------------------
        // Station Identity
        // --------------------------------------------------------------------

        /// <summary>
        /// E.g.: "forge", "campfire", "fletching_bench"
        /// Must match recipe.station in recipe JSON.
        /// </summary>
        public string StationType { get; private set; }

        /// <summary>
        /// Each station has access to the world’s validated recipes.
        /// </summary>
        private readonly Dictionary<string, RecipeDefinition> _recipes;

        // --------------------------------------------------------------------
        // External references
        // --------------------------------------------------------------------

        public InventorySystem InventorySystem { get; set; }

        /// <summary>
        /// Stub: In full version, SkillSystem is responsible for applying XP
        /// and checking level restrictions. In VS we use a placeholder.
        /// </summary>
        public Func<Entity, string, int> GetSkillLevel; // (entity, skillName) => level
        public Action<Entity, string, int> AddSkillXP;   // (entity, skillName, xp)

        // --------------------------------------------------------------------
        // Internal Job Representation
        // --------------------------------------------------------------------

        private class CraftingJob
        {
            public Entity Crafter;
            public RecipeDefinition Recipe;
            public float TimeRemaining;
        }

        private readonly List<CraftingJob> _activeJobs = new List<CraftingJob>();

        // --------------------------------------------------------------------
        // Events (optional)
        // --------------------------------------------------------------------

        public event Action<Entity, RecipeDefinition> OnCraftStarted;
        public event Action<Entity, RecipeDefinition> OnCraftCompleted;
        public event Action<Entity, RecipeDefinition> OnCraftInterrupted;

        // --------------------------------------------------------------------
        // Constructor
        // --------------------------------------------------------------------

        public CraftingStation(string stationType, IEnumerable<RecipeDefinition> recipes)
        {
            StationType = stationType;
            _recipes = new Dictionary<string, RecipeDefinition>();

            foreach (var r in recipes)
            {
                if (r.station == stationType)
                    _recipes[r.id] = r;
            }
        }

        // --------------------------------------------------------------------
        // Public API: Find recipes available at this station
        // --------------------------------------------------------------------

        public IReadOnlyDictionary<string, RecipeDefinition> GetAvailableRecipes()
        {
            return _recipes;
        }

        public bool TryGetRecipe(string recipeId, out RecipeDefinition recipe)
        {
            return _recipes.TryGetValue(recipeId, out recipe);
        }

        // --------------------------------------------------------------------
        // Public API: Attempt to start crafting
        // --------------------------------------------------------------------

        public bool TryStartCrafting(Entity entity, string recipeId, out string reason)
        {
            reason = "success";

            if (entity == null)
            {
                reason = "entity_null";
                return false;
            }

            if (!TryGetRecipe(recipeId, out var recipe))
            {
                reason = "recipe_not_found";
                return false;
            }

            // Check skill requirement
            int level = GetSkillLevel?.Invoke(entity, recipe.skill) ?? 1;
            if (level < recipe.required_level)
            {
                reason = "skill_too_low";
                return false;
            }

            // Check inventory ingredients
            if (!InventorySystem.HasIngredients(entity, recipe.IngredientStructs))
            {
                reason = "missing_ingredients";
                return false;
            }

            // Consume ingredients now (server authoritative)
            if (!InventorySystem.ConsumeIngredients(entity, recipe.IngredientStructs))
            {
                reason = "consume_failed";
                return false;
            }

            // Start crafting job
            var job = new CraftingJob
            {
                Crafter = entity,
                Recipe = recipe,
                TimeRemaining = recipe.time
            };

            _activeJobs.Add(job);

            // Event hook — launching animation / SFX
            OnCraftStarted?.Invoke(entity, recipe);

            // TODO: Trigger crafting animation
            // TODO: Play SFX
            // TODO: Fire UI update events

            return true;
        }

        // --------------------------------------------------------------------
        // Tick / Update method called externally by TickManager or MonoBehaviour
        // --------------------------------------------------------------------

        public void Update(float deltaTime)
        {
            for (int i = _activeJobs.Count - 1; i >= 0; i--)
            {
                var job = _activeJobs[i];
                job.TimeRemaining -= deltaTime;

                if (job.TimeRemaining <= 0f)
                {
                    CompleteCraft(job);
                    _activeJobs.RemoveAt(i);
                }
            }
        }

        // --------------------------------------------------------------------
        // Internal: Completing a craft operation
        // --------------------------------------------------------------------

        private void CompleteCraft(CraftingJob job)
        {
            var entity = job.Crafter;
            var recipe = job.Recipe;

            if (entity == null)
                return;

            // Give result to inventory
            bool added = InventorySystem.TryAddItem(entity, recipe.result.item, recipe.result.qty, out int rem);
            if (!added || rem > 0)
            {
                // If inventory full, spill to world (VS stub)
                DropItemToWorld(entity, recipe.result.item, recipe.result.qty - rem);
            }

            // Award XP
            AddSkillXP?.Invoke(entity, recipe.skill, recipe.xp);

            // Event hook — SFX, UI flash, animation reset
            OnCraftCompleted?.Invoke(entity, recipe);

            // TODO: Stop crafting animation
            // TODO: Trigger VFX glow, spark, etc.
        }

        // --------------------------------------------------------------------
        // Interrupt job (if player moves, disconnects, or station invalidates)
        // --------------------------------------------------------------------

        public void InterruptAllCrafting(Entity entity)
        {
            for (int i = _activeJobs.Count - 1; i >= 0; i--)
            {
                if (_activeJobs[i].Crafter == entity)
                {
                    OnCraftInterrupted?.Invoke(entity, _activeJobs[i].Recipe);
                    // TODO: Stop animation
                    _activeJobs.RemoveAt(i);
                }
            }
        }

        // --------------------------------------------------------------------
        // Helpers (VS stubs)
        // --------------------------------------------------------------------

        private void DropItemToWorld(Entity entity, string itemId, int qty)
        {
            // Override in full game; no-op for VS.
            // Would spawn loot pickup at entity position.
        }
    }

    // ------------------------------------------------------------------------
    // RECIPE STRUCTURES (parsed from JSON)
    // ------------------------------------------------------------------------

    /// <summary>Matches VS_Recipes_Validated.json structure.</summary>
    [Serializable]
    public class RecipeDefinition
    {
        public string id;
        public string skill;
        public int required_level;
        public string station;
        public Ingredient[] ingredients;
        public Result result;
        public float time;
        public int xp;

        [Serializable]
        public class Ingredient
        {
            public string item;
            public int qty;
        }

        [Serializable]
        public class Result
        {
            public string item;
            public int qty;
        }

        // Converts JSON ingredients into InventorySystem.RecipeIngredient structs
        public IEnumerable<RecipeIngredient> IngredientStructs
        {
            get
            {
                foreach (var ing in ingredients)
                {
                    yield return new RecipeIngredient
                    {
                        ItemId = ing.item,
                        Quantity = ing.qty
                    };
                }
            }
        }
    }
}
