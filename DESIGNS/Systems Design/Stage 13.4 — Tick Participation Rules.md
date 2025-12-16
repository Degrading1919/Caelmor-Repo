# Stage 13.4 — Tick Participation Rules

## 1. Purpose

This document defines the canonical, server-authoritative rules governing **tick participation** for Player Sessions in Caelmor.
It specifies when a Player Session participates in the authoritative server tick, how participation begins and ends, and how participation is ordered relative to other systems.
All future systems must treat this document as authoritative and compatible with Stages 13.1–13.3 and Stage 9 validation philosophy.

## 2. Tick Participation Definition

**Tick Participation**  
Tick Participation is the server-defined state in which a Player Session is included in the authoritative 10 Hz server tick and is eligible for per-tick system processing.

**Characteristics**
- Tick Participation **must** be server-defined.
- Tick Participation **must** be binary: a Player Session is either participating or not participating.
- Tick Participation **must not** be partial, gradual, or interpolated.
- Tick Participation **must** be distinct from:
  - Player Session activation,
  - world attachment,
  - zone residency.

**Scope**
- Only Player Sessions that are tick-participating **may** be processed by per-tick gameplay systems.
- Player existence, identity, and persistence **must not** depend on tick participation.

## 3. Entry Into Tick Participation

**Definition**  
Entry into Tick Participation is the server-authoritative transition that includes a Player Session in the next authoritative tick boundary.

**Preconditions**
A Player Session **must not** enter tick participation unless all of the following are true:
- The Player Session is active.
- The Player Session is attached to exactly one world.
- The Player Session has exactly one valid zone residency within that world.

**Rules**
- Entry into tick participation **must** be initiated and ordered by the server.
- Entry into tick participation **must** occur only on an explicit tick boundary.
- Entry into tick participation **must not** occur mid-tick.
- A Player Session **must** be fully attached to a world and zone before entering tick participation.
- Clients **must not** cause, request, accelerate, or delay entry into tick participation.

## 4. Exit From Tick Participation

**Definition**  
Exit from Tick Participation is the server-authoritative transition that excludes a Player Session from the authoritative tick.

**Exit Conditions**
A Player Session **must** exit tick participation if any of the following occur:
- The Player Session is deactivated.
- The Player Session is terminated.
- World attachment is removed.
- Zone residency is removed or becomes invalid.

**Rules**
- Exit from tick participation **must** be initiated and ordered by the server.
- Exit from tick participation **must** occur only on an explicit tick boundary.
- Exit from tick participation **must not** occur mid-tick.
- Once a Player Session exits tick participation, it **must not** be processed by any per-tick system logic.

## 5. Ordering Guarantees

The following ordering guarantees are mandatory:

- A Player Session **must not** participate in combat, crafting, gathering, quest resolution, or any other per-tick gameplay system unless it is tick-participating.
- Tick participation **must** begin before any per-tick system logic is applied to the Player Session.
- Tick participation **must** end only after all per-tick system logic has completed for the final tick in which the session participates.
- All ordering of tick participation entry and exit **must** be deterministic and server-owned.
- Clients **must not** influence ordering or eligibility for tick participation.

## 6. Tick Participation Invariants

The following invariants are mandatory and enforceable by validation:

1. **Binary State**
   - A Player Session **must** be either tick-participating or not tick-participating.
   - No intermediate or transitional tick participation states are allowed.

2. **Boundary Safety**
   - Tick participation **must** change only at explicit tick boundaries.
   - A Player Session **must never** partially participate in a tick.

3. **Prerequisite Enforcement**
   - A Player Session **cannot** be tick-participating unless it is active, world-attached, and zone-resident.

4. **Server Authority**
   - All tick participation state changes **must** be initiated and ordered by the server.
   - Clients **must never** control tick participation.

5. **Isolation**
   - Non-participating Player Sessions **must** be completely excluded from per-tick system processing.

## 7. Failure & Edge Case Handling

The following cases **must** be handled deterministically:

**Session Activation Completing Mid-Tick**
- The Player Session **must not** enter tick participation during the current tick.
- Tick participation **must** begin, if eligible, at the next tick boundary.

**Session Deactivation Requested Mid-Tick**
- The Player Session **must** remain tick-participating for the remainder of the current tick.
- Exit from tick participation **must** occur at the next tick boundary.

**World Detachment During a Tick**
- The Player Session **must** remain tick-participating for the remainder of the current tick.
- Exit from tick participation **must** occur at the next tick boundary.

**Server Crash During Tick Participation**
- All tick participation state **must** be treated as non-existent on restore.
- No Player Session **may** resume as tick-participating after restore.

**Restore Behavior**
- Player Identity and PlayerSave **must** be restored from persisted truth.
- Tick participation **must** be re-established only through normal lifecycle rules.
- No tick participation state **may** be inferred, replayed, or assumed on restore.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Tick phases, system execution order, or engine internals
- Combat, economy, crafting, or quest resolution logic
- Save timing, persistence cadence, or snapshot rules
- Client prediction, rollback, reconciliation, or compensation
- Networking transport, replication, or optimization
- UI, presentation, or user-facing tick concepts
