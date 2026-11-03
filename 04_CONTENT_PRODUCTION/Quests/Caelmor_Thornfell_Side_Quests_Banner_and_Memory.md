# Thornfell Side Quests — Banner and Memory

**Status (2026-11-02):** Authored production content for Creative Director review (Thornfell bible §12, batch 3). Five side quests from `Caelmor_Thornfell_Narrative_Production_Bible.md` §7.1–7.2. Everything here is **[NEW]** unless marked **[CANON]** or **[APPROVED — id]**; consequential story choices are marked **[PROPOSAL — DIRECTOR]**. This file authorizes no release scope and creates no schema, JSON or C#. Format follows `Caelmor_Lowmark_Side_Quests_Discovery_and_Memory.md`: each package carries its own cast notes, dialogue, barks, inspect texts and documents inline. Every package declares the five quest contribution-contract fields (Review §7.1) in its summary card.

**Covers:** the series *The Banner and the Ridge*: **TSL** *Stormlight on the Ridge* (1/2) and **TWC** *Whose Colours* (2/2); the Register of the Unreturned, Thornfell case: **TWN** *The Weight of a Name*; memory/lore **TSN** *The Snow-Height Mark*; environmental **TOS** *Oathkeeper's Step*.

**Canon hooks used:** dossier §V (Stormwake Plateau, Oath Cairn Fields, Ridgewall Heights), §X (storm hawks, fell stags, ridge wolves, rock vipers, stormflower, cairn moss), §XII (Lost Banner of Thornfell, Oathkeeper's Step, the Ridgewalker), §XX (Blood-Oath red-dyed banners and broken-horn motifs; Hearthguard mountain-flower motifs and Crestbridge wool cloaks; Ridge Warden rope and spikes; Cairn-Keepers); Thornfell anchors (Brynjar Korr, Elira Hearthward, Old Torvek, Hadrik Stonewake, Maera Cairnwatch, Kaldren Deepdelver, Iven Ridgeborne) under the Part 4 character ledger limits; Part 3 Thornfell proposal (Black Glass Hostel and its no-colours rule, the erased snow-height mark, Hushfold, *The Weight of a Name*, Maera's temporary-name practice); World Truth H16 [APPROVED — FT-02b] and H23; Revelation Ledger R06 and R14.

**Binding limits honoured throughout:** no Thornfell voice calls anything magic and no player casts anything; phenomena never identify a person, prove anything or settle a claim; combat never reveals evidence; defeated humans yield (TD-7; no human enemies appear in this file); no Remnant presence; no statement of how Lowmark grain reached Thornfell (this file does not mention the grain); quests are only Inactive, Active or Completed; no node names Ingrith, Bersi or Eyvind, so no node carries `[SPLINTER]`.

---

## 0. Shared rules for this file

### 0.1 Unlock gates

| Code | Suggested content id | Unlock | How it is offered | Later gate / variant |
|---|---|---|---|---|
| TSL | `thornfell.side.stormlight_on_the_ridge` | TF-M2 Completed (`TH_SEASON` = snow) | Iven Ridgeborne at the Stormwake warden shelter (bark on approach: "Colour on the crag again. Third flash."); or the TDS08 Lost Banner glimpse on the plateau in any storm window, which points the player to Iven. | — |
| TWC | `thornfell.side.whose_colours` | TSL Completed | Automatic: TSL ends at the Assembly Hall door, where Brynjar and Elira are both waiting. | Brynjar's lines read `TH_BRYNJAR` (always set by TF-M2). |
| TWN | `thornfell.side.weight_of_a_name` | TF-M3 Completed (`TES_horn_roster` exists; `TH_SHATTERFALL_ACCOUNT` set) | Runa Weatherall at Hushfold: "Orm wants to ask you something and won't." Or inspect the name-slip rows at Maera's Name-Stone Wall. | Variant lines if TF-M5 Completed first (§3.13). |
| TSN | `thornfell.side.snow_height_mark` | TF-M2 Completed (`TH_SEASON` = snow) | Enter Black Glass Hostel in a storm window, or Halla Quern's bark at the hostel door: "Door shuts at the drift. In or out, walker." | Optional epilogue at Nettlehook (§4.5). |
| TOS | `thornfell.side.oathkeepers_step` | TF-M1 Completed | Enter the oath-path volume in the Oath Cairn Fields: the path-warden and the young couple are arguing at a rope he is trying to tie across the path. | — |

None of these quests is required by any milestone. TWC sets the region flag `TH_BANNER` (bible §9.1), read by the TF-M5 Assembly placement (§9.3). All other outcomes are quest-local flags.

### 0.2 Discovery and memory philosophy (Thornfell)

1. **Reward attention, never demand it.** Every strange thing has an invitation in the place: a colour seen only in lightning, threads in the wrong part of a plateau, a step with no wear-hollow, a scrape on a doorpost, a phrase that means two things. Missing a detail costs colour, never progress.
2. **Nothing optional solves a main mystery.** These quests do not explain the Ridgewalker, the Echohewn, the null-points, or why some voices carry in the Assembly Hall. Each package's mystery ledger states what it cannot prove.
3. **The strange moment belongs to the player.** No camera takeover, no explanatory text, no music sting. The world does something; a person reacts, or pointedly does not.
4. **Evidence rule.** Records, objects, places and testimony do the proving: stitching and a bunk-board (TWC), a horn roster and a rim cairn (TWN), a daybook and a scraped post (TSN), a soffit and an echo count (TOS). Stormlight, snow in new-cut letters, a turning cord and a quiet step prove nothing and name no one.
5. **The place stays useful.** The crag is still climbable, the camp is still a camp, the wall still takes slips, the hostel still shuts at the drift, the oath path still carries oaths.

### 0.3 Conventions

- **Steps** are scoped by quest code (`TSL` `S00_offer` is distinct from `TWC` `S00_offer`). **Flags** use the quest code prefix. The only region flag set here is `TH_BANNER` (TWC). Region flags read: `TH_SEASON`, `TH_BRYNJAR`, `TH_SHATTERFALL_ACCOUNT`, `TH_CALLS`.
- **Quest items: none added.** TWN **reads** TF-M3's quest item `TES_horn_roster` in place, wherever `TH_SHATTERFALL_ACCOUNT` left it; the player never carries it. All other objects are carry states (the rolled banner, the colour on its walking staff, the cut stone) or placed props. This file adds **0** to the Thornfell quest-item budget (bible §9.5).
- **Dialogue** uses the Lowmark format: node ids `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>`, optional talks `<CODE>-L-<NAME>`; `[condition]` before a line, `{effect}` after it; player options as `>` lines. Addressing is origin-neutral: "walker" for strangers (bible §5.3 rule 4).
- **Storm windows** reuse the Lowmark keep-watch convention (bible §9.5): a named **wait** interaction (a shelter bench, a hearth) advances a per-player presentation hour into a storm or a drift, never world time. Partners in co-op see their own state; fallback: the host's.
- **Wind windows** follow the single Thornfell convention: the fluted-face whistle rises a fifth about **1.5 s** before a gust; a gust lasts about **3 s**; a marked lee (a face, a notch, a cairn) is always safe.
- **Calls glyphs:** where an Ordinary Call sounds and `TH_CALLS` is set, its glyph shows (bible §9.4). TOS can unlock before the player learned them only if TF-M1 is skipped, which it cannot be (TOS requires TF-M1), so glyphs are always available here.
- **Death:** respawn at the package's named safe point with step, flags and carried state restored to the last deposit; a dropped carry returns to its pickup point. No quest here can fail.
- **Co-op:** independent quest instances; shared fauna gives step credit to every participant on that step; step-conditioned props and strange moments are presented per player from their own state, with the fallback named in each package.

### 0.4 How the five quests touch each other (all optional links)

| From | To | Link | If missing |
|---|---|---|---|
| TSL | TWC | The banner TSL brings down is the object TWC disputes. | TWC cannot start without TSL (gate). |
| TWC | TWN | The plain shelter-line knot (TWC) and the knot on Sig Brede's tally-stick thong (TWN) are the same knot. Inspect variant only. | Each inspect stands alone. |
| TWC | TF-M5 | `TH_BANNER` adjusts Assembly posture and Brynjar's and Torvek's placement (bible §9.3). | Neutral. |
| TWN | TF-M5 | Act III's `TSW-D9.51` reads TWN Completed (already authored; §3.13). | No change to TF-M5. |
| TOS | TWN | The oath path is the route up to the Name-Stone Wall's upper field. Repaired in TOS; walkable either way. | Approach by the long cairn path. |
| TSN | — | Self-contained. | — |

---

## 1. TSL — Stormlight on the Ridge

### 1.1 In one paragraph

Every storm since first snow, Iven Ridgeborne has watched colour show on a crag above the Stormwake Plateau: never in daylight, only on the third flash, red where nothing is red. The highsteads call it the Lost Banner of Thornfell, carried into a storm in the war and never returned, and a Blood-Oath boy has already sprained a wrist trying to fetch it. Iven reports it the way he reports everything: crag, flash, direction, nothing else. The player waits out a storm at the warden shelter and sees it. Then they track it the hard way: the storm is tearing the banner apart, and its threads blow downwind across the plateau, snagged on lightning-scarred stone and twisted trees; following them upwind leads past a rutting stag to the foot of **Splitpine Crag**. The climb is three pitches in wind windows, a traverse under nesting storm hawks that dive at anything on their ledge, and a summit block where the iron starts to hum before lightning. Wound round the split pine at the top is a real banner, shredded to a third of its size, its staff driven into a crack as a rally mark. As the player cuts the last lashing, the staff's iron head and the spikes on the player's own boots glow blue and hiss in the storm. That is the stormlight: what the highsteads have been seeing. The player lowers the banner to Iven, decides whether the staff stays on the crag, and walks the colour into Stonewake, where two clans are already waiting to claim it.

**What the player should remember:** their own climbing spikes glowing blue on a crag top, the banner going quiet in their hands. **What they might want next:** to know whose it was (TWC).

### 1.2 Summary card

