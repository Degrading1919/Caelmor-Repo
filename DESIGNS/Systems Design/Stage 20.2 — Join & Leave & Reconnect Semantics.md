# Stage 20.2 — Join / Leave / Reconnect Semantics

## 1. Purpose

This document defines the **authoritative runtime semantics** for client join-in-progress, leave, and reconnect within Caelmor’s networking and replication architecture.
It establishes what a client is permitted to observe, what is explicitly forbidden from reconstruction, and the strict ordering and authority guarantees that prevent replay, inference, or simulation reconstruction.
This document introduces no protocols, handshakes, or implementation details.

## 2. Scope

This document applies exclusively to **server-authoritative join, leave, and reconnect semantics**.
It defines observation boundaries, ordering guarantees, and legality conditions relative to authoritative ticks and snapshots.
It does not define authentication, transport, client recovery logic, or engine internals.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 20.0 — Networking & Replication Architecture
- Stage 20.1 — Snapshot Model & Authority Rules
- Stage 19 — World Simulation & Zone Runtime Architecture (all sub-stages)
- Stage 13 — Player Lifecycle & World Session Authority
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Join Semantics

**Definition**

A **join** is the server-authoritative transition by which a connected client becomes eligible to **observe** authoritative state.

**Observation Rules**
- A joining client **must** observe only the most recent **server-authored snapshot** that has been finalized at a tick boundary.
- A joining client **must not** observe mid-tick state.
- A joining client **must not** observe historical snapshots as authoritative history.

**Authority Boundaries**
- A join **must not** influence simulation, tick execution, or authority decisions.
- A joining client **must not** author, infer, or reconstruct simulation state.
- A join **must not** trigger replay or re-execution of runtime logic.

**Eligibility**
- A client **must not** be eligible to observe snapshots unless a valid Player Session is active under Stage 13.
- A client **must not** be eligible to observe world or zone state outside its authorized scope.

## 5. Leave Semantics

**Definition**

A **leave** is the server-recognized cessation of a client’s eligibility to observe authoritative state, whether voluntary or involuntary.

**Rules**
- A leave **must** immediately revoke the client’s eligibility to observe snapshots.
- A leave **must not** mutate world, zone, entity, or player authoritative state.
- A leave **must not** pause, delay, or alter tick execution.

**Isolation**
- Simulation **must** continue deterministically regardless of client leave.
- No runtime state **must** be retained for the purpose of client reconstruction.

**Authority**
- Leave recognition **must** be server-owned.
- Clients **must not** influence the timing or consequences of leave recognition.

## 6. Reconnect Semantics

**Definition**

A **reconnect** is a join by a client that re-establishes observation eligibility after a prior leave.

**Legality Conditions**
- A reconnect **must** be associated with exactly one valid Player Session under Stage 13.
- A reconnect **must not** restore or resume any client-side runtime state.
- A reconnect **must not** assume continuity of observation.

**Observation Rules**
- On reconnect, a client **must** observe only the most recent finalized snapshot.
- A reconnect **must not** reconstruct missed ticks, snapshots, or events.
- A reconnect **must not** infer transitions, actions, or decisions that occurred while disconnected.

**Illegal Reconnect**
- A reconnect **must** be rejected if it attempts to:
  - influence authoritative state,
  - request historical reconstruction,
  - resume partial simulation context.

## 7. Ordering & Authority Guarantees

**Ordering**
- Snapshot creation **must** occur only after authoritative tick completion.
- Client join or reconnect observation **must** occur only after snapshot finalization.
- No client **must** observe state that predates or postdates the finalized snapshot it receives.

**Authority**
- All join, leave, and reconnect recognition **must** be server-owned.
- Clients **must never** influence tick ordering, snapshot content, or simulation authority.

**Isolation**
- Join, leave, and reconnect **must not** introduce side effects into simulation.
- Observation **must** remain strictly one-way from server to client.

## 8. Forbidden Patterns

The following patterns **are explicitly forbidden** and **must be validation-rejectable**:

- Client-triggered replay or rollback
- Client inference of historical simulation state
- Client reconstruction of missed ticks or decisions
- Snapshot mutation based on join or reconnect
- Join or reconnect influencing simulation timing or authority
- Client-authored authoritative state during join, leave, or reconnect

No exception paths are permitted.

## 9. Join / Leave / Reconnect Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **Observational Only**
   - Clients **must** observe authoritative state only through snapshots.

2. **No Reconstruction**
   - Clients **must not** reconstruct or infer simulation history.

3. **Server Authority**
   - All join, leave, and reconnect semantics **must** be server-owned.

4. **Tick Isolation**
   - Join, leave, and reconnect **must not** affect tick execution or ordering.

5. **Snapshot Finality**
   - Clients **must** observe only finalized snapshots.

6. **Client Exclusion**
   - Clients **must never** author, modify, or influence authoritative state.

## 10. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Join, leave, and reconnect semantics are purely observational and closed.
- Ordering relative to ticks and snapshots is explicit and deterministic.
- Authority boundaries prevent replay, inference, or reconstruction.
- All illegal patterns are enumerated and validation-rejectable.
- No modal or speculative language remains.
- Validation harnesses can deterministically accept or reject join, leave, and reconnect behavior.
