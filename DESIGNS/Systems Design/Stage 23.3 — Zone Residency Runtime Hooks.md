# Stage 23.3 — Zone Residency Runtime Hooks

## 1. Purpose

This document defines the **runtime wiring and responsibilities** for assigning and enforcing Player Session zone residency.
Its purpose is to ensure zone residency is deterministic, ordered, and authority-safe, such that players cannot participate in zone evaluation without a valid active session, and residency cannot drift from world or session truth.

## 2. Scope

This document applies exclusively to **Player Lifecycle runtime hooks** related to zone residency.
It governs eligibility, assignment, ordering guarantees, authority boundaries, rejection conditions, and validation hooks.
It does not define zone simulation rules, spawn logic, movement, networking details, persistence formats, UI, or presentation.

## 3. Canon Dependencies

This runtime implementation is **subordinate to and constrained by** the following LOCKED canon:

- Stage 23.0 — Runtime Implementation (Player Lifecycle)
- Stage 23.2 — Session Activation & Deactivation Runtime
- Stage 19 — World Simulation & Zone Runtime Architecture (all sub-stages)
- Stage 13 — Player Lifecycle & World Session Authority (all sub-stages)
- Stage 20 — Networking & Replication Architecture (all sub-stages)
- Stage 22.1 — Player Lifecycle Implementation Plan
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Residency Eligibility Model

- A Player Session **must** be active to be eligible for zone residency.
- A Player Session **must** be attached to exactly one world before zone residency assignment.
- A Player Session **must not** be resident in any zone while inactive.
- A Player Session **must** have exactly one zone residency or zero during defined transition boundaries.
- Zone residency eligibility **must** be evaluated by the server only.

## 5. Residency Assignment Responsibilities

- Zone residency assignment **must** be performed by the world runtime.
- Residency assignment **must** occur only after session activation completes.
- Residency assignment **must** reference world-owned zone identity only.
- Residency assignment **must** assign exactly one zone at a time.
- Residency assignment **must not** occur mid-tick.
- Any residency assignment request that violates eligibility **must** be rejected deterministically.

## 6. Authority & Ownership Rules

- The server **must** be the sole authority over Player Session zone residency.
- World runtime **must** own and mediate all residency changes.
- Zone runtime **must not** assign or modify Player Session residency.
- Client input **must not** directly assign, alter, or request residency changes.
- No runtime system outside Player Lifecycle and world runtime **must** mutate residency state.

## 7. Runtime Ordering Guarantees

- Session activation **must** complete before any zone residency assignment.
- World attachment **must** complete before zone residency assignment.
- Zone residency assignment **must** occur at a tick boundary.
- A Player Session **must not** participate in zone evaluation until residency assignment completes.
- Zone residency removal **must** occur before session deactivation.
- Residency changes **must not** occur during tick execution.

## 8. Forbidden Runtime States

The following runtime states **must never exist**:

- A Player Session resident in a zone while inactive
- A Player Session resident in multiple zones simultaneously
- A Player Session participating in zone evaluation without residency
- Zone residency assignment occurring mid-tick
- Client-authored or client-mutated residency state
- Zone residency existing without world attachment

Any occurrence of these states **must** be rejected deterministically.

## 9. Validation Hooks

- Validation **must** assert that residency eligibility requires an active session.
- Validation **must** assert that exactly one zone residency exists per active session.
- Validation **must** assert that residency assignment occurs only at tick boundaries.
- Validation **must** assert that zone participation requires residency.
- Validation **must** fail if residency ordering relative to activation or deactivation is violated.

Validation **must** be binary, deterministic, and fail-loud.

## 10. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Residency eligibility and assignment responsibilities are explicit and closed.
- Authority and ownership rules prevent all cross-system or client mutation.
- Ordering guarantees eliminate mid-tick or out-of-order residency.
- Forbidden runtime states are fully enumerated.
- Validation hooks are sufficient to detect all violations.
- No modal or speculative language remains.
