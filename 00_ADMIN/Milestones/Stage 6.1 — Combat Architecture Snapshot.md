# Stage 10 — Combat Systems Architecture
## Milestone Snapshot

Project: Caelmor  
Engine: Unity  
Architecture: Server-authoritative, deterministic (10 Hz)  
Status: PLANNED — GOVERNANCE LOCK

---

## 1. Stage Purpose

Stage 10 defines the **foundational architecture for combat systems** in Caelmor.

This stage establishes:
- What combat *is* at a systems level
- How combat actions are represented, ordered, and resolved
- Where authority lives
- How combat integrates with the validated economy, inventory, and persistence layers

Stage 10 does **not** implement combat.  
It defines the **contracts** combat must obey.

The purpose of this stage is to ensure that all future combat implementation:
- Is deterministic
- Is server-authoritative
- Is compatible with persistence and save/restore
- Does not leak assumptions into AI, UI, or content prematurely

---

## 2. Canon Lock Statement

The following systems and documents are **final, authoritative, and immutable**:

- Stage 7–8 Non-Combat Economy & Persistence
- Stage 9 — Integration Testing & Validation Harness (Stages 9.0–9.4)
- Caelmor_Phase1_4_Technical_Foundation.md

Stage 10 **builds on top of** these systems.

Stage 10 does **not**:
- Modify existing runtime systems
- Modify schemas from prior stages
- Introduce new persistence semantics
- Alter tick or networking models

Any deviation from the above is a failure of scope.

---

## 3. Combat Definition (System-Level)

For the purposes of Caelmor, **combat** is defined as:

> The server-authoritative resolution of hostile interactions between entities, expressed as ordered intents processed on a fixed tick, producing deterministic state changes.

Combat is:
- Intent-driven
- Tick-aligned
- Fully authoritative on the server
- Observable, not predictive

Combat is **not**:
- Animation-driven
- Client-predicted
- Real-time physics simulation
- Reaction-based on frame timing

---

## 4. In-Scope (What Stage 10 Does)

Stage 10 defines:

- Combat action **intent representation**
- Resolution order and tick-phase placement
- Authority boundaries between client and server
- Combat state transitions (e.g., idle → attacking → recovery)
- Damage, mitigation, and outcome **contracts** (not values)
- Separation of concerns between:
  - Input
  - Resolution
  - Effects
  - Presentation

Stage 10 produces:
- Schema definitions (structure only)
- Resolution flow diagrams (conceptual)
- Clear system responsibilities

---

## 5. Explicit Non-Goals (Hard Exclusions)

Stage 10 must NOT include:

- Combat implementation code
- Balance or tuning values
- Weapons, armor, or enemy content
- Animation, VFX, or audio
- Hitboxes or physics simulation
- Client-side prediction or reconciliation
- UI or HUD elements
- Skill trees or progression tuning
- AI behavior logic (consumers only)

If work drifts toward “making combat feel good,” it is out of scope.

---

## 6. Authority & Tick Model (Locked)

Combat resolution obeys the following constraints:

- All combat intents are validated and resolved on the server
- Resolution occurs on the authoritative 10 Hz tick
- Inputs are queued and ordered deterministically
- Identical inputs produce identical outcomes
- No combat logic executes on restore
- Save/load restores state without replay

Combat must remain compatible with:
- Stage 7.5 persistence semantics
- Stage 9 validation guarantees

---

## 7. Schema-First Requirement

All combat systems introduced after Stage 10 must:

- Be defined via schemas before implementation
- Separate data from runtime behavior
- Avoid hidden coupling to content or presentation

Stage 10 will identify:
- Required schema categories
- Entity references
- State representations

Stage 10 will **not** finalize numeric fields or tuning ranges.

---

## 8. Exit Criteria (Definition of Done)

Stage 10 is complete when:

- Combat architecture is fully specified at a system level
- Required schemas are identified and structurally defined
- Authority boundaries are unambiguous
- Tick placement and resolution order are explicit
- No downstream system (AI, content, UI) is forced to guess

Only after these conditions are met may combat implementation begin.

---

## 9. Anchor Statement

> “Combat in Caelmor is not spectacle.  
> It is a deterministic system of intent, resolution, and consequence —  
> designed to endure.”
