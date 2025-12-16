# Stage 29 — Client Replication & Snapshot Runtime Definition

## Purpose
Define the **authoritative runtime contract** for server → client replication, including snapshot generation, eligibility, and delivery guarantees.

This stage specifies **what data may be replicated**, **when snapshots are produced**, and **what ordering and authority rules must be obeyed** so that clients observe a consistent, deterministic view of the world without influencing simulation.

This document is a **binding contract**. No code is implemented here.

---

## Scope Clarification

### This Stage Owns
- Snapshot generation rules
- Replication eligibility gates
- Snapshot delivery ordering guarantees
- Client observation boundaries
- Snapshot invalidation and teardown rules

### This Stage Does NOT Own
- Networking transport implementation
- Compression or serialization formats
- Client-side prediction or interpolation
- Simulation logic (see Stage 28)
- Lifecycle or residency rules (see Stage 23.x)
- Persistence IO

---

## Core Concepts

### Snapshot
A **Snapshot** is a server-authored, read-only representation of authoritative runtime state intended for client consumption.

- Snapshots are immutable once produced
- Snapshots reflect a completed simulation tick
- Snapshots are never client-authored

### Replication Eligibility
An entity is **replication-eligible** if:
1. It is simulation-eligible
2. It is visible to the client’s player context
3. It is not in a transitional or restoring state

Eligibility is evaluated **after** simulation execution.

---

## Snapshot Production Rules

- Snapshots are produced **after** tick finalization
- Snapshots must not reflect partial or mid-tick state
- Snapshot contents are deterministic for a given tick
- Snapshot production must not mutate runtime state

---

## Ordering Guarantees

Replication must respect the following ordering:

1. Simulation tick completes
2. Snapshot is generated from committed state
3. Snapshot is queued for delivery
4. Client receives snapshot asynchronously

Clients must never observe:
- mid-tick state
- partially updated entities
- transient lifecycle or residency changes

---

## Interaction Contracts

### With World Simulation
- Simulation produces authoritative state
- Replication observes state only after commit

### With Player Lifecycle
- Only Active players receive replication
- Suspended or restoring players receive no snapshots

### With Zone Residency
- Only entities resident in visible zones are replicated
- Residency changes are reflected only after completion

---

## Failure Modes

Replication must fail deterministically if:
- Snapshot is attempted mid-tick
- Ineligible entities are included
- Snapshot ordering is violated

Failures must:
- Leave runtime state untouched
- Be observable for diagnostics

---

## Explicitly Forbidden Behaviors

The following are explicitly forbidden:

- Client-authored state replication
- Replication-triggered simulation changes
- Mid-tick snapshot generation
- Snapshot mutation after creation
- Non-deterministic snapshot ordering

Any implementation exhibiting these behaviors is invalid.

---

## Validation Expectations (Future Stage)

Future validation stages must prove:
- Snapshots reflect only committed state
- Eligibility gates are enforced
- Deterministic snapshot contents
- No simulation influence from replication

This document is the sole authority for replication correctness.
