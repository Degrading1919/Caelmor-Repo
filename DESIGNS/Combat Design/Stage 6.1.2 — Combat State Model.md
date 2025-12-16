# Stage 10.2 — Combat State Model

**Scope:** Combat State Semantics Only  
**Authority:** Server-authoritative, deterministic (10 Hz)  
**Intent Set:** Locked per Stage 10.1

This document defines the **minimal viable combat state model** for Caelmor.  
It establishes a shared language for combat legality, intent gating, and authoritative resolution.

This document defines:
- What states exist
- Which intents are valid in each state
- Conceptual state transitions

This document does NOT define:
- Timing, costs, damage, or probability
- Animation, physics, or AI behavior
- Balance, tuning, or resolution rules

---

## Combat Intent Reference (Locked)

The following intents are the **complete and final** combat intent set:

- CombatAttackIntent  
- CombatDefendIntent  
- CombatAbilityIntent  
- CombatMovementIntent  
- CombatInteractIntent  
- CombatCancelIntent  

All state compatibility is defined strictly in terms of these intents.

---

## State Overview (Minimal Set)

The following combat states are defined:

1. **CombatIdle**
2. **CombatEngaged**
3. **CombatActing**
4. **CombatDefending**
5. **CombatRestricted**
6. **CombatIncapacitated**

Each state exists only because it meaningfully constrains intent legality or transitions.

---

## 1. CombatIdle

### Purpose
Represents an entity that is not currently participating in combat resolution.

### What This State Represents (System-Level)
- Entity is not engaged in combat logic
- No combat commitments are active
- Entity may transition into combat via intent submission

### What This State Does NOT Imply
- Safety from attack
- Awareness or targeting state
- Animation or stance

### Allowed Combat Intents
- CombatMovementIntent  
- CombatInteractIntent  

### Blocked Combat Intents
- CombatAttackIntent  
- CombatDefendIntent  
- CombatAbilityIntent  
- CombatCancelIntent  

### Notes on Persistence / Restore Semantics
- Default restored state if no combat engagement is active
- Safe baseline for save/load hydration

### Conceptual Transitions
- Transitions to **CombatEngaged** upon valid combat-triggering intent or authoritative engagement

---

## 2. CombatEngaged

### Purpose
Represents an entity that is participating in combat but not currently executing an action.

### What This State Represents (System-Level)
- Entity is within an active, authoritative combat context
- Combat participation is explicit and server-recognized, not inferred from proximity
- Eligible to submit combat intents
- No exclusive action is currently committed

### What This State Does NOT Imply
- Target lock
- Turn ownership
- Initiative or timing priority

### Allowed Combat Intents
- CombatAttackIntent  
- CombatDefendIntent  
- CombatAbilityIntent  
- CombatMovementIntent  
- CombatInteractIntent  

### Blocked Combat Intents
- CombatCancelIntent  

### Notes on Persistence / Restore Semantics
- Restored if entity was combat-active but not mid-action
- No partial action data implied

### Conceptual Transitions
- To **CombatActing** when an attack or ability is committed
- To **CombatDefending** when a defensive commitment is made
- To **CombatIdle** if combat context ends

---

## 3. CombatActing

### Purpose
Represents an entity that has committed to an attack or ability action.

### What This State Represents (System-Level)
- A combat action is committed and pending resolution
- Entity is under authoritative action control
- Input flexibility is restricted

### What This State Does NOT Imply
- Guaranteed success
- Damage, hit, or outcome
- Animation completion

### Allowed Combat Intents
- CombatCancelIntent  

### Blocked Combat Intents
- CombatAttackIntent  
- CombatDefendIntent  
- CombatAbilityIntent  
- CombatMovementIntent  
- CombatInteractIntent  

### Notes on Persistence / Restore Semantics
- On restore, entity must either:
  - Resume authoritative resolution, or
  - Be restored to a safe post-resolution state
- No duplicate execution permitted

### Conceptual Transitions
- To **CombatEngaged** after resolution
- To **CombatRestricted** if action results in constraint
- To **CombatIncapacitated** if action results in incapacitation

---

## 4. CombatDefending

### Purpose
Represents an entity that has committed to a defensive posture or response.

### What This State Represents (System-Level)
- Defensive intent is active
- Entity is awaiting interaction or resolution
- Defensive constraints apply

### What This State Does NOT Imply
- Guaranteed mitigation
- Directional facing
- Duration or timing

### Allowed Combat Intents
- CombatCancelIntent  

### Blocked Combat Intents
- CombatAttackIntent  
- CombatDefendIntent  
- CombatAbilityIntent  
- CombatMovementIntent  
- CombatInteractIntent  

### Notes on Persistence / Restore Semantics
- Defensive commitment must not be duplicated on restore
- Restore resolves or safely clears defensive state

### Conceptual Transitions
- To **CombatEngaged** after defense resolves
- To **CombatRestricted** if defense imposes limitation
- To **CombatIncapacitated** if overwhelmed

---

## 5. CombatRestricted

### Purpose
Represents an entity that is combat-capable but temporarily limited.

### What This State Represents (System-Level)
- Entity remains in combat
- Some actions are disallowed by authoritative rule
- Restrictions are logical, not physical

### What This State Does NOT Imply
- Helplessness
- Crowd-control mechanics
- Specific restriction sources (e.g., stun, snare, disarm)

### Allowed Combat Intents
- CombatDefendIntent  
- CombatMovementIntent  
- CombatCancelIntent  

### Blocked Combat Intents
- CombatAttackIntent  
- CombatAbilityIntent  
- CombatInteractIntent  

### Notes on Persistence / Restore Semantics
- Restrictions must persist across save/load
- Restore must not silently clear restrictions

### Conceptual Transitions
- To **CombatEngaged** when restriction is lifted
- To **CombatIncapacitated** if condition worsens

---

## 6. CombatIncapacitated

### Purpose
Represents an entity unable to meaningfully participate in combat.

### What This State Represents (System-Level)
- Entity cannot submit combat actions
- Combat resolution excludes this entity
- State is authoritative and enforced

### What This State Does NOT Imply
- Death
- Removal from world
- Recovery rules

### Allowed Combat Intents
- CombatCancelIntent  

### Blocked Combat Intents
- CombatAttackIntent  
- CombatDefendIntent  
- CombatAbilityIntent  
- CombatMovementIntent  
- CombatInteractIntent  

### Notes on Persistence / Restore Semantics
- Must persist across save/load
- Restore must not auto-recover entity

### Conceptual Transitions
- To **CombatEngaged** only via authoritative recovery
- To **CombatIdle** if combat context fully ends

---

## Explicit Non-Goals

This state model does NOT:
- Define damage, success, or timing
- Encode balance or progression
- Represent animation or physics
- Define AI or player decision logic
- Replace intent validation or resolution systems

---

## Design Rationale Summary

- Each state exists only to **meaningfully constrain intent legality**
- No state is cosmetic or redundant
- Transitions are conceptual and enforced by authority
- Model is minimal, extensible, and schema-safe

---

## Exit Condition

Stage 10.2 is complete when:
- All combat systems reference these states
- Intent legality is evaluated against this model
- No additional combat states are required for correctness
