# Stage 19.5 — Spawn / Despawn Semantics

## 1. Purpose

This document defines the **authoritative runtime semantics** for spawning and despawning entities in Caelmor.
It establishes what spawn and despawn mean structurally, which entities are subject to these rules, who has authority, and the exact ordering guarantees required for determinism and restore safety.
This document introduces no content, placement logic, or implementation details.

## 2. Scope

This document applies exclusively to **server-authoritative runtime entity existence semantics** at 10 Hz.
It governs when entities may begin or cease authoritative evaluation within a world and zone context.
It does not define encounter design, geometry, triggers, AI behavior, or engine internals.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 19.0 — World Simulation & Zone Runtime Architecture
- Stage 19.1 — Zone Runtime Definition
- Stage 19.2 — World Runtime Definition
- Stage 19.3 — World & Zone Authority Boundaries
- Stage 19.4 — Zone Residency Constraints
- Stage 13 — Player Lifecycle & World Session Authority
- Stage 16.1 — NPC Runtime Model
- Stage 17.1 — Item Runtime Model

If any conflict exists, the above documents take precedence.

## 4. Spawn / Despawn Definitions

**Spawn**

Spawn is the **server-authoritative transition** by which a runtime entity becomes a **legal participant** in world and zone-scoped evaluation.

**Despawn**

Despawn is the **server-authoritative transition** by which a runtime entity ceases to be a **legal participant** in world and zone-scoped evaluation.

**Existence Rule**
- An entity is either spawned or not spawned.
- No intermediate, partial, or transitional existence state is permitted.

## 5. Spawn Authority Rules

**Authority**
- All spawn decisions **must** be server-owned.
- Clients **must never** author, request, or influence spawn decisions.
- Zones **must not** spawn entities.
- Entities **must not** self-spawn.

**Eligibility Preconditions**
An entity **must not** be spawned unless all of the following are true:
- A valid world runtime exists and is active.
- Valid world attachment is established.
- Valid zone residency is assigned where required.
- The spawn occurs at an explicit tick boundary.

**Scope**
- NPC runtime instances **must** obey spawn rules.
- World-owned item runtime instances **must** obey spawn rules.
- Player sessions **must not** be spawned; player participation is governed exclusively by Stage 13.
- Quest instances **must not** be spawned or despawned.

## 6. Despawn Authority Rules

**Authority**
- All despawn decisions **must** be server-owned.
- Clients **must never** author or influence despawn decisions.
- Zones **must not** despawn entities.
- Entities **must not** self-despawn.

**Rules**
- Despawn **must** occur only at explicit tick boundaries.
- Despawn **must** deterministically remove the entity from all evaluation.
- Despawn **must not** imply destruction of persisted ownership or identity unless defined by owning systems.

## 7. Ordering & Tick Interaction

**Ordering Rules**
- Spawn **must** occur only at tick boundaries before evaluation begins.
- Despawn **must** occur only at tick boundaries after evaluation completes.
- No entity **may** be evaluated in a tick before it is spawned.
- No entity **may** be evaluated in a tick after it is despawned.

**Interaction with Residency**
- Spawn **must** occur only after valid zone residency is assigned.
- Despawn **must** occur before zone residency is cleared.

**Atomicity**
- Spawn and despawn transitions **must** be atomic.
- No partial evaluation **may** occur during a spawn or despawn transition.

## 8. Persistence & Restore Interaction

**Persistence Rules**
- Spawn state **must** be reflected in authoritative persisted truth when required by owning systems.
- Runtime-only spawn state **must not** be persisted.

**Restore Rules**
- Restore **must** reconstruct spawn state solely from persisted authoritative truth.
- No entity **may** resume evaluation unless it is restored as spawned.
- Spawn or despawn transitions **must not** resume, replay, or complete on restore.

## 9. Forbidden Spawn / Despawn States

The following states **must never exist** and **must be validation-rejectable**:

- Spawn or despawn occurring mid-tick
- Entity evaluation before spawn
- Entity evaluation after despawn
- Spawn without valid world attachment
- Spawn without valid zone residency where required
- Client-authored or client-influenced spawn or despawn
- Zone-authored spawn or despawn
- Partial spawn or partial despawn persisted across restore

No exception paths are permitted.

## 10. Spawn / Despawn Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **Server Authority**
   - All spawn and despawn transitions **must** be server-owned.

2. **Binary Existence**
   - An entity **must** be either spawned or not spawned, never both.

3. **Tick Safety**
   - Spawn and despawn **must not** occur outside tick boundaries.

4. **Residency Integrity**
   - No entity **may** be spawned without valid zone residency when required.

5. **Restore Safety**
   - Spawn state **must not** rely on replay, inference, or runtime continuation.

6. **No Delegation**
   - Spawn and despawn authority **must not** be delegated downward.

## 11. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Spawn and despawn semantics are explicit, binary, and authoritative.
- Ordering relative to tick, world attachment, and residency is unambiguous.
- All illegal states are enumerated and validation-rejectable.
- Persistence and restore behavior is deterministic and replay-free.
- No modal or speculative language remains.
- Validation harnesses can deterministically accept or reject spawn state.
