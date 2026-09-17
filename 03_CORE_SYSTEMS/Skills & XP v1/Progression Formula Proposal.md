# Progression Formula Proposal

**Status:** DRAFT FOR CREATIVE DIRECTOR REVIEW  
**Authority:** Gameplay design proposal only. This document is not canonical until reviewed and approved.  
**Scope:** Level-threshold mathematics, fixed activity XP, emergent XP/hour, and progression-calibration rules.  
**Out of scope:** Exact final XP table, exact action XP values, action timings, RNG, resource yields, schemas, JSON, C#, and runtime implementation.

---

## 1. Core correction

Caelmor should **not** derive an activity's XP reward from the player's current level or from a level-based target XP/hour.

An activity has an intrinsic XP reward.

If mining iron awards a defined amount of XP, mining that same iron under the same conditions awards the same XP at level 20, level 60, and level 99.

```text
XP(activity, player level) = XP(activity)
```

Player level is not an input to the activity XP award.

This keeps the world mechanically stable, makes methods understandable, preserves the value of player knowledge, and prevents hidden level scaling from changing the meaning of established resources.

---

## 2. Separation of progression layers

The progression system should be modeled as four separate layers.

### Layer A — Cumulative level thresholds

A universal skill-level curve determines how much accumulated XP is required to reach each level.

```text
RequiredXP(level) = F(level)
```

The threshold curve determines how much total experience separates level milestones.

It does **not** determine what individual actions award.

### Layer B — Fixed activity XP

Each XP-bearing action has a fixed base XP award authored from the action itself.

```text
ActivityXP(action) = constant authored value
```

Examples of distinct actions may include:

- mining a specific ore
- cutting a specific tree
- preparing a specific recipe
- completing a specific craft
- successfully processing a specific material

A different or more advanced action may legitimately award more XP because the action itself is different.

The same action must not become worth more XP merely because the player gained levels.

### Layer C — Method throughput

XP/hour emerges from the actual method the player uses.

For a single repeated action:

```text
XP/hour = ActivityXP × SuccessfulActionsPerHour
```

If success chance applies:

```text
XP/hour = ActivityXP × AttemptsPerHour × SuccessChance
```

For a multi-action training method:

```text
MethodXP/hour = Σ(ActionXP_i × SuccessfulActionsPerHour_i)
```

The resulting rate can improve because the player has access to better tools, routes, resources, recipes, stations, preparation, or knowledge.

The activity XP itself remains stable.

### Layer D — Time to level

Time is a result of the threshold curve and the actual method rate.

```text
Time(level → level+1)
    = XPToNextLevel / MethodXPPerHour
```

Therefore:

```text
Level thresholds
        +
Fixed activity XP
        +
Real gameplay throughput
        =
Emergent time-to-level
```

Hours are an analytical output used to validate the system, not the primary input used to manufacture the progression curve.

---

## 3. Tool and efficiency progression

Improved equipment should generally improve the player's **ability to perform actions**, not inflate the XP value of unchanged actions.

Example:

```text
Iron XP = constant

Basic pick:
6.0 seconds per successful iron action

Improved pick:
5.4 seconds per successful iron action
```

The improved pick can therefore increase iron XP/hour by increasing completed actions per hour.

It should not automatically change:

```text
Iron XP = 35 → 42
```

simply because the player or tool is higher level.

The same principle applies to route knowledge, node density, station access, processing chains, preparation, and other legitimate efficiency gains.

---

## 4. Higher-level methods

Higher-level progression can produce higher XP/hour without level scaling.

This occurs when the player gains access to genuinely different activities or methods.

For example:

```text
Resource A XP = fixed value
Resource B XP = fixed value
Resource C XP = fixed value
```

Resource C may be worth substantially more XP than Resource A because it is a different action with different requirements, risks, availability, inputs, or economic value.

A player can also choose to continue using Resource A indefinitely. Its XP reward remains unchanged.

This preserves early-content relevance and supports self-directed training rather than forcing every player onto a mathematically prescribed replacement ladder.

---

## 5. Level-threshold curve

The universal 1–99 cumulative XP curve remains a separate design problem.

A RuneScape-influenced exponential family remains a useful candidate because it produces increasingly meaningful levels while supporting a long-term mastery horizon.

A generalized candidate form is:

```text
Weight(L) = L + A × 2^(L / K)

RawXP(L) = Σ Weight(i), for i = 1 to L-1

RequiredXP(L)
    = round(
        XP99 × RawXP(L) / RawXP(99)
      )
```

Where:

- `L` is the target level.
- `A` controls the strength of the exponential component.
- `K` controls how sharply progression back-loads.
- `XP99` controls numeric scale and reward granularity.

