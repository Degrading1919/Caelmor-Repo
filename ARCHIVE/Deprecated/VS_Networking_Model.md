# VS_Networking_Model.md
### Caelmor — Vertical Slice Minimal Networking Layer  
### Role: Networking, Persistence & Systems Architect  
### Version: VS v1.0

---

## 1. Purpose & Scope

This document defines the **minimal networking layer** required for the Caelmor Vertical Slice (VS), aligned with the Phase 1.4 Technical Foundation and the TickManager design.

The VS networking layer must:

- Support **2–4 player** co-op sessions.
- Use a **host-authoritative model** for all gameplay state.
- Integrate with a **10 Hz tick** simulation loop.
- Provide a small, explicit set of RPC/message patterns.
- Handle **join/leave** flows cleanly.
- Deliver **player snapshots** and state deltas reliably.

This is a *minimum viable* networking plan, intended to be simple enough for solo-dev implementation and extensible to dedicated servers later.

---

## 2. High-Level Architecture

### 2.1 Roles

- **Host (Server)**  
  - Runs the authoritative TickManager.  
  - Owns all gameplay state (players, enemies, world).  
  - Handles persistence (save/load).  
  - Receives and validates client inputs.  
  - Sends snapshots and events.

- **Client**  
  - Sends local input to the host.  
  - Renders world state from snapshots and events.  
  - Predicts only local movement (optional, non-authoritative).

### 2.2 Core Components

- `NetworkManager`  
  - Connection management, message routing, host/client role.

- `TickManager`  
  - 10 Hz simulation loop driving gameplay and snapshots.

- `EntitySystem`  
  - Registry of networked entities (players, enemies, key world actors).

- `Serializer`  
  - Serializes/deserializes messages & snapshots.

---

## 3. Host-Authoritative Transform Model

### 3.1 Authority Rules

- The **host** is the only authority for:
  - Player and enemy transforms (position, rotation).
  - Combat state (HP, timers, deaths).
  - Resource node and world object states.

- Clients:
  - Send **desired movement** (inputs), not transforms.
  - Display **predicted** movement for their own character.
  - Follow **host corrections** when snapshots differ.

### 3.2 Transform Update Flow

1. **Client Input**  
   - Client reads input each frame (WASD / analog).  
   - Sends `Msg_PlayerInput_Move` at a fixed frequency (e.g., 10–20 Hz).

2. **Host Simulation**  
   - On each tick:
     - Applies movement inputs using server-side movement logic.  
     - Updates authoritative transforms for players and enemies.

3. **Snapshots to Clients**  
   - On each tick (or every N ticks):
     - Host sends `Msg_Snapshot_Transforms` containing:
       - For each relevant entity (interest management):  
         - `entityId`  
         - `position` (x, y, z)  
         - `rotation` (y-axis)  
         - Optional: velocity or movement state.

4. **Client Rendering**  
   - Client interpolates remote entities between received snapshots.  
   - For local player:
     - Predicts movement immediately from input.  
     - When a new snapshot arrives:
       - If deviation > tolerance → lerp or snap to authoritative position.

---

## 4. Join / Leave Flow

### 4.1 Host Start

- Host creates a session via `NetworkManager.StartHost()`.
- Host loads:
  - World data (WorldSave or default).
  - Any available player saves (for returning players).

### 4.2 Client Join

1. **Connect**  
   - Client calls `NetworkManager.StartClient(hostAddress)`.

2. **Handshake**  
   - Client sends `Msg_JoinRequest`:
     - `playerId` (persistent ID or “new”).  
   - Host validates capacity and version compatibility.

3. **Host Acceptance**  
   - Host sends `Msg_JoinAccept` containing:
     - `assignedClientId`  
     - `playerSnapshot` (PlayerSave baseline)  
     - `worldSnapshot` (minimal state for current zone)  
     - List of existing players in session (IDs & appearance data).

4. **Client Initialization**  
   - Client creates a local player avatar using `playerSnapshot`.  
   - Client loads the correct scene/zone.  
   - Client spawns other players and enemies from `worldSnapshot`.  
   - Client begins sending input messages.

