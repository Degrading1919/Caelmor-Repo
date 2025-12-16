# Stage 7.4 — Crafting Execution System  
**Design Reference Document**

---

## 1. Overview

The **Crafting Execution System** is a server-authoritative, deterministic runtime layer that executes crafting requests by:

- Validating a crafting request against canonical recipe and station definitions
- Atomically consuming required input items from player inventory
- Producing recipe-defined outputs into player inventory
- Emitting an informational result event describing what happened

This system operates:
- **After** inventory integration (Stage 7.3)
- **Before** persistence, UI, economy balancing, or crafting timers

All schemas are canonical and immutable.  
This system does not modify schemas and does not introduce probability, time, or quality.

---

## 2. Core Responsibilities

### Craft Validation
On each craft attempt, validate:

- **Recipe exists**
- **Recipe is known by the player**
- **Required crafting station** is present and usable
- Player inventory contains all required inputs (by key + form)
- Crafting skill requirements are satisfied (**boolean-only**; no numeric tuning)

No RNG, no timers, no quality tiers.

### Input Consumption
- Inputs must be deducted **atomically**
- If inventory changes mid-execution, the craft must fail safely with:
  - no partial consumption
  - no outputs produced

### Output Production
- Insert outputs exactly as specified by recipe
- No bonus yields
- No alternative outcomes

### Event Emission
Emit a `CraftingExecutionResult` containing:
- `player_id`
- `recipe_key`
- `success`
- `inputs_consumed`
- `outputs_produced`
- `failure_reason` (if any)

The event is informational only.

---

## 3. Craft Validation Flow

Validation is structured into ordered gates so failure is explicit and diagnosable:

1. **Recipe Lookup**
   - Reject if recipe key unknown / missing

2. **Recipe Known**
   - Reject if player has not learned/known the recipe

3. **Station Presence & Usability**
   - Validate required station type from recipe
   - Validate station instance is present and usable
   - (No station ownership rules at this stage)

4. **Skill Requirements (Boolean)**
   - Validate player has the required skill flag(s)
   - No numeric levels or tuning
   - Missing skill → fail

5. **Inventory Has Inputs**
   - Validate player inventory contains all required items
   - Inputs must match by key and required form identity (if applicable)

Only after all validation gates pass does execution proceed.

---

## 4. Inventory Mutation Strategy (Atomicity)

Crafting requires **atomic mutation** to prevent partial state updates.

### Desired Properties
- Either all inputs are consumed and all outputs granted, or nothing changes
- Safe against concurrent inventory updates (e.g., grants, other crafts)

### Strategy (Conceptual)
Use an inventory transaction / lock approach:

- Begin an inventory transaction for the player
- Re-check required inputs within the transaction scope
- Apply all input deductions
- Apply all output additions
- Commit transaction
- If any step fails → rollback (no state changes)

This system does not define the underlying inventory implementation; it requires the inventory layer to provide an atomic mutation primitive.

---

## 5. Conceptual C# Structures (Illustrative Only)

> **Illustrative only** — these examples are not production code and do not define schemas.

### Input/Output Line Items

```csharp
struct ItemDelta
{
    string ResourceItemKey;
    int Count;
}

Craft Request
struct CraftingRequest
{
    int PlayerId;
    string RecipeKey;
    int StationInstanceId; // specific station in-world the player is using
}

Craft Result Event
struct CraftingExecutionResult
{
    int PlayerId;
    string RecipeKey;
    bool Success;

    List<ItemDelta> InputsConsumed;
    List<ItemDelta> OutputsProduced;

    string FailureReason; // null/empty if Success == true
}

Inventory Transaction Boundary (Conceptual)
interface IInventoryAtomicMutator
{
    bool TryExecuteAtomic(
        int playerId,
        List<ItemDelta> requiredInputs,
        List<ItemDelta> outputs,
        out string failureReason
    );
}

6. Pseudocode for Craft Execution
ExecuteCraft(request):

  // 1) Lookup recipe
  recipe = RecipeRepo.Get(request.RecipeKey)
  if recipe missing:
      EmitResult(Fail("recipe_missing"))
      return

  // 2) Validate recipe known
  if PlayerRecipeBook.Knows(request.PlayerId, request.RecipeKey) == false:
      EmitResult(Fail("recipe_not_known"))
      return

  // 3) Validate station usable
  station = StationSystem.Get(request.StationInstanceId)
  if station missing:
      EmitResult(Fail("station_missing"))
      return

  if station.IsUsable == false:
      EmitResult(Fail("station_unusable"))
      return

  if station.TypeKey != recipe.RequiredStationTypeKey:
      EmitResult(Fail("wrong_station_type"))
      return

  // 4) Validate skill requirements (boolean only)
  if recipe.RequiresSkillKey exists AND PlayerSkills.HasSkillFlag(request.PlayerId, recipe.RequiresSkillKey) == false:
      EmitResult(Fail("missing_required_skill"))
      return

  // 5) Prepare required inputs/outputs
  requiredInputs = recipe.Inputs (key + count, form identity if applicable)
  outputs = recipe.Outputs (key + count)

  // 6) Atomic inventory execution
  success = Inventory.TryExecuteAtomic(
                playerId = request.PlayerId,
                requiredInputs = requiredInputs,
                outputs = outputs,
                failureReason = out reason)

  if success == false:
      EmitResult(Fail(reason, inputsConsumed = [], outputsProduced = []))
      return

  // 7) Emit success result
  EmitResult(Success(
      inputsConsumed = requiredInputs,
      outputsProduced = outputs))


Notes:
Inventory is the authority for whether the mutation succeeds
No partial consumption is permitted
No RNG or timers exist in this stage

7. Failure Modes & Diagnostics
Crafting failures must be explicit and diagnosable. Minimum failure reasons include:
recipe_missing
recipe_not_known
station_missing
station_unusable
wrong_station_type
missing_required_skill
missing_required_inputs
inventory_changed_mid_execution (or equivalent atomic failure)
invalid_request (malformed payload)

Diagnostics Requirement
On failure, the system should emit:
The CraftingExecutionResult with success = false and failure_reason
A server-side diagnostic log entry for investigation (especially for missing mappings or invalid requests)
No client/UI behavior is defined here.

8. Extension Points (Not Implemented)
Crafting Timers / Progress
Future systems may introduce crafting time, queues, interruption
Stage 7.4 remains the authoritative execution path

Quality / RNG
Future: quality tiers, proc chances, bonus yields
Not permitted in current stage

Station Ownership / Permissions
Future: station ownership, access permissions, fuel, degradation
Not part of current scope

Skill Levels & XP
Future: numeric level checks, XP grants, progression gating
Not part of current scope

Persistence
Future: saving inventory deltas and recipe knowledge
Not part of current scope

Networking / UI
Future: replicate crafting results and inventory deltas to client
Not part of current scope

9. Non-Goals
This system explicitly does not handle:
Crafting timers
UI hooks or client sync logic
Quality rolls or RNG
Station ownership, fuel, or durability
Skill XP
Persistence logic
Economy balancing