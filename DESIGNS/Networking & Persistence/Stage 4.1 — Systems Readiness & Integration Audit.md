# Stage 8.1 — Systems Readiness & Integration Audit  
**Scope:** Engine-readiness verification for Stage 7 non-combat economy systems (Resource Nodes → Gathering Resolution → Inventory/Grant → Crafting → Persistence).  
**Constraint:** No redesign. No schema changes. No behavior changes. This document verifies engine anchors, lifecycle hooks, and required scaffolding only.

---

## 1. Tick & Authority Verification

### Confirmed (from Technical Foundation)
- Caelmor uses a **10 Hz authoritative simulation loop** owned by the **host** (“TickManager — 10 Hz authoritative simulation loop” and “Tick rate: 10 Hz… The host executes all authoritative logic”). :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}  
- The tick loop is the ordering backbone for gameplay resolution and explicitly includes “Update world nodes/chests/bosses” as part of the host’s authoritative tick responsibilities. :contentReference[oaicite:2]{index=2}  
- Tick ownership is represented as a **central service** in the module diagram: `NetworkManager -> TickManager` and `WorldManager -> ZoneManager`, indicating tick is **global** and observed by world/zone systems rather than owned per-zone. :contentReference[oaicite:3]{index=3}  

### Required for Stage 7 Implementation (must exist or be stubbed)
- A **single authoritative tick source** (global) that Stage 7 systems can subscribe to deterministically (event or explicit call chain).
- A clear **tick phase** in which economy mutations occur, and a **post-mutation checkpoint boundary** for persistence alignment (see Section 4).

---

## 2. World State Anchors

### Confirmed (from Technical Foundation)
- World lifecycle ownership is defined at the module level:
  - **WorldManager — Zone loading/unloading, world spawning, static/active objects**
  - **ZoneManager — Local zone instance manager** :contentReference[oaicite:4]{index=4}  
- Boot pipeline sequencing exists and explicitly includes:
  1) Load content databases  
  2) Load save files (`PlayerSave.json`, `WorldSave.json`)  
  3) Resolve IDs  
  4) Begin simulation loop :contentReference[oaicite:5]{index=5}  

### Implications for Stage 7 (verification)
- **ResourceNode instances should live in server memory under world/zone ownership**, not under player systems.
- Node instances should be instantiated during **zone load / world boot** before the simulation loop begins for that zone, and they must be present for tick updates.

### Required but Missing (explicit engine hook expectations)
- A concrete **Zone Load Hook** that produces stable, placed node instances from zone content (the system must have a place to call “instantiate node instances by placement definition”).
- A concrete **Zone Unload Hook** that:
  - Stops ticking nodes for that zone
  - Ensures node runtime overrides are already captured in the world save scope prior to unload (per Stage 7.5 checkpoint language)

---

## 3. Player Session Anchors

### Confirmed (from Technical Foundation + Stage 8.0)
- Authority model is host-driven: inventory changes, crafting resolution, world object state, and persistence are host responsibilities. :contentReference[oaicite:6]{index=6}  
- Stage 8.0 explicitly requires “Player session identity” as scaffolding awareness before/during implementation. :contentReference[oaicite:7]{index=7}  

### Required for Stage 7 (must be true at runtime)
- There must be a server-side **PlayerId** resolution mechanism that:
  - Is stable across reconnects
  - Is used as the key for PlayerSave inventory state
- There must be a defined point at which **inventory becomes writable** for a player session (e.g., after PlayerSave is loaded/rehydrated).

### Required but Missing (or not yet specified in canon docs)
- A **server-side action serialization mechanism** ensuring:
  - Gather attempts and craft requests are processed deterministically (ideally at tick boundaries)
  - Concurrent requests from the same player cannot interleave inventory mutations in a way that breaks Stage 7 atomicity guarantees
- A minimal **Session Lifecycle** contract:
  - On connect: load PlayerSave → attach inventory state → allow actions
  - On disconnect: checkpoint PlayerSave scope (without implying frequency/timing beyond boundary)

---

## 4. Persistence Touchpoints

### Confirmed (from Technical Foundation + Stage 8.0)
- A **SaveSystem** exists as a named module and is explicitly “JSON-based persistence.” :contentReference[oaicite:8]{index=8}  
- Boot pipeline explicitly loads both **PlayerSave.json** and **WorldSave.json** before simulation begins. :contentReference[oaicite:9]{index=9}  
- Stage 8.0 freezes the persistence integration goal set:  
  - PlayerSave (inventory)  
  - WorldSave (node state)  
  - Tick-safe restore  
  - No partial commits / no duplicate grants :contentReference[oaicite:10]{index=10} :contentReference[oaicite:11]{index=11}  

### Required checkpoint alignment (implementation discipline, not redesign)
- Stage 7 economy mutations must align to a **single persistence checkpoint cycle**:
  - Inventory mutation (PlayerSave scope)
  - Node state mutation (WorldSave scope)
  - Must be flushed/committed as one logical unit (even if stored separately)

### Required but Missing (engine-level enforcement)
- A **Save Checkpoint Orchestrator** that can:
  - Collect pending changes across save scopes
  - Flush them together at a safe boundary (typically end-of-tick or action-resolution boundary)
