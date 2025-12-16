# Stage 17.2 — Item Location & State Transitions

## 1. Purpose

This document defines the authoritative rules governing **item location** and **item state transitions** at runtime.
It establishes the complete, closed set of allowed item locations, the structural representation of item state, and the legal transitions between locations and states under server authority.
This document introduces no item stats, crafting logic, loot behavior, or UI concepts.

## 2. Item Location Categories

An item runtime instance **must** exist in **exactly one** of the following location categories at any time.
No other locations are permitted.

**Defined Item Locations**

1. **Player Inventory**
   - The item is owned by a Player Identity and resides within that player’s inventory context.

2. **Equipped**
   - The item is owned by a Player Identity and is actively equipped.
   - Equipped is a distinct location, not a sub-state of inventory.

3. **NPC Possession**
   - The item is owned by an NPC runtime instance.

4. **World Placement**
   - The item exists as world-owned state within a world context.

**Location Rules**
- An item **must** exist in exactly one location at all times.
- Hybrid, overlapping, or ambiguous locations **are forbidden**.
- An item **must not** exist without a valid owning context implied by its location.
- An item **must not** exist in multiple locations simultaneously.

## 3. Item State Representation

**Item State**

Item state is the minimal, structural runtime information required to validate and maintain an item’s existence within its current location.

**Rules**
- Item state **must** be independent of item stats, balance, or attributes.
- Item state **must not** encode UI, presentation, or visual information.
- Item state **must** always be valid for the item’s current location.
- Item state **must** be fully authoritative and server-owned.

**Validity Constraint**
- An item **must not** enter or remain in a location with a state that is invalid for that location.
- Illegal or transitional item states **are forbidden** outside an active, atomic transition.

## 4. Legal Location & State Transitions

**Allowed Transitions**

The following location transitions **are permitted** when performed under server authority and valid lifecycle conditions:

- Player Inventory → Equipped
- Equipped → Player Inventory
- Player Inventory → World Placement
- World Placement → Player Inventory
- Player Inventory → NPC Possession
- NPC Possession → Player Inventory
- NPC Possession → World Placement
- World Placement → NPC Possession

**Forbidden Transitions**

The following transitions **are forbidden**:

- Any transition that results in multiple simultaneous locations
- Any transition that bypasses a valid owning context
- Any transition initiated or ordered by a client
- Any transition that violates player, NPC, or world lifecycle rules
- Any transition that occurs partially or incrementally

**Transition Rules**
- All item location and state transitions **must** be server-authoritative.
- All transitions **must** be atomic.
- No partial transition **must** persist.
- An item **must not** change location more than once within a single authoritative transition boundary.

## 5. Transition Ordering & Authority

**Authority Rules**
- Item transitions **must** be initiated, ordered, and resolved by the server.
- Clients **must never** initiate, reorder, or force item transitions.

**Ordering Rules**
- Item transitions **must** occur only at server-defined boundaries.
- Item transitions **must not** occur mid-tick.
- Transition ordering **must** be deterministic and reproducible.

**Boundary Constraints**
- Item transitions **must not** bypass:
  - player lifecycle rules,
  - NPC lifecycle rules,
  - world attachment rules,
  - save or restore boundaries defined in Stage 13.5.

## 6. Failure & Edge Case Handling

The following cases **must** be handled deterministically:

**Invalid Transition Attempt**
- The transition **must** be rejected.
- Item location and state **must** remain unchanged.

**Transition Attempt During Tick Boundary**
- The transition **must** be deferred until the next valid boundary.
- No partial state **must** apply.

**Session Deactivation During Transition**
- The transition **must** be discarded.
- Item location and state **must** remain at the last valid persisted or runtime state.

**Server Crash During Transition**
- The transition **must** be treated as non-existent unless fully persisted.
- Restore **must** reflect the last valid persisted item state only.
- Partial or inferred transitions **must never** apply.

## 7. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Item stats, attributes, rarity, or balance
- Crafting systems or crafting logic
- Loot generation, drop behavior, or acquisition rules
- Inventory UI or presentation behavior
- Visuals, models, or animations
- Client-side authority or item manipulation
- Implementation details, schemas, or engine internals
