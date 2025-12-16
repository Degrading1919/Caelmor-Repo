# Stage 13.6 — Player Lifecycle Validation Scenarios

## 1. Purpose

This document defines the mandatory **validation scenarios** that collectively prove the Player Lifecycle and World Session Authority defined in Stages 13.1–13.5 are deterministic, restore-safe, and server-authoritative.
These scenarios introduce no new rules and exist solely to validate existing guarantees under Stage 9 validation philosophy.

## 2. Validation Scope

Validation applies to:
- Player Identity creation, persistence, and immutability (Stage 13.1)
- Player Session creation, activation, deactivation, and termination (Stage 13.2)
- World attachment and zone residency (Stage 13.3)
- Tick participation entry, exit, and ordering (Stage 13.4)
- Save and restore boundaries, atomicity, and discard rules (Stage 13.5)

All scenarios **must** be deterministically evaluable and fail loudly if violated.

## 3. Baseline Assumptions

- Server authority is absolute.
- Persisted truth consists only of PlayerSave and WorldSave.
- Runtime state is discardable and non-authoritative.
- Validation observes authoritative state only.
- No client input influences lifecycle ordering or outcomes.

## 4. Join & Activation Scenarios

### Scenario: First-Time Player Join
**Exercises:** Stage 13.1 Identity Invariants  
**Given:** No existing Player Identity or PlayerSave  
**When:** Server creates a new Player Identity  
**Then:**  
- Exactly one immutable Player Identity exists  
- Exactly one PlayerSave is created and bound  
**Must Never Observe:**  
- Client-generated identity  
- Multiple saves for one identity

### Scenario: Returning Player Join
**Exercises:** Stage 13.1 Save One-to-One  
**Given:** Existing Player Identity and PlayerSave  
**When:** Server initiates session creation  
**Then:**  
- PlayerSave is loaded before activation  
**Must Never Observe:**  
- New identity creation  
- Missing or replaced PlayerSave

### Scenario: Session Activation With Valid PlayerSave
**Exercises:** Stage 13.2 Activation Ordering  
**Given:** Created session with loaded PlayerSave  
**When:** Server activates session  
**Then:**  
- Session becomes active  
**Must Never Observe:**  
- Activation without PlayerSave

### Scenario: Failed Activation Due to Missing Prerequisites
**Exercises:** Stage 13.2 Preconditions  
**Given:** Session without loaded PlayerSave  
**When:** Activation attempted  
**Then:**  
- Activation fails deterministically  
**Must Never Observe:**  
- Active session without PlayerSave

## 5. Tick Participation Scenarios

### Scenario: Tick Entry at Boundary
**Exercises:** Stage 13.4 Entry Rules  
**Given:** Active, world-attached, zone-resident session  
**When:** Next tick boundary occurs  
**Then:**  
- Session enters tick participation  
**Must Never Observe:**  
- Mid-tick entry

### Scenario: Tick Exit at Boundary
**Exercises:** Stage 13.4 Exit Rules  
**Given:** Tick-participating session  
**When:** Deactivation requested  
**Then:**  
- Exit occurs at next tick boundary  
**Must Never Observe:**  
- Partial tick participation

### Scenario: Activation Mid-Tick
**Exercises:** Stage 13.4 Boundary Safety  
**Given:** Session activation completes mid-tick  
**When:** Tick is in progress  
**Then:**  
- Tick participation begins next tick only  
**Must Never Observe:**  
- Mid-tick participation

### Scenario: Deactivation Mid-Tick
**Exercises:** Stage 13.4 Boundary Safety  
**Given:** Tick-participating session  
**When:** Deactivation requested mid-tick  
**Then:**  
- Participation continues through tick  
- Exit next boundary  
**Must Never Observe:**  
- Early exit

## 6. World & Zone Residency Scenarios

### Scenario: World Attachment After Activation
**Exercises:** Stage 13.3 Ordering  
**Given:** Activated session  
**When:** Server attaches to world  
**Then:**  
- Exactly one world attachment exists  
**Must Never Observe:**  
- Active session without world

### Scenario: Zone Residency Assignment
**Exercises:** Stage 13.3 Single Zone Residency  
**Given:** World-attached session  
**When:** Server assigns zone  
**Then:**  
- Exactly one zone residency exists  
**Must Never Observe:**  
- Zero or multiple zones

### Scenario: Zone Transition Within World
**Exercises:** Stage 13.3 Zone Transitions  
**Given:** Zone-resident session  
**When:** Server transitions zone  
**Then:**  
- Old zone replaced by new zone  
**Must Never Observe:**  
- Overlapping zones