| Field | Value |
|---|---|
| Type | Environmental climb (Phase 1.5 environmental discovery). Series *The Banner and the Ridge* (1/2). Dossier §XII "Lost Banner of Thornfell" [CANON myth]; TDS08 glimpses. |
| Unlock | TF-M2 Completed (`TH_SEASON` = snow). |
| Length | 30–40 minutes. |
| Core verb | **track, climb, recover**. Identity: tracking by wind-carried evidence, a three-pitch climb in wind windows, a lightning hazard read by sound. |
| Combat | ~15%, secondary: an avoidable fell-stag rut on the plateau; storm-hawk harassment on the traverse (fauna; driven off, not required to kill). |
| Skills | None required. Melee optional (strike a landed hawk); Ranged only if S01 allows. |
| NPCs | Iven Ridgeborne [CANON anchor]; Kol Hask, Blood-Oath boy (minor) [NEW]; Brynjar Korr and Elira Hearthward (closing beat, hand-off to TWC). |
| Choice | Does the staff stay on the crag? (2 options) |
| Unlocks | TWC; Splitpine Crag viewpoint and a fixed warden line (per player); Iven's stormwatch bench. |
| **Anchor** | Ridge Wardens (Iven's high-path watch) and the Stormwake Plateau. |
| **World-truth row** | H16 (late-war retreats across the high country) as background only; nothing dated. |
| **Revelation role** | Self-contained. Feeds TWC (local). Plants nothing cross-region. |
| **Recurring evidence** | The banner recurs in TWC (custodian after TSL: Torvek, by Hadrik's word). |
| **State compliance** | Inactive/Active/Completed. Storm windows wait on the player; the climb cannot be failed (falls return the player to the last stance). Choice recorded as quest-local `TSL_STAFF_LEFT` / `TSL_STAFF_TAKEN`. |

### 1.3 Canon grounding

| Element | Source | Use here |
|---|---|---|
| Lost Banner "carried into a storm and never returned; sometimes glimpsed fluttering on impossible ridges" | Dossier §XII [CANON myth] | The banner is real; the "impossible ridge" is a hard crag; the glimpses are stormlight. |
| Stormwake Plateau: frequent storms, lightning-scarred stones, twisted trees | Dossier §V.5 [CANON] | Tracking ground and wind lees. |
| Storm hawks ride updrafts; fell stags | Dossier §X [CANON]; bible §10 (storm hawks are fauna; fell stags are a Stormwake family) | TSL-E1, TSL-E2. |
| Red-dyed banners, broken-horn motif (Blood-Oath); mountain-flower motif (Hearthguard) | Dossier §XX [CANON] | The banner's field and its hem (read properly in TWC). |
| Ridge Wardens carry horns, rope coils, climbing spikes | Dossier §XX [CANON] | The fixed line; the spikes that glow. |
| Iven: high-path scout; reports direction, weather, timing before interpretation | Anchors VI; Part 4 ledger | Every Iven line is a report. |
| The Ridgewalker: seen only from Stormwake in a great storm; never explained | Bible TDS07 [CANON myth; never explained] | Optional view-dependent glimpse (§1.7); never commented on beyond a report. |

### 1.4 The places

**MAP VERIFICATION REQUIRED:** the shelter must have a sightline to the crag's summit block; the thread trail must cross open plateau between the shelter and the crag foot; the further ridge for the optional Ridgewalker glimpse must be visible from the summit block only. No compass bearing is stated anywhere.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Stormwake warden shelter** | Offer; storm wait; safe point. | A stone hut with a turf roof and a horn hook. Iven's stormwatch bench faces the crag through a slot. On the door frame, a column of chalked marks: one per storm, each with a small **3** beside it. A boy's broken climbing spike lies on the bench, bent at the tang. |
| **B. Open plateau** | Tracking. | Lightning-scarred standing stones (each with a black seam down one face), twisted trees bent all one way. In storm windows, threads snag on both. The fell-stag rut ground is a trampled hollow with antler-scored turf. |
| **C. Crag foot** | Start of the climb. | Scree, a cold spring, old iron pegs in the first crack (very old, square-cut), new boot-nail scratches (Kol's). A goat ramp curls left. |
| **D. Pitch one: the chimney** (agility) / **the goat ramp and first warden ring** (walkable) | Ascent. | The chimney is fast and enclosed. The ramp is long and exposed; at its top, an old iron ring in the rock where a warden line can be clipped. |
| **E. Pitch two: the hawk ledge traverse** | Harassment. | A ledge a boot and a half wide along a fluted face. Two hawk nests in the overhang, white-streaked rock beneath, small bones. The flutes whistle before gusts. |
| **F. Pitch three: the summit block** | Lightning hazard. | A bare block crowned by a lightning-split pine, half of it dead and silver, half still green. A lee notch on the downwind side, marked by an old cairn of three stones. |
| **G. The banner** | Recovery. | Wound three times round the living half of the pine, lashed with old rope and new frayed strands; its staff driven into a crack in the block, iron head uppermost. Red faded to rust in the folds, still red inside them. |

### 1.5 Beats

**Beat 0 — Third flash (`S00_offer`).** *Objective: Ask Iven about the colour on the crag.* At the shelter, Iven (TSL-D1) and, on the bench, Kol Hask with his wrist strapped (TSL-L-KOL, optional). Iven reports the sightings and offers his bench.

**Beat 1 — Wait for weather (`S01_glimpse`).** *Objective: Watch the crag in a storm.* Interaction **Keep stormwatch** at Iven's bench (cancellable channel; advances the player's presentation hour into a storm window). Lightning flashes at readable intervals. On the third flash, colour shows on the crag (§1.7 part 1). Iven: "There." The step completes on the third flash whether or not the player was looking; Iven names the place, so the step cannot be missed.

**Beat 2 — Follow the threads (`S02_threads`).** *Objective: Follow what the wind is carrying.* The storm stays up while the step is active. Three **thread** props on the plateau (snagged on a scarred stone, a twisted tree, a cairn), each in a different colour: **red wool**, **blue wool**, **undyed goat-hair**. Each inspect states which way the frayed end points ("the frayed end points downwind; the cut end, back the way it came"). The player walks upwind from thread to thread. The rut ground (TSL-E1) lies across the direct line; it can be skirted along the scarred stones. Inspecting the third thread completes the step and reveals the crag foot.

**Beat 3 — Someone tried (`S03_crag_foot`).** *Objective: Find a way up the crag.* Inspects: **old pegs** (square-cut, very old), **new scratches** (fresh, one set, going up and then very quickly coming down). Iven arrives by the goat ramp (he does not climb the crag) and offers the warden line (TSL-D2).

**Beat 4 — Pitch one (`S04_pitch_one`).** *Objective: Climb to the hawk ledge.* **Agility route:** the chimney (three climb triggers). **Walkable route:** the goat ramp to the first warden ring, then **Clip and climb the line** (4 s channel) to the ledge. Both routes are under wind windows on their exposed parts.

**Beat 5 — The hawk ledge (`S05_traverse`).** *Objective: Cross the hawk ledge.* The traverse is four stances long. Storm hawks dive at the player (TSL-E2). The player braces on the shriek and moves between dives. Optional: striking a landed hawk twice (or, if S01 allows Ranged, two hits from the ledge start) drives it off; it circles away and does not return this visit. Bracing alone always gets the player across.

**Beat 6 — The summit block (`S06_summit`).** *Objective: Reach the pine.* Short climb in wind windows. Here the iron starts to hum (TSL-H2): a rising buzz from the player's spikes and the staff head before each strike near the block; shelter in the lee notch until it passes. The pine and the banner are reached when the player enters the summit volume.

**Beat 7 — Cut it free (`S07_free`) — the strange moment.** *Objective: Free the banner from the pine.* Three lashings, each **Cut lashing** (3 s channel) between gusts and hum. On the last cut, the stormlight takes the staff head and the player's spikes (§1.7 part 2). Then **Roll the banner** (3 s).

**Beat 8 — Send it down (`S08_lower`).** *Objective: Lower the banner to Iven.* **Lower the roll** (3 s) on the warden line from the summit ring. Iven's voice from below: "Got it. Lighter than it looks." No carrying on the climb.

**Beat 9 — The staff (`S09_staff`).** *Objective: Decide about the staff.* Inspect the staff: driven into the crack by someone who meant it to stay. Choose **Work it free** (3 s) or **Leave it standing** (interaction on the staff, instant). See §1.10.

**Beat 10 — Down (`S10_descend`).** *Objective: Climb down to Iven.* Reverse route; the descent is the line for everyone (rappel interaction at the summit ring: 4 s channel, lands at the crag foot). Optional: the further ridge glimpse (§1.7 part 3) is available from the summit block before descending.

**Beat 11 — Into Stonewake (`S11_stonewake`).** *Objective: Bring the banner to Stonewake.* Iven carries the roll; the player walks with him (no escort logic: Iven is placed at Stonewake when the player enters the hall terrace volume). At the Assembly Hall door, Brynjar and Elira are both waiting; word travels faster than wardens (TSL-D6). Quest Completed on TSL-D6 end; TWC becomes Active.

### 1.6 Encounters and hazards

| Id | Enemies / hazard | Placement | AI role | Telegraph (timings) | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TSL-E1** | 1 × rutting stag, 2 × fell stag (Fell Stags family) | Rut ground on the direct thread line (area B) | Rutting stag charges in straight lines; stags hold and flank only if the player enters the hollow. Leashed to the hollow (about 30 m). | Rutting stag paws twice and lowers its head (**1.4 s**), then a straight charge; a bellow (**1.0 s**) turns the two stags toward the player. | Plateau danger while reading threads; teaches that the plateau is open and that going round is a choice. | **Optional.** Skirting via the scarred stones avoids it. If fought, ends at 60–75% HP on a late Competent-identity character (bible TD-12); stags disengage at the leash. |
| **TSL-E2** | 2 pairs of storm hawks (fauna; bible §10) | Overhang nests above the hawk ledge (area E) | Harassment: one hawk dives at a time on a 6–8 s cycle; after a dive it lands on the ledge lip for **2 s** before lifting. | Shriek, then the hawk's shadow sweeps across the rock (**1.2 s**) before the dive. **Brace** (one input; click the rock for click-to-move) negates the knock-back. | Rhythm on the traverse: move between dives, brace on the shriek. | Never fatal. An un-braced dive knocks the player back one stance (no fall). Striking a landed hawk twice, or two Ranged hits from the ledge start, drives that hawk off for the visit. Killing is possible (fauna) and not required. |
| **TSL-H1** | Wind windows | Plateau, ramp, ledge, summit block | Environmental. | Flute whistle rises a fifth (**1.5 s**), gust (**3 s**). | Pace the exposed moves. | In the open during a gust: pushed back to the last stance; never off the crag. |
| **TSL-H2** | Stormlight (lightning near the block) | Summit block only, during the storm window | Environmental. | A rising buzz from iron (the player's spikes, the staff head) with a faint blue flicker on gear, **2.5 s** before a strike within the block volume. | Teaches "when the iron sings, get low". | In the lee notch: safe. Outside it: knockdown and moderate damage, clamped so it cannot drop the player below 10% HP. Never fatal. |

**Rules.** Nothing dropped by stags or hawks advances the quest. Respawn point: the warden shelter (area A), with steps kept; on respawn after S04, the warden line is already clipped, so the player can line-climb straight back to their last pitch. Ridge Crows are not used here (they belong to the vents of TF-M2).

### 1.7 The strange moments: presentation spec

**Part 1 — The glimpse (S01, from the shelter).**

| Element | Spec |
|---|---|
| Trigger | Third lightning flash of the stormwatch (server event `tsl.flash3`). |
| What shows | For the length of the flash (~0.4 s), a small ragged shape of red stands out on the crag top, held out stiff by the wind. Between flashes the crag is grey and the shape cannot be seen. |
| After | On later flashes the colour shows again faintly. A thin blue point of light shows at the crag top on some flashes, too small to be sure of. |
| Audio | Storm, thunder after a count (the player can count it). Iven says "There." and nothing else until the flash fades. |
| UI | Objective update only after the flash. |

**Part 2 — Stormlight (S07, on the summit block).**

| Element | Spec |
|---|---|
| Trigger | The third **Cut lashing** completes (server event `tsl.stormlight`). The storm window is guaranteed active on the summit while S07 is active. |
| Duration | ~10 s. |
| What it shows | The staff's iron head begins to glow a pale blue at its point, with a soft hissing crackle. The same pale glow gathers on the player's climbing spikes, then on any metal they wear. Loose banner threads lift and stand out from the cloth, though the wind has just dropped. The player's hair (or hood edge) lifts. |
| Audio | A thin, steady hiss; the storm's roar seems further away. No music. When it ends, a crack of thunder somewhere off the block, not on it. |
| Hazard link | This is **not** a TSL-H2 strike: the buzz does not rise and no strike follows. It is presented the same way so the player understands that the hum and the glow are one family of thing. |
| UI / camera | None / player-controlled. |
| After | Staff inspect: *"The iron is warm. It shouldn't be."* Iven, at the bottom (TSL-D4), reports what he saw from below: blue on the top, three flashes long. |
| What it means | Nothing the quest states. Nobody calls it anything but **stormlight**. The glimpses were real colour lit by real weather. |

**Part 3 — The further ridge (optional, from the summit block before S10).**

| Element | Spec |
|---|---|
| Trigger | Client-side and view-dependent: the camera faces the further ridge during a flash while the player is in the summit volume after S07. Once per storm window. |
| What shows | For one flash, a tall upright shape on the further ridge's crest, too far to be sure is not a stone. On the next flash, nothing there. |
| Audio / UI | None special. |
| Reaction | If seen (client reports `tsl.ridge_seen`), Iven's TSL-D4 adds one report line. Never explained; never named in UI. This is TDS07, not a quest element. |

### 1.8 Steps

| Step | Objective | Completes on | Required |
|---|---|---|---|
| `S00_offer` | Ask Iven about the colour on the crag. | Enter shelter volume → TSL-D1 end | Yes |
| `S01_glimpse` | Watch the crag in a storm. | `keep_stormwatch` reaches `tsl.flash3` | Yes |
| `S02_threads` | Follow what the wind is carrying. | 3 thread inspects (any order; the third reveals the crag foot) | Yes |
| `S02b_rut` | (Optional) Deal with the rut. | TSL-E1 disengaged or defeated | No |
| `S03_crag_foot` | Find a way up the crag. | 2 inspects (pegs, scratches) + TSL-D2 end | Yes |
| `S04_pitch_one` | Climb to the hawk ledge. | Enter ledge-start volume (either route) | Yes |
| `S05_traverse` | Cross the hawk ledge. | Enter ledge-end volume | Yes |
| `S06_summit` | Reach the pine. | Enter summit volume | Yes |
| `S07_free` | Free the banner from the pine. | 3 × `cut_lashing` + `roll_banner` (fires `tsl.stormlight` on the third cut) | Yes |
| `S08_lower` | Lower the banner to Iven. | `lower_roll` complete | Yes |
| `S09_staff` | Decide about the staff. | `work_staff_free` or `leave_staff` | Yes |
| `S10_descend` | Climb down to Iven. | Enter crag-foot volume → TSL-D4 end | Yes |
| `S11_stonewake` | Bring the banner to Stonewake. | Enter Assembly Hall terrace volume → TSL-D6 end → Completed; TWC Active | Yes |

Each channelled interaction keeps its progress if interrupted by a gust, hum or dive.

### 1.9 Flags

| Flag | Set by | Read by |
|---|---|---|
| `TSL_KOL_HEARD` | TSL-L-KOL end | TSL-D6 (Brynjar's line about Kol) |
| `TSL_RIDGE_SEEN` | `tsl.ridge_seen` | TSL-D4 extra report line |
| `TSL_STAFF_LEFT` / `TSL_STAFF_TAKEN` | `S09_staff` (exactly one) | Crag prop (per player); TWC-D1 variant; TWC rite (which staff carries the colour) |
| `TSL_COMPLETE` | Completion | TWC unlock |

### 1.10 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Leave it standing** — *"It was put there to stay. Leave it."* | The staff stays in the crack, bare. | TWC's rite needs a new staff (Elira's storekeepers cut one; TWC-D1 line). The Blood-Oath bloods grumble that the "horn-iron" was left on a rock. | The crag top keeps its iron. In later storms at Stormwake, a blue point still shows on the crag on some flashes (ambient; per player). Iven: "Still there. Good. Something should be." |
| **Work it free** — *"Bring it down with the colour."* | Two more channel segments (3 s each) between gusts; the staff is lowered on the line after the roll. | The crag loses its mark; storm glimpses stop for this player. Iven says nothing about it, which is his way of minding. | TWC's rite uses the old staff (TWC-D1 variant); Brynjar's line about "horn-iron coming home". |

Neither option is wrong. The banner comes down either way.

### 1.11 Rewards

| Reward | Type | Notes |
|---|---|---|
| **Splitpine Crag fixed line** | Access | The warden line stays clipped for this player: a fast line-climb to the summit viewpoint. |
| **Iven's stormwatch bench** | Place | A rest spot; sitting there in any storm window shows the crag (with or without the blue point, per `TSL_STAFF_*`). |
| **Warden's spike straps** | Tool | Functional name; no stat promised (item pass to derive). Iven: "Yours are bent. Have mine." |
| Small Warden payment | Small payment | Sized by economy tuning. |
| Skill XP | Action only | Melee (Ranged if S01 allows) from E1/E2 if used. No lump quest XP. |

### 1.12 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player leaves during the storm wait | The quest stays Active at `S01`; resume hook: Iven's bench (Iven: "Still watching. Sit if you like."). |
| Player leaves mid-climb | Steps persist; the warden line stays clipped; the storm window re-opens on the next **Keep stormwatch** or on entering the crag foot volume (a crag-foot wait: **Wait for the weather**, same contract). |
| Knocked back / caught in a strike | Back one stance or knocked down; never off the crag; never fatal. |
| Death (unrelated) | Respawn at the shelter; steps and the clipped line kept. |
| Rolled banner lowered, player logs out before S09 | The roll stays with Iven; on return the staff choice is still waiting on the summit (line-climb up). |
| Co-op | Each player has their own storm window, threads and banner prop. Partners on the summit see each other's spikes glow only in their own `tsl.stormlight`. Fallback if per-player props are not ready: the banner prop is world-shared and the first player to cut it frees it; later players' S07 completes on inspecting the bare pine, and their stormlight plays on the staff (if left) or on their own spikes regardless. |

### 1.13 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Storm-window wait (per-player presentation hour, lightning cadence with a numbered third flash) | Systems Engineer | The Lowmark keep-watch contract plus a scripted flash sequence; server event on the third flash. |
| View-dependent glimpse on the further ridge | Systems Engineer / client | Same pattern as the Lowmark True Line far-bank figure; client report event; nothing gated on it. |
| Climbing: agility triggers with a walkable fallback (line stations) | Gameplay Designer | Chimney triggers; line stations are channelled point-to-point moves; one rappel channel. |
| Brace input and hawk dive knock-back to last stance | Gameplay Designer | One input on a timing window; "last stance" checkpoints on the ledge. |
| Hazard: iron hum then strike with HP clamp | Gameplay Designer | Telegraphed area effect on a timer within a volume; safe volume in the lee notch; 10% HP floor. |
| Stormlight presentation (glow on staff head and player metal, lifting threads) | Art / VFX | A blue glow particle on tagged sockets (weapon/boot sockets, staff head); thread cloth sim lift or a simple vertex lift. |
| Lower an object down a face | Gameplay Designer | Channel that despawns the prop above and spawns it with Iven (Lowmark SB slate pattern). |
| Per-player crag prop (staff left/taken; blue point in storms) | Systems Engineer | Step-conditioned prop; fallback above. |

### 1.14 Cast notes and dialogue

**Iven Ridgeborne [CANON anchor].** *Knows:* the dates and flash counts of every sighting; the crag's routes from below; that a boy tried it. *Does not know:* whose banner it is; what stormlight is; and he does not guess. *Voice:* report first: place, weather, time. One interpretation per scene at most, and he labels it as his.

**Kol Hask, Blood-Oath boy, about fourteen [NEW].** *Knows:* how far up he got (the ledge), what the birds did. *Does not know:* that Brynjar has already heard. *Voice:* boast with the edges showing.

**Brynjar Korr / Elira Hearthward [CANON anchors].** Closing beat only here; full notes in TWC.

```
TSL-D1 (Iven at the warden shelter, S00)
TSL-D1.01 IVEN: "Colour on Splitpine Crag. Red. Third flash of a storm, every storm since first snow."
TSL-D1.02 IVEN: "Not in daylight. Not on the first flash. Not on the second."
  > "What is it?"                                   → TSL-D1.03
  > "Who's been up there?"                          → TSL-D1.05
  > "Show me."                                      → TSL-D1.07
TSL-D1.03 IVEN: "Cloth, I'd say. That's me saying, not the crag."
TSL-D1.04 IVEN: "Highsteads say it's the Lost Banner. Highsteads say a lot in winter."   → TSL-D1 options
TSL-D1.05 IVEN: (nods at the bench) "One boy. Got to the ledge. Came down faster."   → TSL-D1 options
TSL-D1.07 IVEN: "Sit. Storm's coming. They always do, up here." (moves off the bench)
       {event: TSL-D1 end → completes S00; enables keep_stormwatch}
```

```
TSL-L-KOL (Kol on the bench, wrist strapped; optional, before S02)
TSL-L-KOL.01 KOL: "I got to the birds' ledge. Nobody else has got to the birds' ledge."
  > "What happened?"                                → TSL-L-KOL.02
  > "How's the wrist?"                              → TSL-L-KOL.04
TSL-L-KOL.02 KOL: "Birds happened. They scream first. Then they come. I didn't know the screaming was the warning."
TSL-L-KOL.03 KOL: "Now I know. Now I'm not allowed."   → TSL-L-KOL.05
TSL-L-KOL.04 KOL: "Fine. It's fine. It's not fine. Don't tell Brynjar."   → TSL-L-KOL.05
TSL-L-KOL.05 KOL: "If you bring it down, say I got to the ledge."   {set TSL_KOL_HEARD} → end
```

```
TSL-D2 (Iven at the crag foot, S03; he came round by the goat ramp)
TSL-D2.01 IVEN: "Chimney's quick if you fit. Ramp's long. There's a ring at the top of it."
TSL-D2.02 IVEN: (hands over a coil) "Warden line. Clip it, climb it, it holds. I'll be here."
  > "You're not coming?"                            → TSL-D2.03
  > "Anything else up there?"                       → TSL-D2.04
TSL-D2.03 IVEN: "Somebody has to see you fall. That's half of scouting."   → end
TSL-D2.04 IVEN: "Hawks on the ledge. Lightning likes the top. Wind likes everything."   → end
       {event: TSL-D2 end → completes S03}
```

```
TSL-D3 (Iven, from below, on the warden line; plays at S08 lower)
TSL-D3.01 IVEN: (far below) "Line's yours. Send it."
TSL-D3.02 IVEN: (after the roll lands) "Got it. Lighter than it looks."
TSL-D3.03 IVEN: "Staff's still up there. Your call."     {event: S08 complete}
```

```
TSL-D4 (Iven at the crag foot after the descent, S10)
TSL-D4.01 IVEN: "Saw blue on the top from here. Three flashes long. Then the cloud came over it."
TSL-D4.02 [TSL_RIDGE_SEEN] IVEN: "And something on the far ridge, one flash. Not there on the next." (beat) "Writing it down. Not saying it."
TSL-D4.03 IVEN: "Old folk call it stormlight. I call it a thing I've seen on spikes before, never that bright."
  > "It was on my spikes."                          → TSL-D4.04
  > "Let's get this home."                          → TSL-D4.05
TSL-D4.04 IVEN: "Then get lower faster next time." (beat) "Have my straps. Yours are bent."   {give warden's spike straps} → TSL-D4.05
TSL-D4.05 IVEN: (shoulders the roll) "Stonewake. Before the highsteads decide whose it is for us."
       {event: TSL-D4 end → completes S10}
```

```
TSL-D6 (Assembly Hall door, Stonewake; S11)
TSL-D6.01 BRYNJAR: (already there) "Red. Broken horn. I heard on the road. Ours."
TSL-D6.02 ELIRA: (already there) "You heard on the road. I heard from a boy with a strapped wrist. Look at the hem before you say ours."
TSL-D6.03 [TSL_KOL_HEARD] BRYNJAR: (to the player) "Kol says he got to the ledge." (beat) "He's not going up again. Tell him I said it proudly."
TSL-D6.04 IVEN: (sets the roll down on the step, not in anyone's hands) "Found on Splitpine. Third flash. That's all I know."
TSL-D6.05 HADRIK: (from the doorway) "Then it isn't anybody's yet. Bring it in out of the wind."
       {event: TSL-D6 end → quest Completed; TWC Active at S00}
```

**Barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSL-B1.01 | Approach the shelter, before S00 | IVEN | "Colour on the crag again. Third flash." |
| TSL-B1.02 | First storm-window flash | IVEN | "One." |
| TSL-B1.03 | Second flash | IVEN | "Two." |
| TSL-B2.01 | Player enters the rut hollow | (none; stag bellow) | — |
| TSL-B5.01 | First hawk shriek on the ledge | (none; shriek) | — |
| TSL-B6.01 | First iron hum on the summit block (Iven, faint, from below) | IVEN | "Get low!" |
| TSL-B9.01 | Staff left; later storm at the shelter | IVEN | "Still there. Good. Something should be." |
| TSL-B9.02 | Staff taken; Blood-Oath bark at Stonewake | BLOOD-OATH HAND | "Horn-iron came down off Splitpine. First time in thirty winters." |

**Inspects**

| Object | Text | Condition |
|---|---|---|
| Door-frame marks | "A chalk mark for every storm since first snow. A small 3 beside each one." | — |
| Broken spike | "A climbing spike, bent at the tang. Somebody young put all his weight on it at once." | — |
| Red thread | "Red wool, faded to rust outside, red inside the twist. The frayed end points downwind; the cut end, back the way it came." | — |
| Blue thread | "Blue wool, finer spun. Same story: torn off upwind, carried here." | — |
| Goat-hair thread | "Undyed goat-hair, coarse, knotted every hand-span with a double knot. Torn off upwind." | — |
| Old pegs | "Square-cut iron, rusted to the rock. Nobody makes them this shape now." | — |
| New scratches | "Boot-nail scratches going up. Then, lower down, long ones going down very quickly." | — |
| Hawk ledge bones | "Small bones under the nests. Hares, mostly. Possibly one boot-lace." | — |
| Lee-notch cairn | "Three stones on a notch out of the wind. Somebody marked the safe place and didn't stay." | — |
| The pine | "Split by lightning long ago. One half is silver and dead. The other half grew round the banner." | before S07 |
| The banner (wound) | "Red cloth, shredded to a third of a banner. A broken horn in black still shows. The hem is stitched in blue. Patches in something rough and undyed." | before S07 |
| The staff (in crack) | "Driven into the crack hard, iron head up. Whoever did this meant it to be found." | before S09 |
| The staff (after stormlight) | "The iron is warm. It shouldn't be." | after S07 |
| The bare pine | "The living half keeps the shape of what was wound round it." | after S07 |

### 1.15 Mystery ledger

| Mystery | Author truth [PROPOSAL — DIRECTOR] | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The Lost Banner** | A real Blood-Oath-made colour carried by a late-war mixed company. In a storm the bearer drove its staff into Splitpine's crack as a rally mark for stragglers making for the ridge camp; the company left the camp in haste and never came back for kit or colour. The pine grew round it. This autumn a gale split more of the pine and the cloth swung out onto the visible face. | Carried into a storm and never returned; glimpsed on impossible ridges. | The banner, its staff, the threads, the camp (TWC). | It walked there; the wind keeps it; it is a sign about Emberholt. | The company's fate and every name. | TSL (that it is real); TWC (whose hands). |
| **Stormlight** | Ordinary storm discharge on iron at height. Not stated in any text. | Old folk's word; "lucky" or "unlucky" by household. | Spikes and staff glow; the hum before strikes. | The banner glows by itself. | — | None needed. |
| **The further-ridge shape** | **Never explained** (TDS07). | The Ridgewalker. | One flash. | — | Everything. | None. |

### 1.16 Open decisions and review log

**Open:** (1) The crag's name, "Splitpine Crag", is [NEW]; the zone package may prefer a dossier-style name. (2) Whether the blue point in later storms (staff left) should be a recurring ambient for all players after the quest (recommend per player only).

**Review log:** First draft found the banner by triangulating sightings from two vantage points; cut, because triangulation is TF-M4's whisper-hall identity. Replaced with tracking wind-carried threads, which also seeds TWC's three thread types. First draft let the stormlight strike the player; changed so the strange moment is harmless and the separate hazard (TSL-H2) teaches the same family of tell. Kol's rescue was considered and cut (rope rescue belongs to TF-M3); he is already down. The Ridgewalker glimpse is optional, view-dependent and only reported, keeping TDS07 unexplained. Storm hawks are fauna (bible §10), so E2 is harassment, never a required kill.

---

## 2. TWC — Whose Colours

### 2.1 In one paragraph

The banner from Splitpine Crag lies on the floor of the Assembly Hall and two clans are standing over it. Brynjar Korr points to the red field and the broken horn: Blood-Oath made it, Blood-Oath carried it. Elira Hearthward points to the hem: that is Hearthguard flower-stitch, and you do not hem a banner you never carried. Hadrik will not decide. He puts the banner in Old Torvek's keeping, because a colour with no living bearer is settled "the old way", and Torvek hands it to the player: "Read it." The stitching tells a third story. The repairs are in three hands: Blood-Oath horn-stitch in red, Hearthguard flower-stitch in blue, and a plain running stitch in undyed goat-hair, knotted every hand-span with a double knot that neither clan ties. The hoist cord carries a knot for every hand that carried the colour, and the plain knots are there too. At the Abandoned Ridge Camp, past a wolf pack denned in the old palisade, the company's bunk-board is carved with the same three knot signs, and a banked ash pit gives up its mending roll: red wool, blue wool, goat-hair. A mixed company carried this banner, and clanless hands were part of it. Torvek's old way is to walk a colour home in the wind's teeth, off the ground, from the place its company last slept. The player carries it unfurled along the Old Watchfire Line in a hard wind, the horn towers answering as it passes. In the hall, the knots are counted aloud by kind. Torvek holds the hoist cord up by its end, and the cord, wet from the wind and warming in the hall, turns slowly in his hand as it untwists, so that each knot comes round to face whoever is counting. When Runa Weatherall, placed by Hadrik at the back wall, counts the plain knots quietly, the hall goes still enough to hear her, and on her last number the cord stops turning. The one who walked the colour home lays it down. Where the player lays it sets `TH_BANNER`.

**What the player should remember:** a quiet clanless voice counting knots, and a whole hall holding still to hear it. **What they might want next:** to stand where Runa stood, in TF-M5.

### 2.2 Summary card

| Field | Value |
|---|---|
| Type | Settlement (Phase 1.5). Series *The Banner and the Ridge* (2/2). Dossier §XVII "The Banner and the Ridge" [CANON series hook]. |
| Unlock | TSL Completed (automatic at the hall door). |
| Length | 40–50 minutes. |
| Core verb | **investigate, rite**. Identity: reading stitching as evidence; a camp to search under a wolf pack; carrying a colour as a sail through wind windows. |
| Combat | ~15%: one required Ridge Wolf pack at the Abandoned Ridge Camp. |
| Skills | None required. Melee (Ranged if S01 allows) for TWC-E1. |
| NPCs | Old Torvek, Brynjar Korr, Elira Hearthward, Hadrik Stonewake [CANON anchors]; Runa Weatherall [NEW, bible]; a Blood-Oath bearer (Kol Hask's elder cousin, minor) and a Hearthguard storekeeper (minor) who walk the rite. |
| Choice | Where the player lays the colour down: `TH_BANNER` = blood-oath / hearthguard / shared. |
| Unlocks | Banner prop in the chosen hall; Torvek's cairn-house as a lore stop; Runa's later trust line (TF-M5 ambient). |
| **Anchor** | Blood-Oath and Hearthguard clans and the Old Stone; Hushfold as the uncounted third. |
| **World-truth row** | H16 [APPROVED — FT-02b]: late-war companies thinned and mixed; clanless hands carried for Thornfell. Nothing dated. |
| **Revelation role** | Supports R06 (sealing) by undercutting a wrong reading on the bible §8.3 ladder ("Hushfold are deserters' families"): clanless hands carried Thornfell's colours. Owns nothing. Self-contained otherwise. |
| **Recurring evidence** | The banner (custodian per `TH_BANNER`); the Ridge Camp bunk-board and mending roll (place custodian, TDS05 site). Two custodians agree: cloth and camp. |
| **State compliance** | Inactive/Active/Completed. The rite's legs can be repeated, never failed; a colour that touches ground is lifted and walked on. Outcome in the region flag `TH_BANNER`; no fail path. |

### 2.3 Canon grounding

| Element | Source | Use here |
|---|---|---|
| Blood-Oath symbols: broken-horn motifs, red-dyed banners | Dossier §XX [CANON] | The banner's field and appliqué; Brynjar's claim. |
| Hearthguard symbols: mountain-flower motifs, Crestbridge wool cloaks | Dossier §XX [CANON] | Flower-stitch hem in blue wool; Elira's claim. |
| Torvek: rarely speaks; ends arguments with a sentence; stones "the old way"; "the wind remembers vows" | Anchors II [CANON] | The rite of walking the colour home; his closing sentence. |
| Hadrik: not a ruler; chooses where people stand; knows the hall carries some voices; never asks why | Anchors I [CANON] | He places Runa at the back wall; he never says why. |
| Brynjar: loud, loyal, would die for any child; not in the splinter | Anchors II; Part 4 ledger; bible TD-2 | Lines vary by `TH_BRYNJAR`; no war service assigned. |
| Elira: rebuilder; argues with Brynjar and defends him | Anchors II [CANON] | Her claim and her defence of him in the "hearthguard" outcome. |
| Abandoned ridge camps: shattered palisade, ash pits | Dossier §II [CANON feature]; bible TP23, TDS05 | The company's last camp; fires banked for a retreat that never came back. |
| Old Watchfire Line horn towers | Bible TP22 [CANON feature] | The rite route; towers blow Answer. |
| Hushfold households are clanless | Bible §2.2 [NEW, Part 3] | The plain knot is a shelter-line knot. |

### 2.4 The places

**MAP VERIFICATION REQUIRED:** the Abandoned Ridge Camp must lie in Ridgewall on a route that can join the Old Watchfire Line and descend to Stonewake; three towers along the rite route; the hall interior needs a back-wall spot with a line of sight to the speaking stone.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Assembly Hall, Stonewake** | Offer; final rite; choice. | Benches by clan in a horseshoe round the speaking stone. Hadrik's chair is lower than the benches. A back wall of carved stone, worn smooth at shoulder height where people have leaned for generations. |
| **B. Torvek's cairn-house** (edge of the Oath Cairn Fields) | Reading the stitching. | A low stone house with a cairn-moss roof and a long table made of one slab. Stones sorted on shelves by size, not by colour. A lamp, a magnifying lens in a horn ring. |
| **C. Abandoned Ridge Camp** | Investigation; wolves. | A shattered palisade, ash pits in a row, a fallen bunk-house. One bunk-board still on its pegs. Rusted cook-pots stacked as if for loading. A wolf den under the collapsed gate. |
| **D. The Old Watchfire Line** | The rite walk. | Three horn towers with acoustic grooves; fluted faces between them; cairn lees at each tower foot. A horn-keeper at each tower for the rite. |
| **E. Hushfold** (optional) | The plain knot. | Shelter-line homes; double knots on every gate-tie and goat-tether. |

### 2.5 Beats

**Beat 0 — Whose? (`S00_offer`).** *Objective: Hear both claims.* In the hall (TWC-D1). Brynjar and Elira claim; Hadrik gives it to Torvek; Torvek gives it to the player to read. TWC-D1 has a variant for `TSL_STAFF_*`.

**Beat 1 — Read the cloth (`S01_read`).** *Objective: Read the banner at Torvek's table.* At the cairn-house, the banner is laid out on the slab. Four inspects with the lens: **field** (red, broken horn), **horn-stitch** (tight red overcast at the torn edges), **flower-stitch** (blue, a five-petal running pattern on the hem), **plain stitch** (undyed goat-hair, double knot every hand-span). A fifth inspect, **hoist cord**, completes the step: knots in three kinds, bound in no order. Torvek (TWC-D2): "A knot for every hand that carried it. That's the old way. Count them later. First find whose the third kind are."

**Beat 2 — Ask (`S02_ask`).** *Objective: Ask who ties the plain knot.* Brynjar (TWC-D3) and Elira (TWC-D4) each know their own stitch and not the plain one. Both are required (2 dialogue ends); either order. Optional: Runa at Hushfold (TWC-L-RUNA) recognises it: "Shelter-line knot. We tie everything with it." (`TWC_RUNA_ASKED`). If not asked, Runa recognises it in the hall instead (Beat 6), so the identification has a guaranteed path.

**Beat 3 — The last camp (`S03_camp`).** *Objective: Find where the banner's company last camped.* Torvek: the bottom corner is scorched, and "colours go up crags from camps, not from halls"; Iven's report (TSL) gave the crag; the camp below it on the old route is the Abandoned Ridge Camp. Travel. The wolf pack (TWC-E1) holds the camp.

**Beat 4 — Search the camp (`S04_search`).** *Objective: Search the camp.* After E1. Required inspects: **bunk-board** (watch tally carved with three knot signs: a horn, a flower, and a plain double loop) and **banked ash pit** (interaction **Dig out the pit**, 4 s channel, reveals the **mending roll**: a bone needle, red and blue wool, a hank of goat-hair, wrapped in a strip of the same red cloth). Optional inspects: cook-pots stacked for loading, the shattered gate. Two custodians now agree with the cloth: the board and the roll.

**Beat 5 — Walk it home (`S05_walk`).** *Objective: Walk the colour home, off the ground.* Torvek meets the player at the camp gate (TWC-D5) with the banner on a staff (the old staff if `TSL_STAFF_TAKEN`, a fresh-cut one if `TSL_STAFF_LEFT`). The player enters **colour-bearing** carry state: walk only, no agility, banner unfurled. Three legs between the camp and Stonewake, a horn tower at the end of each. In the open, gusts pull the banner like a sail (TWC-H1). **Dip the colour** (hold) lowers it to the shoulder: half speed, no pull. Sheltering in a cairn lee is always safe. At each tower the horn-keeper blows **Answer** as the colour passes. The Blood-Oath bearer and the Hearthguard storekeeper walk beside the player; either can be asked to take a leg (**Hand the colour**), the crew alternative: the leg is walked for the player at a slower pace and the player escorts.

**Beat 6 — The count (`S06_count`) — the strange moment.** *Objective: Bring the colour to the speaking stone.* In the hall, Hadrik places people (TWC-D6): Brynjar at the Blood-Oath bench, Elira at the Hearthguard bench, Runa at the back wall. Torvek has the knots counted by kind, each by someone who ties that knot: Brynjar the horn-knots, Elira the flower-knots, Runa the plain knots. See §2.7.

**Beat 7 — Lay it down (`S07_lay`).** *Objective: Lay the colour down.* Torvek's sentence: "Walker carried it. Walker sets it down." The player carries the colour to one of three places in the hall: the Blood-Oath bench, the Hearthguard bench, or the speaking stone (TWC-D7). Laying it sets `TH_BANNER`.

**Beat 8 — After (`S08_after`).** *Objective: See where the colour hangs.* The next time the player enters the chosen hall (or immediately, if shared: the hall itself), the banner hangs. Short closing barks. Quest Completed on TWC-D8 end.

### 2.6 Encounters and hazards

| Id | Enemies / hazard | Placement | AI role | Telegraph (timings) | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TWC-E1** | 3 × Ridge Wolf runner, 1 × howler | Den under the collapsed gate; runners patrol the ash-pit row | Runners lunge and fall back; the howler hangs back and calls. | Runner: crouch with ears flat (**0.8 s**) then lunge 3 m. Howler: lifts its head and draws breath (**2.0 s**), then a readable howl that calls 2 more runners from the palisade gaps; interrupted by any hit during the draw. | The camp is not empty; teaches that interrupting a call matters (a Thornfell sound lesson in fur). | Required. Ends at 60–75% HP on a late Competent-identity character if the howl is interrupted; harder, never unfair, if not. |
| **TWC-H1** | Sail pull (rite walk) | Open ground between towers | Environmental. | Flute whistle rises a fifth (**1.5 s**), gust (**3 s**). | Makes carrying a colour a physical act. | Undipped in the open during a gust: pushed 2 m sideways and slowed; if the push would take the colour to the ground, the bearer NPC beside the player catches it ("Up. It's up."). No restart. |

**Rules.** Nothing the wolves drop advances the quest. Respawn point: Torvek's cairn-house before S05; the last tower passed during S05 (the colour is returned to the player there).

### 2.7 The strange moment: presentation spec

| Element | Spec |
|---|---|
| Trigger | The cord starts turning at TWC-D6.04 (Torvek lifts it); Runa's part plays on TWC-D6 reaching her count line (server event `twc.count_plain`), and the cord stops on TWC-D6.08's last number. |
| Setup | Hadrik has placed Runa at the back wall, at the worn patch. Brynjar and Elira have counted from their benches; their voices sound as they should from where they stand. |
| What happens | Through the whole count, Torvek holds the hoist cord up by its end. Wet from the walk and warming in the hall, it turns slowly in his hand as it untwists, so each knot comes round to face whoever is counting: horn-knots toward Brynjar, flower-knots toward Elira. When Runa begins the plain knots, quietly, almost to herself, the benches go still to hear her, and the cord turns its plain knots toward the back wall. On her last number it stops turning and hangs straight. |
| Audio | Runa's voice is played from her true position, quiet. The ambient hall murmur drops to nothing for her count (people stop moving to hear). The cord makes a faint creak as it turns. No music. No positional trick (the hall-carry belongs to *The Mason's Margin* and TF-M5). |
| Reactions | Brynjar leans forward on his bench to hear. Elira looks at the cord, then at Hadrik. Hadrik does not look at anyone. Torvek nods once per knot and does not stop the cord. |
| UI / camera | None / player-controlled. |
| After | Cord inspect: *"Damp, and warm now. The twist has come out of it. The knots hang in a straight line."* The back-wall patch is an inspect: *"Worn smooth at shoulder height. People have leaned here for a long time."* |
| What it means | Nothing the quest states. A wet cord untwists as it warms. The count is proved by the knots, not by the cord. |

### 2.8 Steps

| Step | Objective | Completes on | Required |
|---|---|---|---|
| `S00_offer` | Hear both claims. | TWC-D1 end | Yes |
| `S01_read` | Read the banner at Torvek's table. | 5 inspects at the cairn-house → TWC-D2 end | Yes |
| `S02_ask` | Ask who ties the plain knot. | TWC-D3 end + TWC-D4 end | Yes |
| `S02b_runa` | (Optional) Ask at Hushfold. | TWC-L-RUNA end | No |
| `S03_camp` | Find where the banner's company last camped. | Enter camp volume; TWC-E1 defeated | Yes |
| `S04_search` | Search the camp. | Bunk-board inspect + `dig_pit` + mending-roll inspect | Yes |
| `S05_walk` | Walk the colour home, off the ground. | TWC-D5 end; pass tower 1, 2, 3 volumes in carry state; enter hall | Yes |
| `S06_count` | Bring the colour to the speaking stone. | TWC-D6 end (fires `twc.count_plain`) | Yes |
| `S07_lay` | Lay the colour down. | `lay_colour` at one of three hall points → TWC-D7 branch end | Yes |
| `S08_after` | See where the colour hangs. | TWC-D8 end → Completed | Yes |

### 2.9 Flags

| Flag | Set by | Read by |
|---|---|---|
| `TWC_RUNA_ASKED` | TWC-L-RUNA | TWC-D6 Runa variant |
| `TWC_LEG_HANDED` | Any leg handed to an NPC | TWC-D6 Torvek variant (no judgment; a line) |
| `TH_BANNER` = blood-oath / hearthguard / shared | `S07_lay` (exactly one) | TF-M5 placement and posture (bible §9.3: blood-oath counts toward sealed); banner prop; barks |
| `TWC_COMPLETE` | Completion | TWN tally-stick inspect variant (§3); TF-M5 ambient (request) |

### 2.10 Choices and consequences

Brynjar's reaction lines vary by `TH_BRYNJAR` (TWC-D7).

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Blood-Oath bench** — *"Their red. Their horn. Their hall."* | The colour hangs in the Korr horn-tower hall under the loudest horn. | Elira goes quiet; Runa leaves the hall before the end. The plain knots stay in the cord but nobody in that hall ties them. Posture: +1 toward sealed (bible §9.3). | `[disowned]` Brynjar promises to name the plain knots at every First Smoke; `[defended]` he says the colour is home and says nothing of the knots. |
| **Hearthguard bench** — *"They hemmed it. They kept it whole."* | The colour hangs in the Hearthguard terrace hall. | Brynjar is shamed in front of the Assembly. Blood-Oath barks turn sour for a while. | Elira hangs it low "where children can see the mending". `[defended]` Brynjar walks out; `[disowned]` he stays, and says it's fair. |
| **The speaking stone** — *"Every knot carried it. It hangs here."* | Hadrik has it hung over the speaking stone, above no bench. Runa ties one new plain knot into the cord: the first a Hushfold hand has tied in public. | Neither clan has it at home. Torvek dislikes new things and says so. | Brynjar and Elira both grumble, together, which Hadrik calls progress. No posture weight (bible §9.3), but TF-M5's hall shows it. |

None is wrong. The proof is the same in all three: the company was mixed and clanless hands carried.

### 2.11 Rewards

| Reward | Type | Notes |
|---|---|---|
| Torvek's cairn-house | Place | A lore stop: the lens table shows the mending roll (if not taken by the chosen hall; it goes with the banner). |
| **Bearer's thong** | Tool (cosmetic) | A short cord with one knot of the player's choice (horn, flower, plain). Functional name; item pass to define. |
| Standing line | Standing | Clan barks reflect `TH_BANNER`. Runa's address follows bible §5.3 rule 4 only (her name for the player comes from a shelter tally, `TSM_PLAYER_TALLIED` or `TME01_TALLIED`, not from this quest). |
| Skill XP | Action only | From TWC-E1. No lump quest XP. |

### 2.12 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player leaves before the camp | Active at the persisted step; resume hook: Torvek at the cairn-house ("Cloth's waiting. So am I. I'm better at it."). |
| Player leaves mid-walk | The colour returns to the last tower passed; Torvek waits there; the walk resumes from that tower. |
| Colour would touch ground | Caught by the walking NPC; walk continues. |
| Death | Respawn as §2.6 rules; carry restored at the last tower. |
| Co-op | Each player walks their own colour (per-player carry prop). The count scene plays per player; partners not on TWC `S06` see the hall without the turning cord. Fallback if per-player props are not ready: one banner prop in the hall for everyone, its hanging location set by the host's `TH_BANNER`; other players' choices are carried in dialogue and flags only. |

### 2.13 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Colour-bearing carry state with sail push and a dip action | Gameplay Designer | Carry state (walk only) + a gust volume impulse when not dipped; dip = hold to halve speed and cancel the impulse. |
| NPC "hand the colour" crew alternative | Gameplay Designer | NPC follows a spline and the player escorts; same gust timings. |
| Turning cord prop | Animation | A held-cord prop with a slow authored rotation keyed to the count lines; stops on Runa's last number. Fallback: the cord simply hangs and the hall-murmur drop carries the beat. |
| Hadrik places NPCs | Level design | Authored stand-points; NPCs walk to them during TWC-D6. |
| Three lay-down points setting one region flag | Systems Engineer | Interaction on three props; writes `TH_BANNER`. |
| Banner prop in three halls by flag | Systems Engineer | Step/flag-conditioned prop per hall; fallback as §2.12. |

### 2.14 Cast notes and dialogue

**Old Torvek [CANON anchor].** *Knows:* the old way for a colour with no living bearer (walk it home, count the knots, the walker lays it down) [NEW custom]; how cairns are placed. *Does not know:* who the company were; he makes no wartime claim. *Voice:* almost silent; one sentence ends things. He likes old things and says when he does not like new ones.

**Brynjar Korr [CANON anchor].** *Knows:* horn-stitch (his clan's mending), the colour's design. *Does not know:* the plain knot; anything about the company. *Voice:* loud, warm under it, interrupts. `[disowned]`: raw, quicker to doubt himself this winter. `[defended]`: pride with the doors shut.

**Elira Hearthward [CANON anchor].** *Knows:* flower-stitch; how a hem is kept. *Does not know:* the plain knot. *Voice:* tired, practical, fiercely fair to Brynjar even when he is wrong.

**Hadrik Stonewake [CANON anchor].** *Knows:* where to put people. *Does not know:* why he puts people where he does, if anyone asks; he does not explain. *Voice:* few words; patient.

**Runa Weatherall [NEW, bible].** *Knows:* the shelter-line knot; that her gran tied it. *Does not know:* anything about this company. *Voice:* warm, tired, proud; says "we" for the shelter line.

```
TWC-D1 (Assembly Hall floor; the banner laid out; S00)
TWC-D1.01 BRYNJAR: "Red field. Broken horn. Blood-Oath made it. Blood-Oath carried it."
TWC-D1.02 ELIRA: "And Blood-Oath hemmed it in flower-stitch? Look at the hem, Brynjar."
TWC-D1.03 BRYNJAR: "Anyone can hem."
TWC-D1.04 ELIRA: "Anyone can't. That's the point of a stitch."
TWC-D1.05 HADRIK: "It has no living bearer. That makes it Torvek's, until it's somebody's."
TWC-D1.06 TORVEK: (to the player, holding out the roll) "Read it."
TWC-D1.07 [TSL_STAFF_TAKEN] BRYNJAR: "And the horn-iron came down with it. That's ours too."
TWC-D1.07 [TSL_STAFF_LEFT] ELIRA: "Staff's still on the crag, I'm told. We'll cut a new one. Hearthguard wood."
TWC-D1.08 BRYNJAR: (to Elira) "Of course it is."   {event: S00 complete} → end
```

```
TWC-D2 (Torvek's cairn-house, after the five inspects; S01)
TWC-D2.01 TORVEK: "Three hands mended it."
  > "Red, blue, and the rough one."                 → TWC-D2.02
  > "What are the knots on the cord?"               → TWC-D2.03
TWC-D2.02 TORVEK: "Two I know. One I don't. I know most things that are tied."   → TWC-D2.03
TWC-D2.03 TORVEK: "A knot for every hand that carried it. That's the old way."
TWC-D2.04 TORVEK: "Count them later. First find whose the third kind are."   {event: S01 complete} → end
```

```
TWC-D3 (Brynjar, at the Blood-Oath benches; S02)
TWC-D3.01 BRYNJAR: "The red overcast? Horn-stitch. My aunt's hand would do it like that. Everyone's aunt."
  > "And the rough stitch with the double knots?"   → TWC-D3.02
TWC-D3.02 BRYNJAR: (turns it over, frowning) "Not ours. Not theirs either. Some carrier's."
TWC-D3.03 [TH_BRYNJAR=disowned] BRYNJAR: "I've had one winter of finding out what's been done under red. Go on. Find out."
TWC-D3.03 [TH_BRYNJAR=defended] BRYNJAR: "Doesn't matter whose. Red carried it. Write that down."
       {event: D3 end} → end
```

```
TWC-D4 (Elira, at the ridge-market; S02)
TWC-D4.01 ELIRA: "Five petals, running. Flower-stitch. We teach it before we teach reading."
  > "And the rough stitch?"                         → TWC-D4.02
TWC-D4.02 ELIRA: "Goat-hair. No dye. Someone who had no colour to mend with, so they mended without one."
TWC-D4.03 ELIRA: "The double knot I don't know. Ask the people who tie everything twice."
TWC-D4.04 ELIRA: "That's Hushfold, if you want a guess. I don't trade in guesses."   {event: D4 end} → end
```

```
TWC-L-RUNA (Hushfold gate; optional)
TWC-L-RUNA.01 RUNA: (looks at the stitch, then at the player) "Where did you get our knot?"
TWC-L-RUNA.02 RUNA: "Shelter-line knot. Twice round, so it holds when you're too tired to check it. We tie everything with it."
  > "It's on a war banner."                         → TWC-L-RUNA.03
TWC-L-RUNA.03 RUNA: (a long breath) "We carried. Everybody knows we carried. Nobody ever says it in a hall."
TWC-L-RUNA.04 RUNA: "Gran tied hers like that. Doesn't mean it's hers. Means it's ours."   {set TWC_RUNA_ASKED} → end
```

**Ridge Camp inspects**

| Object | Text |
|---|---|
| Bunk-board | "A watch tally carved into the board, rows of small signs: a horn, a five-petal flower, a plain double loop. The three kinds take turns down the board. Nobody stood a watch by clan." |
| Banked ash pit | "Ash raked over and capped with turf. Banked to keep, by people who meant to come back for it." |
| Mending roll | "A strip of red cloth, rolled. Inside: a bone needle, red wool, blue wool, a hank of goat-hair. All three threads from the banner, in one roll." |
| Cook-pots | "Stacked inside each other for loading. Nobody loaded them." |
| Shattered gate | "Broken outward. Something left in a hurry, or came in that way. The wood doesn't say." |

```
TWC-D5 (Torvek at the camp gate, after S04; the colour on its staff)
TWC-D5.01 TORVEK: "A colour that comes home is walked home. From where they last slept."
TWC-D5.02 TORVEK: "In the wind. Off the ground. The wind remembers."
  > "And if I can't hold it?"                       → TWC-D5.03
  > "Give it here."                                 → TWC-D5.04
TWC-D5.03 TORVEK: (nods at the two walkers) "Then they carry a leg. Nobody walks a colour alone."   → TWC-D5.04
TWC-D5.04 TORVEK: (hands it over) "Dip it when the faces whistle."
       {enter colour-bearing carry; S05 active}
```

**Rite barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TWC-B5.01 | First gust, undipped | BLOOD-OATH BEARER | "Dip it! Dip it, it's a sail!" |
| TWC-B5.02 | Colour caught before ground | HEARTHGUARD STOREKEEPER | "Up. It's up." |
| TWC-B5.03 | Pass tower 1 | HORN-KEEPER | (Answer: two short) |
| TWC-B5.04 | Pass tower 2 | HORN-KEEPER | (Answer: two short) |
| TWC-B5.05 | Pass tower 3 | HORN-KEEPER | (Answer: two short) then: "First time I've answered a colour." |
| TWC-B5.06 | Between towers 2 and 3 | BLOOD-OATH BEARER | "My gran says this is how they did it. My gran says a lot." |
| TWC-B5.07 | Same | HEARTHGUARD STOREKEEPER | "Mine too. Maybe they knew each other." |

```
TWC-D6 (Assembly Hall; Hadrik places people; the count; S06)
TWC-D6.01 HADRIK: "Brynjar. There." (the Blood-Oath bench) "Elira. There." (Hearthguard) "Runa." (beat) "By the back wall."
TWC-D6.02 RUNA: "At the back. Of course."
TWC-D6.03 HADRIK: "By the back wall." (He does not explain.)
TWC-D6.04 TORVEK: "Count by kind. Each by them as ties it."
TWC-D6.05 BRYNJAR: (loud) "Horn-knots. One. Two. Three. Four. Five. Six. Seven. Eight. Nine."
TWC-D6.06 ELIRA: "Flower-knots. One, two, three, four, five, six, seven."
TWC-D6.07 [TWC_RUNA_ASKED] RUNA: (quietly) "Plain knots. Shelter-line."
TWC-D6.07 [else] RUNA: (quietly, looking at the cord) "Those are ours. Shelter-line. Plain knots."
TWC-D6.08 RUNA: "One. Two. Three. Four. Five. Six."
       {event: twc.count_plain → presentation §2.7}
TWC-D6.09 TORVEK: "Twenty-two hands."
TWC-D6.10 [TWC_LEG_HANDED] TORVEK: (to the player) "And three walked it home. Good."
TWC-D6.11 TORVEK: "Walker carried it. Walker sets it down."   {event: S06 complete}
```

```
TWC-D7 (the player lays the colour; S07)
  > (Lay it at the Blood-Oath bench)                → TWC-D7.10
  > (Lay it at the Hearthguard bench)               → TWC-D7.20
  > (Lay it on the speaking stone)                  → TWC-D7.30
TWC-D7.10 [TH_BRYNJAR=disowned] BRYNJAR: (picks it up carefully) "Home." (beat) "Every knot stays in. I'll name the plain ones at First Smoke. Every year. Hold me to it."
TWC-D7.10 [TH_BRYNJAR=defended] BRYNJAR: (lifts it high) "Home. Where it was made."
TWC-D7.11 ELIRA: (quiet) "Where it was made, yes."
TWC-D7.12 (Runa is already gone from the back wall.)   {set TH_BANNER = blood-oath} → TWC-D7.40
TWC-D7.20 ELIRA: "We'll hang it low. Where the children can see the mending."
TWC-D7.21 [TH_BRYNJAR=defended] BRYNJAR: (stands, says nothing, walks out; the door is heavy and he lets it fall)
TWC-D7.21 [TH_BRYNJAR=disowned] BRYNJAR: (a long breath) "Fair." (beat) "We lost the right to be sure of things this year."
TWC-D7.22 ELIRA: (after him, or to him) "You'll come and see it. You'll tell the children about the horn."   {set TH_BANNER = hearthguard} → TWC-D7.40
TWC-D7.30 HADRIK: "Then it hangs here. Over no bench."
TWC-D7.31 RUNA: (comes forward from the wall, ties one plain knot into the cord) "One more. So there's a Hushfold knot tied in daylight."
TWC-D7.32 [TH_BRYNJAR=disowned] BRYNJAR: "Over nobody's bench." (beat) "I can live with nobody's bench."
TWC-D7.32 [TH_BRYNJAR=defended] BRYNJAR: "Nobody's colour is nobody's." (beat) "Fine. It's everybody's. I'll still say red first."
TWC-D7.33 ELIRA: "He'll say red first. I'll say the hem."
TWC-D7.34 TORVEK: "New." (beat) "I don't like new." (beat) "It'll hold."   {set TH_BANNER = shared} → TWC-D7.40
TWC-D7.40 TORVEK: (to the player, already turning away) "Twenty-two hands. Remember the number. Nobody else will."
       {event: S07 complete}
```

```
TWC-D8 (next entry to the chosen hall; S08)
TWC-D8.01 [TH_BANNER=blood-oath] KORR HORN-KEEPER: "Hangs under the big horn. Brynjar comes and stands under it. Doesn't say anything. Unusual."
TWC-D8.01 [TH_BANNER=hearthguard] HEARTHGUARD CHILD: "That's the mending. That blue's ours. The red's theirs. The brown's somebody's."
TWC-D8.01 [TH_BANNER=shared] HADRIK: "People stop under it. Then they argue under it. Better than in the passes."
       {event: TWC-D8 end → quest Completed}
```

**Banner inspects (hung, by outcome)**

| Outcome | Text |
|---|---|
| blood-oath | "Red, under the loudest horn in the hall. The cord hangs down beside it with its knots. Twenty-two." |
| hearthguard | "Hung low. The blue hem is at a child's eye level. Twenty-two knots on the cord." |
| shared | "Over the speaking stone, above no bench. Twenty-three knots on the cord. The newest is plain, and still pale." |

### 2.15 Mystery ledger

| Mystery | Author truth [PROPOSAL — DIRECTOR] | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Whose colours** | Blood-Oath-made, carried and mended by a late-war company of Blood-Oath, Hearthguard and clanless hands who stood watch by turns. | Blood-Oath's (Brynjar) or Hearthguard's (Elira). | Three stitches; hoist knots; bunk-board; mending roll. | Clanless carriers were hired porters, not part of the company; or Hushfold are deserters' kin. | Every name; the company's fate. | TWC (resolved locally). |
| **The company's fate** | Withheld. They left the camp in haste and did not come back for kit or colour. | Lost in a storm. | Stacked pots; banked fires; outward-broken gate. | They deserted. | Everything beyond the camp. | None in Thornfell. |
| **The turning cord** | A wet cord untwisting as it warms. Nobody says so. | "The old way"; the knots wanted to be counted. | Only the behaviour. | The bearers were answering. | Nothing to withhold. | None. |

### 2.16 Open decisions and review log

**Open:** (1) The "walk it home" rite and the knot-per-bearer custom are [NEW]; the Director may prefer a different form for Torvek's old way. (2) Knot counts (9 / 7 / 6 = 22) are [NEW] and tunable; they record bearers, not dead. (3) Whether Runa's Hushfold knot in the shared outcome should be read by `TH_HUSHFOLD_VOICE` content (recommend: ambient only).

**Review log:** First draft settled the claim by the hall voice (the carrying back wall); cut as a breach of the evidence rule. The knots, board and roll settle it. Independent review: the remaining carrying-voice moment duplicated TMM's hall moment and TF-M5's carrying spot, so it was replaced by the turning cord; Runa's voice is now heard because the hall goes quiet for her. First draft used stone-setting on sound lines for the rite; moved away because TWN uses stone ringing; the rite is now a carried colour in wind windows, distinct from TSL's climb and TWN's carve. TDS05 keeps "whose" withheld for names: the camp is attributed to a mixed company, never to a clan or person. `TH_BANNER` = shared carries no posture weight in bible §9.3; kept as written there. Brynjar's lines vary on `TH_BRYNJAR` at D3, D7 and the shared branch; he is never placed in the war.

---

## 3. TWN — The Weight of a Name

### 3.1 In one paragraph

For thirty springs, Asa Brede of Hushfold has climbed to Maera Cairnwatch's Name-Stone Wall to renew a slip of thin slate: *Sig Brede, went over the pass.* Her brother had no clan, so he has no stone, and Asa is too frail to climb many more springs. Her grandson Orm wants a stone cut while she can see it. Maera's rule is old and plain: a stone needs two that agree, or one record and one voice. Asa's voice is one. The player goes looking for the other, and finds too many. Maera's own private list, the one she showed beside the horn roster at the rim, reads *"Sig Brede. Held."*: on the lower shelf at the fifth hour, by the word of those who came up the rim path after. On the Shatterfall rim, under the rime on the second cairn's face, is **S. BREDE**, "lost in the gorge storm". The horn roster, read again where it is kept, gives the hour of the *Split* and "Rear guard not recalled", and nothing else: the margin where the names were has rotted to lace. An old Hushfold carrier remembers two Bredes carrying water in the war, Sig and his cousin Sten, "one name between them half the time", and a Brede who went on with a late column toward the far gate. And the phrase itself splits in two: before the war, "went over the pass" meant crossed; in the war it came to mean lost where nobody could bring you home. Maera hears it all at the wall, with Asa's hand on the stone, and decides how the stone is cut, on the player's recommendation. The player finds a slab that rings true, splits it and cuts the letters. When it is set and Asa lays thirty springs of slips into its niche, a gust crosses the field and blows the wall clean of snow, every stone but the new one, where the snow catches in the fresh-cut letters and holds there, white in grey, for a breath. "That's the wind," Asa says. Maera says, "Yes."

**What the player should remember:** cutting a name, knowing they do not know what happened to him. **What they might want next:** to read what other places wrote down (an R14 hook that asks nothing now).

### 3.2 Summary card

| Field | Value |
|---|---|
| Type | Memory/lore (Phase 1.5). Register of the Unreturned, Thornfell case. Part 3 Thornfell proposal "The Weight of a Name". |
| Unlock | TF-M3 Completed (required: `TES_horn_roster` exists and `TH_SHATTERFALL_ACCOUNT` is set). |
| Length | 40–50 minutes. |
| Core verb | **gather, testify, carve**. Identity: a testimony walk across three custodians that disagree; listening for a true stone; letter-cutting as a calm channelled craft. |
| Combat | ~5%: an optional Rock Viper nest at the cairn-field stone ledge. |
| Skills | Mining optional (split the slab); crew alternative (Maera's cairn-hands). |
| NPCs | Maera Cairnwatch [CANON anchor]; Runa Weatherall [NEW, bible]; Asa Brede, Orm Brede, Hessa (old Hushfold carrier) [NEW, minor]; the roster's keeper by outcome: Maera, nobody (the niche), or the Passwatch warden-post clerk. |
| Choice | How the stone is cut (3 options; quest-local). |
| Unlocks | The Brede stone at the wall foot; Maera's name-slip rows as a place the player can add an offering; an R14 hook flag. |
| **Anchor** | Thornfell Cairn-Keepers (Maera) and Hushfold. |
| **World-truth row** | H16 [APPROVED — FT-02b]: Shatterfall's rear guard; clanless carriers; the sealing years. |
| **Revelation role** | Supports R06 (horn) with a second reading of the roster; adds weight to R06 (sealing) through Act III's existing TWN line (§3.13); **plants R14** (optional Mire end; exempt from the guaranteed-path rule). Resolves its own case in Thornfell. |
| **Recurring evidence** | Maera's private cairn list (TF-M3 document; "Sig Brede. Held."); `TES_horn_roster` (TF-M3 quest item, read in place; custodian per `TH_SHATTERFALL_ACCOUNT`; its name margin is rotted, so it can confirm the hour and the unrecalled rear guard but no name); the Shatterfall rim cairn (place); the Brede name-slips (the wall and the family). Independent custodians: Maera's list (record), the cairn (place), Asa and Hessa (testimony). |
| **State compliance** | Inactive/Active/Completed. No answer is required; every choice is a cut stone. Outcome in quest-local `TWN_CUT_*`; no fail path. |

### 3.3 Canon grounding

| Element | Source | Use here |
|---|---|---|
| Maera: absolute authority over the dead; no grave or echo identifies a person by itself | Anchors V; Part 4 ledger | She decides the cut; the snow in the letters identifies no one. |
| Maera's temporary-name practice | Part 3 proposal ("allows dignity while testimony remains open") | The name-slip rows. |
| Rim cairns: names, no bodies, "lost in the gorge storm"; Thornfell never speaks of its own dead at Shatterfall | Bible §2.2, TP14; H16 [APPROVED — FT-02b]; Act II rim-cairn inspects (second cairn: "And more, under rime.") | S. BREDE under the rime on the second cairn's face. |
| The horn roster with the hour, *Split*, and "Rear guard not recalled. No answer."; its duty-name margin rotted on every leaf | Bible TF-M3 brief; Act II roster text | Read in place, exactly as Act II gives it. No line is added. |
| Maera's private list: "Sig Brede. Held."; the Hushfold slip "Sig Brede. Went over the pass." | Act II (TF-M3 dialogue documents) | The record and the slip this case starts from. |
| One rear-guard name is also on a Hushfold name-slip as "went over the pass" | Bible TF-M3 brief; §8.2 | This case. |
| Hushfold: clanless; several names on the closure roster | Bible §2.2 | TF-M5 weight (request only). |
| Who blew the Split and how many died stay withheld | Bible TD-9 | Nothing here counts the dead or names the hornman. |
| Torvek's cairns on sound lines | Bible TDS04 [CANON alignment; effect withheld] | Not used. The stone is set where Maera points; nothing here touches the alignment. |

### 3.4 The places

**MAP VERIFICATION REQUIRED:** the stone ledge must be reachable from the Name-Stone Wall without crossing the oath path (TOS); the rim cairns are on the Shatterfall rim, outside the gorge's storm volume.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Hushfold, the Brede house** | Offer; Asa's testimony; household object. | A shelter-line home with a goat byre against it. On a peg by the door, a carrier's tally stick on a knotted thong. A bundle of old chalk in a cup. |
| **B. The Name-Stone Wall** (TP15) | Maera; the slip rows; the hearing; setting. | A long wall of cut name-stones by clan. Below them, at hip height, rows of thin slate slips wedged into the joints, some new, some so old the chalk has gone and only the scratch is left. At the wall foot, a few stones with no clan mark. |
| **C. The stone ledge** | Choosing and splitting a slab. | A shelf of bedded grey stone above the field, wedge-holes from old splitting, offcuts. Shale under the lip where vipers sun. |
| **D. Shatterfall rim cairns** (TP14) | The rim name. | Cairns along the gorge edge; names cut on faces; the inscription "lost in the gorge storm". |
| **E. The roster's keeping** | Second reading. | By `TH_SHATTERFALL_ACCOUNT` (custody as Act II sets it): **amended**: in Maera's keeping with her list at the Name-Stone Wall; **beside**: the lead tin in the largest rim cairn's niche, behind its slate; **kept**: the Passwatch warden post's strongbox, sealed under Maera's cord, read under the clerk's eye. |

### 3.5 Beats

**Beat 0 — A slip, not a stone (`S00_offer`).** *Objective: Hear what Orm wants.* Runa introduces Orm (TWN-D1). Orm asks for help getting Asa's brother a stone "before Gran can't climb to see it".

**Beat 1 — Asa's voice (`S01_asa`).** *Objective: Hear Asa's account.* Asa (TWN-D2) tells what she remembers: she was small; Sig carried water for the companies; one summer he did not come back, and their mother said "he went over the pass". Inspect the **tally stick**: water-run notches to midsummer of one year; a double knot on its thong. (With `TWC_COMPLETE`, the inspect notes it is the shelter-line knot from the banner's cord. Colour only.)

**Beat 2 — Maera's rule (`S02_wall`).** *Objective: Ask Maera for a stone.* At the wall (TWN-D3). Inspect the **slip bundle** (thirty slips in many hands, all the same words). Maera: two that agree, or one record and one voice. She names her own list ("Sig Brede. Held.") as one record, says where the horn roster is now kept, and that the rim has "a Brede" under the rime, without saying what any of it means.

**Beat 3 — The rim (`S03_rim`).** *Objective: Find the Brede on the rim cairns.* At the second cairn (the one whose face reads "And more, under rime" in TF-M3), **Brush the rime** (2 s) and inspect: **S. BREDE**. Required. The rest of the row stays as Act II leaves it; with `amended`, the first cairn's new line is visible along the row.

**Beat 4 — The roster (`S04_roster`).** *Objective: Read the horn roster again.* Wherever it is kept (area E). The player reads it in place (interaction **Read the roster**, 3 s); it is never carried. Read for a name this time, it has none: the left margin is lace on every leaf. What it keeps is the hour of the *Split* (fourth, late) and "Rear guard not recalled. No answer." Maera's list puts Sig Brede on the shelf at the fifth hour. Required. With `kept`, the clerk's line (TWN-D4k). The roster cannot say who was on the shelf.

**Optional — Hessa (`S04b_hessa`).** *Objective: Ask who else carried.* Back at Hushfold, old Hessa (TWN-L-HESSA) carried in the war: two Bredes, Sig and his cousin Sten; "one name between them half the time". She saw "a Brede" go on with a late column toward the far gate. She cannot say which.

**Beat 5 — Two meanings (`S05_phrase`).** *Objective: Ask what "went over the pass" means.* Asked of Maera or Runa (either completes). Before the war, crossed. In the war, lost where nobody could bring you home. Maera: "It meant both. People let it."

**Beat 6 — The hearing (`S06_hearing`).** *Objective: Bring what you found to the wall.* Asa is brought up by Orm and Runa on a goat-sledge (off-screen; they are placed at the wall when the player enters it after S04 and S05). Asa speaks with her hand on the wall (TWN-D5). The player gives their readings, in dialogue, one per custodian. Maera asks the player how they would cut it (the choice, §3.10). Maera decides; her decision is the player's recommendation in every case (she says why).

**Beat 7 — A stone that rings (`S07_stone`).** *Objective: Find a stone without a flaw.* At the stone ledge, five marked slabs. **Strike the slab** (instant): a true slab rings long and clear; a flawed one gives a dead knock and a thin line of dust runs along the hidden crack (visual tell for accessibility). Two of five ring true. Choose one. Vipers in the shale under the lip (TWN-E1) are optional to fight; they are disturbed only by stepping on the shale.

**Beat 8 — Split it (`S08_split`).** *Objective: Split the slab.* **Set wedges** (3 s) and **Drive the wedges** (Mining, 3 segments, progress kept). **Crew alternative:** ask Maera's cairn-hands (TWN-D6): they split it overnight; the player uses the wall's **Keep vigil** wait (per-player presentation hour) and the slab is at the wall in the morning.

**Beat 9 — Cut the name (`S09_carve`).** *Objective: Cut the letters.* At the wall foot, Maera chalks the letters. **Cut a line** (channel per line; 2 or 3 lines depending on the choice; each line 3 segments of 3 s; progress kept). Asa watches. Orm holds the lamp if the player asked him to (optional line).

**Beat 10 — Set it (`S10_set`) — the strange moment.** *Objective: Set the stone.* **Set the stone** (3 s) on the wall-foot line where Maera points. Asa lays the slips into the stone's niche. See §3.7.

**Beat 11 — Close (`S11_close`).** *Objective: Speak to Maera.* TWN-D7: Maera's closing, with the R14 hook line. Quest Completed.

### 3.6 Encounters and hazards

| Id | Enemies / hazard | Placement | AI role | Telegraph (timings) | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TWN-E1** | 2 × rock viper, 1 × shale-coil (Rock Vipers family) | Shale under the stone ledge's lip | Ambush; leashed to the shale. | Viper: tail rattles on shale (**1.0 s**), then a 2 m forward strike. Shale-coil: the shale shivers in a ring round the player (**1.5 s**), then it bursts up inside the ring. | The ledge is not a garden; stepping on shale has a price. | **Optional.** The slabs can be struck from the rock without touching shale. If fought, ends at 75–90% HP on an Advanced-identity character. |
| **TWN-H1** | Wind windows | Rim cairns (exposed edge) | Environmental. | Flute whistle (**1.5 s**), gust (**3 s**). | The rim is an edge. | Pushed back from the edge, never over it (rim volume has an edge blocker). |

**Rules.** Respawn point: the Name-Stone Wall. Nothing the vipers drop advances the quest. The Shatterfall gorge's storm volume (Horn-Echo) is never entered by this quest.

### 3.7 The strange moment: presentation spec

| Element | Spec |
|---|---|
| Trigger | **Set the stone** completes and Asa's lay-slips line ends (server event `twn.set`). |
| Duration | ~8 s. |
| What happens | A gust comes across the Oath Cairn Fields from the plateau side (it whistles first, by the usual tell). It strips the light snow off the whole wall in one sheet: every old face is blown clean and grey. On the new stone the snow catches in the fresh-cut letters and stays, so for a breath the name stands out white on grey, the only lettered thing on the wall. Then the gust is past, the snow in the cuts slumps, and the stone is plain again. |
| Audio | Wind only, and the hiss of blown snow. No music. No ring, no tone (kept distinct from *Witness at the Gate*'s tower-to-tower call). |
| Reactions | Asa: "That's the wind." Maera: "Yes." (TWN-D7.01–.02). Orm looks at the wall for a long time. |
| UI / camera | None / player-controlled. |
| After | New stone inspect gains: *"The cuts are still sharp. Snow sits in them when it blows."* The effect does not repeat as a moment; in later snow the new letters simply hold a little white. |
| What it means | Nothing the quest states. New cuts catch snow. It does not say Sig is dead, alive, or here. |

### 3.8 Steps

| Step | Objective | Completes on | Required |
|---|---|---|---|
| `S00_offer` | Hear what Orm wants. | TWN-D1 end | Yes |
| `S01_asa` | Hear Asa's account. | TWN-D2 end + tally-stick inspect | Yes |
| `S02_wall` | Ask Maera for a stone. | Slip-bundle inspect + TWN-D3 end | Yes |
| `S03_rim` | Find the Brede on the rim cairns. | `brush_rime` on the second cairn + rim-face inspect | Yes |
| `S04_roster` | Read the horn roster again. | `read_roster` at the outcome location (+ TWN-D4k if kept) | Yes |
| `S04b_hessa` | (Optional) Ask who else carried. | TWN-L-HESSA end | No |
| `S05_phrase` | Ask what "went over the pass" means. | TWN-D3b (Maera) or TWN-L-RUNA end | Yes |
| `S06_hearing` | Bring what you found to the wall. | TWN-D5 choice node | Yes |
| `S07_stone` | Find a stone without a flaw. | `strike_slab` on a true slab + `choose_slab` | Yes |
| `S08_split` | Split the slab. | 3 × `drive_wedges`, or TWN-D6 + `keep_vigil` | Yes |
| `S09_carve` | Cut the letters. | All `cut_line` segments for the chosen text | Yes |
| `S10_set` | Set the stone. | `set_stone` (fires `twn.set`) | Yes |
| `S11_close` | Speak to Maera. | TWN-D7 end → Completed | Yes |

### 3.9 Flags

| Flag | Set by | Read by |
|---|---|---|
| *(read)* `TES_NAMESLIP_SEEN` | Act II (TF-M3, optional slip inspect) | TWN-D1.03b opening variant |
| `TWN_HESSA_HEARD` | TWN-L-HESSA | TWN-D5 option; TWN-D7 variant |
| `TWN_CUT_BOTH` / `TWN_CUT_FAMILY` / `TWN_CUT_OPEN` | TWN-D5 (exactly one) | Stone text and prop; Hushfold barks |
| `TWN_MIRE_HOOK` | TWN-D7.10 | Future Mire Register content (R14). No Thornfell reader. |
| `TWN_COMPLETE` | Completion | TF-M5 `TSW-D9.51` (Act III reads TWN Completed; already authored) |

### 3.10 Choices and consequences

| Option | Stone text | Cost | Later |
|---|---|---|---|
| **Both roads** — *"Cut what the family says and where the rim names him. Both are honest."* | SIG BREDE / went over the pass / named at Shatterfall | The rim's "lost in the gorge storm" now has a reader who disagrees with it; some clan visitors call it a slight to the rim. Asa does not like seeing Shatterfall on her brother's stone. | The stone stands beside the rim's version the way TF-M3's records were set side by side. Hushfold bark: "Two places for one man. That's more than most of us get." |
| **The family's words** — *"Cut what Asa's mother said. The rim keeps its own."* | SIG BREDE / went over the pass | The roster line and the rim are not on the stone; the next reader will not know there was a question. | Asa is content. Maera keeps a note of the readings in her own list (not shown). Orm: "Gran sleeps better." |
| **An open stone** — *"Cut the name. Leave the line under it uncut, until somebody knows."* [NEW practice] | SIG BREDE / (a smooth band left blank) | Asa will never see the line filled. Some find a blank band worse than a wrong word. | The slips stay in the niche and are renewed each spring by the family, as before but on his own stone. Maera: "A stone that waits. We've never had one. We've needed one." |

Maera decides; she takes the player's recommendation and says why in her own words. None is wrong.

### 3.11 Rewards

| Reward | Type | Notes |
|---|---|---|
| The Brede stone | Place | A per-player prop at the wall foot; inspect text by choice. |
| **Cairn-keeper's chisel** | Tool | Functional name; lets the player add a stormflower offering at any name-stone (cosmetic). Item pass to define. |
| Hushfold standing line | Standing | Orm and Asa greet the player by name. Runa: "You cut one of ours. People will remember who held the chisel." |
| Skill XP | Action only | Mining from S08 if done by the player. No lump quest XP. |

### 3.12 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player leaves at any step | Active at the persisted step; resume hook: Orm at Hushfold ("Gran asks if you're still looking. I said yes."). |
| Roster location unreachable for a moment (e.g., Passwatch not entered) | The step waits; the location is always reachable after TF-M3. |
| Strikes a flawed slab | Nothing lost; strike another. Five slabs, two true. |
| Split interrupted | Wedge progress kept. |
| Carving interrupted | Each line's segments persist; chalk stays. |
| Co-op | Each player has their own stone prop and hearing. The snow moment plays per player on their `twn.set`. Fallback if per-player props are not ready: one Brede stone in the world showing the **open** text for everyone, with the player's choice carried in dialogue and flags. |

### 3.13 Order variants and requests

| Case | Handling |
|---|---|
| **TF-M5 Completed before TWN** | Optional extra reading at TWN-D5: the player can mention the gatehouse wall (`TSW_closure_rubbing` exists). Maera: "I've read the rubbing. No Brede on it." (beat) "That's not nothing either." Act III's gatehouse roster carries no Brede, and this line keeps it so. Settles nothing. |
| **TWN Completed before TF-M5** | No request. Act III already authors the weight: `TSW-D9.51` (Maera: "That's two walls this autumn kept names nobody read."). The earlier request to add a Brede to the rubbing is withdrawn (it would contradict Act III's roster text). |
| **R14 hook** (request to the Mire bible owner) | `TWN_MIRE_HOOK` marks that the player heard Maera's line about other places keeping books. Thornfell asserts no Mire fact; the Mire end is optional and exempt from the guaranteed-path rule. |
| **Act II alignment** (independent review) | No request. TWN reads `TES_horn_roster` exactly as Act II gives it (no names; margin rotted), uses Maera's private list ("Sig Brede. Held.") and the Hushfold slip as Act II authors them, and finds S. BREDE under the rime on Act II's second rim cairn. The earlier request for an added roster line is withdrawn. |

### 3.14 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Read a quest item in place at one of three locations by flag | Systems Engineer | Three conditional inspect props; whichever matches `TH_SHATTERFALL_ACCOUNT` is active. |
| Strike-and-listen slabs (true/flawed) | Gameplay Designer / Audio | Instant interaction; two sound sets; a dust-line VFX on flawed slabs. |
| Channelled letter-cutting by line, persistent | Gameplay Designer | Segmented channel per line; per-player decal reveal by segment (fallback: whole-line reveal). |
| Snow-in-the-letters moment | VFX | A one-shot snow-strip on the wall props and a snow-fill decal on the new stone's cut lines, fading over ~3 s. Fallback: the decal alone. |
| Vigil wait (crew alternative) | Systems Engineer | Shared keep-watch contract. |
| NPC placement at the wall after two steps | Level design | Step-conditioned NPC spawn (Asa, Orm, Runa, sledge). |

### 3.15 Cast notes and dialogue

**Maera Cairnwatch [CANON anchor].** *Knows:* the cairn names; the slip practice; her own private list (not opened here); what the phrase used to mean. *Does not know:* which Brede; she will not pretend. *Voice:* gentle, unyielding, few words; she decides and says why.

**Asa Brede, about seventy [NEW].** *Knows:* Sig carried water; her mother's words; the summer he did not come back. *Does not know:* anything about the gorge; she has never been to the rim. *Voice:* short, dry, a little deaf on purpose.

**Orm Brede, about twenty [NEW].** *Knows:* that his gran is failing. *Voice:* asks for things by talking around them.

**Hessa, old Hushfold carrier [NEW].** *Knows:* there were two Bredes carrying; one went on with a late column. *Does not know:* which. *Voice:* precise about the things she is sure of, and says so about the rest.

**Runa Weatherall [NEW, bible].** *Knows:* the shelter line's words for things. *Does not know:* her own family's name on the gatehouse wall (bible §2.5); nothing here touches it.

```
TWN-D1 (Hushfold, Runa and Orm; S00)
TWN-D1.01 RUNA: "Orm wants to ask you something and won't. So I'm asking for him. Go on, Orm."
TWN-D1.02 ORM: "It's Gran. Asa. She goes up to the cairn wall every spring with a slip for her brother."
TWN-D1.03 ORM: "Thirty springs. She's not going to manage many more. I'd like her to see a stone."
TWN-D1.03b [TES_NAMESLIP_SEEN] RUNA: "You've seen the slip. Maera showed you on the rim. Same name."
  > "Why doesn't he have one?"                      → TWN-D1.04
  > "What do you need?"                             → TWN-D1.05
TWN-D1.04 RUNA: "No clan. No row. No row, no stone. Unless Maera says."   → TWN-D1.05
TWN-D1.05 ORM: "Maera says she needs more than Gran. I don't know what more is. Gran's inside."
       {event: S00 complete} → end
```

```
TWN-D2 (the Brede house; Asa by the fire; S01)
TWN-D2.01 ASA: "You're the walker. Sit. Don't help me up, I'm not getting up."
TWN-D2.02 ASA: "Sig carried water for the companies. Up and down. He let me hold the yoke."
TWN-D2.03 ASA: "One summer he didn't come back. Mother said he went over the pass. So that's what we say."
  > "Over the pass where?"                          → TWN-D2.04
  > "Is that his tally stick?"                      → TWN-D2.06
TWN-D2.04 ASA: "Over. I was six. Over was a direction."
TWN-D2.05 ASA: "Now it's a slip on a wall." (beat) "Find Maera her more. I'm tired of slate."   → end
TWN-D2.06 ASA: "Notches for every run. He stopped notching at midsummer. Take it to the light, I can't see it."   → TWN-D2.05
```

**Inspects and documents**

| Id / object | Text | Condition |
|---|---|---|
| TWN-I1 Tally stick | "A carrier's tally stick. A notch for each water run, close together, up to midsummer of one year. Then nothing. The thong is tied with a double knot." | — |
| TWN-I1 Tally stick | (adds) "The same double knot as the plain knots on the banner's cord." | `TWC_COMPLETE` |
| Slip bundle | "Thirty slips of thin slate, tied together. The same words on every one, in a dozen hands: *Sig Brede, went over the pass.* The oldest has lost its chalk; only the scratch is left." | — |
| Slip rows | "Slate slips wedged into the joints of the wall at hip height. Names waiting for stones." | — |
| Wall-foot stones | "A few stones with no clan mark. Hushfold names, mostly. Not many." | — |
| Rim face (second cairn, after Brush the rime) | "HALLVARD BRENN. SIGNY ROOK. Under the rime, more: S. BREDE. Beneath, as on every face: *lost in the gorge storm.*" | `TH_SHATTERFALL_ACCOUNT` = beside or kept |
| Rim face (second cairn, after Brush the rime) | "HALLVARD BRENN. SIGNY ROOK. Under the rime, more: S. BREDE. *Lost in the gorge storm.* Along the row, the first cairn carries its new line. This one does not." | = amended |
| TWN-I2 The roster | "The horn-station roster. You have read it before. Fourth hour, late: *Split.* Beneath it: *Rear guard not recalled. No answer.* You look for a name this time. The left margin is lace on every leaf. Whoever stood on the shelf, the roster has lost them." | — |

```
TWN-D3 (the Name-Stone Wall; Maera; S02)
TWN-D3.01 MAERA: "Asa's slip. Thirty springs. I know her knock."
TWN-D3.02 MAERA: "A stone needs two that agree. Or one record and one voice. Asa is a voice."
  > "Where would a record be?"                      → TWN-D3.03
  > "What if nothing agrees?"                       → TWN-D3.05
TWN-D3.03 MAERA: "My list is a record. It says Sig Brede held the shelf. You've seen it." (beat) "The roster's the other. And the rim has a Brede, under the rime."
TWN-D3.04 MAERA: "I'm not saying any of it is him. I'm saying it's there."   {event: S02 complete} → end
TWN-D3.05 MAERA: "Then the slip stays. A slip is not nothing. It's a name that's still being asked about."   → TWN-D3.03

TWN-D3b (Maera, after S03 or S04; S05)
TWN-D3b.01 MAERA: "'Went over the pass.' Before the war it meant crossed. You went over, you'd be back by thaw."
TWN-D3b.02 MAERA: "In the war it came to mean the other thing. Lost somewhere we couldn't fetch you."
TWN-D3b.03 MAERA: "It meant both. People let it."   {event: S05 complete} → end
```

```
TWN-D4k (Passwatch warden post; roster clerk; TH_SHATTERFALL_ACCOUNT = kept)
TWN-D4k.01 CLERK: "Roster's in the box, under Maera's cord. She sent word you could look. You read, I watch. Those are the rules."
TWN-D4k.02 CLERK: (after) "Find what you wanted?" (beat) "Don't tell me. I'd have to write it down."   → end
```

```
TWN-L-HESSA (Hushfold, old carrier; optional)
TWN-L-HESSA.01 HESSA: "Bredes. Two of them carried. Sig and his cousin Sten."
TWN-L-HESSA.02 HESSA: "Shouted 'Brede' and either came. One name between them half the time."
  > "Did one go over the pass?"                     → TWN-L-HESSA.03
TWN-L-HESSA.03 HESSA: "A Brede went on with a late column. Toward the far gate. I saw his back."
TWN-L-HESSA.04 HESSA: "Which one, I couldn't swear. I'm sure of the back. Not the face."   {set TWN_HESSA_HEARD} → end
```

```
TWN-L-RUNA (Hushfold; alternative completion of S05)
TWN-L-RUNA.01 RUNA: "'Over the pass'? Our gran used it for anyone the far side kept."
TWN-L-RUNA.02 RUNA: "Kept alive, kept dead. Same words. We didn't have many words then."   {event: S05 complete} → end
```

```
TWN-D5 (the hearing at the wall; Asa's hand on the stone; S06)
TWN-D5.01 MAERA: "Asa Brede. Speak."
TWN-D5.02 ASA: "My brother Sig carried water. One summer he didn't come back. Mother said he went over the pass. That's all I have. I've had it a long time."
TWN-D5.03 MAERA: (to the player) "And you."
  > "The rim has S. Brede, lost in the gorge storm."             → TWN-D5.04
TWN-D5.04 MAERA: "Yes."
  > "Your list says Sig Brede held the shelf. The roster lost the names."   → TWN-D5.05
TWN-D5.05 ASA: (quietly) "Held." (beat) "He was nine stone wet. Held what?"
  > [TWN_HESSA_HEARD] "Hessa says two Bredes carried, and one went on toward the far gate."   → TWN-D5.06
  > [TSW_closure_rubbing] "The gatehouse wall kept names too."   → TWN-D5.07
  > "That's what I found."                                        → TWN-D5.08
TWN-D5.06 MAERA: "Two Bredes. One name." (beat) "Go on."      → TWN-D5 options
TWN-D5.07 MAERA: "I've read the rubbing. No Brede on it." (beat) "That's not nothing either. Go on."   → TWN-D5 options
TWN-D5.08 MAERA: "Three that disagree, honestly. That's more than two that agree, and less." (to the player) "How would you cut it?"
  > "Cut what the family says and where the rim names him. Both are honest."   → TWN-D5.10
  > "Cut what Asa's mother said. The rim keeps its own."                     → TWN-D5.20
  > "Cut the name. Leave the line under it uncut, until somebody knows."     → TWN-D5.30
TWN-D5.10 MAERA: "Two roads on one stone. The rim won't like it. The rim isn't asked."
TWN-D5.11 ASA: "Shatterfall on his stone." (beat) "If it's true it's true."   {set TWN_CUT_BOTH} → TWN-D5.40
TWN-D5.20 MAERA: "The family's words. A family can keep its words. I'll keep the rest."
TWN-D5.21 ASA: "Good. Mother would like that."               {set TWN_CUT_FAMILY} → TWN-D5.40
TWN-D5.30 MAERA: "A stone that waits." (beat) "We've never had one. We've needed one."
TWN-D5.31 ASA: "I won't see it filled." (beat) "I've seen worse than a blank."   {set TWN_CUT_OPEN} → TWN-D5.40
TWN-D5.40 MAERA: "Then find me a stone that doesn't lie about itself. Strike it. A true one rings."
       {event: S06 complete}
```

```
TWN-D6 (Maera's cairn-hands at the ledge; crew alternative for S08)
TWN-D6.01 CAIRN-HAND: "Split it ourselves? Overnight. Keep vigil at the wall if you like. Somebody should."   → end {enable keep_vigil}
```

**Stone texts (prop decals by choice)**

| Flag | Lines |
|---|---|
| `TWN_CUT_BOTH` | SIG BREDE / went over the pass / named at Shatterfall |
| `TWN_CUT_FAMILY` | SIG BREDE / went over the pass |
| `TWN_CUT_OPEN` | SIG BREDE / (smooth band, uncut) |

```
TWN-D7 (after the set; S11)
TWN-D7.01 ASA: (as the snow goes out of the letters) "That's the wind."
TWN-D7.02 MAERA: "Yes."
TWN-D7.03 ORM: (still looking at the wall) "Gran. Your slips." (Asa has already put them in the niche.)
TWN-D7.04 MAERA: (to the player) "We don't know what happened to him. We know his name is cut. Those are different things. Both are worth doing."
TWN-D7.05 [TWN_HESSA_HEARD] MAERA: "If the one who went on was Sig, then somewhere past the far gate he was still carrying."
TWN-D7.10 MAERA: "Some who went over were never heard of on this side. Other places keep books. Maybe one day someone reads them." (beat) "Not today."
       {set TWN_MIRE_HOOK}
TWN-D7.11 ASA: "Next spring I'll come up and not bring slate. I'll have to bring something. I'm not coming up with nothing."
       {event: TWN-D7 end → quest Completed}
```

**Barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TWN-B1.01 | Hushfold after completion, `TWN_CUT_BOTH` | HUSHFOLD HOUSEHOLD | "Two places for one man. That's more than most of us get." |
| TWN-B1.02 | `TWN_CUT_FAMILY` | ORM | "Gran sleeps better." |
| TWN-B1.03 | `TWN_CUT_OPEN` | HUSHFOLD HOUSEHOLD | "There's a stone up there with a blank on it. Asa says it's the most honest stone on the wall." |
| TWN-B1.04 | Wall, any outcome | CAIRN-HAND | "First chisel a walker's held on this wall. Maera watched every cut. She does that." |

### 3.16 Mystery ledger

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **What happened to Sig Brede** | **Unresolved by design [PROPOSAL — DIRECTOR].** Thornfell content never settles it. | He went over the pass (family); lost in the gorge storm (rim); held (Maera's list). | Slip; Maera's list; rim name; the roster's rotted margin; Hessa; the phrase; optionally the gatehouse wall's silence. | The family invented a story to cover a deserter; the snow in the letters means he is "home". | Which Brede is which. | Thornfell resolves the stone, not the fate. R14 (Mire, optional) may add a later record. |
| **The snow in the letters** | Fresh-cut edges catch blown snow; old weathered faces do not. Nobody says so. | The wind. | Only the behaviour. | The dead answered. | Nothing to withhold. | None. |

### 3.17 Open decisions and review log

**Open:** (1) The "open stone" is a [NEW] practice; the Director may decline it, leaving two options. (2) No Act II change is needed (independent review: the roster is read exactly as Act II gives it). (3) The Mire end of the case belongs to the Register shared civilian ledger (Review and Authoring Sequence, follow-up item 3).

**Review log:** First draft let the roster's "up" line prove Sig survived; corrected with the two-Bredes testimony and the phrase's double meaning, so dignity rests on the cut stone and uncertainty stays. First draft carried the roster to the wall; changed to read-in-place (quest-item rule; the roster's custody is TF-M3's outcome). The ringing run says nothing and is answered only by "That's the wind." / "Yes." Maera decides every cut (anchor authority); the player recommends. No casualty count, no hornman, no Mire fact. TWN unlocks after TF-M3, so the roster always exists.

---

## 4. TSN — The Snow-Height Mark

### 4.1 In one paragraph

Black Glass Hostel was a siege infirmary once; now it is the one roof on the Stormwake road where nobody wears colours past the peg-board. When a drift buries its door, whoever digs it out from inside cuts the snow's height into the drift post with their initials. The player is caught there by a drift and wakes to the hall gone blue: snow over the black-glass panel in the door, light coming through it sideways along the post. In that raking light, beside the highest mark on the post, initials **B.S.**, the wood has been scraped flat, and the scrape shows like writing under water. The hostel hand Ylva Skarde, whose gran was B.S., has never noticed it. Her family's story of the Long Drift is simple: Gran dug Black Glass out alone, and Da's leg healed crooked because there was nobody to set it. Halla Quern, the keeper, says old wood splits. The player digs the door out, drives a wolf off the goat pen, cuts this year's mark with Ylva, and then reads the post again by lamplight, low and sideways: a second set of initials, **M.V.**, and a tiny stitched cross. In the closed ward below, the hostel's old daybook records the Long Drift: a boy's leg set "by the traveller, M.V., of Emberholt, medic, going home"; the door dug "from within by B. Skarde and the traveller"; and, the next season, "mark scraped at B. Skarde's asking. No colours on the door." In the back cover, in a child's hand, someone copied the scraped mark so it would not be lost. Halla was twelve. She held the lamp. The player decides what the post says now.

**What the player should remember:** a blue room, and a scrape that turned into letters. **What they might want next:** nothing in particular; this one ends where it began.

### 4.2 Summary card

| Field | Value |
|---|---|
| Type | Memory/lore (Phase 1.5). Part 3 proposal: Black Glass Hostel's erased snow-height mark [RETAIN AS OPTION]. |
| Unlock | TF-M2 Completed (`TH_SEASON` = snow). |
| Length | 30–40 minutes. |
| Core verb | **read, ask, choose**. Identity: reading a surface by light (snowlight, then a lamp at three angles); a dig-out from inside under drift; asking people who each hold one piece. |
| Combat | ~10%: one required Ridge Wolf pair at the goat pen after the dig-out. |
| Skills | None required. Crew alternative for the dig. |
| NPCs | Halla Quern [NEW, bible]; Ylva Skarde, about fifteen, hostel hand [NEW]; Aske Skarde, her father, of Nettlehook (optional epilogue) [NEW]; a Blood-Oath carter and a Hearthguard drover (guests, minor). |
| Choice | What the post says now (3 options; quest-local). |
| Unlocks | Black Glass ward as an explorable room; the drift post with the player's own mark; Halla's hearth as a safe point. |
| **Anchor** | Black Glass Hostel and its no-colours rule; one Nettlehook household. |
| **World-truth row** | H23 (thirty years of uneven recovery: debt, grudges, help unthanked). The Long Drift is a recovery-years winter, not a war event. |
| **Revelation role** | **Self-contained.** It revises one family's story, not the war's moral ledger. Plants nothing. |
| **Recurring evidence** | The hostel daybook (custodian: Halla, a neutral house) and the scraped drift post (place). They agree. Emberholt: one person, no institution, no Remnant. |
| **State compliance** | Inactive/Active/Completed. The drift waits on the player's hearth wait; the dig cannot fail. Outcome in quest-local `TSN_*`; no fail path. |

### 4.3 Canon grounding

| Element | Source | Use here |
|---|---|---|
| Black Glass Hostel: a siege infirmary kept as a neutral shelter; no-colours rule protects travellers but conceals individual acts of care | Part 3 proposal [NEW; adopted by bible TD-4] | The place; the erased mark. |
| "An erased snow-height mark suggests an Emberholt medic helped during a crisis; it proves no wider absolution"; "revises a specific family story, not the war's moral ledger" | Part 3 proposal | The quest's limit. Aske says it outright. |
| Halla Quern: keeps everyone's secrets including her own | Bible §5.2 | She held the lamp; she copied the mark. |
| Emberholt distrusted rationally, never caricatured | Bible §5.3 rule 6; dossier §XXI.5 | Guests' lines; Aske's last line. |
| An Emberholt arrival may prefer a private cooling pause after anger | Part 3 proposal (migrant and mixed households) | The daybook's one detail about the medic. |
| Ridge wolves, winter-thin | Bible §10 | TSN-E1. |
| No Remnant presence in Thornfell | Bible §2.3; FT-04 bounded reach | The medic is a person going home; nothing else. |

### 4.4 The place: Black Glass Hostel (TP05)

**MAP VERIFICATION REQUIRED:** the hostel door must face the prevailing drift so a bad night buries it; the goat pen and woodstack lie on the lee side; the ward's outer stair opens only once the drift is dug.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. The hall** | Hearth wait; safe point. | One long room, benches along the walls, a hearth in the middle. A peg-board inside the door hung with clan cloaks, badges and a red armband, all taken off on the way in. A hand-lettered board: *Colours on the pegs. Hands in here.* |
| **B. The door and drift post** | The marks. | A heavy door that opens **inward** (high-country hostel doors do, so you can dig out) [NEW]. Set in it, a panel of black glass from the slope, dark and smoky, a hand thick. Beside it, the drift post: notches at different heights, each with initials; the highest has **B.S.** and, beside it, a hand-sized patch scraped flat. |
| **C. The goat pen and woodstack** | Wolves. | Lee side; hurdles, a byre, split wood. Tracks round it in the morning. |
| **D. The old ward** (below) | The daybook. | Reached by an outer stair under the drift side, door locked. Long room, iron bunk frames, a wall of wooden hook-tags numbered not named, a cold store, a cabinet. Snow sifted through a vent in a neat cone. |
| **E. Nettlehook, the Skarde house** (optional) | Epilogue. | Longhouse end. Aske's stick by the door; he does not use it in the house. |

### 4.5 Beats

**Beat 0 — In or out (`S00_offer`).** *Objective: Shelter at Black Glass Hostel.* Halla at the door (TSN-D1). The player hangs nothing on the pegs unless they want to (cosmetic interaction **Hang your colours**). **Wait out the drift** at the hearth (keep-watch contract; presentation hour runs to the morning after a drift).

**Beat 1 — Snowlight (`S01_snowlight`) — the strange moment.** *Objective: Look at the door.* The player wakes to the hall gone blue. See §4.7. The step completes on the inspect of the scraped patch in snowlight. Ylva (TSN-D2) has never noticed it: "I've walked past that post a thousand times."

**Beat 2 — Dig out (`S02_dig`).** *Objective: Dig the door out.* The door opens inward onto a wall of snow. **Dig** (3 segments, 4 s each, progress kept) and **Set a shoring board** between segments. While the tunnel is open, gusts come (whistle tell through the panel, 1.5 s); a segment dug without its board slumps on the gust and loses that segment's progress (only that segment). Crew alternative: ask the guests (TSN-D3): the carter and the drover dig, arguing; it takes one more hearth wait.

**Beat 3 — The pen (`S03_pen`).** *Objective: See to the goats.* Outside, two winter-thin wolves at the pen (TSN-E1). Halla's goats are counted after: all there (TSN-B3.01).

**Beat 4 — The mark (`S04_mark`).** *Objective: Cut this year's mark.* Custom: whoever dug cuts the height. With Ylva: **Cut the notch** (3 s) at this drift's line (lower than B.S.). If the crew dug, Ylva cuts it and puts the player's initials beside it anyway ("You held the shovel once. Counts."). Ylva asks Halla about the scrape; Halla: "Old wood. Splits." (TSN-D4).

**Beat 5 — Low light (`S05_lamp`).** *Objective: Read the post by lamplight.* After dusk (hearth wait to dusk, or simply after S04 if the presentation hour is already late). Take the hall lamp. **Hold the lamp** at three marked positions on the post (high, level, low-to-the-side); only the low side angle shows the scraped patch: a second set of initials, **M.V.**, and a small cross cut like a stitch. Each position gives an inspect; the low one completes the step.

**Beat 6 — Ask (`S06_ask`).** *Objective: Ask who M.V. was.* Three people, any order; two required. **Ylva** (the family story: Gran dug them out alone; Da's leg healed crooked; TSN-D5). **The carter** (Brunhild Skarde's dig-out is a road story: "dug Black Glass out alone, and a fire-folk traveller sat by the hearth and let her"; TSN-B6.01). **Halla** (refuses; then gives the ward key "so you'll stop asking me"; TSN-D6). The key is guaranteed on asking Halla once after the lamp step.

**Beat 7 — The ward (`S07_ward`).** *Objective: Find the hostel's daybook.* Down the outer stair (cleared by the dig). The ward is dark, cold and quiet. Inspects: hook-tags, bunk frames, snow cone. The cabinet holds the daybook. Required: **TSN-I1 the Long Drift pages**. Required: **TSN-I2 the back cover** (the copied mark in a child's hand). Optional: earlier pages from the siege-infirmary years (closed: *"Earlier pages are the infirmary's. You leave them shut."*).

**Beat 8 — Halla (`S08_halla`).** *Objective: Bring the daybook to Halla.* TSN-D7: Halla tells what she must, briefly. Her mother scraped it at Brunhild's asking. Halla held the lamp. She copied it. She does not know where M.V. went.

**Beat 9 — The post (`S09_choose`).** *Objective: Decide what the post says.* With Halla and Ylva at the post (TSN-D8). See §4.10.

**Optional epilogue — Nettlehook (`S10b_aske`).** Available if the outcome told the family. Aske Skarde (TSN-D9) revises his story and not the war. The quest completes on TSN-D8's end node; the epilogue is optional after completion and sets `TSN_ASKE_HEARD`.

### 4.6 Encounters and hazards

| Id | Enemies / hazard | Placement | AI role | Telegraph (timings) | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TSN-E1** | 2 × Ridge Wolf runner | Goat pen hurdles, lee side | Harass the pen; turn on the player when approached; break off at 30% HP and flee (winter-thin animals). | Crouch, ears flat (**0.8 s**), then a 3 m lunge. One circles to the player's back while the other faces; a low growl (**1.0 s**) marks the circler's lunge. | Morning-after danger; ordinary winter. | Required. Ends at 75–90% HP on a Competent-identity character. Fleeing counts as done. |
| **TSN-H1** | Tunnel slump | The dig-out tunnel | Environmental. | Whistle through the black-glass panel rises a fifth (**1.5 s**), gust (**3 s**). | Pace the dig; teach shoring. | An unshored segment slumps: that segment's progress resets. No damage. |

**Rules.** Respawn point: the hostel hearth. Nothing the wolves drop advances the quest.

### 4.7 The strange moment: snowlight (presentation spec)

| Element | Spec |
|---|---|
| Trigger | The drift wait ends (server event `tsn.snowlight`); the player wakes in the hall. |
| Duration | Persists until the dig opens the door (S02), then fades over ~3 s as daylight comes in. |
| What it shows | The whole hall is lit a deep, still blue, from the black-glass panel, with the snow pressed against it outside. The light comes in low and sideways and runs along the drift post. In it, every notch on the post throws a hard shadow, and beside B.S. the scraped patch shows faint lines like writing seen through water: no letters can be read, only that something was there. |
| Audio | The storm is gone. Hall sounds are close and muffled: the hearth, a guest snoring, a goat complaining somewhere. Nobody speaks until the player moves. |
| Reactions | Halla is already up, sitting on the bench by the door, looking at the post. When the player looks at her, she gets up and puts wood on the fire. |
| UI / camera | None / player-controlled. |
| After | Post inspect (during snowlight): *"Beside B.S., the wood is scraped flat. In this light the scrape has lines in it. Not letters. Not nothing."* |
| What it means | Nothing the quest states. It is light through snow and glass. The letters are proved by the lamp, the daybook and its copy, not by the light. |

### 4.8 Steps

| Step | Objective | Completes on | Required |
|---|---|---|---|
| `S00_offer` | Shelter at Black Glass Hostel. | TSN-D1 end + `wait_drift` | Yes |
| `S01_snowlight` | Look at the door. | Scraped-patch inspect during `tsn.snowlight` → TSN-D2 end | Yes |
| `S02_dig` | Dig the door out. | 3 × `dig_segment` (+ boards), or TSN-D3 + `wait_hearth` | Yes |
| `S03_pen` | See to the goats. | TSN-E1 defeated or fled | Yes |
| `S04_mark` | Cut this year's mark. | `cut_notch` (or Ylva's cut) → TSN-D4 end | Yes |
| `S05_lamp` | Read the post by lamplight. | `hold_lamp` at the low position + inspect | Yes |
| `S06_ask` | Ask who M.V. was. | 2 of 3: TSN-D5, TSN-B6.01 talk, TSN-D6 (Halla gives key on D6) | Yes |
| `S07_ward` | Find the hostel's daybook. | TSN-I1 + TSN-I2 inspects | Yes |
| `S08_halla` | Bring the daybook to Halla. | TSN-D7 end | Yes |
| `S09_choose` | Decide what the post says. | TSN-D8 choice → end → Completed | Yes |
| `S10b_aske` | (Optional) Visit the Skardes. | TSN-D9 end | No |

### 4.9 Flags

| Flag | Set by | Read by |
|---|---|---|
| `TSN_CREW_DUG` | TSN-D3 | TSN-D4 variant (Ylva cuts) |
| `TSN_RECUT` / `TSN_TOLD_HOUSE` / `TSN_LEFT` | TSN-D8 (exactly one) | Post prop; Halla and Ylva barks; TSN-D9 availability |
| `TSN_ASKE_HEARD` | TSN-D9 | Nettlehook ambient bark |
| `TSN_COMPLETE` | Completion | None outside this package |

### 4.10 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Cut it again** — *"Put M.V. back beside B.S. Hands, not homes."* | Halla re-cuts the initials and the small stitch-cross. Nothing says Emberholt. | Halla breaks her mother's word to Brunhild. The Blood-Oath carter says he'll use another roof (he comes back next storm; there isn't one). The Skardes will see it every time they pass. | Ylva reads the post to new guests. Aske can visit (epilogue). Post inspect: *"B.S. and M.V., side by side at the highest mark. Two hands dug this door."* |
| **Tell the house** — *"The post stays. Ylva takes the copy home."* | Ylva copies the back-cover line onto a slip and takes it to Nettlehook. The post stays scraped. | The hostel keeps a scrape it no longer needs to; Halla keeps one secret fewer and one habit more. | Aske can visit (epilogue). Ylva: "Da read it twice and put it in his tobacco tin. That's where he keeps things he means." |
| **Leave it** — *"Brunhild asked. Let it stay asked."* | The daybook goes back in the cabinet. Halla thanks the player, briefly. | Ylva knows there is something and not what; she is angry for a while. The family story stays as it is. | Ylva, later: "I'll find out when I'm keeper. She knows I will." No epilogue. |

None is wrong. In every case the daybook says the same thing.

### 4.11 Rewards

| Reward | Type | Notes |
|---|---|---|
| **Your mark on the drift post** | Place | Per-player prop: the player's initials at this year's height. |
| Black Glass ward | Access | An explorable room; a quiet place to wait out storms (second hearth-wait point). |
| **Hostel lamp-hook** | Tool (functional) | A carry lamp for low-light inspects; item pass to define. |
| Small payment | Small payment | Halla pays diggers in bread and coin. |
| Skill XP | Action only | From TSN-E1. No lump quest XP. |

### 4.12 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player leaves before the drift | Active at `S00`; resume hook: Halla ("Door shuts at the drift. Still in or out?"). |
| Player leaves after the dig | The door stays dug for this player; the hall is daylight; the snowlight cannot replay (inspects use the lamp). |
| Segment slumps | Only that segment resets. |
| Death | Respawn at the hearth; steps kept. |
| Co-op | Each player has their own drift and snowlight (per-player presentation hour). Partners waking in the same hall see their own presentation; if one has already dug, the other's door is still buried in their own instance. Fallback if per-player props are not ready: the door is dug for everyone after the first player's S02, later players' S02 completes on talking to Ylva at the open door, and the snowlight plays as a short client-side effect on their first entry after `S00`. Post prop fallback: scraped (the `TSN_LEFT` state) for everyone; outcomes carried in dialogue and barks. |

### 4.13 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Hearth wait into a drift morning; a dusk wait | Systems Engineer | Shared keep-watch contract. |
| Snowlight lighting state (per player) | Art / Systems | A lighting preset swapped on `tsn.snowlight`, ended on S02; decal on the post visible only under it (and under the lamp's low position). |
| Lamp held at marked positions | Gameplay Designer | Three interaction points; each shows a different decal visibility. |
| Dig-out channel with boards and slump | Gameplay Designer | Segmented channel; a "board" interaction between segments; a gust timer resets the current unboarded segment. |
| Per-player drift door and post props | Systems Engineer | Step/flag-conditioned props; fallback above. |

### 4.14 Cast notes and dialogue

**Halla Quern [NEW, bible].** *Knows:* everything in the daybook; that she held the lamp; that she copied the mark. *Does not know:* where M.V. went, or whether she got home. *Voice:* keeps secrets by answering a different question. Not cold; private.

**Ylva Skarde [NEW].** *Knows:* the family story; every notch on the post except this one. *Does not know:* any of the rest. *Voice:* quick, direct, impatient with adults who say "old wood".

**Aske Skarde [NEW].** *Knows:* he was twelve, fevered, and a woman counted out loud while she did something to his leg. He thought it was Gran. *Voice:* slow, fair, stubborn about the war.

**Guests (minor).** The Blood-Oath carter tells the road version; the Hearthguard drover says the hostel rule out loud. Both take off their colours at the pegs and grumble about it.

```
TSN-D1 (Halla at the door; S00)
TSN-D1.01 HALLA: "Door shuts at the drift. In or out, walker."
  > "In."                                           → TSN-D1.02
  > "What's the board say?"                         → TSN-D1.04
TSN-D1.02 HALLA: "Colours on the pegs. Hands in here. Hearth's for everyone. Snoring's for that one." (the carter)
TSN-D1.03 HALLA: "If it drifts, whoever digs us out cuts the height. That's the only rule I didn't make."   → end
TSN-D1.04 HALLA: "It says what it says. This was an infirmary. People bled the same colour in here."   → TSN-D1.02
       {event: D1 end → enables wait_drift}
```

```
TSN-D2 (Ylva, at the post in the snowlight; S01)
TSN-D2.01 YLVA: (whispering, for no reason) "It's all blue."
TSN-D2.02 YLVA: "That's Gran. B.S. Highest one. She dug us out of the Long Drift by herself."
TSN-D2.03 YLVA: (leaning close) "What's that next to it? I've walked past that post a thousand times."
  > "Something was scraped off."                    → TSN-D2.04
  > "Ask Halla."                                    → TSN-D2.05
TSN-D2.04 YLVA: "Who scrapes a mark? That's like scraping a name."   → TSN-D2.05
TSN-D2.05 YLVA: (looks at Halla's back) "She's putting wood on. She does that when she's not answering."   → end
```

```
TSN-D3 (the guests; crew alternative for S02)
TSN-D3.01 CARTER: "Dig? I'm a guest."
TSN-D3.02 DROVER: "You're a guest who wants to leave."
TSN-D3.03 CARTER: "...Give me the shovel. Not that one, the good one."   {set TSN_CREW_DUG; enable wait_hearth} → end
```

```
TSN-D4 (at the post after the dig; S04)
TSN-D4.01 [else] YLVA: "You dug, you cut. Here." (hands over the knife) "Lower than Gran's. Everyone's lower than Gran's."
TSN-D4.01 [TSN_CREW_DUG] YLVA: (cutting it herself) "They dug. You held the shovel once. Counts." (adds the player's initials)
TSN-D4.02 YLVA: (louder, to the hearth) "Halla. What was scraped off next to Gran?"
TSN-D4.03 HALLA: "Old wood. Splits."
TSN-D4.04 YLVA: (to the player, flat) "Old wood. Splits."   {event: S04 complete} → end
```

**Lamp inspects (S05)**

| Position | Text |
|---|---|
| High | "The lamp lights the post flat. The scrape is only a pale patch." |
| Level | "A little shadow in the patch. Nothing you could read." |
| Low, to the side | "Light runs along the wood and catches the bottoms of old cuts. Beside B.S.: **M.V.** And a tiny cross, cut like a stitch." |

```
TSN-D5 (Ylva, after the lamp; S06)
TSN-D5.01 YLVA: "M.V.? There's no M.V. in our house. There's no M.V. anywhere I know."
TSN-D5.02 YLVA: "The story's simple. Long Drift. Door shut nine days. Gran dug us out alone. Da's leg healed crooked because there was nobody to set it."
TSN-D5.03 YLVA: "He tells it every First Smoke. He does the voice for the snow."   → end
```

**Barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSN-B3.01 | After E1 | HALLA | "Eleven goats. Eleven. Good." |
| TSN-B6.01 | Talk to the carter after S05 | CARTER | "Brunhild Skarde? Dug Black Glass out alone in the Long Drift. Everyone knows. Fire-folk traveller sat by the hearth and let her, the way I heard it." |
| TSN-B6.02 | Same, follow-up | DROVER | "The way you heard it from who?" |
| TSN-B6.03 | Same | CARTER | "From everyone. That's how you hear things." |
| TSN-B9.01 | `TSN_RECUT`, later visit | HALLA | "Two hands dug that door. Post says so now." |
| TSN-B9.02 | `TSN_LEFT`, later visit | YLVA | "I'll find out when I'm keeper. She knows I will." |

```
TSN-D6 (Halla, after the lamp; S06)
TSN-D6.01 HALLA: "You've had the lamp down by the post."
  > "Who was M.V.?"                                 → TSN-D6.02
TSN-D6.02 HALLA: "Somebody who isn't here."
  > "That's not an answer."                         → TSN-D6.03
TSN-D6.03 HALLA: "No." (beat; she takes a key off her belt) "Ward's below. The book's in the cabinet. Read it so you'll stop asking me."   {give ward access} → end
```

**Documents**

TSN-I1 — *Black Glass daybook, the Long Drift pages (several hands; the main hand is the keeper's, Halla's mother):*

> *Long Drift. Door shut. Nine guests, two goats inside, one horse in the byre.*
> *Day two. Skarde boy, twelve, leg broke on the ice by the byre. Set by the traveller, M.V., of Emberholt, medic, going home. She asked for the cold room after, alone, a while. Gave it.*
> *Day six. Boy's fever broke.*
> *Day nine. Door dug from within by B. Skarde and the traveller. Marked.*
> *Thaw. Traveller gone down the road. Paid in bandage-linen.*
> (Next season, the keeper's hand:) *Mark scraped at B. Skarde's asking. No colours on the door.*

TSN-I2 — *Daybook, inside the back cover (pencil, a child's hand, small):*

> *B.S. M.V. + so it isnt lost.*

Ward inspects:

| Object | Text |
|---|---|
| Hook-tags | "Wooden tags on hooks, numbered, never named. Infirmary habit. Nobody's colours on a sick man's hook." |
| Bunk frames | "Iron frames, no mattresses. Thirty of them. Some have the rust worn off where hands gripped." |
| Snow cone | "Snow sifted through a vent into a perfect cone. Nobody's been down here since autumn." |
| Earlier pages | "Earlier pages are the infirmary's. You leave them shut." |

```
TSN-D7 (Halla, with the daybook; S08)
TSN-D7.01 HALLA: (sees the back cover, and is quiet for a moment) "I was twelve. I held the lamp. Twice."
TSN-D7.02 HALLA: "Once when she set his leg. Once when Mother scraped the post. Brunhild asked. 'No fire-folk letters on a door I dug.'"
TSN-D7.03 HALLA: "Mother said the rule covered it. No colours on the door. I thought initials weren't colours. So I wrote it in the back."
  > "Where did M.V. go?"                            → TSN-D7.04
  > "Why keep it secret this long?"                 → TSN-D7.05
TSN-D7.04 HALLA: "Down the road at thaw. Home, she said. I don't know if she got there. I don't know her whole name."   → TSN-D7.06
TSN-D7.05 HALLA: "Brunhild was alive. Then she wasn't, and it felt worse to say it after."   → TSN-D7.06
TSN-D7.06 HALLA: "Now you know. Ylva will want to. Come to the post."   {event: S08 complete} → end
```

```
TSN-D8 (at the drift post; Halla, Ylva; S09)
TSN-D8.01 YLVA: "So Gran didn't dig alone."
TSN-D8.02 HALLA: "Your gran dug. She just wasn't the only one."
TSN-D8.03 YLVA: (to the player) "What does the post say? You found it. You say."
  > "Cut it again. Hands, not homes."               → TSN-D8.10
  > "The post stays. Take the copy home to your da."   → TSN-D8.20
  > "Brunhild asked. Let it stay asked."            → TSN-D8.30
TSN-D8.10 HALLA: (takes the knife) "Hands, not homes. That's the rule if we'd read it properly." (cuts M.V. and the small cross)
TSN-D8.11 YLVA: "Two hands dug this door."     {set TSN_RECUT} → TSN-D8.40
TSN-D8.20 YLVA: (copying the line onto a slip) "Da reads things twice when they matter."
TSN-D8.21 HALLA: "The post can keep its scrape. It's used to it."   {set TSN_TOLD_HOUSE} → TSN-D8.40
TSN-D8.30 HALLA: (puts the book under her arm) "Thank you." (beat) "I mean that more than I'd like."
TSN-D8.31 YLVA: "That's not fair." (beat) "I'll find out properly when I'm keeper."   {set TSN_LEFT} → TSN-D8.40
TSN-D8.40 HALLA: "Door shuts at the drift. You know where the shovel is."
       {event: D8 end → quest Completed}
```

```
TSN-D9 (Nettlehook, Aske Skarde; optional; requires TSN_RECUT or TSN_TOLD_HOUSE)
TSN-D9.01 ASKE: "Ylva says a fire-folk medic set my leg." (beat) "Somebody counted out loud while it hurt. I thought it was Mother."
TSN-D9.02 ASKE: "Maybe it was both of them counting." (taps the leg) "Healed straight, near enough. I've been telling it crooked thirty winters."
  > "Does it change anything?"                      → TSN-D9.03
TSN-D9.03 ASKE: "Changes my story. Gran dug us out. With help. I'll say it that way at First Smoke."
TSN-D9.04 ASKE: "Doesn't make the forges right. Doesn't make the war anybody's but whose it was." (beat) "It was one woman, one winter, one leg. I'll thank one woman."
       {set TSN_ASKE_HEARD} → end
```

### 4.15 Mystery ledger

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The scraped mark** | M.V., an Emberholt medic going home, set the Skarde boy's leg and dug the door out with Brunhild in the Long Drift; Brunhild had the mark scraped. | Brunhild dug Black Glass out alone. | Post under lamp; daybook entries; back-cover copy; Halla's testimony. | The scrape hides a crime; or it absolves Emberholt of the war. | M.V.'s full name and fate. | TSN (resolved locally). |
| **The snowlight** | Light through snow and smoky glass. Not stated. | — | Only the behaviour. | The post "showed" the letters. | — | None needed. |

### 4.16 Open decisions and review log

**Open:** (1) Part 3 suggested the second custodian be "a neutral care account from another region"; this package uses the hostel's own daybook (a neutral house's care account) to keep TSN self-contained. The Director may prefer an Emberholt-side record later; nothing here blocks it. (2) The inward-opening door custom is [NEW].

**Review log:** First draft gave the medic an Emberholt guild sign on the post; cut (it would read as an institution vouching for itself, and as a colour under the hostel rule). Now initials and a stitch-cross only. Aske's last line holds the limit: one woman, one winter, not the war. No Remnant, no embercraft, no institution named. The snowlight shows only that something was there; the lamp, book and copy prove what. Halla's secret is her own (the copy), matching her bible voice note.

---

## 5. TOS — Oathkeeper's Step

### 5.1 In one paragraph

On the oath path above the Oath Cairn Fields there is one stone step that never crumbles. The story says it "tests the honest": swear on it in a hard wind and the wind remembers; lie, and you fall. Inga Fellstrand and Joar Stannick mean to swear on it in the next storm. The cairn fields' path-warden, Ottar Lund, means to rope the path off, because this autumn the stones either side of the step have started to go: a goat went over last week. The step itself has not moved. The player walks the path and finds the step is not like the others: one dressed block, bedded deep, joints running into the rock. Standing on it and shouting into the cleft below, the echo comes back in one beat: there is a hollow right under the path. Climbing down beneath shows why: the step is the keystone of an old buried arch spanning the cleft; the path was laid on its back long after. In a gust, the arch hums, and two loose stones in one haunch rattle. They are not lost: the two that fell this autumn lie in the shale below, among vipers. Kaldren Deepdelver, asked, reads the stresses and nothing else: the load goes through the middle stone into both sides, and one side has been robbed. The player hauls the fallen stones back up and reseats them in wind windows. Then the storm comes, and the couple walk out to swear. On the step, the gale's roar drops away. They can hear each other say it in ordinary voices. Afterwards the player decides what to tell them, and who should know what the step is.

**What the player should remember:** a storm going quiet underfoot. **What they might want next:** to stand on it again in the next storm.

### 5.2 Summary card

| Field | Value |
|---|---|
| Type | Environmental discovery (Phase 1.5). Dossier §XII "Oathkeeper's Step" [CANON myth]; Part 3 reading "may preserve a tested route". |
| Unlock | TF-M1 Completed. |
| Length | 25–35 minutes. |
| Core verb | **climb, test, listen**. Identity: echo count to find a hidden void; listening for a rattle in a humming arch; haul-and-reseat repair in wind windows; a null-point in a storm. |
| Combat | ~10%: a Rock Viper nest in the shale under the arch (required, small). |
| Skills | None required. Crew alternative for the haul (Ottar's warden crew). |
| NPCs | Inga Fellstrand and Joar Stannick (the couple) [NEW]; Ottar Lund, path-warden (Ridge Warden) [NEW]; Kaldren Deepdelver [CANON anchor] (optional, stresses only). |
| Choice | What the player tells, and to whom (3 options; quest-local). |
| Unlocks | The oath path repaired (a shorter walk to the upper Cairn Fields and the Name-Stone Wall); the step as a storm place the player can return to. |
| **Anchor** | The Oath Cairn Fields and the oath-giving custom; Echohewn keeping (Kaldren, stresses only). |
| **World-truth row** | None (present-day). Background H05 (Echohewn works) only as unexplained old work. |
| **Revelation role** | **Self-contained.** Echoes the null-point lesson (TDS01, TF-M4) without explaining it. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive/Active/Completed. The storm waits on the player's wait at the path cairn; a stumble returns the player to the last stance. Outcome in quest-local `TOS_*`; no fail path. |

### 5.3 Canon grounding

| Element | Source | Use here |
|---|---|---|
| A single stone step on a dangerous path that never crumbles; said to test the honesty of those who cross | Dossier §XII [CANON myth] | The keystone; the oath custom. |
| Oath Cairn Fields: places for oath-giving; wind can seem to "answer" | Dossier §V.4 [CANON] | The couple's storm oath. |
| Torvek: "the wind remembers vows" | Anchors II [CANON] | The couple quote it; Torvek does not appear. |
| Null-points: Echohewn sound-dead pockets; dust falls straight; footsteps vanish | Bible §1.1, §2.1 [CANON] | The step in a storm. Never named as such by anyone here. |
| Echo count | Bible §1.1 | One beat back from the cleft: a void close below. |
| Kaldren: stresses and alignments, never origins; cannot validate an account | Anchors III; Part 4 ledger | His one scene. |
| Rock vipers: shale ambushers | Bible §10 | TOS-E1. |

### 5.4 The place: the oath path (TP16)

**MAP VERIFICATION REQUIRED:** the cleft under the step must be reachable on foot from the cairn field below (fallback route) and by a down-climb from the path (agility); the path must link the lower fields to the upper field by the Name-Stone Wall.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Path foot and cairn** | Offer; storm wait; safe point. | A waist-high cairn with ribbons and stormflower stems tucked into it. Ottar's coil of rope and stakes. A goat's broken tether on a stake. |
| **B. The oath path** | Approach. | A narrow shelf path of laid stones across a cliff face. Fresh gaps where two stones went. Grit on everything. |
| **C. The step** | The myth. | One dressed block, wider than the path stones, with clean joints that run back into the rock. A shallow wear-hollow in the middle where centuries of feet have stood still. Ribbons tied to an iron ring above it. |
| **D. Under the arch** | The proof. | Down the cleft (agility down-climb, or the long walk round from the field and up the scree). Overhead, a curve of dressed stones: an arch, its middle stone the step's underside. One haunch has two empty sockets. Shale below, and in it two dressed blocks. |
| **E. A nearby cairn** (optional) | Storytelling. | An old cairn whose base stones carry the same tool marks as the arch. Somebody borrowed stone here, long ago. |

### 5.5 Beats

**Beat 0 — A rope across the path (`S00_offer`).** *Objective: Hear out the couple and the path-warden.* TOS-D1. Ottar wants the path shut; the couple want their storm oath; nobody is lying.

**Beat 1 — Walk it (`S01_walk`).** *Objective: Walk the oath path to the step.* Crumbling path stones (TOS-H1) with tells. Inspect the **gaps** and the **step**.

**Beat 2 — Count (`S02_count`).** *Objective: Listen under the step.* From the step, **Call into the cleft** (shout; or the Gather call shape if the player prefers: cosmetic). The echo count is shown in beats (with `TH_CALLS` glyph pacing): **one beat**, with a flat close return. Then from a path stone ten paces on: **four beats**, from the far cleft wall. Inspect: *"One beat from under the step. Something close, right under your feet."* Completes the step.

**Beat 3 — Under (`S03_under`).** *Objective: See what's under the step.* Down-climb (agility; three triggers) or the walk round (field → scree → cleft mouth). Inspect the **arch** and the **empty sockets**. Vipers in the shale (TOS-E1).

**Beat 4 — Listen for the rattle (`S04_rattle`).** *Objective: Find which stones are loose.* Under the arch, wait through gusts (whistle tell). The arch hums in a gust; loose stones rattle, with a trickle of dust as the visual tell. Mark each rattling stone (**Chalk it**, instant). Two rattle beside the empty sockets. The keystone neither hums nor rattles.

**Optional — Kaldren (`S04b_kaldren`).** He is at the path foot (he came to look at the cairn, he says). TOS-D3: stresses only. Sets `TOS_KALDREN_ASKED` (adds a line to the haul).

**Beat 5 — Haul and reseat (`S05_reseat`).** *Objective: Put the fallen stones back.* Two dressed blocks in the shale. For each: **Rig the sheer-legs** (Ottar's poles; 3 s), **Haul** (3 segments, 3 s, progress kept; a gust during a segment pauses it, never undoes it), **Seat the stone** (3 s) in its socket during a calm. Then **Tighten** the two rattling stones (wedge them; 2 × 3 s). Crew alternative: ask Ottar (TOS-D4): his crew hauls; one storm wait later the stones are in.

**Beat 6 — The storm (`S06_storm`).** *Objective: Walk the couple out in the storm.* **Wait for the storm** at the path cairn (keep-watch contract). Lead Inga and Joar along the path in wind windows; they shelter when the player shelters (escort follows the player's stance). The repaired path is sound.

**Beat 7 — The oath (`S07_oath`) — the strange moment.** *Objective: Stand by while they swear.* On the step. See §5.7.

**Beat 8 — What to tell (`S08_tell`).** *Objective: Decide what to tell.* Back at the path foot (TOS-D6). Completed on the choice node's end.

### 5.6 Encounters and hazards

| Id | Enemies / hazard | Placement | AI role | Telegraph (timings) | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TOS-E1** | 2 × rock viper, 1 × shale-coil | Shale under the arch | Ambush; leashed to the shale bed. | Viper: rattle on shale (**1.0 s**), 2 m strike. Shale-coil: shale shivers in a ring (**1.5 s**), then bursts up inside it. | Clears the haul ground; the underside is not for strolling. | Required (they nest on the blocks). Ends at 75–90% HP on a Competent-identity character. |
| **TOS-H1** | Crumbling path stones (pre-repair) | Oath path, 3 stones | Environmental. | Grit trickles and a crack sounds (**1.2 s**) after the player steps on. | The danger Ottar is right about. | If still on it when the tell ends, the stone tips: the player slides back to the last sound stone, small damage. Never off the cliff (path edge blocker). After S05 these stones are sound. |
| **TOS-H2** | Wind windows | Path and arch | Environmental. | Whistle (**1.5 s**), gust (**3 s**). | Pace; and under the arch, the gust is the listening tool. | Pushed against the face; never off. |

**Rules.** Respawn point: the path-foot cairn. Nothing the vipers drop advances the quest.

### 5.7 The strange moment: the quiet step (presentation spec)

| Element | Spec |
|---|---|
| Trigger | The player and the couple are on the step during the storm window (server event `tos.oath`; volume = the step). |
| Duration | Lasts while the player stands on the step; the oath lines take ~15 s. |
| What happens | Stepping onto the step, the storm's roar drops away in one stride to near silence. The wind still tears at cloaks and ribbons; snow still streams past; but the sound is gone. Footsteps vanish. Snow that lands on the step falls straight down and lies still. Stepping off, the roar returns at once. |
| Audio | A dull pressure, very quiet. The couple's voices, ordinary and close. The player's own footsteps silent. No music. |
| Reactions | Inga laughs once, surprised, and then is very serious. Joar looks at his feet. They swear (TOS-D5). |
| UI / camera | None / player-controlled. |
| After | Step inspect: *"In a storm, this stone is quiet. Every other stone on the path is not."* |
| What it means | Nothing the quest states. Nobody calls it anything. Kaldren, if asked afterwards, says it is not a stress question. |

### 5.8 Steps

| Step | Objective | Completes on | Required |
|---|---|---|---|
| `S00_offer` | Hear out the couple and the path-warden. | TOS-D1 end | Yes |
| `S01_walk` | Walk the oath path to the step. | Gap + step inspects | Yes |
| `S02_count` | Listen under the step. | `call_cleft` from the step + from a path stone + inspect | Yes |
| `S03_under` | See what's under the step. | Enter arch volume; arch + sockets inspects; TOS-E1 defeated | Yes |
| `S04_rattle` | Find which stones are loose. | 2 × `chalk_stone` on rattling stones | Yes |
| `S04b_kaldren` | (Optional) Ask Kaldren. | TOS-D3 end | No |
| `S05_reseat` | Put the fallen stones back. | 2 × (`rig`, `haul`, `seat`) + 2 × `tighten`; or TOS-D4 + `wait_storm` | Yes |
| `S06_storm` | Walk the couple out in the storm. | `wait_storm`; escort reaches the step volume | Yes |
| `S07_oath` | Stand by while they swear. | TOS-D5 end (fires during `tos.oath`) | Yes |
| `S08_tell` | Decide what to tell. | TOS-D6 choice → end → Completed | Yes |

### 5.9 Flags

| Flag | Set by | Read by |
|---|---|---|
| `TOS_KALDREN_ASKED` | TOS-D3 | TOS-D4 / haul bark variant |
| `TOS_CREW_HAULED` | TOS-D4 | TOS-D6 Ottar variant |
| `TOS_TOLD` / `TOS_KEPT` / `TOS_WARDEN` | TOS-D6 (exactly one) | Path props (warden marks); barks |
| `TOS_COMPLETE` | Completion | Path repaired state (per player); TWN approach note (§0.4) |

### 5.10 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Tell them** — *"It's the middle stone of an old arch. It carries the path. That's why it doesn't fall."* | The couple hear it. Inga: "Doesn't matter. We heard each other." | Ottar starts calling it "the carrying stone"; the story loses a little of its edge for the next couple. | Path bark: "Carrying stone. Swore on it anyway." |
| **Keep the story** — *"It tests the honest. You passed."* | The couple go home certain. | Nobody knows the haunches matter; the next person who wants a good stone may take one. The repair holds for now. | Ottar keeps his rope coiled at the foot "just in case". |
| **Tell the warden** — *"Leave them the story. Ottar, mark the haunches."* | Ottar cuts a warden's mark on each haunch stone: *Don't lift.* | The player keeps something from people they helped. Joar half-guesses ("You went under it. What's under it?"). | Warden marks visible under the arch (per player). The story and the stone are both kept. |

None is wrong. The step is sound in every outcome.

### 5.11 Rewards

| Reward | Type | Notes |
|---|---|---|
| Oath path repaired | Access | Shorter route to the upper Cairn Fields (per player). |
| The quiet step | Place | In any later storm window, standing on the step repeats the quiet (no dialogue). |
| **Warden's sheer-leg pulley** | Tool | Functional name; item pass to define. |
| Small Warden payment | Small payment | From Ottar. |
| Skill XP | Action only | From TOS-E1. No lump quest XP. |

### 5.12 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player leaves | Active at the persisted step; resume hook: the couple at the path-foot cairn ("Still waiting for weather. And you."). |
| Tipped path stone | Slide back to the last sound stone; never off the path. |
| Haul interrupted | Segment progress kept; a gust only pauses. |
| Death | Respawn at the path-foot cairn; reseated stones stay reseated. |
| Co-op | Per-player storm window and couple. Partners on the step in their own `tos.oath` share the quiet. Fallback if per-player props are not ready: the path is repaired world-wide after the first player's S05; later players' S05 completes on inspecting the reseated stones, and their storm and oath play as normal. |

### 5.13 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Echo count from two points | Gameplay Designer / Audio | Authored echo delay per call point; beat display with glyph pacing. |
| Gust-driven hum and rattle on tagged stones | Audio / Systems | During a gust, play hum on the arch and rattle + dust VFX on tagged loose stones. |
| Null-point volume in a storm (audio duck, straight-falling snow) | Audio / VFX | Volume that ducks storm audio and footsteps and swaps snow particle drift to vertical. Same contract as TF-M4/TDS01 null-points. |
| Sheer-legs haul (channel, gust pause) | Gameplay Designer | Segmented channel; gust timer pauses. |
| Escort that mirrors the player's stance | Gameplay Designer | NPCs follow; shelter when the player is in a lee volume. |
| Per-player path repaired state | Systems Engineer | Flag-conditioned path stones and traversal; fallback above. |

### 5.14 Cast notes and dialogue

**Inga Fellstrand [NEW].** Hearthguard terrace family, Stonewake. *Knows:* the story; what she wants to say. *Voice:* decisive, funny when nervous.

**Joar Stannick [NEW].** Nettlehook rope family. *Knows:* knots and heights; that the path is going. *Voice:* quiet, practical, notices things.

**Ottar Lund, path-warden [NEW].** Ridge Warden posted to the Cairn Fields paths. *Knows:* which stones went and when. *Does not know:* why the step stays. *Voice:* short; would rather tie a rope than be right.

**Kaldren Deepdelver [CANON anchor].** *Knows:* stresses: where the load goes. *Does not know / will not say:* whose work it is, or why the step is quiet. *Voice:* blunt, dryly amused, cautious.

```
TOS-D1 (path foot; S00)
TOS-D1.01 OTTAR: (knotting rope to a stake) "Path's shut. Goat went over last week. Next it's a person."
TOS-D1.02 INGA: "The step's never moved. Not once. Ask anyone."
TOS-D1.03 OTTAR: "The step's fine. It's everything either side of the step."
TOS-D1.04 JOAR: "We're swearing in the next storm. On the step. The wind remembers."
TOS-D1.05 INGA: "Torvek says that. Torvek's never wrong out loud."
  > "Let me look at it first."                      → TOS-D1.06
  > "Why in a storm?"                               → TOS-D1.07
TOS-D1.06 OTTAR: (stops knotting) "Look, then. Carefully. I'd like to not write anybody's name this winter."   → end
TOS-D1.07 JOAR: "Anyone can say it on a calm day." (beat) "Also it's what people do."   → TOS-D1.06
       {event: S00 complete}
```

**Inspects**

| Object | Text | Condition |
|---|---|---|
| Path gaps | "Two stones gone from the path either side of the step. Fresh breaks. The step's edges are clean." | — |
| The step | "One dressed block, wider than the path. Its joints run back into the rock. A shallow hollow in the middle, where people have stood still." | before S07 |
| Echo (from the step) | "One beat from under the step. Something close, right under your feet." | S02 |
| Echo (from a path stone) | "Four beats. The far wall of the cleft." | S02 |
| The arch | "Overhead, a curve of dressed stones meets in the middle. The middle stone's underside is the step." | — |
| Empty sockets | "Two sockets in the near haunch, clean-sided. Their stones lie in the shale below." | — |
| Fallen blocks | "Dressed blocks, the same as the arch. Fallen, not broken." | — |
| Nearby cairn | "Old base stones with the same tool marks as the arch. Somebody borrowed good stone here, long ago." | optional |
| Warden marks | "Cut into each haunch stone: *Don't lift.*" | `TOS_WARDEN` |

```
TOS-D3 (Kaldren at the path foot; optional; S04b)
TOS-D3.01 KALDREN: "You've been under it. Good. People mostly stand on things."
  > "What is it?"                                   → TOS-D3.02
  > "Why doesn't the step fall?"                    → TOS-D3.03
TOS-D3.02 KALDREN: "Old work. Don't ask me whose, or when. I do stresses."   → TOS-D3.03
TOS-D3.03 KALDREN: "Load goes through the middle stone into both sides. One side's been robbed."
TOS-D3.04 KALDREN: "Put back what fell, tight, or the path goes and the step stays, standing in the air like a fool."
  > "Why is it quiet in a wind?"                    → TOS-D3.05
TOS-D3.05 KALDREN: "That's not a stress question." (beat) "Ask the wind. It won't tell you either."   {set TOS_KALDREN_ASKED} → end
```

```
TOS-D4 (Ottar; crew alternative for S05)
TOS-D4.01 OTTAR: "Haul? My lot can haul. Storm'll be in by the time it's done."
TOS-D4.02 [TOS_KALDREN_ASKED] OTTAR: "The dwarf says tight. We'll do tight."   {set TOS_CREW_HAULED; enable wait_storm} → end
```

**Barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TOS-B5.01 | First stone seated | OTTAR (from the path) | "That's one. I felt that through my boots." |
| TOS-B5.02 | `TOS_KALDREN_ASKED`, tightening | (Kaldren, distant) | "Tighter." |
| TOS-B6.01 | Storm starts | INGA | "That's ours. That's our weather." |
| TOS-B6.02 | First gust on the path | JOAR | "Down. Down, Inga." |
| TOS-B8.01 | `TOS_TOLD`, later | OTTAR | "Carrying stone. Swore on it anyway." |
| TOS-B8.02 | `TOS_KEPT`, later | OTTAR | "Rope's coiled at the foot. Just in case. Not because of anything." |

```
TOS-D5 (on the step, in the storm; S07)
TOS-D5.01 INGA: (her voice suddenly ordinary in the quiet) "Oh." (a laugh) "Oh, I can hear you."
TOS-D5.02 JOAR: "Say it, then. While it's quiet."
TOS-D5.03 INGA: "I'll keep your house warm and your rope dry and I won't lie to you about weather."
TOS-D5.04 JOAR: "I'll keep yours. And I'll come back from every crossing, or I'll send word why not."
TOS-D5.05 INGA: (stepping off, and the roar comes back; she shouts over it) "DID THE WIND HEAR?"
TOS-D5.06 JOAR: (shouting) "I HEARD."   {event: S07 complete}
```

```
TOS-D6 (path foot, after; S08)
TOS-D6.01 JOAR: "You went under it. What's under it?"
TOS-D6.02 INGA: "Don't. Unless it's good."
  > "It's the middle stone of an old arch. It carries the path. That's why it doesn't fall."   → TOS-D6.10
  > "It tests the honest. You passed."                                                        → TOS-D6.20
  > "Leave them the story. Ottar, mark the haunches."                                         → TOS-D6.30
TOS-D6.10 INGA: (thinks) "Doesn't matter. We heard each other."
TOS-D6.11 OTTAR: "Carrying stone. I'll call it that."     {set TOS_TOLD} → TOS-D6.40
TOS-D6.20 JOAR: (looks at the player a moment too long) "Passed." (beat) "Good."
TOS-D6.21 OTTAR: "I'll keep the rope coiled at the foot."  {set TOS_KEPT} → TOS-D6.40
TOS-D6.30 OTTAR: "Mark them. Don't lift." (already reaching for his chisel)
TOS-D6.31 JOAR: "There's something under it." (beat) "Fine. Keep it."   {set TOS_WARDEN} → TOS-D6.40
TOS-D6.40 [TOS_CREW_HAULED] OTTAR: "Path's open. My lot did the lifting; you did the listening."
TOS-D6.40 [else] OTTAR: "Path's open. Pay's not much. Rope's yours if you want it."
       {event: D6 end → quest Completed}
```

### 5.15 Mystery ledger

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Why the step never crumbles** | It is the keystone of an Echohewn arch spanning the cleft; it carries the path's load into both haunches. | It tests the honest. | Echo count; the arch; Kaldren's stresses. | The step holds by itself; the oath holds it. | Whose work. | TOS (resolved locally). |
| **Why the step is quiet in a storm** | A null-point in the arch's crown (Echohewn work). **Never stated.** | The wind listens there. | Only the behaviour. | The wind judges oaths. | Everything. | None (bible §7.4 null-points). |
| **Who robbed the haunch** | Old cairn-builders borrowed dressed stone generations ago; this autumn's frost took the weakened ones. | — | The nearby cairn's tool marks. | Vandals; the splinter. | Who. | None (colour). |

### 5.16 Open decisions and review log

**Open:** (1) Whether the quiet step should be listed with TDS01 as a second null-point discovery (recommend: no separate entry; it lives in TOS). (2) Names Fellstrand, Stannick and Lund are [NEW].

**Review log:** First draft used tap-and-count on each haunch stone to find loose ones; cut, as it repeats TF-M3's rope-rig echo count. Echo count is used once, to find the void; loose stones are found by gust rattle. First draft let Kaldren explain why the step is quiet; cut to "not a stress question" (anchor limit). First draft had the player quarry new blocks; replaced with hauling the original fallen stones (no skill gate, a crew alternative, and the fallen stones are the clue). The oath is never judged by the step; the quiet is presented, never named.

---

## 6. File-level integration summary

| Need | Used by | Notes / fallback |
|---|---|---|
| Storm / drift / dusk / vigil waits (per-player presentation hour) | TSL, TSN, TWN (crew), TOS | One shared contract with Lowmark keep-watch and TF-M1's Close clock (bible §9.5). |
| Wind-window convention (whistle tell 1.5 s, gust 3 s, safe lees) | All five | One hazard convention; per-quest effects listed in each package. |
| Carry states | TWC colour (sail), TSL roll (lowered, not carried) | Lowmark carry state; TWC adds a gust impulse and a dip action. |
| Segmented channels with kept progress | TSL lashings, TWN wedges and letters, TSN dig, TOS haul | One channel component; gust pause or segment reset per package. |
| Per-player props with shared fallback | All five | Each package names its fallback. |
| Turning cord prop | TWC | One authored rotation; fallback static. |
| Null-point volume (audio duck, vertical snow) | TOS | Same contract as TF-M4 and TDS01. |
| Lighting preset swap | TSN snowlight | Per-player preset; decal visibility by preset and lamp position. |
| Read a quest item in place by region flag | TWN | `TES_horn_roster` at one of three locations. |
| Agility triggers with walkable fallbacks | TSL (chimney / line), TOS (down-climb / walk round) | All have click-to-move routes. |

## 7. Flags other packages read, and requests

| Flag / request | Owner | Reader |
|---|---|---|
| `TH_BANNER` (blood-oath / hearthguard / shared) | TWC | TF-M5 placement and posture (bible §9.3). |
| `TWC_COMPLETE` | TWC | TWN tally-stick inspect variant (this file). |
| `TWN_COMPLETE` | TWN | Act III `TSW-D9.51` (already authored). Earlier "a Brede on the rubbing" request withdrawn (§3.13). |
| `TWN_MIRE_HOOK` | TWN | **Request** to the Mire bible owner (R14). No Thornfell reader. |
| ~~Roster line request~~ | — | Withdrawn in independent review: TWN reads Act II's roster unchanged (§3.13). |
| *(read)* `TH_BRYNJAR`, `TH_SHATTERFALL_ACCOUNT`, `TH_SEASON`, `TH_CALLS`, `TSW_closure_rubbing` | Main acts | TWC, TWN, TSL/TSN, TOS, TWN variant. |
| `TSL_*`, `TSN_*`, `TOS_*`, `TWN_CUT_*` | Each package | Local props and barks only. |

## 8. Internal review log (file level)

| Check | Result |
|---|---|
| Bible §7.1–7.2 | Codes, unlocks, places, core verbs and pitches match. TSL track/climb/recover; TWC investigate/rite; TWN gather/testify/carve; TSN read/ask/choose; TOS climb/test/listen. No two share a core mechanic: thread-tracking and a climb (TSL), stitch-reading and a carried colour (TWC), testimony, slab-striking and letter-cutting (TWN), light-reading and a dig-out (TSN), echo count to a void, rattle-listening and a null-point (TOS). |
| Strange moments | Stormlight (TSL); a turning cord (TWC); snow in new-cut letters (TWN); snowlight (TSN); a quiet step (TOS). None identifies a person, proves anything or is called magic. |
| Evidence rule | Each resolution rests on records, objects, places or testimony: threads and banner; stitching, bunk-board and mending roll; slip, Maera's list, rim, roster's rotted margin and Hessa; daybook, copy and post; echo, arch and fallen stones. |
| Anchors | Kaldren: stresses only, no origins. Maera decides every cut. Brynjar not in the war or the splinter; lines vary by `TH_BRYNJAR`. Torvek makes no wartime claim. Hadrik places people and never explains. Iven reports before interpreting. Runa does not learn her own name's place on the gatehouse. |
| Withheld | Who blew the Split and how many died (TD-9); the banner company's fate and names; the Ridgewalker; null-point cause; M.V.'s full name; which Brede. |
| Boundaries | No Remnant; no Lowmark grain route; no Mire fact; no `[SPLINTER]` names; no failure states; no new quest items; only `TH_BANNER` set among region flags. |
| Scope | Markdown only; integration needs documented, not implemented. |
| **Independent review (2026-11-03)** | 7 findings (2 high, 3 medium, 2 low). High: TWN depended on a new Act II roster line ("Brede, up past the Seat") that contradicts Act II (no name survives on the roster) and on a Brede on the TF-M5 rubbing that Act III does not have; reworked to read Act II unchanged (Maera's list "Sig Brede. Held.", S. BREDE under the rime on the second rim cairn, the roster's rotted margin), roster custody aligned to Act II, both requests withdrawn, `TES_NAMESLIP_SEEN` variant added. High: TWC's carrying-voice moment duplicated TMM and TF-M5; replaced with the turning cord. Medium: TWN's ringing row duplicated TWG's tower-to-tower call; replaced with snow held in the new-cut letters. Medium: TWC gave Runa name-address without a tally (bible §5.3 rule 4); fixed. Medium: TSL hawk-drive leaned on Ranged while S01 is open; Melee/brace path made primary. Low: Kaldren dated the step ("older than the cairns"); cut. Low: Ranged mentions gated on S01 file-wide. |
