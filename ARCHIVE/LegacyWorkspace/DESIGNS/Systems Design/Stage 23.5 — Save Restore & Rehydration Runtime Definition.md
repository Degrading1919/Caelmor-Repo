# Stage 23.5 — Save Restore & Rehydration Runtime Definition

## Purpose
Define the **authoritative runtime contract** for restoring a player from persistent save data into a valid runtime state.

This stage specifies **when restore occurs**, **what is restored**, **what ordering must be respected**, and **what is explicitly forbidden during restore**. It ensures restore is deterministic, safe, and does not leak partial state into the live simulation.

This document is a **binding contract**. No code is implemented here.

---

## Scope Clarification

### This Stage Owns
- Restore and rehydration sequencing
- Restore eligibility gates
- Restore completion signaling
- Failure handling during restore
- Restore → lifecycle handoff rules

### This Stage Does NOT Own
- Save file IO or serialization format
- Save schema definitions
- Zone residency rules (see Stage 23.3)
- Lifecycle state transitions (see Stage 23.4)
- Tick execution
- Session wiring
- Gameplay logic (combat, AI, quests, items)

---

## Core Concepts

### Save Restore
**Save restore** is the process of taking a persistent save record and deterministically reconstructing the player’s runtime state so that normal lifecycle activation may proceed.

Restore answers:
> “Is the player’s runtime state fully and safely reconstructed?”

Restore is **server-authoritative** and **non-interactive**.

---

## Restore Phases

Restore occurs in discrete, ordered phases:

1. **Restore Requested**
   - Player identity and save binding validated
   - No runtime mutation allowed yet

2. **Restore In Progress**
   - Runtime state is being rehydrated
   - Player is not simulated
   - Player has no zone residency
   - Client control remains disabled

3. **Restore Complete**
   - All required runtime state is reconstructed
   - Player is eligible for lifecycle activation
   - No simulation yet

4. **Restore Failed**
   - Restore aborted deterministically
   - No partial runtime state remains

---

## Restore Invariants (Hard Rules)

The following invariants MUST always hold:

1. Restore must complete **before** lifecycle activation.
2. Restore must complete **before** zone residency attachment.
3. Restore must complete **before** simulation eligibility.
4. Restore is **idempotent**.
5. Restore is **server-authoritative only**.
6. Restore must not occur mid-tick.
7. Restore failures leave **zero partial state**.

Violation of any invariant is a fatal runtime error.

---

## Ordering Guarantees

Restore must respect the following ordering:

1. Player runtime instance exists
2. Session (if required) is validated
3. Restore begins (no simulation allowed)
4. Runtime state rehydrated
5. Restore marked complete
6. Lifecycle activation may proceed
7. Zone residency may be attached
8. Simulation eligibility granted

Restore may never overlap with:
- lifecycle activation
- zone residency attachment
- simulation ticks

---

## Failure Modes

Restore must fail deterministically if:
- Save binding is invalid
- Save data is missing or corrupt
- Restore is attempted at an invalid time
- Restore is attempted concurrently

On failure:
- Player runtime instance may be destroyed or reset
- No lifecycle activation occurs
- No zone residency exists
- No simulation occurs

---

## Interaction Contracts

### With Player Lifecycle
- Lifecycle may not enter **Active** until restore completes
- Restore failure prevents activation

### With Zone Residency
- Restore must complete before residency attach
- Restore logic does not assign zones

### With Simulation / Tick System
- Restore may not occur mid-tick
- Restoring players are excluded from simulation

### With Persistence Systems
- Persistence provides data but does not control restore timing
- Restore logic does not perform IO directly

---

## Explicitly Forbidden Behaviors

The following are explicitly forbidden:

- Partial restore visibility
- Restore during simulation
- Restore triggering lifecycle transitions
- Restore assigning zones
- Restore enabling client control
- Client-initiated restore

Any implementation exhibiting these behaviors is invalid.

---

## Validation Expectations (Future Stage)

Future validation stages must prove:
- Restore blocks activation and simulation
- Restore ordering is enforced
- Failures leave no partial state
- Restore is idempotent and deterministic

This document is the sole authority for restore correctness.
