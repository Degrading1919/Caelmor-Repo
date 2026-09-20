# Caelmor — Noncombat Method Calibration Audit

**Status:** Proposal-stage second-pass audit for Hunting and Woodcutting representative methods
**Scope:** Fixed action XP, complete-loop rates, progression timing, method choice, output pressure, and readiness for Creative Director review

## 1. Audit authority

The audit uses the authoritative 1–99 threshold table without modification:

| Segment | XP earned in segment | Nominal segment hours | Implied average XP/h |
|---|---:|---:|---:|
| 1–30 | 221,617 | 11 | 20,147 |
| 31–50 | 431,241 | 20 | 21,562 |
| 51–70 | 896,769 | 32 | 28,024 |
| 71–80 | 775,187 | 27 | 28,711 |
| 81–99 | 2,675,186 | 55 | 48,640 |

The steep post-80 requirement explains why a late route must improve action density and reduce empty travel. It does not authorize a hidden player-level multiplier. Both proposed late circuits sum the fixed XP of constituent authored actions and add no completion bonus.

## 2. Portfolio summary

| Skill | Representative methods | Provisional fixed XP/action range | Baseline XP/h range | Knowledge-efficient XP/h range |
|---|---:|---:|---:|---:|
| Hunting | 8 | 100–850 | 16,800–45,000 | 18,667–48,000 |
| Woodcutting | 8 | 80–700 | 18,000–45,000 | 20,000–48,000 |

The portfolios use the existing four fauna functions, four woodland source relationships, six archetypes per skill, seven opportunity patterns per skill, one ordinary-wood state, raw hide, tanning bark, edible relationships, and ordinary processor flows. No resource or skill was added.

## 3. Calculation verification

For every method:

```text
base loop XP = sum of fixed authored-action XP
effective XP/hour = base loop XP × 3,600 / analytical complete-loop seconds
```

Circuits follow:

```text
HM8 XP = HM3 + HM4 + HM5 = 900 + 1,500 + 1,450 = 3,850
WM4 XP = 3 × WM2 = 3 × 900 = 2,700
WM8 XP = WM1 + WM2 + WM3 = 600 + 900 + 1,100 = 2,600
```

No method uses player level in its XP calculation. “Knowledgeable” execution changes complete-loop time through fewer false starts, better ordering, prepared destinations, and shorter valid routes. It does not change the base XP of any constituent action.

### Action-XP plausibility checks

| Check | Finding |
|---|---|
| Were loop totals generated from the target XP/hour alone? | No. Each loop first identifies its authored read, preparation, selection, resolution, recovery, or custody actions; the rate is then derived from the summed fixed XP and complete-loop cadence. |
| Do reused actions change value in a circuit? | No. HM8, WM4, and WM8 are exact sums of constituent method actions. |
| Does later level itself increase action XP? | No. Later methods contain denser or more demanding authored work; repeating an earlier method retains its earlier XP. |
| Are output-heavy methods automatically the XP leaders? | No. HM5, WM3, and WM6 deliberately spend time on recovery, processing, custody, or delivery and remain economically useful below the XP leaders. |
| Are action values continuous enough for tuning? | Yes. Represented values span 80–850 XP without a capstone multiplier or a special level-99 action. |

The milestone targets are acceptance tests on the resulting portfolios. They are not per-action reward formulas.

## 4. Modeled milestone results

### Hunting

| Milestone | Calibration reference | Sustainable knowledgeable path | Closed nominal/envelope |
|---:|---:|---:|---:|
| 30 | 11.79 h | 10.61 h | ~11 h / 10–12 h |
| 50 | 31.09 h | 28.18 h | ~31 h / 28–34 h |
| 70 | 63.48 h | 58.61 h | ~63 h / 58–68 h |
| 80 | 87.94 h | 85.74 h | ~90 h / 85–92 h |
| 99 | 147.39 h | 147.06 h | ~145 h / 135–150 h |

### Woodcutting

