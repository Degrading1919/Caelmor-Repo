# Stage 22.3 — NPC Runtime Implementation Plan

## 1. Purpose

This document defines the **implementation plan** for the NPC Runtime in Caelmor.
It translates locked NPC runtime and behavior architecture into a bounded, reviewable, and validation-gated implementation sequence without redefining authority, decision semantics, perception rules, or persistence behavior.
Its purpose is to ensure NPC runtime implementation adheres exactly to canon and cannot introduce silent behavioral, authority, or ordering changes.

## 2. Scope

This document applies exclusively to the **implementation of the NPC Runtime** as defined by canon.
It governs implementation ordering, dependencies, validation gates, and completion criteria.
It does not define gameplay design, content authoring, schemas, networking mechanics, persistence formats, or engine-specific details.

## 3. Canon Dependencies

This implementation plan is **subordinate to and constrained by** the following LOCKED canon:

- Stage 22.0 — Implementation Planning Framework
- Stage 16 — NPC Runtime Architecture (all sub-stages)
- Stage 18 — NPC Behavior & Decision Architecture (all sub-stages)
- Stage 19 — World Simulation & Zone Runtime Architecture (all sub-stages)
- Stage 20 — Networking & Replication Architecture (all sub-stages)
- Stage 21 — Cross-System Persistence Architecture (all sub-stages)
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Implementation Scope Definition

**Included Scope**

The NPC Runtime implementation **must** realize exactly the following canonical responsibilities:

- Server-owned NPC runtime identity and authority
- NPC lifecycle participation within world and zone contexts
- NPC tick participation, perception intake, and evaluation boundaries
- NPC decision evaluation and intent emission strictly as defined by canon
- NPC interaction contracts with world, zone, item, and quest systems
- NPC persistence and restore integration for canon-designated state only

**Excluded Scope**

The NPC Runtime implementation **must not** include:

- NPC content, dialogue, narrative, or encounter design
- World or zone authority logic beyond residency observation
- Player lifecycle, session management, or ownership logic
- Quest progression logic beyond observation and trigger emission
- Item ownership, crafting, or inventory logic
- Networking transport, snapshot encoding, or replication behavior
- Client-side NPC logic or authority

No additional scope is permitted.

## 5. Implementation Ordering & Dependencies

**Ordering Rules**

- World and zone runtime primitives **must** be implemented before NPC runtime implementation begins.
- NPC runtime identity, authority, and tick participation **must** be implemented before behavior evaluation.
- NPC perception boundaries **must** be implemented before decision evaluation.
- NPC decision evaluation and intent emission **must** be implemented before any NPC-to-system interaction.
- Persistence and restore integration **must** be implemented after all NPC runtime transitions and decision flows are implemented.
- Networking and replication integration **must** occur only after authoritative NPC simulation is complete.

**Dependency Discipline**

- NPC Runtime implementation **must not** begin unless all referenced architectural stages are locked.
- NPC Runtime implementation **must not** proceed in parallel with unresolved world/zone authority, networking semantics, or persistence ordering.

## 6. Validation Gates

**Required Validation**

The following validation gates **must** be satisfied before this implementation can advance:

1. **Authority Validation**
   - NPC runtime authority **must** be server-owned and non-delegated.

2. **Tick Participation Validation**
   - NPC tick participation **must** conform exactly to canonical tick boundaries and ordering.

3. **Perception Validation**
   - NPC perception inputs **must** be restricted to the closed canonical input set.

4. **Decision & Intent Validation**
   - NPC decision evaluation and intent emission **must** conform exactly to canonical models.
   - No intent **must** persist across restore.

5. **World & Zone Interaction**
   - NPC interactions **must** respect world and zone authority boundaries.

6. **Persistence & Restore**
   - NPC persisted state **must** restore deterministically without replay, inference, or partial state.

Validation **must** be binary and fail-loud.

## 7. Forbidden Changes

The following changes **are explicitly forbidden** during this implementation:

- Redefining NPC state models or authority ownership
- Altering NPC perception scopes or decision semantics
- Introducing heuristic, probabilistic, or non-deterministic behavior
- Introducing client authority or client-side NPC logic
- Using networking or snapshots to compensate for incomplete NPC simulation
- Introducing partial persistence or inferred restore behavior
- Adding new NPC lifecycle states, intents, or transitions

No exception paths are permitted.

## 8. Completion Criteria

The NPC Runtime implementation is considered complete only when all of the following are true:

- All included scope responsibilities are implemented exactly as defined by canon.
- All validation gates pass deterministically.
- No forbidden changes have been introduced.
- NPC runtime integrates cleanly with world/zone, player lifecycle, quest, item, networking, and persistence systems.
- No undefined, partial, or transitional NPC states exist.

## 9. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Implementation scope and exclusions are explicit and closed.
- Ordering and dependency rules are deterministic and enforceable.
- Validation gates are sufficient to detect all NPC runtime violations.
- Forbidden changes are fully enumerated.
- Completion criteria are unambiguous.
- No modal or speculative language remains.
