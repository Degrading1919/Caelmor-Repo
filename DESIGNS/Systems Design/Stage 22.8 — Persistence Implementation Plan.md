# Stage 22.8 — Persistence Implementation Plan

## 1. Purpose

This document defines the **implementation plan** for cross-system persistence in Caelmor.
It translates locked persistence architecture into a bounded, reviewable, and validation-gated implementation sequence without redefining save or restore semantics, atomicity rules, dependency ordering, authority boundaries, or networking behavior.
Its purpose is to ensure persistence implementation adheres exactly to canon and cannot introduce partial, inferred, or non-deterministic restore behavior.

## 2. Scope

This document applies exclusively to the **implementation of cross-system persistence** as defined by canon.
It governs implementation ordering, dependencies, validation gates, and completion criteria.
It does not define gameplay design, content authoring, schemas, storage formats, serialization mechanics, or engine-specific details.

## 3. Canon Dependencies

This implementation plan is **subordinate to and constrained by** the following LOCKED canon:

- Stage 22.0 — Implementation Planning Framework
- Stage 21 — Cross-System Persistence Architecture (all sub-stages)
- Stage 19 — World Simulation & Zone Runtime Architecture (all sub-stages)
- Stage 20 — Networking & Replication Architecture (all sub-stages)
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Implementation Scope Definition

**Included Scope**

The Persistence implementation **must** realize exactly the following canonical responsibilities:

- Server-owned persistence orchestration across all participating systems
- Enforcement of cross-system save atomicity
- Enforcement of cross-system restore ordering and dependency satisfaction
- Isolation of persistence from runtime simulation and networking observation
- Deterministic restore from persisted structural truth only
- Rejection of partial, missing, or inconsistent persisted state

**Excluded Scope**

The Persistence implementation **must not** include:

- Storage backends, databases, or file formats
- Serialization or deserialization mechanics
- Save triggers, cadence, or scheduling
- Runtime simulation logic during restore
- Networking or snapshot participation in persistence
- Client-side persistence logic or authority
- Inference, replay, or reconstruction of missing state

No additional scope is permitted.

## 5. Implementation Ordering & Dependencies

**Ordering Rules**

- World and zone simulation **must** be implemented before persistence implementation begins.
- Persistence participation boundaries **must** be implemented after all participating systems expose canonical persistence surfaces.
- Save atomicity enforcement **must** be implemented before restore ordering enforcement.
- Restore ordering enforcement **must** be implemented before any system-level restore integration.
- Persistence implementation **must** be complete before networking and snapshot systems are allowed to observe restored state.

**Dependency Discipline**

- Persistence implementation **must not** begin unless all referenced architectural stages are locked.
- Persistence implementation **must not** proceed in parallel with unresolved world/zone authority, networking semantics, or dependency ordering rules.

## 6. Validation Gates

**Required Validation**

The following validation gates **must** be satisfied before this implementation can advance:

1. **Participation Validation**
   - Only canon-designated systems **must** participate in persistence.

2. **Atomicity Validation**
   - Save operations **must** be all-or-nothing across all participating systems.

3. **Restore Ordering Validation**
   - Restore operations **must** occur in canonical order with all dependencies satisfied.

4. **Restore Legality Validation**
   - Restore **must not** execute runtime logic or emit intents.

5. **Isolation Validation**
   - Networking and snapshots **must not** satisfy persistence or restore requirements.

6. **Rejection Validation**
   - Partial, missing, or inconsistent persisted state **must** be rejected deterministically.

Validation **must** be binary and fail-loud.

## 7. Forbidden Changes

The following changes **are explicitly forbidden** during this implementation:

- Redefining save or restore semantics
- Altering atomicity or dependency ordering rules
- Introducing partial or incremental persistence
- Introducing client authority or client-side persistence logic
- Using networking or snapshots to compensate for persistence gaps
- Introducing replay, rollback, or inferred restore behavior
- Adding new persistence participants or dependency paths

No exception paths are permitted.

## 8. Completion Criteria

The Persistence implementation is considered complete only when all of the following are true:

- All included scope responsibilities are implemented exactly as defined by canon.
- All validation gates pass deterministically.
- No forbidden changes have been introduced.
- Persistence integrates cleanly with world/zone simulation, networking isolation, and system restore boundaries.
- No undefined, partial, or transitional persistence states exist.

## 9. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Implementation scope and exclusions are explicit and closed.
- Ordering and dependency rules are deterministic and enforceable.
- Validation gates are sufficient to detect all persistence violations.
- Forbidden changes are fully enumerated.
- Completion criteria are unambiguous.
- No modal or speculative language remains.
