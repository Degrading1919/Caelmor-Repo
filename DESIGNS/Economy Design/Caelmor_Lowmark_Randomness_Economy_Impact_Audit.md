# Caelmor Lowmark Randomness Economy Impact Audit

**Status:** Supporting audit for Creative Director decision

**Scope:** Economic and progression effects of output randomness across Hunting HM1–HM8 and Woodcutting WM1–WM8

## 1. Audit Method

This audit compares three models against the currently approved cadence and throughput:

- **Model A:** deterministic authored outputs;
- **Model B stress case:** deterministic primary output plus a 5% independent chance of one extra unit of the same represented output relationship;
- **Model C stress case:** a 10% independent post-commit failure chance on an otherwise valid completion.

The 5% and 10% values are analytical probes, not proposed balance values. They make the direction and scale of pressure visible without selecting implementation rates.

The audit uses the knowledgeable or efficient rates where supply pressure is greatest. Rounded values may not reproduce from the displayed figures exactly.

## 2. XP-Per-Hour Effects

| Model | XP/hour effect | Calibration consequence |
|---|---:|---|
| **A** | 100% of approved method rates | No change to milestone calibration |
| **B** | 100% if bonuses grant no XP | Progression stays calibrated, but extra goods enter without added time or XP |
| **C, failure withholds the completion award** | 90% in the stress case | Every affected method falls below its approved rate; milestone timing lengthens |
| **C, fixed action XP retained despite output failure** | 100% | Calibration survives, but identical successful execution can lose goods for reasons the player cannot master |

Representative Model C effects if random failure also withholds the completion award:

| Method | Approved efficient XP/h | 10% failure stress case |
|---|---:|---:|
| HM2 | 22,000 | 19,800 |
| HM5 | 26,100 | 23,490 |
| HM8 | 48,000 | 43,200 |
| WM4 | 30,857 | 27,771 |
| WM8 | 48,000 | 43,200 |

Applying the same multiplier to the other methods produces the same structural failure. Model C must either break the closed progression calibration or preserve XP while randomly withholding the economic result. Neither outcome improves the method portfolio.

## 3. Output-Per-Hour Effects

### 3.1 Pressure Summary

| Pressure point | Model A: approved deterministic rate | Model B: 5% bounded bonus stress case | Model C: 10% failure stress case |
|---|---:|---:|---:|
| HM8 edible relationship | 62.3 edible units/h | 64.2 edible units/h | 56.1 edible units/h |
| HM2 raw hide | up to 20.0 hide/h | up to 21.0 hide/h | up to 18.0 hide/h |
| HM5 raw hide | 18.0 hide/h | 18.9 hide/h | 16.2 hide/h |
| HM8 raw hide | 12.5 hide/h | 13.1 hide/h | 11.2 hide/h |
| WM4 ordinary wood | 34.3 wood events/h | 36.0 wood events/h | 30.9 wood events/h |
| WM8 ordinary wood | 55.4 wood events/h | 58.2 wood events/h | 49.8 wood events/h |
| WM4 bark design range | 12–22 bark/h | 12.6–23.1 bark/h | 10.8–19.8 bark/h |
| WM8 bark design range | 18–37 bark/h | 18.9–38.9 bark/h | 16.2–33.3 bark/h |

The Model B HM8 food figure treats each of the three edible recovery relationships in the approved circuit as one chance at one extra edible unit. It therefore adds about 1.9 edible units per hour rather than multiplying all recovered food units by 1.05. Other Model B rows apply the one-extra-unit chance directly to the relevant unit-producing event.

Model C assumes the failed completion produces none of the listed outputs. If failure were rolled separately for every constituent output, variance would increase further and one opportunity could produce incoherent partial results.

### 3.2 Hunting Food Pressure: HM8

Model A preserves the approved efficient continuous estimate of about **62.3 edible units per hour**, with the sustainable post-Practical-Mastery portfolio remaining around the previously modeled **52–55 edible units per hour**.

Model B raises continuous HM8 food to about **64.2 units per hour** in the bounded-bonus stress case. The numerical increase is modest, but it arrives without more time, risk, processing, or demand. Repeated over long mastery play, it increases oversupply pressure in the most productive Hunting portfolio.

Model C reduces the same estimate to about **56.1 units per hour**. This could suppress supply, but it does so by erasing valid completions rather than by creating a choice. The player cannot learn their way out of the loss.

### 3.3 Hunting Hide Pressure: HM2 and HM5

HM2 and HM5 are important because their eligible recoveries produce raw hide with different method identities:

- HM2 rises from up to **20.0** to **21.0 hide per hour** under the Model B stress case, or falls to **18.0** under Model C.
- HM5 rises from **18.0** to **18.9 hide per hour** under Model B, or falls to **16.2** under Model C.

Model B weakens the value of selecting and recovering hide-bearing opportunities by adding supply through luck. Model C makes Leatherworking input less forecastable even when the player follows the approved recovery rules.

HM8 shows the same effect at a lower hide rate: about **12.5**, **13.1**, or **11.2 hide per hour** across Models A, B, and C respectively.

### 3.4 Wood Pressure: WM4 and WM8

WM4 increases from about **34.3** to **36.0 wood events per hour** under Model B and falls to **30.9** under Model C.

WM8 increases from about **55.4** to **58.2 wood events per hour** under Model B and falls to **49.8** under Model C. WM8 already carries the strongest ordinary-wood oversupply risk. Even a rare same-good bonus makes that risk worse without adding a new sink or decision.

Model C reduces supply but also obscures whether public, constrained, or custody-bound work will meet its stated need. A civic request should not fail its material purpose because a hidden roll erased correctly completed work.

