# Stage 23.4 — Player Lifecycle Integration Runtime Definition

## Purpose
Define the **authoritative runtime contract** for integrating player lifecycle state with sessions, zone residency, persistence, and simulation eligibility.

This stage specifies **what lifecycle states exist**, **who is allowed to transition them**, **the required ordering guarantees**, and **what other systems may assume** at each state boundary.

This document is a **binding contract**. No code is implemented here.

---

## Scope Clarification

### This Stage Owns
- Player lifecycle states and transitions
- Ordering guarantees between lifecycle, sessions, zones, persistence, and simulation
- Activation, suspension, deactivation semantics
- Deterministic failure handling for lifecycle transitions

### This Stage Does NOT Own
- Session creation or teardown
- Zone residency rules (see Stage 23.3)
- Tick execution or simulation loops
- Save file IO or serialization
- Combat, AI, quests, or NPC logic
- Client control signaling

---

## Core Concepts

### Player Lifecycle
The **player lifecycle** represents the authoritative runtime state of a player from creation to teardown.

Lifecycle state answers:
> “What is the player allowed to do right now, and what systems may interact with them?”

Lifecycle is **server-authoritative** and **deterministic**.

---

## Lifecycle States

The following lifecycle states are defined:

1. **Created**
   - Runtime player instance exists
   - No zone residency
   - Not simulated

2. **Activating**
   - Preconditions being satisfied
   - No simulation allowed
   - Transitional, short-lived

3. **Active**
   - Player is resident in a zone
   - Eligible for simulation
   - Session may be attached

4. **Suspended**
   - Player exists but is temporarily non-simulated
   - Zone residency may or may not exist (must be explicit)
   - Used for disconnects, transfers, or controlled pauses

5. **Deactivating**
   - Teardown in progress
   - No simulation allowed
   - Transitional, short-lived

6. **Deactivated**
   - Player runtime instance still exists OR is pending destruction
   - No residency
   - No simulation

---

## State Invariants (Hard Rules)

The following invariants MUST always hold:

1. A player in **Active** state must have valid zone residency.
2. A player in **Active** state must be eligible for simulation.
3. A player not in **Active** state must not be simulated.
4. Lifecycle transitions are **explicit and ordered**.
5. Lifecycle state changes are **server-authoritative only**.
6. Lifecycle transitions are **idempotent**.
7. No lifecycle transition may occur mid-tick.

Violation of any invariant is a fatal runtime error.

---

## Allowed Transitions

The only valid transitions are:

- Created → Activating
- Activating → Active
- Active → Suspended
- Suspended → Active
- Active → Deactivating
- Deactivating → Deactivated

All other transitions are invalid and must be rejected deterministically.

---

## Transition Ordering Guarantees

### Activation Path
1. Player runtime instance exists
2. Session (if any) is valid
3. Persistence restore (if required) completes
4. Zone residency is established
5. Lifecycle enters **Active**
6. Simulation eligibility granted

### Suspension Path
1. Simulation eligibility revoked
2. Lifecycle enters **Suspended**
3. Zone residency handling proceeds per policy

### Deactivation Path
1. Simulation eligibility revoked
2. Zone residency detached
3. Session detached (if applicable)
4. Persistence save permitted
5. Lifecycle enters **Deactivated**

Ordering must be strictly enforced.

---

## Failure Modes

Lifecycle transitions must fail deterministically when:
- Preconditions are unmet
- Forbidden transitions are attempted
- Transition is attempted mid-tick
- Required dependencies are missing

Failures must:
- Leave no partial state
- Be observable by callers
- Not trigger implicit recovery

---

## Interaction Contracts

### With Session Runtime
- Sessions do not control lifecycle state
- Lifecycle may require an active session to activate
- Session loss may trigger suspension

### With Zone Residency
- Active lifecycle requires valid residency
- Deactivation requires residency removal first

### With Simulation / Tick System
- Only Active players may be simulated
- Lifecycle transitions may not occur mid-tick

### With Persistence
- Persistence restore must complete before activation
- Persistence save may only occur after deactivation begins

---

## Explicitly Forbidden Behaviors

The following are explicitly forbidden:

- Client-driven lifecycle transitions
- Implicit activation or deactivation
- Mid-tick lifecycle changes
- Lifecycle logic performing persistence IO
- Lifecycle logic assigning zones or sessions
- Lifecycle logic granting client control

Any implementation exhibiting these behaviors is invalid.

---

## Validation Expectations (Future Stage)

Future validation stages must prove:
- All invalid transitions are rejected
- Ordering guarantees are respected
- No simulation occurs outside Active state
- Transitions are idempotent and deterministic

This document is the sole authority for lifecycle correctness.
