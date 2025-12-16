# Stage 19.4 — Zone Residency Constraints

## 1. Purpose

This document defines **zone residency** as a first-class, authoritative runtime contract.
It establishes what it means for an entity to be resident in a zone, enforces exclusivity and boundary rules, and eliminates ambiguity around transitions, ordering, and restore safety.
This document introduces no spawn, movement, geometry, or implementation details.

## 2. Scope

This document applies exclusively to **server-authoritative runtime residency semantics** at 10 Hz.
It defines legality, ordering, and forbidden states for zone residency across applicable entity types.
It does not define spawn/despawn, movement, streaming, or content logic.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 19.0 — World Simulation & Zone Runtime Architecture
- Stage 19.1 — Zone Runtime Definition
- Stage 19.2 — World Runtime Definition
- Stage 19.3 — World & Zone Authority Boundaries
- Stage 13.3 — World Attachment & Zone Residency
- Stage 16.1 — NPC Runtime Model
- Stage 17.1 — Item Runtime Model

If any conflict exists, the above documents take precedence.

## 4. Zone Residency Definition

**Zone Residency**

Zone residency is the **authoritative association** between a runtime entity and **exactly one** zone within an attached world, conferring eligibility for zone-scoped observation and evaluation.

**Rules**
- Zone residency **must** be server-defined and server-owned.
- Zone residency **must** be scoped to a single world context.
- Zone residency **must not** exist without valid world attachment.
- Zone residency **must not** imply ownership, authority, or persistence control.

## 5. Residency Exclusivity Rules

**Exclusivity**
- An entity that requires zone residency **must** be resident in **exactly one** zone at any time.
- An entity **must not** be resident in more than one zone simultaneously.
- An entity **must not** be resident in zero zones while world-attached and eligible for zone-scoped evaluation.

**Applicability**
- NPC runtime instances **must** satisfy residency exclusivity.
- World-owned item runtime instances **must** satisfy residency exclusivity.
- Player sessions **must** satisfy residency exclusivity while actively world-attached.
- Quest instances **must not** have zone residency.

## 6. Boundary Crossing Constraints

**Authority**
- Zone residency assignment and change **must** be mediated by the world runtime.
- Zones **must not** assign, revoke, or alter residency.

**Legality**
- Residency **must** reference a zone that belongs to the entity’s attached world.
- Cross-world residency **is forbidden**.
- Residency changes **must not** occur mid-tick.

**Atomicity**
- A residency change **must** be atomic: old residency ends and new residency begins at the same tick boundary.
- No intermediate or partial residency state **may** exist.

## 7. Residency Transition Ordering

**Ordering Rules**
- Residency changes **must** occur only at explicit tick boundaries.
- Residency changes **must** be ordered before zone-scoped evaluation for the *following* tick.
- Residency changes **must** be ordered after world attachment validation.

**Tick Interaction**
- An entity **must not** be evaluated by any zone during the tick in which its residency changes.
- An entity **must** become eligible for zone-scoped evaluation starting with the next tick after the residency change.
- No zone **may** evaluate an entity whose residency is changing during the current tick.

**Restore Interaction**
- Residency **must** be reconstructed solely from persisted authoritative truth.
- No residency transition **may** resume or complete on restore.

## 8. Forbidden Residency States

The following states **must never exist** and **must be validation-rejectable**:

- Simultaneous residency in multiple zones
- Residency in a zone not owned by the attached world
- Residency without world attachment
- Partial or in-flight residency persisted across save or restore
- Client-authored or client-influenced residency
- Zone-authored residency changes
- Residency changes occurring mid-tick
- Residency assigned to quests

No exception paths are permitted.

## 9. Residency Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **Server Authority**
   - All residency creation, change, and removal **must** be server-owned.

2. **World Mediation**
   - All residency decisions **must** be mediated by the world runtime.

3. **Exclusivity**
   - Exactly one valid zone residency **must** exist for eligible entities.

4. **Tick Safety**
   - Residency **must not** change outside tick boundaries.

5. **Restore Safety**
   - Residency **must not** rely on replay, inference, or runtime continuation.

6. **No Delegation**
   - Zones **must not** own or control residency authority.

## 10. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Spawn or despawn rules
- Movement, pathfinding, or navigation
- Geometry, volumes, triggers, or colliders
- Streaming, loading, or scene management
- Content placement or encounter design
- Implementation details or engine internals

## 11. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Residency meaning and exclusivity are explicit and closed.
- All boundary and transition rules are deterministic and atomic.
- All illegal states are enumerated and validation-rejectable.
- Restore behavior is replay-free and inference-free.
- No modal or speculative language remains.
- Validation harnesses can deterministically accept or reject residency state.





