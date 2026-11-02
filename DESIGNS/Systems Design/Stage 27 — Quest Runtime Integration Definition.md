# Stage 27 — Quest Runtime Integration Definition

**Creative Director ruling — 2026-11-02:** The approved lifecycle is exactly **Inactive, Active, Completed**, aligned with Stage 15.2. The former Failed state and proposals for Abandoned/re-offer are superseded. Players may leave, die, disconnect and retry without losing an Active quest.

## Purpose
Define the **authoritative runtime contract** for quests as deterministic, server-authoritative state machines that integrate with player lifecycle, inventory, combat, and world simulation without violating Phase 1.4 constraints.

This stage specifies **how quests exist at runtime**, how quest state progresses, and when quest systems may read or mutate state.

This document is a **binding contract**. No code is implemented here.

---

## Scope Clarification

### This Stage Owns
- Runtime representation of quest state
- Quest activation, progression, and completion rules
- Quest eligibility gates
- Deterministic quest state transitions

### This Stage Does NOT Own
- Quest narrative content or writing
- Quest data schemas or authoring tools
- UI presentation or journal display
- Persistence IO or serialization
- Combat resolution logic
- NPC dialogue logic
- Tick execution (see Stage 28)

---

## Core Concepts

### Quest
A **Quest** is a server-authoritative runtime state machine representing a structured objective chain.

- Quests have a stable `QuestInstanceId`
- Quests reference immutable content definitions
- Quest state is never client-authored

### Quest State
Quest state represents the player’s progress through a quest.

- State transitions are explicit
- State transitions are deterministic
- State transitions are ordered

---

## Quest Runtime States

Quests may exist in one of the following runtime states:

1. **Inactive**
   - Quest is not yet started
   - Progression checks are not eligible; explicit authoritative activation is allowed

2. **Active**
   - Quest is in progress
   - Eligible for progression checks

3. **Completed**
   - Quest objectives satisfied
   - Completion effects may be granted

Only `Inactive → Active` and `Active → Completed` change lifecycle state. Completed is terminal. Repeated acknowledgement of an already-applied legal transition may be idempotent; it must never replay rewards or reset progress. Runtime enum values remain Inactive = 0, Active = 1, Completed = 2.

---

## State Invariants (Hard Rules)

The following invariants MUST always hold:

1. Quest state is server-authoritative only.
2. Quest state transitions are explicit and ordered.
3. Quest state may not change mid-tick.
4. Quest state transitions are deterministic.
5. Quest state is stable during simulation execution.
6. A quest may not be both Active and Completed.
7. Exactly the three listed lifecycle states are legal; no failure or abandonment transition exists.
8. Leaving, death, disconnect or encounter retry preserves the Active instance and committed progress. No replacement instance is created to restart a quest.

Violation of any invariant is a fatal runtime error.

---

## Quest Progression Rules

Quest progression may be triggered by:
- World events
- Combat outcomes
- Inventory changes
- NPC interactions

### Progression Requirements
- Progression checks occur outside simulation ticks
- Progression checks must validate eligibility
- Progression must not mutate unrelated systems
- Progression must leave no partial state on failure
- Rejected operations and unsuccessful encounter/action attempts do not permanently fail quests

---

## Ordering Guarantees

- Quest progression occurs **after** simulation execution
- Quest progression occurs **before** persistence save windows
- Quest state is read-only during simulation ticks

---

## Interaction Contracts

### With Player Lifecycle
- Only Active players may progress quests
- Suspended players may not progress quests

### With World Simulation
- Simulation may emit events consumed by quest systems
- Quest systems do not mutate simulation state

### With Inventory and Combat
- Quest systems may read inventory and combat outcomes
- Quest systems may not directly modify combat or inventory state

### With Persistence
- Quest state changes may be marked dirty for save
- Quest systems do not perform IO directly
- Active state, committed objective progress, evidence, counters and meaningful choice records survive supported recovery/restore boundaries
- Transient carries, channels and encounters use authored retry/reacquisition paths without removing the Active quest or undoing persistent consequences

---

## Failure Modes

The quest runtime must fail deterministically if:
- Invalid state transitions are attempted
- Progression is attempted mid-tick
- Quest instance references are invalid

Failures must:
- Leave no partial quest state
- Be observable by callers

---

## Explicitly Forbidden Behaviors

The following are explicitly forbidden:

- Client-authored quest state changes
- Implicit quest activation or completion
- Quest logic mutating lifecycle, residency, or simulation state
- Non-deterministic quest progression
- Quest progression during simulation execution
- Permanent quest failure, voluntary abandonment, or resetting an Active quest to Inactive
- Recovery that makes a required objective permanently inaccessible

Any implementation exhibiting these behaviors is invalid.

---

## Validation Expectations (Future Stage)

Future validation stages must prove:
- Deterministic quest progression
- Enforcement of eligibility gates
- No mid-tick quest state mutation
- Correct interaction with simulation, combat, and inventory
- Exactly Inactive, Active and Completed; invalid evaluator results leave Active state unchanged
- Leaving, death, disconnect and encounter retry retain Active progress and meaningful choices
- Required carries/items can be recovered without duplicate grants and every required objective retains a valid completion path
- Completed state and reward receipts remain stable across duplicate events and restore

This document is the sole authority for quest runtime correctness.
