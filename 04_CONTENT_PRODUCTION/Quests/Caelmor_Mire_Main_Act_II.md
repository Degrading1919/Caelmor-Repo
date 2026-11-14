# Mire Main Questline, Act II: Rowan's Crossing, The Chapel of the Sinking Star

**Status:** Authored production content for Creative Director milestone review. This package implements Mire milestones MR-M3 and MR-M4 (bible §6, §6.1), which carry Act II from the end of *The Banners That Refuse to Fall* to the Act II turn. It follows the act-package format used for Thornfell (`Caelmor_Thornfell_Main_Act_II.md`), which itself follows the Lowmark act-package format. Everything marked **[NEW]** is authored here and is not canon until the Director promotes it. Everything marked **[PROPOSAL — DIRECTOR]** rests on an open bible §3 (MD-) decision. **[CANON]** items come from Phase 1 or the reconciled `LORE/` files. No schema, production JSON or C# is created here. The Mire is an internal production milestone of the complete game (CDR-3). Combat follows the Director rulings of 2026-11-03 (`Caelmor_Director_Rulings_Combat_Ranged_Release.md`): every enemy is defeated at 0 HP (CDR-1); every fight accepts melee or ranged and none requires ranged (CDR-2); standard systems are preferred over bespoke simulation (CDR-4).

