# Stage 7.5 — Persistence & Save Integration  
**Design Reference Document**

---

## 1. Overview

Stage 7.5 defines **persistence boundaries and save-state integration** for Caelmor’s non-combat economy runtime systems:

- Stage 7.1: Resource Node Runtime
- Stage 7.3: Inventory & Resource Grant
- Stage 7.4: Crafting Execution

This document specifies **what state must persist**, **when persistence occurs**, and **how restore rehydrates deterministic runtime state**.

It intentionally does **not** define:
- serialization formats
- database technology
- migration or backup strategies
- save frequency tuning

Those concerns belong to infrastructure and operations layers.

---

## 2. High-Level Persistence Architecture

### Authority & Determinism

All persisted state is written by the **authoritative host/server** and restored into authoritative runtime systems.

Determinism is preserved by:
- Persisting **tick-based scheduling state**, not wall-clock time
- Never replaying events (only restoring state)
- Ensuring inventory and node mutations caused by a single action are treated as a **single logical transaction**

### Save Scope Ownership

Persistence is split along canonical boundaries:

- **PlayerSave**
  - Player-owned economy state (inventory, known recipes if canonical)
- **WorldSave**
  - World-owned economy state (resource node runtime overrides)

---

## 3. Persisted vs Non-Persisted State

### Persisted State (Required)

| System | State Element | Save Scope | Notes |
|---|---|---|---|
| Inventory | ResourceItemKey → Count | PlayerSave | Core player economy state |
| Resource Nodes | Node availability (available/depleted) | WorldSave | Prevents duplication |
| Resource Nodes | Respawn scheduling (ticks remaining) | WorldSave | Preserves deterministic respawn |
| Crafting | Known recipes (if canonical) | PlayerSave | Only if already part of PlayerSave |

### Non-Persisted State (Explicit)

- Gathering resolution results
- Informational events (grants, crafts)
- Validation intermediates
- UI-facing or client-facing state
- Any derived or replayable data

---

## 4. Node Instance Identity Ownership

**NodeInstanceId values are assigned by world/zone content placement.**

Persistence:
- Stores **runtime overrides only**
- Keys overrides by stable `NodeInstanceId`
- Never generates new NodeInstanceIds at runtime

Runtime systems must always treat NodeInstanceIds as immutable identifiers originating from content definitions.

---

## 5. Save Boundaries (When Persistence Occurs)

This section defines **logical boundaries**, not save frequency.

### A) On State Mutation (Dirty Marking)

When authoritative state mutates:
- Inventory mutation → mark PlayerSave dirty
- Node state mutation → mark WorldSave dirty

No save is forced immediately; state is marked for later flush.

### B) Checkpoint Cycle

At a checkpoint opportunity (implementation-defined):
- Flush all dirty PlayerSave entries
- Flush WorldSave if dirty

### C) Player Disconnect

On authoritative disconnect handling:
- Flush that player’s PlayerSave if dirty
- Ensure no in-flight inventory mutation remains uncommitted

### D) Graceful Server Shutdown

On shutdown:
- Flush all dirty PlayerSave data
- Flush WorldSave
- Use atomic write semantics

---

## 6. Restore Logic

Restore must rehydrate runtime systems **without duplication** and **with preserved scheduling semantics**.

### A) Server Startup (Host Boot)

**Locked v1 Decision — Respawn Scheduling**

> Respawn scheduling is persisted as **ticks remaining** at save time.  
> On restore, `respawn_tick` is recomputed relative to the new tick base.

This avoids reliance on a persisted absolute world tick index.

**Startup Flow**
1. Load immutable content databases
2. Load WorldSave
3. Rehydrate ResourceNodeSystem:
   - Apply node availability overrides
   - Recompute respawn_tick using persisted ticks_remaining
4. Rebuild respawn scheduler
5. Start tick loop

### B) Zone Load

**Zone Rehydration Flow**
1. Load zone content placements
2. Apply WorldSave overrides by NodeInstanceId
3. Default nodes without overrides to available
4. Rebuild respawn scheduler entries for depleted nodes

### C) Player Reconnect

**Reconnect Flow**
1. Load PlayerSave
2. Rehydrate inventory state
3. Rehydrate known recipes (if canonical)
4. Join world

**Duplication Rule**
- No events are replayed
- Only persisted state is restored

---

## 7. Transaction Boundaries & Atomicity

### Logical Transaction Definition

A single gameplay action (e.g. gather or craft) may mutate:
- Player inventory (PlayerSave)
- Node runtime state (WorldSave)

**Clarification (Locked):**
- Inventory mutation and node state mutation caused by the same action  
  **must be flushed in the same persistence checkpoint cycle**
- They may live in different save scopes
- They must not be committed independently

This guarantees:
- No double grants
- No orphaned node depletion
- No partial craft consumption

### Atomic Save Expectation

Persistence must ensure:
- Either the previous committed state remains valid, or
- The new state is fully committed

Partial saves must never be observable after restore.

---

## 8. Save / Restore Flow Diagrams (Textual)

### Save Flow

```text
[Economy Mutation]
   ├─ Inventory changed → PlayerSave dirty
   ├─ Node state changed → WorldSave dirty

[Checkpoint / Disconnect / Shutdown]
   ├─ Flush PlayerSave (if dirty)
   ├─ Flush WorldSave (if dirty)
   └─ Clear dirty flags only after commit succeeds
Restore Flow — Startup
[Boot]
  ↓ Load Content
  ↓ Load WorldSave
  ↓ Rehydrate Node States
  ↓ Recompute Respawn Ticks
  ↓ Start Tick Loop

Restore Flow — Player Reconnect
[Player Connect]
  ↓ Load PlayerSave
  ↓ Rehydrate Inventory
  ↓ Rehydrate Known Recipes
  ↓ Join World

9. Conceptual Persisted Data Shapes (Illustrative Only)
Player Economy State
struct PersistedInventoryEntry
{
    string ResourceItemKey;
    int Count;
}

struct PersistedPlayerEconomyState
{
    string CharacterId;
    List<PersistedInventoryEntry> Inventory;
    List<string> KnownRecipeKeys; // only if canonical
}

World Node Overrides
enum PersistedNodeState
{
    Available,
    Depleted
}

struct PersistedNodeInstanceOverride
{
    int NodeInstanceId;
    PersistedNodeState State;
    int TicksRemaining; // used to recompute respawn_tick on restore
}

10. Failure Cases & Recovery Behavior
Crash Mid-Save
Atomic write guarantees old or new state survives intact

Crash After Mutation, Before Save Commit
Restore yields last committed state
No replay of grants or crafts

Missing Node Override
Node defaults to available
Correct behavior

Invalid Persisted Inventory
Clamp or discard invalid entries deterministically
Emit diagnostics
Continue with safe state

11. Future Extension Points (Not Implemented)
Time-based crafting queues
Partitioned world saves
Audit trails for economy actions
Network reconciliation layers

These do not alter Stage 7.5 responsibilities.

12. Non-Goals
This design does not include:
database selection
serialization format decisions
migration tooling
backup strategies
versioning logic
save frequency tuning