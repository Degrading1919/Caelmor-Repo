# Stage 22.5 — Item Runtime Implementation Plan

## 1. Purpose

This document defines the **implementation plan** for the Item Runtime in Caelmor.
It translates locked item runtime architecture into a bounded, reviewable, and validation-gated implementation sequence without redefining ownership models, state semantics, transfer rules, or authority boundaries.
Its purpose is to ensure item runtime implementation adheres exactly to canon and cannot introduce silent behavioral, authority, ordering, or persistence changes.

## 2. Scope

This document applies exclusively to the **implementation of the Item Runtime** as defined by canon.
It governs implementation ordering, dependencies, validation gates, and completion criteria.
It does not define gameplay design, content authoring, schemas, networking mechanics, persistence formats, or engine-specific details.

## 3. Canon Dependencies

This implementation plan is **subordinate to and constrained by** the following LOCKED canon:

- Stage 22.0 — Implementation Planning Framework
- Stage 17 — Item Runtime Architecture (all sub-stages)
- Stage 19 — World Simulation & Zone Runtime Architecture (all sub-stages)
- Stage 20 — Networking & Replication Architecture (all sub-stages)
- Stage 21 — Cross-System Persistence Architecture (all sub-stages)
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Implementation Scope Definition

**Included Scope**

The Item Runtime implementation **must** realize exactly the following canonical responsibilities:

- Server-owned item runtime identity and authority
- Item ownership association with players, NPCs, or world contexts as defined by canon
- Item location, residency, and state representation within world and zone contexts
- Item state transitions strictly as defined by canonical item state and transition rules
- Item interaction eligibility signaling without executing gameplay behavior
- Item persistence and restore integration for canon-designated item state only

**Excluded Scope**

The Item Runtime implementation **must not** include:

- Item content definitions, stats, or gameplay effects
- Crafting, upgrading, durability, or consumption mechanics
- Player, NPC, or quest logic beyond ownership references
- World or zone authority logic beyond residency observation
- Networking transport, snapshot encoding, or replication behavior
- Client-side item logic or authority
- Runtime inference, replay, or heuristic state transitions

No additional scope is permitted.

## 5. Implementation Ordering & Dependencies

**Ordering Rules**

- World and zone runtime primitives **must** be implemented before item runtime implementation begins.
- Player lifecycle implementation **must** be complete before player-owned item ownership integration.
- NPC runtime implementation **must** be complete before NPC-owned item ownership integration.
- Item ownership and location primitives **must** be implemented before item state transitions.
- Item state transitions **must** be implemented before persistence and restore integration.
- Networking and replication integration **must** occur only after authoritative item simulation is complete.

**Dependency Discipline**

- Item Runtime implementation **must not** begin unless all referenced architectural stages are locked.
- Item Runtime implementation **must not** proceed in parallel with unresolved world/zone authority, player lifecycle, NPC runtime, or persistence ordering.

## 6. Validation Gates

**Required Validation**

The following validation gates **must** be satisfied before this implementation can advance:

1. **Authority Validation**
   - Item runtime authority **must** be server-owned and non-delegated.

2. **Ownership Validation**
   - Each item **must** have exactly one valid owning context as defined by canon.

3. **State Transition Validation**
   - Item state transitions **must** conform exactly to canonical transition rules.
   - No partial or mid-transition state **must** be observable.

4. **World & Zone Residency Validation**
   - Item residency **must** conform exactly to world and zone residency constraints.

5. **Persistence & Restore**
   - Item persisted state **must** restore deterministically without replay, inference, or partial state.

Validation **must** be binary and fail-loud.

## 7. Forbidden Changes

The following changes **are explicitly forbidden** during this implementation:

- Redefining item ownership models or authority boundaries
- Altering item state definitions or transition semantics
- Introducing implicit or inferred item state
- Introducing client authority or client-side item logic
- Using networking or snapshots to compensate for incomplete item simulation
- Introducing partial persistence or inferred restore behavior
- Adding new item states, locations, or transitions

No exception paths are permitted.

## 8. Completion Criteria

The Item Runtime implementation is considered complete only when all of the following are true:

- All included scope responsibilities are implemented exactly as defined by canon.
- All validation gates pass deterministically.
- No forbidden changes have been introduced.
- Item runtime integrates cleanly with world/zone, player lifecycle, NPC runtime, networking, and persistence systems.
- No undefined, partial, or transitional item states exist.

## 9. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Implementation scope and exclusions are explicit and closed.
- Ordering and dependency rules are deterministic and enforceable.
- Validation gates are sufficient to detect all item runtime violations.
- Forbidden changes are fully enumerated.
- Completion criteria are unambiguous.
- No modal or speculative language remains.
