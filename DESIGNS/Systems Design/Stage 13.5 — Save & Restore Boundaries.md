# Stage 13.5 — Save & Restore Boundaries

## 1. Purpose

This document defines the authoritative boundaries between **persisted truth** and **runtime state** in Caelmor.
It specifies when saving is legally permitted, when it is forbidden, and how restore must occur deterministically for both player and world state.
All future systems must treat this document as binding and compatible with Stages 13.1–13.4, Stages 7–8, Stages 10–12, and Stage 9 validation philosophy.

## 2. Persisted Truth vs Runtime State

**Persisted Truth**

Persisted truth is the authoritative state that survives process termination and is used for restore.

- **PlayerSave** and **WorldSave** **must** be treated as persisted truth.
- Persisted truth **must** be sufficient to restore valid gameplay state without inference.
- Persisted truth **must not** require replay of gameplay logic.
- Persisted truth **must not** depend on runtime-only memory, caches, queues, or guards.

**Runtime State**

Runtime state is all state that exists only during live execution.

- Runtime state **must not** be authoritative.
- Runtime state **must not** be replayed, inferred, or reconstructed during restore.
- Runtime state **must** be treated as discardable at any interruption.

**Replay Prohibition**

- Replay of combat, economy, crafting, gathering, or quest logic **is forbidden**.
- Restore **must** rely exclusively on persisted truth.

## 3. Save Boundaries

**General Rules**

- Saves **must** occur only at explicit, server-defined safe boundaries.
- Saves **must not** occur mid-tick.
- Partial saves **are forbidden**.
- Cross-system atomicity **must** be enforced wherever multiple systems contribute to persisted truth.

**PlayerSave Boundaries**

PlayerSave snapshots **may occur only** when all of the following are true:
- The Player Session is not mid-tick.
- No combat resolution, crafting resolution, gathering resolution, or quest resolution is in progress for the player.
- Player state is internally consistent and fully resolved.

PlayerSave snapshots **must not** occur:
- Mid-tick.
- During combat resolution.
- During crafting or gathering resolution.
- While any authoritative system holds unresolved outcomes for the player.

**WorldSave Boundaries**

WorldSave snapshots **may occur only** when:
- The world is at an explicit safe boundary defined by the server.
- No per-tick logic is executing.
- World state is internally consistent and fully resolved.

WorldSave snapshots **must not** occur:
- Mid-tick.
- While combat, economy, or other authoritative systems are mid-resolution.
- While any partial world state exists.

## 4. Restore Semantics

**General Restore Rules**

- Restore **must** use persisted truth only.
- Restore **must not** replay or infer runtime state.
- Restore **must not** resume tick participation automatically.
- Restore **must** produce the same authoritative state given the same persisted inputs.

**Clean Disconnect Restore**

- PlayerSave **must** be restored as persisted truth.
- Player Identity **must** remain valid.
- No Player Session **may** resume as active or tick-participating.

**Unclean Disconnect Restore**

- PlayerSave **must** be restored from last persisted snapshot.
- Any runtime state after the last save **must** be discarded.
- No Player Session **may** resume as active or tick-participating.

**Server Restart Restore**

- All Player Sessions **must** be treated as non-existent.
- All world attachments, zone residencies, and tick participation **must** be treated as non-existent.
- PlayerSave and WorldSave **must** be restored as authoritative truth only.

## 5. Disconnect Handling

**Disconnect During Tick Participation**

- The current tick **must** complete deterministically.
- No additional runtime state **may** be persisted unless a valid save boundary is reached.
- The Player Session **must** be deactivated after the tick boundary.
- PlayerSave **must** reflect only valid persisted truth.

**Disconnect During Combat Resolution**

- Combat resolution **must** complete deterministically for the current tick.
- No partial combat state **may** be persisted.
- Persisted results **must** reflect either:
  - the fully resolved outcome if a save boundary is reached, or
  - the last valid persisted state if no boundary is reached.

**Disconnect During Crafting or Gathering**

- Crafting or gathering resolution **must** complete deterministically for the current tick.
- Partial progress **must not** be persisted.
- Persisted state **must** reflect only fully resolved outcomes at valid save boundaries.

## 6. Crash Handling

**Crash During Tick Execution**

- All runtime state for the active tick **must** be discarded.
- Persisted truth **must** remain unchanged.
- Restore **must** resume from the last completed save boundary.

**Crash During Save Operation**

- Saves **must** be atomic.
- A save **must** result in either:
  - the previous persisted state remaining intact, or
  - a fully written new persisted state.
- Partially written or corrupted saves **must never** be treated as valid.

## 7. Save & Restore Invariants

The following invariants are mandatory and enforceable by validation:

1. **Authoritative Persistence**
   - PlayerSave and WorldSave **must** be the sole sources of persisted truth.

2. **No Replay**
   - Restore **must not** replay gameplay logic of any kind.

3. **Boundary Safety**
   - Saves **must** occur only at explicit, safe boundaries.
   - Saves **must not** occur mid-tick or mid-resolution.

4. **Atomicity**
   - Persisted state **must** be written atomically.
   - Partial saves **must never** be observable.

5. **Discard on Failure**
   - Any runtime state not captured in persisted truth **must** be discarded on disconnect or crash.

6. **No Automatic Resumption**
   - No Player Session, world attachment, zone residency, or tick participation **may** resume automatically after restore.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Save file formats or storage backends
- Database layouts or serialization mechanisms
- Autosave cadence, frequency, or scheduling
- Rollback, replay, reconciliation, or compensation systems
- Client-driven saving or restore authority
- UI, menus, or user-facing save concepts