- A clear rule: **gameplay systems may request a checkpoint**, but must not directly write saves (to prevent independent commits).

---

## 5. Required Engine Scaffolding

> Format: **System** — Responsibility (one sentence) — Status

### Core Loop / Authority
- **GameManager** — Bootstraps and holds references to core managers across scenes. — **Confirmed in foundation scaffolds** :contentReference[oaicite:12]{index=12}  
- **TickManager** — Owns authoritative 10 Hz tick index and exposes deterministic tick notifications. — **Confirmed in foundation scaffolds** :contentReference[oaicite:13]{index=13}  
- **NetworkManager** — Establishes host/client roles and message flow entry point for player requests. — **Confirmed in module list** :contentReference[oaicite:14]{index=14}  

### World / Zone Ownership
- **WorldManager** — Owns zone load/unload and world object lifetime. — **Confirmed** :contentReference[oaicite:15]{index=15}  
- **ZoneManager** — Owns per-zone instance containers (where ResourceNode instances should reside). — **Confirmed** :contentReference[oaicite:16]{index=16}  
- **Zone Lifecycle Hooks** — Explicit callbacks/events for “zone loaded” and “zone unloading/unloaded.” — **Required but missing/not specified**

### Player Session / Identity
- **Player Session Manager** — Resolves PlayerId, binds session to inventory state, governs connect/disconnect boundaries. — **Required but missing/not specified**
- **Server Action Router / Command Queue** — Serializes gather/craft requests into deterministic processing order (preferably tick-aligned). — **Required but missing/not specified**

### Messaging / Events
- **Server Event Dispatch** — Publishes informational events (GatheringResolutionResult, ResourceGrantedEvent, CraftingExecutionResult) without UI coupling. — **Required but missing/not specified** (Stage 8.0 calls this out as needed scaffolding) :contentReference[oaicite:17]{index=17}  

### Persistence
- **SaveSystem** — Owns save/load boundaries and JSON persistence entry points. — **Confirmed as module** :contentReference[oaicite:18]{index=18}  
- **PlayerSave Manager** — Owns PlayerSave scope state in memory and exposes checkpoint requests. — **Required but missing/not specified**
- **WorldSave Manager** — Owns WorldSave scope state in memory and exposes checkpoint requests. — **Required but missing/not specified**
- **Checkpoint Coordinator** — Flushes both save scopes together as one logical checkpoint cycle. — **Required but missing/not specified**

---

## 6. Ordering & Dependency Constraints

### Initialization order (must be respected)
1. **GameManager boot** (service container ready) :contentReference[oaicite:19]{index=19}  
2. **Load content databases** (items/skills/recipes/zones/etc.) :contentReference[oaicite:20]{index=20}  
3. **Load saves** (PlayerSave + WorldSave) :contentReference[oaicite:21]{index=21}  
4. **Resolve IDs** via databases :contentReference[oaicite:22]{index=22}  
5. **Zone load** (instantiate node instances into zone state containers)  
6. **Begin simulation loop** (TickManager drives tick) :contentReference[oaicite:23]{index=23}  

### Systems that must never depend on each other (directionality constraints)
- **Stage 7 runtime systems must not depend on UI** (UI is downstream only). (Supported by modular diagram separation of UIManager from core simulation path.) :contentReference[oaicite:24]{index=24}  
- **Inventory/Crafting/Economy systems must not write persistence directly**; they must only request checkpoints through persistence orchestration (to uphold Stage 7.5 atomicity guarantees without glue logic drift).

### Critical ordering assumptions for implementers
- Economy resolution occurs in a stable phase of the host tick where:
  - Inputs are already gathered/validated
  - Mutations occur deterministically
  - Snapshots/events are emitted after resolution
  - Persistence checkpoint (if requested by the action) occurs before the tick is considered complete  
(“host executes all authoritative logic… construct and send state snapshots” implies tick-phase ordering as a core concept). :contentReference[oaicite:25]{index=25}  

---

## Conclusion: Readiness Verdict

### Ready (confirmed anchors exist)
- Global authoritative 10 Hz tick model and host authority assumptions are canon-aligned and explicitly documented. :contentReference[oaicite:26]{index=26}  
- World/Zone ownership model exists at the module boundary level and supports “fixed nodes in world” conceptually. :contentReference[oaicite:27]{index=27}  
- Save/load inclusion in boot pipeline (PlayerSave + WorldSave) is compatible with Stage 7.5 persistence boundaries. :contentReference[oaicite:28]{index=28}  

### Not yet specified (must be stubbed before Stage 7 implementation to avoid glue invention)
- Zone lifecycle hooks (load/unload events)
- Player session identity manager + deterministic action serialization
- Server-side event dispatch mechanism
- Persistence checkpoint coordinator across PlayerSave + WorldSave scopes

### Redesign risk?
- **No.** All missing items are **engine scaffolding/services** already anticipated by Stage 8.0 and the Phase 1.4 modular foundation. :contentReference[oaicite:29]{index=29}  
They can be added as stubs or thin implementations without changing any Stage 7 system behavior or schema assumptions.
