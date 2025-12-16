# Stage 26 — Item & Inventory Runtime Integration Definition

## Purpose
Define the **authoritative runtime contract** for items and inventory as deterministic, server-authoritative systems that integrate with lifecycle, zone residency, persistence, and simulation without violating Phase 1.4 constraints.

This stage specifies **what items and inventories are at runtime**, how they may be mutated, and when they are visible to other systems.

This document is a **binding contract**. No code is implemented here.

---

## Scope Clarification

### This Stage Owns
- Runtime representation of items and inventories
- Inventory mutation rules
- Item visibility and ownership guarantees
- Item interaction eligibility gates

### This Stage Does NOT Own
- Item schemas or content definitions
- Crafting recipes or progression tuning
- Persistence IO or serialization
- Combat resolution logic
- Quest logic
- UI presentation
- Tick execution (see Stage 28)

---

## Core Concepts

### Item
An **Item** is a server-authoritative runtime entity representing an instance of content-defined item data.

- Items have stable `ItemInstanceId`
- Items reference immutable content definitions
- Items are never client-authored

### Inventory
An **Inventory** is a server-owned container that holds item instances.

- Inventories belong to exactly one owner (player, NPC, container)
- Inventories do not exist without an owner
- Inventory contents are authoritative on the server

---

## Inventory Invariants (Hard Rules)

The following invariants MUST always hold:

1. Items belong to exactly one inventory at a time.
2. Inventory mutations are server-authoritative only.
3. Inventory mutations are explicit and ordered.
4. Inventory mutations may not occur mid-tick.
5. Inventory state is deterministic.
6. Inventory visibility is governed by ownership and context.

Violation of any invariant is a fatal runtime error.

---

## Mutation Rules

Inventory mutations include:
- Add item
- Remove item
- Transfer item between inventories

### Mutation Requirements
- Mutations must occur outside simulation ticks
- Mutations must be atomic
- Mutations must leave no partial state on failure
- Mutations must validate ownership and eligibility

---

## Ordering Guarantees

- Inventory mutations occur **after** lifecycle eligibility checks
- Inventory mutations occur **before** persistence save windows
- Inventory state is stable during simulation ticks

---

## Interaction Contracts

### With Player Lifecycle
- Only Active players may mutate their inventory
- Suspended or deactivated players may not mutate inventory

### With World Simulation
- Inventory state is read-only during simulation execution
- Simulation may read inventory data but not mutate it

### With Persistence
- Inventory changes may be marked dirty for save
- Inventory systems do not perform IO directly

---

## Failure Modes

The inventory runtime must fail deterministically if:
- Ownership rules are violated
- A mutation is attempted mid-tick
- An invalid item instance is referenced

Failures must:
- Leave no partial inventory state
- Be observable by callers

---

## Explicitly Forbidden Behaviors

The following are explicitly forbidden:

- Client-authored inventory mutations
- Implicit item transfers
- Inventory mutation during simulation
- Inventory logic triggering lifecycle or residency changes
- Non-deterministic inventory ordering

Any implementation exhibiting these behaviors is invalid.

---

## Validation Expectations (Future Stage)

Future validation stages must prove:
- Inventory mutation gating
- Ownership enforcement
- Deterministic inventory state
- No mid-tick mutations

This document is the sole authority for item and inventory runtime correctness.
