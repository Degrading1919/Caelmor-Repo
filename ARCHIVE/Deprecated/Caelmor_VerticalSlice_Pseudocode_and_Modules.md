# Caelmor — Vertical Slice Pseudocode & Module Diagrams
Version: v1.0 (Derived from Vertical Slice Technical Specification)
Role: Engine-Agnostic Coding Assistant

---

## 1. High-Level Module Overview

### 1.1 Core Modules (Vertical Slice Scope)

- `GameManager`
- `NetworkManager`
- `TickManager`
- `WorldManager`
- `ZoneManager`
- `EntitySystem`
- `AIController`
- `CombatSystem`
- `StatsSystem`
- `SkillSystem`
- `InventorySystem`
- `EquipmentSystem`
- `CraftingSystem`
- `SaveSystem`
- `UIManager`

### 1.2 Text Module Diagram

Top-level orchestration:

```text
               ┌─────────────────┐
               │   GameManager   │
               └────────┬────────┘
                        │
        ┌───────────────┼─────────────────┐
        │               │                 │
┌───────▼───────┐ ┌─────▼─────────┐ ┌─────▼─────┐
│ NetworkManager│ │   TickManager  │ │ UIManager │
└───────┬───────┘ └─────┬─────────┘ └─────┬─────┘
        │               │                 │
        │      ┌────────▼─────────┐       │
        │      │   WorldManager   │       │
        │      └────────┬─────────┘       │
        │               │                 │
        │        ┌──────▼───────┐         │
        │        │ ZoneManager  │         │
        │        └──────┬───────┘         │
        │               │                 │
        │       ┌───────▼─────────┐       │
        │       │  EntitySystem   │◄──────┘ (UI reads entity state)
        │       └──────┬──────────┘
        │              │
        │   ┌──────────┼───────────────────────────────┐
        │   │          │                               │
┌───────▼──────┐ ┌─────▼────────┐ ┌────────▼────────┐ ┌──────────▼──────────┐
│ CombatSystem │ │ StatsSystem  │ │ InventorySystem │ │   SkillSystem       │
└───────┬──────┘ └─────┬────────┘ └────────┬────────┘ └──────────┬──────────┘
        │              │                  │                     │
        │              │                  │                     │
        │      ┌───────▼────────┐  ┌──────▼─────────┐   ┌───────▼─────────┐
        │      │ EquipmentSystem│  │ CraftingSystem │   │    SaveSystem    │
        │      └────────────────┘  └───────────────┘   └──────────────────┘
        │
        └── NetworkManager syncs state to/from clients
2. GameManager & Boot Sequence
2.1 GameManager Responsibilities
Initialize core systems in correct order.

Distinguish host vs client mode.

Delegate to NetworkManager and TickManager.

Handle zone loading bootstrap.

2.2 Pseudocode — GameManager
pseudo
Copy code
class GameManager:
    static instance: GameManager

    networkManager: NetworkManager
    tickManager: TickManager
    worldManager: WorldManager
    uiManager: UIManager
    saveSystem: SaveSystem
    isHost: bool

    method Init(mode: HostOrClient):
        GameManager.instance = this

        // 1) Initialize persistence & data
        saveSystem = new SaveSystem()
        ContentDatabase.LoadAll() // Items, Skills, Recipes, Enemies, Zones

        // 2) Initialize world + tick
        worldManager = new WorldManager()
        tickManager = new TickManager()

        // 3) Initialize networking (host/client)
        networkManager = new NetworkManager()
        networkManager.Init(mode)

        isHost = (mode == Host)

        if isHost:
            // host loads world save and starts listening
            saveSystem.LoadWorldOrCreateDefault()
            networkManager.StartHost()
            tickManager.StartAuthoritativeLoop()
        else:
            // client connects to host
            networkManager.StartClient(connectAddress)

        // 4) Initialize UI
        uiManager = new UIManager()
        uiManager.Init()

    method OnClientConnected(connectionId):
        if isHost:
            // Load or create PlayerSave
            playerSave = saveSystem.LoadPlayerOrCreateDefault(connectionId)
            // Spawn entity
            playerEntity = worldManager.SpawnPlayerFromSave(playerSave)
            // Send initial snapshots
            networkManager.SendInitialWorldSnapshot(connectionId, saveSystem.worldState)
            networkManager.SendInitialPlayerSnapshot(connectionId, playerSave)

    method OnHostShutdown():
        if isHost:
            saveSystem.SaveAllConnectedPlayers()
            saveSystem.SaveWorld()
3. TickManager — Authoritative 10 Hz Loop
3.1 Responsibilities
Run authoritative tick on host only.

Invoke simulation steps in consistent order.

Trigger periodic autosaves via SaveSystem.

3.2 Pseudocode — TickManager (Host)
ps
Copy code
class TickManager:
    const TICK_INTERVAL_SECONDS = 0.1
    tickIndex: long = 0
    accumulator: float = 0.0
    isRunning: bool = false

    // References
    worldManager: WorldManager
    combatSystem: CombatSystem
    statsSystem: StatsSystem
    skillSystem: SkillSystem
    craftingSystem: CraftingSystem
    saveSystem: SaveSystem
    networkManager: NetworkManager

    // Autosave config
    autosaveIntervalSeconds: float = 300.0  // 5 minutes
    timeSinceLastAutosave: float = 0.0

    method StartAuthoritativeLoop():
        isRunning = true

    method Update(deltaTime: float):  // called from engine main loop
        if not isRunning: return
        accumulator += deltaTime
        timeSinceLastAutosave += deltaTime

        while accumulator >= TICK_INTERVAL_SECONDS:
            accumulator -= TICK_INTERVAL_SECONDS
            RunTick()

        if timeSinceLastAutosave >= autosaveIntervalSeconds:
            saveSystem.SaveWorld()
            saveSystem.SaveAllConnectedPlayers()
            timeSinceLastAutosave = 0.0

    method RunTick():
        tickIndex += 1

        // 1. Collect inputs from NetworkManager
        inputs = networkManager.DrainBufferedInputs()

        // 2. Validate & apply movement
        worldManager.ApplyPlayerMovementInputs(inputs.movementCommands)

        // 3. AI Decisions
        worldManager.UpdateAIControllers(tickIndex)

        // 4. Combat timers & resolution
        combatSystem.ProcessAttackTimersAndIntents(tickIndex, inputs.attackCommands)

        // 5. Apply damage & deaths
        combatSystem.ApplyPendingDamage(statsSystem, skillSystem)

        // 6. World state updates (nodes, crafting jobs, flags)
        worldManager.UpdateWorldState(tickIndex)
        craftingSystem.ProcessCraftingJobs(tickIndex)

        // 7. Persistence hooks: set dirty flags
        saveSystem.MarkDirtyFromWorld(worldManager)
        saveSystem.MarkDirtyFromPlayers(worldManager.GetPlayerEntities())

        // 8. Build snapshot & sync
        snapshot = worldManager.BuildStateSnapshot()
        networkManager.BroadcastSnapshot(snapshot)
4. NetworkManager — Messages & Flow
4.1 Message Structs (Conceptual)
pseudo
Copy code
// Client → Host (Input)
struct PlayerInput_Move:
    playerId: string
    tickClientTimestamp: long
    direction: Vector2

struct PlayerInput_Attack:
    playerId: string
    targetEntityId: string
    isStart: bool
    optional abilityId: string? // null for auto-attack

struct PlayerInput_Interact:
    playerId: string
    targetObjectId: string
    interactionType: enum { Loot, CraftStation, Node, Chest }

struct PlayerInput_InventoryAction:
    playerId: string
    actionType: enum { Move, Equip, Unequip, Split, Drop }
    sourceSlot: int
    destSlot: int
    optional quantity: int

struct PlayerInput_CraftRequest:
    playerId: string
    stationId: string
    recipeId: string
    quantity: int

// Host → Clients (State & Events)
struct Snapshot_Transforms:
    tickIndex: long
    transforms: list<TransformSnapshot>

struct TransformSnapshot:
    entityId: string
    position: Vector3
    rotationY: float

struct Event_CombatResult:
    tickIndex: long
    sourceEntityId: string
    targetEntityId: string
    damage: int
    newHp: int
    isKill: bool
    isCrit: bool

struct Event_InventoryChanged:
    playerId: string
    inventorySlots: list<InventorySlotState>
    equipmentSlots: dict<string, string?> // slotName -> itemId

struct Event_CraftingResult:
    playerId: string
    success: bool
    recipeId: string
    quantity: int
    reasonCode: CraftFailReason
    grantedItems: list<ItemStack>
    xpGained: int

struct Event_WorldObjectUpdate:
    objectId: string
    objectType: enum { ResourceNode, Chest, QuestObject }
    statePayload: any

struct Event_SkillXP:
    playerId: string
    skillId: string
    xpDelta: int
    newLevel: int
4.2 Pseudocode — NetworkManager (Host/Client)
pseudo
Copy code
class NetworkManager:
    isHost: bool
    tickManager: TickManager

    bufferedInputs: list<PlayerInputBase>

    method Init(mode: HostOrClient):
        isHost = (mode == Host)

    method StartHost():
        // Bind listen socket / start server
        // On new connection → GameManager.OnClientConnected

    method StartClient(address: string):
        // Connect to host at address
        // On receiving initial snapshots → spawn local entities, load zone

    // INPUT FLOW (host)
    method OnReceiveClientMessage(msg):
        if isHost:
            if msg is PlayerInputBase:
                bufferedInputs.add(msg)

    method DrainBufferedInputs() -> InputBatch:
        batch = new InputBatch()
        for msg in bufferedInputs:
            match msg.type:
                case Move: batch.movementCommands.add(msg)
                case Attack: batch.attackCommands.add(msg)
                case Interact: batch.interactCommands.add(msg)
                case InventoryAction: batch.inventoryCommands.add(msg)
                case CraftRequest: batch.craftRequests.add(msg)
        bufferedInputs.clear()
        return batch

    // SNAPSHOT FLOW (host)
    method BroadcastSnapshot(snapshot: WorldSnapshot):
        // Send transforms (UNRELIABLE)
        SendToAll(snapshot.transforms, unreliableChannel)

        // Send queued events (RELIABLE)
        for evt in snapshot.events:
            SendToTargets(evt, reliableChannel)

    // CLIENT-SIDE HANDLING
    method OnReceiveServerMessage(msg):
        if msg is Snapshot_Transforms:
            ClientWorld.ApplyTransformSnapshot(msg)
        else if msg is Event_CombatResult:
            ClientWorld.ApplyCombatEvent(msg)
        else if msg is Event_InventoryChanged:
            ClientWorld.ApplyInventoryChange(msg)
            UIManager.RefreshInventory(msg.playerId)
        else if msg is Event_CraftingResult:
            ClientWorld.ApplyCraftingResult(msg)
            UIManager.ShowCraftingResult(msg)
        else if msg is Event_WorldObjectUpdate:
            ClientWorld.UpdateWorldObject(msg)
        else if msg is Event_SkillXP:
            ClientWorld.UpdateSkillXP(msg)
            UIManager.RefreshSkills(msg.playerId)
5. EntitySystem & AIController
5.1 Entity Data Model
pseudo
Copy code
class Entity:
    entityId: string
    isPlayer: bool
    position: Vector3
    rotationY: float
    stats: StatsComponent
    combat: CombatComponent
    inventory: InventoryComponent?      // only for players
    equipment: EquipmentComponent?      // only for players
    skills: SkillComponent?            // players or special enemies
    ai: AIController?                  // enemies only
    // possibly other components
pseudo
Copy code
class StatsComponent:
    maxHp: int
    currentHp: int
    armorRating: int
    // other stats if needed
pseudo
Copy code
class CombatComponent:
    isAutoAttacking: bool
    targetId: string?
    weaponId: string?              // from equipment
    attackSpeedTicks: int
    nextAttackTick: long
    pendingDamageEvents: list<PendingDamage>
5.2 AIController Pseudocode (Simple)
pseudo
Copy code
class AIController:
    owner: Entity
    state: enum { Idle, Patrol, Chase, Attack, Return }
    leashCenter: Vector3
    leashRadius: float
    detectionRadius: float

    method UpdateAI(tickIndex: long, world: WorldManager):
        target = world.FindNearestPlayerInRadius(owner.position, detectionRadius)

        if target is null:
            // No player nearby
            if state == Chase or state == Attack:
                state = Return
            else if state == Return:
                MoveTowards(leashCenter)
                if Distance(owner.position, leashCenter) < smallThreshold:
                    state = Idle
            return

        // Player detected
        distance = Distance(owner.position, target.position)
        if distance > detectionRadius or distance > leashRadius:
            state = Return
            return

        if distance > owner.combat.attackRange:
            state = Chase
            MoveTowards(target.position)
        else:
            state = Attack
            owner.combat.isAutoAttacking = true
            owner.combat.targetId = target.entityId
WorldManager.UpdateAIControllers simply iterates all entities with ai and calls UpdateAI.

6. CombatSystem — Attack Timers & Resolution
6.1 API Surface
pseudo
Copy code
class CombatSystem:
    worldManager: WorldManager
    statsSystem: StatsSystem
    skillSystem: SkillSystem
    networkManager: NetworkManager

    method ProcessAttackTimersAndIntents(tickIndex: long, attackCommands: list<PlayerInput_Attack>):
        // 1) Apply new attack intents
        for cmd in attackCommands:
            entity = worldManager.GetEntity(cmd.playerId)
            if entity is null: continue

            if cmd.isStart:
                StartAutoAttackOrAbility(entity, cmd.targetEntityId, cmd.abilityId, tickIndex)
            else:
                StopAutoAttack(entity)

        // 2) For all entities with combat component, check timers
        for entity in worldManager.GetAllEntities():
            if not entity.combat: continue
            if entity.combat.isAutoAttacking and tickIndex >= entity.combat.nextAttackTick:
                TryResolveAttack(entity, tickIndex)

    method StartAutoAttackOrAbility(attacker: Entity, targetId: string, abilityId: string?, tickIndex: long):
        target = worldManager.GetEntity(targetId)
        if not ValidateTarget(attacker, target): return

        if abilityId is null:
            // basic auto-attack
            attacker.combat.isAutoAttacking = true
            attacker.combat.targetId = targetId
            attacker.combat.attackSpeedTicks = GetWeaponAttackSpeedTicks(attacker)
            attacker.combat.nextAttackTick = tickIndex + attacker.combat.attackSpeedTicks
        else:
            // special ability (windup)
            ScheduleSpecialAttack(attacker, targetId, abilityId, tickIndex)

    method StopAutoAttack(attacker: Entity):
        attacker.combat.isAutoAttacking = false
        attacker.combat.targetId = null

    method TryResolveAttack(attacker: Entity, tickIndex: long):
        target = worldManager.GetEntity(attacker.combat.targetId)
        if not ValidateTarget(attacker, target):
            attacker.combat.isAutoAttacking = false
            return

        if not InAttackRange(attacker, target):
            // Could choose to move closer or stop
            return

        // Compute hit/miss
        if not CheckHit(attacker, target):
            BroadcastMiss(attacker, target, tickIndex)
            attacker.combat.nextAttackTick += attacker.combat.attackSpeedTicks
            return

        // Compute damage
        damage = ComputeDamage(attacker, target)
        ApplyDamage(attacker, target, damage, tickIndex)

        // Schedule next attack
        attacker.combat.nextAttackTick += attacker.combat.attackSpeedTicks

    method ApplyDamage(attacker: Entity, target: Entity, damage: int, tickIndex: long):
        newHp = statsSystem.ApplyDamage(target, damage)
        isKill = (newHp <= 0)

        if isKill:
            HandleDeath(attacker, target)

        // Award XP
        xpAmount = GetXPValueForTarget(target)
        skillSystem.AwardXP(attacker, "melee", xpAmount)

        // Broadcast event
        evt = Event_CombatResult(
            tickIndex = tickIndex,
            sourceEntityId = attacker.entityId,
            targetEntityId = target.entityId,
            damage = damage,
            newHp = newHp,
            isKill = isKill,
            isCrit = false
        )
        networkManager.BroadcastEvent(evt)
6.2 StatsSystem Pseudocode
pseudo
Copy code
class StatsSystem:
    method ApplyDamage(target: Entity, damage: int) -> int:
        mitigated = max(0, damage - target.stats.armorRating)
        target.stats.currentHp = max(0, target.stats.currentHp - mitigated)
        return target.stats.currentHp
7. InventorySystem & EquipmentSystem
7.1 Data Structures
pseudo
Copy code
struct InventorySlot:
    slotIndex: int
    itemId: string | null
    quantity: int

class InventoryComponent:
    slots: array<InventorySlot>  // fixed size
pseudo
Copy code
class EquipmentComponent:
    slots: dict<string, string?>  // slotName -> itemId or null
    // e.g., "head", "chest", "legs", "weaponMain", "weaponOff"
7.2 InventorySystem Pseudocode
pseudo
Copy code
class InventorySystem:
    worldManager: WorldManager
    equipmentSystem: EquipmentSystem
    networkManager: NetworkManager

    method HandleInventoryCommands(commands: list<PlayerInput_InventoryAction>):
        for cmd in commands:
            player = worldManager.GetEntity(cmd.playerId)
            if player is null or not player.inventory: continue

            success = false

            switch cmd.actionType:
                case Move:
                    success = MoveItem(player.inventory, cmd.sourceSlot, cmd.destSlot)
                case Equip:
                    success = EquipItem(player, cmd.sourceSlot, cmd.destSlot) // destSlot is equipment slot name
                case Unequip:
                    success = UnequipItem(player, cmd.sourceSlot, cmd.destSlot) // source = equip slot, dest = inv slot
                case Split:
                    success = SplitStack(player.inventory, cmd.sourceSlot, cmd.destSlot, cmd.quantity)
                case Drop:
                    success = DropItemToWorld(player, cmd.sourceSlot, cmd.quantity)

            if success:
                // Recalculate equipment-derived stats if needed
                equipmentSystem.UpdateDerivedStats(player)
                // Mark dirty for persistence
                player.inventoryDirty = true
                player.equipmentDirty = true
                // Notify owner client
                SendInventoryUpdateToOwner(player)

    method MoveItem(inv: InventoryComponent, source: int, dest: int) -> bool:
        if not IsValidSlot(inv, source) or not IsValidSlot(inv, dest): return false
        // swap
        temp = inv.slots[source]
        inv.slots[source] = inv.slots[dest]
        inv.slots[dest] = temp
        return true

    method EquipItem(player: Entity, sourceSlotIndex: int, equipSlotName: string) -> bool:
        slot = player.inventory.slots[sourceSlotIndex]
        if slot.itemId is null: return false

        itemDef = ContentDatabase.Items[slot.itemId]
        if not itemDef.CanEquipTo(equipSlotName): return false

        // Move to equipment
        prevItemId = player.equipment.slots[equipSlotName]
        player.equipment.slots[equipSlotName] = slot.itemId

        // Remove from inventory
        slot.quantity -= 1
        if slot.quantity <= 0:
            slot.itemId = null

        // Optionally return previous item to inventory if exists
        if prevItemId is not null:
            AddItemToInventory(player.inventory, prevItemId, 1)

        return true

    method SendInventoryUpdateToOwner(player: Entity):
        evt = Event_InventoryChanged(
            playerId = player.entityId,
            inventorySlots = player.inventory.slots,
            equipmentSlots = player.equipment.slots
        )
        networkManager.SendToPlayer(player.entityId, evt)
7.3 EquipmentSystem Pseudocode
pseudo
Copy code
class EquipmentSystem:
    method UpdateDerivedStats(entity: Entity):
        baseStats = GetBaseStatsForEntity(entity)
        armorSum = 0
        weaponDamage = baseStats.weaponDamage

        for slotName, itemId in entity.equipment.slots:
            if itemId is null: continue
            itemDef = ContentDatabase.Items[itemId]
            armorSum += itemDef.armorBonus
            if slotName == "weaponMain":
                weaponDamage = itemDef.weaponDamage

        entity.stats.armorRating = baseStats.armorRating + armorSum
        entity.combat.attackDamage = weaponDamage
8. CraftingSystem — Immediate Crafting
8.1 Core Flow
pseudo
Copy code
class CraftingSystem:
    inventorySystem: InventorySystem
    skillSystem: SkillSystem
    networkManager: NetworkManager

    // For vertical slice, jobs list may be empty (immediate crafting)
    activeJobs: list<CraftingJob>

    method HandleCraftRequests(craftRequests: list<PlayerInput_CraftRequest>):
        for req in craftRequests:
            player = worldManager.GetEntity(req.playerId)
            if player is null: continue
            station = worldManager.GetCraftingStation(req.stationId)
            recipe = ContentDatabase.Recipes[req.recipeId]

            result = TryCraftImmediate(player, station, recipe, req.quantity)
            networkManager.SendToPlayer(req.playerId, result)

    method TryCraftImmediate(player: Entity, station: CraftingStation, recipe: RecipeDef, qty: int) -> Event_CraftingResult:
        if not IsInRange(player, station): return Failure("OutOfRange")
        if station.type != recipe.stationType: return Failure("WrongStation")
        if not skillSystem.MeetsRequirement(player, recipe.requiredSkillId, recipe.minSkillLevel):
            return Failure("SkillTooLow")
        if not HasIngredients(player.inventory, recipe, qty):
            return Failure("MissingIngredients")

        if not HasInventorySpaceForOutput(player.inventory, recipe, qty):
            return Failure("InventoryFull")

        // Consume inputs
        ConsumeIngredients(player.inventory, recipe, qty)
        // Add outputs
        outputStacks = AddOutputs(player.inventory, recipe, qty)
        // Award XP
        xpGained = recipe.xpPerCraft * qty
        skillSystem.AwardXP(player, recipe.requiredSkillId, xpGained)

        return Success(recipe.id, qty, outputStacks, xpGained)

    method ProcessCraftingJobs(tickIndex: long):
        // For timed crafting variant (optional in slice)
        for job in activeJobs:
            if tickIndex >= job.completeTick:
                CompleteJob(job)
                activeJobs.remove(job)
Failure(...) and Success(...) construct Event_CraftingResult objects.

9. SaveSystem — JSON Persistence
9.1 Data Structures (Vertical Slice)
pseudo
Copy code
struct SkillSave:
    skillId: string
    level: int
    xp: int

struct InventorySlotSave:
    slotIndex: int
    itemId: string
    quantity: int

struct PlayerSave:
    schemaVersion: int
    characterId: string
    name: string
    zoneId: string
    position: Vector3
    skills: list<SkillSave>
    inventory: list<InventorySlotSave>
    equipment: dict<string, string?> // slotName -> itemId
    knownRecipes: list<string>
    gold: int

struct ResourceNodeSave:
    nodeId: string
    isDepleted: bool
    nextRespawnTimestamp: long

struct ChestSave:
    chestId: string
    isOpened: bool

struct WorldSave:
    schemaVersion: int
    worldId: string
    resourceNodes: list<ResourceNodeSave>
    chests: list<ChestSave>
    questObjects: list<QuestObjectSave>
    worldFlags: dict<string, any>
9.2 SaveSystem Pseudocode
pseudo
Copy code
class SaveSystem:
    worldSave: WorldSave
    dirtyPlayers: set<string>  // characterId
    worldDirty: bool = false

    method LoadWorldOrCreateDefault():
        if FileExists("WorldSave.json"):
            worldSave = JsonLoad("WorldSave.json")
        else:
            worldSave = CreateDefaultWorldSave()
            JsonSaveAtomic("WorldSave.json", worldSave)

    method LoadPlayerOrCreateDefault(characterId: string) -> PlayerSave:
        filename = "Player_" + characterId + ".json"
        if FileExists(filename):
            return JsonLoad(filename)
        else:
            save = CreateDefaultPlayerSave(characterId)
            JsonSaveAtomic(filename, save)
            return save

    method MarkDirtyFromWorld(worldManager: WorldManager):
        if worldManager.HasStateChangesSinceLastTick():
            worldDirty = true

    method MarkDirtyFromPlayers(players: list<Entity>):
        for p in players:
            if p.inventoryDirty or p.equipmentDirty or p.skillsDirty or p.positionDirty:
                dirtyPlayers.add(p.entityId)

    method SaveWorld():
        if not worldDirty: return
        worldSave = worldManager.ExportWorldSave()
        JsonSaveAtomic("WorldSave.json", worldSave)
        worldDirty = false

    method SaveAllConnectedPlayers():
        for characterId in dirtyPlayers:
            player = worldManager.GetEntity(characterId)
            if player is null: continue
            playerSave = ExportPlayerSave(player)
            filename = "Player_" + characterId + ".json"
            JsonSaveAtomic(filename, playerSave)

        dirtyPlayers.clear()

    method JsonSaveAtomic(path: string, data: any):
        tmpPath = path + ".tmp"
        FileWrite(tmpPath, JsonSerialize(data))
        FileMoveReplace(tmpPath, path)
Export helpers (outline):

pseudo
Copy code
method ExportPlayerSave(player: Entity) -> PlayerSave:
    // read from components (position, skills, inventory, equipment, etc.)
    // fill struct and return

method WorldManager.ExportWorldSave() -> WorldSave:
    // collect node/chest/flags states from world
10. Client-Side Prediction & UI Hooks
10.1 Client Movement Prediction
ps
Copy code
class ClientPlayerController:
    localEntity: Entity
    networkManager: NetworkManager

    method Update(deltaTime: float):
        inputDir = ReadMovementInput()
        if inputDir != Vector2.zero:
            // local prediction
            localEntity.position += inputDir * LOCAL_MOVE_SPEED * deltaTime

        // send input to host (unreliable)
        msg = PlayerInput_Move(
            playerId = localEntity.entityId,
            tickClientTimestamp = LocalTimeToTicks(),
            direction = inputDir
        )
        networkManager.SendToHost(msg)
10.2 Applying Transform Snapshots
pseudo
Copy code
class ClientWorld:
    entities: dict<string, Entity>

    method ApplyTransformSnapshot(snapshot: Snapshot_Transforms):
        for ts in snapshot.transforms:
            entity = entities[ts.entityId]
            if entity is null: continue

            // Smoothly move toward authoritative position
            entity.targetPosition = ts.position
            entity.rotationY = ts.rotationY

    method Update(deltaTime: float):
        for entity in entities.values:
            entity.position = Lerp(entity.position, entity.targetPosition, SMOOTHING_FACTOR * deltaTime)
10.3 UIManager Hooks
pseudo
Copy code
class UIManager:
    method Init():
        // bind UI panels: HP bar, hotbar, inventory, crafting window

    method RefreshHP(entityId: string):
        // read StatsComponent for entity and update HP bar

    method RefreshInventory(playerId: string):
        // rebuild inventory grid from InventoryComponent

    method ShowCraftingResult(evt: Event_CraftingResult):
        if evt.success:
            ShowToast("Crafted " + evt.quantity + "x " + evt.recipeId)
        else:
            ShowError("Craft failed: " + evt.reasonCode)
11. End-to-End Flow Summaries
11.1 Combat (Player Attacks Enemy)
text
Copy code
Client:
  1) Player clicks enemy → sends PlayerInput_Attack(start, targetId).

Host:
  2) NetworkManager buffers input.
  3) TickManager.RunTick:
     - DrainBufferedInputs → attackCommands
     - CombatSystem.ProcessAttackTimersAndIntents:
       • StartAutoAttack for player.
     - CombatSystem.TryResolveAttack when nextAttackTick reached:
       • ComputeDamage, ApplyDamage via StatsSystem.
       • AwardXP via SkillSystem.
       • Build Event_CombatResult.
  4) NetworkManager.BroadcastEvent(Event_CombatResult).

Clients:
  5) Receive Event_CombatResult:
     - Update HP bars in ClientWorld + UI.
     - Play hit/death animations locally.
11.2 Crafting (Immediate)
text
Copy code
Client:
  1) Player interacts with forge → opens crafting UI.
  2) Player selects recipe + quantity → sends PlayerInput_CraftRequest.

Host:
  3) NetworkManager buffers input.
  4) TickManager.RunTick:
     - DrainBufferedInputs → craftRequests.
     - CraftingSystem.HandleCraftRequests:
       • Validate station, skill, ingredients, space.
       • Consume ingredients through InventorySystem.
       • Grant outputs, AwardXP.
       • Build Event_CraftingResult + InventoryChanged.

Clients:
  5) Owner receives Event_CraftingResult + Event_InventoryChanged:
     - Update inventory UI.
     - Show crafting toast.
11.3 Persistence (Autosave)
text
Copy code
Host:
  1) SaveSystem marks world/players dirty during ticks.
  2) Every 5 minutes:
     - TickManager triggers SaveSystem.SaveWorld + SaveAllConnectedPlayers.
  3) On host shutdown or player disconnect:
     - SaveSystem.SaveWorld / SavePlayer(characterId).

On restart:
  4) GameManager.Init(Host) → SaveSystem.LoadWorldOrCreateDefault.
  5) On client connect:
     - GameManager.LoadPlayerOrCreateDefault(characterId).
     - NetworkManager sends initial PlayerSave + WorldSave snapshot.
