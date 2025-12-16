# Stage 17.3 — Item Persistence & Restore

## 1. Purpose

This document defines the authoritative rules governing **item persistence, restore semantics, and validation**.
It establishes when item runtime state becomes persisted truth, how item state is restored deterministically, and how item invariants are validated under Stage 9 philosophy.
This document introduces no new item behavior and relies exclusively on rules defined in Stages 17.1–17.2 and Stage 13.5.

## 2. Item Persistence Boundaries

**Persistence Eligibility**

Item runtime state **must** be persisted only at explicit, server-defined save boundaries compliant with Stage 13.5.

**Mandatory Persistence Conditions**
- Item state **must** be persisted when its owning context is persisted:
  - Player-owned items with PlayerSave
  - NPC-owned items with WorldSave or NPC persistence model
  - World-owned items with WorldSave

**Forbidden Persistence Conditions**
- Item state **must not** be persisted:
  - mid-tick
  - during an active item transition
  - during any illegal transition defined in Stage 17.2
  - independently of its owning context
  - as a partial or incremental write

**Atomicity Rules**
- Item persistence **must** be atomic with its owning context.
- Partial item persistence **is forbidden**.
- Item persistence **must not** occur unless the item occupies a legal location and valid state at the persistence boundary.

## 3. Item Restore Semantics

**Restore Source of Truth**
- Item restore **must** use persisted truth only.
- Runtime-only state **must not** be replayed, inferred, or reconstructed.

**Restore Rules**
- Item location **must** be restored exactly as persisted.
- Item state **must** be restored exactly as persisted.
- No item transitions **must** be replayed on restore.
- No item state **must** be inferred from surrounding context.

**Post-Restore Validity**
- Every restored item **must**:
  - occupy exactly one legal location (Stage 17.2),
  - satisfy all item invariants,
  - belong to a valid owning context.
- Any persisted item state that violates invariants **must** cause restore failure.

## 4. Disconnect Handling

**Disconnect During Item Transition**
- The transition **must** be discarded.
- Item state **must** remain at the last valid persisted or runtime-stable state.
- No partial transition **must** persist.

**Disconnect Outside Transition**
- Item persistence behavior **must** follow normal save boundary rules.
- No additional item persistence **must** occur due solely to disconnect.

## 5. Crash Handling

**Crash During Item Transition**
- The transition **must** be treated as non-existent.
- Restore **must** use the last valid persisted item state only.

**Crash During Item Persistence**
- Persistence **must** be treated as atomic.
- On failure:
  - either the full item state is present,
  - or no item persistence is applied.
- Partial item state **must never** be restored.

## 6. Validation Scenarios

The following validation scenarios **must** pass deterministically:

1. **Disconnect During Item Transition**
   - Enforced invariants:
     - Atomic transition rule
     - No partial persistence
   - Forbidden outcome:
     - Item in hybrid or intermediate location

2. **Crash During Item Persistence**
   - Enforced invariants:
     - Atomic persistence
     - Persisted truth only
   - Forbidden outcome:
     - Partially restored item state

3. **Restore With Items in Each Legal Location**
   - Enforced invariants:
     - Exactly one location per item
     - Valid owning context
   - Forbidden outcome:
     - Orphaned or duplicated items

4. **Illegal or Partial Item State Rejection**
   - Enforced invariants:
     - Legal location set
     - Valid state-location pairing
   - Forbidden outcome:
     - Silent correction or inference

All violations **must** fail loudly under Stage 9 validation philosophy.

## 7. Item Invariants

The following invariants **must always hold**:

- An item **must** exist in exactly one legal location.
- Item persistence **must never** occur outside defined persistence boundaries.
- Item restore **must never** infer, replay, or reconstruct transitions.
- Partial item state **must never** be persisted or restored.
- Item state **must** always be valid for its location.
- Item ownership **must** be consistent with its location.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Item stats, rarity, or balance
- Crafting, loot, or drop systems
- UI or inventory presentation
- Client-side authority or manipulation
- Replay, rollback, or reconciliation systems
- Persistence formats, schemas, or databases
- Implementation or engine internals
