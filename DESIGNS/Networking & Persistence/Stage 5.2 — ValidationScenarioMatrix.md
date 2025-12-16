# Stage 9.1 — Validation Scenario Matrix  
**Scope:** Non-Combat Economy, Networking & Persistence  
**Authoritative Systems:** Stage 7–8 (Frozen)

This document defines the **minimum viable validation scenarios** required to trust the correctness of Caelmor’s non-combat economy and persistence layer.

All scenarios assume:
- Server-authoritative execution
- Deterministic 10 Hz tick model
- Atomic inventory and crafting operations
- Save/load hydrates state without replaying gameplay logic

This document defines **what must be validated**, not how it is implemented.

---

## 1. Inventory Determinism & Persistence

### 1.1 Atomic Inventory Grant Persistence

**Category:** Inventory Determinism & Persistence

**Initial Assumptions**
- 1 player connected
- Player inventory empty
- Server tick = T

**Ordered Actions**
1. Player completes a valid gathering interaction at tick T
2. Server grants a single resource item
3. Server writes PlayerSave at tick T+1
4. Player disconnects
5. Player reconnects and PlayerSave is loaded

**Expected Authoritative Outcomes**
- Inventory contains exactly one granted item
- No duplicate or missing items
- No re-execution of grant logic

**Failure Conditions**
- Item missing after reconnect
- Item duplicated
- Grant logic replays on load

---

### 1.2 Deterministic Inventory Mutation Ordering

**Category:** Inventory Determinism & Persistence

**Initial Assumptions**
- 1 player connected
- Inventory contains exactly one resource item
- Server tick = T

**Ordered Actions**
1. Player submits multiple crafting requests within the same server tick
2. All requests target the same inventory item
3. Server resolves requests in a deterministic, authoritative order

**Expected Authoritative Outcomes**
- Exactly one crafting action succeeds
- Exactly one inventory consumption occurs
- Remaining requests are rejected due to authoritative resolution order

**Failure Conditions**
- More than one action succeeds
- Inventory goes negative
- Resolution order is non-deterministic

---

## 2. Resource Node State & Respawn Persistence

### 2.1 Node Depletion Persistence Across Save

**Category:** Resource Node State & Respawn Persistence

**Initial Assumptions**
- 1 player connected
- Resource node is available
- Node respawn tick scheduled at T+R

**Ordered Actions**
1. Player depletes node at tick T
2. Server marks node unavailable
3. WorldSave is written at tick T+1
4. Server shuts down
5. Server restarts and loads WorldSave

**Expected Authoritative Outcomes**
- Node remains unavailable after load
- Respawn tick remains scheduled at T+R
- No early respawn occurs

**Failure Conditions**
- Node resets to available on load
- Respawn tick is lost or recalculated
- Node can be gathered again immediately

---

### 2.2 Node Respawn Determinism After Load

**Category:** Resource Node State & Respawn Persistence

**Initial Assumptions**
- Node is unavailable
- Respawn tick = T+R
- Server tick resumes at T+X where X < R

**Ordered Actions**
1. Server advances ticks normally
2. Tick reaches exactly T+R

**Expected Authoritative Outcomes**
- Node transitions to available exactly at T+R
- Transition occurs once
- Node is gatherable afterward

**Failure Conditions**
- Early respawn
- Delayed respawn
- Multiple respawn transitions

---

## 3. Crafting Atomicity Across Save/Load

### 3.1 Crafting Commit Integrity on Disconnect

**Category:** Crafting Atomicity Across Save/Load

**Initial Assumptions**
- 1 player connected
- Inventory contains valid recipe inputs
- Server tick = T

**Ordered Actions**
1. Player initiates crafting action at tick T
2. Server consumes inputs and produces outputs atomically
3. Player disconnects immediately after
4. Player reconnects

**Expected Authoritative Outcomes**
- Either:
  - Inputs consumed and outputs present, OR
  - No changes occurred
- No partial state possible

