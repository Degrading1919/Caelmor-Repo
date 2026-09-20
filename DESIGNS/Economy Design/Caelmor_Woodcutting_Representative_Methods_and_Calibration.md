# Caelmor — Woodcutting Representative Methods and Calibration

**Status:** Proposal-stage numerical calibration for Creative Director audit
**Scope:** Representative Woodcutting methods from level 1 through 99; no exact unlocks, final timings, species, tools, prices, yields, or implementation data

## 1. Calibration authority and rules

This proposal uses the authoritative cumulative XP thresholds:

| Milestone | Cumulative XP | Nominal engaged time |
|---:|---:|---:|
| 30 | 221,617 | ~11 h |
| 50 | 652,858 | ~31 h |
| 70 | 1,549,627 | ~63 h |
| 80 | 2,324,814 | ~90 h |
| 99 | 5,000,000 | ~145 h |

A fixed authored Woodcutting action awards the same base XP under the same conditions at every player level. Later efficiency comes from different work, better source selection, familiar routes, reduced invalid cutting, combined delivery, improved preparation, better access, and later-approved tools. It never comes from a hidden level multiplier.

All cadence values are analytical assumptions for calibration. They do not define runtime locks, tool speeds, respawn, source regeneration, or final placement.

## 2. What counts as a Woodcutting method

A method is a complete work and destination loop:

```text
managed source and current purpose
→ inspect and select
→ authorized cut / pruning / recovery
→ ordinary wood inventory + eligible bark
→ keep / bank / baseline trade / repair / tannery / fuel-worker supply
→ return or continue route
```

One broad provisional ordinary-wood state serves every method. Methods differ through source condition, stewardship, route, demand, bark eligibility, risk, and destination rather than better wood tiers.

## 3. Fixed authored-action XP vocabulary

| Method ID | Fixed authored actions | Loop base XP |
|---|---|---:|
| WM1 | Maintenance inspection 90; authorized selection 80; household cut 260; ordinary recovery 170 | 600 |
| WM2 | Rotation read 140; eligible-section selection 180; renewal harvest 360; wood/bark recovery 220 | 900 |
| WM3 | Bank-stability assessment 260; minimum-intervention choice 220; constrained cut/prune 360; protected recovery 260 | 1,100 |
| WM4 | Three WM2 renewal works completed as one planned route; no circuit bonus XP | 2,700 |
| WM5 | Damage diagnosis 300; safe-scope preparation 240; recoverable cut 520; usable-output recovery 440 | 1,500 |
| WM6 | Repair-demand inspection 360; source matching 420; authorized harvest 650; custody-preserving recovery 570 | 2,000 |
| WM7 | Multi-constraint diagnosis 500; viable-source selection 450; extraction planning 350; selective harvest 700; output routing 500 | 2,500 |
| WM8 | One WM1 work + one WM2 work + one WM3 work; no circuit bonus XP | 2,600 |

**Provisional Woodcutting XP/action range:** 80–700 XP for represented fixed actions.

WM4 and WM8 reuse constituent action XP exactly. Route efficiency shortens empty movement and duplicated preparation; it does not add a completion bonus or alter action XP by player level.

## 4. Representative method portfolio

### WM1 — Household maintenance round

| Dimension | Proposal |
|---|---|
| Progression role | Novice; reliable low-attention method with lasting convenience |
| Opportunity pattern | WN-01 household managed-tree maintenance; S1 source relationship |
| Complete loop | Inspect disclosed need → select authorized growth → cut/prune → recover ordinary wood and eligible bark → household, bank, market, repair, or fuel route |
| Why choose it | Short familiar route, dependable ordinary wood, low risk, useful household context |
| Attention / knowledge | Low after markings and retained growth are learned |
| Risk | Low; unsafe fall zone or active household use can close work |
| Outputs | One ordinary-wood output event per completed work; bark only when source/action qualifies |
| Banking / processing burden | Low when tied to household or market intake |
| Self-supply value | General repair relationship and indirect charcoal supply |
| Economic value | Dependable baseline trade and ordinary repair/fuel demand |
| Mastery improvement | Faster invalid-source rejection, cleaner route, fewer unnecessary cuts |
| Later relevance | Convenient wood near ordinary destinations; reliable familiar routine after later methods unlock |

