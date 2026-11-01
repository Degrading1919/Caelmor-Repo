# Stage 23.3 — Player Zone Residency Runtime Definition

## Purpose
Define the **authoritative runtime contract** for player zone residency.

This stage specifies **what it means for a player to be resident in a zone**, how residency is established and removed, and what guarantees other systems may rely on. This document is a **binding contract** for all future implementations.

This stage does **not** implement code.

---

## Scope Clarification

### This Stage Owns
- The concept of **zone residency**
- Player ↔ zone association rules
- Residency invariants and guarantees
- Attach and detach semantics
- Residency query contracts

### This Stage Does NOT Own
- Zone loading or unloading
- World streaming or scene management
- Tick execution
- Player lifecycle state transitions
- Session management
- Persistence or save logic
- Combat, AI, quests, or NPC behavior

---

## Core Concepts

### Zone
A **Zone** is a server-defined world partition that may contain:
- Players
- NPCs
- Environmental simulation
- Interactive entities

Zones are assumed to exist and be identifiable by a stable `ZoneId`.

### Zone Residency
**Zone residency** is the authoritative declaration that:
> “This player is currently present in, and simulated within, this zone.”

A player may be **resident in exactly one zone at a time**.

---

## Residency Invariants (Hard Rules)

The following invariants MUST always hold:

1. A player may be resident in **zero or one** zones.
2. A player **cannot** be resident in multiple zones simultaneously.
3. A player **must** have a valid runtime player instance before residency.
4. Residency is **server-authoritative only**.
5. Residency changes are **explicit**, never implicit.
6. Residency attach and detach operations are **idempotent**.
7. A player with no residency is **not simulated by the world**.

Violation of any invariant is a fatal runtime error.

---

## Residency Lifecycle

### Attach Residency
Attaching a player to a zone establishes residency.

**Preconditions**
- Player runtime instance exists
- Target zone exists
- Player is not resident in another zone

**Behavior**
- Player becomes resident in the target zone
- Zone residency state is updated atomically
- Queries reflect new residency immediately

**Postconditions**
- Player has exactly one active zone residency
- Zone lists player as resident

---

### Detach Residency
Detaching a player removes zone residency.

**Preconditions**
- Player runtime instance exists
- Player is currently resident in a zone

**Behavior**
- Player is removed from zone residency
- Zone no longer lists player as resident
- Operation is safe to call multiple times

**Postconditions**
- Player has zero active zone residencies

---

## Ordering Guarantees

Zone residency operations must respect the following ordering guarantees:

- Residency attach occurs **after** player runtime instance creation
- Residency detach occurs **before** player runtime instance destruction
- Residency detach occurs **before** session deactivation side effects
- Residency changes must not occur mid-tick (see Stage 28)

---

## Query Contracts

The zone residency system must expose deterministic queries:

- GetZoneForPlayer(PlayerId) → ZoneId | None
- GetPlayersForZone(ZoneId) → Set<PlayerId>
- IsPlayerResident(PlayerId) → bool

Queries must:
- Be constant-time or bounded-time
- Reflect authoritative state only
- Never return partial or transitional state

---

## Failure Modes

The system must define deterministic failure handling for:

- Attaching to a nonexistent zone
- Attaching a player already resident elsewhere
- Detaching a player with no residency
- Detaching during forbidden execution windows

Failures must:
- Leave no partial state
- Be explicit and detectable by callers

---

## Interaction Contracts

### With Player Runtime Instances
- Residency requires a valid runtime player instance
- Residency does not create or destroy player instances

### With Lifecycle Systems
- Residency does not control lifecycle state
- Lifecycle systems may require residency to proceed

### With World Simulation
- World simulation must only process resident players
- Non-resident players are excluded from simulation

---

## Explicitly Forbidden Behaviors

The following are **explicitly forbidden**:

- Implicit zone assignment
- Automatic zone switching
- Client-selected zone residency
- Residency changes during simulation ticks
- Residency logic triggering lifecycle transitions
- Residency logic interacting with persistence

Any implementation exhibiting these behaviors is invalid.

---

## Validation Expectations (Future Stage)

Future validation stages must prove:
- Single-zone invariant enforcement
- Idempotent attach/detach
- Deterministic failure handling
- Correct ordering relative to lifecycle and simulation

This document is the sole authority for correctness.
