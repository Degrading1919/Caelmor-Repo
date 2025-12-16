# Task 23.1 — Player Identity + Save Binding Runtime

## 1. Purpose

This document defines the **runtime wiring and responsibilities** for Player Identity creation and its binding to persisted save data.
Its purpose is to make identity/save drift impossible at runtime by enforcing exclusive ownership, deterministic ordering, and fail-loud rejection of illegal bindings.
This document does not redefine architecture and exists solely to specify runtime responsibilities and guarantees.

## 2. Scope

This document applies exclusively to **Player Lifecycle runtime wiring** for identity creation, save binding, and authority enforcement.
It governs identity existence, save association, ordering relative to session and world attachment, and validation hooks.
It does not define save formats, authentication, client concepts, UI, or error handling strategies.

## 3. Canon Dependencies

This runtime implementation is **subordinate to and constrained by** the following LOCKED canon:

- Stage 13 — Player Lifecycle & World Session Authority (all sub-stages)
- Stage 21 — Cross-System Persistence Architecture (all sub-stages)
- Stage 22.1 — Player Lifecycle Implementation Plan
- Stage 19 — World Simulation & Zone Runtime Architecture (all sub-stages)
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Runtime Identity Model

- A Player Identity **must** be a server-owned runtime construct.
- Exactly one Player Identity **must** exist per active player session.
- A Player Identity **must not** be client-authored, client-mutated, or client-reconstructed.
- A Player Identity **must** have a stable, server-assigned identity key for its lifetime.
- A Player Identity **must not** exist outside an active or initializing server session.

## 5. Save Binding Responsibilities

- Each Player Identity **must** be bound to exactly one persisted save.
- Each persisted save **must** bind to exactly one Player Identity.
- Save binding **must** be established by the server during Player Identity initialization.
- A Player Identity **must not** become active without a valid save binding, except during a defined bootstrap window.
- The bootstrap window **must** exist only between identity instantiation and persistence restore completion.
- Save binding **must** reference persisted structural truth only and **must not** rely on runtime inference.
- Any attempt to bind a Player Identity to zero or multiple saves **must** be rejected.

## 6. Authority & Ownership Rules

- The server **must** be the sole authority over Player Identity creation and save binding.
- No runtime system other than Player Lifecycle **must** mutate identity/save associations.
- World, zone, NPC, item, quest, and networking systems **must not** alter save bindings.
- Client input **must not** influence identity/save binding selection or reassignment.
- Save binding **must not** be transferred between Player Identities.

## 7. Runtime Ordering Guarantees

- Player Identity creation **must** occur before session activation.
- Save binding **must** be established before world attachment.
- Persistence restore **must** occur after save binding and before any world or zone residency.
- A Player Identity **must not** participate in world or zone evaluation before persistence restore completes.
- Session activation **must not** complete unless identity/save binding is valid and restored.
- Identity/save binding **must not** change after persistence restore.

## 8. Forbidden Runtime States

The following runtime states **must never exist**:

- A Player Identity with zero save bindings outside the bootstrap window
- A Player Identity bound to multiple saves
- A save bound to multiple Player Identities
- A Player Identity participating in world or zone logic without restored save state
- Client-authored or client-mutated identity/save bindings
- Identity/save reassignment after session activation

Any occurrence of these states **must** be rejected deterministically.

## 9. Validation Hooks

- Validation **must** assert one-to-one identity/save binding at all times outside the bootstrap window.
- Validation **must** assert server ownership of identity and save binding.
- Validation **must** assert ordering of identity creation, save binding, persistence restore, and world attachment.
- Validation **must** fail if identity/save bindings change after restore.
- Validation **must** reject any identity or save participating in runtime evaluation without a valid binding.

Validation **must** be binary, deterministic, and fail-loud.

## 10. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Identity and save binding responsibilities are explicit and closed.
- Authority and ownership rules prevent all forms of drift.
- Ordering guarantees eliminate partial or inferred binding.
- Forbidden runtime states are fully enumerated.
- Validation hooks are sufficient to detect all violations.
- No modal or speculative language remains.
