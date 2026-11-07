# Thornfell — Encounter and Enemy Requirements

**Status (2026-11-03):** review-state content. Gameplay Designer requirement set, Batch 4 of the Thornfell production plan (bible §12). It brings together every enemy family, variant, boss, miniboss, wildlife fight and hazard authored in the Thornfell narrative packages into one implementation reference. Everything here is **[NEW]** authored content and is not canon until the Creative Director promotes it (TD-14). Items marked **[PROPOSAL — DIRECTOR]** are consequential rules the content depends on. Numbers are **framing targets** (fight length, HP remaining, telegraph duration), not balance values. Health, damage, armour and XP values belong to the tuning pass after a playable build exists. This file is **documented dependencies only**: no schema, JSON or C# is authored or implied (bible §11.11).

**Director rulings (2026-11-03, binding):** `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`. CDR-1: every enemy is defeated at **0 HP**; no health-threshold yield, break-off or downed state; Ingrith's scripted surrender on defeat (SX-3) is Thornfell's only exception. CDR-2: Ranged is a core combat skill (S01 resolved); every fight accepts melee or ranged and none requires ranged. CDR-3: Thornfell is an internal milestone of the complete game. Engineering consequences: `Quests/Caelmor_Combat_Ranged_Release_Engineering_Handoff.md`.

**Sources read:** `Quests/Caelmor_Thornfell_Narrative_Production_Bible.md` (whole; §2.4, §2.6, §3 TD-7/TD-8/TD-12, §9.4–9.5, §10, §11 binding); `Quests/Caelmor_Thornfell_Main_Act_I.md` (§A7, §B7), `_Act_II.md` (§A7, §A8.1, §B7, §B8.3), `_Act_III.md` (§7, §7.1, §11, §E); `Quests/Caelmor_Thornfell_Side_Quests_Horn_and_Highsteads.md`, `_Banner_and_Memory.md`, `_Work_and_Skills.md`, `_Settlements_and_Combat.md` (every encounters-and-hazards table, the TME and TDS sections); the Lowmark encounter file as the format standard.

**Source state.** The three main acts were reviewed and committed before this file was written. The four side-quest files were still in independent review when it was drafted; those reviews have since landed, and the independent review of this file (§16) re-checked ids, flags and names against the committed text. Number differences that remain in the packages are superseded by §13 (shared canonical register C-1 to C-8 and rows I-1 to I-21).

**Companion:** `04_CONTENT_PRODUCTION/Zones/Caelmor_Thornfell_POI_and_Zone_Requirements.md` (places, arenas, horn rests, echo faces, phasing). Arena geometry requirements here are repeated there as level-design requirements.

**Ownership:** the Gameplay Designer owns this file. The Schema & Content Engineer owns creature data schema and naming (Roadmap 33.7). The Systems Engineer owns spawn rules, hazard volumes, the call system and status effects. Animation, VFX and audio own the tells.

---

## 0. How to use this file

| You are | Read |
|---|---|
| Building creature definitions | §4 roster, §5 family specs, §6 wildlife, §7 bosses and minibosses |
| Building spawn and encounter data | §11 encounter-pocket index, §10 Horn-Echo storm sites |
| Building hazards and the sound system | §3 telegraph grammar, §9 hazard register (the Summit node is in §9.2) |
| Building combat runtime support | §1 constraints, §8 defeat (CDR-1), §9.4 runtime needs |
| Tuning after the first playable build | §2 bands and universal targets; the band notes in §5 |
| Reviewing for the Director | §13 inconsistencies, §14 questions |

**Id convention.** Thornfell packages already prefix every encounter with its three-letter quest code (`TPW-E1`, `TSG-E2`), so no id collides with Lowmark or with another Thornfell package. Hazards keep `H` ids with the same prefix. Hazards the packages describe without an id get one here, marked **[NEW id]**. World pockets outside any quest use `TW-<nn>` (§11.3).

---

## 1. Runtime constraints that shape every encounter

These are the Lowmark constraints (Lowmark encounter file §1), unchanged, plus the Thornfell-specific lines.

| Constraint (source) | What it means for encounter design |
|---|---|
| **Click-to-move on a host NavMesh; Shift sprint; no jump** (Unity README; Phase 1.3 §1) | Every dodge is "click a floor point and walk there". No counter needs a jump, dash, roll or precise input timing. "Brace" (TSL-E2) is a single click on the rock, not a timed input. |
| **Agility triggers approved, not built** | No encounter may need an agility trigger. Every Thornfell shortcut into an arena (goat track, chimney, shimmy, scramble) has a walkable fallback, and shelter faces, niches and pillars must be NavMesh-reachable. |
| **10 Hz authoritative tick; intents enqueue for T+1** (Stage 6.1.1) | **Minimum telegraphs (carried from Lowmark):** light hits ≥ 0.8 s; moderate or heavy hits ≥ 1.0 s; any hit at or above 25% max HP, any displacement and any area effect ≥ 1.5 s. Gusts are displacement, so the wind-window tell must be ≥ 1.5 s (canonical 2.5 s, §13 I-1). |
| **Auto-attack on interval; specials on cooldown; no stamina** (Phase 1.3 §2) | Fights are about position, target priority and **sound** (who is about to call), not input speed. |
| **AI roles Passive / Aggressive / Defensive; enemies never flee** (Phase 1.3 §2) | Matches CDR-1: every Thornfell enemy, human or animal, fights until defeated at 0 HP (§8). The former wolf break-off and human yield are removed (§13 C-5, I-6). Leash/reset stays. |
| **Combat states; Incapacitated "does not imply death"** (Stage 6.1.2) | No longer required by Thornfell content: humans are defeated at 0 HP. Ingrith's SX-3 outcome is a quest on-defeat hook that spawns her as a non-hostile NPC (§7.1, §8). |
| **Interaction needs reach and line of sight** | Channels under attack (winch, snub post, pull-line cut, Take the horn, Unbolt) need a clear standing pad facing the object. |
| **Player camera only** | Telegraphs must read at default zoom from any angle. In Thornfell the **audio tell is primary** and the visual tell is its required twin, except in null-points, where only the visual tell plays (TGM). |
| **Solo-first; per-player state** (bible §9) | Every encounter is solo-clearable at its band. Co-op scales health per participant, shares world creatures and gives step credit to all participants on the step. Storm windows, whiteout, Close count and Ingrith's SX-3 scene are per player. |
| **Combat never reveals evidence** (bible §11.3) | No creature drop advances an investigation, and defeated ordinary enemies have no dialogue. Testimony comes from non-combatants (Bersi), allies, places or Ingrith's SX-3 scene. Phenomena prove nothing. |
| **No resonance outside canon sites** (bible §2.4; TD-8) | Horn-Echo figures exist only in Shatterfall's storm volume. Node pulses exist only in the Summit great hall. The Gatefall, every settlement and every side-quest site use ordinary dangers only. |

---

## 2. Progression bands and universal solo targets

Bible TD-12 sets the framing. Thornfell has no quest prerequisite but is tuned as post-Lowmark content. Exact levels belong to tuning.

| Band | Content | Equipment assumption | Combat role |
|---|---|---|---|
| **Competent (early)** | TF-M1, TF-M2; side quests unlocked after TF-M1 (TTH, TNR, TSR, TST, TGY, TBC, TAS, TOS, TWG) | Milestone 2 identity | Learn sound tells, wind windows and hornmen. First humans of the region. First wolves, crows, vipers. |
| **Competent (late)** | Side quests unlocked after TF-M2 (TSL, TWC, TFS, TMM, TSN, TGM, TSM) | Milestone 2 toward 3 | Fauna and elites on the plateau; Greymantle as the reference visual-only fight. |
| **Advanced** | TF-M3, TF-M4, TF-M5; side quests after TF-M3 (TWN, TSG, TRR, TNK) | Milestone 3 | Horn-Echo, the Held Line, node pulses, the Gatefall crews, Ingrith, the Brigand Foreman. |
| **Post-arc** | After TF-M5 | Toward Milestone 4 | World pockets (§11.3), the revisitable Shatterfall storm, world elites. |

**Universal targets (all bands; Lowmark values kept)**

