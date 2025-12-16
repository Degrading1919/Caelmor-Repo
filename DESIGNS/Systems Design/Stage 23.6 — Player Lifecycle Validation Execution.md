# Stage 23.6 — Player Lifecycle Validation Execution

## 1. Purpose

This document defines the **runtime validation execution requirements** for the Player Lifecycle.
Its purpose is to ensure that all Player Lifecycle runtime wiring defined in Stage 23 is continuously and deterministically validated, that illegal states fail-loud immediately, and that no lifecycle guarantees rely on trust, convention, or downstream correction.

## 2. Scope

This document applies exclusively to **runtime validation execution** for the Player Lifecycle.
It governs validation checkpoints, ordering, failure enforcement, and completion criteria.
It does not define validation tooling, frameworks, logging, metrics, implementation hooks, UI, or presentation.

## 3. Canon Dependencies

This validation execution specification is **subordinate to and constrained by** the following LOCKED canon:

- Stage 23.0 — Runtime Implementation (Player Lifecycle)
- Stage 23.1 — Player Identity + Save Binding Runtime
- Stage 23.2 — Session Activation & Deactivation Runtime
- Stage 23.3 — Zone Residency Runtime Hooks
- Stage 23.4 — Tick Participation Runtime Wiring
- Stage 23.5 — Player Lifecycle Save & Restore Wiring
- Stage 22.1 — Player Lifecycle Implementation Plan
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Validation Coverage Overview

Runtime validation **must** cover all Player Lifecycle guarantees, including:

- Identity existence and save binding correctness
- Session activation and deactivation ordering
- World attachment and zone residency eligibility
- Tick participation admission and removal
- Save and restore ordering and legality

Validation coverage **must** be exhaustive at the structural level.
No Player Lifecycle responsibility defined in Stage 23 **must** exist without corresponding validation enforcement.

## 5. Runtime Validation Execution Points

Validation **must** execute at the following runtime boundaries:

- **Identity Initialization**
  - Validate exactly one save bound to exactly one Player Identity.
- **Session Activation Attempt**
  - Validate identity existence, save binding, and completed restore.
- **World Attachment**
  - Validate session activation precedes attachment.
- **Zone Residency Assignment**
  - Validate active session, world attachment, and exclusivity.
- **Tick Admission**
  - Validate active session, valid residency, and restore completion.
- **Tick Removal**
  - Validate removal precedes deactivation and residency removal.
- **Session Deactivation**
  - Validate tick removal and snapshot revocation.
- **Save Participation**
  - Validate inactive or canonical boundary state.
- **Restore Completion**
  - Validate restored lifecycle legality before activation.

Validation **must** execute before state commitment at each boundary.

## 6. Failure Conditions & Enforcement

- Any validation failure **must** halt the current lifecycle transition.
- Any validation failure **must** be fail-loud and non-recoverable without correction.
- Validation failures **must not** be deferred, suppressed, or conditionally ignored.
- Validation failures **must** prevent further runtime participation by the affected session.
- No lifecycle state **must** advance after a failed validation.

Validation enforcement **must** be deterministic and binary.

## 7. Forbidden Validation Gaps

The following validation gaps **must never exist**:

- Session activation without prior validation
- Zone residency assignment without validation
- Tick participation without validation
- Save participation without validation
- Restore completion without validation
- Cross-stage lifecycle transitions without validation checkpoints

Any missing validation coverage **must** be treated as a fatal architecture violation.

## 8. Completion Criteria

Player Lifecycle validation execution is considered complete only when all of the following are true:

- Every runtime boundary defined in Stage 23 has an associated validation execution point.
- All forbidden runtime states defined in Stage 23 are detectably invalid.
- Validation execution order matches lifecycle ordering exactly.
- No Player Lifecycle transition can occur without validation.
- All validation outcomes are deterministic and fail-loud.

## 9. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Validation execution points fully cover Stage 23 runtime wiring.
- Failure conditions and enforcement rules are explicit and closed.
- No validation gaps exist.
- Completion criteria are unambiguous and enforceable.
- No modal or speculative language remains.
