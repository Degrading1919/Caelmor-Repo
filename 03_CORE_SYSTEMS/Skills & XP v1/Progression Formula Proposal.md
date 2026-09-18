# Progression Formula Proposal

**Status:** CREATIVE DIRECTOR DECISIONS LOCKED; DRAFT PR FOR REPOSITORY REVIEW  
**Authority:** The Creative Director has approved the non-combat fixed-base-XP architecture, the RuneScape-like generalized exponential threshold family, the closed milestone-time envelopes, and a 5,000,000 XP level-99 display scale. Exact curve coefficients, final per-level thresholds, and final activity XP values remain calibration work.  
**Scope:** Non-combat skilling/economy XP architecture, chosen level-threshold family, XP display scale, emergent XP/hour, and progression-calibration rules.  
**Out of scope:** Combat XP, quest XP, encounter XP, other future XP sources, final curve coefficients, exact final per-level XP table, exact action XP values, action timings, RNG, resource yields, schemas, JSON, SQLite, calculator code, C#, and runtime implementation.

---

## 1. Core correction

For authored **non-combat skilling/economy activities**, Caelmor should **not** derive an activity's base XP reward from the player's current level or from a level-band target XP/hour.

The same authored non-combat action under the same conditions should award the same base XP regardless of the player's current skill level.

If mining iron awards a defined amount of base XP, mining that same iron under the same conditions awards that same base XP at level 20, level 60, and level 99.

```text
BaseXP(nonCombatAction, playerLevel) = BaseXP(nonCombatAction)
```

Player level itself is not an input to the action's base XP award.

This keeps authored skilling activities mechanically stable, makes methods understandable, preserves the value of player knowledge, and prevents hidden level scaling from changing the meaning of established resources.

This rule applies to non-combat activities such as:

- gathering
- processing
- crafting
- cooking
- other equivalent authored skilling actions

This draft does **not** define the reward model for Melee, Ranged, combat encounters, quests, or other future XP sources. Combat progression may depend on enemy attributes or other combat-specific variables defined elsewhere.

Explicit XP modifiers may be designed later if they have a separately authored and authorized gameplay source. The prohibited behavior is an invisible multiplier caused solely by player level.

---

## 2. Separation of non-combat progression layers

The non-combat skilling/economy XP model should separate four concerns.

### Layer A — Candidate cumulative level thresholds

A 1–99 threshold architecture determines how much accumulated XP is required to reach each level.

```text
RequiredXP(level) = F(level)
```

This draft proposes using a common 1–99 threshold architecture for the non-combat skills covered by this system unless later approved documentation establishes skill-specific threshold curves.

The threshold curve determines how much total experience separates level milestones.

It does **not** determine what individual non-combat actions award.

A universal level cap does not, by itself, imply a universal reward model across every XP source in the game.

### Layer B — Fixed base XP for authored non-combat activities

Each XP-bearing non-combat action has a fixed base XP award authored from the action itself.

```text
BaseActivityXP(action) = authored constant
```

Examples of distinct actions may include:

- mining a specific ore
- cutting a specific tree
- preparing a specific recipe
- completing a specific craft
- successfully processing a specific material
- cooking a specific food

A different or more advanced action may legitimately award more base XP because the action itself is different.

The same authored action must not become worth more base XP merely because the player gained levels.

### Layer C — Method throughput

XP/hour emerges from the actual method the player uses.

For a single repeated action:

```text
XP/hour = EffectiveActivityXP × SuccessfulActionsPerHour
```

If success chance applies:

```text
XP/hour = EffectiveActivityXP × AttemptsPerHour × SuccessChance
```

For a multi-action training method:

```text
MethodXP/hour = Σ(EffectiveActivityXP_i × SuccessfulActionsPerHour_i)
```

Where:

```text
EffectiveActivityXP
    = BaseActivityXP × ExplicitAuthorizedModifiers
```

Any modifier must come from an explicit gameplay rule or authored source. Player level itself must not silently multiply the reward.

The resulting rate can improve because the player has access to better tools, routes, resources, recipes, stations, preparation, or knowledge.

The base XP identity of the underlying action remains stable.

### Layer D — Derived time to milestone

Time is a result of the threshold curve and the representative method rate.

```text
Time(level → level+1)
    = XPToNextLevel / MethodXPPerHour
```

Therefore:

```text
Candidate level thresholds
        +
Fixed non-combat activity base XP
        +
Believable gameplay throughput
        =
Derived time-to-level
```

Those derived times are then validated against the already-closed Creative Director pacing envelopes.

The approved pacing envelopes are **acceptance constraints**. They are not a formula that directly assigns XP to every action.

---

## 3. Closed progression-time acceptance targets

The current approved analytical progression targets remain authoritative for this design pass.

| Milestone | Closed nominal engaged time | Closed tuning envelope |
|---|---:|---:|
| Level 30 | ~11 h | ~10–12 h |
| Level 50 | ~31 h | ~28–34 h |
| Level 70 | ~63 h | ~58–68 h |
| Practical mastery around level 80 | ~90 h | ~85–92 h |
| Level 99 | ~145 h | ~135–150 h |