### 3.5 Bark Pressure

Bark is already controlled by physical eligibility and woodland stewardship. Model A preserves the design ranges:

- WM4: **12–22 bark per hour**;
- WM8: **18–37 bark per hour**.

Model B pushes those ranges to about **12.6–23.1** and **18.9–38.9**. This is a direct violation of bark's approved identity as guaranteed when physically produced, absent when ineligible, and never a weighted drop.

Model C lowers the ranges to **10.8–19.8** and **16.2–33.3**, but makes an eligible managed action unpredictably fail to recover bark. That encourages repetition against the same eligible work and risks turning the co-output into the bark grind the architecture was designed to avoid.

## 4. Hunting Failure-Semantics Audit

| Event | Material result under Model A | XP treatment | Random? | Fairness condition |
|---|---|---|---|---|
| Invalid opportunity | No recovery output | Only XP for an authored diagnostic action actually completed | No | Invalidity is readable or inferable |
| Player execution failure | Output follows the specific failed approach or recovery | Fixed XP for completed actions only | No | Feedback identifies the failed step |
| Deliberate refusal | No recovery output | Authored assessment/inquiry XP where applicable | No | Correct refusal remains a valid mastery choice |
| World-condition loss | No output when the recovery window or access is visibly lost | No uncompleted-action award | No | Condition is authored and not a hidden throttle |
| Correct valid completion | Guaranteed authored edible relationship and eligible raw hide | Fixed completion XP | No | Same action and conditions give the same result |
| Random failure | Not used | Not applicable | **None** | Knowledge remains causally useful |

## 5. Woodcutting Output-Semantics Audit

| Event | Material result under Model A | XP treatment | Random? | Fairness condition |
|---|---|---|---|---|
| Valid productive harvest | Guaranteed authored ordinary-wood relationship | Fixed authored-action XP | No | Source and accepted work are legible |
| Bark-eligible work | Guaranteed authored bark co-output | Same fixed action XP; no bonus XP | No | Eligibility follows source and action |
| Bark-ineligible work | No bark | Same fixed action XP for the work performed | No | Absence is explained by physical eligibility |
| Damage recovery | Usable supply follows diagnosed damage and accepted scope | Fixed XP for work actually completed | No | Nonproductive cleanup is an authored state |
| Constrained/public work | Output follows authorized productive completion | Fixed authored-action XP | No | Closure, refusal, and custody are readable |
| Random failure | Not used | Not applicable | **None** | Civic and economic purpose remains forecastable |

## 6. Fairness and Trust Comparison

| Criterion | Model A | Model B | Model C |
|---|---|---|---|
| Player can explain the result | Strong | Partial: bonus lacks a causal world explanation | Weak when valid execution fails |
| Knowledge improves realized efficiency | Strong | Strong for primary output; luck adds unmasterable variance | Partial: chance caps mastery |
| Source eligibility remains meaningful | Strong | Partial: bonuses blur authored quantities | Partial: eligible output can disappear |
| Short-session predictability | Strong | Moderate | Weak |
| Long-session economic forecast | Strong | Moderate; bonus supply accumulates | Moderate average, high session variance |
| Trust in public/custody work | Strong | Moderate | Weak |
| Compatibility with fixed authored XP | Strong | Strong only if bonuses grant no XP | Either breaks calibration or decouples XP and output |
| Need for extra UI explanation | Low | Moderate | High |

Model A gives every no-output outcome a cause the player can investigate or improve. This makes failure compatible with mastery without making the economy perfectly effortless.

## 7. Source-to-Sink Consequences

### Model A

- preserves every approved rate and pressure finding;
- keeps hide and bark supply tied to eligibility rather than luck;
- leaves HM8 food and WM8 wood oversupply as visible balance questions for later sink and demand tuning;
- supports dependable repair, workshop, and ordinary-supply planning;
- requires no new item, tier, mechanic, or skill.

### Model B

- creates additional food, hide, wood, or bark without a new sink;
- increases late-method oversupply pressure;
- rewards luck rather than opportunity selection;
- invites future expansion into critical harvests or bonus tables;
- has no demonstrated function that authored opportunity variation does not already serve.

### Model C

- suppresses all affected supplies by the failure rate in expectation;
- destabilizes short-session access to hides and bark;
- either lowers XP/hour or grants XP for inexplicable material loss;
- makes ordinary suppliers comparatively more reliable than player gathering for arbitrary reasons;
- risks using frustration as an economic throttle.

## 8. Largest Economy Impact

The largest absolute pressure is on **late ordinary-wood supply through WM8**. In the illustrative tests, Model B raises efficient WM8 output from about **55.4 to 58.2 wood events per hour**, while Model C lowers it to about **49.8**. Because ordinary wood feeds several civic and economic relationships, chance would propagate beyond a single crafting input.

HM8 edible supply is the next largest absolute flow. Its pressure should be handled later through real consumption, trade, preservation, and demand relationships rather than random loss or bonus production.

## 9. Audit Conclusion

Model A is the only model that preserves all approved constraints without introducing an unneeded supply source or an unmasterable failure layer.

- **Primary outputs deterministic:** Yes.
- **Random failure:** No.
- **Random bonus outputs:** No.
- **XP/hour:** Approved method rates remain unchanged.
- **Output/hour:** Approved throughput remains unchanged.
- **Fairness:** No-output outcomes remain attributable to opportunity state, player execution, deliberate choice, or readable world conditions.

**LOWMARK GATHERING RANDOMNESS DECISION: READY FOR CREATIVE DIRECTOR APPROVAL**
