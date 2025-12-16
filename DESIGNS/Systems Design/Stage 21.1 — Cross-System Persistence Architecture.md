# Stage 21.1 — Cross-System Persistence Architecture

## 1. Purpose

This document defines the **cross-system persistence architecture** for Caelmor.
It establishes which runtime systems participate in persistence, the authority and ownership boundaries between those systems, and the atomic save and deterministic restore rules required to prevent partial, inconsistent, or desynchronized restores.
This document introduces no storage formats, serialization mechanics, or implementation details.

## 2. Scope

This document applies exclusively to **server-authoritative persistence semantics** across multiple runtime systems.
It defines participation, ownership, atomicity, ordering, and legality rules for save and restore.
It does not define save cadence, triggers, databases, performance optimizations, or engine internals.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 21.0 — Cross-System Persistence Architecture
- Stage 19 — World Simulation & Zone Runtime Architecture (all sub-stages)
- Stage 20 — Networking & Replication Architecture (all sub-stages)
- Stage 13.5 — Save & Restore Boundaries
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Persistence Participation Overview

**Participating Systems**

The following runtime systems **must** participate in persistence as authoritative sources of truth:

- Player Identity and PlayerSave
- World runtime (including zone structural composition)
- NPC runtime (state designated as persistable by canon)
- Item runtime (ownership and location state)
- Quest runtime (player-owned quest state)

**Non-Participating Systems**

The following systems **must not** participate in persistence:

- Networking and replication systems
- Snapshots or replication artifacts
- Tick execution or scheduling systems
- Runtime evaluation, intent, or decision systems
- Client-side or client-derived state

No other systems are permitted to participate in persistence.

## 5. Cross-System Ownership & Authority

**Ownership Rules**
- Each persisted datum **must** have exactly one owning system.
- Ownership **must** be defined by canon and **must not** overlap across systems.
- No system **must** persist data owned by another system.

**Authority Boundaries**
- All persistence authority **must** originate at the server.
- Systems **must not** delegate persistence authority to other systems.
- Clients **must never** author, modify, or influence persisted state.

**Dependency Constraints**
- Persisted data **must not** depend on runtime-only state from another system.
- Persisted data **must not** require reconstruction through cross-system inference.

## 6. Save Atomicity Rules

**Atomic Save Definition**

A save operation is atomic only if **all participating systems** persist their authoritative state as a single, coherent unit.

**Rules**
- Cross-system persistence **must** be atomic.
- Partial saves **are forbidden**.
- A save **must not** complete if any participating system fails to produce authoritative persisted state.
- Persisted state **must** represent a mutually consistent snapshot of authoritative truth across systems.

**Isolation**
- Runtime mutation **must not** interleave with save completion.
- No system **must** observe partially saved cross-system state.

## 7. Restore Ordering & Legality

**Restore Ordering**

Restore **must** occur in the following deterministic order:

1. Player Identity and PlayerSave
2. World structural state and zone composition
3. NPC, item, and quest persisted state bound to the restored world and players
4. Eligibility for runtime activation

No other ordering is permitted.

**Legality Rules**
- Restore **must** use persisted authoritative truth only.
- Restore **must not** replay, infer, or reconstruct runtime execution.
- Restore **must** fail deterministically if any required persisted component is missing, inconsistent, or illegal.
- No system **must** activate runtime evaluation during restore.

**Post-Restore State**
- All restored systems **must** be inactive until explicitly activated by the server.
- No tick participation **must** occur automatically on restore.

## 8. Forbidden Cross-System Persistence Patterns

The following patterns **are explicitly forbidden** and **must be validation-rejectable**:

- Partial cross-system saves
- Mixed-version or mixed-epoch persisted state
- Persisting runtime-only, tick-internal, or evaluation state
- Cross-system inference during restore
- Replay-based or event-log-based reconstruction
- Snapshot-based restore or networking-assisted restore
- Client-authored or client-influenced persisted state

No exception paths are permitted.

## 9. Persistence Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **Single Ownership**
   - Every persisted datum **must** have exactly one owning system.

2. **Atomicity**
   - Cross-system persistence **must** be all-or-nothing.

3. **Authoritative Truth**
   - Persisted state **must** represent authoritative truth only.

4. **Deterministic Restore**
   - Given identical persisted truth, restore outcomes **must** be identical.

5. **No Replay**
   - Restore **must not** execute or resume runtime logic.

6. **Client Exclusion**
   - Clients **must never** author, modify, or influence persisted state.

## 10. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Persistence participation is explicit and closed.
- Ownership and authority boundaries are unambiguous and non-overlapping.
- Cross-system save atomicity is absolute.
- Restore ordering and legality rules are deterministic and complete.
- All forbidden persistence patterns are enumerated and rejectable.
- No modal or speculative language remains.
- Validation harnesses can deterministically accept or reject cross-system persistence state.
