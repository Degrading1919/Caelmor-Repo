# Caelmor — Vertical Slice Technical Specification  
Version: v1.0  
Role: Networking, Persistence & Systems Architect  
Target: 02_VERTICAL_SLICE (Movement, Combat, Inventory, Crafting, Persistence, Co-op)

---

## 1. Purpose & Scope

This document defines the **authoritative tick loop**, **networking sync rules**, **combat pipeline**, **inventory flow**, **crafting calls**, and **persistence hooks** required to implement the Caelmor **Vertical Slice**.

Vertical Slice content includes:

- Movement + camera in a small Lowmark Vale test area  
- Basic melee combat vs a small set of enemy variants  
- Inventory & equipment  
- Simple crafting at 1–2 stations  
- JSON-based persistence for player and world state  
- 1–4 player **host-authoritative** co-op

---

## 2. High-Level Architecture (Vertical Slice Subset)

The Vertical Slice reuses the Phase 1.4 architecture but only wires up the minimum required modules:

- **GameManager** — Bootstraps core systems, owns references
- **NetworkManager** — Host/client roles, connections, message dispatch
- **TickManager** — Authoritative 10 Hz simulation loop
- **WorldManager / ZoneManager** — Load test zone, spawn static entities & nodes
- **EntitySystem** — Shared component for all actors (players, enemies)
- **CombatSystem** — Attack timers, hit resolution, XP awards
- **StatsSystem** — HP/armor tracking for entities
- **SkillSystem** — XP & level state (read/write for skills)
- **InventorySystem** — Slot-based inventory model and operations
- **EquipmentSystem** — Applies item stats to entities
- **CraftingSystem** — Recipe lookup and craft resolution
- **SaveSystem** — JSON save/load of player + world state
- **UIManager** — HUD for HP, hotbar, inventory, and crafting

All authoritative logic executes on the **host**, with **clients acting as thin input/visual layers**.

---

## 3. Authoritative Tick Loop

### 3.1 Tick Rate

- **Tick interval:** `0.1s` (10 Hz)
- **Source of truth:** `TickManager` on the host
- **Tick index:** `long TickIndex` incremented each tick, used for ordering and debugging

### 3.2 Tick Execution Order (Host)

On each host tick:

1. **Collect Inputs**
   - Drain buffered client input messages since last tick:
     - Movement commands
     - Attack commands
     - Interaction commands (loot, crafting, node interaction)
2. **Validate & Apply Movement**
   - For each player:
     - Apply movement input with speed constraints and collision checks
     - Update authoritative transforms
3. **AI Decisions**
   - For each active enemy:
     - Evaluate aggro state (distance to players, threat)
     - Choose behavior (idle, patrol, chase, attack, return-to-leash)
4. **Combat Timers & Resolution**
   - Update attack cooldown timers (players & enemies)
   - Process any new attack intents (auto-attack start/stop, specials)
   - Resolve attacks which land on this tick:
     - Hit/miss, damage, on-hit effects
5. **Apply Damage & Death**
   - Update HP values in `StatsSystem`
   - For entities reaching 0 HP:
     - Trigger death logic
     - Award XP to responsible players
     - Queue loot spawns (if any)
6. **World State Updates**
   - Resource node depletion/respawn
   - Crafting completion timers
   - Short-lived world flags relevant to the slice (e.g., “door opened”)
7. **Persistence Hooks**
   - Mark dirty flags for:
     - Player changes (HP, skills, inventory)
     - World changes (nodes, chests, flags)
   - Defer actual disk I/O to SaveSystem (see §8)
8. **Snapshot & Sync**
   - Build minimal state deltas:
     - Transforms (players, relevant enemies)
     - HP changes
     - Enter/exit combat states
     - Inventory or crafting results
   - Send to clients according to **sync rules** in §4

### 3.3 Client-Side Tick & Prediction

- Clients **do not run an authoritative tick**.
- Clients:
  - Interpolate/extrapolate remote entity transforms based on snapshots
  - Apply **local prediction** only for their own movement:
    - Immediate movement feedback when pressing movement keys
    - Smooth correction toward host position when snapshots arrive
  - Do **not** predict combat results; they only play animations & wait for server events

---

## 4. Networking Sync Rules

### 4.1 Roles

