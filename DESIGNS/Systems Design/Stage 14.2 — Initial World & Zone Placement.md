# Stage 14.2 — Initial World & Zone Placement

## 1. Purpose

This document defines the authoritative rules for **initial world and zone placement** of an entry-eligible player.
It specifies how the server assigns world attachment and zone residency for first-time and returning players.
This stage establishes structural placement only and does not grant control, tick participation, or gameplay exposure.

## 2. Placement Definition

**Placement**

Placement is the server-authoritative assignment of:
- a **world attachment**, and
- an **initial zone residency**
to an entry-eligible Player Session.

**Rules**
- Placement **must** occur only after entry eligibility is granted (Stage 14.1).
- Placement **must** assign exactly one world and exactly one zone.
- Placement **must** begin world attachment and zone residency immediately upon completion.
- Placement **must not** grant:
  - player control,
  - tick participation,
  - access to gameplay systems.
- Placement **must** be server-defined and server-ordered.

## 3. World Selection Rules

**World Selection**

World selection is the server-owned determination of which world runtime a Player Session will attach to during placement.

**Rules**
- World selection **must** be performed by the server.
- World selection **must** be deterministic given the same authoritative inputs.
- World selection **must not** be influenced by the client.
- World selection **must** result in exactly one world attachment.
- World selection **must** not modify Player Identity or PlayerSave.

**Eligibility Constraint**
- Placement **must not** proceed unless the selected world is available to accept the Player Session.

## 4. Zone Selection Rules

**Zone Selection**

Zone selection is the server-defined assignment of an initial zone residency within the selected world.

**Rules**
- Zone selection **must** be performed by the server.
- Zone selection **must** result in exactly one zone residency.
- Zone residency **must** begin immediately upon placement.
- A Player Session **must not** exist without zone residency once placement completes.
- Zone selection **must not** be influenced by the client.

## 5. First-Time Player Placement

**Definition**

A first-time player is a Player Identity whose persisted truth indicates no prior completed placement.

**Rules**
- First-time placement **must** use server-defined default world and zone selection rules.
- First-time placement **must not** rely on inferred or client-declared state.
- First-time placement **must** result in valid world attachment and zone residency.
- First-time placement **must** be fully deterministic based on server rules.

## 6. Returning Player Placement

**Definition**

A returning player is a Player Identity whose persisted truth indicates prior completed placement.

**Rules**
- Returning placement **must** be based solely on persisted truth in PlayerSave.
- Persisted world and zone references **must** be used if valid.
- Client input **must not** influence returning placement.
- If persisted placement data is invalid or unavailable, placement **must** fail deterministically.

## 7. Authority & Ordering Invariants

The following invariants are mandatory and enforceable by validation:

1. **Server Authority**
   - World and zone placement **must** be initiated and ordered by the server.
   - Clients **must never** select, alter, or negotiate placement.

2. **Ordering**
   - Entry eligibility **must** precede placement.
   - Placement **must** precede any control, tick participation, or gameplay exposure.

3. **Atomicity**
   - World attachment and zone residency **must** be applied together.
   - Partial placement **must never** be observable.

4. **Exclusivity**
   - A Player Session **must** be attached to exactly one world.
   - A Player Session **must** reside in exactly one zone after placement.

## 8. Failure & Edge Case Handling

The following cases **must** be handled deterministically:

**World Unavailable at Placement Time**
- Placement **must not** proceed.
- World attachment and zone residency **must not** be applied.
- The Player Session **must** remain entry-eligible only.

**Invalid or Missing Persisted Placement Data**
- Placement **must** fail deterministically.
- No fallback or inference **may** occur.

**Session Deactivation During Placement**
- Placement **must** be aborted.
- No partial world or zone assignment **may** persist.

**Server Crash During Placement**
- Placement state **must** be treated as non-existent on restore.
- World attachment and zone residency **must not** resume automatically.
- Placement **must** be re-attempted only through normal lifecycle flow.

## 9. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Spawn points, coordinates, or geometry
- Movement, collision, traversal, or physics
- Player control, input handling, or camera logic
- Tick participation or gameplay system activation
- UI, tutorials, narrative, or onboarding presentation
- Client authority, negotiation, or placement choice
