# TickManager_Design.md
### Caelmor — Vertical Slice Tick Manager Specification  
### Role: Networking, Persistence & Systems Architect  
### Version: VS v1.0

---

# 1. Purpose
The TickManager is the **authoritative simulation clock** for Caelmor’s Vertical Slice.  
It executes all deterministic logic affecting movement, AI, combat, world simulation, and network snapshots on the **host**.  
This follows Caelmor’s Phase 1.4 Technical Foundation, where the tick loop is defined as a central server-authoritative system.  
(Ref: Caelmor_Phase1_4_Technical_Foundation.md) :contentReference[oaicite:4]{index=4}

---

# 2. Tick Frequency
- **Tick Rate:** 10 Hz  
- **Tick Interval:** `0.1 seconds`  
- **Clock Mode:** Fixed interval using accumulated delta time  
- **Indexing:** `long TickIndex` increments every tick to maintain global ordering

Rationale:  
10 Hz balances determinism, solo-dev implementation feasibility, and VS requirements for slow, readable combat aligned with design pillars (Pillar B — deliberate melee).  
(Ref: Pillars & Tenets) :contentReference[oaicite:5]{index=5}

---

# 3. Tick Responsibilities (High-Level)

### The TickManager MUST:
1. Consume all client inputs since last tick.  
2. Validate + apply movement for all players.  
3. Run AI decision-making.  
4. Update and resolve combat timers and hit events.  
5. Update StatsSystem, apply damage, deaths, and XP awards.  
6. Update world state objects (resource nodes, timers, crafting jobs).  
7. Set persistence dirty-flags for changed entities.  
8. Generate and broadcast **network snapshots**.  
9. Emit tick-level events for subsystems (OnTick).

These responsibilities directly reflect the authoritative tick model in Phase 1.4.  
(Ref: Phase1_4 — Tick Model 3.1, Host Responsibilities 3.2) :contentReference[oaicite:6]{index=6}

---

# 4. Tick Execution Order (Deterministic Sequence)

Each tick executes the following pipeline in this exact order:

1. **Input Collection**  
   - Drain queued `PlayerInput_*` messages from NetworkManager.  
   - Timestamp or sequence number ordering is maintained but tick alignment is authoritative.

2. **Movement Simulation**  
   - For each player:  
     - Validate current input (movement direction, sprint flag).  
     - Apply movement respecting:  
       - collision  
       - zone navigation mesh  
       - server-authoritative movement rules  
     - Update player transform in EntitySystem.

3. **AI Behavior Execution**  
   - For each active enemy:  
     - Evaluate aggro conditions  
     - Choose behavior state: idle, chase, attack, return-to-leash  
     - Update movement pathing toward target or home position  
   - AI state changes must be deterministic.

4. **Combat Timers & Attack Resolution**  
   - Update attack cooldowns for players + enemies.  
   - If an attack timer completes on this tick:  
     - Validate target  
     - Check range/LOS  
     - Resolve hit/miss  
     - Apply damage packet (StatsSystem)  
   - Emit combat events to NetworkManager for reliable dispatch.

5. **HP, Death, and XP Updates**  
   - Reduce HP where damage applied  
   - Trigger death state transitions  
   - Award XP based on enemy definitions  
   - Mark inventory, skills, and entity states dirty for persistence

6. **World State Updates**  
   - Resource node timers advance  
   - Crafting jobs complete on designated tick  
   - World flags update (door opened, chest looted, etc.)  
   - Updated elements flagged for WorldSave serialization

7. **Persistence Hooking**  
   - TickManager invokes SaveSystem "changed state" notifications  
   - Actual disk writes are performed asynchronously or on autosave interval  
   - No blocking file I/O permitted during tick execution

8. **Network Snapshot Generation**  
   - Compress transforms, combat state deltas, node updates  
   - Send UNRELIABLE transforms at 10 Hz  
   - Send RELIABLE deltas for HP, inventory, crafting results, world objects  
   - Snapshot generated **after** all simulation steps to represent authoritative world state for the frame

9. **OnTick Event Dispatch**  
   - Emit `OnTick(TickIndex)` for subscribed systems:  
     - CombatSystem  
     - AIController  
     - WorldManager  
     - CraftingSystem (optional timer mode)  
     - QuestSystem (objective polling, if needed)

---

# 5. Event Hooks

### 5.1 Internal Hooks
TickManager exposes subscription events for other systems:

| Hook | Description |
|------|-------------|
| `OnTick(long tickIndex)` | Fired at end of each tick; core driver for subsystems. |
| `OnBeforeTick(long tickIndex)` | Systems may prepare state before movement/AI/combat runs. |
| `OnAfterSnapshot(long tickIndex)` | Broadcast after network snapshot; useful for debug tools. |

### 5.2 Subsystem Responsibilities

**MovementSystem**  
- Reads player input → resolves routes → collision checks.  
- Must not modify combat timers.

**AIController**  
- Subscribed to OnTick.  
- Executes deterministic decision tree per enemy variant.

