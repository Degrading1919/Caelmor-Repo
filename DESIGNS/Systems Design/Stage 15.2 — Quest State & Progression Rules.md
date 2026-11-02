# Stage 15.2 — Quest State & Progression Rules

## 1. Purpose

This document defines the authoritative **quest state model** and the **rules governing quest progression** at runtime.
It specifies the complete set of legal quest states, the allowed transitions between those states, and the structural model by which quest progress is evaluated.
This document introduces no content, narrative, triggers, rewards, or UI behavior.

**Revision (2026-11-02):** the state model is reduced to the Creative Director's approved three-state lifecycle, **Inactive, Active, Completed**. The earlier `Uninitialized` state is renamed `Inactive` to match Stage 27 and the runtime; the `Failed` and `Abandoned` states are removed.

## 2. Quest State Definitions

Each quest instance **must** exist in **exactly one** of the following states at any time.
No other states are permitted.

**Defined States**

1. **Inactive**
   - The quest instance exists but has not yet been started by the player.
   - This is the initial state for all newly created quest instances.

2. **Active**
   - The quest has been started and is eligible for progress evaluation.

3. **Completed**
   - The quest has reached its completion condition.
   - This is the only terminal state.

**State Rules**
- A quest instance **must** be in exactly one state at all times.
- Illegal or undefined states **are forbidden**.
- Terminal states **must not** transition to any other state.
- There is **no** failed or abandoned state. Quests never permanently fail and are never abandoned (Creative Director ruling, 2026-11-02). Player choices, losses and missed moments are recorded as outcome flags on the quest instance or character, never as a quest state.
- A quest the player walks away from **must** remain `Active` with its persisted progress intact, and **must** stay resumable. Content may provide a resume hook (for example, the original offer point re-prompting the player); a resume hook never creates a new quest instance.

## 3. Legal State Transitions

**Permitted Transitions**

- `Inactive → Active`
- `Active → Completed`

**Forbidden Transitions**

- Any transition **into** `Inactive`
- Any transition **out of** `Completed`
- Direct transitions from `Inactive` to `Completed`
- Any transition not explicitly listed as permitted

**Transition Rules**
- All state transitions **must** be server-authoritative.
- All state transitions **must** be deterministic.
- State transitions **must not** be skipped.
- A quest instance **must not** change state more than once within a single authoritative transition boundary.

## 4. Progress Evaluation Model

**Definition**

Progress evaluation is the server-authoritative assessment of whether a quest instance satisfies the conditions required to advance or terminate its state.

**Rules**
- Progress evaluation **must** operate only on the current quest state.
- Progress evaluation **must not** occur if the quest state is `Inactive`.
- Progress evaluation **must not** occur for any terminal state.
- Progress evaluation **must** be structurally defined and content-agnostic.
- Progress evaluation **must not** embed:
  - narrative logic,
  - dialogue logic,
  - reward logic,
  - presentation logic.

**Outcome Constraints**
- Progress evaluation **must result in exactly one** of the following outcomes:
  1. No state change occurs, and the quest remains in its current state.
  2. A single legal state transition occurs.
- No other outcomes are permitted.
- Partial progress application **is forbidden**.

## 5. Tick vs Event Evaluation (Structural Only)

**Evaluation Invocation Model**

Quest progress evaluation **must** be invoked through **exactly one** of the following server-authoritative mechanisms:

1. **Tick-Based Evaluation**
   - Evaluation is invoked as part of authoritative tick processing.

2. **Event-Based Evaluation**
   - Evaluation is invoked in response to a server-recognized authoritative event.

3. **Combined Invocation**
   - Both tick-based and event-based evaluation are used together under server authority.

**Structural Constraints**
- No other invocation mechanisms are allowed.
- All evaluation invocation **must** be server-initiated.
- Evaluation **must not** occur outside the scope of an active Player Session with valid tick participation.
- The choice of invocation mechanism **must not** alter:
  - legal state transitions,
  - ordering guarantees,
  - or determinism of progression.

No engine timing, scheduling, or dispatch details are defined in this document.

## 6. Authority & Ordering Invariants

The following invariants are mandatory and enforceable by validation:

1. **Server Authority**
   - Quest state creation, evaluation, and transition **must** be performed by the server.
   - Clients **must never** mutate or advance quest state.

2. **State Exclusivity**
   - A quest instance **must** occupy exactly one defined state at all times.

3. **Transition Validity**
   - Only explicitly permitted transitions **must** be allowed.
   - All forbidden transitions **must** be rejected deterministically.

4. **Lifecycle Isolation**
   - Quest state transitions **must not** control or redefine:
     - player identity,
     - player session lifecycle,
     - world attachment,
     - tick participation.

5. **Persistence Safety**
   - Quest state **must** follow Stage 13 save and restore boundaries.
   - Restore **must not** replay state transitions.

## 7. Failure & Edge Case Handling

The following cases **must** be handled deterministically:

**Invalid State Transition Attempt**
- The transition **must** be rejected.
- Quest state **must** remain unchanged.

**Progress Evaluation Without Valid Prerequisites**
- Evaluation **must not** occur.
- Quest state **must** remain unchanged.

**Session Deactivation During Progression**
- Any in-progress evaluation **must** be discarded.
- No partial state transition **must** apply.

**Server Crash During State Transition**
- The transition **must** be treated as non-existent unless fully persisted.
- Restore **must** reflect the last valid persisted quest state only.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Quest triggers, conditions, or events
- Quest objectives, steps, or task structures
- Rewards, penalties, or completion effects
- NPCs, dialogue, or narrative content
- Client-side quest tracking or UI
- Scripting systems or implementation details
- Any form of client authority over quest progression