| Rule | Target |
|---|---|
| Standard fight length | 20–90 s per group; set pieces 2–5 min with phases or windows; minibosses 2.5–4.5 min; the Act III boss 5–7 min |
| HP after a first-attempt standard fight | 50–85% remaining |
| Largest single non-boss hit | ≤ 30% of band max HP, telegraphed ≥ 1.5 s |
| Hazards | **Cannot kill a player above 25% HP** (§13 I-12). Stormlight (TSL-H2) additionally clamps at 10%. No hazard or knockback can move a player off a ledge, rim, span or crag: every push goes to a defined safe side (wall, rail, inner side). |
| Group size | 1–4 hostiles active outside set pieces; set pieces cap at 5 (the Held Line's 7 figures are one stand, §7.2) |
| Death | Respawn at the named safe point with step, flags, items and completed segments intact; the pocket resets as its row in §11 says |
| Toughness framing | **fragile** (crow flock members, viper) · **standard** · **sturdy** (howler, shale-coil, plate-thrower, rutting stag) · **elite** (~3–5× standard) · **miniboss/boss** (fight-length driven) |

---

## 3. Telegraph grammar (sound first)

Thornfell's readable system is sound (bible §1.1). Every telegraph has an **audio tell and a visual tell**. Where a call is involved, the call's accessibility glyph (bible §9.4) shows at the screen edge toward the source. Durations below are canonical; where packages differ, §13 gives the reconciliation.

| Shape | What the player hears / sees | Canonical duration | Counter | Used by |
|---|---|---|---|---|
| **Whistle (wind window)** | Fluted face whistles **up a fifth**; snow or grit lifts off the edge in the last 0.5 s; red rag flutters harder (TF-M5) | **2.5 s** tell, **3 s** gust | Step behind a marked face, niche, pillar or hood | Every outdoor site (§9.1) |
| **Call** | An NPC raises a horn (visible arm and horn lift) then blows a call; glyph at screen edge | **1.5 s** raise; call plays its shape | Interrupt the raise with any hit, or blow **Rest within 3 s** of a Gather | Hornman, wolf howler (howl as a call), slinger groove call (TWG) |
| **Line** | Shale line shifts, reeds of haze thicken in a lane, a spear set under the arm | 1.0 s light-moderate · 1.6 s lanes and first-appearance | Step off the line | Spear, viper, echo-figure lane, crow diver |
| **Charge** | Pawing (with dust puffs), head down, front-foot stamp | **1.5 s** minimum | Sidestep; behind a pillar the charger hits it and is stunned 2 s | Rutting stag, Storm Stag, Greymantle, the old ram |
| **Ring** | Shale shivers in a ring; dust lifts round a centre stone; frost flakes off in a ring | 1.5–2.0 s | Walk out of the ring, or into a marked shadow | Shale-coil burst, node pulse, Greymantle's silent roar |
| **Count** | A spoken count ("One. Two. Three."), one beat per ~0.8 s, a step per beat; later silent steps with a raised spear | 0.8 s per beat, three beats | Move once per beat | Ingrith's Count |
| **Fall (shed)** | **Fall** call (short-long-short) from a warden, then grit circles or a dust strip on the ground | ~2.0 s from the grit | Leave the circles; get under a hood or into a niche | Gatefall sheds, the shedding face (TF-M1), spoil slide (TSG) |
| **Echo count** | The player blows **Answer** at a face and counts the beats back; smeared or short means the face is moving | Not timed | Wait for the slide, then go | The shedding face (TF-M1), the whiteout (TF-M5) |

**Four rules for every telegraph.**
1. Audio and visual twins, so a player looking away still gets it; in a **null-point** only the visual twin plays and every visual tell is a large silhouette or dust/frost event, never colour alone (TGM is the reference case).
2. Every heavy tell names its safe space by the environment (white shoulder bar, chalk notch, red-rag niche, pillar snow-wedge, drum hood, stake of a stance) rather than by UI.
3. Every heavy attack has a punish window.
4. **Calls are tools both ways.** Any NPC call the player can hear, the player can answer or cancel with the Ordinary Calls they know: Rest cancels a Gather buff; Fall startles a howler or makes bandits duck once (TTH-E1, TSM-E1, TWG-E1); any call blown at a howler makes it flinch (TPW-E3). This is the region's combat identity and must work in every pocket with a hornman or howler (§13 I-4).

---

## 4. Roster and Phase 1.5 count check

### 4.1 Families (bible §10; Phase 1.5 §4.1: 4 low, 3 mid, 2 high)

| Tier | Family | Default AI role | Standard variants | Elite | Variants counted |
|---|---|---|---|---|---|
| Low | **Ridge Crows** | Aggressive harassers, leashed to a nest volume | flock, diver | — (vermin) | 2 |
| Low | **Ridge Wolves** | Aggressive pack | runner, howler | **Pack-Mother** (unplaced in every package; §11.3 TW-04) | 3 |
| Low | **Rock Vipers** | Aggressive ambush, leashed to shale | viper, shale-coil | — | 2 |
| Low | **Pass Bandits** | Aggressive; some prop-targeting | cutter, slinger | **Corner-Boss** | 3 |
| Mid | **Iron Winter crews** | Aggressive line-holders with a signaller | spear, hornman | none separate: Ingrith is the Act III boss (§13 I-15) | 2 |
| Mid | **Shatterfall Brigands** | Aggressive; plate-throwing; prop-cutting | pick-hand, plate-thrower | **Brigand Foreman** | 3 |
| Mid | **Fell Stags** | Defensive herd; charge when the rut ground is entered | stag, rutting stag | **the Storm Stag** (unplaced; §11.3 TW-05) | 3 |
| High | **Horn-Echo** (resonance imprints) | Storm-bound, lane-charging, blind | echo-figure, echo-line | (slot filled by the Held Line, a miniboss phenomenon, §7.2) | 2 |
| High | **Ridge Bears** | Defensive in dens; Aggressive when woken | bear (unplaced; §11.3 TW-06) | (slot filled by Greymantle, a miniboss, §7.3) | 1 |

**Variant total:** 21 standard and elite variants, inside Phase 1.5 §4.2's ~20–22. **Bosses:** 1 Act III boss (Ingrith Scarrow) and 2 minibosses (the Held Line, Greymantle), matching bible §10 and Phase 1.5 §4.3. **Sub-forms, not variants:** the TIW crew boss (a spear with more health), the uphill group (non-hostile presentation, §10), the young ram (fauna bluff).

**Placement gaps.** Three counted variants (Pack-Mother, Storm Stag, ridge bear standard) appear in no package. §11.3 proposes world placements. If the Director prefers fewer world elites, cutting Pack-Mother and Storm Stag drops the count to 19, still near range.

### 4.2 Wildlife (Hunting fauna; not counted; fight only when provoked)

Cliff goats (incl. the old ram and young ram), storm hawks, snowhares, fell stags out of season (ambient, Passive). Full behaviour in §6.

### 4.3 First appearance and recurrence

| Family | First possible appearance | Main-line first | Recurs in |
|---|---|---|---|
| Ridge Crows | TIW-E1b (ledge route, TF-M2) | TF-M2 (E1b or E3) | TSH-E1, TNR-E1, TRR-E1, TGM-E1 (flock only) |
| Ridge Wolves | TPW-E2 (TF-M1) | TF-M1 | TPW-E3, TTH-E1, TST-E1, TAS-E2, TSM-E1, TWC-E1, TSN-E1, TGM-E1, TSW-E1 |
| Rock Vipers | **TSR-E1 or TOS-E1 (both after TF-M1)** (§13 I-7) | TES-E1 (TF-M3) | TWN-E1 |
| Pass Bandits | TPW-E1 (TF-M1) | TF-M1 | TAS-E1, TWG-E1, TBC-E1; TP26 world pocket |
| Iron Winter crews | TIW-E1 (TF-M2) | TF-M2 | TIW-E2/E4/E5, TSH-E2/E3, TSW-E2/E3/E4; TP08 and TP27 with `leverage` |
| Shatterfall Brigands | TF-M3 overlook (presentation only, TES C5) | — | TSG-E1/E2/E3 only |
| Fell Stags | TSL-E1 (after TF-M2) | — | Storm Stag world elite (proposal) |
| Horn-Echo | TES-E2 (TF-M3) | TF-M3 | TES-E3/E4; post-story Shatterfall storm (§10) |
| Ridge Bears | TGM-E2 (after TF-M2) | — | Ridge bear world pocket (proposal) |

---
## 5. Family specifications

Each table lists the variant kit with canonical telegraphs. "Band notes" gives the role the family plays, not numbers. Telegraph values marked † were reconciled from differing package values (§13).

### 5.1 Ridge Crows (low)

**Ecology.** Black ridge crows that roost in vent shafts, cliff cracks, sheave housings and stair faces. They follow patrols, mob the weak and steal food. They lift all at once on a horn-trial note (TIW S09 trial frame, TSH-E1), which is a tell of the trials and never evidence.

**AI role.** Aggressive inside a nest volume; leashed to it. The flock is one creature with one health pool and is defeated at 0 HP like any creature (the swirl breaking up is its defeat presentation). Vent draughts suspend dives (TIW-E3).

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Flock** | One combined creature (a swirl of 4–6 birds) with one health pool; mobs a spot | The swirl darkens and tightens over one spot, birds go silent (**1.2 s**†), then pecks in a **2 m circle** (light) | Leave the circle; cross under vents on the draught | Competent (all) |
| **Diver** | Single bird; climbs and dives in a straight line from a shaft mouth or tower top | Sharp caw, wings fold, shadow on the floor (**1.2 s**†), then a straight drop strike (light-moderate) | Step aside; shoot it from below with Ranged (C-8) | Competent–Advanced |

**Variants in context.** TRR-E1's flock targets the bread trestle, never people (comic beat). TGM-E1's crows mob only a player under 50% HP; they fight to 0 HP like any flock.

**Defeat / loot.** Defeated at 0 HP. Loot: ordinary feathers or nothing (tuning pass). Nothing advances a quest. Band: flock and diver **fragile**.

### 5.2 Ridge Wolves (low)

**Ecology.** Winter-thin packs on high trails, drawn to carcasses, goat pens, mule trains and carried meat. The **howl is a readable call**: its rising shape rhymes with the Lost glyph (TTH), which is presentation, not meaning.

**AI role.** Aggressive pack. Runners circle and flank; the howler hangs back on a rock and calls. Wolves fight until defeated at **0 HP** (CDR-1; the former 30% break-off is removed, §13 C-5). Escort and protect pockets: runners target the beasts, mules or carried meat first, which can be bitten, made to halt or dropped, but never killed or lost.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Runner** | Flanks in pairs (one front, one circles behind); lunge-bite; snatch variant in TSM-E1 (dives for the carry) | Chest down, ears flat, tail flat (**0.9 s**†), then a lunge 3–4 m. Circler: low growl (**1.0 s**) before its lunge. Snatch: circles behind, head low, growl (**1.2 s**) | Side-step; keep runners in front; pick up a dropped carry | Competent–Advanced |
| **Howler** | Holds a rock 10–15 m upslope; calls reinforcements | Head lifts, ribcage swells (**1.5 s**†), then a long rising howl; if completed, **+1 runner** from the ridge, once per fight (TPW-E3: +2, authored escort pressure). Optional delayed commit form: runners commit 4 s after the howl (TAS-E2, TGM-E1) | Interrupt the draw with any hit, any call blown at it (it flinches; Fall startles it), or a Ranged shot (C-8) | Competent–Advanced |
| **Pack-Mother** (elite; unplaced) | Leads a pack of runners and a howler; **rally howl** that calls one extra runner from the ridge, once; heavy lunge with knockdown | Rally howl: head back, two short barks then a held howl (**2.0 s**). Heavy lunge: hindquarters drop, snow kicks up behind (**1.5 s**), lunge 5 m with knockdown 1 s | Interrupt the rally; sidestep the heavy lunge; fight her last or first, never in between | Advanced / post-arc (TW-04) |

**Band notes.** TF-M1 teaches wolves (TPW-E2, 30–45 s). Every later wolf pocket is a variation on one question: **who is about to call?** In TF-M5 (TSW-E1) the fight is by ear in near-white (3 m visibility): the howl is positional and captioned ("a howl, left") and the lunge comes from that side. Runner **standard**, howler **sturdy**, Pack-Mother **elite**.

**Defeat / loot.** Defeated at 0 HP. Loot: hides belong to the economy pass (goat and wolf leather are not catalog items, TD-13); nothing advances a quest.

### 5.3 Rock Vipers (low)

**Ecology.** Shale ambushers that sun under ledges, in shale fans and on fallen dressed blocks. Leashed to shale: stepping onto bare rock off the fan ends contact (TSR).

**AI role.** Aggressive ambush, leashed to a shale volume. Defensive when the player is off shale.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Viper** | Hidden in a shale patch; fast forward strike 2 m | Tail rattles on shale / a line of shale shifts toward the player (**1.0 s**; **1.6 s** first-appearance version in TSR and TOS†) | Step aside; step off the shale | Competent–Advanced |
| **Shale-coil** | Holds a narrow or a station stone; two attacks (the packages each authored one; both kept†) | **Lunge:** coil draws back, shale slides under it (**1.4 s**), then a lunge along a straight line; a hit applies a short slow (TSR). **Burst:** shale shivers in a ring round the player (**1.5 s**), then it bursts up inside the ring | Step aside of the line; walk out of the ring | Competent–Advanced |

**Band notes.** First reading of shale is optional or short (TSR-E1 30–45 s; TOS-E1 required, 75–90% HP remaining). TES-E1 is the Advanced warm-up under gusts. Viper **fragile**, shale-coil **sturdy**.

**Defeat / loot.** Defeated at 0 HP. Nothing advances a quest.

### 5.4 Pass Bandits (low)

**Ecology.** Deserters and clanless robbers at blind corners and lookouts. They know the Ordinary Calls (TWG: they duck on Fall once). They fight to 0 HP (§8).

**AI role.** Aggressive. Prop-targeting: cutters go for a waiting load's lead line (TBC-E1, ~4 s channel) or pick over pack-frames (TAS-E1) until engaged.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Cutter** | Rushes; two quick cuts; works props | Drops the shoulder, blade drawn back low (**1.0 s**†), then a two-cut rush (moderate). Prop work: crouch at the line, knife drawn (**1.0 s**) then a 4 s cut; any hit interrupts | Step aside; interrupt the prop work | Competent |
| **Slinger** | Holds a ledge or parapet; stone in a straight line; at TWG-E1 leans into a horn-tower groove to call help | Sling whirled overhead with a **rising whirr** (**1.2 s**†; glyph: a spiral), one stone along a line (light-moderate). Groove call: steps to the channel and leans (**2.0 s**); if not interrupted, +1 cutter once | Strafe; interrupt the groove call with a hit or Fall | Competent |
| **Corner-Boss** (elite) | A deserter in a Warden's coat with the badge cut off; anchors a bend; steps in when a cutter is defeated; the last of his group to fall | Raises the hood and plants his feet (**1.4 s**), then a two-hit heavy chop, the second hit bigger | Step out after the first hit; punish the recovery | Competent (TPW-E1) |

**Band notes.** TPW-E1 is the first Thornfell fight (90–120 s, 50–70% HP); the goat track gives the player the slingers first (~20% easier). Later bandit pockets are short and readable. Cutter **standard**, slinger **standard**, Corner-Boss **elite**. **World:** the Blind Corners (TP26) keep a bandit population after TF-M1 (TW-01).

**Defeat / loot.** Defeated at 0 HP with the ordinary defeat presentation (§8). Ordinary loot only (§12); nothing evidentiary. No dialogue after defeat; the Corner-Boss's cut badge is read on the overturned cart (T-2).

### 5.5 Iron Winter crews (mid)

**Ecology.** The splinter's fighters: Blood-Oath households and clanless hires with new ridge-iron spears and horns. They drill to calls. Clanless **hires** (TIW-E1) are non-combatants who drop their spears and run downhill when a fight starts; they are not enemies and are not targetable. Iron Winter crews never appear after TF-M5 (the splinter is over, Act III §E.10) except in the `leverage` pockets before it.

**AI role.** Aggressive line-holders. They obey hazards too: they shelter from node pulses (TSH-E3) and from gusts.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Spear** | Holds a line, a stair or a landing; long straight thrust | Sets the haft under the arm, plants the back foot and steps (**1.0 s**), then a long thrust along a line (moderate). With `TH_STORES = leverage` at the Gatefall: bright new spearheads; thrust adds a short bleed (§13 I-10) | Sidestep the line | Competent–Advanced |
| **Hornman** | Hangs back by a horn ring or pull-line; signals | **Raise (1.5 s**†**)**, then **Gather** (three short): allies within 8 m attack faster for **8 s**†. In TIW-E4 his Gather instead calls counting-room crew B to the fight. In TSW-E4 he blows **Close** for Ingrith's slab drop (§7.1) | **Interrupt the raise** with any hit, or **blow Rest within 3 s** of the Gather to cancel it (every hornman pocket, §13 I-4) | Competent–Advanced |
| *Crew boss* (sub-form) | A spear with more health that counts the drill (TIW-E1) | As spear | As spear | Competent |

**Band notes.** TF-M2 teaches the hornman and the Rest-cancel (TIW-E1, E4). TF-M4 asks the player to fight between node pulses (TSH-E3). TF-M5's gallery crews are optional if the pull-line is cut (TSW-E2/E3). Strength by `TH_STORES`: `reported` standard; `seized` fewer (TSH-E3 has no extra spear; TSW-E3 unmanned); `leverage` more (TSH-E3 +1 spear; TSW-E3 crew of 4 with new spearheads; Ingrith's phase 2 +1 spear). Spear **standard**, hornman **standard**.

