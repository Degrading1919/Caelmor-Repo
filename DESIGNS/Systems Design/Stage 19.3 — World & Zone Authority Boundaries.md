# Stage 19.3 — World & Zone Authority Boundaries

## 1. Purpose

This document defines the **authoritative boundaries** between the server, world runtime, zone runtime, and all entity systems.
Its sole purpose is to make **authority leakage structurally impossible** by specifying which layers are permitted to mutate which state, which interactions are forbidden, and how ordering is guaranteed.
This document introduces no enforcement mechanisms or implementation details.

## 2. Scope

This document applies exclusively to **server-authoritative runtime architecture** at 10 Hz.
It defines authority boundaries, permitted mutations, forbidden transfers, and ordering guarantees across runtime layers.
It does not define behavior, content, persistence formats, or client participation.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 19.0 — World & Zone Runtime Architecture
- Stage 19.1 — Zone Runtime Definition
- Stage 19.2 — World Runtime Definition
- Stage 13 — Player Lifecycle & World Session Authority
- Stage 16 — NPC Runtime Architecture
- Stage 17 — Item Runtime Architecture
- Stage 15 — Quest Runtime Architecture

If any conflict exists, the above documents take precedence.

## 4. Authority Layers Overview

**Authority Layers (Top to Bottom)**

1. **Server**
2. **World Runtime**
3. **Zone Runtime**
4. **Entity Systems**
   - Player Identity / Player Session
   - NPC Runtime
   - Item Runtime
   - Quest Runtime

**Global Rules**
- Authority **must** flow strictly downward.
- No lower layer **may** redefine, override, or bypass a higher layer.
- Each layer **must** mutate only state it explicitly owns.
- All authority **must** originate at the server.

## 5. World–Zone Authority Boundary

**World Authority**
- The world **must** own all zones within its scope.
- The world **must** determine zone creation, activation, tick participation, ordering, and destruction.
- The world **must** mediate all cross-zone interactions.

**Zone Constraints**
- Zones **must not** exist without a world.
- Zones **must not** act independently of world authority.
- Zones **must not** determine their own tick participation.
- Zones **must not** mutate world-owned state.

**Ordering**
- Zone evaluation order **must** be defined by the world.
- Zones **must not** influence or reorder world evaluation.

## 6. Zone–Entity Authority Boundary

**Zone Authority**
- Zones **must** provide structural context only.
- Zones **must not** own entities.

**Entity Constraints**
- Players **must** be owned exclusively by Player Identity and Player Session systems.
- NPCs **must** be owned by the world runtime.
- Items **must** be owned by player, NPC, or world contexts only.
- Quests **must** be owned exclusively by Player Identity.

**Residency**
- Zone residency **must** be assigned and changed only by the world.
- Zones **must not** change entity ownership, lifecycle, or persistence.

## 7. Cross-Zone and Cross-System Authority Rules

**Cross-Zone Interaction**
- Zones **must not** directly mutate state belonging to other zones.
- All cross-zone effects **must** be mediated by the world runtime.
- The world **must** impose deterministic ordering on all cross-zone interactions.

**Cross-System Interaction**
- Entity systems **must not** directly mutate world or zone authority state.
- World and zone systems **must not** directly mutate player identity, quest ownership, or item ownership.

**Observation vs Mutation**
- Lower layers **may** observe higher-layer state when explicitly allowed by canon.
- Observation **must not** imply authority to mutate.

## 8. Forbidden Authority Transfers

The following transfers **are explicitly forbidden**:

- Server authority delegated to clients
- World authority delegated to zones
- Zone authority delegated to entities
- Entity authority delegated upward
- Player sessions owning worlds or zones
- Zones owning players, NPCs, items, or quests
- Quests mutating world, zone, or entity lifecycle
- NPCs mutating zone or world authority
- Items mutating ownership rules or authority scope

No exception paths are permitted.

## 9. Authority & Ordering Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **Single Source of Authority**
   - All authoritative mutation **must** originate at the server.

2. **Strict Layering**
   - Authority **must** flow only from server → world → zone → entity systems.

3. **Ownership Exclusivity**
   - Every runtime entity **must** have exactly one owning authority layer.

4. **Tick Containment**
   - No authority layer **may** mutate state outside authoritative tick boundaries.

5. **Restore Safety**
   - No authority **may** resume runtime-only state after restore.
   - Restore **must** rely solely on persisted authoritative truth.

6. **Client Exclusion**
   - Clients **must never** author, reorder, or influence authoritative state.

## 10. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Enforcement mechanisms or guardrails
- Error handling or failure recovery
- Logging, metrics, or debugging systems
- Performance optimization or scaling
- Client-side behavior or presentation
- Implementation patterns or engine details

## 11. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- All authority boundaries are explicit, closed, and non-overlapping.
- No downward delegation of ownership or authority exists.
- All forbidden transfers are enumerated and unambiguous.
- Ordering guarantees are deterministic and restore-safe.
- No modal or speculative language remains.
- Validation harnesses can deterministically detect authority violations.
