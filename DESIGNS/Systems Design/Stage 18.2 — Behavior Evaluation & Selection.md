# Stage 18.2 — Behavior Evaluation & Selection

## 1. Purpose

This document defines the **deterministic evaluation and selection process** for NPC decisions.
It specifies how candidate decisions are evaluated, how exactly one decision is selected, and how ordering and tie-breaking are enforced under full server authority.
This document introduces no behavior logic, AI algorithms, or content semantics.

## 2. Candidate Decision Set

The **candidate decision set** is the complete, finite set of decisions eligible for evaluation during a single decision cycle.

**Candidate Set Rules**
- The candidate decision set **must be finite**.
- The candidate decision set **must be derived exclusively by the server**.
- The candidate decision set **must be fully determined before evaluation begins**.
- A decision **must not** be evaluated or selected unless it is a member of the candidate decision set.
- No decision outside the candidate decision set **can** be selected.

The construction of the candidate decision set **does not** imply evaluation or selection.

## 3. Evaluation Pass Definition

The **evaluation pass** is a deterministic examination of all candidate decisions.

**Evaluation Characteristics**
- Evaluation **must** examine every candidate decision in the set.
- Evaluation **must not** execute decisions.
- Evaluation **must not** mutate NPC, world, or player state.
- Evaluation **must** produce comparable evaluation outputs for all candidates.

**Evaluation Constraints**
- The evaluation pass **must** complete fully before selection begins.
- Partial evaluation results **must not** be used for selection.
- Evaluation **must not** be short-circuited or terminated early for any reason.

Evaluation produces *selection-relevant information only*.

## 4. Selection Rules

The **selection phase** chooses exactly one outcome based on completed evaluation results.

**Selection Requirements**
- Selection **must** result in exactly one of the following outcomes:
  - One selected decision, or
  - An explicit no-decision outcome
- Selection **must not** result in multiple selected decisions.
- Selection **must** be deterministic.
- Selection **must** be server-authoritative.
- Selection **must not** be influenced by clients.

A no-decision outcome **is a valid and explicit result**, not an error state.

## 5. Determinism & Tie-Breaking

**Tie-Breaking Rules**
- All ties **must** be resolved deterministically.
- Tie-breaking **must** rely only on stable, server-owned ordering inputs.
- Tie-breaking **must not** rely on randomness, probability, or time-based variation.

**Determinism Guarantees**
- Identical candidate sets and evaluation outputs **must** always result in the same selection outcome.
- Selection results **must** be reproducible across sessions and restores.

## 6. Authority & Ordering Invariants

The following invariants **must always hold**:

- Evaluation and selection **must** be fully server-authoritative.
- Evaluation and selection **must** occur only at server-defined tick boundaries.
- Evaluation and selection **must not** occur mid-tick.
- Clients **must never** influence candidate ordering, evaluation results, or selection.
- Decision selection **must not** bypass save, restore, or validation boundaries.

## 7. Failure & Edge Case Handling

**Empty Candidate Set**
- An empty candidate set **must** result in an explicit no-decision outcome.

**Invalid Candidate Decisions**
- Invalid or illegal candidates **must** be excluded before evaluation.
- If exclusion results in an empty set, a no-decision outcome **must** occur.

**Evaluation Failure**
- If evaluation cannot complete deterministically, no selection **must** occur.
- Partial evaluation results **must not** be applied.

**Session Deactivation**
- If session deactivation occurs during evaluation or selection:
  - Evaluation and selection **must** be discarded.
  - No decision **must** be selected.

**Server Crash**
- If a server crash occurs during evaluation or selection:
  - No decision **must** be persisted.
  - Evaluation and selection **must not** be replayed on restore.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- AI algorithms or heuristics
- Utility scoring systems
- Probabilistic or random selection
- Behavior trees, planners, or graphs
- Combat tactics or movement logic
- Quest logic or progression
- Execution of selected decisions
- Implementation details or engine internals