### WM2 — Managed renewal-stand harvest

| Dimension | Proposal |
|---|---|
| Progression role | Novice through Competent; principal general supply method |
| Opportunity pattern | WN-02 renewal-stand rotation; S2 managed coppice/renewal relationship |
| Complete loop | Read rotation → select eligible section → harvest selectively → recover ordinary wood and qualifying bark → bank, market, tannery, repair, or fuel worker |
| Why choose it | Balanced XP, tangible accumulation, strongest dependable bark relationship, several sinks |
| Attention / knowledge | Moderate until the rotation and retained growth are familiar; then moderate-low |
| Risk | Low to moderate from access, fire condition, or wet ground |
| Outputs | One ordinary-wood event per work; conditional guaranteed bark from eligible source/action |
| Banking / processing burden | Moderate; bark and wood can have different destinations |
| Self-supply value | Strong for Leatherworking bark input and indirect Smithing charcoal supply |
| Economic value | Broad ordinary value; not the fastest later XP method |
| Mastery improvement | Better section choice, fewer closures/invalid cuts, efficient wood-and-bark routing |
| Later relevance | Continues as the balanced wood/bark/self-supply routine and contributes to WM4/WM8 |

### WM3 — Bank-protection intervention

| Dimension | Proposal |
|---|---|
| Progression role | Competent; stewardship and civic-value alternative |
| Opportunity pattern | WN-03 bank-protection intervention; S3 riparian/bank relationship |
| Complete loop | Assess growth and stability → choose minimum intervention → cut/prune → protect recovery → deliver or trade ordinary wood and eligible bark |
| Why choose it | Public/repair meaning, possible bark, useful outputs, distinctive water-edge judgment |
| Attention / knowledge | Moderate to high; cutting the obvious source can be wrong |
| Risk | Moderate from bank condition, footing, water, and invalid intervention |
| Outputs | Ordinary wood; eligible bark where physically produced |
| Banking / processing burden | Moderate to high because safe recovery and public destination can lengthen return |
| Self-supply value | Moderate; bark and ordinary wood remain useful but access is purpose-led |
| Economic value | Economically attractive through repair/civic demand despite lower XP than WM2/WM4 |
| Mastery improvement | Earlier stability diagnosis, smaller intervention, better recovery path |
| Later relevance | Remains a meaningful public-demand and bank-care method; supplies WM8 knowledge |

### WM4 — Renewal-stand circuit

| Dimension | Proposal |
|---|---|
| Progression role | Advanced; reference XP-focused Woodcutting method |
| Opportunity pattern | Three familiar WN-02 works connected through a verified managed-woodland route |
| Complete loop | Inspect and harvest three eligible renewal sections → consolidate wood/bark return → bank, trade, tannery, repair, or fuel route |
| Why choose it | Strong XP/hour through route familiarity and shared destination, not better wood |
| Attention / knowledge | Moderate; efficient section order and closure reading matter |
| Risk | Low to moderate; invalid sections and overcutting erase efficiency |
| Outputs | Three ordinary-wood events per complete route; bark for each physically eligible constituent work |
| Banking / processing burden | Moderate; one consolidated return lowers travel but outputs still require real destinations |
| Self-supply value | High for general wood and bark throughput |
| Economic value | Strong broad throughput; may not beat WM3/WM6 when contextual demand matters |
| Mastery improvement | Better order, fewer invalid sections, reduced duplicated preparation and return travel |
| Later relevance | Familiar profitable routine and a clear benchmark for knowledge-based route efficiency |

### WM5 — Bounded damage-recovery work