| Milestone | Calibration reference | Sustainable knowledgeable path | Closed nominal/envelope |
|---:|---:|---:|---:|
| 30 | 11.29 h | 10.18 h | ~11 h / 10–12 h |
| 50 | 31.92 h | 28.81 h | ~31 h / 28–34 h |
| 70 | 64.21 h | 58.62 h | ~63 h / 58–68 h |
| 80 | 88.32 h | 85.58 h | ~90 h / 85–92 h |
| 99 | 147.77 h | 146.45 h | ~145 h / 135–150 h |

Both calibration reference paths and both sustainable knowledgeable paths land inside every closed envelope. The knowledgeable paths model believable method availability rather than assuming that conditional hazards, commissions, repair demands, damage states, or complete mixed routes can be repeated continuously for an entire progression segment.

| Skill / segment | Sustainable knowledgeable method mix | Effective segment XP/h | Why the mix is structurally credible |
|---|---|---:|---|
| Hunting 51–70 | 82% HM4; 18% HM5 | 29,476 | Movement windows support XP focus, while the durable grazer route remains part of real output-led practice |
| Hunting 71–80 | 25% HM6; 65% HM5; 10% HM7 | 28,570 | Hazard recoveries and inquiries are conditional; grazer supply is the durable high-skill routine |
| Hunting 81–99 | 80% HM8; 10% HM6; 5% HM5; 5% HM7 | 43,629 | Mixed circuits lead when valid but do not erase focused supply, danger, or inquiry work |
| Woodcutting 51–70 | 82% WM4; 18% WM5 | 30,083 | Renewal circuits are durable; damage recovery remains authored and conditional |
| Woodcutting 71–80 | 20% WM7; 30% WM4; 30% WM6; 20% WM3 | 28,755 | Constraint and reserve work require real conditions; renewal and bank work remain dependable |
| Woodcutting 81–99 | 80% WM8; 10% WM7; 5% WM4; 5% WM6 | 43,952 | Mixed circuits lead without becoming the only valid source or purpose |

These shares are calibration assumptions, not exact unlocks, quotas, random closures, or scheduled downtime. Playtesting must confirm sustainable opportunity availability.

## 5. Required strategy coverage

| Player strategy | Hunting support | Woodcutting support | Result |
|---|---|---|---|
| Pure XP | HM3/HM4/HM6/HM8 | WM2/WM4/WM7/WM8 | **STRONG** |
| Profit/output | HM2/HM5 | WM2/WM3/WM6 | **STRONG** |
| Self-supply | HM2/HM5 and selected HM8 leg | WM2/WM4 | **STRONG** |
| Low attention / familiar route | HM1 and learned HM3 | WM1 and learned WM2 | **STRONG** |
| Knowledge-efficient | HM4/HM6/HM8 | WM3/WM7/WM8 | **STRONG** |
| Post-Practical-Mastery | HM8 plus optional HM7/HM5 | WM8 plus optional WM6/WM7 | **STRONG** |

### Economically useful methods that are not XP leaders

- **HM5 Traveling-grazer supply route:** focused edible/raw-hide/renderer value and Leatherworking self-supply at 23,200–26,100 XP/h, below HM4/HM6/HM8.
- **WM3 Bank-protection intervention:** bark, ordinary wood, repair, and civic value at 18,857–20,842 XP/h, below WM2/WM4/WM7/WM8.
- **WM6 Public-repair reserve selection:** contextual repair demand and trusted work at 27,692–30,638 XP/h, below the late XP leaders.

### Convenient methods that remain useful

- **HM1 Familiar margin forage:** low-risk food and market routine near ordinary destinations.
- **HM3 Reed-margin flock circuit:** familiar food route and constituent of HM8.
- **WM1 Household maintenance round:** dependable nearby ordinary wood with low route burden.
- **WM2 Renewal-stand harvest:** balanced wood/bark supply and constituent of WM4/WM8.

## 6. Universal-dominance audit

### Hunting

