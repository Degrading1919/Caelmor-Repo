# Stage 15.1 — Quest Runtime Model

## 1. Purpose

This document defines the canonical **Quest Runtime Model** for Caelmor.
It establishes what a quest is at runtime, how quest instances are owned and scoped, and how they relate to player lifecycle, world context, and persistence.
This document introduces no content, narrative, or UI concepts and serves as authoritative groundwork for subsequent quest stages.

## 2. Quest Runtime Definition

**Quest Instance**

A **quest instance** is a server-defined, server-owned runtime entity representing the authoritative state of a single quest for a specific player.

**Rules**
- A quest instance **must** be server-defined.
- A quest instance **must** be server-owned.
- A quest instance **must** exist only as runtime state governed by server authority.
- A quest instance **must not** be content, narrative, or UI.
- A quest instance **must** be distinct from:
  - quest templates,
  - narrative descriptions,
  - reward definitions,
  - dialogue or presentation data.

**Identity**
- Each quest instance **must** have a unique runtime identity within the scope of its owning player.
- Quest runtime identity **must not** be derived from client input.

## 3. Quest Ownership & Scope

**Ownership**

- Every quest instance **must** be owned by exactly one Player Identity.
- A quest instance **must not** exist without a valid owning Player Identity.
- A quest instance **must not** be shared across multiple Player Identities.

**Scope**

- A quest instance **must** be scoped to a world context.
- A quest instance **must not** exist outside an active or previously active world context.
- A quest instance **must not** outlive its owning Player Identity.

**Constraints**
- Destruction of a Player Identity **must** result in the destruction of all associated quest instances.
- Quest instances **must not** migrate between Player Identities.

## 4. Quest Lifecycle Relationship

**Player Session Relationship**
- Quest instances **must** be associated with their owning Player Identity, not with a specific Player Session.
- Quest instances **must** persist across Player Sessions according to persisted truth.
- Loss or termination of a Player Session **must not** destroy quest instances.

**World Attachment Relationship**
- Quest instances **must** be evaluated and progressed only when the owning Player Session is attached to a world.
- Quest instances **must not** determine or alter world attachment.

**Tick Participation Relationship**
- Quest logic **must not** execute unless the owning Player Session is tick-participating.
- Quest instances **must not** grant, revoke, or influence tick participation.
- Quest instances **must not** control player lifecycle or session state.

## 5. Quest Persistence Relationship

**Persistence Nature**

- Quest state **must** be persisted as player-owned state.
- Quest persistence **must** follow Stage 13 Save & Restore Boundaries.
- Quest persisted state **must** represent authoritative truth.

**Rules**
- Quest state **must not** rely on replay, inference, or reconstruction of runtime events.
- Quest state **must** be sufficient for restore without executing quest logic.
- Quest runtime-only state **must** be treated as discardable on disconnect or crash.

**Restore Behavior**
- On restore, quest instances **must** be reconstructed solely from persisted quest state.
- Quest instances **must not** resume partial runtime execution after restore.

## 6. Authority & Ordering Invariants

The following invariants are mandatory and enforceable by validation:

1. **Server Authority**
   - All quest instance creation, mutation, and destruction **must** be performed by the server.
   - Clients **must never** author, modify, or advance quest runtime state.

2. **Ownership Integrity**
   - Every quest instance **must** belong to exactly one Player Identity.
   - Quest instances **must not** exist without a valid owning player.

3. **Lifecycle Isolation**
   - Quest instances **must not** control or redefine:
     - player identity,
     - player session lifecycle,
     - world attachment,
     - tick participation.

4. **Persistence Safety**
   - Quest persisted state **must** be authoritative.
   - Restore **must not** replay quest logic or infer intermediate state.

## 7. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Quest states, steps, or transitions
- Quest triggers, conditions, or events
- Rewards, consequences, or completion outcomes
- NPCs, dialogue, narrative structure, or storytelling
- Client-side quest tracking, journals, or UI
- Scripting languages, data schemas, or implementation details
- Any form of client authority or quest-driven lifecycle control