| Dimension | Proposal |
|---|---|
| Progression role | Advanced; variable output and authored-condition method |
| Opportunity pattern | WN-04 bounded damage recovery; S1/S2/S3 with W4 |
| Complete loop | Diagnose bounded damage → secure scope → cut recoverable material → separate usable ordinary wood/bark → route output or complete nonproductive cleanup outcome |
| Why choose it | Occasional useful variation, public value, salvage of ordinary supply without a salvage material |
| Attention / knowledge | High; not every damaged source is safe or productive |
| Risk | Moderate to high from tension, unstable ground, contamination, or closure |
| Outputs | Ordinary wood only when usable material exists; eligible bark under normal rules |
| Banking / processing burden | Variable; safe recovery may be slower than the shortest market route |
| Self-supply value | Useful but inconsistent; not a dependable bulk supply method |
| Economic value | Can answer local shortage/repair demand while remaining below the XP leader |
| Mastery improvement | Faster damage diagnosis, safer scope, less waste, correct refusal |
| Later relevance | Occasional authored state that changes familiar sources without continuous world churn |

### WM6 — Public-repair reserve selection

| Dimension | Proposal |
|---|---|
| Progression role | Masterful; output-purpose and custody specialization |
| Opportunity pattern | WN-05 public-repair reserve selection; S4 reserve relationship |
| Complete loop | Inspect repair demand → match authorized source → harvest → recover tangible ordinary wood → deliver under disclosed custody |
| Why choose it | Trusted civic work, meaningful repair destination, useful wood demand, strong identity |
| Attention / knowledge | High; source matching and what remains reserved matter |
| Risk | Moderate access/logistics risk; physical danger depends on final placement |
| Outputs | Ordinary wood; eligible bark where physically valid; no superior reserve wood |
| Banking / processing burden | Purpose-bound delivery can be less convenient than baseline market sale |
| Self-supply value | Low during bound commissions; normal released wood can use ordinary choices |
| Economic value | Contextual public/repair value, not unlimited premium purchasing |
| Mastery improvement | Better matching, less collateral removal, cleaner custody and delivery |
| Later relevance | Optional public work and repair relationship without new material or daily task structure |

### WM7 — Constrained selective extraction

| Dimension | Proposal |
|---|---|
| Progression role | Masterful through Practical Mastery; high-attention XP method |
| Opportunity pattern | WN-06 constrained selective extraction; S2/S3/S4 using W6 |
| Complete loop | Diagnose several constraints → select viable source → plan extraction → harvest selectively → route ordinary wood and bark without violating purpose |
| Why choose it | Strong XP from genuinely denser judgment and execution; no superior tree required |
| Attention / knowledge | High; familiar cues must be combined correctly |
| Risk | Moderate to high from route, stability, fire, neighboring claims, or closure |
| Outputs | Ordinary wood; eligible bark under normal source/action rules |
| Banking / processing burden | Moderate; route and destination planning are part of the method |
| Self-supply value | Good when the selected source aligns with wood/bark need, but less reliable than WM2/WM4 |
| Economic value | Variable; contextual repair/tannery/fuel demand matters |
| Mastery improvement | Earlier diagnosis, smaller intervention, fewer invalid actions, combined delivery |
| Later relevance | Recombines source and demand constraints for post-80 refinement without new outputs |

### WM8 — Familiar mixed-stewardship circuit

| Dimension | Proposal |
|---|---|
| Progression role | Practical Mastery and post-80 refinement; reference late XP route |
| Opportunity pattern | One WN-01, one WN-02, and one WN-03 work connected by verified route logic |
| Complete loop | Complete household maintenance → renewal work → bank intervention in the best current order → consolidate storage/market/processor return |
| Why choose it | Highest modeled XP/hour through route knowledge, source reading, and shared receiving rather than material replacement |
| Attention / knowledge | Moderate to high; order changes with eligibility, closures, bark need, and destination |
| Risk | Mixed ordinary risk; no mastery-only tree or hazard |
| Outputs | Three ordinary-wood events per circuit; bark only from qualifying constituent work |
| Banking / processing burden | Moderate; consolidated return helps but does not bypass storage or processors |
| Self-supply value | Broad ordinary wood, bark, and indirect charcoal relationships |
| Economic value | High throughput creates sink pressure; focused WM2/WM3/WM6 can still be better for a particular need |
| Mastery improvement | Fewer invalid legs, better ordering, combined delivery, reduced empty movement |
| Later relevance | Familiar preferred route with no exclusive output or mandatory commission |

WM8 uses fixed WM1, WM2, and WM3 action XP. It receives no circuit bonus and no player-level multiplier.

