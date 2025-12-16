# Stage 13.3 — World Attachment & Zone Residency

## 1. Purpose

This document defines the canonical, server-authoritative rules governing **world attachment** and **zone residency** for an active Player Session.
It establishes how a Player Session becomes attached to a world runtime, how zone residency is defined within that world, and how authority and ordering are enforced.
All future systems must treat this document as authoritative and compatible with Stage 13.1 (Player Identity Model) and Stage 13.2 (Player Session Lifecycle).

## 2. World Attachment Definition

**World Attachment**  
World Attachment is the server-authoritative association of an **active Player Session** with **exactly one world runtime**, enabling world-governed logic to apply to that session.

**Characteristics**
- World Attachment **must** occur only after Player Session activation.
- A Player Session **must** be attached to **exactly one** world at all times while active.
- A Player Session **must not** exist in an active state without being attached to a world.
- A Player Session **must not** exist “between worlds.”

**Authority Relationship**
- The world runtime **is authoritative** over all world-scoped state affecting the Player Session.
- Player Session state **must** be subordinate to world authority while attached.

## 3. World Attachment Rules

- World Attachment **must** be initiated by the server.
- World Attachment **must** be ordered by the server.
- World Attachment **must not** be initiated, selected, modified, or influenced by the client.
- World Attachment **must** bind the Player Session to a specific world runtime before any world or zone logic applies.
- World Attachment **must not** modify Player Identity.
- World Attachment **must not** modify PlayerSave.
- If a Player Session cannot be attached to a world, the session **must not** proceed as active.

## 4. Zone Residency Definition

**Zone Residency**  
Zone Residency is the server-defined association of an attached Player Session with **exactly one zone** within the currently attached world.

**Characteristics**
- Zone Residency **exists only within** the context of a world attachment.
- A Player Session **must** reside in **exactly one** zone at any time while attached to a world.
- Zone Residency **must not** exist independently of a world attachment.

**Scope of Effect**
- Zone-scoped logic **must** apply to the Player Session only while it resides in that zone.
- Zone-scoped logic **must** cease immediately when the Player Session leaves the zone or loses world attachment.

## 5. Zone Residency Rules

- Zone Residency **must** be assigned by the server.
- Zone Residency **must** be ordered by the server.
- Zone Residency **must not** be influenced by the client.
- Zone Residency **must** begin applying immediately upon assignment.
- Zone Residency **must** cease applying immediately upon removal or replacement.
- A Player Session **must not** reside in more than one zone at any time.
- A Player Session **must not** have zero zone residency while attached to a world.

## 6. Zone Transitions (Structural Only)

**Definition**  
A **Zone Transition** is the server-authoritative reassignment of a Player Session from one zone to another within the same world.

**Structural Rules**
- Zone Transitions **must** occur only within an existing world attachment.
- Zone Transitions **must** be initiated and ordered by the server.
- Zone Transitions **must** replace the previous zone residency with a new one.
- Zone Transitions **must not** result in overlapping or undefined zone residency.
- The specific causes, timing, or mechanics of zone transitions are out of scope for this document.

## 7. Authority & Ordering Invariants

The following invariants are mandatory and enforceable by validation:

1. **Server Authority**
   - All world attachments, detachments, zone assignments, and zone transitions **must** be initiated and ordered by the server.
   - Clients **must never** initiate, select, alter, or negotiate world or zone attachment.

2. **Single World Attachment**
   - A Player Session **must** be attached to exactly one world while active.
   - A Player Session **must never** be attached to multiple worlds simultaneously.

3. **Single Zone Residency**
   - A Player Session **must** reside in exactly one zone at any time while attached to a world.

4. **Ordering**
   - Session activation **must** precede world attachment.
   - World attachment **must** precede zone residency.
   - Zone residency **must** be valid before zone-scoped logic applies.

5. **Authority Supremacy**
   - World and zone state **must** be authoritative over Player Session behavior within their scope.

## 8. Failure & Edge Case Handling

The following cases **must** be handled deterministically:

**Session Activation When Target World Is Unavailable**
- The Player Session **must not** attach to any world.
- The Player Session **must not** proceed as active.
- The session **must** be deactivated or terminated according to server authority.

**Session Deactivation While Attached to a World**
- World attachment **must** be removed.
- Zone residency **must** be cleared.
- Player Identity and PlayerSave **must** remain intact.

**Server Crash With Active World Attachments**
- All world attachments and zone residencies **must** be treated as non-existent on restore.
- No Player Session **may** resume as attached or resident after restore.

**Restore Behavior**
- Player Identity and PlayerSave **must** be restored from persisted truth.
- World attachment and zone residency **must** be re-established only through normal session lifecycle rules.
- No attachment or residency state **may** be inferred or replayed.

## 9. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- World instancing, shards, layers, or matchmaking
- Zone geometry, boundaries, layouts, or spatial representation
- Movement, traversal, collision, or physics
- Tick timing or update order
- Save timing or persistence cadence
- Streaming, loading, or unloading mechanics
- Client prediction, reconciliation, or authority
- UI, onboarding, or user-facing world concepts
