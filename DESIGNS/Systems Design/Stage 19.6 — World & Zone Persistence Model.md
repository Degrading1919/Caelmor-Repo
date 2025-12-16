# Stage 19.4 — World & Zone Persistence Model

## 1. Purpose

This document defines the **structural persistence and restore model** for worlds and zones in Caelmor.
It establishes what world and zone persistence represent as authoritative truth, which state is permitted to persist, which state is forbidden, and the deterministic ordering and legality guarantees for restore.
This document introduces no storage formats, serialization logic, or implementation details.

## 2. Scope

This document applies exclusively to **server-authoritative runtime persistence semantics**.
It defines persistence meaning, restore legality, and discard rules for world and zone runtime constructs.
It does not define save cadence, triggers, checkpoints, or performance considerations.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 19.0 — World & Zone Runtime Architecture
- Stage 19.1 — Zone Runtime Definition
- Stage 19.2 — World Runtime Definition
- Stage 19.3 — World & Zone Authority Boundaries
- Stage 13.5 — Save & Restore Boundaries
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Persistence Model Overview

**Persistence Definition**

Persistence represents **authoritative structural truth** required to reconstruct a legal runtime state without replay, inference, or execution of runtime logic.

**Global Rules**
- Persistence **must** represent truth, not history.
- Persistence **must not** encode runtime execution, evaluation progress, or transient state.
- Persistence **must** be sufficient for restore without replay.
- Partial persistence **is forbidden**.

**World–Zone Composition**
- World persistence **must** define the existence and composition of zones.
- Zone persistence **must not** exist independently of world persistence.

## 5. World Persistence Rules

**Persisted World State**

World persistence **must** represent only the following structural truths:
- World runtime identity
- World existence and eligibility for activation
- World-owned structural state required for legal restore
- Zone composition belonging to the world

**Rules**
- World persisted state **must** be authoritative.
- World persisted state **must not** represent runtime-only evaluation or tick state.
- World persisted state **must not** represent partially applied transitions.
- World persistence **must** be atomic with respect to world structural truth.

**World Unload**
- On world unload, all runtime-only world state **must** be discarded.
- Persisted world state **must** remain unchanged unless explicitly updated as authoritative truth.
- No runtime execution state **may** survive world unload.

## 6. Zone Persistence Rules

**Zone Persistence Scope**

Zones **must not** persist independent runtime authority.
Zone persistence, if present, **must** exist solely as part of persisted world structural truth.

**Allowed Zone Persistence**
- Zone identity within the world
- Zone existence as a structural subdivision
- Zone-to-world association

**Forbidden Zone Persistence**
- Zone tick state
- Zone evaluation state
- Zone ordering state
- Zone residency transitions in progress
- Any runtime-only zone data

**Rules**
- Zone persistence **must** be atomic with world persistence.
- Zones **must not** be restored independently of their world.
- Zones **must not** exist in persisted form without a valid owning world.

## 7. Restore Ordering & Legality

**Restore Ordering**
Restore **must** occur in the following deterministic order:

1. World structural state
2. Zone structural composition
3. Eligibility for world activation

No other ordering is permitted.

**Legality Rules**
- Restore **must** use persisted truth only.
- Restore **must not** replay runtime logic.
- Restore **must not** infer or regenerate missing persisted state.
- Illegal or partial persisted state **must** cause restore failure.

**Post-Restore State**
- Restored worlds and zones **must** be inactive until explicitly activated by the server.
- No tick participation **may** occur automatically on restore.

## 8. Forbidden Persistence Patterns

The following persistence patterns **are explicitly forbidden**:

- Partial world persistence
- Partial zone persistence
- Runtime-only state persistence
- Tick, evaluation, or ordering state persistence
- Replay-based or event-log-based reconstruction
- Cross-version mixed persistence
- Client-authored or client-influenced persisted state
- Persistence of transient residency or in-flight transitions

No exception paths are permitted.

## 9. Persistence & Restore Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **Authoritative Truth**
   - Persisted world and zone state **must** represent authoritative structural truth only.

2. **Atomicity**
   - World and zone persistence **must** be atomic and internally consistent.

3. **Restore Determinism**
   - Given identical persisted truth, restore outcomes **must** be identical.

4. **No Replay**
   - Restore **must not** execute or resume runtime logic.

5. **Discard of Runtime State**
   - All runtime-only world and zone state **must** be discarded on unload or crash.

6. **Client Exclusion**
   - Clients **must never** author, influence, or modify persisted world or zone state.

## 10. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Storage formats, databases, or files
- Serialization or deserialization logic
- Save frequency, checkpoints, or autosave behavior
- Performance optimization or memory management
- Error recovery strategies or logging
- Implementation details or engine internals

## 11. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Persistence meaning is structural, authoritative, and closed.
- All allowed and forbidden persisted state is explicit.
- Restore ordering is deterministic and complete.
- No replay, inference, or partial persistence is permitted.
- No modal or speculative language remains.
- Validation harnesses can deterministically accept or reject persisted state.
