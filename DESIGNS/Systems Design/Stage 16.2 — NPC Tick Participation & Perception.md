# Stage 16.2 — NPC Tick Participation & Perception

## 1. Purpose

This document defines the authoritative rules governing **NPC tick participation** and the **structural perception model** for NPCs.
It establishes when NPCs participate in the server tick, what perception means at a system level, and how ordering and determinism are enforced.
This document introduces no AI behavior, decision-making, or content logic.

## 2. NPC Tick Participation Definition

**NPC Tick Participation**

NPC tick participation is the server-defined state in which an NPC runtime instance is included in authoritative per-tick system processing.

**Rules**
- NPC tick participation **must** be server-defined and server-owned.
- NPC tick participation **must** be binary: participating or not participating.
- NPC tick participation **must not** be gradual, partial, or conditional.
- NPC tick participation **must** be independent of player tick participation.
- An NPC runtime instance **must not** participate in the tick unless explicitly included by the server.

## 3. Tick Entry & Exit Rules

**Tick Entry Conditions**

An NPC runtime instance **must** enter tick participation only when all of the following are true:
- The NPC exists in a valid world context.
- The NPC has valid zone residency within that world.
- The world and zone are active.
- The server explicitly includes the NPC at a tick boundary.

**Tick Exit Conditions**

An NPC runtime instance **must** exit tick participation when any of the following occur:
- The NPC is despawned or destroyed.
- The NPC loses valid world attachment.
- The NPC loses valid zone residency.
- The world or zone becomes inactive.

**Boundary Rules**
- Tick entry **must** occur only at explicit tick boundaries.
- Tick exit **must** occur only at explicit tick boundaries.
- NPCs **must not** enter or exit tick participation mid-tick.
- All tick entry and exit ordering **must** be server-owned and deterministic.

## 4. NPC Perception Model

**Definition**

NPC perception is the passive, server-controlled observation of authoritative world state available to an NPC during tick participation.

**Rules**
- NPC perception **must** be passive observation only.
- NPC perception **must not** imply awareness, intent, decision-making, or behavior.
- NPC perception **must not** guarantee reaction, response, or action.
- NPC perception **must** occur only while the NPC is tick-participating.
- NPC perception **must not** exist outside authoritative tick participation.

## 5. Perception Scope & Limits

**Allowed Perception Scope**

While tick-participating, an NPC **must perceive only** the following authoritative server state:
- Server-recognized entities within its world context.
- Server-recognized state changes scoped to its zone.
- Server-recognized events explicitly scoped to the NPC’s world or zone.

An NPC **must not** perceive anything outside this allowed scope.

**Forbidden Perception**

An NPC **must not** perceive:
- Client-authored or client-suggested state.
- State outside its world context.
- State outside its zone residency.
- Future, inferred, or speculative state.
- Any data not recognized as authoritative server state.

**Scope Enforcement**
- Perception scope **must** be enforced by world attachment and zone residency.
- Perception **must not** bypass authority, save, or restore boundaries.

## 6. Ordering & Determinism Guarantees

The following guarantees are mandatory and enforceable by validation:

- NPC perception **must** occur only during authoritative tick participation.
- NPC perception **must** follow server-defined, deterministic ordering.
- NPC perception **must not** influence tick ordering or system execution order.
- NPC perception **must not** create or mutate authoritative state directly.
- NPC perception **must not** bypass save or restore rules defined in Stage 13.

## 7. Failure & Edge Case Handling

The following cases **must** be handled deterministically:

**NPC Spawn or Activation Mid-Tick**
- Tick participation **must** be deferred until the next tick boundary.
- No perception **must** occur during the current tick.

**NPC Despawn or Deactivation Mid-Tick**
- Tick exit **must** be deferred until the next tick boundary.
- No partial tick participation **must** apply.

**Server Crash During NPC Tick Participation**
- All NPC runtime-only tick and perception state **must** be discarded.
- NPC restore **must** rely solely on persisted world state or deterministic regeneration.
- No tick participation **must** resume automatically on restore.

**Restore Behavior**
- NPCs **must** re-enter tick participation only through normal tick entry rules.
- Perception state **must not** persist across restore.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- AI behavior, reasoning, or decision-making
- Behavior trees, planners, or state machines
- Pathfinding, navigation, or movement logic
- Combat logic, threat evaluation, or targeting
- Client-side NPC perception or authority
- UI, presentation, or visualization systems
- Engine internals or implementation details