**Defeat / loot.** Defeated at 0 HP with the ordinary defeat presentation (§8). Ordinary loot only; nothing evidentiary. Defeated crews have no dialogue.

### 5.6 Shatterfall Brigands (mid)

**Ecology.** Out-of-work miners turned raiders, using salvaged plates as weapons and the siege works as a camp. Two of them are Gerrit Carrick's own men (TSG). Thrown and toppled plates **ring**, which is a tell of tuned stone (bible §2.1), never resonance-as-attack.

**AI role.** Aggressive. Cutters at the prop stones **ignore the player until attacked** and work a visible ~90 s cut (TSG-E3).

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Pick-hand** | Presses; heavy single blow; prop cutter | Pick raised high, back arched (**1.1 s**), heavy blow | Step aside; punish the recovery; attack a cutter to stop its work bar | Advanced |
| **Plate-thrower** | Holds the breastwork or a high ledge; throws flat plates | Draws a plate back and it **rings rising** as it is wound (**1.2 s**; glyph: rising bar); flat disc flies straight; a second delayed ring when it lands | Side-step | Advanced |
| **Brigand Foreman** (elite) | Ex-miner in a plate-shard apron with a pry-bar; talks the whole fight. Full kit §7.4 | Pry sweep 1.2 s; stack topple 1.5 s; second wind 2 s | §7.4 | Advanced (TSG-E2) |

**Band notes.** TSG only, by design (bible §10: "TF-M3 edge, *Salvage Ledge*"); in TF-M3 they are seen from the overlook and never fought. Pick-hand **standard**, plate-thrower **sturdy**, Foreman **elite**.

**Defeat / loot.** All defeated at 0 HP, the Foreman included (§7.4). **Plates are not loot**: the stack is a carry-state crate returned to the Horn Seat (TSG S07).

### 5.7 Fell Stags (mid)

**Ecology.** Stormwake herds made aggressive in the rut and by resonance winds (bible §10). Leashed to the rut ground (~30 m). Out of season they are Hunting fauna (§6).

**AI role.** Defensive herd. The rutting stag turns the herd when the player enters the hollow.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Stag** | Holds and flanks only inside the hollow | Turns toward the player on the rutting stag's bellow (**1.0 s**) | Stay out of the hollow; skirt along the scarred stones | Competent (late) |
| **Rutting stag** | Straight charges | Paws twice and lowers its head (**1.5 s**†), straight charge (heavy) | Sidestep; it overruns and stands exposed ~1.5 s | Competent (late) |
| **Storm Stag** (elite; unplaced) | An old white-flanked stag that charges only in storm windows; its antlers carry stormlight | **Charge** as rutting stag (**1.5 s**). **Stormlight:** a rising buzz from its antlers (**2.5 s**, the TSL-H2 tell) before a lightning strike near it; get low in a lee or away from it | Sidestep; leave its side when its antlers sing | Advanced / post-arc (TW-05) |

**Defeat / loot.** Defeated at 0 HP; standard leash/reset at the leash edge (not a retreat). Antler and hide belong to the economy pass. Nothing advances a quest.

### 5.8 Horn-Echo (high) — resonance imprints

Full rules in §10. **Author truth:** imprints of the wartime horn blast in violent storm wind, not spirits. **Combat disperses, conditions decide** (bible §2.6).

**AI role.** Storm-bound and **blind**: each figure forms in a lane and charges straight down it, colliding with whatever is in the lane. No tracking, no target selection. Struck figures break into haze and re-form in their lane while the storm window lasts. When the window turns, all fade.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Echo-figure** | Forms in a lane and charges; re-forms after **12 s** (window 2) or **9 s** (window 3) | **Lane tell:** haze thickens along the whole lane and snow lifts off the ledge in a line, low drag in the audio (**1.6 s**). Charge: knockback toward the wall plus moderate damage; never off the ledge | Step out of the lane; shelter behind a marked face; strike to break it (it re-forms) | Advanced |
| **Echo-line** | Three figures abreast across two lanes, charging as one; breaking the middle figure collapses the line | Haze darkens in a broad band and the fluted faces **drop a note** (**2.0 s**) | Leave both lanes, or break the middle figure | Advanced |
| *Uphill group* (presentation, not a variant) | Five or six shapes that run **uphill toward the Horn Seat** and break on the wall below it; pass through the player as haze; no damage | Ordinary lane tell | None needed | TES S05 only |

**Defeat / loot.** Not creatures that die or drop anything (spirit place rule: they re-form while the storm lasts, CDR rulings §3.1.2). No target frame name (blank), no nameplate, no colours, no face, no clan mark.

### 5.9 Ridge Bears (high)

**Ecology.** Apex animals that hibernate in cliff caves. Greymantle woke on a horn-trial night (TGM; a dated coincidence that proves nothing, TGM S01).

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Bear** (standard; unplaced) | Defensive in its den; Aggressive if the den is entered; swipe and charge | Swipe: weight back, ruff lifts (**1.0 s**), wide arc. Charge: head down, two paw-strikes with dust (**1.6 s**), straight charge (heavy) | Sidestep; pillars and boulders stop the charge | Advanced / post-arc (TW-06) |
| **Greymantle** (miniboss) | §7.3 | §7.3 | §7.3 | Competent (late)–Advanced |

**Defeat / loot.** Defeated at 0 HP. Greymantle is defeated like any creature; how he is left is a quest choice (TGM S06), not loot. A standard bear's materials belong to the economy pass.

---

## 6. Wildlife combat behaviour (Hunting fauna; not counted)

| Animal | Default role | Provoked / scripted state | Telegraph | Counter | Appears |
|---|---|---|---|---|---|
| **Storm hawks** | Passive (ride updrafts) | Harass anything on their ledge: one dive at a time on a 6–8 s cycle; lands on the lip 2 s after each dive | Shriek, then the hawk's shadow sweeps the rock (**1.2 s**) | **Brace** (one click on the rock) negates the knockback; a landed hawk is an ordinary target defeated at 0 HP with melee or Ranged (C-8); defeating it is allowed, never required (Brace alone gets the player across) | TSL-E2 (Splitpine Crag hawk ledge) |
| **The old ram** (cliff goat) | Passive herd leader | Charges along the shoulder path at dusk or at a careless approach, then resettles | Head down and a front-foot stamp (**1.5 s**†), straight charge along the path | Step into a moss-marked niche or sidestep downhill into the heather; never off a cliff | TGY-E1 |
| **The young ram** | Passive | Bluffs travellers for a season after the cull path; charge stops short | As old ram, shorter charge | Harmless | TGY-E2 (post-quest ambient, `TGY_WAY = cull`) |
| **Cliff goats** | Passive | Driven by Gather and Fall calls (TGY drive); never hostile | — | — | TP28; TME07 skull only |
| **Snowhares** | Passive, flee into drifts | Hunting interaction only (snare or still-approach) | — | — | TFS, TSM |
| **Fell stags (out of season)** | Passive | Become the Fell Stags family only on the rut ground (§5.7) | — | — | Stormwake plateau |