### 4.3 Client Leave

- Client initiates leave:
  - Calls `NetworkManager.Disconnect()`.  
  - Sends `Msg_LeaveNotice` (best effort, not required for correctness).

- Host-side behavior:
  - Host removes the player entity from EntitySystem.  
  - Host persists PlayerSave for that player.  
  - Host sends `Msg_PlayerDespawn` to remaining clients.

- Unclean disconnects:
  - Host detects timeout / connection loss.  
  - Performs same cleanup (remove entity, save state, notify others if possible).

### 4.4 Host Shutdown

- Host signals all clients with `Msg_Shutdown`:
  - Clients display “Host disconnected” and return to menu.  
- Host saves:
  - All PlayerSave data.  
  - WorldSave.

---

## 5. RPC / Message Patterns

The VS uses a **small set of message types** with clear responsibilities.

### 5.1 Client → Host (Inputs & Requests)

1. `Msg_PlayerInput_Move` (UNRELIABLE)
   - `clientId`  
   - `moveVector` (2D or 3D)  
   - `sprintFlag`  

2. `Msg_PlayerInput_Attack` (RELIABLE)
   - `clientId`  
   - `action` (StartAuto, StopAuto, UseAbility)  
   - `targetEntityId` (optional)  
   - `abilityId` (for specials)

3. `Msg_PlayerInput_Interact` (RELIABLE)
   - `clientId`  
   - `interactType` (UseNode, UseStation, TalkNpc, OpenChest)  
   - `targetObjectId`

4. `Msg_PlayerInput_InventoryAction` (RELIABLE)
   - `clientId`  
   - `actionType` (Move, Equip, Unequip, Split, Drop)  
   - `sourceSlotIndex`, `destSlotIndex`  
   - Optional `quantity`

5. `Msg_PlayerInput_CraftRequest` (RELIABLE)
   - `clientId`  
   - `stationId`  
   - `recipeId`  
   - `quantity`

6. `Msg_JoinRequest` (RELIABLE)
   - `desiredPlayerId` (existing or new)  
   - `clientVersion`

7. `Msg_LeaveNotice` (RELIABLE, best-effort)
   - `clientId`

### 5.2 Host → Client (Snapshots & Events)

1. `Msg_Snapshot_Transforms` (UNRELIABLE)
   - Tick-aligned transform updates:
     - `tickIndex`  
     - Array of:
       - `entityId`  
       - `position`  
       - `rotation`  
       - Optional `moveState`

2. `Msg_Event_CombatResult` (RELIABLE)
   - `sourceEntityId`  
   - `targetEntityId`  
   - `damage`  
   - `newHp`  
   - Flags: `isKill`, `isCritical` (if relevant)

3. `Msg_Event_InventoryChanged` (RELIABLE)
   - `playerId`  
   - List of changed slots:
     - `slotIndex`, `itemId`, `quantity`  
   - Equipment updates (if changed):

4. `Msg_Event_CraftingResult` (RELIABLE)
   - `playerId`  
   - `recipeId`  
   - `success` (bool)  
   - Item outputs (if success)  
   - Reason code (if failure)

5. `Msg_Event_WorldObjectUpdate` (RELIABLE)
   - `objectId`  
   - `type` (ResourceNode, Chest, Door, etc.)  
   - New state data (e.g., `isDepleted`, `isOpened`)

6. `Msg_Event_SkillXP` (RELIABLE)
   - `playerId`  
   - `skillId`  
   - `xpGained`  
   - Optional: `newLevel`

7. `Msg_JoinAccept` (RELIABLE)
   - `assignedClientId`  
   - `playerSnapshot`  
   - `worldSnapshot`

8. `Msg_PlayerSpawn` / `Msg_PlayerDespawn` (RELIABLE)
   - For additional players joining/leaving after initial connection.

9. `Msg_Shutdown` (RELIABLE)
   - Notification that the host is shutting down.

---

## 6. Network Tick Integration

### 6.1 TickManager & NetworkManager Coordination

On the **host**, each 10 Hz tick:

1. **Input Drain**  
   - NetworkManager provides a list of all messages received since last tick (batched by client).  
   - TickManager processes input messages in deterministic order.

