# Stage 24 — NPC Runtime Architecture Definition

## Purpose
Define the **authoritative runtime contract** for Non-Player Characters (NPCs) as simulation participants within the Caelmor world.

This stage specifies **what an NPC is at runtime**, how NPCs participate in simulation, and what boundaries NPC systems must obey. It ensures NPC behavior integrates cleanly with zones, lifecycle rules, and the world simulation core without violating determinism or authority.

This document is a **binding contract**. No code is implemented here.

---

## Scope Clarification

### This Stage Owns
- NPC runtime identity and instance existence
- NPC eligibility for simulation
- NPC participation in zone-based simulation
- High-level NPC state categories (not AI logic)
- NPC lifecycle boundaries relative to simulation

### This Stage Does NOT Own
- NPC AI decision-making logic
- Combat resolution
- Dialogue systems
- Quest logic
- Persistence schema or save IO
- Zone residency rules (see Stage 23.3)
- Tick execution (see Stage 28)

---

## Core Concepts

### NPC
An **NPC** is a server-authoritative runtime entity that:
- Exists independently of player sessions
- May be simulated within a zone
- May interact with players, the world, and other NPCs
- Obeys the same simulation invariants as players

NPCs are **not clients** and have no session representation.

---

## NPC Runtime Identity

- Each NPC has a stable, server-defined `NpcId`
- NPC identity is never client-authored
- NPC identity remains stable across simulation ticks
- NPC identity may persist across sessions or restarts (persistence handled elsewhere)

---

## NPC Runtime States

NPCs exist in one of the following runtime states:

1. **Spawned**
   - NPC instance exists
   - Not yet simulated

2. **Active**
   - NPC is resident in a zone
   - Eligible for simulation

3. **Dormant**
   - NPC exists but is not simulated
   - Used for unloaded zones or scripted pauses

4. **Despawned**
   - NPC instance is removed from runtime
   - No simulation allowed

---

## State Invariants (Hard Rules)

The following invariants MUST always hold:

1. NPCs may only be simulated while in **Active** state.
2. NPCs may be resident in **exactly one zone** at a time.
3. NPC state changes are **server-authoritative only**.
4. NPC state changes are **explicit and ordered**.
5. NPC state may not change mid-tick.
6. NPC simulation eligibility is evaluated before each tick.

Violation of any invariant is a fatal runtime error.

---

## Zone Integration

- NPCs must be explicitly attached to a zone before simulation.
- Zone residency rules apply equally to NPCs and players.
- NPCs may not transition zones mid-tick.
- NPCs without zone residency are excluded from simulation.

---

## Simulation Integration

- NPCs participate in simulation during the **Simulation Execution** phase only.
- NPC simulation must obey:
  - deterministic ordering
  - no side effects outside the tick boundary
- NPC logic must not mutate lifecycle, residency, or eligibility state during simulation.

---

## Failure Modes

The NPC runtime must fail deterministically if:
- An NPC is simulated without zone residency
- An NPC transitions state mid-tick
- Multiple zone residency is attempted
- NPC simulation violates deterministic ordering

Failures must:
- Leave no partial state
- Be observable by callers

---

## Interaction Contracts

### With World Simulation Core
- NPCs are evaluated for eligibility before each tick
- NPCs execute only within tick boundaries

### With Zone Residency
- NPCs require explicit residency to simulate
- Residency attach/detach is ordered outside ticks

### With Combat and AI Systems
- AI and combat systems operate on NPCs only while Active
- These systems may not change NPC eligibility or residency

---

## Explicitly Forbidden Behaviors

The following are explicitly forbidden:

- Client-authored NPC behavior or state
- NPC state changes mid-tick
- NPC-driven lifecycle changes of players
- NPC simulation outside tick execution
- Implicit NPC spawning or despawning

Any implementation exhibiting these behaviors is invalid.

---

## Validation Expectations (Future Stage)

Future validation stages must prove:
- NPC simulation eligibility enforcement
- Zone residency invariants
- Deterministic NPC execution
- Correct exclusion of dormant or despawned NPCs

This document is the sole authority for NPC runtime correctness.
