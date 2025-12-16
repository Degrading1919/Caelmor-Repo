# Stage 17.1 — Item Runtime Model

## 1. Purpose

This document defines the canonical **Item Runtime Model** for Caelmor.
It establishes what an item is at runtime, how item instances are owned and authorized, how they relate structurally to players, NPCs, and the world, and how persistence is handled.
This document introduces no item stats, balance, crafting, loot logic, or UI concepts.

## 2. Item Runtime Definition

**Item Runtime Instance**

An **item runtime instance** is a server-defined, server-owned runtime entity representing a discrete, authoritative item existing within the game world or an owning context.

**Rules**
- An item runtime instance **must** be server-defined.
- An item runtime instance **must** be server-owned.
- An item runtime instance **must** exist as authoritative runtime state.
- An item runtime instance **must not** be content data, UI, or presentation.
- An item runtime instance **must** be distinct from:
  - item templates,
  - crafting outputs,
  - loot tables or loot definitions.

**Identity**
- Each item runtime instance **must** have a unique runtime identity.
- Item runtime identity **must not** be client-generated or client-influenced.

## 3. Item Ownership & Authority

**Ownership Models**

An item runtime instance **must** belong to exactly one of the following owning contexts at any time:

- **Player-Owned**
  - The item is owned by a specific Player Identity.
- **NPC-Owned**
  - The item is owned by a specific NPC runtime instance.
- **World-Owned**
  - The item exists as part of world state without a player or NPC owner.

**Ownership Rules**
- An item runtime instance **must not** exist without a valid owning context.
- An item runtime instance **must not** be owned by more than one context simultaneously.
- Ownership transfer **must** be server-authoritative and explicit.

**Authority**
- All item creation, mutation, transfer, and destruction **must** be performed by the server.
- Clients **must never** create, destroy, duplicate, or mutate item runtime instances.
- Client input **must not** be treated as authoritative item state.

## 4. Item Scope & Relationships

**Player Relationship**
- Player-owned items **must** be structurally associated with a Player Identity.
- Item existence **must not** control or redefine player lifecycle, session state, or tick participation.

**NPC Relationship**
- NPC-owned items **must** be structurally associated with an NPC runtime instance.
- Item possession **must not** grant NPC authority over item persistence rules.

**World Relationship**
- World-owned items **must** be associated with a valid world context.
- World-owned items **must not** exist outside an active or persisted world state.

**Lifecycle Constraints**
- Item runtime instances **must not** outlive their owning context.
- Destruction of an owning context **must** result in deterministic item resolution according to server rules defined elsewhere.
- Item runtime instances **must not** bypass player, NPC, or world lifecycle boundaries.

## 5. Item Persistence Relationship

**Persistence Nature**

- Item state **must** be persisted according to Stage 13.5 Save & Restore Boundaries.
- Item persistence **must** be authoritative truth.
- Partial item persistence **is forbidden**.

**Restore Rules**
- Item restore **must** use persisted truth only.
- Item restore **must not** replay item-related runtime logic.
- Item restore **must not** infer missing or intermediate state.
- Restored item state **must** always represent a legal item runtime instance with a valid owning context.

**Runtime State**
- Item runtime-only state **must** be discarded on restore unless explicitly persisted.
- No item runtime state **must** resume automatically after restore.

## 6. Authority & Ordering Invariants

The following invariants are mandatory and enforceable by validation:

1. **Server Authority**
   - All item runtime state **must** be created, mutated, transferred, and destroyed by the server.
   - Clients **must never** influence authoritative item state.

2. **Ownership Exclusivity**
   - Every item runtime instance **must** have exactly one owning context.
   - Item runtime instances **must not** exist without ownership.

3. **Lifecycle Isolation**
   - Item runtime instances **must not** control or redefine:
     - player identity,
     - player session lifecycle,
     - NPC lifecycle,
     - world attachment,
     - tick participation.

4. **Persistence Safety**
   - Item persistence **must** follow Stage 13.5 rules.
   - Restore **must not** replay or infer item state.
   - Partial or mixed-version item state **must never** be observable.

## 7. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Item stats, attributes, rarity, or balance
- Crafting systems or crafting logic
- Loot generation or drop behavior
- Inventory UI or presentation
- Visuals, models, or animations
- Client-side item authority
- Implementation details, schemas, or storage formats
