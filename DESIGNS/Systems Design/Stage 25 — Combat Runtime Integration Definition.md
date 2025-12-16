# Stage 25 — Combat Runtime Integration Definition

## Purpose
Define the **authoritative runtime contract** for combat as a deterministic simulation subsystem within Caelmor.

This stage specifies **how combat participates in the simulation**, what combat is allowed to read and write, and what ordering and authority rules must be obeyed. It integrates previously locked combat intents and states into the runtime without redefining them.

This document is a **binding contract**. No code is implemented here.

---

## Scope Clarification

### This Stage Owns
- Combat participation in the simulation tick
- Combat execution ordering relative to other systems
- Combat read/write boundaries
- Combat eligibility requirements
- Combat result commitment rules

### This Stage Does NOT Own
- Combat intents or state definitions (see Stage 10.x — LOCKED)
- Animation, VFX, or audio
- Input handling
- AI decision-making
- Persistence IO
- Zone residency rules
- Player or NPC lifecycle definitions

---

## Core Concepts

### Combat Action
A **combat action** is a resolved intent executed during simulation that may:
- Apply damage
- Modify combat-related state
- Produce deterministic outcomes

Combat actions are **server-authoritative** and **deterministic**.

---

## Combat Eligibility

An entity is **combat-eligible** if all of the following are true:

1. Entity is simulation-eligible (see Stage 28)
2. Entity is resident in a zone
3. Entity lifecycle state permits combat participation
4. Entity is not in a restore or transition state

Eligibility is evaluated **before** the simulation tick begins.

---

## Combat Execution Window

Combat executes **only** during the **Simulation Execution** phase of a tick.

- Combat logic may not execute outside ticks
- Combat logic may not change eligibility, lifecycle, or residency state
- Combat logic may read but not mutate non-combat systems

---

## Ordering Guarantees

Combat execution must respect the following ordering:

1. Eligibility gates evaluated pre-tick
2. Combat intents collected (from players, NPCs, AI systems)
3. Combat resolution executed deterministically
4. Combat results committed atomically
5. Post-tick systems may observe results

Combat may not interleave with:
- lifecycle transitions
- residency changes
- restore operations

---

## State Mutation Rules

Combat logic may:
- Modify combat-specific state
- Apply damage or status effects
- Trigger combat outcomes

Combat logic may NOT:
- Create or destroy entities
- Change zone residency
- Change lifecycle state
- Perform persistence IO
- Enable or disable simulation eligibility

---

## Determinism Requirements

Combat must be deterministic:

- Fixed execution order
- No randomness without seeded control
- Same inputs produce same outputs
- No reliance on wall-clock time
- No iteration over unordered collections

Violation of determinism is a fatal runtime error.

---

## Failure Modes

Combat execution must fail deterministically if:
- An ineligible entity participates
- Combat is attempted outside simulation execution
- Ordering rules are violated

Failures must:
- Abort the combat step safely
- Leave no partial combat state
- Be observable for debugging

---

## Interaction Contracts

### With World Simulation Core
- Combat executes strictly within tick boundaries
- Combat respects simulation phase ordering

### With Player and NPC Runtime
- Combat reads runtime state only
- Combat does not control lifecycle or residency

### With Persistence
- Combat results may be marked dirty for later save
- Combat does not perform IO directly

---

## Explicitly Forbidden Behaviors

The following are explicitly forbidden:

- Client-authoritative combat outcomes
- Mid-tick eligibility changes due to combat
- Combat-triggered lifecycle transitions
- Non-deterministic combat resolution
- Combat logic modifying non-combat systems

Any implementation exhibiting these behaviors is invalid.

---

## Validation Expectations (Future Stage)

Future validation stages must prove:
- Combat executes only within simulation windows
- Deterministic resolution under identical inputs
- Enforcement of eligibility gates
- No forbidden state mutations

This document is the sole authority for combat runtime correctness.
