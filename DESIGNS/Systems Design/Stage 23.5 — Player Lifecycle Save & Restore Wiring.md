Stage 23.5 — Player Lifecycle Save/Restore Wiring

## 1. Purpose

This document defines the **runtime wiring and responsibilities** for Player Lifecycle participation in save and restore.
Its purpose is to ensure Player Lifecycle state participates in cross-system persistence atomically, restores deterministically into a legal lifecycle state, and cannot drift across save/load boundaries.
This document specifies wiring and ordering only and does not redefine persistence architecture.

## 2. Scope

This document applies exclusively to **Player Lifecycle runtime wiring** for save participation and restore.
It governs save eligibility, restore ordering, authority boundaries, rejection conditions, and validation hooks.
It does not define persistence formats, serialization, storage systems, networking behavior, save cadence, or UI.

## 3. Canon Dependencies

This runtime implementation is **subordinate to and constrained by** the following LOCKED canon:

- Stage 23.0 — Runtime Implementation (Player Lifecycle)
- Stage 21 — Cross-System Persistence Architecture (all sub-stages)
- Stage 23.2 — Session Activation & Deactivation Runtime
- Stage 23.4 — Tick Participation Runtime Wiring
- Stage 13 — Player Lifecycle & World Session Authority (all sub-stages)
- Stage 22.1 — Player Lifecycle Implementation Plan
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Save Participation Responsibilities

- Player Lifecycle **must** participate in cross-system save operations as a single atomic participant.
- Player Lifecycle **must** expose exactly one persistence surface representing lifecycle structural truth.
- Player Lifecycle **must** contribute save data only when the Player Session is inactive or at a canonical save boundary.
- Player Lifecycle **must not** contribute partial, inferred, or transitional state.
- Player Lifecycle **must** reject save participation if lifecycle state is illegal or incomplete.
- Player Lifecycle **must not** initiate save operations and **must** respond only to orchestration by cross-system persistence.

## 5. Restore Responsibilities & Ordering

- Player Lifecycle restore **must** occur before any session activation.
- Player Lifecycle restore **must** occur before tick participation eligibility.
- Player Lifecycle restore **must** occur before world or zone residency assignment.
- Restore **must** reconstruct lifecycle state from persisted structural truth only.
- Restore **must not** execute runtime logic, emit intents, or advance lifecycle transitions.
- Restore **must** produce either a fully valid lifecycle state or fail deterministically.
- Session activation **must not** proceed unless Player Lifecycle restore completes successfully.

## 6. Authority & Ownership Rules

- The server **must** be the sole authority over Player Lifecycle save and restore participation.
- No client input **must** influence lifecycle persistence or restore outcomes.
- World, zone, networking, NPC, item, and quest systems **must not** mutate Player Lifecycle persisted state.
- Player Lifecycle **must not** read from snapshots or networking artifacts during restore.

## 7. Forbidden Runtime States

The following runtime states **must never exist**:

- Player Lifecycle state partially restored
- Session activation occurring before lifecycle restore
- Tick participation occurring before lifecycle restore
- World or zone residency assigned before lifecycle restore
- Runtime logic executed during lifecycle restore
- Lifecycle persistence satisfied by networking or snapshot data

Any occurrence of these states **must** be rejected deterministically.

## 8. Validation Hooks

- Validation **must** assert that Player Lifecycle participates in persistence atomically.
- Validation **must** assert that restore occurs before activation, tick participation, and residency.
- Validation **must** assert that restore does not execute runtime logic.
- Validation **must** assert rejection of partial or inconsistent lifecycle restore.
- Validation **must** fail if lifecycle state differs before save and after restore.

Validation **must** be binary, deterministic, and fail-loud.

## 9. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Save and restore responsibilities are explicit and closed.
- Ordering guarantees eliminate lifecycle drift across persistence boundaries.
- Authority rules prevent client or cross-system mutation.
- Forbidden runtime states are fully enumerated.
- Validation hooks are sufficient to detect all violations.
- No modal or speculative language remains.