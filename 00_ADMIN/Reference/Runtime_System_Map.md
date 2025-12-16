# Caelmor — Runtime System Map
## Authoritative Runtime Ownership & Execution Reference

Status: ACTIVE  
Authority Level: Runtime-Authoritative  
Derived From: Phase 1.4 — Technical Foundation  
Applies To: All runtime C# systems and execution paths

---

## 1. Purpose

This document defines **which runtime systems exist**, **what data they own**, **how they update**, and **what they persist**.

It exists to:
- Eliminate ambiguity during C# implementation
- Prevent scope creep and speculative systems
- Provide a single source of truth for runtime ownership
- Ensure all execution aligns with Phase 1.4 constraints

This document is **not** a design or brainstorming artifact.  
It is **binding** for implementation.

---

## 2. Global Runtime Constraints (From Phase 1.4)

These rules apply to **all systems**:

- Engine: Unity
- Language: C#
- Authority Model: Host-authoritative
- Tick Rate: 10 Hz fixed server tick
- Client Role: Input + presentation only
- Persistence: Explicit save boundaries, no implicit autosave
- Content Source: JSON only (schema-validated)
- Runtime Code: Never generates content definitions

---

## 3. Runtime Systems Overview

### System Categories
- Core Execution
- Player & Session
- World & Zones
- Entities & Actors
- Interaction & Progression
- Persistence & Validation
- Networking
- Client Presentation (Minimal)

---

## 4. Core Execution Systems

### 4.1 TickSystem
**Purpose:** Global time authority

- Owns:
  - Server tick loop (10 Hz)
- Updates:
  - Every tick
- Calls:
  - All tick-participating systems
- Does NOT:
  - Own game state
  - Perform logic beyond scheduling

---

### 4.2 ValidationHarness
**Purpose:** Deterministic correctness validation

- Owns:
  - Scenario execution
  - Snapshot capture
  - Assertion evaluation
- Updates:
  - Explicit invocation only
- Used For:
  - Save/restore safety
  - Tick determinism
  - Cross-system invariants

---

## 5. Player & Session Systems

### 5.1 PlayerIdentitySystem
**Purpose:** Player identity authority

- Owns:
  - PlayerId generation
  - Player ↔ Save binding
- Updates:
  - On session creation
- Persists:
  - Player identity reference
- Prohibits:
  - Client-supplied identifiers

---

### 5.2 PlayerSessionSystem
**Purpose:** Session lifecycle control

- Owns:
  - Session activation/deactivation
  - Reconnect handling
- Updates:
  - On connect/disconnect events
- Persists:
  - Session state as needed

---

### 5.3 PlayerLifecycleSystem
**Purpose:** Player runtime state machine

- Owns:
  - Player active/inactive state
  - Tick eligibility
- Updates:
  - Tick-gated
- Depends On:
  - PlayerIdentitySystem
  - Zone residency

---

## 6. World & Zone Systems

### 6.1 WorldManager
**Purpose:** Global world authority

- Owns:
  - World-level state
  - Zone registry
- Updates:
  - Tick-gated
- Persists:
  - WorldSave data

---

### 6.2 ZoneManager
**Purpose:** Zone lifecycle and residency

- Owns:
  - Zone instances
  - Player and NPC residency
- Updates:
  - Tick-gated
- Persists:
  - Zone-local state
- Prohibits:
  - Cross-zone logic execution

---

### 6.3 SpawnSystem
**Purpose:** Controlled entity creation

- Owns:
  - Spawn/despawn rules
- Updates:
  - Event-driven + tick-gated
- Depends On:
  - ZoneManager
- Does NOT:
  - Decide behavior

---

## 7. Entity & Actor Systems

### 7.1 EntitySystem
**Purpose:** Base entity state

- Owns:
  - Entity IDs
  - Alive/dead state
- Used By:
  - Players
  - NPCs
  - World objects

---

### 7.2 NPCSystem
**Purpose:** NPC runtime ownership

- Owns:
  - NPC state
  - Tick participation
- Updates:
  - Tick-gated
- Depends On:
  - ZoneManager
  - NPCDecisionSystem

---

### 7.3 NPCDecisionSystem
**Purpose:** Deterministic decision evaluation

- Owns:
  - Candidate construction
  - Evaluation
  - Selection
- Emits:
  - ActionIntents
- Updates:
  - Tick-gated
- Prohibits:
  - Direct world mutation

---

### 7.4 IntentResolutionSystem
**Purpose:** Safe execution of intents

- Owns:
  - Intent validation
  - Ordered execution
- Updates:
  - Tick-gated
- Prohibits:
  - Client-side execution

---

## 8. Items & Inventory

### 8.1 InventorySystem
**Purpose:** Item ownership and containment

- Owns:
  - Player inventories
  - Containers
- Updates:
  - Event-driven
- Persists:
  - Inventory state

---

### 8.2 ItemSystem
**Purpose:** Item runtime state

- Owns:
  - Item location
  - Item transitions
- Depends On:
  - InventorySystem
  - WorldManager

---

## 9. Quest & Progression

### 9.1 QuestSystem
**Purpose:** Quest state tracking

- Owns:
  - Quest states
  - Objective progress
- Updates:
  - Event-driven + tick-gated
- Persists:
  - Quest progress
- Prohibits:
  - Direct NPC or world mutation

---

## 10. Combat

### 10.1 CombatSystem
**Purpose:** Combat resolution

- Owns:
  - Damage calculation
  - State transitions
- Updates:
  - Tick-gated
- Depends On:
  - IntentResolutionSystem

---

## 11. Persistence

### 11.1 SaveSystem
**Purpose:** Explicit persistence control

- Owns:
  - Save boundaries
  - Serialization ordering
- Persists:
  - PlayerSave
  - WorldSave
- Prohibits:
  - Implicit autosave

---

## 12. Networking

### 12.1 NetworkSessionSystem
**Purpose:** Client connection management

- Owns:
  - Join/leave
  - Reconnect
- Depends On:
  - PlayerSessionSystem

---

### 12.2 ReplicationSystem
**Purpose:** State replication

- Owns:
  - Snapshot generation
  - AOI filtering
- Updates:
  - Tick-gated
- Prohibits:
  - Authority override

---

## 13. Client Presentation (Minimal)

### 13.1 InputSystem (Client)
**Purpose:** Input capture

- Emits:
  - Input commands only
- Prohibits:
  - Game logic

---

### 13.2 UIPresentationSystem
**Purpose:** State visualization

- Owns:
  - HUD
  - Debug views
- Depends On:
  - Replicated snapshots

---

## 14. Explicitly Out of Scope (v1)

The following systems do NOT exist in v1 runtime:

- Dynamic server scaling
- Sharding
- Client-side prediction
- AI learning systems
- Emergent simulation beyond tick rules
- Procedural narrative generation

Any implementation implying these is invalid.

---

## 15. Authority Statement

If a system or behavior is not listed in this document,  
**it does not exist at runtime without explicit approval**.

This document overrides:
- Assumptions
- Inspiration material
- External game references
