# Stage 16.1 — NPC Runtime Model

## 1. Purpose

This document defines the canonical **NPC Runtime Model** for Caelmor.
It establishes what an NPC is at runtime, how NPC instances are owned and authorized, how they relate to world and zone structure, and how persistence is handled.
This document introduces no AI behavior, dialogue, combat logic, or content definitions.

## 2. NPC Runtime Definition

**NPC Runtime Instance**

An **NPC runtime instance** is a server-defined, server-owned runtime entity representing a non-player character’s authoritative presence in the world.

**Rules**
- An NPC runtime instance **must** be server-defined.
- An NPC runtime instance **must** be server-owned.
- An NPC runtime instance **must** exist as authoritative runtime state.
- An NPC runtime instance **must not** be content, narrative, or presentation.
- An NPC runtime instance **must not** be AI logic or decision-making.

**Separation of Concerns**
An NPC runtime instance **must** be distinct from:
- NPC templates or archetypes
- Dialogue, personality, or narrative data
- AI behavior definitions or decision trees
- Visual, audio, or presentation assets

## 3. NPC Ownership & Authority

**Ownership**

- NPC runtime instances **must** be owned by the world.
- NPC runtime instances **must not** be owned by Player Identities.
- NPC runtime instances **must not** be shared across worlds.

**Authority**

- All NPC creation, mutation, and destruction **must** be server-authoritative.
- Clients **must never** author, control, mutate, or influence NPC runtime state.
- NPC runtime instances **must not** accept client-authored input as authoritative state.

## 4. NPC Scope & Lifecycle Relationship

**World Relationship**
- An NPC runtime instance **must** exist within exactly one world context.
- An NPC runtime instance **must not** exist outside a world context.
- Destruction or unload of a world context **must** result in destruction of all associated NPC runtime instances.

**Zone Relationship**
- An NPC runtime instance **must** reside in exactly one zone within its world.
- NPC zone residency **must** be server-defined and server-ordered.
- An NPC runtime instance **must not** exist without zone residency while active.

**Tick Participation Relationship**
- NPC runtime instances **must** participate in the authoritative server tick only when:
  - their world is active, and
  - their zone is active.
- NPC runtime instances **must not** influence player tick participation.
- NPC runtime instances **must not** control player lifecycle, session state, or onboarding flow.

**Quest Relationship**
- NPC runtime instances **are permitted only** to be observed by quest systems via server-recognized events defined outside this document.
- NPC runtime instances **must not** own quests.
- NPC runtime instances **must not** author, emit, mutate, or directly trigger quest state, progression, or persistence.
- All other forms of NPC–quest interaction **are forbidden**.

## 5. NPC Persistence Relationship

**Allowed Persistence Models**

NPC persistence **must** use **exactly one** of the following models:

1. **Persisted World-Owned State**
   - NPC state is persisted as world-owned authoritative truth.
   - Persisted NPC state **must** follow all Stage 13 save and restore boundaries.

2. **Deterministic Regeneration**
   - NPC state is fully regenerated deterministically on world restore.
   - Regeneration **must** rely only on persisted world truth and deterministic rules.

**Persistence Rules**
- NPC runtime-only state **must** be treated as discardable unless explicitly persisted under one allowed model.
- Partial persistence **is forbidden**.
- Mixed persistence models **are forbidden**.
- NPC restore **must not** rely on replay, inference, or reconstruction of runtime execution.
- NPC restore **must** result in a fully legal NPC runtime state using one allowed model only.

## 6. Authority & Ordering Invariants

The following invariants are mandatory and enforceable by validation:

1. **Server Authority**
   - All NPC runtime state **must** be created, mutated, and destroyed by the server.
   - Clients **must never** influence NPC runtime state.

2. **World Ownership**
   - NPC runtime instances **must** be world-owned.
   - NPC runtime instances **must not** outlive their world context.

3. **Lifecycle Isolation**
   - NPC runtime instances **must not** control or redefine:
     - player identity,
     - player session lifecycle,
     - world attachment,
     - zone residency,
     - tick participation,
     - quest lifecycle.

4. **Persistence Safety**
   - NPC runtime state **must not** be partially persisted.
   - NPC persistence **must** use exactly one allowed persistence model.
   - NPC restore **must** produce a fully legal NPC runtime state without replay or inference.

## 7. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- AI behavior, decision-making, or state machines
- Dialogue systems, narrative roles, or personality traits
- Combat logic, threat models, or abilities
- Pathfinding, navigation, or movement mechanics
- Visuals, animation, audio, or presentation
- Client-side NPC representation or control
- Implementation details, schemas, or data formats