The exact values are **not approved by this draft**.

The purpose of using this family is structural, not to copy OSRS or RS3 numbers.

Caelmor's curve must be independently tuned so that practical mastery around level 80 and completion at 99 both remain meaningful.

---

## 6. Why the threshold curve and action XP must remain independent

If action XP is automatically derived from level or from a desired XP/hour target, the system creates several undesirable effects:

1. The same world action changes value depending on who performs it.
2. Resource knowledge becomes less durable because XP values effectively move with the player.
3. Designers can hide poor progression pacing by inflating rewards instead of fixing the level curve.
4. Economy and content progression become entangled with an artificial level multiplier.
5. Early resources lose a stable mathematical identity.
6. Players cannot reliably reason about or compare methods.

Fixed activity XP avoids these problems.

The level curve determines **how much progression is required**.

The world determines **how progression is earned**.

---

## 7. Calibration workflow

The progression model should be tuned in this order:

### Step 1 — Select a candidate 1–99 threshold curve

Define:

- total XP scale
- curve parameters
- cumulative XP at key levels
- XP-to-next-level progression

### Step 2 — Author representative fixed XP values

Create representative XP awards for a small set of real actions across early, middle, advanced, and masterful play.

Do not attempt to populate every future action before validating the model.

### Step 3 — Model representative training methods

For each representative method, calculate:

- action duration
- success probability where applicable
- travel/setup burden where analytically modeled
- actions per hour
- fixed XP per action
- resulting XP/hour

### Step 4 — Derive time-to-milestone

Calculate actual progression time to:

- level 30
- level 50
- level 70
- practical mastery around level 80
- level 99

### Step 5 — Compare against Caelmor's progression goals

Evaluate whether the derived journey supports:

- slow but rewarding progression
- meaningful early momentum
- long-term attachment
- practical mastery before cap
- a meaningful optional 80–99 dedication tail
- knowledge-driven efficiency
- no mandatory chore-like grind

### Step 6 — Tune the correct variable

If progression is wrong:

- change the threshold curve if the entire level journey is mis-shaped;
- change a particular action's XP if that action is incorrectly valued relative to comparable actions;
- change action timing or method structure if throughput is wrong;
- change content access if method progression is wrong.

Do **not** automatically scale all XP rewards by player level to force a desired hours-to-level result.

---

## 8. Treatment of the current 145-hour target

The previously recorded approximately 145-hour level-99 figure should be treated as a **provisional calibration hypothesis**, not as a foundational progression constant.

It may be useful as a comparison target while testing candidate formulas.

It should not force the formula to produce predetermined milestone hours.

If a coherent threshold curve plus sensible fixed activity XP and believable method throughput produces a materially different completion time while better satisfying Caelmor's design principles, the hours target should change.

The formula and gameplay must justify the hours, not the reverse.

---

## 9. Relationship to the current calculator

The existing analytical calculator currently supports:

- a power threshold curve;
- an OSRS-shaped threshold curve;
- target XP/hour values by level band;
- derived XP per action from target XP/hour and action throughput.

That final dependency is not appropriate for the proposed Caelmor model as a canonical content rule.

Under this proposal, the future analytical model should instead accept or read **fixed authored activity XP**, calculate method XP/hour from real throughput, and use the threshold curve to derive time-to-level.

Target XP/hour may still be useful as an analytical comparison or warning metric.

It should not be the authoritative source from which unchanged activities receive their XP rewards.

---

## 10. Proposed governing rules

If approved, the progression system should adopt these rules:

1. **The same action awards the same base XP regardless of player level.**
2. **Player level is not an input to base action XP.**
3. **Different actions may have different fixed XP rewards.**
4. **Better methods increase XP/hour through actual gameplay efficiency or access to different actions.**
5. **The cumulative level curve is independent from activity rewards.**
6. **Time-to-level is derived from thresholds and real method throughput.**
7. **Hours are validation outputs, not the primary balancing formula.**
8. **Target XP/hour is an analytical metric, not an automatic XP-award generator.**
9. **Early actions retain stable mathematical identities even when later methods become more efficient.**
10. **Any future XP modifier must have an explicit gameplay source and must not be an invisible player-level multiplier.**

---

## 11. Review outcome requested

Creative Director review should determine whether this fixed-action-XP architecture becomes the governing progression model.

If approved, follow-up work should:

- correct existing progression documentation that currently implies a level-derived XP/hour target should determine activity XP;
- mark current milestone-hour targets as provisional validation targets;
- derive and compare candidate 1–99 threshold formulas;
- build representative fixed-XP activity samples;
- update the analytical calculator only after the design model is approved;
- leave schemas, JSON content, and runtime C# unchanged until the appropriate downstream handoff.