## 5. Loop calibration

```text
effective XP/hour = loop base XP × 3,600 / complete-loop seconds
```

| Method | Base XP/loop | Baseline loop assumption | Baseline XP/h | Knowledgeable loop assumption | Efficient XP/h | Baseline output pressure |
|---|---:|---:|---:|---:|---:|---|
| WM1 Household round | 600 | 120 s | 18,000 | 108 s | 20,000 | 30 ordinary-wood events/h; bark only on eligible work |
| WM2 Renewal harvest | 900 | 155 s | 20,903 | 140 s | 23,143 | 23.2 wood events/h plus eligible bark events |
| WM3 Bank intervention | 1,100 | 210 s | 18,857 | 190 s | 20,842 | 17.1 wood events/h plus eligible bark events |
| WM4 Renewal circuit | 2,700 | 350 s | 27,771 | 315 s | 30,857 | 30.9 wood events/h plus qualifying bark |
| WM5 Damage recovery | 1,500 | 220 s | 24,545 | 200 s | 27,000 | Up to 16.4 usable wood events/h; invalid/cleanup outcomes reduce supply |
| WM6 Repair reserve | 2,000 | 260 s | 27,692 | 235 s | 30,638 | 13.8 purpose-bound wood events/h before closures |
| WM7 Constrained extraction | 2,500 | 280 s | 32,143 | 255 s | 35,294 | 12.9 wood events/h plus qualifying bark |
| WM8 Mixed circuit | 2,600 | 208 s | 45,000 | 195 s | 48,000 | 51.9 wood events/h plus qualifying bark; primary throughput risk |

An “output event” is an analytical completed-work relationship, not a final item count. One event may later yield a tuned quantity of the single ordinary-wood state. Bark remains guaranteed only when that constituent source/action physically qualifies.

## 6. Modeled progression paths

### Calibration reference path

The reference path uses:

- Novice XP: 40% from WM1 and 60% from WM2 at baseline execution;
- Competent XP: WM2 baseline;
- Advanced XP: WM4 baseline;
- Masterful approach to 80: WM7 baseline;
- post-80: WM8 baseline.

| Milestone | Incremental XP | Segment time | Cumulative time | Target / envelope | Result |
|---:|---:|---:|---:|---:|---|
| 30 | 221,617 | 11.29 h | 11.29 h | 10–12 h | Within |
| 50 | 431,241 | 20.63 h | 31.92 h | 28–34 h | Within |
| 70 | 896,769 | 32.29 h | 64.21 h | 58–68 h | Within |
| 80 | 775,187 | 24.12 h | 88.32 h | 85–92 h | Within |
| 99 | 2,675,186 | 59.45 h | 147.77 h | 135–150 h | Within |

### Sustainable knowledge-efficient path

Knowledgeable execution improves every selected loop, but it does not turn purpose-bound or compound work into an indefinitely available source. WM5 needs actual bounded damage, WM6 needs a real repair demand, WM7 needs a valid combination of constraints, and WM8 needs three compatible works along a verified route. Sustainable expert progression therefore mixes those opportunities with durable WM3/WM4 work.

The modeled XP shares are analytical portfolio shares, not exact unlocks or rotating schedules:

- Novice: the same 40% WM1 / 60% WM2 mix at knowledgeable cadence;
- Competent: WM2 at knowledgeable cadence;
- Advanced: 82% WM4 and 18% WM5;
- Masterful approach to 80: 20% WM7, 30% WM4, 30% WM6, and 20% WM3;
- post-80: 80% WM8, 10% WM7, 5% WM4, and 5% WM6.

| Milestone | Segment effective XP/h | Segment time | Cumulative time | Closed envelope | Result |
|---:|---:|---:|---:|---:|---|
| 30 | 21,774 | 10.18 h | 10.18 h | 10–12 h | Within |
| 50 | 23,143 | 18.63 h | 28.81 h | 28–34 h | Within |
| 70 | 30,083 | 29.81 h | 58.62 h | 58–68 h | Within |
| 80 | 28,755 | 26.96 h | 85.58 h | 85–92 h | Within |
| 99 | 43,952 | 60.87 h | 146.45 h | 135–150 h | Within |