### Scenario: Deactivation While World-Attached
**Exercises:** Stage 13.3 Failure Handling  
**Given:** World-attached, zone-resident session  
**When:** Session deactivates  
**Then:**  
- World attachment cleared  
- Zone residency cleared  
**Must Never Observe:**  
- Residual attachment

## 7. Disconnect Scenarios

### Scenario: Disconnect During Tick Participation
**Exercises:** Stage 13.5 Disconnect Handling  
**Given:** Tick-participating session  
**When:** Disconnect occurs  
**Then:**  
- Tick completes  
- Session deactivates at boundary  
**Must Never Observe:**  
- Partial persistence

### Scenario: Disconnect During Combat Resolution
**Exercises:** Stage 13.5 Save Boundaries  
**Given:** Combat resolving  
**When:** Disconnect occurs  
**Then:**  
- Resolution completes for tick  
- Save only at legal boundary  
**Must Never Observe:**  
- Partial combat state saved

### Scenario: Disconnect During Crafting or Gathering
**Exercises:** Stage 13.5 Save Boundaries  
**Given:** Crafting or gathering resolving  
**When:** Disconnect occurs  
**Then:**  
- Resolution completes for tick  
- Persist only resolved outcome  
**Must Never Observe:**  
- Partial progress saved

### Scenario: Disconnect Before Activation Completes
**Exercises:** Stage 13.2 Failure Handling  
**Given:** Session creation incomplete  
**When:** Disconnect occurs  
**Then:**  
- Session terminated  
**Must Never Observe:**  
- Active session

## 8. Crash & Restore Scenarios

### Scenario: Server Crash Mid-Tick
**Exercises:** Stage 13.5 Crash Handling  
**Given:** Tick executing  
**When:** Server crashes  
**Then:**  
- Runtime state discarded  
- Restore from last persisted truth  
**Must Never Observe:**  
- Tick replay

### Scenario: Server Crash During Save
**Exercises:** Stage 13.5 Atomicity  
**Given:** Save in progress  
**When:** Crash occurs  
**Then:**  
- Either old save or fully written new save exists  
**Must Never Observe:**  
- Partial save

### Scenario: Server Restart With Active Sessions
**Exercises:** Stage 13.2, 13.4 Restore Rules  
**Given:** Active sessions before crash  
**When:** Server restarts  
**Then:**  
- No session resumes  
**Must Never Observe:**  
- Automatic activation or tick participation

### Scenario: Restore From Last Valid Persisted State
**Exercises:** Stage 13.5 Restore Semantics  
**Given:** Persisted PlayerSave and WorldSave  
**When:** Restore occurs  
**Then:**  
- State matches persisted truth exactly  
**Must Never Observe:**  
- Inferred or replayed state

## 9. Save Boundary Scenarios

### Scenario: Save at Legal Boundary
**Exercises:** Stage 13.5 Save Boundaries  
**Given:** Safe boundary  
**When:** Save occurs  
**Then:**  
- Atomic save succeeds  
**Must Never Observe:**  
- Partial save

### Scenario: Attempted Save at Illegal Boundary
**Exercises:** Stage 13.5 Boundary Safety  
**Given:** Mid-tick or mid-resolution  
**When:** Save attempted  
**Then:**  
- Save rejected  
**Must Never Observe:**  
- Mid-tick persistence

### Scenario: Atomic Save Success
**Exercises:** Stage 13.5 Atomicity  
**Given:** Valid save  
**When:** Save completes  
**Then:**  
- Persisted truth updated entirely  
**Must Never Observe:**  
- Mixed versions

### Scenario: Atomic Save Failure
**Exercises:** Stage 13.5 Atomicity  
**Given:** Save interrupted  
**When:** Failure occurs  
**Then:**  
- Previous persisted truth remains  
**Must Never Observe:**  
- Corrupted state

## 10. Invariant Enforcement Matrix

All scenarios enforce:
- Server authority over identity, session, world, zone, and tick state
- One-to-one identity and save mapping
- Single active session per identity
- Explicit tick boundary entry and exit
- No replay, inference, or partial persistence
- Deterministic restore behavior

Any violation **must** fail validation loudly.

## 11. Explicit Non-Goals

This document does not define:
- New lifecycle rules
- Engine internals or execution details
- Retry or compensation logic
- Client behavior or UI flows
- Networking or transport mechanics
