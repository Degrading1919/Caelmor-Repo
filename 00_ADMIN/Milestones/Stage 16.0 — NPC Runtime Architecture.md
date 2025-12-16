# Stage 16.0 — NPC Runtime Architecture

---

## 1. Purpose

Stage 16 defines the **runtime architecture for Non-Player Characters (NPCs)** in Caelmor.

This stage establishes:
- What an NPC is at runtime
- How NPCs exist, tick, perceive, and interact under server authority
- How NPC runtime behavior is persisted and restored

This stage exists to prevent NPC behavior from being:
- embedded in content or dialogue
- implemented ad hoc per region
- coupled to client-side assumptions
- intertwined with quest or combat logic without clear contracts

---

## 2. Scope

Stage 16 governs **NPC runtime behavior only**.

It applies to:
- NPC runtime instances
- NPC lifecycle and authority
- NPC tick participation and perception
- NPC interaction contracts (structural only)

Stage 16 does **not** define:
- NPC content or personalities
- Dialogue trees or narrative
- AI behavior trees or scripts
- Combat tuning or abilities
- UI or presentation

---

## 3. Canon Dependencies

Stage 16 assumes the following are LOCKED and authoritative:
- Stage 13 — Player Lifecycle & World Session Authority
- Stage 14 — Onboarding & First-Session Flow
- Stage 15 — Quest Runtime Architecture
- Stage 9 — Validation Philosophy & Harness
- Stage 10–12 — Combat Architecture & Runtime

Stage 16 must not bypass or redefine any of the above.

---

## 4. Stage Breakdown

Stage 16 is split into small, lockable sub-stages:

### 16.1 — NPC Runtime Model
Defines:
- What an NPC instance is
- Ownership, authority, and scope
- Relationship to world, zone, and tick

### 16.2 — NPC Tick Participation & Perception
Defines:
- When NPCs participate in ticks
- Structural perception rules (no AI logic)

### 16.3 — NPC Interaction Contracts
Defines:
- How players and systems interact with NPCs
- Structural interaction rules only

### 16.4 — NPC Save, Restore & Validation
Defines:
- Persistence boundaries
- Restore semantics
- Validation scenarios aligned with Stage 9

Each sub-stage is independently lockable.

---

## 5. Explicit Non-Goals

Stage 16 does not define:
- NPC behavior trees or state machines
- Dialogue or writing
- Quest logic
- Combat AI logic
- Pathfinding or navigation
- Client-side NPC prediction
- Scripting languages
- Content schemas

Any of the above appearing in Stage 16 is a canon violation.

---

## 6. Lock Criteria

Stage 16.0 is LOCKED when:
- NPC runtime concerns are fully separated from content and AI logic
- Sub-stage boundaries are explicit
- Authority, tick, and persistence rules are unambiguous

Stage 16.0 exists solely to frame Stages 16.1–16.4.