- **Host**
  - Runs TickManager and all authoritative simulation
  - Owns SaveSystem & world data
  - Receives input messages from clients
  - Sends state updates (snapshots + events)

- **Client**
  - Sends user input to host
  - Renders snapshots and events
  - Never mutates authoritative state

### 4.2 Connection Lifecycle

1. Client connects to host (via NetworkManager)
2. Host authenticates connection (simple session auth for slice)
3. Host sends:
   - Initial **PlayerSave** snapshot (or default template)
   - Initial **WorldSave** snapshot (or test-zone defaults)
   - Zone/scene load instruction
4. Client loads zone, spawns local player representation, and begins rendering snapshots

### 4.3 Message Categories & Reliability

**Input → Host** (client → host):

- `PlayerInput_Move` (UNRELIABLE)
  - Contains directional vector + timestamp
  - High frequency; latest wins
- `PlayerInput_Attack` (RELIABLE)
  - Start/stop auto-attack, trigger special attacks
- `PlayerInput_Interact` (RELIABLE)
  - Interact with resource node, NPC, crafting station, chest
- `PlayerInput_InventoryAction` (RELIABLE)
  - Move item, equip/unequip, split stack, drop item
- `PlayerInput_CraftRequest` (RELIABLE)
  - Request to craft a recipe at a station

**State & Events → Clients** (host → client):

- `Snapshot_Transforms` (UNRELIABLE)
  - Batched authoritative positions/rotations (players, nearby enemies)
  - Sent every tick or every other tick depending on bandwidth
- `Event_CombatResult` (RELIABLE)
  - Hit/miss, damage, HP deltas, death events
- `Event_InventoryChanged` (RELIABLE)
  - Item added/removed/moved; equipment changes
- `Event_CraftingResult` (RELIABLE)
  - Crafting success/failure; output items
- `Event_WorldObjectUpdate` (RELIABLE)
  - Resource node depleted/respawned, chest opened
- `Event_SkillXP` (RELIABLE)
  - XP gain events and level-ups

### 4.4 Sync Groups & Frequencies

- **Transforms**
  - Frequency: 10–20 Hz (configurable; default 10 Hz to match tick)
  - Channel: UNRELIABLE
  - Content: entityId, position, rotation, optional velocity
- **Combat State**
  - Frequency: On change
  - Channel: RELIABLE
  - Content: attack started/stopped, combat result events
- **Inventory, Crafting, Skills**
  - Frequency: On change
  - Channel: RELIABLE
- **World Objects**
  - Frequency: On change
  - Channel: RELIABLE
  - Scope: only objects in the client’s current zone and interest radius

---

## 5. Combat Pipeline (Vertical Slice)

### 5.1 Core Concepts

- All combat is **tick-resolved on the host**.
- Players experience **cooldown-based** attacks, but under the hood:
  - Attack readiness is gated by timers keyed to `TickIndex`.
- No client-side damage prediction.

### 5.2 Auto-Attack Flow (Player vs Enemy)

1. **Input**
   - Client sends `PlayerInput_Attack` (start auto-attack) with target entityId.
2. **Host Validation**
   - Checks:
     - Entity is alive
     - Target is valid and in line-of-sight (simplified for slice)
     - Player in range based on weapon reach
   - If invalid, host sends `Event_CombatResult` with “attack denied” (optional for debugging).
3. **Attack Timer Setup**
   - CombatSystem starts an attack timer for the player:
     - `nextAttackTick = currentTick + attackSpeedInTicks`
   - Sets player’s `isAutoAttacking = true` and remembers `targetId`.
4. **Attack Resolution**
   - On each tick:
     - If `isAutoAttacking` and `TickIndex >= nextAttackTick`:
       - Confirm target still valid & in range
       - Resolve hit vs miss
       - Compute damage
       - Apply damage to target
       - Emit `Event_CombatResult` to all relevant clients
       - Set `nextAttackTick += attackSpeedInTicks`
5. **Stopping Auto-Attack**
   - Client sends `PlayerInput_Attack` (stop) or changes target.
   - Host sets `isAutoAttacking = false`.

### 5.3 Special Attacks (If Included in Slice)

- Similar to auto-attack but:
  - Use separate cooldown timers per ability.
  - Can modify damage formula, range, or apply flags (e.g. “armor-piercing”).