These targets define the intended pacing relationship of the 1–99 non-combat skill journey.

They do **not** mean every action should be back-solved directly from a target XP/hour.

The model must naturally reproduce these approved pacing envelopes through a coherent combination of:

- threshold XP
- stable authored non-combat activity rewards
- believable method access
- believable tool progression
- believable routing and preparation
- believable throughput
- knowledge-driven efficiency

If the derived milestone times fall outside the approved envelopes, the design variables must be reconciled without introducing invisible player-level XP scaling.

---

## 4. Tool and efficiency progression

Improved equipment should generally improve the player's **ability to perform actions**, not inflate the base XP value of unchanged actions merely because the tool or player is higher level.

Example:

```text
Iron base XP = constant

Basic pick:
6.0 seconds per successful iron action

Improved pick:
5.4 seconds per successful iron action
```

The improved pick can therefore increase iron XP/hour by increasing completed actions per hour.

It should not automatically change:

```text
Iron base XP = 35 → 42
```

simply because the player or tool is higher level.

The same principle applies to route knowledge, node density, station access, processing chains, preparation, and other legitimate efficiency gains.

If a future tool, perk, buff, event, or other system explicitly grants an XP modifier, that modifier must be separately designed and authorized rather than inferred from player level.

---

## 5. Higher-level methods

Higher-level progression can produce higher XP/hour without hidden level scaling.

This occurs when the player gains access to genuinely different activities or methods.

For example:

```text
Resource A base XP = fixed value
Resource B base XP = fixed value
Resource C base XP = fixed value
```

Resource C may be worth substantially more base XP than Resource A because it is a different action with different requirements, risks, availability, inputs, or economic value.

A player can also choose to continue using Resource A indefinitely. Its base XP reward remains unchanged.

This preserves early-content viability and supports self-directed training rather than forcing every player onto a mathematically prescribed replacement ladder.

Early methods do not need to remain optimal forever. They should remain mechanically honest and mathematically stable.

---

## 6. Chosen level-threshold family and XP scale

The 1–99 cumulative XP threshold curve remains mathematically separate from activity rewards.

The Creative Director has selected a **RuneScape-like generalized exponential family** for Caelmor. This is a structural choice, not a decision to copy OSRS or RS3 XP totals.

The chosen family is:

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

### Closed XP display scale

The Creative Director has selected:

```text
XP99 = 5,000,000
```

This is the absolute display scale for the working 1–99 progression model. It does **not** change the normalized curve shape or the closed time-to-milestone targets.

The 5,000,000 scale was selected because it provides enough integer granularity for stable authored non-combat activity rewards without pushing ordinary actions into unnecessarily inflated numbers.

### Curve-coefficient status

The exact generalized-exponential coefficients are **not yet closed**.

Current analytical work indicates that a back-loading parameter around:

```text
K ≈ 17
```

is a strong working calibration anchor because it can reconcile the closed milestone-time envelopes with believable growth in method efficiency under fixed activity XP.

Treat approximately `K = 17` as the current analytical anchor, not as final canon. The coefficient should be finalized only after representative fixed-XP activities and believable training methods are tested.

The coefficient `A` also remains open for calibration. It must not be copied from RuneScape by default.

Any coefficient set must be tested against the closed milestone-time envelopes using representative fixed-XP non-combat activities and believable methods.

The curve does not get to override the approved pacing philosophy.

The pacing targets do not get to directly manufacture every action's XP value.

Both must be reconciled through coherent design.

---

## 7. Why the threshold curve and non-combat action XP must remain independent

If non-combat action XP is automatically derived from player level or directly generated from a desired XP/hour target, several undesirable effects appear:

1. The same authored skilling action changes value depending on who performs it.
2. Resource knowledge becomes less durable because XP values effectively move with the player.
3. Designers can hide poor progression pacing by inflating rewards instead of correcting thresholds, methods, or content structure.
4. Economy and content progression become entangled with an artificial level multiplier.
5. Early resources lose a stable mathematical identity.
6. Players cannot reliably reason about or compare methods.

Fixed base activity XP avoids these problems.

The candidate threshold architecture determines **how much progression is required**.

The authored non-combat activity model determines **how progression is earned**.

The approved milestone envelopes determine whether the combined system is paced correctly.

---

## 8. Calibration workflow

The progression model should be tuned in this order.

### Step 1 — Calibrate the selected generalized-exponential 1–99 curve

The curve family and 5,000,000 XP level-99 scale are already selected.

Calibration must determine:

- the final generalized-exponential coefficients;
- cumulative XP at key levels;
- XP-to-next-level progression.

Use `K ≈ 17` as the current analytical anchor while testing representative methods. Do not promote a coefficient merely because it resembles RuneScape numerically.

### Step 2 — Author representative fixed non-combat activity XP values

Create representative base XP awards for a small set of real non-combat actions across early, middle, advanced, and masterful play.

Do not attempt to populate every future action before validating the model.

### Step 3 — Model believable representative methods and throughput

For each representative method, calculate:

- action duration
- success probability where applicable
- travel/setup burden where analytically modeled
- actions per hour
- fixed base XP per action
- explicit authorized modifiers, if any
- resulting XP/hour

### Step 4 — Derive milestone times

Calculate actual progression time to:

- level 30
- level 50
- level 70
- practical mastery around level 80
- level 99

### Step 5 — Compare derived times against the CLOSED Creative Director milestone envelopes

Validate against:

- level 30: ~10–12 h
- level 50: ~28–34 h
- level 70: ~58–68 h
- level 80: ~85–92 h
- level 99: ~135–150 h

The nominal targets remain approximately 11 / 31 / 63 / 90 / 145 engaged hours.

### Step 6 — Tune the correct variables

If the derived journey falls outside the approved envelopes, tune the appropriate variables while preserving stable activity identity and believable gameplay.

Possible tuning levers include:

- threshold-curve shape or total XP scale
- a particular non-combat action's authored XP if it is incorrectly valued relative to comparable actions
- access timing to methods
- tool efficiency
- method composition
- station or route structure
- success model if separately authorized
- other explicit gameplay factors

Do not automatically scale all XP rewards by player level to force a desired hours-to-level result.

### Step 7 — Reject invalid solutions

Reject any solution that reaches the approved pacing envelopes only by:

- hidden player-level XP scaling
- implausible action throughput
- implausible resource availability
- arbitrary reward inflation disconnected from activity identity
- direct mechanical back-solving of every action reward from a target XP/hour

The acceptance target and the activity-reward model must both remain intact.

---

## 9. Treatment of the closed milestone-hour targets

The approximately 145-hour level-99 target and its milestone envelopes are **already-closed analytical progression targets**.

They are not provisional hypotheses in this draft.

They are also not a per-action reward formula.

The correct relationship is:

```text
Threshold curve
        +
Fixed non-combat activity XP
        +
Representative believable methods
        =
Derived milestone times
        ↓
Validate against closed pacing envelopes
```

If the derived times miss those envelopes, tune the appropriate design variables without introducing invisible player-level XP scaling.

The model must naturally reproduce the approved pacing envelopes through coherent thresholds, fixed activity rewards, and believable methods rather than mechanically back-solving every action from a target XP/hour.

---

## 10. Relationship to the current calculator

The existing analytical calculator currently supports:

- a power threshold curve;
- an OSRS-shaped threshold curve;
- target XP/hour values by level band;
- derived XP per action from target XP/hour and action throughput.

That final dependency is not appropriate for the proposed non-combat Caelmor content model as a canonical reward rule.

Under this proposal, a future analytical model should instead accept or read **fixed authored non-combat activity XP**, calculate representative method XP/hour from real throughput, derive time-to-level from candidate thresholds, and validate the resulting milestone times against the closed Creative Director envelopes.

Target XP/hour may still be useful as:

- an analytical comparison
- a diagnostic metric
- a warning threshold
- a way to compare training methods

It should not be the authoritative source from which unchanged non-combat activities receive their base XP rewards.

No calculator code is changed by this draft PR.

---

## 11. Proposed governing rules for non-combat skilling/economy XP

If approved, the non-combat skilling/economy XP architecture should adopt these rules:

1. **The same authored non-combat action under the same conditions awards the same base XP regardless of player level.**
2. **Player level is not an invisible multiplier on non-combat base action XP.**
3. **Different non-combat actions may have different fixed base XP rewards.**
4. **Better methods increase XP/hour through actual gameplay efficiency, explicit modifiers, or access to different actions.**
5. **The candidate cumulative level-threshold architecture is independent from non-combat activity rewards.**
6. **Time-to-level is derived from thresholds and representative real method throughput.**
7. **Derived milestone times must satisfy the already-closed Creative Director pacing envelopes.**
8. **Target XP/hour is an analytical metric, not an automatic non-combat XP-award generator.**
9. **Early actions retain stable mathematical identities even when later methods become more efficient.**
10. **Any XP modifier must have an explicit gameplay source and must not be inferred solely from player level.**
11. **This PR does not define combat XP, quest XP, encounter XP, or every future XP source in the game.**
12. **RuneScape remains an emotional and structural reference, not a numeric blueprint.**

---

## 12. Review outcome requested

The Creative Director has approved the governing direction captured by this document.

This PR should be reviewed for repository consistency and then, if accepted, used as the authority for the next calibration pass.

Follow-up work should:

- correct remaining progression documentation that implies a level-derived XP/hour target should determine non-combat activity XP;
- preserve the closed milestone-time targets as calibration and acceptance constraints;
- retain the selected RuneScape-like generalized exponential family;
- retain the 5,000,000 XP level-99 display scale;
- use `K ≈ 17` as a working analytical anchor while testing coefficients;
- build representative fixed-XP non-combat activity samples;
- model believable representative methods;
- validate derived milestone times against the approved envelopes;
- finalize curve coefficients only after that calibration;
- update the analytical calculator only after the design model is accepted;
- leave combat XP, quest XP, encounter XP, schemas, JSON content, SQLite, and runtime C# unchanged until their appropriate downstream design or implementation handoffs.