| Candidate dominance | Failure found | Correction / constraint | Result |
|---|---|---|---|
| HM5 could lead both XP and valuable outputs | Initial mixed-output role risked replacing HM4 | HM5 is set below HM4 in XP/h and carries higher processing burden; it owns focused hide/self-supply value | Corrected |
| HM6 could replace safer methods | High fixed XP reflects hazard diagnosis and recovery | Declined/failed attempts, risk, attention, and ordinary outputs prevent reliable profit/supply dominance | Controlled pending playtest |
| HM7 could become commission farming | High loop XP could reward stationary repetition | Authored evidence, occasional access, variable material outcome, and no daily board keep it non-bulk | Controlled pending content cadence |
| HM8 could dominate XP and hide supply | Three-source circuit produces high broad throughput | The representative composition uses only one hide-focused leg; HM5 remains the focused hide route. HM8 needs several valid opportunities and verified route geography | Corrected architecturally |

### Woodcutting

| Candidate dominance | Failure found | Correction / constraint | Result |
|---|---|---|---|
| WM2 could dominate XP, bark, and convenience | Renewal work has broad outputs and learnable route | WM4/WM7/WM8 lead XP; WM3/WM6 own civic/repair purpose; WM1 is more convenient | Corrected |
| WM4 could obsolete WM2 | Circuit is faster and uses the same source | WM4 has greater route/attention burden and output pressure; WM2 remains simpler for focused bark/self-supply | Controlled pending map |
| WM7 could replace every Masterful method | Strong XP and meaningful judgment | Constraint/access variability and lower bulk reliability preserve WM6 repair and WM2/WM4 supply roles | Controlled pending playtest |
| WM8 could dominate XP and ordinary-wood profit | It leads XP and modeled wood events/hour | High attention, multi-source validity, route dependence, mixed small/ordinary work, bark focus elsewhere, and later-tuned baseline market value prevent guaranteed universal profit. This remains the largest economic risk | Partial but auditable |

No universal dominant method survives as an approved conclusion. WM8 Woodcutting remains a clear tuning risk; if playtesting shows its broad wood throughput also leads profit under realistic market values, its realized output quantity, sustainable source density, or circuit cadence must change before lock. New wood tiers or junk sinks are not acceptable fixes.

## 7. Material throughput pressure

| Pressure | Modeled evidence | Required later test |
|---|---|---|
| Hunting edible oversupply | HM8 models ~35 edible recovery events/h | Final edible item quantities, Cooking/household sinks, storage, and baseline market value |
| Hunting hide oversupply | HM2/HM5 model 16–18 hide-qualified recoveries/h; HM8's single hide leg ~11.7/h baseline | Final fauna eligibility, hide yield, Leatherworking consumption, ordinary tannery demand |
| Ordinary-wood oversupply | WM8 models ~51.9 wood output events/h baseline; WM4 ~30.9 | Item quantity per event, repair/fuel demand, ordinary forestry competition, baseline market value |
| Bark oversupply | WM2/WM4 can generate repeated eligible bark events | Final source eligibility and Leatherworking/tannery consumption; bark must remain a co-output |
| Market deletion pressure | Every normal lawful transferable good has a baseline outlet | Baseline value must prevent stranding without making bulk XP routes the best profit route |

Output events are not final item yields. The correct response to excess pressure is to tune legitimate quantities, sustainable opportunity density, processing demand, and values. It is not to add arbitrary byproducts, disposable recipes, or premium deletion buyers.

## 8. Does 145 hours contain changing decisions?

### Hunting

- Novice changes from short sign/approach learning to mixed food/hide preparation.
- Competent adds group alert, wet footing, and repeatable route knowledge.
- Advanced separates movement-window XP from grazer supply and processing choices.
- Masterful adds hazard ownership, valid refusal, and inquiry evidence.
- Practical Mastery combines known opportunities into a route while optional inquiries preserve judgment and civic meaning.

### Woodcutting

- Novice learns authorization, retained growth, and tangible recovery.
- Competent chooses between balanced renewal supply and slower bank-purpose work.
- Advanced adds route circuits and bounded damage diagnosis.
- Masterful separates repair custody from multi-constraint extraction.
- Practical Mastery integrates familiar sources and destinations without changing material identity.