Flow:

1. Client sends `PlayerInput_Attack` with `abilityId`.
2. Host checks:
   - Cooldown ready
   - Required weapon type equipped
   - Target valid/in range
3. Host schedules special attack resolution:
   - `resolveTick = currentTick + windupTicks`
4. On `resolveTick`, apply combat logic and send `Event_CombatResult`.

### 5.4 Damage & XP Calculation

For each successful hit:

1. **Base Damage**
   - From weapon definition (`weaponDamage`) + equipment bonuses.
2. **Mitigation**
   - From target’s armor (simple linear or table-driven formula).
3. **HP Change**
   - `targetHp = max(0, targetHp - finalDamage)`.
4. **Death Handling**
   - If HP reaches 0:
     - Trigger death animation/event
     - Spawn loot (if configured)
     - Award XP to the attacker:
       - Skill: Melee (or relevant)
       - Amount: from enemy variant (`xpValue`)
5. **Events**
   - Broadcast `Event_CombatResult` with:
     - Source entityId
     - Target entityId
     - Damage value
     - New HP values
     - Flags: `isKill`, `isCrit` (if supported)

### 5.5 Enemy Combat

- Enemies use same CombatSystem pipeline:
  - Attack timers
  - Attack range and speed from enemy variant definition
- AIController chooses targets and sets:
  - `isAutoAttacking = true`
  - `targetId = playerId`

---

## 6. Inventory Flow

### 6.1 Data Model

Inventory (per player):

- `slots[]` — fixed-size array of slot entries
  - `slotIndex: int`
  - `itemId: string|null`
  - `quantity: int`
- All item definitions are immutable ScriptableObjects referenced by `itemId`.

Equipment (per player):

- `equipment`:
  - `head`, `chest`, `legs`, `hands`, `weaponMain`, `weaponOff`, etc.
  - Each slot holds an `itemId` or `null`.

### 6.2 Client Interactions

Client-side actions:

- Open/close inventory UI
- Drag/drop between:
  - Inventory slots
  - Inventory → equipment
  - Equipment → inventory
- Drop item to ground (optional in slice)
- Split stacks (basic support or deferred)

Each action results in a **single authoritative request**:

- `PlayerInput_InventoryAction` with:
  - `actionType` (`Move`, `Equip`, `Unequip`, `Split`, `Drop`)
  - `sourceSlotIndex` / `destSlotIndex`
  - Optional `quantity`

UI applies optimistic visual feedback (e.g., drag ghost) but only updates confirmed layout when server approves.

### 6.3 Host Validation & Application

On receiving `PlayerInput_InventoryAction`:

1. Validate the player owns the inventory being modified.
2. Validate source slot/equipment slot contains expected item.
3. Validate destination slot or equipment type rules:
   - Equipment slot can accept the item’s category
   - Inventory slots are within bounds
4. Apply inventory changes:
   - Move items
   - Swap if destination occupied
   - Split stack if requested and allowed
5. Recalculate derived stats via EquipmentSystem:
   - Update entity stats (e.g., HP max, armor, weapon damage)
6. Mark:
   - Player inventory as dirty for persistence
   - Equipment state as dirty for combat (if changed)
7. Send `Event_InventoryChanged` to:
   - The owner (full detail)
   - Other clients as needed (only equipment appearance, if implemented)

---

## 7. Crafting Calls

### 7.1 Craft Request Flow

1. **Client Interaction**
   - Player walks near crafting station (forge, bench, etc.).
   - Client opens crafting UI (local).
   - Player selects recipe and quantity.
   - Client sends `PlayerInput_CraftRequest`:
     - `stationId`
     - `recipeId`
     - `quantity`

2. **Host Validation**
   - Verify:
     - Player is within interaction range of station.
     - Station type matches recipe’s `stationType`.
     - Recipe exists and is unlocked (if gating is used).
     - Player has required ingredients in inventory and/or station storage.
     - Skill requirements met (`minSkill`).
   - If any check fails:
     - Send `Event_CraftingResult` (failure reason) to client.
     - No changes applied.