**CombatSystem**  
- Processes attack timing, range checks, hit results.  
- Must rely on TickIndex rather than real-time timestamps.

**StatsSystem**  
- Applies HP changes and death transitions.

**WorldManager / ResourceNodeManager**  
- Updates respawn timers and world flags.

**SaveSystem**  
- Subscribes to state changes; does not block tick execution.

These integrations match systemic responsibilities defined in the Phase 1.4 architecture.  
(Ref: Phase1_4 Modules 2.1 & Tick Flow Diagram 7.1) :contentReference[oaicite:7]{index=7}

---

# 6. Networking Responsibilities

TickManager directly influences networking through:

### 6.1 Snapshot Responsibilities
TickManager MUST generate a snapshot every tick, containing:

- Authoritative positions of:  
  - All players  
  - Nearby enemies (AOI-based)  
- HP deltas  
- Combat state changes (start/stop attack)  
- Resource node changes  
- Crafting results  
- Any world object state updates  
- Optional: Animation state hints (non-authoritative)

Snapshots align with the sync categories of Phase 1.4:  
- Transforms → UNRELIABLE @ 10–20 Hz  
- Combat state → RELIABLE  
- Inventory → RELIABLE  
- World objects → RELIABLE  
(Ref: Phase1_4 Networking 3.3) :contentReference[oaicite:8]{index=8}

### 6.2 Input Integration
- TickManager requests from NetworkManager all buffered client input commands since last tick.  
- Commands processed strictly in arrival order up to tick execution to prevent desync.

### 6.3 Correction Rules
TickManager state governs client corrections:  
- Clients interpolate/extrapolate between snapshots.  
- If position delta exceeds tolerance → server instructs correction.  
- Combat is never predicted; only animation timing may be predicted.

---

# 7. AI Integration

AI is fully tick-driven:

1. Per tick, AIController calculates target choice and movement vector.  
2. Movement applied via same movement validator as players.  
3. Attack timers updated identically to player timers.  
4. Leash behavior evaluated every tick.

AI behavior must remain simple and readable, consistent with VS encounter design and earlygame fairness.  
(Ref: Zone & Encounter design — Lowmark VS Whitebox) :contentReference[oaicite:9]{index=9}

---

# 8. Combat Integration

CombatSystem uses the tick clock as its singular timing source:

- Attack cooldowns defined in ticks (e.g., 28 ticks ≈ 2.8s).  
- Windup frames resolved on specific TickIndex.  
- Hits apply damage packets through StatsSystem.  
- All combat results broadcast via reliable network events.

Design rationale fits Phase 1.2 Pillar B (deliberate, rhythmic melee).  
(Ref: Pillars & Tenets) :contentReference[oaicite:10]{index=10}

---

# 9. Movement Integration

Movement is updated first in tick order to ensure:

- AI decisions reflect real player positions  
- Combat range checks use authoritative post-movement positions  
- Snapshot accuracy matches real server transforms

Movement rules follow Phase 1.3 movement constraints (walk, sprint, no jump, agility triggers only).  
(Ref: Phase1_3 Deep Dive Movement) :contentReference[oaicite:11]{index=11}

---

# 10. Persistence Hooks

TickManager MUST provide the following persistence hooks:

| Persistence Trigger | Description |
|---------------------|-------------|
| `OnStateChanged(Entity)` | Called when HP, inventory, skills, or equipment change. |
| `OnWorldObjectChanged(Node)` | Called when resource nodes deplete or respawn. |
| `OnTick_AutosaveCheck` | Evaluates autosave timer (default 5 minutes). |

Actual file I/O is deferred to SaveSystem and must not occur inside tick execution.

Persistence specification aligns with Phase 1.4 Save Pipeline.  
(Ref: Phase1_4 Persistence 6.3) :contentReference[oaicite:12]{index=12}

---

# 11. Performance & Determinism Rules

- Tick execution must complete < 8 ms per tick on minimum VS target to maintain deterministic pacing.  
- No allocations inside the tick loop (object pooling required).  
- No async/scheduled operations allowed that modify state mid-tick.  
- All randomness must use a deterministic RNG scoped to tick context for reproducibility.

---

# 12. Debugging & Visualization

Optional development-only hooks:

- `TickIndex` overlay for debug UI  
- Per-tick log (throttled) for combat or AI events  
- Snapshot byte-size reporting for networking debug

---

# 13. Summary

TickManager is the heartbeat of the Vertical Slice simulation:

- **10 Hz deterministic timing**  
- **Input → Movement → AI → Combat → World → Snapshot**  
- **Server-authoritative for all gameplay**  
- **NetworkManager syncs clients using tick-aligned data**  
- **SaveSystem reacts to state changes outside the tick loop**

Its behavior is foundational to Caelmor’s long-term architecture as described in Phase 1.4 and Roadmap Stage 3.1.  
(Ref: Caelmor_Expanded_Roadmap_v2 — Stage 3.1 TickManager) :contentReference[oaicite:13]{index=13}

---

# End of Document