**Controlling document:** `04_CONTENT_PRODUCTION/Quests/Caelmor_Mire_Narrative_Production_Bible.md`. Its §6 table, §6.1 briefs, §5.3 voice rules, §9 flags, §10 encounter families and §11 conventions are binding and are implemented as written. Where detail had to be invented it is marked [NEW] and stays inside those briefs.

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Mire_Main_Act_II_Dialogue.md`. It holds cast notes, every dialogue node referenced here (`MRC-`, `MCS-` prefixes), barks, inspect texts, Sennic's three stories, and the full text of the vestry regimental log and `MCS_warden_leaves`.

**Director decisions this package builds on (tagged where they apply):**
- `[MD-3]` **First-light crossing.** Rowan never crosses at night. The crossing runs at first light in fog ("the grey"), which Rowan does not count as night. The player is out at night in this act only on foot (the moss at Stillgrave's edge) and inside the chapel (the vigil on the roof). Every node that depends on the crossing hour is tagged.
- `[MD-4]` **Staged drainage, no breath meter.** The chapel is entered dry from the roof and the nave is dropped in three stages by opening sluice boards in order at Slack. There is no swimming, no air bar and no new movement mode; deep water is non-walkable. Lantern lines hold ground against Chapel Shades (a hazard with no HP). Every node that depends on drainage is tagged.
- **MD-6** (the Warden record's form) and **MD-9** (relative map placement) are applied as the bible recommends.
- **MD-7** (Hollowfoot) does not apply: no Hollowfoot appear in Act II. Each quest carries an "MD-7 swap" line saying so.

**Parallel dependency:** Act I (`Caelmor_Mire_Main_Act_I.md`, MR-M1 and MR-M2) is being authored in parallel. This package reads only what the bible defines for Act I: `MR_CHANNELS`, `MR_NAME_RECORD`, `MR_BANNERS`, `MR_CAUSEWAY`, the quest item `MBR_unit_logs` (three regimental day-books that stop on one day), the Memorywarden shard in Calwen's unsorted chest ("a clay fragment with faint marks"), and Ysolde Haverel's reading of the day-books as Memorykeeper records. If the Act I author names any of these differently, only the read-conditions in §A9.2 and §B9.2 and the matching dialogue conditions change. **Coordinated with the Act I designer (2026-11-08):** the day-books carry **no calendar date**. Ysolde matches them by a shared **weather run** written in each: *rain, rain, rain, a hard frost, a thaw, fog, fog*, and then all three stop. The vestry log in MR-M4 records the same run and stops on the second fog (§B8.4). No calendar date or year appears anywhere in Act II.

---

## Act II header

### What Act II does

Act I showed the player a community feeding itself across its own battlefield, and three regimental day-books from different columns that all stop on the same day. Act II answers the question those books raise: *what stopped three columns on one day?* The player earns the answer slowly, by preparing, waiting and reading water, and then takes it out of a drowned building with their hands.

| Quest | The player learns | By doing |
|---|---|---|
| MR-M3 **Rowan's Crossing** | The Sunken Church is where "the mages who listened" went out from. Only one living person can take you there, and he will only go when the water and the light say so. | Mending a boat, a harness and a lantern; sitting with an old man three times; reading stakes and knots; waiting for the turn; a first-light crossing in fog through a cut where the mud stands up. |
| MR-M4 **The Chapel of the Sinking Star** | The last Memorywardens went out from the chapel at the turning of the light and laid a calm over the battlefield so the armies could not keep fighting. It worked. Most of them did not come back. Their circle on Bannerline was never closed. | Relighting a lantern line, reading the building's own water stains to open three sluice boards in order, dropping the nave stage by stage while the dark presses at the edge of the light, reading a soldier's log in place and carrying a box of clay leaves out by lantern. |

**Act II turn (Arcs §3.2; bible §1 part 2):** the place everyone calls haunted is a place where people chose to break. The last thing the player does in Act II is sit a night on a chapel roof with a Tender who keeps a lantern lit, and then hand a record to the people who will keep it. The last thing they hear is Ysolde, at the landing, putting two things side by side and saying plainly that the link between them is her reading, not a hold.

### Dependencies on Act I

| Act I state (bible §9.1, §6.1) | Read by | Effect |
|---|---|---|
| MR-M2 Completed | MR-M3 availability | MR-M3 is offered only after MR-M2 completes (bible §6 prerequisites). |
| `MR_CHANNELS` | Both quests | Always true by Act II (MR-M1 sets it). The player already reads channel stakes (pale / ochre / black). Act II adds Rowan's knots and the chapel's buttress stake. |
| `MBR_unit_logs` held, or Ysolde holding them | `MRC-D1` variants; vestry log inspect (`MCS-I6.02`) | Ysolde reads the day-books at her table at the offer, from the player's pack or from her own shelf. In the vestry, the inspect adds the weather-run match either way (MR-M2 Completed guarantees the player has read them). The quest is complete without the item in the pack. |
| The shard in Calwen's unsorted chest (MR-M2 completion) | `MCS-I7.06` (optional line) | One optional line on the leaves: the pressed office mark is *like* the faint marks on the clay shard from the causeway. Likeness only; it proves nothing. |
| `MR_NAME_RECORD` = amended / qualified | `MRC-D1` one variant; post-quest barks | Ysolde's opening and one Sorrowmere bark. Flavour. |
| `MR_BANNERS` = retired / restored | Post-quest barks; `MCS-D11` one variant | Griefwatch's banner (restored) is mentioned once by Ysolde at the landing. Flavour; it does not change the record. |
| `MR_CAUSEWAY` = reset | One ferry-household bark `[CAUSEWAY]` | The causeway is open and quiet; the ferry way is still Sour. Flavour. |

### Region flags (bible §9.1 only)

| Flag | Act II role |
|---|---|
| `MR_CHANNELS`, `MR_NAME_RECORD`, `MR_BANNERS`, `MR_CAUSEWAY` | **Read.** Act II never writes them. |
| `MR_LANTERN_LINE` (side quest *The Broken Lantern Light*) | **Read** if set: one moss crew-alternative variant in MR-M3 and one Mabyn line in MR-M4 (bible §9.1 lists MR-M4 as a reader). |
| `MR_ROWAN_TRUST` = told / kept | **Set** by MR-M3. Read by MR-M5 (Rowan at the circle if told) and post-story Rowan lines. |
| `MR_WARDEN_RECORD` = sorrowmere / altar / tenders | **Set** by MR-M4. Read by MR-M5 (roll source line) and CV-M1 (custody line). |

Act II invents no other `MR_` flag. Quest-local flags use `MRC_` and `MCS_`. Those read by later packages are marked in each quest's flags table. (Validators should match the trailing underscore: `MR_` and `MRC_` are distinct strings that read alike; bible §13.)

### Quest-item budget (bible §9.4: Mire total 4)

| Item | Quest | Fate |
|---|---|---|
| `MCS_warden_leaves` (the Memorywarden record: four clay leaves wrapped in Mabyn's oilcloth) | MR-M4 | Acquired in the crypt (`S05`). Leaves the pack at the MR-M4 choice or at the landing: to Ysolde (**sorrowmere**), back into the lead box under the altar (**altar**), or into the Tenders' chest in Mabyn's roof loft (**tenders**). Readable afterwards at its location (inspect). Not droppable, not sellable while held. |

**Act II total: 1.** Running Mire total with Act I (`MNS_name_tape`, `MBR_unit_logs`) is 3 of 4; `MBL_names_roll` (Act III) is the fourth. Everything else in Act II is a carry-state object (reed bundles, a split root-knee, the tow harness, the moss bundle, Mabyn's hand lantern, the reed-paper rubbing), a record read in place (the vestry log, the buttress stake), oral testimony (Sennic, Rowan) or knowledge carried in flags.

### Season, weather and level identity

- **Season:** the long wet is close. Rain is presentation only; it never changes a rule.
- **Hours:** both quests use the per-player **presentation hour** (morning, noon, dusk, night) and the Lowmark **keep watch** convention to wait for a turn (bible §9.2, §9.4). There is no world clock. Act II asks the player to wait more than any other Mire milestone, and every wait is one interaction.
- **Fog:** MR-M3's crossing runs in a quest-pinned **grey** (fog at first light), per player, never world weather `[MD-3]`. The fog lifts at the chapel.
- **Level identity (MD-10):** both quests are tuned as **Advanced** content in production terms. Exact levels are Gameplay Designer calls. The skill hooks in MR-M3 carry light requirements as `[GD]` placeholders and each has a crew alternative that costs time, never access.

### Structure check against the bible §6 core verbs

| Quest | Primary verb | Distinct from |
|---|---|---|
| MR-M1 MNS | search and match records; walk a shifting route | (Act I) |
| MR-M2 MBR | recover and retire under attack; read banner states | (Act I) |
| MR-M3 **MRC** | **prepare, learn, wait**; then a guided crossing | The only quest in the Mire where the player's main work is mending and waiting. The only boat set piece. The readable system is taught as a pair: stake (what the water is doing) and knot (what Rowan knows it will do). |
| MR-M4 **MCS** | **drain and light**: a sluice puzzle at Slack, lantern lines, a crypt delve | Indoors and vertical. The building is read (water stains, a stake through a window), not the field. The danger is the dark, not an enemy; the hazard has no HP. |
| MR-M5 MBL | read the count and hold the gap | (Act III) |

No two quests share a set piece or a reading mechanic. MRC reads water from a boat; MCS reads a building from inside it. Combat changes family across the act: Reedlurkers and Earthen Echoes (MRC) → Reedlurkers and Silt Crawlers, with Chapel Shades as a hazard (MCS).

### Unlocks across Act II (bible §7)

After MR-M3: the **Chapel route** (Rowan ferries the player to the Chapel at Slack from now on); *The Book of Arrivals* (MBA, if *The Stranger's Seat* is also complete); *The Father at the Ford* (MFW); *The Returning Wage* (MRW). After MR-M4: *The Lantern That Would Not Go Out* (MLW, if *The Broken Lantern Light* is also complete); the chapel interior as a lit, revisitable place; MR-M5 *Bannerline* (automatic on next entry to Sorrowmere or Griefwatch).

---
---

# Part A: MR-M3 Rowan's Crossing (`MRC`)

## A1. The quest in one paragraph

Ysolde Haverel has the three day-books from the causeway chest open on the register table. Three columns, three hands, one day, and then nothing. She wants to know what stopped them, and she has already asked the oldest person she knows: Old Sennic Vale says the Sunken Church "listened", and that the mages "went out from there". That is Sennic's story, and Ysolde says so. Only one living person knows the way to the Sunken Church: **Rowan Mirewake**, the ferryman at Blackwater Landing. Rowan says no. He says it twice. Then, because the player is still standing there, he says the boat leaks. The quest becomes *Help at the landing.* The player re-caulks Rowan's boat with reed and resin and fits a new thwart split from a driftwood root-knee, mends his tow harness, walks out to Stillgrave's edge at night to gather lantern moss for the bow lantern, and sits with Sennic three times on three different days to hear about bells that rang without sound, mages who listened more than they spoke, and a church that went down "slow as a held breath". When the boat is whole and the player has a light, Rowan teaches his knots in daylight: one knot, the channel turns at dusk; two, at first light; a knot cut through, never this season. Twice the boat runs into mud on a wrong call, and Rowan says mud is honest. A player who asks him gently, on three separate visits, why he will not cross at night, hears the answer: the woman who taught him the route went out one night for a sick child and did not come back, and he found her boat in the morning with her knots still tied. At the end of a night the player keeps watch at the landing. In the grey, Rowan says "Now." They cross in fog, reading stakes and knots aloud. The boat is hauled over a shoal by the harness the player mended. In the cut past the Drowned Encampment, mud stands up on the banks and wades toward the boat. Past Stillgrave, a bell rings across the water with no sound in it: the reeds lie down in rings and the fog shivers, and there is nothing to hear. Rowan does not look round. Out of the fog comes the roof of the Sunken Chapel, its lantern line half dark, and a woman on the roof with a pole lantern, who says the line has been failing since spring.

**What the player should remember:** the boat they mended carrying them, the reeds lying down in silence, and Rowan's knots. **What the player should want next:** to go inside.

## A2. Selection record

| Candidate | Verdict |
|---|---|
| **A. A night crossing by lantern, as Arcs §3.2 first wrote it.** | Rejected `[MD-3]`. Rowan's canon anchor refuses night crossings, and the anchor is locked. The night stays in the quest on foot (the moss walk) and in MR-M4 (the roof vigil). |
| **B. Rowan agrees after one favour.** | Rejected. Canon asks for gradual trust, preparation and restraint. One favour is a transaction. |
| **C. The player persuades Rowan in dialogue.** | Rejected. Rowan explains why "unless pressed gently, and repeatedly". The asking is optional and gentle; the passage is earned by work and waiting, not by talk. |
| **D. Offer from Ysolde → two refusals → four preparations (boat, harness, moss, Sennic) → knots by day → optional asking over three visits → the grey crossing (stakes and knots called aloud, the shoal, the Encampment cut, the soundless bell) → the roof** (selected; the bible brief). | **Selected.** The quest is quiet on purpose (bible §6: 35–45 minutes, "deliberately quieter"). The player is competent before the crossing begins, so the crossing is a test the player passes rather than a lesson. |

## A3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Rowan: ferryman of the Blackwater Channels; refuses night crossings; avoids certain channels; explains why only if pressed gently and repeatedly; reserved, dry-witted, deeply cautious | Mire anchors §III | [CANON] |
| Rowan is the only known living guide to the one chapel; learned the routes from someone who never returned; knows when the land will accept passage; treats the church as a place of mourning, not power; passage only once the player shows restraint | Mire anchors §III; Part 4 ledger (Rowan row) | [CANON] |
| One site, three names: Chapel of the Sinking Star (formal), Sunken Chapel (common), Sunken Church (riverfolk and ferrymen); origin of the formal name unknown | Dossier §VI.6; C14 | [CANON] |
| Sennic: elder at a driftwood rise; childhood stories of the Sunken Church; bells that rang without sound; mages who listened more than they spoke; the church sinking slowly; gives *where*, not *why*; fragmented speech, lucid about the past | Mire anchors §IV; Part 4 ledger (Sennic row) | [CANON] |
| Drowned Encampment: wagons and tents sunk into peat; rusted weapons through the surface; repeating sounds of distant shouting or weeping | Dossier §VI.2 | [CANON] |
| Stillgrave Hollow: stagnant water; unnervingly clear reflection; lantern light bends near the surface | Dossier §VI.4 | [CANON] |
| Lantern moss glows faintly when damp; lights walkways at night | Dossier §X | [CANON] |
| Earthen Echoes: mud silhouettes; jerky repeated motion; collapse when struck; near sites of grief | Dossier §IX; bible §2.4, §2.6 | [CANON]; re-form by condition per bible |
| Reedlurkers: amphibious ambushers in shallows | Dossier §IX; bible §10 | [CANON] |
| Channel stakes (pale / ochre / black); Rowan's knots; Blackwater Landing; Sennic's Driftwood Rise as a POI name; Rowan's teacher's story; the Chapel route | Bible §1.1, §4.2, §6.1 | [NEW] |
| Mabyn Coyle, Chapel-Tender | Bible §5.2 | [NEW] |
| First-light crossing in fog | Bible MD-3 | [PROPOSAL — DIRECTOR] |

## A4. Quest summary card

| Field | Value |
|---|---|
| Working title | **Rowan's Crossing** |
| Suggested content id | `mire.main.03_rowans_crossing` |
| Arc position | Act II opener; Arcs §3.2 "Earn the Chapel through restraint and preparation" |
| Prerequisite | MR-M2 Completed |
| Offer | Ysolde Haverel at the Sorrowmere register table on the player's next entry to Sorrowmere after MR-M2 completes (`MRC-D1`); journal lead "Three columns, one day" on MR-M2 completion |
| Target length | 35–45 minutes (deliberately quieter; bible §6) |
| Combat share | ~15% (Reedlurkers at Stillgrave's edge; Earthen Echoes in the Encampment cut) |
| Dialogue share | ~25% (Sennic's sittings, Rowan's lessons and asks) |
| Mending, gathering, reading, waiting, crossing | ~60% |
| Skills | Woodcutting ~[GD: low] (the thwart); Leatherworking ~[GD: low] (the harness repair). Each has a crew alternative that costs a day, never access. Melee or ranged in both fights (ranged natural from the boat; never required). |
| Choices | Ask Rowan gently, on three separate visits, why he will not cross at night, or let him keep it (`MR_ROWAN_TRUST` = told / kept). Neither is wrong; the crossing happens either way. |
| Unlocks | The Chapel route; MR-M4 (continuous); *The Book of Arrivals* (with MSS), *The Father at the Ford*, *The Returning Wage* |
| **Anchor** | Ferry households of Blackwater Landing; Rowan Mirewake; Old Sennic Vale (oral memory) |
| **World-truth row** | H12 (seed: the Mire as the war's central battlefield; Memorywardens conscripted as guides and healers; their practice broke) |
| **Revelation role** | **Plants R08:** Sennic's listening mages who "went out from" the Sunken Church; the church sinking slowly; the soundless bell; the altar "under the big window" (a lead MR-M4 pays). Nothing in MRC is a custodian of R08. |
| **Recurring evidence** | Sennic's stories (oral; leads only, never holds). The `MBR_unit_logs` recur as Ysolde's question at the offer and as the weather run (rain, rain, rain, hard frost, thaw, fog, fog) the vestry log matches in MR-M4 (independent custodian: the chapel vestry). |
| **State compliance** | Inactive / Active / Completed only. No step can fail: a wrong channel call grounds the boat softly or puts it in a side channel to wait; waiting is always available; Rowan's refusals are a step, not a gate the player can lose. Choice recorded in `MR_ROWAN_TRUST`. |
| **Combat compliance** | Reedlurkers (MRC-E1) and Earthen Echoes (MRC-E2) are defeated at 0 HP. Echoes collapse into mud and re-form on the cut's banks while the grey lasts (place condition, bible §2.6). Every fight accepts melee or ranged; ranged is natural from the boat and never required. No SX. |

## A5. The places

All placement is relative. **MAP VERIFICATION REQUIRED** for every placement in this section. The narrative needs only that: Blackwater Landing sits below Sorrowmere at the edge of the Blackwater Channels; Sennic's Driftwood Rise is a short walk from the landing along the peat edge; Stillgrave's near edge can be reached on foot from the landing by a peat path; and the Chapel is reached only by Rowan's route through the Blackwater, past the Drowned Encampment and Stillgrave Hollow, in that order (bible §4.2 route order). No compass direction toward any region is given, and no route leaves the Mire (MD-9).

### A5.1 The Sorrowmere register room [MP01] (offer only)

| Area | Storytelling |
|---|---|
| **R1. The register table** | Ysolde's long table with the Names Below register at one end and the three day-books from the causeway chest open at the other, each held flat with a river stone. The stranger's seat on the visitor's side. Ysolde has laid a reed strip in each book at its last page. |
| **R2. The story shelf** | Reed-bound books of oral testimony, each spine marked with whose story it is. One is Sennic's, written down years ago in a younger Memorykeeper's hand. Optional inspect (an alternative reading of Sennic's stories; see Beat 2). |

### A5.2 Blackwater Landing [MP06]

| Area | Storytelling |
|---|---|
| **L1. The reed docks** | Plank docks on stilts over black water. Ferry households' punts tied in a row; Rowan's mooring at the end is empty because his boat is on trestles in the shed. |
| **L2. The boat shed and bench** | Rowan's boat on trestles, upside down: a long, shallow, flat-bottomed pole boat, black with old resin, three seams weeping, a cracked thwart. His bench: resin pot, caulking irons, a tow harness hung on a peg with both traces rotted through. |
| **L3. Rowan's fire and the landing stake** | A peat fire in an iron tray. At the end of the dock, a Reedsward channel stake painted in three bands (pale, ochre, black) and, beside it, a clump of reed heads with knots tied in them. Before MRC-D5 the knots are only knots; after it, they inspect as Rowan's. |
| **L4. The reed beds** | Reed beds in the shallows beside the landing where the ferry households cut reed for caulking and thatch. Six cutting spots are highlighted when the hull task is active. Walkable at any state (they are at the bank). |
| **L5. The practice cuts** | Two short channels off the landing, each with a stake and a knot clump at its mouth. Used only in Beat 3. |
| **L6. The ferry households' row** | Three stilt houses behind the landing. Barks, food, and the crew alternatives (a boatwright, a harness-mender). Nobody here is named. |
| **L7. The peat path** | A path of laid peat and old planks along the channel edge from the landing toward Stillgrave's near edge. Walkable at any hour. Lantern-moss posts line it but most are dark this season (a dark post means its foot is dry, bible §1.1). |

### A5.3 Sennic's Driftwood Rise [MP18]

| Area | Storytelling |
|---|---|
| **D1. Sennic's fire** | A peat-edge shelter under a lean of driftwood, a fire, a pot of smoked eel, two stools. Sennic sits facing the water. |
| **D2. The driftwood piles** | Old timber washed up over the years: drowned roots, broken stakes, a wrecked punt. Three **root-knees** (natural bends of root wood) are marked for cutting when the thwart task is active. Reclaimed wood (MD-11). |
| **D3. The view** | From the top of the rise, the Blackwater runs out into a low fog bank that never quite lifts. Sennic: "It's out there. You can't see it from here. Nobody can." |

### A5.4 Stillgrave Hollow, near edge [MP11]

| Area | Storytelling |
|---|---|
| **S1. The stilt-stumps** | Old stilt-house stumps standing in the shallows at the basin's edge. Lantern moss grows thick on their north faces (no compass meaning; "the damp side"). At night five clusters glow and can be gathered. By day they are only moss and hard to tell from weed. |
| **S2. The shallows** | Knee-deep water between the stumps; Reedlurker ground (MRC-E1). |
| **S3. The surface** | The still water of the Hollow beyond the stumps. Too clear. A lantern held over it bends its light. Stillgrave's reflection (MDS02) is presented by the discoveries package; MRC triggers nothing extra here. |

### A5.5 Rowan's route through the Blackwater

Reached only in the boat with Rowan. The route is fixed (bible §11.1 ferry convention).

| Area | Storytelling |
|---|---|
| **C1. Junction one** | Two cuts between reed islands. Each has a stake and a knot clump. On the crossing morning: the left cut's stake is at ochre (Slack) with **two knots** (turns at first light); the right cut's stake is also at ochre but its reed is **cut through** (never this season). |
| **C2. The shoal** | A broad bar of grey silt that grounds any boat at Slack. A tow path of old posts runs along the bank beside it. The harness is used here. |
| **C3. The Drowned Encampment cut** [MP09] | A narrow cut between two banks of the Drowned Encampment: wagon wheels and tent poles standing out of the peat, rusted weapons through the surface, a field kitchen's iron stove on its side. Faint, repeating sounds of distant shouting (canon). The banks are where the Echoes stand up (MRC-E2). |
| **C4. Junction two** | One cut ahead with its stake at **pale** (Running) and **two knots**; one side channel with a **leaning** stake (Sour). |
| **C5. Stillgrave's open water** | The boat passes along the far side of Stillgrave Hollow, on open still water. The soundless bell (§A8.2). |
| **C6. The fog bank and the roof line** [MP13] | The fog thickens, then the chapel roof stands out of it: a long ridge of moss-green tiles and a squat bell-tower just above the water, a row of lantern posts along the ridge, half of them dark. A plank landing stage on the roof's lower slope. |

## A6. Player-facing sequence

### Beat 0: Three Columns, One Day (`S00_offer`)
**Objective:** *Talk to Ysolde at the register table.*
On the player's next entry to Sorrowmere after MR-M2, a Memorykeeper's runner finds them on the raised way (`MRC-B0.1`). At the register table **Ysolde Haverel** has the three day-books open (`MRC-D1`): from the player's pack if they still carry `MBR_unit_logs` ("May I?"), or from her own shelf. She reads the last line of each aloud: *ground will not take a step*; a word that stops in the middle; *men sat down*. "Three hands. Three columns. One day. Then nothing." She does not like nothing. She asked Sennic. Sennic says the Sunken Church "listened", and the mages "went out from there". "That's Sennic's story. I'm not saying it's so." The only person who knows the way to the Sunken Church is the ferryman at Blackwater Landing, Rowan Mirewake. "He'll say no. Go anyway." She writes in her reed book that the player was asked.
Optional: the story shelf (R2): Sennic's stories in another Memorykeeper's hand, short and flat.
**Verbs:** talk, listen.

### Beat 1: No (`S01_no`)
**Objective:** *Ask Rowan Mirewake for a crossing.* Then: *Help at the landing.*
At the landing, **Rowan** is at his bench with the harness across his knees (`MRC-D2`). The player asks to be taken to the Sunken Church. Rowan says no, dryly. The player asks again (any of the options that ask counts). He says no again, and gives the only reason he gives anyone: "The boat leaks." He does not explain the second no. He does not ask the player to leave either. If the player lingers (any further option), he points at the shed with his chin: "If you're staying, it leaks there." The objective changes to *Help at the landing*. The quest asks nothing faster of the player than that.
A ferry household offers food before anyone asks a question (`MRC-B1.2`; bible §5.3 rule 6). Optional.
**Verbs:** ask, be refused, stay.

### Beat 2: Help at the Landing (`S02_prepare`)
**Objective:** *Help at the landing.* Sub-objectives appear as the player learns of them (`MRC-D3`): *Mend the boat.* *Mend the tow harness.* *Find moss for the bow lantern.* *Sit with Sennic.* Any order. Each mending task has a **crew alternative** that costs a day (keep watch until the next morning; the work is done when the player wakes). Crew alternatives commissioned before a keep watch all complete on that one wait: a player who asks the boatwright, the harness-mender and the Tender and then keeps watch once to morning has all three done. Rowan does not comment on which the player chooses.

**1. Mend the boat** (hull).
- **Reed:** cut six bundles of reed at the reed beds (L4; gather interaction ~2 s each). Carry-state "reed bundles".
- **The thwart:** walk to Sennic's Driftwood Rise and split one of the three marked **root-knees** (D2). **Woodcutting ~[GD: low]**: channelled, 3 segments of ~4 s; completed segments persist. Carry-state "a split root-knee". (Rowan: "Driftwood's honest. It's already been drowned once.")
- **Resin:** warm the resin pot at Rowan's fire (interaction ~3 s).
- **Caulk:** work reed and resin into the three weeping seams (channelled, one segment of ~4 s per seam; segments persist). A seam caulked without warm resin will not take; the log says "Cold resin. It won't take." and the player warms it again. No penalty.
- **Fit the thwart** (interaction ~3 s). Rowan and the player turn the boat (a two-person lift; Rowan does the heavy end) and slide it into the water. It floats. Sets `MRC_HULL_DONE`.
- **Crew alternative:** ask the ferry households' boatwright (L6). She does the whole hull. Keep watch until morning. Sets `MRC_HULL_CREW` (barks only).

**2. Mend the tow harness.**
- At Rowan's bench: cut away the two rotten traces (interaction), take a length of **trade leather** from Rowan's store (he bought it; the Mire does not tan, source process), and **stitch new traces**. **Leatherworking ~[GD: low]**: channelled, 3 segments of ~4 s; segments persist. Stuff the chest pad with reed fluff (interaction ~2 s). Sets `MRC_HARNESS_DONE`.
- **Crew alternative:** the ferry households' harness-mender (L6) takes it overnight. Keep watch until morning. Sets `MRC_HARNESS_CREW`.
- The player does not know what the harness is for until the shoal (Beat 5). Rowan: "For the shallow bits. You'll see."

**3. Find moss for the bow lantern.**
- Rowan's bow lantern has no wick. Lantern moss "only shows itself in the dark. Stillgrave's edge has it. Go at night. On your feet. Not in my boat." `[MD-3]`
- The player keeps watch until night (or arrives at night), walks the peat path (L7) to Stillgrave's near edge (S1) and gathers **five glowing moss clusters** from the stilt-stumps (gather ~2 s each). Reedlurkers in the shallows (**MRC-E1**). Carry-state "a moss bundle" (enough for the bow lantern and for the chapel wicks in MR-M4; there is no shortage mechanic). Back at the landing (any hour), Rowan wicks the bow lantern. Sets `MRC_MOSS_DONE`.
- **Crew alternative:** a Chapel-Tender at Sorrowmere's memorial gardens brings a jar from the gardens' stock in the morning. Keep watch until morning. Sets `MRC_MOSS_CREW`. With `MR_LANTERN_LINE` set, the Stillgrave family from *The Broken Lantern Light* brings it instead (`MRC-B2.6`).
- Optional, at night at Stillgrave's edge: the lantern light bending over the surface (S3). Inspect only.

**4. Sit with Sennic.**
- Three sittings at Sennic's fire (D1), one story each (`MRC-D4.10`, `.20`, `.30`). Each sitting opens only when the **presentation hour has turned** since the last one, by any wait anywhere (the player can keep watch at his fire; Sennic dozes). The objective says so: *Sit with Sennic (he's clearer once the hour has turned; any wait counts).* In the fiction these are different days; Sennic is clearer at some hours than others and says so. He offers smoked eel before every story.
- The stories, in order: **bells that rang without sound** ("you'd see the reeds lie down"); **mages who listened more than they spoke** ("they'd sit with you; you'd go home lighter; they went out from the church, the last time, and that's all I know"); **the church going down "slow as a held breath"** ("a step a year; my mother marked it on the door; the door's under now; you go in by the top"). Each story gives one *where* and never a *why*: the bell side faces the slack water; the altar is "under the big window"; the way in is from the roof. Sets `MRC_SENNIC` (count to 3).
- **No crew alternative** is needed: this is dialogue, not a skill gate. Ysolde's written copy (R2) is an optional reading that adds nothing new and does not count toward the sittings (Ysolde: "It's in the book. It's better from him.").

`S02` completes when the hull, harness and moss are done (by the player or by a crew) and the third sitting has ended. Rowan: "Boat's whole. Harness is whole. You've a light. And you've let an old man talk." (`MRC-D3.40`).
**Verbs:** gather, cut, caulk, stitch, walk at night, fight, sit, listen, wait.

### Beat 3: The Knots (`S03_knots`)
**Objective:** *Learn Rowan's knots.*
In daylight only (morning or noon; at dusk or night Rowan says "Tomorrow." and the player can keep watch). At the landing stake (L3), Rowan ties knots in reed heads and teaches them (`MRC-D5`): **one knot**, this channel turns at dusk; **two knots**, it turns at first light; **a knot cut through**, never this season. Only he ties them, and they mark only his route. He also turns the stake rule the player already knows to his own use: "Pale's running. Ferries like it; they go with it. My cuts don't. It pours through them like a weir. Ochre's slack: the cuts go still, the shoals go dry. We pole the cuts and haul the shoals. Black, nobody." (This is how the bible's stake rule and its "Rowan ferries at Slack" fit together; see §A14.)
Then two **practice runs** in the boat, Rowan poling, through the practice cuts (L5). At each cut mouth the player reads stake and knot and calls the channel through a dialogue choice (`MRC-D5.20`, `.30`):
- **Run one:** both cut mouths at ochre; one has two knots, one has a knot cut through. Call the two-knot cut. A wrong call runs the boat softly onto mud a few lengths in (§A8.4). Rowan: "That's mud. Mud's honest." He poles off and they try again.
- **Run two:** it is daytime; one cut has one knot at ochre (it will turn at dusk, so "we're back before then"), one has a knot cut through but its stake reads ochre too. Call the one-knot cut. A wrong call grounds the boat again. Rowan: "The stake says yes. I said no. Who's been on this water longer?"
Sets `MRC_KNOTS_READ`. After this, Rowan's knots are inspectable as world markers anywhere on his route (§A8.3).
Rowan closes the lesson (`MRC-D5.40`): "The grey, then. Tomorrow's. Come at the end of the night and don't talk till I do."
**Verbs:** read, call, be wrong, be corrected, learn.

### Beat 4: Asking (`S04_ask`, optional)
**Objective (optional, shown once the first ask has happened):** *Ask Rowan why he won't cross at night.*
Available from the end of `S01` until the crossing starts (and afterward; see §A9.3). The player can ask Rowan gently why he will not cross at night. **Each ask needs a separate visit**: the presentation hour must have turned since the last ask (keep watch, or leave and come back). Pushing options exist ("Just tell me.") and get a flat "No." that does not count and costs nothing (`MRC-D6.05`).
- **First ask** (`MRC-D6.10`): "Can't see the knots." Dry. Nothing more.
- **Second ask** (`MRC-D6.20`): "Lanterns show you water. Not what it's doing." A pause. "Somebody I knew thought a lantern was enough."
- **Third ask** (`MRC-D6.30`): he tells it. The woman who taught him the route went out one night to fetch a sick child from the far channels, and did not come back. He found her boat in the morning, in a side channel, with her knots still tied. He does not say her name. He does not say what became of the child. "So. The grey. Not the dark." Sets `MRC_ASKED` = 3. [NEW detail inside his ledger row; no war relation is given.]
A player who never asks is not told why. Rowan notices, and says so once, at the roof (`MRC-D9.11`).
**Verbs:** ask, wait, ask again, listen.

### Beat 5: The Grey (`S05_crossing`) `[MD-3]`
**Objective:** *Wait at the landing for the grey.* Then: *Cross with Rowan.*
Requires `S02` and `S03` complete. The player keeps watch at Rowan's fire until morning (if they arrive in the morning, Rowan says "Late. It's still grey. Get in."). The **grey** is a quest-pinned per-player fog (§A8.1). Rowan is already in the boat with the bow lantern lit. He says one word: "Now." (`MRC-D7.01`). The crossing is an escorted ride on a fixed route (ferry convention). The player sits in the bow. Rowan stops at each junction and waits for the player's call.
1. **Junction one** (C1). Call the cut (`MRC-D8.10`). Right: the two-knot cut at ochre. Wrong (the cut-through reed): Rowan says why and poles into a side channel; they wait for the turn (~20 s presentation; the fog moves, a heron lifts). Then on.
2. **The shoal** (C2). The boat grounds. Rowan hands the player the harness: "Your turn to be a horse." The player wears the harness (carry-state; weapons sheathed) and **hauls** the boat along the bank path between tow posts: channelled, 3 segments of ~5 s, walking a few metres between each; segments persist. Rowan pushes from the stern. With `MRC_HARNESS_CREW`: one bark from Rowan ("Good stitching. Not yours. Still good."). Afloat again.
3. **The Encampment cut** (C3). **MRC-E2.** Rowan poles through in three stretches. On each stretch, mud stands up on the banks and wades toward the boat. While an Echo is at the gunwale, Rowan holds the boat (the ride halts on enemy proximity, the ordinary escort rule the Act I cart uses) until it is defeated. The player fights from the bow: ranged reaches them on the banks and in the water; melee reaches them at the gunwale; both finish the cut. The Echoes re-form on their banks while the grey lasts. Once the boat is out of the cut, they stand on the banks and do not follow. Rowan says nothing during the fight except "Bank." when one forms.
4. **Junction two** (C4). One cut ahead: stake at pale, two knots. One side channel: a leaning stake. Rowan stops. Call it (`MRC-D8.20`). The right call is **"Wait. Two knots. It turns now."** Calling "Go, it's running" or "Take the side channel" gets the reason from Rowan and the same wait. Either way they wait (~25 s); the water on the stake drops to ochre as the light comes up. Rowan, on a right call: "That's it. That's all it is." Sets `MRC_WRONG_CALLS` (count; barks only).
5. **Stillgrave** (C5). **The strange moment** (§A8.2). Open still water. A bell rings across the water with no sound in it. The reeds along the far edge lie down outward in rings, one ring after another, and the fog shivers. There is nothing to hear. Rowan does not look round. He keeps poling. Sets `MRC_BELL_SEEN` (barks only).
6. **The fog bank** (C6). The fog thickens, then the roof comes out of it.
**Verbs:** wait, read, call, haul, fight, witness.

### Beat 6: The Roof (`S06_roof`)
**Objective:** *Climb onto the chapel roof.*
Rowan brings the boat in to the plank landing stage on the roof's lower slope. The roof lantern line runs along the ridge, half its lanterns dark. **Mabyn Coyle**, a Chapel-Tender with a pole lantern and peat-wax on her sleeves, comes down the ridge to meet them (`MRC-D9`). She knows Rowan; she does not know the player; she offers the player a hand up and a cup before asking anything. The line has been failing since spring: "Since the spate. Damp gets in the housings. And I can't keep it alone." Rowan hands up the moss bundle. He will not come onto the roof: "Not my place. It's hers." He tells the player when he will come back: "Morning slack. Not before." `[MD-3]` With `MRC_ASKED` < 3 he adds the once-line about not being asked (`MRC-D9.11`); with `MRC_ASKED` = 3 he says only "You know why." He poles away into the fog.
Sets `MR_ROWAN_TRUST` = **told** (`MRC_ASKED` = 3) or **kept** (otherwise). The quest completes on `MRC-D9` end. MR-M4 becomes Active at once (Beat 0 of Part B is the same conversation continued).
**Verbs:** arrive, climb, meet.

## A7. Encounters

Tuned for **Advanced** identity (MD-10). Earth-memory enemies follow bible §2.6: **combat disperses, conditions decide.** Each Echo is defeated at 0 HP and collapses into mud; re-forming while the grey lasts is a place rule (rulings §3.1.2), not a retreat. Every fight accepts melee or ranged (CDR-2); ranged is natural from the boat and never required. No Echo has a nameplate, face, unit mark or colours; target frames show no name.

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MRC-E1** | 2 × Reedlurker (lurker), 1 × Reedlurker (snapper) | Stillgrave's near edge, the shallows between the stilt-stumps (S2), at night during the moss task | Lurkers wait submerged beside moss clusters and lunge at a player who gathers. The snapper hangs back in deeper water and spits. | **Lunge:** the reeds ripple outward from the lurker's spot (~1.2 s), then a lunge in a straight line (step aside). **Spit:** the snapper's head rises clear of the water and the reed-ripple stops (~1.0 s), then a lobbed spit that leaves a short slowing slick (standard slow). | A light night fight; reading ripples by moss-light; ranged answers the snapper, melee closes on it in knee-deep water | 60–90 s; 65–80% HP remaining |
| **MRC-E2** | Earthen Echoes (echo), 2 per bank per stretch, 3 stretches | The Drowned Encampment cut (C3) during `S05` | Each Echo stands up out of the bank and **wades** toward the boat along a straight line. It repeats a motion (a man bracing a pole, a woman hauling a rope). At the gunwale it lays two mud hands on the wood (presentation; the ride halts while any Echo is in reach of the boat) and **swings**. Struck: collapses into mud. Re-forms at its bank spot ~10 s later while the grey lasts and the boat is in its stretch. | **Forming:** the bank bulges and a column of mud rises (~1.5 s); Rowan: "Bank." **Wading:** slow (~6 s from bank to boat), readable at range. **At the gunwale:** two mud hands on the wood, the boat rocks (no damage; presentation only). **Swing:** the arm lifts, mud dripping (~1.2 s), then a slap (moderate damage; no knockback, so nobody is moved toward the gunwale). | Teach Echoes before MR-M5: slow, readable, collapse when struck, come back by place. Ranged clears waders early; melee clears those at the gunwale. Both finish the cut. | 2–3 min for the cut; ~55–70% HP remaining |

**MD-7 swap:** none needed. No Hollowfoot appear in MRC.

**Rules**
- **Combat never reveals evidence.** Nothing in MRC is evidence; Sennic's stories are leads and nobody treats the Echoes as people. A ferry-household bark calls them "the drowned getting up" (belief); Rowan's only answer is "Mud." (`MCS-B9.10` in the dialogue file, post-quest at the landing; `MRC-B5.4` in the boat).
- **The cut always ends.** Out-ranging Echoes never ends the fight on its own (they re-form); passing through the three stretches does. The boat holds while an Echo is at the gunwale and poles on (~12 s per stretch) whenever none is; an Echo re-forms ~10 s after defeat and wades ~6 s, so clearing the gunwale always buys the boat its stretch. The player must fight, by either style; nothing else is asked.
- **No falls, no drowning.** Knockback stays inside the boat; deep water is non-walkable (bible §11.1). At the shoal and on the tow path the player walks only on authored ground.
- **Death:** at Stillgrave's edge, respawn at Blackwater Landing (gathered moss kept). During the crossing, respawn aboard at the last passed junction (checkpoint); the grey stays pinned while `S05` is active; the Encampment cut restarts at its first stretch.
- **Co-op:** shared enemies; a defeat credits each partner whose own active step consumes it (Lowmark §8.1). The boat carries Rowan and the party (party size [GD]); if the party is larger than the boat, a ferry household's punt may follow (optional co-op presentation only; not needed for solo, CDR-6). Rowan acts on the first call he hears (shared presentation only); each partner's call counts only for that partner's own `MRC_WRONG_CALLS`, a partner who did not call records nothing, and every partner hears Rowan's reason (CDR-6). `MR_ROWAN_TRUST` is per player: each partner's asks count only for them.

## A8. The discovery and strange moments: presentation specs

### A8.1 The grey `[MD-3]`

| Element | Spec |
|---|---|
| What it is | A quest-pinned, per-player fog at the presentation hour **morning**, active from `MRC-D7.01` until the roof (`S06`). Never world weather. |
| Look | Visibility ~30 m at the landing, ~15 m in the cut, ~40 m on Stillgrave's open water, closing to ~10 m in the fog bank before the roof. The bow lantern's moss light is soft green-gold and does not cut the fog; it shows the water just ahead of the bow. |
| Sound | Pole in water; drips; a heron; the faint repeating shouting in the Encampment cut (canon distortion; never words). No music until the roof. |
| Rule | Rowan's line, once, when the player first notices: "Grey isn't night. Night's when you can't see your own knots." (`MRC-D7.05`) |
| If replaced | If the Director rules a true night crossing (MD-3 replaced), only nodes tagged `[MD-3]` change: the keep-watch target hour, the fog becomes dark with the bow lantern as the only light, and Rowan's lines `MRC-D6.30`, `MRC-D7.01–.05` and `MRC-D9.10` need new reasons. His canon refusal would then need the Director's reconciliation. |

### A8.2 The soundless bell (Beat 5): *the strange moment*

| Time | Element | Spec |
|---|---|---|
| Trigger | The boat reaches the middle of Stillgrave's open water (C5) during `S05`. Once per player. | |
| 0–2 s | **The hush** | All ambience fades out over two seconds: water, pole, birds. Rowan's pole stays in the water and still drips, silently. |
| 2–6 s | **The rings** | Along the far reed edge, the reeds lie down outward in a ring, as if something struck the air at the centre of the Hollow; then a second ring, wider; then a third. The fog shivers in the same rings (a ripple through the fog volume). The water surface does not move. |
| 6–8 s | **Nothing** | There is no sound at all. No tone, no hum, no low frequency. The silence is the event. |
| 8–10 s | **Return** | Ambience fades back in. The reeds stand up slowly over a few seconds. |
| Rowan | | He does not look round. He keeps poling. If the player speaks to him (an optional "Did you see—" interaction during the next 20 s), he says: "Keep your eyes on the knots." (`MRC-B6.2`). Nothing else, then or later. |
| UI | | No popup, no objective change, no log line. Subtitle for accessibility: **"[Silence. The reeds lie down.]"** |
| After | | `MRC_BELL_SEEN` set (barks only). **Never explained** (bible §7.5). Sennic's first story told of bells that rang without sound and reeds lying down; nobody draws the line for the player. |

### A8.3 Rowan's knots (world marker)

| Element | Spec |
|---|---|
| Prop | A clump of reed heads beside a channel stake on Rowan's route, with one of three states: **one knot**, **two knots**, **cut through** (the knot sliced and the head hanging). Readable at interaction range; no glow, no UI icon. |
| Inspect before `MRC_KNOTS_READ` | "Reed heads with knots tied in them. Somebody ties these on purpose." |
| Inspect after | One knot: "Rowan's knot. One: it turns at dusk." Two: "Rowan's knot. Two: it turns at first light." Cut: "Rowan's knot, cut through. Never this season." |
| Where | The landing stake, the practice cuts, the crossing route, and (post-story) the Chapel route. Never anywhere Rowan does not go. |
| Rule | Knots mark only his route and are tied only by him. No other NPC reads them aloud. |

### A8.4 Grounding on a wrong call

| Element | Spec |
|---|---|
| Practice runs | The boat slides onto a mud bank a few lengths into the wrong cut, tilts slightly and stops. A soft scrape. No damage. Rowan stands, leans on the pole, and pushes off. ~6 s. Then back to the cut mouth to call again. |
| Crossing | A wrong call never grounds the boat on the crossing. Rowan explains and takes the safe line himself into a side channel, and they wait for the turn. |
| Failure | None. A wrong call costs a few seconds and a dry line from Rowan. |

## A9. Quest structure for implementation

### A9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to Ysolde at the register table. | `MRC-D1` end | Yes | Quest Active on `MRC-D1` start (MR-M2 Completed). Journal lead on MR-M2 completion. |
| `S01_no` | Ask Rowan Mirewake for a crossing. / Help at the landing. | `MRC-D2` reaches `.20` (second refusal) and `.30` | Yes | Two refusals in one conversation. Objective text changes at `.30`. Opens `S04_ask`. |
| `S02_prepare` | Help at the landing. (Mend the boat. / Mend the tow harness. / Find moss for the bow lantern. / Sit with Sennic.) | (`MRC_HULL_DONE` or `MRC_HULL_CREW`) + (`MRC_HARNESS_DONE` or `MRC_HARNESS_CREW`) + (`MRC_MOSS_DONE` or `MRC_MOSS_CREW`) + `MRC_SENNIC` = 3 + `MRC-D3.40` | Yes | Any order. Crew alternatives each run a keep watch to the next morning; every crew alternative commissioned before a keep watch completes on that one wait. Sennic's sittings each require the presentation hour to have turned, by any wait (objective text says so). MRC-E1 at Stillgrave's edge. |
| `S03_knots` | Learn Rowan's knots. | `MRC-D5` lesson + practice run 1 + practice run 2 + `MRC-D5.40` | Yes | Daylight only (morning or noon). Wrong calls ground the boat (time only). Sets `MRC_KNOTS_READ`. |
| `S04_ask` | Ask Rowan why he won't cross at night. | `MRC-D6.30` end | **No** | Three asks, each on a separate presentation hour. Available from `S01` end. See §A9.3 for asks after the crossing. |
| `S05_crossing` | Wait at the landing for the grey. / Cross with Rowan. | Keep watch to morning (or arrive in morning) + `MRC-D7` + junction one + shoal (3 × `haul` segments) + MRC-E2 cut (3 stretches) + junction two + Stillgrave trigger + enter fog-bank volume | Yes | `[MD-3]` Grey pinned. Checkpoints at junctions. |
| `S06_roof` | Climb onto the chapel roof. | Enter roof volume + `MRC-D9` end | Yes | Sets `MR_ROWAN_TRUST`; quest → Completed; MR-M4 → Active. |

### A9.2 Flags

| Flag | Set by | Read by (here) | Read by (later) |
|---|---|---|---|
| `MRC_REFUSED` (count 0–2) | `MRC-D2` | `MRC-D2` options | — |
| `MRC_HULL_DONE` / `MRC_HULL_CREW` | Hull task path | `S02` predicate; barks | MR-M4 one Mabyn bark (`MCS-B1.4`) |
| `MRC_HARNESS_DONE` / `MRC_HARNESS_CREW` | Harness task path | `S02`; shoal bark | — |
| `MRC_MOSS_DONE` / `MRC_MOSS_CREW` | Moss task path | `S02`; `MRC-D9` (Rowan hands the bundle) | MR-M4 wicks (no difference in play) |
| `MRC_SENNIC` (count 0–3) | Each sitting end | `MRC-D4` sitting gate; `MRC-D3.40` | MR-M4 lead lines (`MCS-D4.05`, `MCS-B5.1`) |
| `MRC_KNOTS_READ` | `S03` | Knot inspect texts | Chapel route knot inspects; post-story |
| `MRC_ASKED` (count 0–3) | Each counted ask | `MRC-D6` gate; `MRC-D9.10`/`.11` | Sets `MR_ROWAN_TRUST` |
| `MRC_LAST_ASK_HOUR` | Each counted ask | `MRC-D6` gate (hour must differ) | — |
| `MRC_WRONG_CALLS` (count) | Crossing junctions | Barks (`MRC-B5.9`) | — |
| `MRC_BELL_SEEN` | Stillgrave trigger | Barks | — |
| `MR_ROWAN_TRUST` = told / kept | `S06` (`MRC_ASKED` = 3 → told; otherwise kept) | `MRC-D9` | MR-M5 circle (Rowan comes if told; keeps the landing lantern lit if kept); post-story Rowan lines |

No quest item. MRC is complete without `MBR_unit_logs` in the pack.

### A9.3 Choice: whether Rowan tells it

This is not a menu choice. It is the sum of the player's restraint and patience.

| Outcome | How it is reached | Immediate result | Later |
|---|---|---|---|
| **Told** (`MR_ROWAN_TRUST = told`) | Three gentle asks on three separate visits before the roof (`MRC_ASKED` = 3) | Rowan tells the story of the woman who taught him the route (`MRC-D6.30`). At the roof: "You know why." | **MR-M5:** Rowan comes up from the landing and stands at a stone of the circle (bible §9.3). Post-story: a few Rowan lines mention her boat. |
| **Kept** (`= kept`) | Fewer than three counted asks by the roof | Rowan says once, at the roof, that he noticed the player did not press him, and thanks them (`MRC-D9.11`). | **MR-M5:** Rowan keeps the landing lantern lit below the ridge; the player sees it from the circle. Post-story: Rowan's lines are drier and kinder. |

**Asks after the crossing (re-offerable missed moment, bible §11 rule 4).** The asking stays open at the landing after MRC completes, until MR-M5 becomes Active. A third counted ask in that window upgrades `MR_ROWAN_TRUST` from kept to told (`MRC-L-ROWAN`). The flag never moves from told to kept. If the Director prefers the flag to be final at MRC completion, cut `MRC-L-ROWAN` and nothing else changes (§A14).

Neither outcome is wrong. The crossing, the route and every later quest work the same either way.

## A10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| **The Chapel route** | Access | Rowan ferries the player between Blackwater Landing and the Chapel roof at Slack (morning or noon on his route schedule; at dusk he says "Morning." and at night he does not come). A Running or Sour channel means wait (keep watch). The crossing is a short ride after MRC: no fight, no calls; knots inspectable on the way. `[MD-3]` |
| **Rowan's knots** | Knowledge | Readable as world markers on his route for the rest of the game. |
| **A ferryman's pole** | Tool (functional name; item pass to define) | Rowan gives the player his spare pole at the roof if the player mended the boat themselves; the boatwright gives it at the landing if the crew did. A walking aid in wading segments (presentation); no stats proposed. |
| Small payment | Currency | A Memorykeepers' errand due from Ysolde, paid at the register room after MR-M4 (economy tuning). Rowan does not pay and is not paid. |
| Skill XP | Action only | Woodcutting and Leatherworking (if done by the player); Melee and Ranged by use. No lump quest XP (bible §11 rule 6). Relative weight [GD]: the two skill tasks are small intro-sized actions, not grinds. |
| Side-quest unlocks | Story | *The Father at the Ford* (MFW); *The Returning Wage* (MRW); *The Book of Arrivals* (MBA) if *The Stranger's Seat* is complete. |
| MR-M4 | Story | Continuous at the roof. |

## A11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Rowan says no | A step, not a gate. Two refusals always lead to *Help at the landing*. |
| A mending task is beyond the player's skill level | The crew alternative is always offered in the same dialogue (`MRC-D3.20`, `.25`). It costs a day (keep watch), never access. |
| Cold resin, wrong seam | Log line; warm again. No penalty. |
| Sennic is dozing | The sitting is not available until the hour turns. Keep watch at his fire. |
| Wrong call (practice) | The boat grounds softly; Rowan pushes off; call again. |
| Wrong call (crossing) | Rowan explains and waits in a side channel. Same outcome, a few seconds later. |
| Death | Respawn points per §A7. All mending, moss, sittings, knots and asks persist. During the crossing, the last passed junction is the checkpoint. |
| Player leaves during the crossing | The crossing cannot be left mid-ride (the boat is the player's only ground). Logout mid-crossing restores the player to Blackwater Landing at morning with `S05` active; Rowan: "Grey's still on. Get in." (`MRC-D7.90`). |
| Walking away | Stays Active. Resume hook: Ysolde at the register table before `S01` (`MRC-D1.90`); Rowan at his bench for `S01`–`S04` (`MRC-D3.90`); Rowan at the landing at morning for `S05` (`MRC-D7.90`). Mabyn waits on the roof (Part B). |
| Fail state | None. |
| Co-op | §A7. Mending and gathering progress is shared only with a partner whose own active `S02` consumes it (CDR-6; Integration MI-CO-03): a task a partner finished counts for the other as that task's crew path (crew flag, crew lines, the pole from the boatwright); the "mended it yourself" pole and lines go only to a player who mended the boat themselves. Sennic's sittings are per player (each partner hears their own sitting; a partner who has already heard one sits quietly). The grey is per player; any shared presentation is a presentation fallback only (Integration MI-CO-06, CDR-6; conflicts in Integration §5.2 Q-18) and never decides another player's route, step or credit. |

## A12. Integration needs

Documented dependencies for a later Systems Engineer. None is implemented here. Bible §11.2 needs are referenced by number.

| Need | Owner | Minimum viable form |
|---|---|---|
| **Channel states on Rowan's route** (N-1) | Systems | Per-crossing three-state table (Running / Slack / Sour) keyed to the presentation hour. **Fallback:** quest-pinned states only. MRC pins every junction for `S03` and `S05`, so MRC works on the fallback alone. |
| **Rowan's knot props** | Art + Systems | One reed-clump prop with three states; inspect text gated by `MRC_KNOTS_READ`. Authored data, not simulation. |
| **Boat ride with stops and calls** | Systems | Lowmark ferry convention (*Night Ferry*): an escorted ride on a fixed spline with authored stop points; at each stop a dialogue choice; a wrong choice plays an authored detour (practice: grounding; crossing: side-channel wait). |
| **Ride halts on enemy proximity** | Gameplay | The ordinary escort rule (as the MR-M1 cart: halts on enemy proximity): the ride spline pauses while any Echo is within reach of the boat and resumes when none is. No new enemy state. **Fallback:** the boat stops at each stretch start and moves on when that stretch's Echoes have each been defeated once. |
| **Harness haul** | Systems | Carry-state harness (weapons sheathed) + three channelled `haul` segments along a tow-post path; the boat prop moves with segment completion. Reuses channel convention with kept progress. **Fallback for Sol (if the walking haul is not available):** the haul is presented as three channel segments at a fixed bank pad beside the grounded boat (no walking between posts); the boat prop still moves on segment completion. |
| **Hour-turn gate** | Systems | A check that the presentation hour has changed since a stored value (`MRC_LAST_ASK_HOUR`, Sennic's sitting). Uses the existing keep-watch hour. |
| **The grey** | VFX + audio | Quest-pinned per-player fog volume with four density settings along the route; the bell's ring ripple through the fog volume. |
| **The soundless bell** | VFX + audio | Reed-flatten rings (three, expanding, ~1 s apart) on the far reed edge; full ambience duck to silence for ~6 s; no tone. |
| **Night gathering** | Art | Lantern-moss clusters as gather nodes that glow and are highlighted only at night; by day, non-interactive moss. |
| Creatures | Schema / Gameplay | Reedlurker (lurker, snapper); Earthen Echo (echo) with a straight-line "wade" approach (ordinary pathing in shallow water). |
| **Act I read-conditions** | Act I author / Schema | MR-M2 Completed; `MBR_unit_logs` possession check; `MR_NAME_RECORD`; `MR_CAUSEWAY`. |

## A13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **What stopped three columns on one day** (R08 seed) | The last Memorywardens grounded the battlefield (FT-02c). | Nobody has asked. | The day-books (Act I); Sennic's mages who "went out from" the church. | A rout; a flood; a curse. | — | **MR-M4 (owned).** |
| **Why Rowan won't cross at night** | His teacher went out one night for a sick child and did not come back. | "Rowan's careful." | His three answers. | He is afraid of the chapel; the chapel is cursed. | Her name; the child. | MRC (optional, told). |
| **The soundless bell** | Unexplained. | Riverfolk say the Sunken Church still rings. | The rings in the reeds; Sennic's story. | The bell is a warning; the Memorywardens are calling. | Everything. | **Never explained** (bible §7.5). |
| **The church sinking slowly** | It sank slowly into the bank; its drains rotted shut and it filled. | It sank in one night with everyone in it. | Sennic's "a step a year"; the door under; entry from the roof. | It was swallowed as a punishment. | Why it was built there. | MR-M4 (the drains, ordinary building). |
| **The name "Sinking Star"** | Unknown. | Many guesses. | Rowan: "Riverfolk say Church. I say Church." | Any. | The origin. | **Never explained.** |

## A14. Open decisions

1. **MD-3 (first-light crossing)** is built on as recommended. Tagged nodes and the swap are listed in §A8.1.
2. **"Rowan ferries at Slack" vs. "Slack grounds boats".** Bible §1.1 says boats ground at Slack; bible §6.1 says Rowan ferries at Slack. This package reconciles them without changing either: the stakes mean the same thing for everyone, and Rowan's route uses them his own way. His cuts are narrow, so at Running they pour like a weir and cannot be poled across; at Slack the cuts go still and the shoals go dry, so he poles the cuts and **hauls the shoals** (which is what the harness is for). Rowan teaches this in `MRC-D5.10`. If the Director prefers the bible §1.1 boat rule to read literally, Rowan's schedule flips to Running and the shoal becomes a channel; only `MRC-D5.10`, the junction stake states and §A10 change.
3. **Reed for the hull** is cut at the landing's own reed beds (an area of MP06), not at the Fowling Meres (MP26), so the hull task does not send the player across subzones. The bible says "at the meres"; if the Director wants MP26 used, only the reed-bed location changes.
4. **Sennic's "different days"** are implemented as sittings separated by a turn of the presentation hour (there is no world clock). Each sitting is short.
5. **`MR_ROWAN_TRUST` after the crossing** (§A9.3): asks remain open until MR-M5 starts and can upgrade kept → told. Cut `MRC-L-ROWAN` if the flag must be final at completion.
6. **Rewards:** "a ferryman's pole" needs the item pass. If cut, the line stays and the reward is the route alone.
7. **Map:** all geometry in §A5 needs the zone package (MAP VERIFICATION REQUIRED), especially the peat path from the landing to Stillgrave's near edge and the order of the route.

## A15. Internal review log

| Finding | Revision |
|---|---|
| The crossing risked teaching the stake rule again instead of testing it. | The stake rule is taught in MR-M1. MRC adds knots and makes the player call the route; the crossing is a test of things learned in `S03`, with Rowan's reasons on every wrong call. |
| Arcs §3.2 asks for a "guided night crossing". | `[MD-3]` first-light crossing in fog; night appears on foot at Stillgrave and on the chapel roof in MR-M4. |
| Asking risked becoming persuasion. | Asks are gentle, separated by time, optional, and a pushing option gets a flat "No." that does not count. Passage is granted by work and waiting, not by the asks (canon: restraint). |
| Rowan's story risked creating a second guide or a war relation. | The teacher is dead (she "never returned", canon); unnamed; no war relation; no other living guide is created. |
| Sennic risked explaining. | Three stories, each a *where*: the bell side faces slack water; the altar is under the big window; the way in is from the top. He never says what the mages did or why the church sank. Ysolde frames his words as his story. |
| The soundless bell risked a sound effect. | Silence is the effect; visual rings carry it for players without audio; subtitle "[Silence. The reeds lie down.]". |
| The boat fight risked letting ranged trivialise it, or requiring it. | Echoes re-form while the grey lasts; the cut ends by passage. Echoes at the gunwale hold the boat, so melee always has work; waders can be shot early, so ranged has work. (Independent review: the bespoke "grip" state and the contradictory "a player who does nothing still finishes" were replaced by the ordinary escort halt-on-proximity rule.) |
| Combat as evidence. | The Echoes prove nothing; the only belief bark ("the drowned getting up") is answered with "Mud." |
| Skill hooks. | Woodcutting (thwart) and Leatherworking (harness) at ~[GD: low], each with a crew alternative that costs a day (CDR-4 meaningful requirement without a gate). |
| Length. | Four preparations, one lesson, one crossing: within 35–45 minutes with short sittings and one night walk. |

---
---

# Part B: MR-M4 The Chapel of the Sinking Star (`MCS`)

## B1. The quest in one paragraph

Rowan has gone back into the fog and will not come again until morning slack. **Mabyn Coyle** keeps the Sunken Chapel's roof lantern line, alone since the spate, and has not been below the gallery since. She will let the player in if they help her relight the line. On the roof the player relights the outer lanterns with moss from the crossing and Mabyn's peat-wax, and clears the Reedlurkers out of the shallows round the lowest posts. Mabyn teaches the Tenders' one rule: lit is held. In the dark, the Chapel Shades come: not ghosts, she says, only dark that is heavy, and they lean on your light until it goes out and push you back to the nearest lit post. Down through the bell-loft hatch, past an empty bell frame, the player reaches the gallery and looks down at a nave full of black water with stained glass glowing faintly under it, and a vestry door under the surface. The chapel was built on a raised bank and drained by stone culverts with wooden sluice boards; the boards rotted shut and the chapel filled. Through the gallery windows the player reads the buttress stake and, over each of the three culvert mouths outside, an old water stain. The board under the highest stain opens first, and only at Slack. The first board drops the nave one stage and lifts the channel to Running, so the player sits by a lit post with Mabyn until dusk. Each correct board drops the water another stage and opens new ground with dark posts that must be lit before the Shades fill it, while Silt Crawlers stirred out of the silt and Reedlurkers in the pools come at the light. At the second stage the vestry door stands clear: a wartime field post, and on a hook an officer's dispatch case with a log whose last entries are the same day as the day-books from the causeway. The log says the chapel's people went out at grey light in a line with lanterns and no arms, and the field went quiet, and the men sat down where they stood. At the third stage, as the last water falls, the stained glass is lit from behind, gold and blue, by nothing; then it is only glass with peat behind it. Under the altar, beneath the great window, crypt steps go down to a lead-lined box of fired clay leaves pressed with office marks and no names: the plan to lay the calm across the field of standards at the turning of the light, a list of stones to be held on Bannerline, a row of marks for those going out that runs off a broken edge, and a last leaf, unfired and cracked, in a different hand, with a short row for those who came back and the words *"The circle is not closed. We could not."* Opening the crypt pulls a draught through the nave; the posts gutter one by one, and the player carries the leaves up through the pressing dark to Mabyn holding the top post. They sit the rest of the night on the roof with the line lit, and the player decides who keeps the record. At first light Rowan comes. At the landing, Ysolde is waiting.

**What the player should remember:** the water falling in stages, the posts going dark one after another on the way out, and the glass lit by nothing. **What the player should want next:** to go up Bannerline and see the circle that was never closed.

## B2. Selection record

| Candidate | Verdict |
|---|---|
| **A. A submerged dive with breath and lantern management (Arcs §3.2 wording).** | Rejected `[MD-4]`. No swimming, no air bar, no new movement mode (CDR-4, bible §11.1). The same fear of a drowned building is carried by dark ground and light. |
| **B. The record is read aloud by Mabyn or Ysolde.** | Rejected. R08 requires the player to read two custodians: the leaves and the vestry log. Mabyn does not know what is under the altar; Ysolde sees the record only at the landing and calls her one link "my reading". |
| **C. A boss in the crypt.** | Rejected. The bible gives MR-M4 no boss; the Mire's danger here is the dark. A fight at the record would also tempt combat as evidence. |
| **D. Roof line → gallery → read the building → three boards at Slack with a dusk wait → vestry log at stage two → glass and crypt at stage three → the draught out → a night vigil and a custody choice → first light → Ysolde at the landing** (selected; the bible brief). | **Selected.** The quest runs morning, dusk, night and grey in one visit, so the chapel is seen in every light. The truth arrives in two separate rooms and two separate hands. |

## B3. Canon grounding

| Element | Source | Status |
|---|---|---|
| The Chapel of the Sinking Star: almost fully submerged war-chapel; Chapel-Tenders maintain lantern lines from its roof; stained glass intact beneath the surface; a Memorywarden relic rumoured beneath the altar; one site, three names; origin of the formal name unknown | Dossier §VI.6; C14 | [CANON] |
| The church sank slowly, not by collapse | Sennic anchor; Part 4 ledger | [CANON] (as Sennic's story) |
| Chapel-Tenders: religious, not magical; lantern lines; river hymns at burials; bone pits; reflection pools; memory altars | Dossier §III, §XIII | [CANON] |
| Lantern lines stay lit through wind by peat-wax blends, thick wicks and covered housings; people credit "the land's approval" but it is craft | Dossier §XVI.4 | [CANON] |
| The Lantern That Would Not Go Out: lit seven nights after a devastating battle; belief that it was a Memorywarden's final act | Dossier §XII.4 | [CANON myth] |
| Chapel Shades: minor, place-bound memory impressions, not souls | Dossier §IX; bible §2.4 | [CANON]; hazard treatment [NEW, bible §10] |
| Silt Crawlers: hard-shelled crustaceans that thrive near drowned encampments | Dossier §X | [CANON] fauna; stirred by draining [NEW] |
| The Mire as the war's central battlefield; Memorywardens conscripted as guides and healers | World truth H12 | [CANON] |
| The last great battle; the calm-field laid by the last Memorywardens; it stopped the fighting, killed most of them and concentrated the General | FT-02c; Timeline §V | [APPROVED — FT-02c] |
| Withheld forever in Mire content: the Memorywardens' names, which armies collided, how many died; the origin of "Sinking Star" | Revelation ledger R08; FT-02; bible §2.2 | [APPROVED] withheld |
| The chapel's drains and sluice boards; the field post in the vestry; the lead-lined box of clay leaves with office marks; the leaves' wording; the draught; the Tenders' roof loft | Bible §2.1, §2.2, MD-6, §6.1 | [NEW] |
| Staged drainage and lantern lines in place of breath management | Bible MD-4 | [PROPOSAL — DIRECTOR] |

## B4. Quest summary card

| Field | Value |
|---|---|
| Working title | **The Chapel of the Sinking Star** |
| Suggested content id | `mire.main.04_chapel_of_the_sinking_star` |
| Arc position | Act II turn; Arcs §3.2 "Recover the Memorywardens' last record" |
| Prerequisite | MR-M3 Completed (continuous) |
| Offer | Automatic at `MRC-D9` end on the chapel roof; Mabyn continues the conversation (`MCS-D1`). Resume offer from Mabyn on the roof whenever the player arrives by the Chapel route. |
| Target length | 55–70 minutes (one visit: morning, dusk, night, grey) |
| Combat share | ~20% (Reedlurkers, Silt Crawlers) |
| Hazard share | ~20% (Chapel Shades, the draught) |
| Dialogue share | ~15% |
| Drainage puzzle, lighting, reading, carrying, vigil, choice | ~45% |
| Skills | Melee or ranged (CDR-2; ranged never required). No skill gate. Agility (optional gallery gap; walkable fallback). |
| Choices | Who keeps the record: **sorrowmere** / **altar** / **tenders** (3 options; each keeps the knowledge public) |
| Unlocks | `MR_WARDEN_RECORD`; the chapel interior lit and revisitable; *The Lantern That Would Not Go Out* (with MLL); MR-M5 (automatic on next entry to Sorrowmere or Griefwatch) |
| **Anchor** | Chapel-Tenders (Mabyn Coyle); the Chapel of the Sinking Star; Memorykeepers (Ysolde) as receivers |
| **World-truth row** | **H17** (the Mire's stop: the Memorywardens' last grounding, FT-02c) |
| **Revelation role** | **Owns R08:** the Mire's front stopped because the last Memorywardens grounded the battlefield; the overload killed them. (That it concentrated the General is not in the record; Ysolde links it as her own reading, and MR-M5 pays it as consequence.) |
| **Recurring evidence** | **Two custodians, both required:** `MCS_warden_leaves` (the altar record) and the **vestry regimental log** (read in place; a soldier's field post, not the chapel's). The `MBR_unit_logs` (Act I, Calwen's causeway chest) add weight: the same weather run and the same last day (the second fog), different columns. The leaves' stone list recurs in MR-M5 at the Bannerline circle. |
| **State compliance** | Inactive / Active / Completed only. The drainage puzzle resets harmlessly on a wrong board; a board at Running simply will not turn; Shades cost time and never health; the draught gutters each post once. Choice recorded in `MR_WARDEN_RECORD`. No fail path. |
| **Combat compliance** | Reedlurkers (MCS-E1, MCS-E3) and Silt Crawlers (MCS-E2, MCS-E3) are defeated at 0 HP; Crawlers are harvestable per the economy pass. Chapel Shades are a hazard with no HP and cannot be targeted (bible §10). Every fight accepts melee or ranged. No SX. |

## B5. The places

All placement is relative. **MAP VERIFICATION REQUIRED** for the chapel's setting (MP13 in the Blackwater, reached only by Rowan's route). The interior is a self-contained interior zone; its geometry is authored here for the zone package and needs only: a roof ridge just above the water with a squat bell-tower at one end (the **bell side**); a hatch in the tower roof into the bell-loft; a ladder down to a **gallery** running round three sides of the nave at clerestory height; the nave flooded to just below the gallery; the **great window** at the altar end, wholly below gallery level, its outer face against the bank's peat; a **vestry** off one side of the nave; and three gallery-level windows (plus the bell-loft window) looking out over the side channel at the chapel's outer wall.

### B5.1 The roof [MP13]

| Area | Storytelling |
|---|---|
| **T1. The ridge line** | Six lantern posts along the roof ridge and down the lower slope, each with a covered housing. Half are dark: damp in the housings, wicks rotted. Moss on the tiles. Optional inspect: tiles worn in a path along the ridge by generations of Tenders' feet. |
| **T2. The lower slope and landing stage** | The roof's lower slope runs into shallows. A plank landing stage for Rowan's boat. The two lowest lantern posts stand in knee-deep water; Reedlurker ground (MCS-E1). |
| **T3. Mabyn's loft** | A Tenders' shelter built against the bell-tower on the roof: reed thatch, a peat stove, jars of moss, a cake of peat-wax, a wooden **Tenders' chest** with a peg lock. Where the leaves go in the *tenders* outcome. Respawn point before `S02`. The peat stove is an ordinary cooking spot and Mabyn offers food in the loft ("Sit. Eat."), so a player low on food after the crossing can restock before the chapel fights without waiting for Rowan. |
| **T4. The bell-tower hatch** | A trapdoor in the tower roof with a ladder down. Mabyn's own pole lantern hangs on a hook beside it: the **top post** of the inner line. |

### B5.2 The bell-loft and the gallery

| Area | Storytelling |
|---|---|
| **G1. The bell-loft** | A square loft. An **empty bell frame**: oak beams, an iron pin where a bell hung, a rope groove worn into the beam. No bell, no clapper, nothing on the floor. Two dark lantern posts (the first inner posts). The Shades are first met here. |
| **G2. The bell-loft window and Windlass A** | A narrow window on the bell side, looking out over the slack side channel. Through it: the **buttress stake** (a Reedsward-style stake painted on the chapel's own buttress, three bands) and, below the window, the outfall mouth of culvert A with its **stain**. Beside the window, **Windlass A**: a wooden windlass on the floor with an iron rod running down a slot in the wall. |
| **G3. The gallery** | A timber gallery on stone corbels round three sides of the nave, a rail carved with Tenders' marks. Below: black water to within a metre of the gallery floor; faint colour in it where the great window lies under the surface. The vestry door's top is a dark line under the water on one side. A broken section of gallery between G3 and G5: an **agility gap** (step across) with a walkable fallback back round through the loft. |
| **G4. The far window and Windlass B** | At the far end of the gallery, above the altar end. Window, outfall mouth B and its stain; Windlass B. |
| **G5. The corner window and Windlass C** | At the gallery corner on the vestry side. Window, outfall mouth C and its stain; Windlass C. |
| **G6. The gallery post** | A lantern post at the head of the stair down into the nave. Mabyn stands here from `S03` on; it is lit for the rest of the quest and is the wait point for the dusk turn. Respawn point after `S02`. |

### B5.3 The nave, by stage `[MD-4]`

The nave is one space with three discrete water levels (environment variants, bible N-3). Deep water is non-walkable at every stage. Each stage exposes new walkable ground and new dark lantern posts.

| Stage | Exposed ground | Posts | Encounters |
|---|---|---|---|
| **0 (start)** | None below the gallery. | — | — |
| **1** (Board B) | **N1. The upper aisle walk**: a stone walk along the nave walls at the height of the old aisle roofs, slick with silt, with a stair down from the gallery post (G6). | 4 (P1–P4) | MCS-E2 (Silt Crawlers) |
| **2** (Board C) | **N2. The lower bays**: the side bays of the nave, pools left in their hollows; the **vestry door** stands clear. | 5 (P5–P9) | MCS-E3 (Reedlurkers in the pools, Crawlers) |
| **3** (Board A) | **N3. The nave floor and the altar**: the flagged floor, the altar on its step, and behind it the **great window**, now clear of water. | 4 (P10–P12 and the altar post P13) | None (the glass) |

### B5.4 The vestry

| Area | Storytelling |
|---|---|
| **V1. The field post** | A small stone room used as a wartime field post: a folding camp table swollen with water, an ink stone, a cot frame, a broken lamp. Nothing here is a body and nothing is countable. |
| **V2. The hook and the dispatch case** | On an iron hook high on the wall (above the old water line, which is why it survived), an officer's dispatch case in oiled leather. Inside, a **regimental log**. The case's unit mark has rotted away. **Required read in place** (`S04`). |

### B5.5 The crypt

| Area | Storytelling |
|---|---|
| **K1. The altar** | A plain stone altar on a step, directly under the great window (Sennic's "under the big window"). A slab in the step lifts on an iron ring once the water is gone. |
| **K2. The steps** | A short stair down. Dry, because the crypt was sealed. Cold air. |
| **K3. The shelf and the box** | A stone shelf with a **lead-lined box**, its lid sealed with a lead strip. Nothing else. Bare walls. The box is opened by prising the strip (channelled). Inside: four clay leaves (`MCS_warden_leaves`). |

### B5.6 Blackwater Landing at morning [MP06]

| Area | Storytelling |
|---|---|
| **L1–L3** (as §A5.2) | Morning after the vigil. Ysolde on the dock with a ferry household's bread in a cloth. |

## B6. Player-facing sequence

### Beat 0: Help Me With the Line (`S00_offer`)
**Objective:** *Talk to Mabyn on the roof.*
Continuous from `MRC-D9`. Mabyn (`MCS-D1`) has heard from the ferry households that someone was asking about the Sunken Church. She does not ask why yet. She asks for help: the line is half dark, she cannot keep it alone, and she has not been below the gallery since the spate. "Help me light it and I'll let you in. That's the trade. It's a fair one; I'm the one who has to live on the roof." With `MR_LANTERN_LINE`: one line about the Stillgrave ring (`MCS-D1.06`).
**Verbs:** talk.

### Beat 1: The Roof Line (`S01_roofline`)
**Objective:** *Relight the roof lanterns.*
Six posts along the ridge and down the lower slope (T1, T2). At each: open the housing, scrape out the rotted wick, set a moss wick from the bundle Rowan handed up, seal with peat-wax, light (one channelled interaction, ~3 s). Mabyn works the ridge posts alongside and teaches as she goes (`MCS-D2`): peat-wax, thick wick, covered housing, "and somebody awake". The two lowest posts stand in the shallows: **MCS-E1** (Reedlurkers). When all six are lit, Mabyn teaches the rule at the hatch: lit is held; in the dark, the Shades come; they are "only dark that's heavy", never people; they lean on your light until it goes out and push you back to the nearest lit post. "They don't hurt you. They take your time. Down there, time's the thing." She gives the player a **Tender's hand lantern** (carry-state, §B8.1).
**Verbs:** clean, wick, light, fight, listen.

### Beat 2: The Gallery (`S02_gallery`)
**Objective:** *Go down into the bell-loft.* Then: *Look down into the nave.*
Through the hatch (T4) into the bell-loft (G1). The empty bell frame (optional inspect, `MCS-I2.01`). Two dark posts. The player lights the first; crossing to the second, the dark ground ahead thickens and the hand lantern's flame leans away: **the first Shade press** (scripted teach, §B8.1). If the lantern goes to ember the player is pushed back to the first post; Mabyn calls down the hatch (`MCS-B2.2`). With the second post lit, the loft is held. Down the ladder to the gallery (G3). Required inspects: **the nave water** with the glass under it (`MCS-I3.02`) and **the vestry door** under the surface (`MCS-I3.03`). Optional: the Tenders' marks on the rail. Mabyn comes down the ladder as far as the gallery post (G6), lights it, and stays there (`MCS-D3`): "This far I'll come. Below the gallery's yours."
**Verbs:** descend, light, endure, look.

### Beat 3: Read the Building (`S03_drain`, first part) `[MD-4]`
**Objective:** *Read the stake on the buttress.* Then: *Read the culvert stains.* Then: *Open the sluice boards in order.*
Mabyn knows the chapel had drains; every Tender knows that; nobody has worked them in her life (`MCS-D4`). "The boards rotted shut. Water came in at the top and had nowhere to go." She knows two rules from her own teacher: **the boards work only at Slack**, and **"the chapel tells you where the water stood."** She does not know which board is first.
- **The stake.** At the bell-loft window (G2), inspect the **buttress stake**: ochre (Slack) on arrival. With `MRC_SENNIC` = 3, a line: the bell side faces the slack water, as Sennic said (`MCS-I4.01`).
- **The stains.** At each windlass window (G2, G4, G5), inspect the culvert mouth outside and the **old water stain** above it (`MCS-I4.02`–`.04`). Each stain is described against the chapel's own stonework (a string-course under the windows, the coursing of the wall): **B** reaches the string-course under the window (highest); **C** reaches the second course above the mouth (between); **A** is a band just above the mouth (lowest). The order is read, not told: highest first (§B8.2).
- **The boards.** Each windlass is wound by a channelled interaction (2 segments of ~3 s; segments persist).
  - At **Running** (pale), a windlass will not turn: "The board won't lift. The water outside is leaning on it." (`MCS-B3.1`). No penalty.
  - **Wrong order** at Slack: the board lifts, water roars into the culvert, then the culvert chokes; water backs up and bubbles at the outfall, and the board drops back into its slot. Nothing drains. Harmless reset (`MCS-B3.2`). `MCS_WRONG_BOARDS` +1. After two wrong boards Mabyn offers her teacher's words again; after three she says plainly "Look at each mouth from its window. Highest stain first. That's all she ever told me." (guaranteed path).
  - **Board B** first. The nave drops to **stage 1** (§B8.2): the water falls with a long roar through the walls, the gallery shakes, and the upper aisle walk (N1) comes out of the water, silted and dark.
**Verbs:** read, compare, wind, be wrong, reset.

### Beat 4: Stage One and the Wait (`S03_drain`, second part)
**Objective:** *Light the aisle walk before the dark fills it.* Then: *Wait for Slack.*
The aisle walk (N1) is dark ground. Shades fill it ~6 s after the player steps off the lit stair (§B8.1). The player lights P1–P4 in turn; each post's light reaches just short of the next. **MCS-E2:** Silt Crawlers, stirred by the falling water, burst out of the fresh silt and come at the light (two waves of two). Fight in a lit stretch or on the edge of one; fighting in the dark means Shade presses while you fight.
When P1–P4 are lit, the buttress stake reads **pale** (Running): the first board let out the top of the water, which is most of it, and the side channel has risen. Mabyn: "Running till dusk now. Come and sit by a lit post." (`MCS-D5`). The player **keeps watch** at the gallery post with Mabyn until **dusk**. Mabyn talks (optional, `MCS-D5.10`–`.40`): how she came to the Tenders, what the line is for, a dry joke about Rowan. The stake turns ochre.
**Verbs:** light, fight, wait, sit.

### Beat 5: Stage Two (`S03_drain`, third part)
**Objective:** *Open the next sluice board.* Then: *Light the lower bays.*
**Board C** at dusk Slack. The nave drops to **stage 2**: the lower bays (N2) and the vestry door. The player lights P5–P9 down the bays. **MCS-E3:** Reedlurkers in the pools left in the bay hollows (two lurkers and a snapper) and two more Crawlers. The vestry door is clear and opens (Beat 6 may be done now or after Beat 7's board; the crypt waits for it).
**Verbs:** wind, light, fight.

### Beat 6: The Vestry (`S04_vestry`)
**Objective:** *Search the vestry.*
Available from stage 2. The vestry (V1, V2) is dark ground with no post: the player lights it with the hand lantern alone, and the Shades lean in at the door but the room is small. On the hook, the officer's dispatch case. **Required read in place:** the **regimental log** (`MCS-I6.02`; full text in the dialogue file). Its entries are headed by the weather, not by date, and they run the same weather as the three day-books from the causeway chest: rain, rain, rain, a hard frost, a thaw, fog, fog. It stops on the second fog, as they do. It is from a column those day-books do not cover; its unit mark has rotted off the case. It says, in a soldier's plain hand: the field post was moved into the chapel vestry; the chapel's people kept the roof lantern; nobody on the field could go back over the channels and nobody could win the ground; the chapel's people asked that nobody fire on anyone walking out at first light without arms; at grey light they went out from the chapel in a line with lanterns and no arms, onto the field; then quiet, not a shot, not a shout, and the men sitting where they stood; at dusk, not many of the chapel's people came back past the post; they would not be helped; they went down under the big window and shut the stair. Last line: *"The lantern on the roof is lit."* Sets `MCS_VESTRY_READ`. The log stays on its hook.
Mabyn, from the gallery, asks what is in there. The player can tell her now (`MCS-D6`) or later on the roof.
**Verbs:** search, read.

### Beat 7: Stage Three: the Glass (`S03_drain`, end): *the strange moment*
**Objective:** *Open the last sluice board.* Then: *Light the nave floor.*
**Board A** (the bell-loft windlass, nearest the hatch and last in order). The nave drops to **stage 3**. **The strange moment** (§B8.3): as the last water falls away from the great window, the stained glass is lit from behind, gold and blue, by nothing; then it is only glass with peat behind it. Mabyn, at the gallery rail, sees it too. She says nothing until the player looks up at her, then: "Seen: it lit. Thought: I don't know. That's all I've got." (`MCS-B4.3`). The player lights P10–P12 across the floor and the altar post P13. Sets `MCS_STAGE` = 3, `MCS_GLASS_SEEN`. `S03` completes.
**Verbs:** wind, witness, light.

### Beat 8: The Crypt (`S05_crypt`)
**Objective:** *Look beneath the altar.* Then: *Open the box.* Then: *Read the leaves.*
Requires `S03` and `S04`. The altar stands under the great window (Sennic's lead). Lift the slab in the altar step by its ring (interaction ~2 s). Down the steps (K2). On the shelf, the lead-lined box (K3). **Prise the lead strip** (channelled, 3 segments of ~3 s; persist). Inside, wrapped in rotted cloth, four clay leaves. Take them (`MCS_warden_leaves`; Mabyn's oilcloth wraps them on the way out). **Read them** (document view, four leaves; text in the dialogue file):
1. **The plan** (fired): from "the wardens of memory kept at this house". *"We will lay the calm across the field of standards at the turning of the light. The ground will take what we give it. If we cannot carry it, it will carry us."* They go without arms and without names; the marks are enough.
2. **The stones** (fired): the stones to be held on Bannerline, by their places (the post stone, the low stone by the palisade, the split stone, the stone that faces the field, the stone with the old cut in it), the list running onto a broken corner; and "the last stone, which closes it, to be set when the calm is laid".
3. **Going out** (fired): a row of tally marks that runs off the broken edge of the leaf.
4. **Come back** (unfired, sun-dried, cracked across; a different hand): a short row of marks smeared where a thumb pressed them, and *"The circle is not closed. We could not."* The office mark pressed twice, the second time crooked.
No leaf states or totals a number, and the marks cannot be counted (§B8.4). No leaf names a person, an army or a battle. With MR-M2 Completed, an optional inspect notes the pressed office mark is *like* the faint marks on the clay shard from the causeway (`MCS-I7.06`). Sets `MCS_LEAVES_READ`.
Together with the vestry log: **two custodians**. The Memorywardens went out at the turning of the light to stop the fighting on the field of standards; the field went quiet; few came back; their circle on Bannerline was not closed (R08).
**Verbs:** lift, prise, read.

### Beat 9: Out by the Line (`S06_out`)
**Objective:** *Carry the leaves up to Mabyn.*
Opening the sealed crypt lets its air out, and with all three culverts open, a **draught** pulls up through the nave toward the bell-loft hatch (§B8.5). The posts gutter, one after another, from the floor upward. Each post gutters **once**. The player carries the leaves up: floor → bays → aisle walk → gallery → loft → hatch, relighting guttered posts (~2 s each) or running between them. The Shades press hard in the gutters' dark (form after ~3 s, press every ~2 s). At ember the player is pushed back to the nearest lit post reachable on the walkable route (never across a level change), which is never further back than the last post the player relit. **Mabyn holds the top post** at the hatch with her pole lantern, which does not gutter; she calls down the stair (`MCS-B6`). At the hatch she takes the player's wrist and pulls them up into the air. The draught dies. Below, the line she and the player relight is steady.
**Verbs:** carry, relight, endure, climb.

### Beat 10: The Vigil and the Record (`S07_vigil`)
**Objective:** *Sit the night with Mabyn.* Then: *Decide who keeps the record.*
Night on the roof. Mabyn lights the last ridge lantern, makes peat-tea, and sits (`MCS-D9`). Food and tea before the question (§5.3 rule 6). If the player tells her the vestry log's last line (*"The lantern on the roof is lit."*), she is quiet for a long moment and then tells the Tenders' story of the seven-night lantern as craft and stubbornness: "They kept it lit for people who went out and didn't come back. That's what it was for. Not a miracle. People not sleeping." (seed for MLW; belief stays belief.) She asks what is in the leaves and the player tells her (or shows them).
Then the question: who keeps the record (§B9.3). Mabyn: "You brought it up. The leaves were never ours; we only kept the roof. Say where it goes and I'll pray over it either way." The player chooses:
- **Sorrowmere:** the leaves stay in the player's pack for Ysolde.
- **Altar:** the player and Mabyn go back down the lit line to the crypt; the player lays the leaves back in the box; Mabyn says a river hymn over it; the player takes a **reed-paper rubbing** of the last leaf with Mabyn's charcoal (carry-state) for Ysolde; they close the slab.
- **Tenders:** the player lays the leaves in the Tenders' chest in Mabyn's loft (T3); Mabyn pegs it.
Sets `MR_WARDEN_RECORD`. The player keeps watch until first light `[MD-3]`.
**Verbs:** sit, tell, decide, carry, keep watch.

### Beat 11: First Light and the Landing (`S08_landing`)
**Objective:** *Cross back with Rowan.* Then: *Tell Ysolde what you found.*
At first light Rowan's boat comes out of the grey (`MCS-D10`). He looks at the lit line along the ridge, then at Mabyn. "Line's lit." That is all he says about it. The ride back is short and quiet (no calls, no fight; knots inspectable). At Blackwater Landing, **Ysolde** is on the dock with bread in a cloth (`MCS-D11`). "Sit. Eat. Then tell it." The player tells her (dialogue recall): the vestry log (the weather run that stops on the same fog; the line of people going out; the men sitting down); the leaves (the plan, the stones, the rows, "the circle is not closed"). Ysolde sets them side by side: "The log is one hold. The leaves are another. Two holds. That's an account." Then, carefully, she makes one link herself: Griefwatch talks about something on Bannerline that gives orders and has since the war, and the leaves say the circle on Bannerline was never closed. "I've put those two side by side. That's my reading. It isn't a hold." She writes in her reed book (outcome lines, §B9.3). The quest completes when she blots the page.
**Verbs:** cross, eat, tell, witness.

## B7. Encounters

Tuned for **Advanced** identity (MD-10). Every enemy is defeated at 0 HP (CDR-1). Every fight accepts melee or ranged; none requires ranged (CDR-2). Fauna here fight because the draining has stirred them; outside the quest they fight only when provoked (bible §10). Chapel Shades are not enemies.

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MCS-E1** | 2 × Reedlurker (lurker), 1 × Reedlurker (snapper) | The roof's lower slope (T2), in the shallows round the two lowest posts, during `S01` | Lurkers wait submerged by the posts and lunge at a player working a housing. The snapper spits from deeper water off the slope. | As MRC-E1: **lunge** reed-ripple ~1.2 s; **spit** head rises, ripple stops ~1.0 s, slowing slick. | Open the quest with a familiar threat while the player learns the posts. | 60–90 s; 65–80% HP remaining |
| **MCS-E2** | 4 × Silt Crawler, two waves of two | The upper aisle walk (N1) at stage 1 | Crawlers burst out of fresh silt near the player and close. **Hard front shell:** hits from the front deal reduced damage; sides and back take full. They turn to face slowly. (Optional: if directional armour is not built, the shell is replaced by more health and the slow turn stays as presentation; Enemies file R-9, I-14.) | **Burst:** silt bubbles in a line toward the player (~1.5 s), then the crawler erupts at the line's end (step off the line). **Pinch:** shell clatters and claws rise (~1.0 s), then a pinch. **Turn:** visible shuffle (~1.5 s to face a player who steps round). | Teach a fight inside the light: step round for the flank (melee) or reposition for an angle (ranged). | 60–90 s per wave; 60–75% HP remaining after both |
| **MCS-E3** | 2 × Reedlurker (lurker) in bay pools, 1 × Reedlurker (snapper), 2 × Silt Crawler | The lower bays (N2) at stage 2 | Lurkers in the pools left in the bay hollows lunge at players lighting posts on the pool edges. The snapper spits from the largest pool. Crawlers burst from the silt between bays. | As above. | The densest fight in the act; mixes the two families; pools make lanes. | 2–3 min; 55–70% HP remaining |
| **MCS-H1** | **Chapel Shades** (hazard; no HP; untargetable) | All dark ground inside the chapel | Thickening dark at the edge of the player's light. Presses the hand lantern; at ember, pushes the player back to the nearest lit post. Suppressed within a lit post's radius. | **Lean:** the hand lantern's flame leans away from the dark (~2 s), then a **press** (one lantern state lost). | The chapel's real danger: time and the dark. Makes lighting the line matter. | — |
| **MCS-H2** | **The draught** (scripted hazard) | Floor to hatch, `S06` | Each post gutters once in a wave from the floor upward; Shades form faster (~3 s) and press more often (~2 s). | Gutter: the post's flame shrinks and smokes (~1.5 s) before it goes out. | The way out: carry the record up through a dark that keeps coming. | 2–3 min |

**MD-7 swap:** none needed. No Hollowfoot appear in MCS.

**Rules**
- **Combat never reveals evidence.** The log is read in place; the leaves are read in the crypt; the glass and the Shades prove nothing. No Shade has a face, a name, a voice, a unit mark or a word. No NPC calls them souls or ghosts; Mabyn calls them "the press" or "the shades", and "only dark that's heavy".
- **Shades never harm.** No HP damage, no debuff beyond the lantern's light state; the push returns the player to a lit post. They are suppressed within ~6 m of a lit post (bible N-2).
- **Fights in the light.** Every encounter spawns at or next to lit ground once its stage's first post is lit; a player can always draw enemies into light. Enemies are not affected by Shades.
- **No drowning.** Deep water is non-walkable at every stage. A player who steps toward deep water is stopped at its edge.
- **Death:** respawn in Mabyn's loft (T3) before `S02`; at the gallery post (G6) after. Water stage, opened boards, lit posts, the vestry read and the leaves persist. Shades reset. In `S06`, guttered posts the player has relit stay lit.
- **Co-op:** shared enemies; a defeat credits each partner whose own active step consumes it (Lowmark §8.1). Water stage is per player; co-op presentation is unresolved (MI-CO-06, CDR-6; Integration Q-18). Boards and posts credit only the partner who works them on their own step. Each partner reads the log and the leaves for themselves. Each partner chooses custody in their own state; where per-player props are unavailable, a shared custody prop may be shown as a presentation fallback only (Integration MI-CO-06, CDR-6) that never decides a partner's choice; each partner's own `MR_WARDEN_RECORD` drives their own lines and epilogue.

## B8. The discovery and strange moments: presentation specs

### B8.1 Lantern lines, the hand lantern and the Shades `[MD-4]`

| Element | Spec |
|---|---|
| **Lantern post** | A post with a covered housing. States: **dark** (cold housing), **lit** (steady green-gold moss light, radius ~6 m), **guttering** (`S06` only: flame shrinks and smokes, ~1.5 s, then dark). Light: one channelled interaction (~3 s) with the moss bundle and peat-wax in the pack; relight after guttering ~2 s. |
| **Hand lantern** (carry-state, Mabyn's) | Three visible looks on the prop itself: **bright** (radius ~3 m), **low**, **ember**. These are presentation of one dark-ground timer (presses 0–2), not a stored light stat: no meter, no bar, no fuel, and the timer simply resets on entering a lit post's radius (shown as the flame recovering over ~2 s). A log line on each state change ("Your lantern dims." / "Your lantern is down to an ember."). |
| **Dark ground** | Any walkable ground outside every lit post's radius. After **~6 s** continuous in dark ground (`S06`: ~3 s), Shades form at the edge of the hand lantern's light. |
| **Shades** | Not figures. Dark that thickens into shapes at the very edge of the light, heavier low down, never a face, never an outline of a person, never a unit or banner. They do not move toward the player; the dark closes. |
| **Press** | **Tell:** the hand lantern's flame leans away from the thickest dark and the light shrinks (~2 s). **Press:** the lantern drops one state. Every **~4 s** while in dark ground (`S06`: ~2 s). |
| **Push** | At ember, the next press pushes the player back to the nearest lit post reachable on the walkable route (never across a level change): the screen dims at the edges, the player staggers (~2 s, no control), then stands in the post's light. No damage. |
| **Audio** | No voices. A low pressure in the ears; the moss light's faint crackle; drips. When a post is lit, the pressure lifts. |
| **Accessibility** | Subtitles: "[The dark leans on your lantern.]" / "[Pushed back to the light.]" The lantern's state is also shown by its prop size and colour, never by sound alone. |
| **Fallback (N-2 not built)** | Pre-authored lit and dark zones that flip at each drainage stage, with the same press timings inside dark zones. |

### B8.2 Staged drainage: solution table (design) `[MD-4]`

| Windlass | Location | Stain as seen from its window | Order | Result when correct |
|---|---|---|---|---|
| **B** | Gallery far end (G4) | "The stain reaches right up to the string-course under this window. The stone is black to there." | **1st** | Stage 1: upper aisle walk (N1), P1–P4. The side channel lifts to **Running** until dusk. |
| **C** | Gallery corner, vestry side (G5) | "The stain stops at the second course of stone above the mouth." | **2nd** | Stage 2: lower bays and the vestry door (N2), P5–P9. Channel stays Slack. |
| **A** | Bell-loft window (G2) | "A low band, just above the mouth. Barely higher than the water at Slack." | **3rd** | Stage 3: nave floor, altar, great window (N3), P10–P13. Channel stays Slack. |

| Rule | Spec |
|---|---|
| Why the order | Each culvert takes the water from a different height. The highest stain marks the culvert that carried the top of the water; open it first and the water falls to the next. Mabyn's teacher put it as "the chapel tells you where the water stood". (Lowmark's outfall boards are read by rope wear; the Mire's are read from the walls, so the puzzle does not repeat; bible §13.) |
| Slack | A windlass turns only when the buttress stake reads ochre. The stake is read through the bell-loft window. Pinned: morning Slack on arrival; Running after Board B until the player keeps watch to dusk; dusk Slack; night Running; morning Slack. |
| Wrong board | Lifts, roars, chokes, drops back. ~5 s. Nothing drains; nothing else resets; boards already opened stay open. |
| Hint ladder | 0 wrong: none. 2 wrong: Mabyn repeats her teacher's words. 3 wrong: she says "Highest stain first." |
| Each stage's fall | ~15 s: a long roar inside the walls; the gallery shakes (camera shake light); the water surface drops in a visible slide; silt and debris swirl; then the environment variant settles and the new ground drips. The player keeps control throughout. |

### B8.3 The glass lit by nothing (Beat 7): *the strange moment*

| Time | Element | Spec |
|---|---|---|
| Trigger | Stage 3's fall completes (Board A). Once per player. | |
| 0–3 s | **The last water** | The final sheet of water slides off the great window's lowest panes. The glass is dark, its leading black, its colours only guessable in the hand lantern's light. |
| 3–8 s | **Lit** | The window lights **from behind**: gold and blue, evenly, as if the sun were on the other side. The nave floor takes the colour. Every Shade at the edge of every dark goes, for those seconds, completely still. The design shows **reeds and water, herons, and a ring of low stones under a pale sky**. No star, no sinking, no figure. |
| 8–10 s | **Only glass** | The light goes out of it, not fading so much as never having been. It is glass with black peat pressed against its outer face. |
| Audio | | No music, no choir, no tone. The drip of the drained nave continues throughout. |
| Mabyn | | At the gallery rail. She makes no sound. When the player next looks up or approaches the stair, she says `MCS-B4.3`: "Seen: it lit. Thought: I don't know. That's all I've got." |
| UI | | No popup. Subtitle: **"[The glass is lit from behind.]"** then **"[It is only glass.]"** |
| After | | `MCS_GLASS_SEEN` (barks only). **Never explained** (bible §7.5). Inspecting the glass afterward: "Glass, with peat pressed up against the outside of it. There is nothing behind it to give light." |
| Art rule | | **No star motif anywhere in the chapel**: not in the glass, carving, ironwork or Tender marks. The formal name stays unexplained (C14). |

### B8.4 The two records: presentation and custody rules (R08)

| Element | Spec |
|---|---|
| **Vestry log** (read in place) | Document view, one opened page spread plus earlier leaves shown as pulp. **No calendar date** (coordinated with Act I). Each readable entry is headed by the day's weather, in the soldiers' habit, and the run matches the `MBR_unit_logs` exactly: **rain, rain, rain, a hard frost, a thaw, fog, fog**; the log stops on the second fog (the day the wardens went out), with a later and a dusk entry on that same fog day. With MR-M2 Completed the inspect adds: "Rain, rain, rain, a hard frost, a thaw, fog, fog. The same weather as the three day-books from the causeway chest, and it stops on the same fog." No unit name, no army, no direction, no number of men or dead anywhere in it. |
| **The leaves** (`MCS_warden_leaves`) | Document view, four leaves, one per page. Clay rendered with pressed letters and marks. **Tally art rule:** leaf 3's row runs off the broken edge (the beginning is never visible; no one can count it); leaf 4's row is smeared and crossed by a crack so the strokes run together (cannot be counted). **Inspect text never gives a figure.** Office marks only: the same simple pressed mark on leaves 1–3, a second mark (a different hand) twice on leaf 4. |
| **Never stated, never computable** | The Memorywardens' names; which armies collided; how many went out, how many came back, how many died on the field (R08, FT-02). No document, inspect, bark or line totals or estimates anyone. The vestry log's "not many" is the only quantity word, and it is not a number. |
| **The General** | Not named in either record. Ysolde's link at the landing is called her reading and "not a hold" (§B6 Beat 11). |
| **Form for MR-M5 (binding for Act III)** | Leaf 2 (**the stone list**): stones named **by place only**, in this order: *the post stone; the low stone by the palisade; the split stone; the stone that faces the field; the stone with the old cut in it*; then the list runs onto a broken corner (whatever followed is lost); below the break, *"and the last stone, which closes it, to be set when the calm is laid"*. No person, office mark or count beside any stone; the list never states how many stones there are. Leaf 3 (**going out**): a row of **tally marks only**, running off a broken edge. Leaf 4 (**come back**): a short row of **tally marks only**, smeared and cracked, then *"The circle is not closed. We could not."* **Never a numeral or a number word on any leaf, and no row can be counted.** MR-M5 may cite the named stones and the unclosed last stone; it may not count marks or stones from the leaves. |
| **Order** | The log is read before the leaves (`S05` requires `S04`), so the player sees the soldiers' side first and the wardens' side second. |
| **Side by side** | At the landing, Ysolde sets the two accounts together in dialogue (recall), not in a document view; the custody outcome decides which object is physically present. |

### B8.5 The draught (Beat 9)

| Time | Element | Spec |
|---|---|---|
| Trigger | The player takes the leaves from the box (`MCS_warden_leaves` acquired). | |
| 0–3 s | **The breath** | A cold pull of air up the crypt steps past the player, toward the nave. The hand lantern's flame streams upward. A long, low sigh in the culverts. |
| 3 s on | **The wave** | Starting at the altar post (P13), each post gutters (~1.5 s tell) and goes dark, one after another up the nave, every ~4 s, in the order P13 → P1, then the gallery post (G6), then the loft posts. The top post (Mabyn's pole lantern at the hatch) never gutters. Each post gutters **once**. |
| Shades | | Form ~3 s after dark; press every ~2 s. |
| Mabyn | | Calls from the hatch at fixed points (`MCS-B6.1`–`.6`): "Keep coming." "Light it and move." "I've got the top. I've got it." |
| End | | The player reaches the hatch; Mabyn pulls them up by the wrist. The draught dies; every post the player relit stays lit; Mabyn relights the rest over the night (presentation, seen from the hatch as a line of lights coming back one by one). |

## B9. Quest structure for implementation

### B9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to Mabyn on the roof. | `MCS-D1` end | Yes | Quest Active at MRC completion. |
| `S01_roofline` | Relight the roof lanterns. | 6 × `light_post` (T1–T2) + MCS-E1 defeated + `MCS-D2` end (hand lantern given) | Yes | Sets `MCS_OUTER_LIT`. |
| `S02_gallery` | Go down into the bell-loft. / Look down into the nave. | 2 × loft `light_post` + enter gallery volume + inspects `MCS-I3.02`, `MCS-I3.03` + `MCS-D3` end | Yes | First Shade press scripted in the loft. |
| `S03_drain` | Read the stake on the buttress. / Read the culvert stains. / Open the sluice boards in order. / Light the aisle walk... / Wait for Slack. / Open the next sluice board. / Light the lower bays. / Open the last sluice board. / Light the nave floor. | Stake inspect + 3 stain inspects + Board B (stage 1) + P1–P4 lit + MCS-E2 defeated + keep watch to dusk + Board C (stage 2) + P5–P9 lit + MCS-E3 defeated + Board A (stage 3) + P10–P13 lit | Yes | `[MD-4]` Wrong boards reset harmlessly (`MCS_WRONG_BOARDS`). Board at Running will not turn. Glass trigger at stage 3. Sets `MCS_STAGE` 1–3, `MCS_GLASS_SEEN`. |
| `S04_vestry` | Search the vestry. | Read-in-place `MCS-I6.02` | Yes | **Opens at stage 2**, in parallel with the rest of `S03`. Sets `MCS_VESTRY_READ`. |
| `S05_crypt` | Look beneath the altar. / Open the box. / Read the leaves. | `S03` + `S04` complete + slab lifted + 3 × `prise_lead` + `MCS_warden_leaves` acquired + leaves document closed | Yes | Sets `MCS_LEAVES_READ`. Triggers the draught. |
| `S06_out` | Carry the leaves up to Mabyn. | Enter hatch volume | Yes | MCS-H2. Each post gutters once. |
| `S07_vigil` | Sit the night with Mabyn. / Decide who keeps the record. | `MCS-D9` choice + outcome interaction (altar: return to crypt, lay leaves, rubbing; tenders: chest; sorrowmere: none) + keep watch to morning | Yes | Sets `MR_WARDEN_RECORD`. `[MD-3]` first light. |
| `S08_landing` | Cross back with Rowan. / Tell Ysolde what you found. | `MCS-D10` + ride complete + `MCS-D11` end | Yes | Sorrowmere: `MCS_warden_leaves` leaves the pack at `MCS-D11.40`. Altar: rubbing handed over. Quest → Completed. MR-M5 offer armed. |

### B9.2 Flags

| Flag | Set by | Read by (here) | Read by (later) |
|---|---|---|---|
| `MCS_OUTER_LIT` | `S01` | Roof line props | Post-quest roof state (lit) |
| `MCS_STAGE` (0–3) | Each correct board | Nave environment variant; posts; encounters; `S04` opening | Post-quest chapel state (drained, lit) |
| `MCS_WRONG_BOARDS` (count) | Wrong-order board | Mabyn hint ladder (`MCS-B3.4`, `.5`) | — |
| `MCS_STAINS_READ` (count 0–3) | Stain inspects | `MCS-D4` options | — |
| `MCS_VESTRY_READ` | `S04` | `S05` gate; `MCS-D6`, `MCS-D9`, `MCS-D11` options | CV-M1 (the vestry log as the Mire's second custodian; read in place) |
| `MCS_TOLD_MABYN_LANTERN` | `MCS-D6.20` or `MCS-D9.20` (telling her the log's last line) | `MCS-D9.21` (seven-night story) | *The Lantern That Would Not Go Out* (MLW; one opening line) |
| `MCS_GLASS_SEEN` | Stage 3 trigger | Barks | — |
| `MCS_LEAVES_READ` | `S05` | `MCS-D9`, `MCS-D11` | — |
| `MCS_MARK_LIKENESS` | Optional `MCS-I7.06` | `MCS-D11.25` (optional line) | — |
| `MR_WARDEN_RECORD` = sorrowmere / altar / tenders | `S07` | `MCS-D9`, `MCS-D10`, `MCS-D11` | MR-M5 roll source line; CV-M1 custody line |

Quest item: `MCS_warden_leaves` (acquired `S05`; leaves the pack at `S07` for altar and tenders, at `S08` for sorrowmere).
Carry-state objects: the Tender's hand lantern (kept as the reward, §B10), the reed-paper rubbing (altar only; handed to Ysolde at `S08`).

### B9.3 Choice: who keeps the record

The player decides; Mabyn agrees in every case. Every outcome keeps the knowledge public. CV-M1 reads the custody line only.

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Sorrowmere** (`MR_WARDEN_RECORD = sorrowmere`): *"Ysolde's people should keep it, and read it out."* | The leaves leave the chapel in the player's pack and are given to Ysolde at the landing. She will read them on the raised way where anyone can hear, and she starts a new page in the Names Below register **for people held without names** (`MCS-D11.40`). | The chapel loses the thing it kept without knowing. Mabyn: "Bring them back to be read here sometimes. They were under our roof a long while." The leaves are in a busy room now, handled. | **MR-M5:** Ysolde's names roll carries a line read from the leaves (bible §9.1). **CV-M1:** the record is in Sorrowmere's register room. Post-story: a Memorykeeper reading from them on the raised way (bark). |
| **Altar** (`= altar`): *"Put it back where they left it."* | The player and Mabyn go down the lit line to the crypt. The player lays the leaves in the box; Mabyn says a river hymn; the player takes a **reed-paper rubbing** of the last leaf; they close the slab. At the landing, Ysolde takes the rubbing and makes a reed copy of the last leaf for the register (`MCS-D11.42`). | Only the last leaf travels. The rest is under the altar, reached by Rowan's route at Slack and Mabyn's line. Ysolde: "Then I'll go out and read the rest myself. With Rowan. At Slack." | **MR-M5:** the roll's source line names the reed copy and the altar. **CV-M1:** the record is beneath the altar; Mabyn keeps the way lit. Post-story: the crypt can be visited; the box is there; the leaves can be read in place. |
| **Tenders** (`= tenders`): *"The Tenders kept the light for them. Let the Tenders keep this."* | The leaves go into the Tenders' chest in Mabyn's roof loft, pegged. Mabyn will read them to anyone Rowan brings (`MCS-D9.71`). At the landing, Ysolde writes where the record is held (`MCS-D11.44`): "That's a hold too. A keeper and a place." | The record is only as reachable as Rowan's route. Mabyn is alone on the roof and says so. | **MR-M5:** the roll's source line names the Tenders' loft. **CV-M1:** the record is in the Tenders' keeping on the chapel roof. Post-story: Mabyn reads a leaf aloud on request at her loft. |

**All** outcomes: the vestry log stays on its hook, readable; the player has read both custodians; the chapel stays drained and lit for the player (post-quest state); Ysolde has heard the account and made her reading. Nobody is told the Memorywardens' names, the armies or the dead; none of the records contains them. None of the options is wrong.

## B10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| **The chapel, lit** | World change | The roof line and inner line stay lit; the nave stays at stage 3 (drained) for this player. The chapel can be walked by the Chapel route at Slack. Shades still form in any dark corner (the vestry, the crypt steps) but every main path is lit. |
| **A Tender's hand lantern** | Tool (functional name; item pass to define) | Mabyn's spare. A carried light for dark interiors and night walks; no stats proposed. If cut, the line stays and the player uses the lantern only inside the chapel. |
| **The account** | Knowledge | R08 learned; the open circle on Bannerline is the lead into MR-M5. |
| Small payment | Currency | Ysolde's Memorykeepers' errand due for MR-M3 and MR-M4 together, paid at the register room on next visit (economy tuning). |
| Skill XP | Action only | Melee and Ranged by use; Hunting harvest from Silt Crawlers per the economy pass. No lump quest XP. |
| Side-quest unlocks | Story | *The Lantern That Would Not Go Out* (MLW) if *The Broken Lantern Light* is complete; MLW opens with Mabyn's wax-book line and reads `MCS_TOLD_MABYN_LANTERN` for one extra line. |
| MR-M5 | Story | Automatic on next entry to Sorrowmere or Griefwatch (bible §6.1). |

## B11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Wrong-order board | Harmless reset (§B8.2). Hint ladder guarantees the path. |
| Board at Running | Will not turn. Keep watch. |
| Pushed back by the Shades | Time cost; no damage. The push never sends the player further back than the nearest lit post. |
| The draught | Each post gutters once; posts relit by the player stay lit; the top post never gutters. Always completable. |
| Out of moss wicks | Not possible in practice: the bundle is generous; Mabyn's loft jars refill it (interaction at T3: "Take what you need."). |
| Death | Respawn points per §B7. All stages, boards, posts, the vestry read and the leaves persist. |
| Player wants to leave mid-quest | Ask Mabyn to hang the second lantern on the hatch hook (`MCS-D1.80`): Rowan comes at the next morning Slack `[MD-3]`. Leaving the chapel does not reset anything; the water stays at its stage for this player. Return by the Chapel route at Slack. |
| Logout | Restore to the persisted step at the nearest respawn point. If logged out during `S06`, the draught has ended on return; any guttered post the player had not relit is relit by Mabyn ("I did the rest."). |
| Walking away | Stays Active. Resume hooks: Mabyn on the roof (`MCS-D1.90`) for `S00`–`S02`; Mabyn at the gallery post (`MCS-D5.90`) for `S03`–`S06`; Mabyn on the roof (`MCS-D9.90`) for `S07`; Ysolde at the landing for `S08`, and after one presentation-hour turn at the register table (`MCS-D11.90`). |
| Fail state | None. |
| Co-op | §B7. Custody prop: where per-player props are unavailable, a shared prop may be shown as a presentation fallback only (MI-CO-06, CDR-6); it never decides a partner's choice, and each partner's flag is their own. |

## B12. Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| **Staged water level** (N-3) | Systems + Art | Three discrete nave environment variants (stage 1, 2, 3) plus the flooded start, swapped by quest step (`MCS_STAGE`), per player. Co-op presentation is unresolved (MI-CO-06, CDR-6; Integration Q-18); a partner's walkable ground follows their own stage. This is already the fallback form; nothing more is needed. A ~15 s transition presentation (water slide, debris, shake) is VFX over the swap. |
| **Light-gated hazard volumes** (N-2) | Systems | Spawn gating by a lantern post's lit state (radius ~6 m). Hazard volume in dark ground applies the press timer to the carried hand lantern and, at ember, a scripted push to the nearest lit post reachable on the walkable route (never across a level change). **Fallback:** pre-authored lit/dark zones flipped at each stage, as §B8.1. **Fallback for Sol (push target):** the push may target the last lit post on the player's own level, or the stair head above it. |
| **Hand lantern looks** | Systems + Art | A carry-state prop whose light radius shows the dark-ground timer (three looks) with a log line on change; the timer resets in a lit radius. Part of N-2; no stored light value, no new UI. |
| **Lantern post states** | Systems + Art | Dark / lit / guttering, with light and relight interactions; persisted per player. |
| **Channel-state pin for the buttress stake** (N-1 fallback) | Systems | Quest-pinned stake state per presentation hour (§B8.2). |
| **Windlass interaction with order check** | Systems | Channelled interaction on three windlasses; a sequence check (B → C → A); wrong order plays an authored reset; Running blocks the interaction. Standard interact sequence with harmless reset (bible §11.1). |
| **The draught wave** | Systems | A scripted sequence that sets each post to guttering → dark in order on a timer, once each; does not touch posts already relit by the player afterward; top post exempt. |
| **The glass** | VFX + Art | An emissive state on the great window's glass for ~5 s, then off; the Shade volumes freeze for that time (presentation only). |
| **Multi-leaf document view** | UI | A document with four pages; the log as a page spread. Standard document view. |
| **Custody props** | Art + Systems | Box under altar with/without leaves; Tenders' chest pegged/unpegged; per player; presentation fallback only per MI-CO-06 (CDR-6); each partner's `MR_WARDEN_RECORD` drives their own lines. |
| **Mabyn across levels** | Systems | Beat 2 (ladder down to G6) and Beat 10 altar outcome (back down to the crypt with the player) move Mabyn across levels. **Fallback for Sol (if NPC ladder and stair traversal is not available):** placement sets (MI-PP-04) put her at G6; in the altar outcome she waits at the gallery post (G6), as in `S02`, while the player goes down to the crypt; the choice, the rubbing and `MR_WARDEN_RECORD` are unchanged. Primary design unchanged. |
| Creatures | Schema / Gameplay | Reedlurker (lurker, snapper); Silt Crawler with burst-from-silt spawn and front-shell damage reduction (optional; fallback more health, Enemies file R-9). |
| Quest item `MCS_warden_leaves` | Schema | Non-droppable four-page document; leaves the pack by outcome; location-bound readable copy at the register room, the crypt box or the Tenders' chest. |
| **Act I read-conditions** | Act I author / Schema | MR-M2 Completed; the day-books' weather run (rain, rain, rain, hard frost, thaw, fog, fog; vestry log matches it exactly); the shard's "faint marks" (for the optional likeness line). |

## B13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **What stopped the Mire's front** (R08) | The last Memorywardens laid a calm-field over the battlefield at the turning of the light; the armies could not keep fighting; the overload killed most of them and concentrated the General (FT-02c). | The Memorywardens cursed the land; the land swallowed the armies; the General is a commander who would not die. | The vestry log (they went out; the field went quiet; the men sat down; not many came back); the leaves (the plan; the stones; the rows; "the circle is not closed"); the day-books' matching weather run. | The wardens killed the soldiers; the chapel is a place of power; the glass is a sign. | The wardens' names; which armies; how many died. | **MR-M4 (owned).** |
| **The General's origin** | Concentrated by the same grounding. | A real commander on the ridge. | Ysolde's link (the open circle, Griefwatch's talk), called her reading. | The wardens made a monster on purpose. | — | MR-M5 (consequence). |
| **The empty bell frame** | Unexplained. | The bell is still ringing somewhere. | The frame, the rope groove, the soundless bell from MRC. | The bell was taken by the wardens; the bell is the "star". | Where the bell went. | **Never explained.** |
| **The glass lit by nothing** | Unexplained. | Tenders' stories of the chapel glowing. | The moment; peat behind the glass. | A sign from the dead. | Everything. | **Never explained** (bible §7.5). |
| **The seven-night lantern** | Tenders kept a roof lantern lit seven nights for people who did not come back. Craft. | A miracle; a Memorywarden's final act. | The log's last line; Mabyn's story. | It was magic. | — | MLW (side). |
| **"Sinking Star"** | Unknown. | Guesses. | The name, used by Ysolde and in the log as "the chapel". No star motif anywhere. | Any. | The origin. | **Never explained** (C14). |
| **The circle not closed** | The rite that should have closed the Bannerline circle was never finished. | An old mourning ring "never done properly" (Griefwatch). | Leaf 4; the stone list. | The circle holds the General in. | — | MR-M5. |

## B14. Open decisions

1. **MD-4 (staged drainage)** is built on as recommended. If the Director restores breath management, every `[MD-4]` node changes: §B5.3, Beats 3–7, §B8.1–B8.2, §B12 (N-2, N-3), and the stage-based encounters. The vestry, crypt, leaves, log and choice survive unchanged.
2. **MD-3** governs the departure and return only (`S07` end, `S08`).
3. **Vestry log matching (resolved with the Act I designer, 2026-11-08).** The day-books carry no calendar date; the vestry log matches them by the same weather run (rain, rain, rain, a hard frost, a thaw, fog, fog) and stops on the second fog. No calendar date or year number is used anywhere (FT-02 withholds year numbers).
4. **The leaves' last leaf being added after the battle.** The bible says the leaves were sealed under the altar before the wardens went out, and that the last leaf, in a different hand, records those who came back. This package reconciles the two: the box was sealed before they went out; the survivors came back at dusk, went down under the big window, added the unfired last leaf and shut the stair (witnessed in the vestry log's dusk entry). If the Director prefers another reconciliation, only the log's dusk entry and leaf 4's description change.
5. **Ysolde at the landing.** She comes down to meet the boat because Rowan told the ferry households when he would be back. If the Director prefers the completion at the register room, move `MCS-D11` and keep "complete at Blackwater Landing" as the ride's end; the bible says complete at the landing.
6. **The rubbing** (altar outcome) is a carry-state object, not a quest item (budget 4). Ysolde makes the reed copy from it, as the bible asks.
7. **Shades without damage.** Bible §10 says Shades have no HP and press the player toward light. This package gives them no damage at all, so the chapel's cost is time. If the Gameplay Designer wants more threat, a small damage-over-time in dark ground is the smallest change.
8. **Rewards:** "a Tender's hand lantern" needs the item pass.
9. **Map:** the chapel's setting and the interior geometry need the zone package (MAP VERIFICATION REQUIRED).

## B15. Internal review log

| Finding | Revision |
|---|---|
| The leaves' tally rows risked letting a player count deaths (bible §13 high finding). | Leaf 3's row runs off a broken edge; leaf 4's row is smeared and cracked; art rule forbids countable strokes; inspect text never gives a figure; "not many" in the log is the only quantity word. Nothing is stated or computable. |
| The log risked naming a unit or army. | The case's mark has rotted; the officer writes "the column", "the other lot behind them", "the chapel's people". No names, no direction, no strength. |
| The stone list risked giving a headcount of wardens (one stone per person). | Stones are listed by place, with no mark or name beside them, and the list runs onto a broken edge. The circle's stone count belongs to MR-M5 and is not linked to people. |
| The leaves risked naming the General or explaining the grounding as a system. | They give a plan in the wardens' own plain words and "the circle is not closed. We could not." The General is not named; Ysolde's link is "my reading, not a hold". Nobody describes how a calm-field works. |
| The glass risked hinting at "Sinking Star". | Its design is reeds, water, herons and a ring of low stones; no star motif anywhere in the chapel (art rule). |
| Shades risked reading as ghosts. | No faces, no outlines, no voices; Mabyn's words: "only dark that's heavy"; never targetable; no NPC calls them souls. |
| The drainage risked repeating Lowmark's outfall puzzle. | Read from water stains on the chapel's own stonework through its windows, with a Slack check through another window; the dusk wait makes the order matter in time as well as sequence. |
| The draught risked a frustration loop. | Each post gutters once; relit posts stay lit; the push never sends the player further back than the last post they relit; the top post never gutters. |
| Mabyn risked knowing too much. | She does not know what is under the altar; she knows the drains existed, two of her teacher's rules, and the Tenders' lantern craft. She hears the log from the player. |
| R08 custody (ledger "altar record plus one regimental log"). | Both required (`S04` gates `S05`); the log is read in place, the leaves carried; the day-books add weight and are not required. |
| Combat as evidence. | No fight near either record; the vestry and crypt have no encounter. |
| Hollowfoot. | None in Act II (MD-7 swap: nothing to swap). |
| Length. | Roof, gallery, three stages with a dusk wait, vestry, crypt, the way out, a vigil and a ride: within 55–70 minutes. |

---

## Act II cross-check (final review)

| Rule | Check |
|---|---|
| Canon anchors | **Rowan:** refuses night crossings (`[MD-3]` grey); explains only when pressed gently and repeatedly (three separate asks); the only living guide; his teacher never returned (unnamed, no war relation); passage after restraint (preparation and waiting); treats the church as a place of mourning ("Not my place. It's hers."); passage proves nothing about the chapel. **Sennic:** three stories (bells without sound, listening mages, slow sinking), each a *where*; never explains; framed by Ysolde as his story. **Chapel-Tenders (Mabyn):** religious, not magical; lantern craft; no miracle claimed; does not know what is under the altar. **Ysolde:** two holds; calls her General link "my reading". |
| Evidence rule | R08 rests on the leaves and the vestry log, both required, both objects. Sennic's stories, the bell, the glass, the Shades and the Echoes prove nothing. No defeated enemy speaks. |
| Withheld | The Memorywardens' names; which armies collided; how many died (no figure stated or computable: tally art rule, broken and smeared rows, "not many" only); the origin of "Sinking Star" (no star motif; Rowan and Mabyn decline to explain the name). |
| Three states | No fail or abandon logic. Wrong calls, cold resin, wrong boards, Running boards, Shade pushes and the draught cost time only. Every wait is one keep-watch. |
| Guaranteed paths | All R08 custodians are on required steps. Mabyn's hint ladder guarantees the board order. The cut always ends by passage. The draught always ends. |
| No cutscenes | Every presentation spec keeps the camera with the player and keeps control (the push and the haul are the only brief control losses, ~2 s). |
| Solo / co-op | Solo-clearable; per-player grey, hour gates, water stage (co-op presentation unresolved; MI-CO-06, CDR-6), asks and choices. |
| Movement reality | Click-to-move; the gallery gap is the only agility trigger and has a walkable fallback; no swimming; deep water non-walkable. |
| Quest items | 1 in Act II (`MCS_warden_leaves`); Mire running total 3 of 4 with Act I. |
| Region flags | Read: `MR_CHANNELS`, `MR_NAME_RECORD`, `MR_BANNERS`, `MR_CAUSEWAY`, `MR_LANTERN_LINE`. Set: `MR_ROWAN_TRUST`, `MR_WARDEN_RECORD`. No new `MR_` flag. |
| Causeway tagging | One ferry-household bark names the causeway decision and is tagged `[CAUSEWAY]` in the dialogue file. No other Act II node depends on MD-1. |
| Map | Relative placement only; MAP VERIFICATION REQUIRED in §A5, §B5. No route or direction to another region; trade leather has no named origin. Mirebone Crossing does not appear. |
| Magic stays dormant | Nobody practises or recognises magic. Sennic says "mages" as his childhood story; Ysolde calls the Memorywardens "the old order. History." Mabyn: "Not a miracle. People not sleeping." |
| Cross-region independence | No Lowmark or Thornfell state is read or required. |
| Release wording | None. "Mire milestone" only. |
| Independent review (2026-11-08, Acts I–II reviewer) | 8 defects fixed in place, none high. **Medium (CDR-4):** the boat fight's bespoke Echo "grip" state, and its contradictory claim that "a player who does nothing still finishes", replaced by the ordinary escort halt-on-enemy-proximity rule the Act I cart already uses (Beat 5, MRC-E2, rules, §A12, §A15, `MRC-B5.6`); the hand lantern's three states restated as presentation of one dark-ground timer with no stored light value or refill logic (§B8.1, §B12). **Low:** §B9.3 cited non-existent `MCS-D9.42` (now `MCS-D9.71`); Beat 6 said "neither column", implying two forces where the log says "the other lot, and the lot behind them" (reworded); duplicate conditional ids made unique (`MRC-D9.11b`, `MRC-B5.3b`, `MCS-D10.04b`/`.04c`); Rowan's "I was younger than you" presumed the player's age (origin-neutral rule; now "I was young"); beat headings used em-dashes (now colons, matching Act I). **Verified unchanged:** every other cited id exists; flags and step predicates match; R08 custody (leaf 3 runs off a broken edge, leaf 4 smeared, "not many"/"fewer" only; no names, armies or numerals; Rowan and the glass leave "Sinking Star" unexplained, no star motif); Rowan (night refusal, gentle repeated asks, only guide, unnamed teacher), Sennic (where, never why); MD-3/MD-4 tags and swap notes; the weather run matches Act I's three day-books exactly; MAP VERIFICATION REQUIRED on every place section; tables well-formed. |
| Batch 4 encounter alignment review, 2026-11-09 | Aligned with `Enemies/Caelmor_Mire_Encounter_and_Enemy_Requirements.md` §13.3 (numbers and text only; no id, step or flag renamed): MRC-E2 Echo swing has no knockback (C-1, I-6); MCS-E2 front shell and the §B12 creature row marked optional with the more-health fallback (R-9, I-14). |
| Playability audit fixes, 2026-11-13 | SM-05 (content fallbacks for Sol: push target on the player's own level or the stair head above; Mabyn waits at G6 in the altar outcome; primary design unchanged), SM-06 (harness-haul fallback at a fixed bank pad), SM-12, SM-18, SM-21, CO-03, CO-05, CO-06, TD-05. Authored walkthrough only (no Unity build exists; nothing was played). Text only; no id, step, flag or geography changed. MI-CO-06 host presentation is stated as a provisional fallback pending Director review that never decides a partner's navigation, step or credit. |
| Playability audit fixes review, 2026-11-13 | Independent review of the same-day fixes. §A11 co-op row: "host fallback" for the grey restated as provisional (MI-CO-06); shared mending credit marked as an open Director item (Integration MI-CO-03). Authored walkthrough only; text only; no id, step, flag or geography changed; no Director recommendation promoted. |
| CDR-6 solo-completion sweep, 2026-11-14 | §A7 co-op: junction calls count only for the caller's own `MRC_WRONG_CALLS`; the extra ferry punt is optional co-op presentation. §A11 co-op: mending and gathering credit only a partner whose own `S02` consumes it, as that task's crew path; the "mended it yourself" pole and lines only for the player who mended. MI-CO-06 references restated as presentation fallback only under CDR-6. Text only; no id, step, flag, line or geography changed; Sol's co-op conflicts kept as presentation questions. |
