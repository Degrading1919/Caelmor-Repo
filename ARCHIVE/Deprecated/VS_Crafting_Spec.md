1. SYSTEM OVERVIEW

Crafting in the Vertical Slice uses a server-authoritative workflow:

Player interacts with crafting station

Server validates recipe, skill, items

Server starts a timed crafting job

TickManager decrements timers (10 Hz)

When finished → consume inputs, grant outputs, award XP

Notify client

Basic recipe flow examples:

Ore → Bar → Training Sword (Forge)

Logs → Shafts → Arrows (Fletching Bench)

Raw Meat → Cooked Meat (Campfire)

2. DATA STRUCTURES
2.1 Recipe Definition
struct RecipeDef:
    id: string
    skill: string               # e.g., smithing, fletching, cooking
    required_level: int
    station: string             # forge, fletching_bench, campfire
    ingredients: list<IngredientReq>
    result: { itemId, qty }
    time: float                 # seconds
    xp: int

2.2 Crafting Station Component
class CraftingStation:
    stationType: string              # "forge", "campfire", etc.
    activeJobs: list<CraftingJob>    # VS limits to one job per player

2.3 Crafting Job
struct CraftingJob:
    playerId: string
    recipeId: string
    recipe: RecipeDef
    timeRemaining: float
    state: enum { RUNNING, COMPLETED }

3. PLAYER INTERACTION FLOW
3.1 Client → Server
onPlayerPressCraft(recipeId, stationId):
    send CraftRequest { stationId, recipeId }

3.2 Server Validation
onServerReceive(CraftRequest req):

    station = World.FindStation(req.stationId)
    recipe  = RecipeDB[req.recipeId]
    player  = World.GetPlayer(req.playerId)

    if station.type != recipe.station:
        reject("WrongStation")

    if player.skills[recipe.skill].level < recipe.required_level:
        reject("SkillTooLow")

    if !Inventory.HasIngredients(player, recipe.ingredients):
        reject("MissingIngredients")

    station.activeJobs.add(
        CraftingJob(playerId = player.id,
                    recipeId = recipe.id,
                    recipe = recipe,
                    timeRemaining = recipe.time,
                    state = RUNNING)
    )

    notifyClient("CraftStarted", recipeId, recipe.time)

4. TICK INTEGRATION (SERVER)

Crafting progression occurs inside TickManager (10 Hz).

TickManager.RunTick():
    for each station:
        for each job in station.activeJobs:
            if job.state == RUNNING:
                job.timeRemaining -= TICK_INTERVAL
                if job.timeRemaining <= 0:
                    job.state = COMPLETED
                    CompleteCraftJob(station, job)

5. CRAFTING COMPLETION PIPELINE
5.1 CompleteCraftJob()
function CompleteCraftJob(station, job):

    player = World.GetPlayer(job.playerId)
    recipe = job.recipe

    # 1. Consume Inputs
    Inventory.Consume(player.inventory, recipe.ingredients)

    # 2. Grant Outputs
    Inventory.Add(player.inventory, recipe.result.itemId, recipe.result.qty)

    # 3. Award XP
    SkillSystem.AwardXp(player, recipe.skill, recipe.xp)

    # 4. Notify Client
    sendToClient(player.id,
        CraftCompleted { recipeId = recipe.id,
                         itemId = recipe.result.itemId,
                         qty = recipe.result.qty })

    # 5. Cleanup
    station.activeJobs.remove(job)

6. INVENTORY OPERATIONS
6.1 Ingredient Check
Inventory.HasIngredients(player, ingredients):
    for each ing in ingredients:
        if Inventory.Count(player, ing.item) < ing.qty:
            return false
    return true

6.2 Consume Ingredients
Inventory.Consume(inv, ingredients):
    for ing in ingredients:
        remove ing.qty of ing.item from inv

6.3 Add Output Items
Inventory.Add(inv, itemId, qty):
    if stackable:
        merge into existing stacks
        if overflow → new stack
    else:
        place single-item entries in free slots

7. CLIENT-SIDE VISUAL FLOW
onReceive CraftStarted:
    UI.ShowCraftingProgress(duration)

onReceive CraftCompleted:
    UI.UpdateInventory()
    UI.ShowToast("Crafted " + msg.itemId)

8. STATION RULESETS
8.1 Forge

Recipes: smelt_iron_bar, craft_training_sword

For metalworking progression

8.2 Fletching Bench

Recipes: craft_wooden_shaft, craft_training_arrows

8.3 Campfire

Recipe: cook_meat

9. ERROR CASES
reject("SkillTooLow") → send CraftFailed { reason = "SkillTooLow" }

reject("MissingIngredients") → send CraftFailed { reason = "MissingIngredients" }

reject("WrongStation") → send CraftFailed { reason = "WrongStation" }

reject("StationBusy") → send CraftFailed { reason = "StationBusy" }

10. CONSISTENCY & SECURITY

Server performs all validation

Client cannot spoof timers

Player cannot start multiple jobs at one station in VS

Output always produced after successful server-side crafting completion

11. EXTENSION PATHS (BEYOND VS)

Multi-slot concurrent crafting

Batch crafting

Station durability

Craft quality tiers

Profession specialization

NPC-assisted crafting queues