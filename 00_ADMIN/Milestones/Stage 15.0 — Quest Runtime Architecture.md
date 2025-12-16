# Stage 15.0 — Quest Runtime Architecture

---

## 1. Purpose

Stage 15 defines the **runtime architecture for quests** in Caelmor.

This stage establishes:
- What a quest is at runtime
- How quests are owned, progressed, resolved, and persisted
- How quest logic interacts with the authoritative server model

This stage exists to prevent quest behavior from being:
- embedded in NPCs
- embedded in regions
- embedded in content data
- implemented ad hoc without validation

---

## 2. Scope

Stage 15 governs **quest runtime behavior only**.

It applies to:
- Quest instances
- Quest state transitions
- Quest progress evaluation
- Quest persistence and restore
- Quest validation

Stage 15 does **not** define:
- Quest content
- Quest writing
- NPC dialogue
- Narrative structure
- Rewards or balance values

---

## 3. Canon Dependencies

Stage 15 assumes the following are LOCKED and authoritative:
- Stage 13 — Player Lifecycle & World Session Authority
- Stage 14 — Onboarding & First-Session Flow
- Stage 9 — Validation Philosophy & Harness
- Stage 7–8 — Non-Combat Economy
- Stage 10–12 — Combat Architecture & Runtime

Stage 15 must not bypass or redefine any of the above.

---

## 4. Stage Breakdown

Stage 15 is split into small, lockable sub-stages:

### 15.1 — Quest Runtime Model
Defines:
- What a quest instance is
- Ownership and authority rules
- Relationship between player, quest, and world
- High-level persistence expectations

### 15.2 — Quest State & Progression Rules
Defines:
- Quest states and legal transitions
- Progress evaluation rules
- Structural progression model (no content logic)

### 15.3 — Quest Triggers & Events (Structural)
Defines:
- How world events advance quests
- How quests listen to server-side events
- No scripting language, no content wiring

### 15.4 — Quest Save, Restore & Validation
Defines:
- Persistence boundaries
- Restore semantics
- Validation scenarios aligned with Stage 9

Each sub-stage is independently lockable.

---

## 5. Explicit Non-Goals

Stage 15 does not define:
- Quest JSON schemas
- Quest authoring tools
- NPC quest givers
- Dialogue trees
- Reward tuning
- UI or journal presentation
- Scripting languages
- Client-driven quest logic

Any of the above appearing in Stage 15 is a canon violation.

---

## 6. Lock Criteria

Stage 15.0 is LOCKED when:
- Quest runtime concerns are fully separated from content
- Sub-stage boundaries are explicit
- No authority, lifecycle, or persistence rules are duplicated

Stage 15.0 exists solely to frame Stages 15.1–15.4.
