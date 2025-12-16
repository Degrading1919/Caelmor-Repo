# Stage 17.0 — Item Runtime Architecture

---

## 1. Purpose

Stage 17 defines the **runtime architecture for items** in Caelmor.

This stage establishes:
- What an item is at runtime
- How items exist, move, equip, and persist under server authority
- How items participate in inventory, world, and equipment contexts

This stage exists to prevent item behavior from being:
- embedded in content data
- hardcoded in UI or equipment logic
- implicitly defined by crafting or loot systems
- reworked later due to missing authority or persistence rules

---

## 2. Scope

Stage 17 governs **item runtime behavior only**.

It applies to:
- Item runtime instances
- Item ownership and authority
- Item location (inventory, world, equipment)
- Item persistence and restore

Stage 17 does **not** define:
- Item stats or balance
- Item rarity or progression
- Item crafting recipes
- Loot tables
- Visual models or icons
- UI presentation

---

## 3. Canon Dependencies

Stage 17 assumes the following are LOCKED and authoritative:
- Stage 13 — Player Lifecycle & World Session Authority
- Stage 14 — Onboarding & First-Session Flow
- Stage 15 — Quest Runtime Architecture
- Stage 16 — NPC Runtime Architecture
- Stage 7–8 — Economy & Crafting Foundations
- Stage 9 — Validation Philosophy & Harness

Stage 17 must not bypass or redefine any of the above.

---

## 4. Stage Breakdown

Stage 17 is split into small, lockable sub-stages:

### 17.1 — Item Runtime Model
Defines:
- What an item instance is
- Authority and ownership rules
- Relationship to player, world, and NPCs

### 17.2 — Item Location & State Transitions
Defines:
- Inventory presence
- World presence
- Equipped state
- Legal transitions between states

### 17.3 — Item Persistence & Restore
Defines:
- Persistence boundaries
- Restore semantics
- Validation scenarios

Each sub-stage is independently lockable.

---

## 5. Explicit Non-Goals

Stage 17 does not define:
- Item balance or stats
- Crafting math
- Loot generation
- UI or inventory screens
- Equipment visuals or animation
- Client-side prediction
- Content schemas

Any of the above appearing in Stage 17 is a canon violation.

---

## 6. Lock Criteria

Stage 17.0 is LOCKED when:
- Item runtime concerns are fully separated from content and presentation
- Sub-stage boundaries are explicit
- Authority, lifecycle, and persistence rules are unambiguous

Stage 17.0 exists solely to frame Stages 17.1–17.3.