The portfolios change decision structure at each identity without requiring an unlock every level. Repetition remains familiar, while methods are differentiated by purpose, attention, route, risk, output, and downstream use.

## 9. Progression gaps and assumptions requiring playtesting

### No architecture-level gaps

- Every progression identity has at least one viable method.
- Competent and later bands have meaningful alternatives.
- Both skills have output-led, convenience-led, and XP-led choices.
- Post-80 participation does not require a new material or source family.

### Playtest assumptions

1. Complete-loop cadence includes believable reading, travel, recovery, banking, and destination handling.
2. HM8 and WM8 route geometry can exist without implausible adjacency. **MAP VERIFICATION REQUIRED.**
3. Knowledge reduces wasted time by the modeled amount without removing meaningful decisions.
4. Source availability can support reference-path play without a live population or market simulation.
5. Failed, declined, closed, or nonproductive work occurs often enough to matter but does not become arbitrary throttling.
6. Low-attention methods remain readable and safe without becoming unattended automation.
7. Output event quantities and ordinary-supply competition keep gathered goods useful without overwhelming sinks.
8. HM6 combat handoff keeps Hunting eligibility and recovery separate from combat rewards.
9. HM7/WM6 civic content stays optional and occasional rather than becoming mandatory rotating work.
10. Fixed action values feel proportionate in play; the 80–850 XP range must be tested against perceived effort, not only time targets.

## 10. Creative Director decision status

The closed milestone envelopes govern both reference and sustainable knowledgeable progression. CD-M02 is approved; no Creative Director decision remains open for this calibration package.

### CD-M02 — Post-80 mixed-route model

**Ruling: APPROVED**

HM8 and WM8 are valid representative post-80 method structures with no circuit bonus XP. Their advantage comes from constituent-action density, shared returns, route knowledge, and player familiarity. Map verification and playtesting remain production checks, not approval blockers.

Exact unlocks, timings, tools, output quantities, prices, source counts, and market values remain playtest and balance work.

## 11. Second-pass classification

| Category | Classification | Finding |
|---|---|---|
| Hunting method coverage | **STRONG** | Eight methods cover all identities and six player strategies |
| Woodcutting method coverage | **STRONG** | Eight methods cover all identities and six player strategies |
| Fixed action XP rule | **STRONG** | Every modeled rate derives from fixed authored actions and loop assumptions |
| Reference milestone pacing | **STRONG** | Both skills land inside every closed milestone envelope |
| Sustainable knowledgeable pacing | **STRONG** | Both skills remain inside every closed milestone envelope through credible method mixes |
| Non-reskinned progression | **STRONG** | Methods change behavior, evidence, stewardship, routes, recovery, and destinations |
| Economic alternatives | **STRONG** | HM5, WM3, and WM6 are useful without leading XP |
| Early-method relevance | **STRONG** | HM1/HM3 and WM1/WM2 retain convenience, outputs, or circuit roles |
| Hunting throughput | **PARTIAL FOR PLAYTEST** | Edible/hide quantities and sinks remain unset |
| Woodcutting throughput | **PARTIAL FOR PLAYTEST** | WM8 ordinary-wood pressure requires yield and sink testing |
| Universal dominance | **CONTROLLED** | No approved universal winner; WM8 economic dominance remains a named rejection gate |
| Solo-development scope | **STRONG** | Sixteen representative methods reuse existing opportunities and interfaces |
| New catalog dependency | **NONE** | No new resource, skill, fauna function, or woodland relationship is required |

No category is **MISSING** or **CONTRADICTORY**. CD-M02 and the named playtest risks are bounded and do not require redesigning the economy architecture.

## 12. Final readiness

Both skills have coherent long-form portfolios. Reference and sustainable knowledgeable paths satisfy every closed milestone envelope, fixed action XP remains independent of player level, several legitimate strategies survive, and the next pass can place exact unlocks and refine real baseline-versus-efficient cadence through prototypes and map verification.

HUNTING & WOODCUTTING METHOD CALIBRATION: READY FOR CREATIVE DIRECTOR AUDIT
