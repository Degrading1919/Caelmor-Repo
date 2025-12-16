Stage 23.4 — Tick Participation Runtime Wiring

## 1. Purpose

This document defines the **runtime wiring and responsibilities** for Player Session admission to and removal from authoritative tick participation.
Its purpose is to ensure that only valid, active, and correctly resident Player Sessions participate in tick execution, and that tick participation cannot drift from Player Lifecycle, world, or zone truth.

## 2. Scope

This document applies exclusively to **Player Lifecycle runtime wiring** for tick participation.
It governs eligibility, admission, removal, ordering guarantees, authority enforcement, rejection conditions, and validation hooks.
It does not define tick execution logic, simulation rules, networking mechanics, persistence formats, UI, or presentation.

## 3. Canon Dependencies

This runtime implementation is **subordinate to and constrained by** the following LOCKED canon:

- Stage 23.0 — Runtime Implementation (Player Lifecycle)
- Stage 23.2 — Session Activation & Deactivation Runtime
- Stage 23.3 — Zone Residency Runtime Hooks
- Stage 19 — World Simulation & Zone Runtime Architecture (all sub-stages)
- Stage 13 — Player Lifecycle & World Session Authority (all sub-stages)
- Stage 20 — Networking & Replication Architecture (all sub-stages)
- Stage 22.1 — Player Lifecycle Implementation Plan
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Tick Participation Eligibility Model

- A Player Session **must** be active to be eligible for tick participation.
- A Player Session **must** be attached to exactly one world to be eligible for tick participation.
- A Player Session **must** have exactly one valid zone residency to be eligible for tick participation.
- A Player Session **must not** be eligible for tick participation while inactive.
- A Player Session **must not** be eligible for tick participation without completed persistence restore.
- Tick participation eligibility **must** be evaluated by the server only.

## 5. Participation Admission Responsibilities

- Admission to tick participation **must** be performed by the world runtime.
- Admission **must** occur only after session activation completes.
- Admission **must** occur only after zone residency assignment completes.
- Admission **must** occur only at a tick boundary.
- Admission **must** add exactly one Player Session to tick participation.
- Any admission request that violates eligibility **must** be rejected deterministically.

## 6. Authority & Ownership Rules

- The server **must** be the sole authority over Player Session tick participation.
- World runtime **must** own and mediate tick admission and removal.
- Zone runtime **must not** admit or remove Player Sessions from tick participation.
- Client input **must not** directly influence tick admission or removal.
- No runtime system outside Player Lifecycle and world runtime **must** mutate tick participation state.

## 7. Runtime Ordering Guarantees

- Session activation **must** complete before tick admission.
- Zone residency assignment **must** complete before tick admission.
- Tick admission **must** occur before any tick execution that includes the session.
- Tick removal **must** occur before session deactivation.
- Tick removal **must** occur before zone residency removal.
- Tick admission and removal **must not** occur during tick execution.

## 8. Forbidden Runtime States

The following runtime states **must never exist**:

- A Player Session participating in ticks while inactive
- A Player Session participating in ticks without zone residency
- A Player Session participating in ticks without world attachment
- Tick admission or removal occurring mid-tick
- Client-authored or client-mutated tick participation state
- Tick participation drifting from session or residency truth

Any occurrence of these states **must** be rejected deterministically.

## 9. Validation Hooks

- Validation **must** assert that tick participation requires an active session.
- Validation **must** assert that tick participation requires valid world attachment and zone residency.
- Validation **must** assert that tick admission and removal occur only at tick boundaries.
- Validation **must** assert that tick removal precedes session deactivation.
- Validation **must** fail if any forbidden runtime state is detected.

Validation **must** be binary, deterministic, and fail-loud.

## 10. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Tick participation eligibility and admission responsibilities are explicit and closed.
- Authority and ownership rules prevent all cross-system or client mutation.
- Ordering guarantees eliminate mid-tick or out-of-order participation.
- Forbidden runtime states are fully enumerated.
- Validation hooks are sufficient to detect all violations.
- No modal or speculative language remains.