**Rules.** Fauna in a fight are defeated at 0 HP (CDR-1); none flees on health. The old ram's resettle after a charge is a scripted pathing beat outside combat, not a health retreat. Quest-spawned fauna is one instance per player.

---

## 7. Bosses and minibosses (consolidated)

### 7.1 Ingrith Scarrow, the Quartermaster — Act III boss (TF-M5, `TSW-E4`) `[SPLINTER]`

Source: Act III §6 Beat 4, §7, §7.1 (committed). Summary for creature building; the Act III spec is authoritative.

| Field | Spec |
|---|---|
| Read | Broad, weathered woman in a quartermaster's quilted coat with tally cords at the belt; ridge-iron spear; lips moving as she counts. Not a monster: never threatens the column. |
| Arena | Winch floor (H3) over the Gatefall cut: ~18 × 10 m timber floor, **drum hood** (~6 × 4 m, cover), **slab slot** (2 m strip, danger on a drop), hornman's parapet with a fluted stone, inner stair (entry) and outer stair (phase-2 crew). Railed edges; no fall. |
| **The Count** | Says "One." "Two." "Three." (~0.8 s each), stepping forward; a thrust on each number (moderate). P3: silent, telegraphed by steps and a raised spear per number. Counter: step aside each beat. |
| **Short Measure** | Says "Short." and reverses the spear (**1.0 s**); butt-stroke, 2 m knockback, brief stagger. |
| **The Close** | Hornman raises (**1.5 s**†, §13 I-3) and blows Close (two long falling, ~2.0 s); on the second note she kicks the drum brake: the slab drops a notch, heavy damage + knockdown **in the slot only**; dust falls along the slot first. Counter: be out of the slot by the second note, or interrupt the raise. Period ~20 s (P1), ~15 s (P2), ~12 s (P3). |
| **The Gust** | Fluted parapet whistles (**2.5 s**); she steps behind the hood post; gust pushes open-floor players 2 m toward the inner wall and slows 3 s; she lunges at a slowed player. Counter: under the hood with her, or brace at the rail. |
| **Gate gallery shed** (P2–P3) | Dorn's **Fall** from below, grit circles (~2 s), stone; hits her too. |
| Phases | P1 Count 100–60% → "Gather." two crew up the outer stair (three with `leverage`) → P2 Crew 60–35% → she drops her tally cords and goes silent → P3 Silent 35–0%. |
| Defeat (SX-3) | Defeated at **0 HP**; no health threshold. **When Ingrith is defeated, the quest plays her scripted surrender** instead of the ordinary defeat presentation: she plants the spear and sits on the drum frame, still counting under her breath, and is spawned as a non-hostile NPC (CDR rulings §4 SX-3). The hornman and any crew fight on to 0 HP; `TSW-D5` opens when the winch floor is clear. **No loot. Nothing evidentiary.** |
| Targets | Solo 5–7 min (Advanced identity, cooked food); ends at 30–60% HP. No single hit above 30% max HP except The Close in the slot (~35%; the one sanctioned exception, telegraphed ~3.5 s from raise to drop). |
| Death / logout / co-op | Respawn in the warden room; fight resets to the top of the current phase (100/60/35%); defeated crew stay defeated. Logout restarts at 100%. Shared boss; health scales; the Count rotates targets; per-player SX-3 scene. |
| Splinter swap | Name, coat and lines swap under TD-1; the mechanics (count, gate, gust) survive any "quartermaster who knows the gate". |

### 7.2 The Held Line — miniboss phenomenon (TF-M3, `TES-E4`)

Source: Act II §A6 Beat 6, §A7 (committed). **Design name only: never shown in UI, never said in dialogue.**

| Field | Spec |
|---|---|
| What it is | A stand of **7 echo-figures** across the seat approach (L7), re-forming in place, during storm window 4 (peak, then turning). |
| Arena | Shelf path ~8 m wide between wall and drop, climbing to the Horn Seat; **three marked shelter faces**; walkable ramp (agility scramble optional). Drop side has an edge blocker. |
| **Surge** | Horn swell builds (**2.5 s**: haze darkens, every figure leans), then the wall pushes ~4 m: heavy damage + knockback in the open; nothing behind a marked face. |
| **Short charge** | Between swells, single figures step out and charge short lanes (lane tell **1.6 s**). |
| Gaps | A broken figure leaves a gap that closes in **~6 s**. Breaking all seven before the gaps close disperses the stand, which counts as one swell endured early; it re-forms on the next swell. |
| End | **Never by a kill.** The window turns after 4 swells (2.5–3 min of endurance; ~1.5–2 min with aggressive play). Whistle drops, haze thins from the top down, figures fade. |
| Persistence | Swells endured persist on death; the stand re-forms at its start position. Respawn at the camp shelf. |
| Co-op | Shared figures; either partner's breaks count. |
| Rules | Blank target frame; no nameplate, face, colours or clan mark; no voiced identity. Dorn: "Window's turning." Nothing else. |

### 7.3 Greymantle — side miniboss (TGM, `TGM-E2`)

Source: Settlements and Combat TGM.7.1 (committed).