This mix keeps sustainable expert progression inside every closed envelope without lowering the XP of skilled execution. It reflects the actual opportunity structure: renewal and bank work remain durable, while damage recovery, repair reserves, multi-constraint extraction, and complete mixed circuits require their authored conditions.

## 7. Player-strategy tests

| Strategy | Likely methods | Why it is legitimate | Dominance control |
|---|---|---|---|
| Pure XP | WM2 → WM4 → WM7 → WM8 | Dense valid work and route integration | High attention/route dependence; WM8 creates output pressure and needs several valid sources |
| Profit/output | WM2, WM3, WM6 | Bark, repair/civic purpose, specialist destinations | Lower XP/h, access limits, or purpose-bound delivery |
| Self-supply | WM2 and WM4 | Ordinary wood, bark, indirect charcoal support | Processing/destination time and no superior material |
| Low attention / familiar route | WM1 and learned WM2 | Stable markings, short route, dependable wood | Lower XP ceiling; closures and retained growth still matter |
| Knowledge-efficient | WM3, WM7, WM8 | Avoids invalid cutting and reduces duplicate travel | Requires actual source reading; no hidden player-level modifier |
| Post-Practical-Mastery | WM8 plus optional WM6/WM7 | Route refinement, repair demand, trusted work, useful routines | No daily board, exclusive material, or universal objective |

No method simultaneously leads XP, bark supply, public purpose, convenience, safety, low attention, and focused self-supply.

## 8. Throughput and sink pressure

- WM8 creates about 52 ordinary-wood output events per modeled baseline hour and about 55 under efficient assumptions. This is the portfolio’s clearest oversupply risk.
- WM4 creates about 31 wood events per baseline hour and can also create frequent bark events if every constituent source qualifies. Final ecology must not make every renewal cut bark-eligible by default merely to boost value.
- WM2 remains the strongest balanced bark/self-supply method, while WM3/WM6 carry public and repair value at lower bulk rates.
- Ordinary wood has baseline trade, storage, household/public repair, and accepted fuel-worker sinks. Those sinks justify the state but do not guarantee any quantity will be healthy.
- Exact item yields, market value, repair consumption, charcoal feed ratios, tannery bark consumption, and NPC supply must be tested together before content data is locked.
- If WM8 output overwhelms all sinks, reduce item quantity per output event, limit sustainable route composition through real source conditions, or lower its repeatable route density. Do not invent superior wood or junk recipes.

## 9. Risks and playtest assumptions

1. **WM8 route density:** 208–195 seconds for three completed works is only plausible if the map supports a compact but credible mixed route. **MAP VERIFICATION REQUIRED.**
2. **Sustainable method shares:** prototypes must verify that durable WM3/WM4 work and conditional WM5–WM8 opportunities produce the modeled mix without arbitrary throttling.
3. **Ordinary-wood oversupply:** the tangible state needs sufficient repair, fuel, trade, and later approved use without an unlimited premium buyer.
4. **Bark pressure:** qualifying bark events must support Leatherworking without turning renewal work into a disguised bark farm.
5. **Authored disruptions:** closures can vary routes occasionally but cannot be used as a hidden throttle or rotating chore system.
6. **Low-attention claim:** WM1/WM2 still require readable source eligibility and must not become indiscriminate click repetition.
7. **Purpose-bound custody:** WM6 must preserve disclosed delivery without converting wood into a token or removing normal inventory ownership.

## 10. Woodcutting calibration result

Eight methods cover the five progression identities. Fixed authored actions produce a baseline method range of **18,000–45,000 XP/hour** and a knowledgeable method range of **20,000–48,000 XP/hour**. The reference path reaches the authoritative milestones in approximately **11.29 / 31.92 / 64.21 / 88.32 / 147.77 hours**; the sustainable knowledgeable path reaches them in **10.18 / 28.81 / 58.62 / 85.58 / 146.45 hours**.

The portfolio provides XP, output, self-supply, low-attention, knowledge-efficient, civic, and post-mastery choices without species tiers, wood grades, new materials, or hidden level scaling.
