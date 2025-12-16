# Stage 11 — Combat Implementation Plan
## Milestone Snapshot

Project: Caelmor  
Engine: Unity  
Architecture: Server-authoritative, deterministic (10 Hz)  
Status: PLANNED — GOVERNANCE LOCK

---

## 1. Stage Purpose

Stage 11 translates the **fully locked combat architecture (Stage 10)** into a **concrete, executable implementation plan**.

This stage answers:

> “How do we implement combat in C# without violating any architectural contracts?”

Stage 11:
- Breaks combat into implementable runtime systems
- Defines system responsibilities and boundaries
- Establishes implementation order and dependencies
- Identifies validation hooks and failure surfaces

Stage 11 does **not** implement combat.  
It defines **how combat will be implemented safely**.

---

## 2. Canon Lock Statement

The following documents are **final, authoritative, and immutable**:

- Stage 7–8 — Non-Combat Economy & Persistence
- Stage 9 — Integration Testing & Validation Harness (9.0–9.4)
- Stage 10 — Combat Systems Architecture (10.0–10.4)
- Caelmor_Phase1_4_Technical_Foundation.md

Stage 11 must strictly conform to the above.

No system designed in Stage 11 may:
- Redefine combat behavior
- Add authority to the client
- Modify persistence semantics
- Alter the tick model
- Introduce prediction, rollback, or replay

Any deviation is a scope failure.

---

## 3. Implementation Philosophy

Combat implementation in Caelmor must be:

- **Layered** (intent → state → resolution → outcome)
- **Deterministic** (same inputs, same outputs)
- **Server-authoritative**
- **Observable but not speculative**
- **Validated continuously** (Stage 9 patterns)

Implementation must favor:
- Clear contracts over clever code
- Explicit phases over implicit flow
- Failure over silent correction

---

## 4. In-Scope (What Stage 11 Does)

Stage 11 defines:

- Runtime combat subsystems (names and roles)
- Data flow between subsystems
- Tick-phase mapping for each subsystem
- Schema finalization checkpoints (structure only)
- Error handling and observability strategy
- Validation strategy using the existing harness

Stage 11 produces:
- A staged implementation roadmap (11.1, 11.2, …)
- Clear ownership per subsystem
- Non-negotiable invariants per stage

---

## 5. Explicit Non-Goals (Hard Exclusions)

Stage 11 must NOT include:

- Combat C# implementation
- Numeric tuning or balance
- Weapons, armor, enemies, or abilities
- Animation, VFX, or audio hooks
- UI or HUD work
- AI behavior implementation
- Network optimization or prediction

If code is written in this stage, the stage has failed.

---

## 6. Proposed Implementation Decomposition (Conceptual)

Combat implementation will be decomposed into **isolated runtime systems**, for example:

- Combat Intent Intake & Queue
- Combat State Authority
- Combat Resolution Engine
- Damage & Mitigation Processor
- Combat Outcome Broadcaster
- Combat Persistence Integration
- Combat Validation Hooks

These are **conceptual groupings**, not folders or classes yet.

---

## 7. Validation & Safety Strategy

Combat implementation must be continuously validated by:

- Reusing Stage 9 harness patterns
- Introducing combat-specific validation scenarios
- Asserting determinism across save/load
- Failing loudly on contract violations

Validation is not optional and not deferred.

---

## 8. Exit Criteria (Definition of Done)

Stage 11 is complete when:

- Combat implementation stages are fully enumerated
- System responsibilities are unambiguous
- Dependencies and ordering are explicit
- Validation strategy is defined for each stage
- No architectural ambiguity remains

Only after Stage 11 is locked may combat implementation begin.

---

## 9. Anchor Statement

> “Combat implementation is not experimentation.
> It is the careful execution of a locked design,
> validated at every step.”
