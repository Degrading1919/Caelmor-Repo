# Stage 23.2 — Session Activation/Deactivation Runtime

## 1. Purpose

This document defines the **runtime wiring and responsibilities** for Player Session activation and deactivation.
Its purpose is to enforce deterministic eligibility, ordering, and authority boundaries so that sessions cannot activate or deactivate in illegal states, cannot bypass persistence or identity binding, and cannot leak authority across systems.

## 2. Scope

This document applies exclusively to **Player Lifecycle runtime behavior** for session activation and deactivation.
It governs eligibility gates, ordering guarantees, authority enforcement, rejection conditions, and validation hooks.
It does not define authentication, network protocols, UI, error handling strategies, or behavior outside Player Lifecycle scope.

## 3. Canon Dependencies

This runtime implementation is **subordinate to and constrained by** the following LOCKED canon:

- Stage 23.0 — Runtime Implementation (Player Lifecycle)
- Stage 23.1 — Player Identity + Save Binding Runtime
- Stage 13 — Player Lifecycle & World Session Authority (all sub-stages)
- Stage 20 — Networking & Replication Architecture (all sub-stages)
- Stage 21 — Cross-System Persistence Architecture (all sub-stages)
- Stage 22.1 — Player Lifecycle Implementation Plan
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Session Activation Model

- A Session **must** be a server-owned runtime construct.
- Exactly one Session **must** correspond to exactly one Player Identity.
- A Session **must not** exist without an associated Player Identity.
- A Session **must** transition from inactive to active only through the activation process defined in this document.
- A Session **must not** be client-authored, client-activated, or client-deactivated.

## 5. Activation Responsibilities & Gates

- Session activation **must** occur only after Player Identity creation and valid save binding are complete.
- Session activation **must** be gated on successful persistence restore of the bound save.
- Session activation **must not** occur if identity/save binding is missing, invalid, or ambiguous.
- Session activation **must** occur before world attachment and zone residency assignment.
- Session activation **must** establish eligibility for snapshot observation but **must not** grant world or zone participation.
- Session activation **must not** complete if any required validation fails.

**Activation Gates (All Required)**

- Valid Player Identity exists
- Exactly one save bound to the identity
- Persistence restore completed successfully
- No forbidden runtime states present

Failure of any gate **must** deterministically reject activation.

## 6. Session Deactivation Model

- Session deactivation **must** be a server-owned operation.
- Session deactivation **must** represent the authoritative end of session participation.
- Session deactivation **must** occur through the ordered process defined in this document.
- Session deactivation **must not** destroy Player Identity or save binding.
- Session deactivation **must not** execute runtime simulation logic.

## 7. Deactivation Responsibilities & Ordering

- Session deactivation **must** occur before world detachment and zone residency removal.
- Session deactivation **must** revoke snapshot eligibility immediately.
- Session deactivation **must** occur before any persistence save operation.
- Session deactivation **must** complete before Player Identity becomes inactive.
- Session deactivation **must not** alter save binding or persisted structural truth.
- Session deactivation **must** be idempotent and deterministic.

**Deactivation Ordering (Strict)**

1. Snapshot eligibility revoked  
2. World and zone participation ended  
3. Session marked inactive  
4. Persistence save permitted  

No reordering is permitted.

## 8. Forbidden Runtime States

The following runtime states **must never exist**:

- An active Session without a valid Player Identity
- An active Session without a completed persistence restore
- A Session participating in world or zone evaluation before activation
- A Session eligible for snapshots after deactivation
- Client-authored or client-mutated session state
- Session activation or deactivation occurring mid-tick

Any occurrence of these states **must** be rejected deterministically.

## 9. Validation Hooks

- Validation **must** assert that session activation occurs only after identity/save binding and restore.
- Validation **must** assert that session activation precedes world attachment.
- Validation **must** assert that session deactivation precedes world detachment and persistence save.
- Validation **must** assert that snapshot eligibility aligns exactly with session active state.
- Validation **must** fail if activation or deactivation ordering is violated.

Validation **must** be binary, deterministic, and fail-loud.

## 10. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Session activation and deactivation responsibilities are explicit and closed.
- Ordering guarantees eliminate ambiguity across lifecycle boundaries.
- Authority rules prevent client or cross-system mutation.
- Forbidden runtime states are fully enumerated.
- Validation hooks are sufficient to detect all violations.
- No modal or speculative language remains.
