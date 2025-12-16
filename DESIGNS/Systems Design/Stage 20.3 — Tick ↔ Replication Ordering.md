# Stage 20.3 — Tick ↔ Replication Ordering

## 1. Purpose

This document defines the **ordering contract** between authoritative tick execution, snapshot creation, replication eligibility, and client observation.
Its purpose is to eliminate ambiguity, prevent mid-tick or cross-tick observation, and enforce deterministic, restore-safe replication that cannot influence simulation.
This document introduces no implementation details or performance considerations.

## 2. Scope

This document applies exclusively to **server-authoritative ordering semantics** between simulation and replication.
It defines when state becomes observable, what ordering is legal, and which violations are forbidden.
It does not define snapshot frequency, buffering, interpolation, or transport behavior.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 20.0 — Networking & Replication Architecture
- Stage 20.1 — Snapshot Model & Authority Rules
- Stage 20.2 — Join / Leave / Reconnect Semantics
- Stage 19 — World Simulation & Zone Runtime Architecture (all sub-stages)
- Stage 9 — Validation Philosophy & Harness
- Stage 1.4 — Technical Foundation

If any conflict exists, the above documents take precedence.

## 4. Tick Execution Model

**Authoritative Tick**

An authoritative tick is the server-owned, deterministic execution window in which all legal simulation state mutation occurs.

**Rules**
- Tick execution **must** be server-owned and server-ordered.
- Tick execution **must** complete fully before any snapshot is created.
- No authoritative state **must** be observable outside completed tick boundaries.
- No state **must** mutate outside the authoritative tick.

## 5. Snapshot Creation Ordering

**Ordering Rules**
- Snapshot creation **must** occur strictly after authoritative tick completion.
- Snapshot creation **must not** occur mid-tick.
- Snapshot creation **must** observe only finalized authoritative state.

**Uniqueness**
- For any given tick, **exactly one** snapshot **must** be eligible for replication per scope defined by Stage 20.0.
- Duplicate or conflicting snapshots for the same tick **must** be rejected.

## 6. Replication Eligibility Rules

**Eligibility**
- Only snapshots created after tick completion **are eligible** for replication.
- No partial, mid-tick, or speculative state **is eligible** for replication.
- Replication eligibility **must not** depend on client presence or demand.

**Isolation**
- Replication **must not** influence snapshot content.
- Replication **must not** influence tick execution or ordering.

## 7. Client Observation Ordering

**Observation Rules**
- Clients **must** observe only replicated snapshots derived from completed ticks.
- Clients **must not** observe mid-tick or in-progress state.
- Clients **must not** observe cross-tick mixtures of state.

**Join / Reconnect**
- On join or reconnect, a client **must** observe only the most recent finalized snapshot.
- Clients **must not** observe historical sequences as authoritative history.

## 8. Forbidden Ordering Patterns

The following patterns **are explicitly forbidden** and **must be validation-rejectable**:

- Snapshot creation before tick completion
- Snapshot creation during tick execution
- Replication of mid-tick or partial state
- Client observation of in-progress simulation
- Client observation of mixed or cross-tick state
- Snapshot creation or replication influencing simulation ordering
- Use of snapshots for replay, rollback, or prediction

No exception paths are permitted.

## 9. Ordering Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **Tick Supremacy**
   - All authoritative state mutation **must** occur within the tick.

2. **Post-Tick Observation**
   - All observation **must** occur only after tick completion.

3. **Snapshot Finality**
   - Snapshots **must** reflect finalized state only.

4. **Replication Isolation**
   - Replication **must** be observational and one-way.

5. **No Cross-Tick Ambiguity**
   - No observable state **must** span multiple ticks.

6. **Client Exclusion**
   - Clients **must never** influence tick execution, snapshot creation, or ordering.

## 10. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Tick, snapshot, replication, and observation ordering is explicit and closed.
- No mid-tick or cross-tick observation is possible.
- All illegal ordering patterns are enumerated and rejectable.
- Ordering guarantees are deterministic and restore-safe.
- No modal or speculative language remains.
- Validation harnesses can deterministically accept or reject ordering correctness.