| Field | Spec |
|---|---|
| Read | Huge old ridge bear, grey across the back, ribs showing; left forepaw lame (left-side swipes slower). |
| **Audio rule** | Inside the inner chamber (G9, a null-point) **no world audio plays**: no bear sounds, footsteps, hits or voiced lines; UI sounds also muted [PROPOSAL — DIRECTOR, TGM-OD1]. Rumble carries impacts. Every tell is visual with a fixed duration. |
| Arena | Round chamber, **three free-standing pillars** (block charges; a charge into a pillar stuns him 2 s), the hollow at the back, thick dust on all ledges. |
| **Swipe** (all) | Weight onto back legs, ruff lifts, snow sloughs off the swiping shoulder (**1.0 s**; left **1.4 s**); wide arc, moderate. ~6 s cadence. |
| **Charge** (all) | Head down, two paw-strikes each throwing a dust puff (**1.6 s**); straight charge, heavy. ~12 s. |
| **Silent roar** (P2–P3) | Rears, breath plumes (**2.0 s**); no sound; dust jumps off every ledge and falls straight; frost ring expands (8 m): knockdown 1.5 s inside. Dust curtains hide his outline for 6 s except where he moves through them. ~18 s (P2), ~14 s (P3). |
| **Ceiling fall** (P2–P3) | Rears against a wall; dust shadows on the floor (**1.8 s**) then a stone; max 3 at once. |
| **From the side** (P3, <35%) | Into the hollow; 3 s later out from behind a pillar; **dust trickles from that pillar's top** (**1.5 s**). Once per 20 s. |
| Phases | P1 100–60%; P2 60–35%; P3 <35%. No enrage. |
| End | Defeated at **0 HP** like any creature (the 10% lie-down is removed, CDR-1). He falls in the chamber; the S06 choice is **how the old bear is left**: seal the den as his resting place (three stones and Yrsa's stormflower net, "so the wind can't reach him"; `sleeping`) or leave him to the trappers (`ended`; Yrsa butchers, Hunting optional). Same steps and flags (CDR rulings §4). |
| Targets | 3.5–4.5 min, late Competent to early Advanced. |
| Reset / co-op | Leaving G9 or dying resets him to full in the hollow; tracking steps persist. Shared creature; silence applies to every player in G9. |
| Reference case | The slate's reference for visual-only telegraph readability (large silhouette or dust/frost events, never colour alone). |

### 7.4 Brigand Foreman — elite (TSG, `TSG-E2`)

Source: Settlements and Combat TSG.7.1 (committed).

| Ability | Telegraph | Effect | Counter |
|---|---|---|---|
| **Pry sweep** | Plants the pry-bar's foot and leans (**1.2 s**) | Low sweep, knockdown on hit; ~8 s cadence | Step back out of reach |
| **Stack topple** (once per stack, 3 stacks) | Heaves a plate stack; it **rings as it tilts** (**1.5 s**) | Plates spill in a cone; damage and a 3 s ringing patch that slows | Leave the cone and the patch |
| **Second wind** (<50%, once) | Drinks from a flask (2 s) | Heals 10% if not interrupted | Any hit interrupts |
| Defeat | At **0 HP** (the 20% yield is removed). He bellows "Cut the props!" as his **second wind** bark; TSG S04–S05 start **on his defeat** (step trigger "on defeat" replaces "on yield") | — | — |
| Reset | Leaving the shed resets him to 100% unless defeated; stacks re-stack | — | — |
| Target | 2–3 min with 1 pick-hand | — | — |

---
## 8. Defeat (CDR-1; supersedes TD-7)

**Rule.** Every Thornfell enemy, human, animal or Horn-Echo figure, fights until defeated at **0 HP**. No health threshold ends a fight early; nothing yields, kneels, breaks off, limps away or lies down because of its health. Leash/reset stays standard RPG behaviour. Echo-figures re-form while the storm lasts (a place rule, §10). XP, loot and co-op credit are awarded at defeat. Every step that completed "on yield" completes **on defeat**. The former TD-7 table (bandits, Iron Winter crews and brigands yield at 0%; the Foreman and Ingrith at 20%) is retired.

**Defeated humans.** Ordinary defeat presentation: the enemy falls and fades after the standard corpse time, with ordinary loot (§12). No tied or bound props, no downed state, no "walked down" or "marched to Passwatch" afterlife, no dialogue with a defeated ordinary enemy. One short, sober ally line after a human fight is enough where the old text had a "they'll live" beat. Where the old text said crews were walked down, say the pass is clear.

**The one scripted exception (SX-3).** Ingrith Scarrow is defeated at 0 HP like any boss; the TSW quest's on-defeat hook then plays her scripted surrender instead of the ordinary defeat presentation and spawns her as a non-hostile NPC for `TSW-D5` (§7.1). She is held in the warden room, walked to Stonewake at dawn and kept for a clan tribunal at thaw.

**Non-combatants (never targetable; SX-N, not exceptions):** **Bersi Coldbrook** (TIW-E5) never fights; when the last crew member in the counting room is defeated he gives up (a quest script) and testifies (SX-N1). The crews fight to 0 HP; there is no encounter-level surrender, and a fight that only comes near him does not end the encounter. **Eyvind Stall** (TSH) is stopped by **Take the horn** (~2 s channel, SX-N2). Gallery crews whose haul ends because the player **cut the pull-line** sit down: a puzzle outcome, not a health outcome (SX-N3). Also never targetable: the clanless hires (TIW-E1; run downhill when the fight starts), the Blood-Oath tower crew (TAS; de-escalated, never hostile), every Thornfell settler, child and warden.

**Runtime need (Systems Engineer).** None beyond standard defeat at 0 HP. The former health-threshold yield event, CombatIncapacitated use and hostile-to-neutral swap for ordinary humans are **removed**. One quest-level need remains: a **quest on-defeat hook for named creatures** (Ingrith SX-3; also step triggers "on defeat" such as TSG S04), see the integration handoff and `Quests/Caelmor_Combat_Ranged_Release_Engineering_Handoff.md`.

**Animals.** Wolves, crows, stags, hawks and bears are defeated at 0 HP and can be harvested where the economy allows. The wolf break-off (former C-5) and Greymantle's 10% lie-down are removed.

---

## 9. Hazard register

Hazards are environmental. They have no health, no target frame and no AI. All obey §2: **cannot kill a player above 25% HP** and **never push anyone off an edge**.

### 9.1 Wind windows and weather hazards

| Id | Hazard | Where | Tell | Effect | Safe space | Source |
|---|---|---|---|---|---|---|
| **TPW-H1** [NEW id] | Gust | Pass road, Narrows scree path, span | Whistle up a fifth (**2.5 s**†) | Push 2 m† toward the wall, light damage in the open | White shoulder bar (S1–S3) | Act I §A6 Beat 7, §A7 |
| **TPW-H2** [NEW id] | The shedding face | Narrows S2 | Answer echo comes back short or smeared; dust spills (**~2 s**), then stones | Moderate damage, knockback to S2; line stays paid out | Wait at S2 for the slide | Act I Beat 4, Beat 7 |
| **TIW-H1** [NEW id] | Shaft down-draught | Whinstone hoist shaft (G2) | Vent slits whistle up a fifth (**2.5 s**†) | On the rungs: pushed, light damage, climb pauses | Rest ledges | Act I Beat 5 |
| **TIW-H2** [NEW id] | Vent draught (benefit) | Iron gallery vents (G5) | Whistle up a fifth, then **~3 s** draught | Crows cannot dive; crossing is free | Cross on the draught | Act I TIW-E3 |
| **TES-H1** [NEW id] | Gorge gusts | Shatterfall ledges L1–L7 | Whistle **~2.5 s**; cycle 25 → 22 → 18 → 15 s by storm window | Push wallward, light damage | Chalk-notched shelter faces | Act II §A8.1 |
| **TES-H2** [NEW id] | Swell masking | The Hollow (L5) | Haze darkens and faces drop a note (**~2 s**) | A seam struck during the swell gives no reading (time cost only) | Strike between swells | Act II Beat 5 |
| **TSH-H2** [NEW id] | Air-channel draw | Summit inner stair (S2) | Torch flames lean to the channel (**1.5 s**), then the draw (~2 s) | Pushed back one step, carried lantern out; **no damage** | Sconce niches | Act II Beat 2 |
| **TSW-H1** [NEW id] | Whiteout sheds | High track C2–C6 | Warden blows **Fall**; grinding creak, grit | Moderate damage + knockdown in the open; never lethal at full health | Red-rag niches; wait for Rest | Act III Beat 1 |
| **TSW-H2** [NEW id] | Whiteout gust | High track | Whistle **2.5 s** | Push 1 step to the inner wall, slow 3 s | Lee of any face | Act III Beat 1 |
| **TSW-E5** | Winch-floor gusts and G7 sheds | Winch floor, far apron | Whistle **2.5 s**; Fall + grit circles **~2 s** | Interrupts the winch channel (completed segments kept); moderate damage in circles | Drum hood | Act III §7 |
| **TMM-H1** | Terrace gust | Plank under the Signal Terrace | Whistle **1.5 s** in source (→ 2.5 s†) | Push 2 m along the plank, inspect cancelled | Buttress niche | Settlements TMM.7 |
| **TAS-H1** | Scaffold gust | Passwatch arch scaffold | Whistle 1.5 s in source (→ 2.5 s†) | Interrupts a channel (progress kept) | Lee of the arch pier | Settlements TAS.7 |
| **TSL-H1** | Wind windows | Plateau, ramp, hawk ledge, summit block | Whistle 1.5 s in source (→ 2.5 s†); gust 3 s | Pushed back to the last stance | Marked lees | Banner TSL 1.6 |
| **TSL-H2** | Stormlight strike | Splitpine Crag summit block | Rising buzz from iron, blue flicker on gear (**2.5 s**) | Knockdown, moderate damage; **clamped at 10% HP** | Lee notch (three-stone cairn) | Banner TSL 1.6 |
| **TWC-H1** | Sail pull | Old Watchfire Line rite walk | Whistle (→ 2.5 s†), gust 3 s | Bearer pushed 2 m sideways and slowed; the NPC catches the colour | Dip the colour; cairn lees | Banner TWC 2.6 |
| **TWN-H1** | Rim gust | Rim cairns | Whistle (→ 2.5 s†) | Pushed back from the edge (edge blocker) | Cairn lees | Banner TWN 3.6 |
| **TSN-H1** | Tunnel slump | Black Glass Hostel dig-out | Whistle through the glass panel (→ 2.5 s†), gust 3 s | Unshored segment's progress resets; **no damage** | Shore before the gust | Banner TSN 4.6 |
| **TOS-H2** | Wind windows | Oath path, under the arch | Whistle (→ 2.5 s†) | Pushed against the face | The face | Banner TOS 5.6 |
| **TSR-H2** | Scarp gust | Red Slope scarp | Whistle ~3 s in source (→ 2.5 s†) | Stagger, small damage | Chalk faces | Work TSR.6 |
| **TST-H1 / H2** | Stem whip; gust in the open | Burned Slope stands | Whistle ~3 s in source (→ 2.5 s†) | Knockback, small damage | Chalk faces | Work TST.6 |
| **TGY-H1** | Shoulder gust | Goat ledges | Whistle | Stagger | Moss niches | Work TGY.6 |
| **TBC-H1** | Gust on the span | Narrows span | Whistle (→ 2.5 s†) | Loads stop; stagger only; guide line holds | Kneel marks, guide line | Work TBC.6 |
| **TFS** (no id) | Snow-shelf gust | Nettlehook snow shelf | Whistle | Stagger | Drift lees | Work TFS.6 |
| **TTH/TWG/TNR/TSM/TRR** (no ids) | Wind windows | Answering stones, tower parapets, span, shelf path | Whistle "a fifth before the gust" | Stagger / knockdown in source (→ push, §13 I-2) | Chalk-marked faces | Horn and Highsteads §0.6 |

### 9.2 The Summit node (passive hazard; never a creature)

| Field | Spec |
|---|---|
| Ids | `TSH-E3` (pulse hazard inside the crew fight) and `TSH-H1` (pulses after Eyvind is stopped) |
| What it is | Old stone under Echochamber Summit responding to Echohewn plates being sounded (C11, R07). **Not an enemy.** No health, no target frame, no name, no AI, no voice, no intent. It never speaks, warns, judges, chooses or turns toward anyone. |
| Cycle with Eyvind playing | Four audible heel-taps (~2 s; captioned "[Four taps.]") → test note (~3 s) → hum climbs and dust lifts round the **centre stone** into rough upright shapes that **lean outward** and never hold (**2.0 s**) → pressure ring rolls out to the walls (~1 s). Period **~14 s**. |
| Cycle after Eyvind stops (`TSH-H1`) | No taps; the hum steps up first (~1 s), then the dust lean (**2.0 s**), then the ring. Period **~18 s**, +4 s per correct plate damped (18 → 22 → 26 → 30), **−6 s once per wrong plate**; weaker as plates are damped. A dropped plate rings and brings the next pulse a few seconds sooner. |
| Damage | Heavy damage + stagger **in the open**; **none behind a pillar** (pressure shadow, marked by snow wedges) or in a silent alcove (II, V); half in an ordinary alcove. Staggers the crew too. Hit while carrying a plate: the plate drops (pick up again). |
| Stop condition | Stops entirely when the last plate is set in a silent alcove (`S09_silence`). One breath of total silence; dust falls straight (Act II §B8.4). Afterwards the hall hums only in storms, **without pulses**, forever. |
| Rules | The dust shapes are the tell, not a creature. No NPC calls it a guardian, warning or judgement except as a crew belief bark nobody confirms. Never appears anywhere but the great hall. Never used to date or identify anything (the trial record and Iven's log do that). |
| Co-op | Shared pulses; plates are shared objects; all present credited. |

### 9.3 Other environmental hazards

| Id | Hazard | Where | Tell | Effect | Source |
|---|---|---|---|---|---|
| TSW slab drop | Slab-slot notch | Gatefall winch floor | Hornman's Close, dust strip along the slot | §7.1 (boss ability) | Act III §7.1.2 |
| TSW-H3 [NEW id] | Forced shelter | Gatefall cut during `S03` | Fall + whistle together; "Shelter. Wait for Rest." | The cut stays closed by wind until the rubbing is taken (gates movement, no damage) | Act III Beat 3 |
| **TSR-H1** | Slab drop | Red Slope upper face | Grit trickles, crack (**1.5 s**); fall lane chalked | Small damage + stagger in the lane | Work TSR.6 |
| **TOS-H1** | Crumbling path stones (pre-repair) | Oath path, 3 stones | Grit trickles and a crack (**1.2 s**) after stepping on | Slide back to the last sound stone, small damage; gone after TOS S05 | Banner TOS 5.6 |
| **TBC-H2** | Forge spark | Aud's anvil | A bright spit after a clack | Cosmetic sting, no damage | Work TBC.6 |
| TSG slide [NEW id TSG-H1] | Spoil-terrace slide | Spoil slope below the prop stones | Ground-dust line (**1.5 s**) | Fall hazard if both props are cut before all three pairs answer; the terrace "holds one more breath" | Settlements TSG Beat 5 |
| Greymantle ceiling fall | Dust shadow | TGM G9 | Dust falls straight in a patch (**1.8 s**) | Boss ability (§7.3) | Settlements TGM.7.1 |

### 9.4 Status and runtime needs (documented dependencies; nothing implemented)

| Need | Used by | Recommendation |
|---|---|---|
| **Push toward a defined safe side** (wall, rail, inner side), clamped so no edge is crossed | Every gust, charge knockback, surge, butt-stroke | One push effect with a direction source (volume tag) and an edge-clamp |
| **Knockdown / stagger** (timed movement block within CombatRestricted) | Ingrith slab, Foreman sweep, Greymantle roar, Fall sheds, pulses | Same ruling Lowmark asked for (Lowmark I-18) |
| **Slow** (short) | Gust slow (TSW), shale-coil lunge (TSR), Foreman ringing patch, sail pull | One slow status, durations per source |
| **Bleed** (short) | TSW-E3 `leverage` spearheads | **Avoid a new status**: replace with +damage on the thrust and the bright-iron visual (§13 I-10) |
| **Ally buff on a call** | Hornman Gather | One timed attack-speed buff in 8 m; cancellable by a Rest call event within 3 s |
| **Call events** (`call_blown(shape)` with source position) | Hornmen, howlers, wardens, the player | From TF-M1's call system; every listener in this file reads it |
| **Interrupt on hit during a raise / draw / drink** | Hornman, howler, slinger groove call, Foreman flask | One interruptible-windup flag |
| **Dispersal and re-form in a lane** | Echo-figures | Lowmark drift re-form pattern with lane volumes and a storm-window condition |
| **Hazard clamp** (cannot reduce below 25%; TSL-H2 10%) | All hazards | One clamp parameter on hazard damage |
| **Audio-null volume** | TGM G9, TF-M4 W4/alcoves II and V, TDS01, TWG gateposts, TME05 niche, TIW K3 | Mutes world audio by layer; TGM also mutes UI (proposal) |
| **Pressure-shadow volumes** | Summit pillars and silent alcoves | Tagged safe volumes read by the pulse |

---

## 10. Horn-Echo rules and storm sites

### 10.1 Binding rules (bible §2.4, §2.6, §11.3)

1. **The Horn-Echo never identifies anyone.** No nameplate, no name, no face, no colours, no clan mark. Target frames are blank. No UI, NPC, bark, inspect or document names a figure after a real person or says who they are. The one wrong reading voiced aloud ("the dead are up", a miner's bark) is answered only by Dorn's "Wind trick."
2. **The figures prove nothing.** The R06 horn half rests on the Seat's aim, the strata and the roster (TF-M3 required inspects). The uphill group is a seed; the player makes any link from the roster.
3. **Combat disperses, conditions decide.** Striking breaks a figure; it re-forms while the storm window lasts and fades when the window turns. No quest cures the Horn-Echo.
4. **Only at Shatterfall, only in violent storm wind.** Never at the Gatefall (TD-8; Act III §7 "no resonance"), never on the rim cairns (TWN keeps outside the gorge storm volume), never at the Salvage Ledge (TSG's ringing plates are tuned stone, not figures), never in a settlement.
5. **Lanes are readable and charges are blind.** No figure tracks a player. Charges push wallward and never off a ledge.
6. **No boss frame.** The Held Line has no health bar and no UI name. It ends when the window turns.
7. **Footfalls belong to the uphill group only** (the only figures with footsteps; subtitle "[Footsteps, climbing.]").

### 10.2 Storm sites

| Site id | Place | Condition | Content | State after |
|---|---|---|---|---|
| `storm.shatterfall_quest` | Shatterfall Ledges L3, L5, L7 (TP11) | TF-M3 per-player storm windows 2–4 (Act II §A8.1) | TES-E2, TES-E3, uphill group, TES-E4 | Window 5 clears; quest-local |
| `storm.shatterfall_world` [PROPOSAL — Gameplay Designer] | Shatterfall Ledges (lower shelf and seat approach) | After TF-M3 Completed; a world storm presentation window (keep-watch at the Broken Engine can wait for one) | 2 lanes of echo-figures, one echo-line per swell; **no Held Line** and no uphill group (both stay unique to the quest) | Revisitable canon scar (bible §2.6). Never quieted by any outcome |

---
## 11. Encounter-pocket index

**Respawn rules** (Lowmark set). **STEP**: spawns on step entry; gone when the step completes. **→WORLD**: after its step, the area keeps an ordinary population of the same family on the standard world timer. **ONCE**: never respawns for that player. **STORM**: governed by §10.2. **OPT**: optional pocket. Solo targets are the package values (§2 targets apply where none is given).

### 11.1 Main quests (committed packages)

| Id | Step | Place (POI) | Families / variants | Band | Solo target | Respawn | Source |
|---|---|---|---|---|---|---|---|
| TPW-E1 | `S03_corners` | Blind Corners (TP26) | 2 cutter, 2 slinger, Corner-Boss | Competent | 90–120 s; 50–70% HP | ONCE → WORLD (TW-01) | Act I §A7 |
| TPW-E2 | `S05_stakes` | Stormwood slope below the Narrows (Windscar) | 2 runner | Competent | 30–45 s | STEP | Act I §A7 |
| TPW-E3 | `S10_escort` | Blind Corners goat track (TP26) | 3 runner, howler (+2 runners if howl completes) | Competent | 60–90 s; beasts cannot die | STEP | Act I §A7 |
| TIW-E1 | `S04_hut` (yard route) | Muster Hut drill yard (TP27) | 2 spear, hornman, crew boss; 6 hires (non-combatant) | Competent | 90–120 s; 50–70% HP | ONCE; `leverage`: TW-02 | Act I §B7 |
| TIW-E1b | `S04_hut` (ledge route) | Cliff ledge K5 (Windscar) | Crow flock | Competent | 30–45 s or avoided | → WORLD (ambient crows) | Act I §B7 |
| TIW-E2 | `S06_grain` | Whinstone Store grain gallery (TP08) | 2 spear (on break: 1.5 s to stand) | Competent | 30–50 s | ONCE | Act I §B7 |
| TIW-E3 | `S07_iron` | Iron gallery vents (TP08) | 2 flock, 2 diver; vent draughts | Competent | 45–75 s fought; ~20 s on draughts | ONCE (nests stay as props) | Act I §B7 |
| TIW-E4 | `S08_plates` | Plate gallery passage (TP08) | spear, hornman (Gather calls crew B) | Competent | 45–70 s | ONCE | Act I §B7 |
| TIW-E5 | `S09_counting` | Counting room (TP08) | Crew A (spear, hornman), crew B (2 spear unless drawn in E4); Bersi non-combatant | Competent | 60–90 s | ONCE; `leverage`: TW-03 | Act I §B7 |
| TES-E1 | `S02_descent` | Shale before the Jam, L1–L2 (TP11) | 2 viper, shale-coil | Advanced | 40–60 s; 70–85% HP | → WORLD (vipers on the shale) | Act II §A7 |
| TES-E2 | `S04_rig_one` | The Lip, L3 (TP11) | Echo-figures, 2 lanes × 2 per swell | Advanced | Rig in 2–4 min; HP ≥ ~40% with shelter | STORM | Act II §A7 |
| TES-E3 | `S05_rig_two` | The Hollow, L5 (TP11) | Echo-figures, 3 lanes + echo-line; uphill group | Advanced | 3–5 min incl. resets | STORM | Act II §A7, §A8.3 |
| TES-E4 | `S06_seat_approach` | Seat approach, L7 (TP11) | **The Held Line** (7 figures) | Advanced | 2.5–3 min; 1.5–2 min aggressive | STORM (quest only) | Act II §A7 |
| TSH-E1 | `S02_ascent` | Summit outer stair, Narrow Turn (TP17) | Crow flock (6) + 2 diver | Advanced | 40–60 s; ends at the test note (~45 s) | → WORLD (ambient crows) | Act II §B7 |
| TSH-E2 | `S03_landing` | Upper Landing (TP17) | spear, hornman | Advanced | 45–70 s; 65–80% HP | ONCE | Act II §B7 |
| TSH-E3 | `S07_great_hall` | Great hall (TP17) | 2 spear, hornman (+1 spear `leverage`); node pulse | Advanced | 90–120 s / 2–2.5 min / 2.5–3.5 min by map tier | ONCE | Act II §B7, §B8.2 |
| TSH-H1 | `S08`–`S09` | Great hall (TP17) | Node pulses only | Advanced | 4–6 min for five plates | STEP (stops forever) | Act II §B7 |
| TSW-E1 | `S01_whiteout` | Lee rocks below Iven's Post, C5 (Windscar high track) | 2 runner, howler (near-white) | Advanced | 40–60 s; 65–85% HP | STEP | Act III §7 |
| TSW-E2 | `S02_galleries` | G3 pull ledge (TP09) | 2 spear, hornman (skipped if line cut) | Advanced | 50–70 s; 60–80% HP | ONCE | Act III §7 |
| TSW-E3 | `S02_galleries` | G5 pull ledge (TP09) | As E2 (`reported`); unmanned (`seized`); 3 spear + hornman, new spearheads (`leverage`) | Advanced | 50–90 s by value | ONCE | Act III §7 |
| TSW-E4 | `S04_ingrith` | Winch floor H3 (TP09) | **Ingrith** + hornman; P2 +2 spear (+3 `leverage`) | Advanced | 5–7 min; ends 30–60% HP | ONCE | Act III §7.1 |
| TSW-E5 | `S05_wind`, `S06_hold` | Winch floor, far apron (TP09) | Hazards only | Advanced | ~3–4 min total | STEP | Act III §7 |

### 11.2 Side quests (committed packages)

| Id | Step | Place (POI) | Families / variants | Band | Solo target | Respawn | Source |
|---|---|---|---|---|---|---|---|
| TTH-E1 | Corner Stone beat | Corner Stone shoulder above TP26 | 2 runner, howler (+1) | Competent | 40–60 s; 60–80% HP | STEP | Horn TTH.7 |
| TWG-E1 | Tower 4 | Old Watchfire Line T4 (TP22) | 2 cutter, slinger (lookout; groove call +1 cutter) | Competent | 50–75 s; 60–80% HP | ONCE (hide stays empty) | Horn TWG.6 |
| TNR-E1 | Sheave tower | Nettlehook sheave platform (TP03) | Flock, 2 diver | Competent | 35–50 s; 70–90% HP | ONCE (crows return as ambient, no nest) | Horn TNR.6 |
| TSM-E1 | Hunt descent | Goat shoulder above Nettlehook (TP28 edge) | 3 runner (snatch), howler (+1) | Competent (late) | 55–80 s; 55–75% HP | STEP | Horn TSM.6 |
| TRR-E1 | After the knots (OPT) | Narrows meal ledge (TP07) | Flock (targets bread) | Advanced band, trivial | 20–30 s | ONCE | Horn TRR.6 |
| TSL-E1 | `S02_threads` (OPT) | Stormwake rut ground (plateau) | Rutting stag, 2 stag | Competent (late) | 60–75% HP if fought | → WORLD (rut ground) | Banner TSL 1.6 |
| TSL-E2 | `S05_traverse` | Splitpine Crag hawk ledge [NEW place] | 2 pairs storm hawks (fauna) | Competent (late) | Never fatal | → WORLD (hawks nest) | Banner TSL 1.6 |
| TWC-E1 | Camp investigation | Abandoned Ridge Camp (TP23) | 3 runner, howler (+2 in source; →+1†) | Competent (late) | 60–75% HP | → WORLD (den under the gate) | Banner TWC 2.6 |
| TWN-E1 | Stone ledge (OPT) | Shale under the stone ledge, Oath Cairn Fields (TP15) | 2 viper, shale-coil | Advanced | 75–90% HP | → WORLD | Banner TWN 3.6 |
| TSN-E1 | Morning after | Black Glass Hostel goat pen (TP05) | 2 runner (fight to 0 HP) | Competent (late) | 75–90% HP | STEP | Banner TSN 4.6 |
| TOS-E1 | Under the arch | Shale under Oathkeeper's Step (TP16) | 2 viper, shale-coil | Competent | 75–90% HP | ONCE (nest cleared) | Banner TOS 5.6 |
| TSR-E1 | Third sounding station | Red Slope scarp shale fan (TP21) | 2 viper, shale-coil (first-appearance tells) | Competent | 30–45 s | → WORLD | Work TSR.6 |
| TST-E1 | Below the second stand | Burned Slope foot (TP24) | 2 runner, howler (+1) | Competent | 45–60 s | → WORLD | Work TST.6 |
| TGY-E1/E2 | Warm stretch | Goat Ledges shoulder path (TP28) | Old ram; young ram (post-cull) | Competent | Not a fight | Fauna | Work TGY.6 |
| TBC-E1 | `S05_cross`, second window | Narrows Passwatch-side bridgehead (TP07) | cutter (prop: lead line), slinger | Competent | 40–60 s | STEP | Work TBC.6 |
| TAS-E1 | `S03_cramps` | Mule cache below the Blind Corners (TP26 edge) | 2 cutter, slinger | Competent | 45–70 s; 60–80% HP | ONCE | Settlements TAS.7 |
| TAS-E2 | `S03_cramps` return (OPT) | Road below Passwatch gate (TP02) | Howler, 2 runner (target mules) | Competent | 40–60 s | STEP | Settlements TAS.7 |
| TGM-E1 | `S02_track` | Kill cache G5, Stormwake (TP25 approach) | Howler, 2 runner; 4 crows | Competent (late) | 50–80 s | STEP | Settlements TGM.7 |
| TGM-E2 | `S04_fight` | Greymantle's Den inner chamber (TP25) | **Greymantle** | Competent (late)–Advanced | 3.5–4.5 min | ONCE (den prop by `TGM_OUTCOME`) | Settlements TGM.7.1 |
| TSG-E1 | `S02_works` | Salvage Ledge outer works (TP12) | 3 pick-hand, 2 plate-thrower | Advanced | 70–100 s | ONCE | Settlements TSG.7 |
| TSG-E2 | `S03_shed` | Plate shed (TP12) | **Brigand Foreman** + pick-hand | Advanced | 2–3 min | ONCE | Settlements TSG.7.1 |
| TSG-E3 | `S04_warn`/`S05_props` | Prop stones L6; thrower above L5 (TP12) | 2 pick-hand (cutters), plate-thrower | Advanced | 2–3 min total | ONCE | Settlements TSG.7 |

**No-combat quests (checked):** TNK (none), TMM (hazard only), TFS (hazard only), TME01–TME10 and TDS01–TDS10 (no encounters; TDS10 Gatefall is approached from the road with no hostiles before TF-M5).

### 11.3 World pockets and proposed elite placements [PROPOSAL — Gameplay Designer]

| Id | Place | Unlock / condition | Content | Band | Respawn |
|---|---|---|---|---|---|
| TW-01 Blind Corners bandits | TP26 switchbacks | After TF-M1 Completed | 1 cutter + 1 slinger, occasionally 2 + 1 | Competent | WORLD |
| TW-02 Muster Hut drill (`leverage` only) | TP27 | TF-M2 Completed with `TH_STORES = leverage`, until TF-M5 Completed | 2 spear, hornman; hires drill and flee if attacked | Competent | WORLD until TF-M5; then the hut is empty (splinter over) |
| TW-03 Whinstone Store guard (`leverage` only) | TP08 galleries | As TW-02 ("still filling: crew present; avoid or fight; no quest content", Act I §B10) | 2 spear, hornman per gallery visited | Competent | WORLD until TF-M5 |
| TW-04 **Pack-Mother** | Ridgewall high trail between Hushfold and the Old Watchfire Line (MAP VERIFICATION REQUIRED), off any quest path | After TF-M3 Completed; snow; dusk | Pack-Mother + 2 runner + howler | Advanced / post-arc | WORLD elite (long timer) |
| TW-05 **the Storm Stag** | Stormwake plateau rut ground (TSL area B), only in a storm presentation window | After TSL Completed | Storm Stag + 2 stag | Advanced / post-arc | WORLD elite (long timer); storm only |
| TW-06 Ridge bear | A second Stormwake cliff cave, not Greymantle's Den (MAP VERIFICATION REQUIRED) | After TGM Completed (either outcome) | 1 bear | Advanced / post-arc | WORLD (long timer) |
| TW-07 Shatterfall storm | `storm.shatterfall_world` (§10.2) | After TF-M3 Completed | 2 lanes echo-figures, echo-line | Advanced / post-arc | STORM |
| TW-08 Ridge wolves | Windscar high track, Ridgewall trails, Burned Slope | After TF-M1 | runner pairs, occasional howler | Competent | WORLD |
| TW-09 Crows | Summit outer stair, Whinstone K5 ledge, Nettlehook sheave tower | Any | Ambient flocks; Passive unless a nest is approached | Competent | WORLD |
| TW-10 Shale | Shatterfall L1–L2, Red Slope scarp, Oath Cairn stone ledge | Any | Vipers, shale-coil | Competent–Advanced | WORLD |

**Never after TF-M5:** Iron Winter crews (TW-02, TW-03 end). **Never anywhere:** a Horn-Echo figure outside Shatterfall; a node pulse outside the Summit great hall; any creature at the Gatefall after TF-M5.

---

## 12. Loot and drop notes

| Rule | Detail |
|---|---|
| **No new quest items** | The Thornfell budget is four (`TIW_store_ledger`, `TES_horn_roster`, `TSH_trial_record`, `TSW_closure_rubbing`); none comes from a creature. All four are picked up from places (desk, niche, bench, rubbed wall). |
| **Combat drops nothing evidentiary** | No chit, ledger page, roster leaf, sketch or tally is carried by an enemy. Pay chits (TES) are on a nail; the broadsheet is on a door. |
| **Defeated humans drop ordinary loot only** | Ordinary drops per the economy pass; nothing evidentiary. Ingrith (SX-3) drops nothing. Coin rewards in the packages still come from NPCs (peddlers' handcart, Aud, Gerrit, Elira's finder's share), not corpses. |
| **Plates are never loot** | TSG's plate crate is a carry-state object returned to the Horn Seat; Iron Winter plates follow `TH_HORN` and TNK. No player-held plate exists. |
| **Animals** | Ordinary materials (feathers, hides, antler, meat) are economy-pass items; ridge iron, stormwood and goat leather are **not catalog items** (TD-13). Greymantle's meat appears only through the TGM `ended` choice. |
| **Fauna** | Hunting yields only through Hunting interactions (snowhares, goats), never through combat kills in a quest step. |

---

## 13. Inconsistencies found and recommended canonical values

**Shared canonical register (canonical for implementation; quest packages defer to this register).** Added in the independent review of 2026-11-03. The three Batch 4 handoffs (Enemies, Zones, Integration) state these values in the same words. Where a quest package gives a different number, the package value is superseded for implementation; the package text changes only when its author next edits it.

| # | Topic | Canonical value |
|---|---|---|
| C-1 | Wind window | Fluted face whistles up a fifth **2.5 s** before a **3 s** gust. The gust pushes **2 m toward the defined safe side** with light damage, no knockdown, never off an edge; a marked shelter negates it. TF-M5 whiteout adds a 3 s slow; climbing stances keep "back to the last stance / hang on". One exception: TST stand-cutting gusts last ~6 s (a labelled "long gust"; same 2.5 s tell). |
| C-2 | Hazard clamp | No hazard can kill a player above **25% HP**; TSL-H2 stormlight clamps at **10%**. |
| C-3 | Hornman | Raise **1.5 s**; Gather gives allies within 8 m faster attacks for **8 s**; any hit during the raise interrupts; the player's **Rest within 3 s** cancels it in every hornman pocket. |
| C-4 | Howler and calls | Draw **1.5 s**; a completed howl adds **+1 runner once** (TPW-E3 keeps +2 as authored escort pressure). Any call blown at a howler makes it flinch; Fall also makes bandits duck once per fight. |
| C-5 | Ridge Wolves at low health | **Removed by CDR-1 (2026-11-03).** Wolves fight until defeated at 0 HP; no break-off, no limp-away. Step and co-op credit at defeat. |
| C-6 | Narrows bridge (TP07) | One per-player state machine, owned by the Zones package: **N0 down** (before TPW `S08_span`) → **N1 patched** → **N2 cracked only while TBC is Active** (overrides N1, N3 or N4 for that player) → **N3 mended** (TBC Completed) → **N4 permanent span** (TRR Active or Completed). Before TBC is accepted the bridge shows its ordinary state and TBC is offered by Aud's bark after a storm. The scree path is walkable in every state. |
| C-7 | Season and thaw | `TH_SEASON` has two values: autumn, then snow from TIW `S13_elira` start. Thaw is the quest-local bool `TSW_THAW` (first re-entry to Thornfell after TF-M5 Completed and leaving the region once) **[APPROVED — CDR 2026-11-03]**; no third `TH_SEASON` value. |
| C-8 | Ranged | **S01 resolved by CDR-2.** Ranged is a first-class option in every fight and is never required; every counter that names Ranged also has a melee, brace or call answer. No fight is designed so ranged trivialises it (no boss shootable from a place it cannot reach). TST teaches the bow (cut, string, fletch, shoot); the racked unstrung stave is only the bowyer's display piece. Weapon, ammunition and XP values belong to the item and systems specialists. |

| # | Inconsistency | Packages | Recommended canonical value |
|---|---|---|---|
| **I-1** | **Wind-window whistle lead time** varies: "about two breaths" (Act I), ~2.5 s (Act II, Act III, Ingrith), 1.5 s (Banner and Memory §0.3, TMM, TAS), ~3 s (Work and Skills TSR, TST, TBC). Gust length 3 s (Banner) vs ~6 s (TST S02). | All | **2.5 s tell, 3 s gust** everywhere (committed main acts; meets the 1.5 s displacement minimum with tick latency). TST's ~6 s gust is kept for TST stand-cutting only as a labelled "long gust" (C-1). Side files change the number only. **Canonical for implementation; quest packages defer to this register.** |
| **I-2** | **Gust effect** varies: push a step + light damage (TF-M1), push 2 m + slow 3 s (TF-M5), knockdown/stagger (Horn and Highsteads §0.6), pushed back to the last stance (TSL). | All | **Push 2 m toward the safe side, light damage, no knockdown.** TF-M5's slow 3 s stays as the whiteout upgrade. Climbing stances (TSL, TIW shaft) keep "back to the last stance / hang on". |
| **I-3** | **Hornman raise and Gather buff** differ: raise 1.5 s, faster thrusts 8 s (TIW); raise 2.0 s, +damage 15 s (TSH-E2); raise 1.2 s, faster attacks in 8 m for 8 s (TSW-E2; Ingrith's Close raise 1.2 s). | Act I, II, III | **Raise 1.5 s; allies in 8 m attack faster for 8 s.** TSH-E2 and TSW-E2/E4 change the numbers only. |
| **I-4** | **Rest-cancel** taught in TF-M2 is not restated for TSH-E2/E3 or TSW-E2/E3. | Act II, III | Rest within 3 s cancels every hornman Gather in every pocket. One line in each encounter table; no other change. |
| **I-5** | **Howler draw** 1.5 s (TPW, TTH, TSM, TAS, TGM, TSW) vs 2.0 s (TWC, TST); reinforcements +2 (TPW-E3, TWC-E1) vs +1 (others). | Act I; Horn; Banner; Work; Settlements | **1.5 s draw; +1 runner once.** TPW-E3's +2 kept as authored escort pressure (committed); TWC-E1 to +1. |
| **I-6** | **Wolves at low health**: flee at 30% (TSW-E1, TSN-E1), "disperse" (TTH, TSM), fight to defeat (TPW). Phase 1.3 says enemies never flee. | Act III; Banner; Horn; Act I | **Resolved (CDR-1, 2026-11-03):** wolves fight to 0 HP (C-5). Act III "Wolves flee", TSN "flee" and Horn and Highsteads "disperse" all become defeat at 0 HP; text changes only. |
| **I-7** | **Rock Vipers' first appearance**: bible §10 says TF-M3; TSR and TOS both unlock after TF-M1 and use vipers. TSR lengthens the viper tell to 1.6 s for "first appearance"; TOS uses 1.0 s. | Bible; Work TSR.6; Banner TOS 5.6 | **First appearance is TSR or TOS** (whichever the player takes first). Both use the **1.6 s** first-appearance viper tell; TES and TWN use 1.0 s. Bible §10 "First seen" should read "TSR / TOS (after TF-M1)". |
| **I-8** | **Shale-coil kit**: straight lunge 1.4 s (TES, TSR + slow) vs ring burst 1.5 s (TWN, TOS). | Act II; Work; Banner | Keep **both** as one kit (§5.3). Each pocket may use one or both; slow on the lunge is optional. |
| **I-9** | **Crow tells**: diver 0.8 s (TNR) vs 1.2 s (TIW, TSH); flock tighten 1.0 s (TIW-E1b, TSH-E1, TGM) vs 1.2 s (TNR, TRR); flock effect "accuracy debuff" (TSH) vs 2 m peck circle (TNR). | Act I, II; Horn; Settlements | **Diver 1.2 s; flock 1.2 s (area effect); 2 m peck circle, light damage; no accuracy debuff** (avoids a new status). |
| **I-10** | **Bleed** on `leverage` spearheads (TSW-E3) is a new status no other Thornfell creature uses. | Act III | Replace with **+damage** on the thrust and the bright-iron visual. If Systems already has a bleed, keep it. |
| **I-11** | **Pass bandit tells**: cutter 0.9 s (TPW, TAS) vs 1.0 s (TWG, TBC); slinger 1.2 s (TPW, TAS, TBC) vs 1.4 s (TWG). | Act I; Horn; Work; Settlements | **Cutter 1.0 s** (two moderate hits); **slinger 1.2 s**. |
| **I-12** | **Hazard lethality clamp** varies: "cannot kill above a quarter health" (TSR, TST), "never lethal at full health" (TSW Fall), 10% clamp (TSL-H2), unstated elsewhere. | Act III; Work; Banner | **Cannot kill above 25% HP** for every hazard (Lowmark rule); TSL-H2 keeps its stronger 10% clamp. |
| **I-13** | **Charge minimums**: rutting stag 1.4 s (TSL-E1), old ram stamp 1.2 s (TGY-E1) are displacement attacks below the 1.5 s minimum. | Banner; Work | **1.5 s** for both. |
| **I-14** | **Runner lunge** 0.8 s (TPW, TSW, TAS, TGM, TWC, TSN) vs 0.9 s (TTH, TSM) vs 1.0 s (TST). | All | **0.9 s** (light, with tick latency). Changes are numbers only. |
| **I-15** | **Iron Winter elite slot** is Ingrith, who is the Act III boss; Phase 1.5 counts bosses separately (same issue as Lowmark I-13). | Bible §10 | Count Ingrith as the boss only; the family has **no separate elite** (2 variants). The TIW crew boss stays a sub-form. Total stays 21 with the three proposed placements. |
| **I-16** | **Greymantle** is listed as the Ridge Bears' elite and as a side miniboss. | Bible §10 | Count as the miniboss; the elite slot is filled by it (like the Held Line for Horn-Echo). |
| **I-17** | **Unplaced variants**: Pack-Mother, the Storm Stag, the standard ridge bear. | Bible §10 | World placements TW-04, TW-05, TW-06 (§11.3), or cut Pack-Mother and Storm Stag (count 19). |
| **I-18** | **Ridge Crows' first appearance**: bible says "TF-M2 vents"; the ledge route (TIW-E1b) comes earlier in TF-M2. | Bible; Act I | "First seen: TF-M2" (either route). Text only. |
| **I-19** | **Yield threshold** default not stated for the Corner-Boss; Horn and Highsteads says humans yield "at 0 HP". | Act I; Horn | **Resolved (CDR-1):** no yield thresholds; every human, the Corner-Boss, the Foreman and Ingrith included, is defeated at 0 HP (§8). Ingrith's SX-3 outcome plays on defeat. |
| **I-20** | **Fall as a startle** works on howlers (TTH, TSM) and bandits (TWG) but not in TF-M1's wolves (any call makes the howler flinch). | Act I; Horn | Both true: **any call** makes a howler flinch; **Fall** additionally makes bandits duck once per fight. |
| **I-21** | **Ridge Crows "not used" in TSL** "because they belong to the vents of TF-M2", while TSH, TNR, TRR and TGM use crows. | Banner TSL 1.6 rules | Harmless; crows are a ridge-wide family. Recommend deleting the reason clause in TSL's rule. |

---

## 14. Director-level questions

1. ~~Wolves break off at 30% (I-6)~~ **Resolved 2026-11-03 (CDR-1):** wolves fight to 0 HP.
2. **World elites (I-17):** place Pack-Mother, the Storm Stag and a standard ridge bear as proposed, or cut the two elites?
3. **Post-story Shatterfall storm (§10.2 `storm.shatterfall_world`):** approve the revisitable storm event without the Held Line or the uphill group?
4. **Greymantle UI mute (TGM-OD1):** mute UI sounds inside the null-point as well as world audio?
5. **Count (I-15, I-16):** approve Ingrith as boss-only and Greymantle/Held Line as the high-tier slot fillers?

## 15. Hand-offs (documented dependencies; nothing implemented)

| To | What |
|---|---|
| Schema & Content Engineer (33.7) | Creature definitions for 21 variants + 3 bosses/minibosses + sub-forms (crew boss, uphill group presentation) + fauna (storm hawks, old and young ram, goats, snowhares); pocket data from §11; hazard ids including the [NEW id]s in §9 |
| Systems Engineer | Standard defeat at 0 HP (the §8 yield mechanism is removed); quest on-defeat hook for named creatures (Ingrith SX-3, TSG Foreman step trigger); §9.4 status list; call events, Rest-cancel and interrupt-on-windup; lane dispersal and storm windows; node pulse with pressure-shadow volumes; audio-null volumes; push-to-safe-side clamp |
| Animation / VFX / Audio | §3 telegraph grammar and canonical tells; whistle a fifth up at 2.5 s; visual-only Greymantle set; blank echo-figure presentation |
| Level design (Zones file) | Arenas (winch floor, seat approach, great hall, G9 den, plate shed), shelter faces and niches, edge blockers, echo faces, horn rests |
| Side-quest authors | Number-only changes from I-1, I-2, I-5, I-7, I-9, I-11, I-13, I-14; TSL rule clause (I-21) |
| Bible owner | §10 "First seen" for Rock Vipers (I-7) and Ridge Crows (I-18) |

## 16. Review log

| Check | Result |
|---|---|
| Coverage | Every encounter and hazard id in the three main acts and four side-quest files is in §9 or §11; quests with no combat are listed. Nine families, 21 variants, 3 bosses/minibosses, fauna. |
| Binding rules | Summit node is a passive hazard with no health, frame, name, AI or voice (§9.2). Horn-Echo never identifies anyone and stays at Shatterfall (§10). Every enemy is defeated at 0 HP; Ingrith SX-3 is the only scripted surrender (§8, CDR-1). Combat reveals nothing; no new quest items (§12). No resonance at the Gatefall. No Remnant, no magic, no player spellcasting. |
| Click-to-move | No counter needs a jump or timed input; every arena shortcut has a walkable fallback; every push is clamped to a safe side. |
| Telegraph minimums | After §13 reconciliation, every tell meets 0.8 / 1.0 / 1.5 s. |
| Splinter tagging | Ingrith, Bersi and Eyvind entries tagged `[SPLINTER]`. |
| Scope | No schema, JSON or C#; integration needs are documented only. |
| Name changes (2026-11-03) | This file names no roster or name-slip family; the review-pass renames (the name-slip "Sig Brede", the roster's Lunde family, the Tofte carters) need no edit here. |
| **Reconciliation needed** | The four side-quest files were under independent review while this file was written. **After those reviews land, re-check every side-quest row in §9 and §11.2 and inconsistencies I-1, I-2, I-5 to I-9, I-11 to I-14, I-19 to I-21 against the revised text.** The main-act rows reflect the committed packages. |
| **Independent review (2026-11-03)** | 5 findings (0 high, 3 medium, 2 low). Grep checks against the committed packages: every encounter id in §9 and §11 exists in its package (hazard ids absent from packages are all marked [NEW id]); every flag named exists; the four quest items match; no stale names (this file names no renamed NPC). Medium: the three handoffs disagreed on wind-window, howler, hornman and hazard-clamp values and on the Narrows bridge and thaw models; the shared canonical register C-1 to C-8 (§13) now states them identically in all three, marked canonical for implementation. Medium: I-1 left TST's gust undecided; now 3 s everywhere with TST's ~6 s kept as a labelled long gust. Medium: Ranged appeared as a counter (diver, howler, storm hawks) without the S01 gate; now optional "if S01 allows" (C-8). Low: I-6 restated as the canonical rule "break-off counts as defeat" [PROPOSAL — DIRECTOR] (C-5). Low: source-state lines and §7.3, §7.4, §11.2 headings still said "in review"; updated to committed. Binding rules re-checked: Summit node passive; Horn-Echo never identifies; humans yield; no Remnant; no grain route; walkable fallbacks; no scope expansion; no contract change. The reconciliation row above is closed by this review. |
| **Director rulings reconciliation (2026-11-03)** | Applied CDR-1..3 (`Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`). §8 rewritten as defeat at 0 HP (TD-7 superseded); per-family Defeat/loot rows replace Yield/loot (bandits, Iron Winter crews, brigands, Foreman 20% → 0 HP); wolf break-off removed (AI role, Pack-Mother rally, C-5, I-6, TSN-E1); Ingrith §7.1 defeat at 0 HP with the SX-3 scripted surrender on defeat, crew fight to 0 HP; Greymantle 10% lie-down removed, S06 reframed (seal the den / leave him to the trappers; flags unchanged); Foreman TSG S04–S05 start on his defeat; crows and hawks defeated at 0 HP (TGM-E1 "scatter when the wolves are down" removed; hawks no longer "driven off"); C-7 thaw approved; C-8 and every "if S01 allows" hedge → Ranged first-class, never required; I-19 and §14 Q1 resolved; runtime yield mechanism removed, quest on-defeat hook named; pointer to the engineering handoff. Earlier rows in this log describe past states. |
