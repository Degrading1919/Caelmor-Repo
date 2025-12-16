# Stage 20.1 — Snapshot Model & Authority Rules

## 1. Purpose

This document defines the **authoritative snapshot model** for Caelmor networking and replication.
It establishes what a snapshot represents at runtime, who authors it, which state is eligible to appear in snapshots, and the strict authority, immutability, and ordering guarantees that prevent snapshots from influencing simulation, encoding intent, or enabling replay.
This document introduces no serialization, transport, or client interpretation details.

## 2. Scope

This document applies exclusively to **server-authoritative snapshot semantics**.
It defines snapshot meaning, authorship, content eligibility, lifecycle, and invariants relative to the authoritative tick.
It does not define encoding, bandwidth, reliability, frequency tuning, or implementation details.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 20.0 — Networking & Replication Architecture
- Stage 19 — World Simulation & Zone Runtime Architecture (all sub-stages)
- Stage 13 — Player Lifecycle & World Session Authority
- Stage 9 — Validation Philosophy & Harness
- Stage 1.4 — Technical Foundation

If any conflict exists, the above documents take precedence.

## 4. Snapshot Definition

**Snapshot**

A **snapshot** is a server-authored, immutable **observational record** of authoritative runtime state at a specific tick boundary.

**Meaning**
- A snapshot **must** represent **observed truth**, not intent, plan, or history.
- A snapshot **must not** represent execution, causality, or future state.
- A snapshot **must not** be authoritative input to simulation.

**Identity**
- Each snapshot **must** be associated with exactly one authoritative tick.
- Snapshot identity **must not** be client-authored or client-derived.

## 5. Snapshot Authority Rules

**Authorship**
- Snapshots **must** be authored exclusively by the server.
- Clients **must never** author, modify, reorder, or acknowledge snapshots as authoritative.

**Authority Separation**
- Snapshots **must not** mutate world, zone, entity, or player state.
- Snapshots **must not** influence tick ordering, evaluation, or authority decisions.
- Snapshot generation **must** occur strictly after authoritative state is finalized for the tick.

**Delegation**
- Snapshot authority **must not** be delegated to worlds, zones, entities, or clients.

## 6. Snapshot Content Eligibility

**Eligible State (Closed Set)**

Only the following classes of state **are eligible** to appear in snapshots:

- Server-finalized **world structural state** observable at the tick boundary
- Server-finalized **zone structural state** observable at the tick boundary
- Server-finalized **entity observable state** (players, NPCs, items) that does not encode intent or execution
- Server-finalized **ownership and residency outcomes** (results only, not transitions)

**Ineligible State (Explicitly Forbidden)**

The following classes of state **must not** appear in snapshots:

- Runtime intent, decisions, plans, or action descriptors
- Evaluation progress, partial results, or in-flight transitions
- Tick-internal or mid-tick state
- Ordering queues, schedulers, or execution metadata
- Persistence records, save state, or restore markers
- Historical data, deltas-as-truth, or replay inputs
- Client-authored or client-influenced data

No other state classes are permitted.

## 7. Snapshot Lifecycle & Immutability

**Immutability**
- A snapshot **must** be immutable once created.
- A snapshot **must not** be amended, merged, or partially replaced.

**Lifecycle**
- Snapshot creation **must** occur at a tick boundary after state finalization.
- Snapshot consumption **must not** affect snapshot content or authority.
- Snapshot disposal **must** have no effect on simulation or persistence.

**Uniqueness**
- For any given tick, **at most one snapshot must be produced** per scope defined by Stage 20.0.
- Duplicate snapshots for the same tick **must** be rejected.

## 8. Tick & Snapshot Relationship

**Ordering**
- Authoritative tick execution **must** complete before snapshot creation.
- Snapshot creation **must not** occur mid-tick.
- Snapshot creation **must not** trigger additional simulation.

**Isolation**
- Snapshot generation **must** observe finalized state only.
- No system **may** read from snapshots to influence the same or subsequent ticks.

**Restore Interaction**
- Snapshots **must not** be used for restore.
- Restore **must** rely solely on persisted authoritative truth, not snapshots.

## 9. Forbidden Snapshot Patterns

The following patterns **are explicitly forbidden** and **must be validation-rejectable**:

- Snapshots used as authoritative inputs
- Snapshots encoding intent, decisions, or future actions
- Snapshots encoding partial or mid-tick state
- Snapshots enabling replay, rollback, or prediction
- Snapshots containing persistence or save data
- Client-authored, client-merged, or client-ordered snapshots
- Snapshot mutation after creation

No exception paths are permitted.

## 10. Snapshot Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **Server Authorship**
   - Every snapshot **must** be authored by the server.

2. **Observational Only**
   - Snapshots **must** represent observed truth only and **must not** influence simulation.

3. **Immutability**
   - Snapshots **must** be immutable after creation.

4. **Tick Alignment**
   - Each snapshot **must** correspond to exactly one completed authoritative tick.

5. **No Replay**
   - Snapshots **must not** enable replay, rollback, or reconstruction of runtime logic.

6. **Client Exclusion**
   - Clients **must never** author, modify, or treat snapshots as authoritative inputs.

## 11. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Snapshot meaning is purely observational and closed.
- Authority boundaries between simulation and snapshots are absolute.
- Eligible and forbidden snapshot content is explicit and exhaustive.
- Snapshot lifecycle and immutability are unambiguous.
- No modal or speculative language remains.
- Validation harnesses can deterministically accept or reject snapshot legality.
