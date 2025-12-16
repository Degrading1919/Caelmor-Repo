# Stage 14.0 — Onboarding & First-Session Flow

---

## 1. Purpose

Stage 14 defines the **authority-safe entry of a player into active play** for the first time and on subsequent returns.

This stage formalizes:
- How a player transitions from “exists” (Stage 13) to “playing”
- How first-time and returning players are distinguished structurally
- How control and tick participation are granted without violating lifecycle, persistence, or determinism

This stage exists to prevent onboarding logic from leaking into:
- content
- quests
- UI
- client-side assumptions

---

## 2. Scope

Stage 14 governs **entry semantics only**.

It applies to:
- First-time players
- Returning players after disconnect or crash
- Re-entry after restore

Stage 14 builds directly on **Stage 13** and introduces **no new lifecycle authority**.

---

## 3. Canon Dependencies

Stage 14 assumes the following are LOCKED and authoritative:
- Stage 13.1 — Player Identity Model
- Stage 13.2 — Player Session Lifecycle
- Stage 13.3 — World Attachment & Zone Residency
- Stage 13.4 — Tick Participation Rules
- Stage 13.5 — Save & Restore Boundaries
- Stage 13.6 — Lifecycle Validation Scenarios

Stage 14 must not contradict or bypass any Stage 13 rule.

---

## 4. Stage Breakdown

Stage 14 is intentionally split into small, lockable sub-stages:

### 14.1 — Initial Entry Conditions
Defines:
- What qualifies a player to enter play
- First-time vs returning player conditions
- Required persisted truth
- Forbidden assumptions

### 14.2 — Initial World & Zone Placement
Defines:
- Structural spawn placement rules
- Authority over placement
- No movement, camera, or narrative logic

### 14.3 — Control Handoff & First Tick Eligibility
Defines:
- When player input is accepted
- When tick participation may begin
- What is forbidden during initial entry

Each sub-stage is independently lockable.

---

## 5. Explicit Non-Goals

Stage 14 does not define:
- Tutorials
- Quests
- Narrative beats
- UI flows or menus
- Difficulty tuning
- Movement, camera, or animation
- Client-driven onboarding
- Account systems or character selection

Any of the above appearing in Stage 14 is a canon violation.

---

## 6. Lock Criteria

Stage 14.0 is LOCKED when:
- Entry concerns are cleanly separated from content and UI
- Sub-stage boundaries are explicit
- No authority or lifecycle rules are redefined

Stage 14.0 exists solely to frame 14.1–14.3.
