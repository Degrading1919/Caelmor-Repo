# Stage 19.1 — Zone Runtime Definition

## 1. Purpose

This document defines the canonical **Zone Runtime Definition** for Caelmor.
It establishes what a zone is as an authoritative runtime construct, how zones relate structurally to worlds and other runtime entities, and the strict authority, lifecycle, tick, and persistence rules governing zones.
This document introduces no content, presentation, or implementation details.

## 2. Scope

This document applies to **server-authoritative runtime architecture** only.
It defines structural meaning, authority boundaries, and ordering guarantees for zones.
It does not define geometry, population, navigation, encounters, streaming, or engine behavior.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 13 — Player Lifecycle & World Session Authority
- Stage 14 — Onboarding & First-Session Flow
- Stage 15 — Quest Runtime Architecture
- Stage 16 — NPC Runtime Architecture
- Stage 17 — Item Runtime Architecture
- Stage 18 — NPC Behavior & Decision Architecture
- Stage 19.0 — World & Zone Runtime Architecture
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Zone Runtime Definition

**Zone Runtime Instance**

A **zone runtime instance** is a server-defined, server-owned, world-scoped runtime construct representing a bounded **structural subdivision of a world** for authority, observation, and tick-scoped evaluation.

**Rules**
- A zone runtime instance **must** be server-defined.
- A zone runtime instance **must** be server-owned.
- A zone runtime instance **must** belong to **exactly one** world runtime.
- A zone runtime instance **must not** exist outside a valid world runtime.
- A zone runtime instance **must not** be independently authoritative.
- A zone runtime instance **must not** own players, NPCs, items, or quests.

**Identity**
- Each zone runtime instance **must** have a unique identity within its owning world runtime.
- Zone identity **must not** be client-authored or client-derived.

## 5. Zone Authority & Ownership

**Authority Model**
- Zones **must** operate strictly under world authority.
- Zones **must not** bypass, replace, or override world ownership or ordering.
- Zones **must not** exercise authority over player lifecycle, NPC lifecycle, item lifecycle, or quest ownership.

**Ownership Constraints**
- Players **must** be owned by Player Identity and Player Session systems, not by zones.
- NPCs **must** be owned by the world runtime, not by zones.
- Items **must** be owned by player, NPC, or world contexts, not by zones.
- Quests **must** be owned by Player Identity, not by zones.

Zones provide **structural context only** and never ownership.

## 6. Zone Residency Rules

**Residency Definition**
Zone residency is the authoritative association of a runtime entity with a specific zone within its world context.

**Rules**
- An entity that participates in zone-scoped evaluation **must** have exactly one valid zone residency at any time.
- Zone residency **must** be world-mediated and server-authoritative.
- Zone residency **must not** be client-authored or client-influenced.

**Entity Residency Requirements**
- NPCs **must** have valid zone residency to participate in tick or perception.
- World-owned items **must** have valid zone residency to exist in the world.
- Players **must** have valid zone residency while actively participating in a world.
- Quests **must not** have zone residency; quests observe zones without residing in them.

**Exclusivity**
- No runtime entity **may** reside in more than one zone simultaneously.
- Loss of valid zone residency **must** result in deterministic removal from zone-scoped evaluation.

## 7. Zone Tick Participation Rules

**Tick Participation Definition**
Zone tick participation is the server-defined inclusion of a zone in authoritative per-tick evaluation.

**Rules**
- Zone tick participation **must** be server-defined and server-owned.
- Zone tick participation **must** be binary: participating or not participating.
- Zone tick participation **must not** occur unless the owning world is tick-participating.
- Zone tick participation **must not** occur mid-tick.
- Zone tick participation **must not** mutate zone state outside tick boundaries.

**Participation Scope**
- A zone **must** participate in the tick only when explicitly included by the server.
- Entities within a zone **must not** tick-participate unless both the world and the zone are active.
- Zones **must not** grant tick participation to entities independently of world rules.

## 8. Zone Persistence Relationship

**Persistence Nature**
- Zone runtime state **must** be treated as **world-scoped structural state**.
- Zone persistence **must** follow world persistence boundaries defined in Stage 13.
- Zones **must not** persist runtime-only evaluation state.

**Rules**
- Persisted zone state **must** represent authoritative truth only.
- Zone persistence **must not** rely on replay, inference, or reconstruction of runtime activity.
- On restore, zones **must** be reconstructed solely from persisted world state.
- Runtime-only zone state **must** be discarded on unload, disconnect, or crash.

**World Unload**
- When a world unloads, all zone runtime instances **must** be deterministically destroyed.
- No zone runtime instance **may** survive world unload.

## 9. Authority & Ordering Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **World Supremacy**
   - Zones **must not** exist without a world.
   - Zones **must not** act independently of world authority.

2. **No Ownership Leakage**
   - Zones **must never** own players, NPCs, items, or quests.

3. **Tick Containment**
   - Zone state **must not** mutate outside authoritative tick boundaries.
   - Zone tick participation **must** follow world tick ordering.

4. **Restore Safety**
   - Zone restore **must not** replay runtime logic.
   - No zone runtime-only state **may** persist across restore.

5. **No Cross-Zone Mutation**
   - Zones **must not** directly mutate state belonging to other zones.
   - All cross-zone effects **must** be mediated by the world runtime.

6. **Client Exclusion**
   - Clients **must never** author, influence, or reorder zone state or zone transitions.

## 10. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Scene loading, streaming, or geometry
- Navigation meshes, pathfinding, or movement
- NPC behavior, AI logic, or encounters
- Content population or spawn rules
- Performance optimization or load balancing
- UI, presentation, or visualization
- Client-side logic or prediction
- Engine internals, schemas, or implementation details

## 11. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- All authority boundaries are explicit and closed.
- Zone-world relationships are deterministic and non-overridable.
- No modal or speculative language remains in enforceable rules.
- Restore behavior is fully defined without replay or inference.
- Validation harnesses can deterministically accept or reject zone state.
- No downstream system can reinterpret zone ownership, authority, or lifecycle.
