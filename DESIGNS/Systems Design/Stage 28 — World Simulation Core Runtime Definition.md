# Stage 28 — World Simulation Core Runtime Definition

## Purpose
Define the **authoritative runtime contract** for the world simulation core, including tick structure, execution ordering, and eligibility rules.

This stage specifies **how time advances**, **what is allowed to execute per tick**, and **what is explicitly forbidden during simulation**. It is the foundational contract that all simulation participants must obey.

This document is a **binding contract**. No code is implemented here.

---

## Scope Clarification

### This Stage Owns
- Tick structure and phase ordering
- Simulation execution rules
- Eligibility requirements for simulation
- Mid-tick mutation prohibitions
- Deterministic execution guarantees

### This Stage Does NOT Own
- Player lifecycle transitions
- Zone residency rules
- Session management
- Persistence IO
- Combat resolution logic
- AI decision logic
- Quest or NPC behavior definitions

---

## Core Concepts

### Tick
A **tick** is a fixed-duration server-side simulation step during which eligible entities are updated deterministically.

- Tick rate is fixed and globally defined (see Phase 1.4)
- All simulation work occurs inside ticks
- Ticks are server-authoritative

### Simulation Eligibility
An entity is **simulation-eligible** if it satisfies all required gates (lifecycle, residency, restore completion, etc.).

Eligibility is evaluated **before** a tick begins.

---

## Tick Phases

Each tick is composed of ordered, non-overlapping phases:

1. **Pre-Tick Gate Evaluation**
   - Determine eligible entities
   - Reject mid-tick state changes

2. **Simulation Execution**
   - Update eligible entities
   - Deterministic ordering enforced

3. **Post-Tick Finalization**
   - Commit simulation results
   - Prepare for next tick

No phase may be skipped or reordered.

---

## Simulation Invariants (Hard Rules)

The following invariants MUST always hold:

1. Only eligible entities may be simulated.
2. No entity eligibility may change mid-tick.
3. Lifecycle, residency, and restore state must be stable during a tick.
4. Simulation order is deterministic.
5. Simulation produces the same result given the same inputs.
6. No side effects escape the tick boundary.

Violation of any invariant is a fatal runtime error.

---

## Ordering Guarantees

- Eligibility is evaluated **before** simulation begins.
- No attach/detach, activate/deactivate, or restore operations may occur mid-tick.
- Simulation effects are committed atomically at tick end.

---

## Failure Modes

Simulation must fail deterministically if:
- Eligibility changes mid-tick
- Required invariants are violated
- Execution order becomes non-deterministic

Failures must:
- Halt the simulation safely
- Leave no partial committed state
- Be observable for debugging

---

## Interaction Contracts

### With Player Lifecycle
- Only Active players may be simulation-eligible
- Lifecycle transitions must occur outside ticks

### With Zone Residency
- Only resident entities may be simulated
- Residency changes are forbidden mid-tick

### With Restore Systems
- Entities restoring are excluded from simulation
- Restore completion must occur between ticks

### With Gameplay Systems
- Gameplay systems execute only within Simulation Execution
- Gameplay systems must not mutate eligibility state

---

## Explicitly Forbidden Behaviors

The following are explicitly forbidden:

- Mid-tick lifecycle transitions
- Mid-tick zone residency changes
- Mid-tick restore operations
- Simulation-triggered eligibility changes
- Non-deterministic iteration or execution order
- Client-influenced simulation timing

Any implementation exhibiting these behaviors is invalid.

---

## Validation Expectations (Future Stage)

Future validation stages must prove:
- Eligibility gating is enforced
- Mid-tick mutations are rejected
- Execution order is deterministic
- Simulation boundaries are respected

This document is the sole authority for simulation correctness.