2. **Simulation Step**  
   - TickManager runs movement, AI, combat, world updates.

3. **Delta Collection**  
   - Systems report changes since last tick:
     - Transforms  
     - HP & combat results  
     - Inventory changes  
     - World object changes  
     - Crafting completions  
     - Skill XP gains  

4. **Snapshot & Event Dispatch**  
   - TickManager bundles:
     - Transforms into `Msg_Snapshot_Transforms` (UNRELIABLE).  
     - Other changes into event messages (RELIABLE).  
   - NetworkManager sends messages to each client (respecting AOI filters if implemented).

5. **Persistence Hooks**  
   - TickManager marks changed entities/world objects as dirty.  
   - SaveSystem handles autosave according to schedule (not in-tick I/O).

### 6.2 Client Side

- Clients are not tick-authoritative but:
  - Run their own **render loop** (frame-based).  
  - Interpolate known entities between snapshots.  
  - Apply corrections:  
    - For local player when host transform deviates too far.  
    - For other entities to avoid jitter.

- No client needs to know the exact server tick rate, but may:
  - Store `lastSnapshotTickIndex` for debugging and smoothing.

---

## 7. Player Snapshot Responsibilities

### 7.1 Initial Join Snapshot

When a client joins:

- Host constructs a **full snapshot** for that player (`playerSnapshot`):

  - `playerId`, `name`  
  - Current `zoneId` & `position`  
  - Skills: levels & XP  
  - Inventory slots (items, quantities)  
  - Equipment (per slot)  
  - Known recipes  
  - Gold

- And a **minimal world snapshot** (`worldSnapshot`) tailored for VS:

  - Zone ID and seed (if any)  
  - Resource node states in local AOI (e.g., near VS zone)  
  - Chest/quest object states (if used)  
  - Already-connected players’ IDs and key properties (position, appearance)

### 7.2 Ongoing Player Snapshots (Deltas)

The host must maintain:

- **Per-player** snapshot responsibilities:
  - Ensure that each player receives:
    - All transform snapshots for entities in their area.  
    - All combat events where they are source/target or in visual range.  
    - All inventory, crafting, and skill events affecting them.  
    - All world object updates in their local zone.

- **Minimal Payload Strategy**:
  - Do not resend full state each tick.  
  - Use:
    - Transform-only snapshots for frequent updates.  
    - Event-based, reliable messages for discrete changes.

### 7.3 Resync / Correction

In case of:

- Detected desync (client requests resync or host detects impossible state).
- Late join to a running session.
- After large-scale world changes (e.g., hot reload during dev).

Host can send a **partial or full resync snapshot**:

- `Msg_Resync_PlayerState`:
  - Full player state for the requesting client.  
- `Msg_Resync_WorldState` (optional in VS):
  - Non-compressed world objects within AOI.

For VS, these resync messages are primarily a **debug tool** and may be triggered from the console or dev UI rather than gameflow.

---

## 8. Error Handling & Minimal Security

### 8.1 Input Validation

Host must reject or ignore:

- Movement inputs that warp beyond a reasonable distance.  
- Attacks on invalid or out-of-range targets.  
- Inventory actions violating slot rules or quantities.  
- Craft requests without sufficient ingredients or wrong station.

### 8.2 Timeouts

- If no heartbeat/input from a client for `N` seconds:
  - Host flags them as disconnected.  
  - Executes the leave flow (save state, despawn).

### 8.3 Version Mismatches

- On `Msg_JoinRequest`, host checks `clientVersion`.  
- If mismatched, responds with a “reject” message and closes connection.

---

## 9. Extensibility Notes (Beyond Vertical Slice)

The VS networking layer is intentionally minimal but structured to:

- Drop host logic into a **dedicated server build** later.  
- Swap local JSON saves for DB-backed world state.  
- Extend message set for:
  - Grouping, chat, emotes.  
  - Advanced AI or events.  
  - Larger AOI and streaming.

Core principle: **Do not change the authority model** when scaling up; only replace where the host runs and how persistence is stored.

---

# End of Document
