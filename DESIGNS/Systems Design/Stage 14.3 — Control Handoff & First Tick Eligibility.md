# Stage 14.3 — Control Handoff & First Tick Eligibility

## 1. Purpose

This document defines the authoritative rules governing **control handoff** and **first tick eligibility** for a Player Session.
It establishes the final, ordered transition from “placed” to “playing” under full server authority.
This stage does not define gameplay behavior and does not modify any rules established in Stage 13.

## 2. Control Handoff Definition

**Control**

Control is the server-granted permission for a Player Session to issue gameplay-relevant input that can be considered by server systems.

**Rules**
- Control **must** be granted by the server.
- Control **must** be revocable by the server at any time.
- Control **must not** imply tick participation.
- Control **must not** imply eligibility for tick participation.
- Control **must** be treated as a distinct state from placement and tick participation.

**Ordering Constraint**
- Control handoff **must** occur only after successful world attachment and zone residency have been completed (Stage 14.2).

## 3. Control Grant Conditions

Control **must not** be granted unless all of the following are true:

- The Player Session is active.
- Entry eligibility has been granted (Stage 14.1).
- World attachment is valid.
- Zone residency is valid.

**Prohibitions**
- Control **must not** be granted to an inactive or deactivated session.
- Control **must not** be granted prior to placement.
- Control **must not** be granted based on client request or acknowledgment.

## 4. First Tick Eligibility Definition

**First Tick Eligibility**

First tick eligibility is the server-determined state indicating that a placed Player Session is permitted to enter tick participation for the first time.

**Rules**
- First tick eligibility **must** be determined by the server.
- First tick eligibility **must** be distinct from control handoff.
- A Player Session **must not** be tick-participating solely because control has been granted.
- First tick eligibility **must** represent readiness only, not participation.

## 5. First Tick Entry Rules

**Entry Rules**
- Tick participation **must not** begin until first tick eligibility has been granted.
- Entry into tick participation **must** occur only on an explicit tick boundary.
- Entry into tick participation **must not** occur mid-tick.
- All first tick entry **must** comply fully with Stage 13.4 Tick Participation Rules.
- Clients **must not** influence first tick eligibility or entry timing.

## 6. Authority & Ordering Invariants

The following invariants are mandatory and enforceable by validation:

1. **Server Authority**
   - Control handoff and first tick eligibility **must** be granted and revoked by the server.
   - Clients **must never** grant, retain, or negotiate control or tick eligibility.

2. **Strict Ordering**
   - Placement **must** precede control handoff.
   - Control handoff **must** precede first tick eligibility.
   - First tick eligibility **must** precede tick participation.

3. **Isolation**
   - Control handoff **must not** mutate PlayerSave.
   - First tick eligibility **must not** create partial tick participation state.

4. **Revocability**
   - Control **must** be revocable independently of tick participation state.

## 7. Failure & Edge Case Handling

The following cases **must** be handled deterministically:

**Session Deactivation Before Control Handoff**
- Control **must not** be granted.
- First tick eligibility **must not** be granted.
- Tick participation **must not** occur.

**Session Deactivation After Control but Before Tick**
- Control **must** be revoked.
- First tick eligibility **must not** be granted.
- Tick participation **must not** occur.

**Server Crash After Control but Before Tick**
- Control state **must** be treated as non-existent on restore.
- First tick eligibility **must** be re-evaluated through normal lifecycle flow.
- Tick participation **must never** resume automatically.

**Server Crash During First Tick Entry**
- Tick participation **must** be treated as non-existent on restore.
- Control state **must** be re-evaluated.
- Entry into tick participation **must** occur only through standard boundary rules.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Input mappings, bindings, or control schemes
- Camera behavior or presentation logic
- Movement, combat, crafting, or interaction systems
- Tutorials, onboarding UI, or narrative flow
- Client authority, negotiation, or confirmation
- Any modification to tick rules defined in Stage 13.4
