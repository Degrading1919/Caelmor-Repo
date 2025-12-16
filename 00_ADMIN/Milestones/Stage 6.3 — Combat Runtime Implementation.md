# Stage 12.0 — Combat Runtime Implementation
## Milestone Snapshot

Project: Caelmor  
Engine: Unity  
Language: C#  
Architecture: Server-authoritative, deterministic (10 Hz)  
Status: PLANNED — IMPLEMENTATION GATE

---

## 1. Stage Purpose

Stage 12 marks the transition from **fully locked combat design** to **runtime implementation**.

This stage answers:

> “How do we implement combat in C# while obeying every architectural, schema, authority, and validation rule already defined?”

Stage 12 is not exploratory.  
It is the **execution of a proven plan**.

---

## 2. Canon Lock Statement

The following are **final, authoritative, and immutable** and must be treated as law:

- Stage 7–8 — Non-Combat Economy & Persistence
- Stage 9 — Validation Harness & Philosophy (9.0–9.4)
- Stage 10 — Combat Architecture (10.0–10.4)
- Stage 11.1 — Combat Runtime System Breakdown
- Stage 11.2 — Combat Schema Finalization
- Stage 11.3 — Tick-Phase Wiring Plan
- Stage 11.4 — Combat Validation Scenarios
- Caelmor_Phase1_4_Technical_Foundation.md

Any implementation that diverges from these documents is **incorrect by definition**.

---

## 3. Implementation Philosophy

Combat implementation must be:

- **Deterministic** — same inputs, same outputs
- **Server-authoritative** — no client resolution
- **Tick-aligned** — no frame-based logic
- **Schema-driven** — no ad hoc data
- **Validation-first** — correctness before feel
- **Fail-loud** — no silent correction or recovery

Implementation must never:
- Guess
- Repair
- Replay logic on restore
- Infer outcomes client-side

---

## 4. Scope (What Stage 12 Includes)

Stage 12 includes:

- C# implementation of combat runtime systems defined in Stage 11.1
- Tick-phase execution wired exactly as defined in Stage 11.3
- Schema consumption exactly as finalized in Stage 11.2
- Emission of CombatEvents exactly as defined in Stage 10.3 / 10.4
- Validation hooks wired to the existing Stage 9 harness

Stage 12 implementation must be **incremental and verifiable**.

---

## 5. Explicit Non-Goals

Stage 12 must NOT:

- Redesign combat systems
- Modify schemas
- Introduce new combat mechanics
- Tune damage, timing, or balance
- Implement animation, VFX, or audio
- Implement UI or HUD logic
- Add prediction, rollback, or reconciliation
- Change persistence semantics

If a design question arises, implementation must stop and escalate.

---

## 6. Required Implementation Order

Combat must be implemented **in slices**, not all at once.

The minimum safe order is:

1. Combat Intent Intake & Queue (read-only validation)
2. Combat State Authority (state gating only)
3. Combat Resolution Engine (stateless execution)
4. Damage & Mitigation Processing (outcome generation)
5. Combat Outcome Broadcasting
6. Combat Persistence Adapter (checkpoint integration)
7. Combat Validation Hook Layer (assertions only)

Each slice must:
- Compile
- Pass relevant validation scenarios
- Introduce no regressions

---

## 7. Validation Requirements (Non-Negotiable)

- All Task 11.4 scenarios must pass
- Determinism must be proven across identical runs
- Save/load during combat must produce identical outcomes
- No combat logic may execute during restore
- Validation failures must halt execution

Validation is a **gate**, not a post-step.

---

## 8. Failure Handling Rules

During implementation:

- **Fail loudly** on contract violations
- Do NOT auto-correct state
- Do NOT retry resolution
- Do NOT clamp values silently
- Do NOT “make it work for now”

A broken invariant is a stop condition.

---

## 9. Exit Criteria (Definition of Done)

Stage 12.0 is complete when:

- Combat runtime systems are implemented per Stage 11.1
- Tick-phase wiring matches Stage 11.3 exactly
- All combat schemas are consumed without mutation
- All Task 11.4 validation scenarios pass
- No architectural questions remain unanswered

Only after this point may:
- Combat feel tuning
- Content authoring
- AI combat behavior
- Client presentation work

begin.

---

## 10. Anchor Statement

> “At this stage, code is not where decisions are made.
> It is where decisions are proven correct.”
