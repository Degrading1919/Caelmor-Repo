# Stage 14.1 — Initial Entry Conditions

## 1. Purpose

This document defines the authoritative conditions under which a player is considered **eligible to enter active play** following session activation.
It establishes a strict gate between lifecycle readiness and actual participation in gameplay systems.
This stage does not grant control, tick participation, placement, or exposure to gameplay logic.

## 2. Entry Eligibility Definition

**Entry Eligibility**

Entry eligibility is a server-defined determination that a player has satisfied all structural prerequisites required to proceed toward active play.

**Rules**
- Entry eligibility **must** be evaluated by the server only.
- Entry eligibility **must not** grant:
  - player control,
  - tick participation,
  - world attachment,
  - zone residency,
  - access to gameplay systems.
- Entry eligibility **must** represent readiness only, not participation.
- Entry eligibility **must** be a binary state: eligible or not eligible.

## 3. First-Time Player Conditions

**Definition**

A **first-time player** is a Player Identity whose persisted truth indicates no prior completion of initial entry.

**Rules**
- First-time status **must** be determined solely from persisted truth in PlayerSave.
- Client declarations, flags, or assumptions **must not** influence first-time determination.
- Absence of required persisted entry markers **must** classify the player as first-time.
- First-time players **must** satisfy all general entry preconditions before eligibility is granted.

## 4. Returning Player Conditions

**Definition**

A **returning player** is a Player Identity whose persisted truth indicates prior completion of initial entry.

**Rules**
- Returning status **must** be determined solely from persisted truth in PlayerSave.
- Client input **must not** influence returning classification.
- Presence of required persisted entry markers **must** classify the player as returning.
- Returning players **must** satisfy all general entry preconditions before eligibility is granted.

## 5. Entry Preconditions

Entry eligibility **must not** be granted unless all of the following are true:

- A valid Player Identity exists.
- A PlayerSave exists and is successfully loaded.
- The Player Session is active.
- The server has determined that world attachment is possible for the session.

**Prohibitions**
- Entry eligibility **must not** be granted if PlayerSave is missing, invalid, or incomplete.
- Entry eligibility **must not** be granted if the Player Session is inactive or deactivated.
- Entry eligibility **must not** imply world attachment has occurred.

## 6. Authority & Ordering Invariants

The following invariants are mandatory and enforceable by validation:

1. **Server Authority**
   - Entry eligibility **must** be evaluated and granted by the server.
   - Clients **must never** influence eligibility evaluation or outcome.

2. **Ordering**
   - Session activation **must** precede eligibility evaluation.
   - Entry eligibility **must** precede any placement, control, or tick participation stages.

3. **Isolation**
   - Eligibility evaluation **must** not mutate PlayerSave.
   - Eligibility evaluation **must** not create runtime gameplay state.

## 7. Failure & Edge Case Handling

The following cases **must** be handled deterministically:

**Missing or Invalid PlayerSave**
- Entry eligibility **must not** be granted.
- The session **must not** proceed toward placement or control.

**Corrupted or Incomplete Persisted Data**
- Entry eligibility **must not** be granted.
- No inference or reconstruction **may** occur.

**Session Deactivation During Evaluation**
- Eligibility evaluation **must** be aborted.
- Entry eligibility **must not** be granted.

**Server Crash During Evaluation**
- Eligibility state **must** be treated as non-existent on restore.
- Eligibility evaluation **must** be re-attempted only through normal lifecycle flow.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Player placement, spawning, or positioning
- Zone residency or world attachment mechanics
- Player control, input handling, or camera logic
- Tick participation or gameplay system exposure
- UI, tutorials, narrative, or onboarding presentation
- Client authority, negotiation, or decision-making
