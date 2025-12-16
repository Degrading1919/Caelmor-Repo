# Stage 21.3 — Persistence Validation Scenarios

## 1. Purpose

This document defines the **validation scenarios** required to deterministically verify **cross-system persistence correctness** in Caelmor.
Its purpose is to ensure save atomicity, restore ordering, dependency satisfaction, and rejection of illegal or inconsistent persisted state across all participating systems.
This document introduces no tooling, implementation, or content logic.

## 2. Scope

This document applies exclusively to **server-authoritative persistence validation**.
It defines structural scenarios that validation harnesses must accept or reject deterministically.
It does not define test frameworks, diagnostics, performance testing, or engine internals.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 21.0 — Cross-System Persistence Architecture
- Stage 21.1 — Cross-System Persistence Architecture
- Stage 21.2 — Persistence Ordering & Dependency Graph
- Stage 13.5 — Save & Restore Boundaries
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Validation Coverage Overview

Validation **must** exhaustively cover the following dimensions:

- Atomic save across all participating systems
- Deterministic restore ordering and dependency satisfaction
- Rejection of partial, missing, or inconsistent persisted state
- Rejection of circular or illegal dependency graphs
- Guarantee that restore does not execute runtime logic
- Guarantee that networking or snapshots cannot satisfy persistence requirements

Validation **must** be binary and fail-loud.
No partial acceptance is permitted.

## 5. Save Validation Scenarios

The validation harness **must** detect and reject the following illegal save conditions:

1. **Partial Save**
   - Any save that persists state for fewer than all participating systems **must** be rejected.

2. **Non-Atomic Save**
   - Any save that exposes partially completed cross-system state **must** be rejected.
   - Any save that completes while any participating system fails to produce authoritative persisted state **must** be rejected.

3. **Ownership Violation**
   - Any system persisting data owned by another system **must** be rejected.
   - Any persisted datum with ambiguous or multiple owners **must** be rejected.

4. **Runtime State Persistence**
   - Any save containing runtime-only, tick-internal, evaluation, intent, or decision state **must** be rejected.

5. **Client Influence**
   - Any save influenced, authored, or modified by a client **must** be rejected.

## 6. Restore Validation Scenarios

The validation harness **must** detect and reject the following illegal restore conditions:

1. **Missing Required State**
   - Restore with any required persisted system state missing **must** be rejected.

2. **Inconsistent Persisted State**
   - Restore with internally contradictory or mutually incompatible persisted state **must** be rejected.

3. **Illegal Restore Ordering**
   - Restore that violates the defined system ordering **must** be rejected.
   - Restore that activates dependent systems before their dependencies **must** be rejected.

4. **Runtime Execution During Restore**
   - Any execution, resumption, or evaluation of runtime logic during restore **must** be rejected.

5. **Snapshot or Networking Substitution**
   - Any restore attempt that uses snapshots, replication data, or networking artifacts as persisted truth **must** be rejected.

## 7. Dependency & Ordering Validation

The validation harness **must** detect and reject the following dependency and ordering violations:

1. **Illegal Dependencies**
   - Persisted state that depends on networking, snapshots, ticks, or runtime evaluation **must** be rejected.

2. **Circular Dependencies**
   - Any circular dependency in the persistence dependency graph **must** be rejected.

3. **Implicit Dependencies**
   - Persisted state that requires inference or reconstruction from another system **must** be rejected.

4. **Out-of-Order Save or Restore**
   - Any save or restore sequence that differs from the defined ordering **must** be rejected.

## 8. Forbidden Persistence States

The following persistence states **must never exist** and **must be validation-rejectable**:

- Partial cross-system persisted state
- Mixed-version or mixed-epoch persisted state
- Persisted runtime-only or evaluation state
- Replay-based or event-log-based persisted state
- Snapshot-derived or network-derived persisted state
- Client-authored or client-influenced persisted state

No exception paths are permitted.

## 9. Validation Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **Atomicity**
   - Cross-system persistence **must** be all-or-nothing.

2. **Closed Dependency Graph**
   - Persistence dependencies **must** be explicit, acyclic, and closed.

3. **Deterministic Restore**
   - Given identical persisted truth, restore outcomes **must** be identical.

4. **No Runtime Logic**
   - Restore **must not** execute, resume, or infer runtime logic.

5. **Server Authority**
   - All persistence validation **must** assume server-owned authoritative truth.

6. **No Networking Substitution**
   - Networking and snapshots **must not** satisfy persistence requirements.

## 10. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Persistence validation scenarios exhaustively cover save, restore, and dependency legality.
- All illegal persistence states are explicitly enumerated and rejectable.
- Restore execution is provably free of runtime logic.
- Atomicity and ordering requirements are structurally enforceable.
- No modal or speculative language remains.
- Validation harnesses can deterministically accept or reject persistence correctness.
