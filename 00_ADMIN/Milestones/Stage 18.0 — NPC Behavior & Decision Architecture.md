# Stage 18.0 — NPC Behavior & Decision Architecture

---

## 1. Purpose

Stage 18 defines the **behavioral and decision-making architecture for NPCs** in Caelmor.

This stage establishes:
- How NPCs decide what to do
- How decisions are evaluated and executed
- How behavior remains deterministic, authoritative, and bounded

This stage exists to prevent NPC behavior from being:
- hardcoded
- embedded in dialogue or quests
- implemented as opaque AI logic
- tightly coupled to combat or world systems

---

## 2. Scope

Stage 18 governs **NPC decision architecture only**.

It applies to:
- Behavior evaluation
- Decision selection
- Action intent generation

Stage 18 does **not** define:
- AI behavior trees
- Navigation or pathfinding
- Combat tactics
- Dialogue writing
- Personality content
- NPC schedules or scripts

---

## 3. Canon Dependencies

Stage 18 assumes the following are LOCKED:
- Stage 13 — Player Lifecycle & Authority
- Stage 14 — Onboarding
- Stage 15 — Quest Runtime Architecture
- Stage 16 — NPC Runtime Architecture
- Stage 17 — Item Runtime Architecture
- Stage 10–12 — Combat Architecture
- Stage 9 — Validation Philosophy

Stage 18 must not redefine or bypass any of the above.

---

## 4. Stage Breakdown

Stage 18 is split into:

### 18.1 — NPC Decision Model
Defines:
- What a decision is
- Inputs and outputs
- Authority and ordering rules

### 18.2 — Behavior Evaluation & Selection
Defines:
- How possible actions are evaluated
- Deterministic selection rules

### 18.3 — Action Intent Emission
Defines:
- How decisions become action intents
- Integration with combat, quests, and world systems

Each sub-stage is independently lockable.

---

## 5. Explicit Non-Goals

Stage 18 does not define:
- AI algorithms
- Behavior trees
- Machine learning
- Navigation
- Dialogue
- Scripting languages
- Client-side NPC logic

Any of the above appearing in Stage 18 is a canon violation.

---

## 6. Lock Criteria

Stage 18.0 is LOCKED when:
- Decision-making is fully separated from content
- Behavioral authority is explicit
- Sub-stage boundaries are clear

Stage 18.0 exists solely to frame Stages 18.1–18.3.
