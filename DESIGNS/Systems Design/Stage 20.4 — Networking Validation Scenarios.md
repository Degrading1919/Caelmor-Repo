# Stage 20.4 — Networking Validation Scenarios

## 1. Purpose

This document defines the **validation scenarios** required to deterministically verify networking and replication correctness in Caelmor.
Its purpose is to ensure that snapshot legality, ordering guarantees, join/leave/reconnect behavior, and authority isolation are **unambiguous, enforceable, and fail-loud** under automated validation.
This document introduces no tooling, implementation, or content logic.

## 2. Scope

This document applies exclusively to **server-authoritative networking validation**.
It defines structural scenarios that must be accepted or rejected deterministically by the validation harness.
It does not define test frameworks, diagnostics, or performance characteristics.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 20.0 — Networking & Replication Architecture
- Stage 20.1 — Snapshot Model & Authority Rules
- Stage 20.2 — Join / Leave / Reconnect Semantics
- Stage 20.3 — Tick ↔ Replication Ordering
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Validation Coverage Overview

Validation **must** exhaustively cover the following dimensions:

- Snapshot legality, immutability, and uniqueness
- Tick completion, snapshot creation, and replication ordering
- Client join, leave, and reconnect observation legality
- Client observation constraints and isolation
- Authority boundaries and non-interference
- Deterministic rejection of illegal networking states

Validation **must** be binary and fail-loud.
No partial acceptance is permitted.

## 5. Snapshot Validation Scenarios

The validation harness **must** detect and reject the following illegal snapshot conditions:

1. **Unauthorized Snapshot Authorship**
   - Any snapshot not authored by the server **must** be rejected.
   - Any client-authored or client-modified snapshot **must** be rejected.

2. **Snapshot Immutability Violation**
   - Any snapshot that mutates after creation **must** be rejected.
   - Any merged, amended, or partially replaced snapshot **must** be rejected.

3. **Snapshot Uniqueness Violation**
   - More than one snapshot produced for the same tick and scope **must** be rejected.
   - Conflicting snapshots associated with the same tick **must** be rejected.

4. **Snapshot Content Illegality**
   - Snapshots containing intent, decisions, execution metadata, or mid-tick state **must** be rejected.
   - Snapshots containing persistence or restore data **must** be rejected.

## 6. Ordering Validation Scenarios

The validation harness **must** detect and reject the following ordering violations:

1. **Pre-Tick Snapshot Creation**
   - Snapshot creation before authoritative tick completion **must** be rejected.

2. **Mid-Tick Observation**
   - Replication or observation of mid-tick or partial state **must** be rejected.

3. **Cross-Tick State Mixing**
   - Any snapshot or replication payload containing state spanning multiple ticks **must** be rejected.

4. **Replication-Driven Simulation Influence**
   - Any influence of replication or snapshot creation on tick execution or ordering **must** be rejected.

## 7. Join / Leave / Reconnect Validation

The validation harness **must** detect and reject the following illegal join, leave, or reconnect behaviors:

1. **Illegal Join Observation**
   - A joining client observing anything other than the most recent finalized snapshot **must** be rejected.
   - Observation of historical snapshots as authoritative history **must** be rejected.

2. **Leave-Induced Simulation Mutation**
   - Any mutation of authoritative state caused by client leave **must** be rejected.
   - Any pause, delay, or reordering of ticks due to leave **must** be rejected.

3. **Illegal Reconnect Reconstruction**
   - Reconnect attempts that reconstruct missed ticks, events, or decisions **must** be rejected.
   - Reconnect attempts that resume client-side runtime state **must** be rejected.

4. **Authority Intrusion**
   - Any client influence over join, leave, or reconnect ordering **must** be rejected.

## 8. Forbidden Networking States

The following networking states **must never exist** and **must be validation-rejectable**:

- Client observation of mid-tick state
- Snapshot use as authoritative simulation input
- Snapshot-based replay, rollback, or prediction
- Client-authored authoritative state
- Multiple authoritative snapshots per tick
- Observation of unfinalized or speculative state
- Reconstruction of simulation history from snapshots

No exception paths are permitted.

## 9. Validation Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **Server Authority**
   - All networking-relevant authoritative state **must** originate from the server.

2. **Observational Replication**
   - Replication **must** be strictly observational and one-way.

3. **Tick Finality**
   - Only completed ticks **must** produce observable snapshots.

4. **Snapshot Finality**
   - Snapshots **must** be immutable and final once created.

5. **Client Isolation**
   - Clients **must never** influence simulation, snapshots, or ordering.

6. **Deterministic Rejection**
   - Identical illegal states **must** always produce identical validation failures.

## 10. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Networking validation scenarios exhaustively cover snapshot, ordering, and observation legality.
- All illegal networking states are explicitly enumerated and rejectable.
- Authority isolation is structurally verifiable.
- Validation outcomes are deterministic and binary.
- No modal or speculative language remains.
- Validation harnesses can deterministically accept or reject networking correctness.
