# Stage 19.2 — World Runtime Definition

## 1. Purpose

This document defines the canonical **World Runtime Definition** for Caelmor.
It establishes what a world is as an authoritative runtime construct, how worlds relate to zones and other runtime entities, and the strict authority, lifecycle, tick, and persistence rules governing worlds.
This document introduces no content, simulation systems, or implementation details.

## 2. Scope

This document applies exclusively to **server-authoritative runtime architecture**.
It defines structural meaning, authority boundaries, ordering guarantees, and restore-safe behavior for worlds.
It does not define infrastructure, scaling, content, or presentation.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 19.0 — World & Zone Runtime Architecture
- Stage 19.1 — Zone Runtime Definition
- Stage 13 — Player Lifecycle & World Session Authority
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. World Runtime Definition

**World Runtime Instance**

A **world runtime instance** is a server-defined, server-owned, authoritative runtime construct representing a complete, bounded simulation context within which zones, players, NPCs, items, and world-scoped state exist and are evaluated.

**Rules**
- A world runtime instance **must** be server-defined.
- A world runtime instance **must** be server-owned.
- A world runtime instance **must** have a unique runtime identity.
- A world runtime instance **must not** be client-authored or client-influenced.
- A world runtime instance **must** act as the highest authority boundary below the server itself.
- A world runtime instance **must not** exist outside server control.

**Lifetime**
- A world runtime instance **must** be explicitly created by the server.
- A world runtime instance **must** be explicitly unloaded by the server.
- A world runtime instance **must not** self-create, self-duplicate, or self-resurrect.

## 5. World Authority & Ownership

**Authority Model**
- The world **must** be the authoritative owner of all zones within it.
- The world **must** mediate all cross-zone interactions.
- The world **must** define ordering and eligibility for zone evaluation.
- The world **must not** delegate authority to zones beyond structural context.

**Ownership Constraints**
- Players **must** be owned by Player Identity and Player Session systems, not by the world.
- NPCs **must** be owned by the world runtime.
- Items **must** be owned by player, NPC, or world contexts as defined in Stage 17.
- Quests **must** be owned by Player Identity, not by the world.

The world **must** provide containment and ordering, not ownership reassignment.

## 6. World–Zone Relationship

**Zone Containment**
- A world runtime instance **must** contain zero or more zone runtime instances.
- Each zone runtime instance **must** belong to exactly one world runtime instance.
- A zone **must not** exist outside its owning world.

**Authority Rules**
- Zones **must** operate under world authority.
- Zones **must not** bypass world ordering, tick rules, or persistence boundaries.
- Zones **must not** interact directly with other zones without world mediation.

**Cross-Zone Mediation**
- All cross-zone effects **must** be mediated by the world runtime.
- Zones **must not** directly mutate state belonging to other zones.
- The world **must** enforce deterministic ordering for all zone-to-zone interactions.

## 7. World Tick Participation Rules

**Tick Participation Definition**
World tick participation is the server-defined inclusion of a world runtime instance in the authoritative 10 Hz server tick.

**Rules**
- World tick participation **must** be server-defined and server-owned.
- World tick participation **must** be binary: participating or not participating.
- World tick participation **must not** occur mid-tick.
- World tick participation **must** gate all zone tick participation.
- A zone **must not** tick-participate unless its owning world is tick-participating.

**Ordering Responsibilities**
- The world **must** define deterministic ordering for zone evaluation.
- The world **must** ensure that all zone evaluation occurs within the same tick boundary.
- The world **must not** allow zone state mutation outside the authoritative tick.

## 8. World Persistence Relationship

**Persistence Nature**
- World persisted state **must** represent authoritative structural truth.
- World persistence **must** follow Stage 13 save and restore boundaries.
- Partial world persistence **is forbidden**.

**Rules**
- World persistence **must not** rely on replay, inference, or reconstruction of runtime activity.
- Runtime-only world state **must** be discarded on unload, disconnect, or crash.
- On restore, the world **must** be reconstructed solely from persisted world state.
- No world runtime activity **may** resume automatically after restore.

**Unload Semantics**
- When a world unloads, all zones **must** be deterministically destroyed.
- All world-scoped runtime-only state **must** be discarded.
- No world-owned runtime entity **may** survive world unload.

## 9. Authority & Ordering Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **Server Supremacy**
   - Worlds **must** exist only under server authority.
   - Clients **must never** author, influence, or reorder world state.

2. **World Containment**
   - All zones **must** belong to exactly one world.
   - Cross-zone interaction **must** be world-mediated.

3. **Tick Integrity**
   - World and zone state **must not** mutate outside authoritative tick boundaries.
   - Tick ordering **must** be deterministic and server-owned.

4. **Restore Safety**
   - World restore **must not** replay runtime logic.
   - No runtime-only world state **may** persist across restore.

5. **No Authority Leakage**
   - Worlds **must not** redefine player identity, session lifecycle, or quest ownership.
   - Worlds **must not** introduce client authority or prediction.

## 10. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Sharding, instancing, or scaling strategies
- Server infrastructure or deployment topology
- Scene loading, streaming, or geometry
- Time-of-day, weather, or simulation subsystems
- Content population or encounter design
- UI, presentation, or visualization
- Client-side logic, prediction, rollback, or replay
- Engine internals, schemas, or implementation details

## 11. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- World authority boundaries are explicit and closed.
- World–zone relationships are deterministic and non-overridable.
- Tick participation and ordering responsibilities are unambiguous.
- Persistence and restore rules are complete and replay-free.
- No modal or speculative language remains.
- Validation harnesses can deterministically accept or reject world state.