**Failure Conditions**
- Inputs consumed without outputs
- Outputs granted without input consumption
- Crafting replays on reconnect

---

### 3.2 Crafting Rejection Persistence

**Category:** Crafting Atomicity Across Save/Load

**Initial Assumptions**
- Inventory lacks required inputs
- Server tick = T

**Ordered Actions**
1. Player attempts crafting action
2. Server rejects recipe
3. Player disconnects and reconnects

**Expected Authoritative Outcomes**
- Inventory unchanged
- No delayed crafting execution

**Failure Conditions**
- Craft executes after reconnect
- Inventory mutated despite rejection

---

## 4. Multi-Actor Resource Contention

### 4.1 Simultaneous Node Interaction Resolution

**Category:** Multi-Actor Resource Contention

**Initial Assumptions**
- 2 players connected
- Node is available
- Server tick = T

**Ordered Actions**
1. Both players initiate gather interaction on same node during tick T

**Expected Authoritative Outcomes**
- Exactly one player succeeds
- Node transitions to unavailable once
- Other player receives deterministic failure

**Failure Conditions**
- Both players succeed
- Node grants twice
- Non-deterministic winner selection

---

### 4.2 Contention Persistence After Save

**Category:** Multi-Actor Resource Contention

**Initial Assumptions**
- Node is depleted by Player A
- Player B’s interaction was rejected
- WorldSave written

**Ordered Actions**
1. Both players disconnect
2. Server restarts
3. WorldSave loaded

**Expected Authoritative Outcomes**
- Node remains unavailable
- No retroactive grant to Player B

**Failure Conditions**
- Node resets
- Player B receives item on reconnect

---

## 5. Reconnect & Session Boundary Integrity

### 5.1 Mid-Tick Disconnect Safety

**Category:** Reconnect & Session Boundary Integrity

**Initial Assumptions**
- Player connected
- Server tick = T

**Ordered Actions**
1. Player initiates valid interaction
2. Player disconnects before tick completes
3. Tick resolves server-side
4. Player reconnects

**Expected Authoritative Outcomes**
- Result reflects server-side resolution only
- No double application
- No rollback of committed state

**Failure Conditions**
- Interaction lost
- Interaction applied twice
- Client-side state leaks into authority

---

### 5.2 Session Resume Without Replay

**Category:** Reconnect & Session Boundary Integrity

**Initial Assumptions**
- Player disconnected after multiple valid actions
- PlayerSave written

**Ordered Actions**
1. Player reconnects
2. PlayerSave loaded

**Expected Authoritative Outcomes**
- State exactly matches save
- No actions replayed
- No timers reset

**Failure Conditions**
- Actions replay
- State diverges from save

---

## 6. Tick-Boundary Edge Conditions

### 6.1 Cross-Tick Action Ordering

**Category:** Tick-Boundary Edge Conditions

**Initial Assumptions**
- Player submits two actions across tick boundary
- Server ticks T and T+1

**Ordered Actions**
1. Action A submitted just before tick T ends
2. Action B submitted just after tick T+1 begins

**Expected Authoritative Outcomes**
- Actions resolved in strict tick order
- Deterministic resolution sequence

**Failure Conditions**
- Order inversion
- Non-deterministic execution

---

### 6.2 Save Request During Active Tick

**Category:** Tick-Boundary Edge Conditions

**Initial Assumptions**
- Save request issued during server tick T
- Pending actions exist

**Ordered Actions**
1. Save is requested during tick T
2. Server completes tick T normally
3. Save commits at the next valid checkpoint boundary
4. Server restarts and loads save

**Expected Authoritative Outcomes**
- Save reflects only fully committed state
- Pending actions are neither partially saved nor replayed
- State after load matches last committed checkpoint

**Failure Conditions**
- Partial state saved
- Pending actions replay
- State divergence after load

---

## Exit Criteria

Stage 9.1 is considered **validated** when:
- All scenarios pass deterministically
- No scenario reveals state duplication, loss, or replay
- All failures are attributable only to implementation bugs, not system design