3. **Immediate vs Timed Crafting**
   - **Vertical Slice simplification:**
     - Use **immediate crafting** with optional short simulated delay (0–2 seconds) to avoid full timer complexity.
   - For immediate crafting:
     - Consume ingredients from inventory.
     - Add result items (or queue for overflow handling).
     - Award skill XP.
     - Send `Event_CraftingResult` (success, items crafted, XP gained).
   - For timed crafting (if desired for feel):
     - Create a crafting job:
       - `jobId`, `playerId`, `stationId`, `recipeId`, `completeTick`.
     - Process jobs in Tick loop (§3.2 step 6).
     - On `completeTick`, apply results, then send `Event_CraftingResult`.

4. **Inventory Integration**
   - Crafting input & output is entirely mediated via InventorySystem:
     - Removes ingredient stacks
     - Adds crafted items
   - Any change triggers `Event_InventoryChanged`.

### 7.2 Failure States (Vertical Slice)

- Not enough ingredients
- Wrong station type
- Out of range
- Inventory full (cannot place result)
- Missing skill requirement

Each failure yields `Event_CraftingResult` with a reason code used by client UI.

---

## 8. Persistence Hooks

### 8.1 Save Data Structures (Minimum Slice)

**PlayerSave.json (per player):**

- `schemaVersion: int`
- `characterId: string`
- `name: string`
- `zoneId: string`
- `position: { x, y, z }`
- `skills: [ { skillId, level, xp } ]`
- `inventory: [ { slotIndex, itemId, quantity } ]`
- `equipment: { slotName: itemId|null }`
- `knownRecipes: [ recipeId ]`
- `gold: int`

**WorldSave.json (per host/world):**

- `schemaVersion: int`
- `worldId: string`
- `resourceNodes: [ { nodeId, isDepleted, nextRespawnTimestamp } ]`
- `chests: [ { chestId, isOpened } ]`
- `questObjects: [ { objectId, state } ]` (minimal in slice)
- `worldFlags: { [flagId]: bool|int|string }`

These structures match the broader Technical Foundation but the slice may omit unused sections.

### 8.2 Save Triggers (Vertical Slice)

**Host-only SaveSystem** executes:

- **On player disconnect**
  - Save that player’s **PlayerSave.json**
- **On host shutdown**
  - Save all connected players
  - Save **WorldSave.json**
- **Periodic Autosave**
  - Every **5 minutes**:
    - Save **WorldSave.json**
    - Save all connected players
- **On major events** (optional for slice, but recommended)
  - Upon completing key story quest states (if present)
  - Upon major inventory events (rare-item loot, major craft)

SaveSystem must support:

- Atomic writes (write to `*.tmp`, then move/replace final file)
- Simple versioning via `schemaVersion`

### 8.3 Load Order (Host)

On host boot:

1. **Load ScriptableObject Databases**:
   - Items, Skills, Recipes, Enemies, Zones
2. **Load WorldSave.json**
   - If absent, create default from zone definitions
3. **Listen for client connections**
4. **For each connecting player**:
   - Load `PlayerSave.json` (if exists) or create default character
   - Send initial player + world snapshot
   - Spawn player entity in zone

### 8.4 Client Persistence

- Vertical Slice assumes **no client-side save data**.
- All save state is held by the host machine (even in “single-player” mode, the host and player are the same machine).

---

## 9. Vertical Slice Success Criteria

The Vertical Slice is considered **technically successful** when:

1. **Tick Loop**
   - Host tick runs at 10 Hz; logs confirm stable loop
   - Movement, AI, and combat all depend on tick execution

2. **Networking Sync**
   - 2–4 clients can join a host session
   - Movement is smooth with interpolation & correction
   - Combat results are displayed identically on all clients

3. **Combat**
   - Auto-attack and at least one special attack (optional) work
   - HP bars update correctly
   - XP is awarded and persists across sessions

4. **Inventory**
   - Drag/drop, equip/unequip, and loot handling function correctly
   - Inventory and equipment changes are authoritative & synchronized

5. **Crafting**
   - Player can craft at least 2–3 items at a station
   - Crafting consumes ingredients and creates items
   - Crafting grants skill XP and persists

6. **Persistence**
   - Exiting and rejoining a session restores:
     - Player position
     - HP, inventory, equipment
     - Skill levels & XP
     - Resource node depletion/restoration from world state

Once these are met, Caelmor has a **felt** core identity consistent with its design pillars and is ready for expansion into full systems and content production.

---
