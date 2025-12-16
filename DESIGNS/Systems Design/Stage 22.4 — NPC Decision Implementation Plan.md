# Stage 22.4 — NPC Decision Implementation Plan

## 1. Purpose

This document defines the **implementation plan** for NPC decision evaluation and intent emission in Caelmor.
It translates locked NPC decision architecture into a bounded, reviewable, and validation-gated implementation sequence without redefining decision models, intent semantics, perception rules, or authority boundaries.
Its purpose is to ensure NPC decision implementation adheres exactly to canon and cannot introduce silent behavioral, authority, ordering, or persistence changes.

## 2. Scope

This document applies exclusively to the **implementation of NPC decision evaluation and intent emission** as defined by canon.
It governs implementation ordering, dependencies, validation gates, and completion criteria.
It does not define gameplay design, content authoring, schemas, networking mechanics, persistence formats, or engine-specific details.

## 3. Canon Dependencies

This implementation plan is **subordinate to and constrained by** the following LOCKED canon:

- Stage 22.0 — Implementation Planning Framework
- Stage 18 — NPC Behavior & Decision Architecture (all sub-stages)
- Stage 16 — NPC Runtime Architecture (all sub-stages)
- Stage 19 — World Simulation & Zone Runtime Architecture (all sub-stages)
- Stage 20 — Networking & Replication Architecture (all sub-stages)
- Stage 21 — Cross-System Persistence Architecture (all sub-stages)
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Implementation Scope Definition

**Included Scope**

The NPC decision implementation **must** realize exactly the following canonical responsibilities:

- Deterministic evaluation of NPC decision inputs as defined by canon
- Deterministic selection of a single decision outcome per evaluation cycle
- Intent emission strictly as defined by canonical intent definitions
- Enforcement of tick-aligned evaluation boundaries
- Enforcement of non-persistence of intents across restore
- Isolation of decision evaluation from world, zone, and entity authority mutation

**Excluded Scope**

The NPC decision implementation **must not** include:

- Changes to decision models, scoring, or selection semantics
- Changes to intent definitions, structures, or meanings
- Changes to perception input scope or acquisition rules
- Execution of intents or behavior resolution
- World, zone, or entity authority mutation
- Networking transport, snapshot encoding, or replication behavior
- Persistence of decision evaluation state or intents
- Client-side decision logic or authority

No additional scope is permitted.

## 5. Implementation Ordering & Dependencies

**Ordering Rules**

- NPC runtime identity, authority, and tick participation **must** be implemented before NPC decision implementation begins.
- NPC perception boundaries **must** be implemented before decision evaluation.
- Decision evaluation **must** be implemented before intent emission.
- Intent emission **must** be implemented before any behavior resolution systems that consume intents.
- Persistence and restore integration **must** be implemented after decision evaluation and intent emission are complete.
- Networking and replication integration **must** occur only after authoritative decision evaluation and intent emission are complete.

**Dependency Discipline**

- NPC decision implementation **must not** begin unless all referenced architectural stages are locked.
- NPC decision implementation **must not** proceed in parallel with unresolved NPC runtime authority, tick ordering, or persistence semantics.

## 6. Validation Gates

**Required Validation**

The following validation gates **must** be satisfied before this implementation can advance:

1. **Authority Validation**
   - Decision evaluation and intent emission **must** be server-owned and non-delegated.

2. **Determinism Validation**
   - Given identical inputs at a tick boundary, decision outcomes **must** be identical.

3. **Input Scope Validation**
   - Decision evaluation **must** consume only the closed, canonical input set.

4. **Selection Validation**
   - Exactly one decision outcome **must** be selected per evaluation cycle.

5. **Intent Semantics Validation**
   - Emitted intents **must** conform exactly to canonical intent definitions.
   - No intent **must** persist across restore.

6. **Tick Boundary Validation**
   - Decision evaluation and intent emission **must** occur only within canonical tick boundaries.

Validation **must** be binary and fail-loud.

## 7. Forbidden Changes

The following changes **are explicitly forbidden** during this implementation:

- Redefining decision models, scoring, or selection rules
- Redefining intent structures, meanings, or lifetimes
- Expanding or altering perception input scope
- Introducing probabilistic, heuristic, or non-deterministic behavior
- Introducing client authority or client-side decision logic
- Persisting decision evaluation state or intents
- Using networking or snapshots to compensate for incomplete decision logic
- Introducing new decision states, intents, or transitions

No exception paths are permitted.

## 8. Completion Criteria

The NPC decision implementation is considered complete only when all of the following are true:

- All included scope responsibilities are implemented exactly as defined by canon.
- All validation gates pass deterministically.
- No forbidden changes have been introduced.
- Decision evaluation and intent emission integrate cleanly with NPC runtime, tick execution, world/zone authority, networking, and persistence systems.
- No undefined, partial, or transitional decision states exist.

## 9. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Implementation scope and exclusions are explicit and closed.
- Ordering and dependency rules are deterministic and enforceable.
- Validation gates are sufficient to detect all NPC decision violations.
- Forbidden changes are fully enumerated.
- Completion criteria are unambiguous.
- No modal or speculative language remains.
