# Stage 15.2 — Quest State & Progression Rules

**Creative Director ruling — 2026-11-02:** This contract has exactly three quest lifecycle states: **Inactive, Active, Completed**. It supersedes the earlier five-state model. Failed and Abandoned are not lifecycle states, and quests cannot be permanently failed or voluntarily abandoned.

## 1. Purpose

This document defines the authoritative **quest state model** and the **rules governing quest progression** at runtime.
It specifies the complete set of legal quest states, the allowed transitions between those states, and the structural model by which quest progress is evaluated.
This document introduces no content, narrative, triggers, rewards, or UI behavior.

## 2. Quest State Definitions

Each quest instance **must** exist in **exactly one** of the following states at any time.
No other states are permitted.

**Defined States**

1. **Inactive**
   - The quest instance exists but has not yet been accepted by the player.
   - This is the initial state for all newly created quest instances.

2. **Active**
   - The quest has been accepted and is eligible for progress evaluation.

3. **Completed**
   - The quest has reached a successful terminal condition.
   - This is a terminal state.

**State Rules**
- A quest instance **must** be in exactly one state at all times.
- Illegal or undefined states **are forbidden**.
- Completed is the only terminal state and **must not** transition to any other state.
- Leaving an area, death, disconnect, encounter retry, or an interrupted action **must not** close or reset an Active quest.
- Required objectives **must** retain a valid completion path. Recovery may reset transient encounter/action state, but must preserve committed quest progress, choices, consequences and required evidence.

## 3. Legal State Transitions

**Permitted Transitions**

- `Inactive → Active`
- `Active → Completed`

**Forbidden Transitions**

- Any transition **into** `Inactive`
- Any transition **out of** `Completed`
- Direct transitions from `Inactive` to `Completed`
- Quest failure, voluntary abandonment, or replacement of an Active instance to restart its progress
- Any transition not explicitly listed as permitted

**Transition Rules**
- All state transitions **must** be server-authoritative.
- All state transitions **must** be deterministic.
- State transitions **must not** be skipped.
- A quest instance **must not** change state more than once within a single authoritative transition boundary.

## 4. Progress Evaluation Model

**Definition**

Progress evaluation is the server-authoritative assessment of whether an Active quest instance satisfies its completion conditions.

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
- Unknown evaluator decisions are rejected without changing the Active state or any committed progress.

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

**Recovery and Retry**
- An encounter defeat is an encounter result, not a quest lifecycle state.
- Death, leaving, disconnect and retry preserve the Active instance and its committed objectives, counters, evidence, choice records and consequences.
- Interrupted carries/channels may return to their authored recovery points; they must remain reacquirable when required. No recovery path may duplicate a completed reward or erase an established choice.
- Validation must demonstrate that every required objective remains completable after each supported interruption.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Quest triggers, conditions, or events
- Quest objectives, steps, or task structures
- Rewards, penalties, or completion effects
- NPCs, dialogue, or narrative content
- Client-side quest tracking or UI
- Scripting systems or implementation details
- Any form of client authority over quest progression
