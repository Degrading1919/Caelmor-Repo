# Mire Side Quests — Cloth and Colour; Memory in the Ground

**Status (2026-11-08):** Authored production content for Creative Director review (Mire bible §12, Batch 3, part A). Five side-quest packages: the interconnected questline ***Cloth and Colour*** (**MBS** *A Banner With No Side*, **MCF** *Cloth for Sale*; bible §7.1) and three standalone quests on memory in the ground and water (**MFW** *The Father at the Ford*, **MMR** *The Mud That Remembers*, **MSG** *The Singing Trench*; bible §7.2). Everything marked **[NEW]** is authored here and is not canon until the Director promotes it. **[CANON]** items come from the reconciled `LORE/` files. **[PROPOSAL — DIRECTOR]** marks a consequential choice. No schema, JSON or C# is created here. The Mire is an internal production milestone of the complete game (CDR-3). Combat follows `Caelmor_Director_Rulings_Combat_Ranged_Release.md`: every enemy is defeated at 0 HP (CDR-1); no scripted exception; melee or ranged in every fight, ranged never required (CDR-2); standard systems (CDR-4).

**Controlled by:** `Caelmor_Mire_Narrative_Production_Bible.md` (§2 author truth, §5 cast and voice, §7.1–§7.3 slate and contracts, §9 flags, §10 encounter families, §11 conventions). **Format:** mirrors `Caelmor_Thornfell_Side_Quests_Horn_and_Highsteads.md`; dialogue inline per package (§x.12) with node ids `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>`, inspects `<CODE>-I<n>.<nn>`, encounters `<CODE>-E<n>`. Companion file: `Caelmor_Mire_Side_Quests_Names_and_Lanterns.md` (its §0.6 shared rules apply here unchanged and are summarised in §0.6 below).

**Main-quest inputs read (checked on 2026-11-08):** Act III's input table reads **`MR_CLOTH`** (returned / burned / unset) from MCF at circle placement: with `returned`, Calwen lays the recovered cloth at the foot of his stone (`MBL-B7.2a`). MCF sets it exactly so.

---

## 0. Slate header

### 0.1 The five quests at a glance

| Code | Quest | Series / type | Unlock | Where | Core verb | Gameplay identity | Strange / wonder moment | Sets |
|---|---|---|---|---|---|---|---|---|
| **MBS** | A Banner With No Side | Cloth and Colour (1/2); Memory/lore | MR-M2 Completed | Calwen's Reed Sanctuary; Griefwatch | **inspect**, ask, retire | **Read a cloth by its stitches**, gather testimony from three keepers, re-stitch rotten hoist tabs, then retire or keep it in front of two visitors who each wanted it as proof | In the washing frame, two dyes bleed from the cloth and meet in the water as one colour | `MBS_FATE` (retired / kept) |
| **MCF** | Cloth for Sale | Cloth and Colour (2/2); Combat challenge | MBS Completed | Marshfall jetty; the Reed Hide | **track**, assault, recover | **Follow a trail of cut reed and fibre**, read a go-between's ledger, assault a drowned-trench camp by day, carry the cloth home or burn it | Around the stripped cloth stack the reeds lie flat in a ring, as if something heavy had sat there | **`MR_CLOTH`** (returned / burned) |
| **MFW** | The Father at the Ford | Standalone; Memory/lore | MR-M3 Completed | The Wading Ford; Blackwater Landing | **watch**, read, ask | **Keep a dusk hide at a ford**, hear the names a figure calls, find them in an old ferry list and a family's naming board | The figure turns toward the player's hide, opens its mouth, and the name it calls is the player's own word for "here" | `MFW_TOLD` (told / kept) |
| **MMR** | The Mud That Remembers | Standalone; Environmental | MR-M2 Completed | The Drowned Encampment (landward side) | **observe**, track, correct | **Read prints that loop**, follow fleeing does as a warning, clear Echoes woken by a scholar's survey, find the camp's ration board | After the strings come up, the prints fill with water one after another, in walking order, round the loop once more | `MMR_MAP` (corrected / annotated) |
| **MSG** | The Singing Trench | Standalone; Environmental | MR-M1 Completed | The Singing Trench (Field edge) | **listen**, dig, prop | **Tune a trench in a storm**: open and close three vents, listening bay by bay, to draw water off a failing revetment, then prop it | After the storm drops, the trench keeps humming for a few seconds into still air | none (quest-local `MSG_LISTENED`) |

**Length targets:** MBS 30–40 min; MCF 35–45; MFW 25–35; MMR 30–40; MSG 25–35.

**Combat share:** MBS 0%; **MCF ~55% (combat core)**; MFW 0%; MMR ~25%; MSG ~15%.

### 0.2 Spines

**Cloth and Colour: a banner nobody owns, and cloth somebody is selling.** Calwen refuses to name a banner's side; Rootshadow cutters will sell any cloth to anyone. MBS shows why a banner cannot be proof; MCF shows what happens when it becomes goods.

| Part | What the cloth is to people | What the player does with it | What stays unknown |
|---|---|---|---|
| MBS | Proof (to two visitors, each for their own side). | Reads it, mends it, and lets Calwen decide with the player's word whether it is retired or kept unsorted. | Whose it was. A mixed treatment crew is suggested by a stitch, never confirmed. |
| MCF | "Commemorative goods" at a jetty stall. | Tracks it to its source, takes it back by force from the cutters, and returns it to Calwen or burns it so it cannot be sold. | The buyers. Gethin's ledger has marks, not names, and no route. |

**Memory in the ground and water (standalones).** Three places where the Mire seems to remember. Each is solved by a living record or a practical fix, never by the phenomenon: a ferry list and a naming board (MFW), a ration board (MMR), airflow and timber (MSG).

### 0.3 Unlock graph

```
MR-M1 ──► MSG The Singing Trench
MR-M2 ──► MBS A Banner With No Side ──► MCF Cloth for Sale ──► MR_CLOTH ──► MR-M5 circle (Calwen, stone S4)
      └─► MMR The Mud That Remembers
MR-M3 ──► MFW The Father at the Ford
```

No quest here gates a milestone or another region.

### 0.4 Flags set and read

**Region flag set** (bible §9.1):

| Flag | Values | Set by | Read by | Effect |
|---|---|---|---|---|
| `MR_CLOTH` | returned / burned (unset if MCF not done) | MCF `S07_cloth` | **MR-M5 circle placement**: `returned`, Calwen lays the recovered cloth folded at the foot of stone S4 (`MBL-B7.2a`: "Came home off a jetty. Lie down."); `burned` or unset, no line | Act III input table implemented exactly. |

**Quest-local flags other packages may read:**

| Flag | Values | Set by | Read by |
|---|---|---|---|
| `MBS_FATE` | retired / kept | MBS | MCF opener (Calwen); Griefwatch bark (Eskil) |
| `MCF_LEDGER_READ` | bool | MCF | Marshfall barks |
| `MFW_TOLD` | told / kept | MFW | Landing barks |
| `MMR_MAP` | corrected / annotated | MMR | Sorrowmere register room prop (Lenna's map) |
| `MSG_LISTENED` | bool | MSG | Ysolde / Prue barks |

**Read here:** `MR_CHANNELS`, `MR_BANNERS`, `MR_CAUSEWAY`, `MR_ROWAN_TRUST`, `MBR_CORRA_CORNER` (one MBS line), `TH_STANDING` (one Eskil line in MBS), MR-M5 Completed (post-story variants).

### 0.5 How these feed MR-M5

Only MCF feeds a main quest: `MR_CLOTH = returned` puts the recovered cloth at Calwen's stone in the Bannerline circle; `burned` gives no line (Calwen still stands at S4; he is an always-stone). Nothing else here is read by a milestone.

### 0.6 Shared rules (as the companion file §0.6)

- **Quest items: none.** Carry-state objects (cloth bundles, a folded banner, props of timber, a hide kit) and read-in-place records (Gethin's ledger, the ferry list, the Lusk naming board, the ration board).
- **Dating:** no calendar dates; weather runs or events only.
- **R08 custody:** no names of Memorywardens, armies, units or sides; no figure of dead. Calwen never names a side; stitch styles are leads, never proof.
- **Evidence rule:** the figure at the ford, the prints, the hum and the bleeding dye prove nothing and identify nobody. **Combat never reveals evidence; no defeated enemy speaks.**
- **Three states only;** no fail; every skill step has a crew alternative; every wait is a keep-watch; missed dusks re-offer.
- **Defeat (CDR-1):** every enemy to 0 HP. Earthen Echoes re-form only while their condition lasts. Rootshadow cutters are human and use the ordinary defeat presentation; Gethin Scarth never fights and is never targetable.
- **MD-7:** no Hollowfoot appear in any of these five quests. Each package carries the swap note.
- **MD-3:** Rowan does not cross at night; MFW's dusk watch is reached on foot.
- **Co-op:** Lowmark per-player prop pattern. Where a row here says "fallback: host", that is a provisional presentation fallback only (Integration MI-CO-06, pending Director review): it never decides another player's walkable ground, interactions, credit or completion, which follow each player's own quest state (conflicts: Integration §5.2 Q-18).
- **Skills (MD-11):** Leatherworking (MBS), Hunting (MCF, MFW, MMR), Woodcutting (MSG), Melee and Ranged (MCF, MMR, MSG). Levels are `[GD]` placeholders.
- **Map:** relative placement only; **MAP VERIFICATION REQUIRED** wherever it matters. "The high passes" and "the lowlands" are people's words for where someone or something came from; no route, distance or direction is stated.

### 0.7 Distinctness check

| Quest | What the player physically does | Not the same as |
|---|---|---|
| MBS | Inspects stitches with a lens, re-stitches hoist tabs, washes and folds or stores a single cloth before an audience | MR-M2 (three standards under attack; here one cloth, no enemy, two claimants) |
| MCF | Tracks, reads a ledger, assaults a camp in three stages, carries bundles under no pressure, burns or returns | MNK (raiders at a crossing; stakes); MR-M2 (Wraiths, standards) |
| MFW | Sets a hide at dusk, listens, reads a list and a board | MLL (night work at water with a family; here stillness, alone) |
| MMR | Tracks prints into loops, pulls survey stakes under Echo pressure, reads a ration board | MR-M3 (Echoes from a boat) |
| MSG | Opens and closes vents by ear, holds them under Reedlurker pressure, then props timber | MR-M4 (sluice order read from stains; here a combination read by sound) |

### 0.8 Ids and names used

Content ids (suggested): `mire.side.a_banner_with_no_side`, `mire.side.cloth_for_sale`, `mire.side.the_father_at_the_ford`, `mire.side.the_mud_that_remembers`, `mire.side.the_singing_trench`.

New minor names [NEW] (checked for collisions on 2026-11-08): **Eskil Stenning** (Thornfell Ridge Warden visiting Griefwatch, MBS); **Tess Albery** (a visitor "from the lowlands", MBS); **Abner Lusk** (named only; a war-years ferryman, MFW); **Morwen Lusk** and **Nye Lusk** (his children, born in the war's last years, MFW); **Granny Lusk** (his widow, role name, MFW); **Lenna Coote** (visiting Memorykeeper scholar from Griefwatch, MMR); **Ned Siskin** (reed cutter, MSG). Bible cast: Calwen Reed-Binder, Mara Fenholt, Corra Sallis, Ide Larrow, Gethin Scarth, Hob Merrit, Rowan Mirewake, Ysolde Haverel; Prue Calloway from the companion file.

---

# Cloth and Colour

---

## MBS — A Banner With No Side

### MBS.1 The quest in one paragraph

Among the standards that came off the causeway, **Calwen Reed-Binder** has one he cannot place and will not guess at. Its ground-cloth is stitched in a **high-pass manner**: tight double running stitch, cord-wrapped at the hoist. Its tears are mended in a **lowland manner**: long reed-thread darns, laid flat. Two visitors have heard of it. **Eskil Stenning**, a Thornfell Ridge Warden visiting Griefwatch, wants it as proof that highland companies held the field. **Tess Albery**, a visitor from the lowlands asking after her grandmother's company, wants it as proof of the opposite: the lowland mend means it was theirs. Calwen wants testimony, not a story. The player reads the cloth with Calwen's lens (three stitch inspects), asks **Mara** where it lay, reads **Calwen's store book** for the day it came in, and asks **Corra** what the Bannerbearers say. Each answer is honest and none settles anything. One mend, though, is neither manner: a field-dressing stitch, the kind used on wounds, in linen thread. Mara has seen it on the dead from both sides. Somebody mended this banner the way a treatment crew mended people. Calwen will not say more than that. Before it can be either hung or folded, its rotten **leather hoist tabs** must be re-stitched (Leatherworking). Then Calwen asks the player's word: retire it, or keep it unsorted with a note that says "two hands, one mend". In the washing frame, as the mud comes out, two dyes bleed from the cloth into the water and meet as one colour.

**Remember:** two colours running together in a wash. **Want next:** the cloth Calwen hears is being sold at the Marshfall jetty (MCF).

### MBS.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. Stitches prove one side.** | Rejected. Calwen's limit: a banner needs a second channel before naming anyone; no region is proven (bible §7.1). |
| **B. A treatment crew is confirmed.** | Rejected. "Mixed treatment crew suggested, never confirmed" (bible §7.1). |
| **C. Lens → three testimonies → the field-dressing stitch → re-stitch the tabs → retire or keep before both visitors** (selected). | **Selected.** Inspect, ask, retire; a Leatherworking hook; a calm resolution with two disappointed people and an honest record. |

| Element | Source | Status |
|---|---|---|
| Calwen refuses to identify banners by faction; needs a second channel | Mire anchors; Part 4 ledger | [CANON] |
| Thornfell Ridge Wardens sometimes visit Griefwatch | Dossier §VII.3 | [CANON] |
| Retirement pool; unsorted chest; fold by seams | Act I §B5.1 | [NEW] |
| Stitch styles as leads only; mixed treatment crew suggested | Bible §7.1 | [NEW] |
| Eskil, Tess, the store book, the field-dressing stitch | This package | [NEW] |

### MBS.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.a_banner_with_no_side` |
| Series | *Cloth and Colour*, part 1 of 2 |
| Type | Memory/lore |
| Unlock | MR-M2 Completed. Calwen at the sanctuary (`MBS-D1`); or Eskil's bark at Griefwatch (`MBS-B2.01`) sends the player to Calwen. |
| Length | 30–40 minutes |
| Combat share | 0% |
| Skills | **Leatherworking ~[GD: low–mid]**: re-stitch two rotten leather hoist tabs (imported leather, repair only, MD-11). Crew alternative: Calwen does it over a night ("my hands are slow, not bad"). |
| Choice | Retire or keep (`MBS_FATE`: retired / kept). |
| Outputs | `MBS_FATE`; MCF unlock |
| **Anchor** | Banner tenders (Calwen; Mara as finder; Corra for Bannerbearer lore). |
| **World-truth row** | H23 (recovery: things nobody can own). |
| **Revelation role** | Self-contained (thematic link to other regions through stitch styles only). |
| **Recurring evidence** | The banner (Calwen's store) needs a second channel; none is supplied, so no identity. Calwen's store book is read in place. |
| **State compliance** | Inactive → Active on `MBS-D1` accept; Completed on `MBS-D6` end. No fail. Retire / keep quest-local. Resume hook: Calwen (`MBS-B1.02`). |
| **Combat compliance** | None. |

### MBS.4 The places

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Calwen's sanctuary** (MP14) | Hook; lens; tabs; choice | Washing frames, fold table, retirement pool with its rows, the unsorted chest. The banner on the fold table under a reed weight: grey-brown, mud in the weave, two hoist tabs of leather gone to felt. A brass lens on a cord. |
| **A2. The store book** | Testimony (record) | A ledger on Calwen's shelf: what came in, from where on the causeway, in what state. Never whose. |
| **B. Griefwatch vigil hall** (MP03) | Eskil | Eskil Stenning at the long table with a Griefwatch Marshwarden. With `MR_BANNERS = restored`, the Banner That Sank Twice over the door; Eskil keeps looking at it. While MR-M5 is Active for a player, this vigil-hall scene and Eskil's bark are held until MR-M5 `S03` is complete, then resume (no new placements). |
| **C. Causeway, standard 2's site** (MP08) | Mara | The pale hole where this standard stood (Act I's middle standard). |

### MBS.5 Player-facing sequence

**Beat 0 — Two letters (`S00_offer`).** *Objective: Ask Calwen about the banner on his table.* `MBS-D1`. Calwen has two messages asking for the same banner, one from Griefwatch, one from a lowland visitor staying at Sorrowmere.

**Beat 1 — The lens (`S01_lens`).** *Objective: Read the stitches.* Three required inspects with the lens (an inspect variant): **ground seams** (high-pass manner, `MBS-I1.01`), **darns** (lowland manner, `MBS-I1.02`), and a **small mend at the lower corner** (linen thread, a field-dressing stitch, `MBS-I1.03`). Calwen names the first two by manner only: "I don't say whose. I say how."

**Beat 2 — Three keepers (`S02_ask`, any order).** *Objective: Ask who can say anything about it.*
- **Mara** at the causeway site (`MBS-D2`): where it lay, how deep (shallow, face down), nothing with it. On the lower-corner mend: "That's how they stitched people. I've seen it on bones. Both kinds of bones."
- **Calwen's store book** (`MBS-I2.01`): the day it came in (the morning after the Risen Colour), the site, "cloth sound, tabs rotten, two hands of mending". Never whose.
- **Corra** (`MBS-D3`): Bannerbearers say a banner mended by the other side "belongs to both"; she adds it's a saying, not a rule. With `MBR_CORRA_CORNER`, she offers to take a corner again.

**Beat 3 — The visitors (`S03_visitors`).** *Objective: Hear both visitors.* **Eskil** at Griefwatch (`MBS-D4`): the high-pass stitch; his company's grandfathers "held this ground"; with `TH_STANDING`, a line about the Assembly keeping honest accounts now, "so let me take an honest one home". **Tess** at Sorrowmere (`MBS-D5`): her grandmother "mended for the lowland companies"; the darns are what her grandmother taught her. Both are sincere. Neither has a second hold.

**Beat 4 — The tabs (`S04_tabs`).** *Objective: Re-stitch the hoist tabs.* **Leatherworking ~[GD: low–mid]**: two tabs, each unpick (2 s) and re-stitch (4 s); segments persist. **Crew alternative:** Calwen overnight (`MBS_TABS = crew`).

**Beat 5 — Calwen asks (`S05_choice`).** *Objective: Tell Calwen what you'd do with it.* `MBS-D6` at the sanctuary with Eskil and Tess both present. The player sets out what was found (dialogue recall): two manners, one field-dressing mend, a store book that says "two hands". Calwen: "That's not a second channel. That's a mend." Choice (`MBS_FATE`):
- **Retired:** washed and folded; laid in the retirement pool in its own place, not in any row. Eskil and Tess each hold a corner of the fold.
- **Kept:** washed and stored in the unsorted chest with a strip: *"Two hands. One mend. Not known."* Anyone may come and look.

The wash happens either way: **the wonder moment** (MBS.7). Quest Completed (`MBS-D6` end).

### MBS.6 Encounters

None. **MD-7 swap note:** no Hollowfoot content.

### MBS.7 The wonder moment: two dyes (Beat 5)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Into the frame** | The player lowers the banner into the washing frame (interaction *Wash*, 3 s). |
| 3–8 s | **Mud out** | Brown runs off. Then two colours come out of the weave: a rust-red from the ground cloth, a blue-grey from the darns. |
| 8–14 s | **Meet** | The two threads of colour drift across the frame toward each other and run together into a single dull violet in the water. It sits in the frame and does not separate. |
| After | **People** | Tess: "Oh." Eskil says nothing. Calwen: "Dye does that. Old dye." (beat) "I've washed a thousand. I don't remember it doing that." |
| What it means | | Dye chemistry, or not. It proves nothing about either side; nobody says it does. |

### MBS.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Ask Calwen about the banner on his table. | `MBS-D1` end with accept | Yes |
| `S01_lens` | Read the stitches. | 3 lens inspects | Yes |
| `S02_ask` | Ask who can say anything about it. | `MBS-D2` + `MBS-I2.01` + `MBS-D3` | Yes (any order) |
| `S03_visitors` | Hear both visitors. | `MBS-D4` + `MBS-D5` | Yes (any order with S02) |
| `S04_tabs` | Re-stitch the hoist tabs. | 2 × (`unpick` + `stitch_tab`) **or** keep watch (crew) | Yes |
| `S05_choice` | Tell Calwen what you'd do with it. | `MBS-D6` choice + wash + `MBS-D6.40` end | Yes (→ Completed) |

### MBS.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `MBS_TABS` = self / crew | `S04` | Calwen bark |
| `MBS_FATE` = retired / kept | `MBS-D6` | MCF opener; Eskil and Tess barks |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Retired** — *"Lay it down. On its own."* | Folded with both visitors holding corners; laid in the pool apart from every row. | Neither visitor takes anything home. Eskil is stiff; Tess cries a little and is glad she held a corner. | Retirement pool inspect shows it alone. Eskil bark at Griefwatch. |
| **Kept** — *"Keep it unsorted. Write what we know."* | In the chest with the strip. | It stays a question in a box; both visitors may come back and argue. They do (bark). | Inspectable in the chest. Calwen: "It'll outlive all of us. Somebody may bring a second channel. I doubt it." |

### MBS.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **Calwen's lens** | Tool (functional) | "A banner-tender's lens": inspect variant on cloth and stitching anywhere [GD]. |
| Small payment | Currency | From both visitors, oddly, for the trouble [GD]. |
| Skill XP | Actions only [GD] | Leatherworking. |
| *Cloth for Sale* | Story | `MBS-D6.42`. |

| Situation | Handling |
|---|---|
| No Leatherworking | Crew alternative. |
| Visits visitors before the lens | They talk; the "proof" lines need the lens inspects to be challenged (dialogue option appears after). |
| Walking away | Stays Active; resume Calwen (`MBS-B1.02`). Visitors stay in place. |
| Fail state | None. |
| Co-op | Per-player banner prop and choice (fallback: host). |

### MBS.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Lens inspect variant | Systems | A second inspect text on cloth props when the lens is in use. **Fallback:** plain inspects carry the detail. |
| Dye-meeting VFX | VFX | Two coloured fluid decals in the wash frame that merge. **Fallback:** inspect text. |
| Leatherworking repair | Systems | As MBA. |

**Mystery ledger.**

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Whose banner** | Not determined in content. | "Ours" (each visitor). | Two stitch manners; the field-dressing mend; the store book. | Highland proof; lowland proof. | **Yes.** | None (no second channel). |

**Open decisions.** If the Director prefers no Thornfell visitor in the Mire, Eskil becomes "a visitor from the high passes" with the same lines minus `TH_STANDING`.

| Review finding | Revision |
|---|---|
| The lowland mend risked naming Lowmark. | Only "lowland manner" and "lowlands"; no region named, no route. |
| "Both kinds of bones" risked counting. | Mara says only that she has seen the stitch on both; no number. |

### MBS.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Calwen Reed-Binder** [CANON] | How a cloth was made and mended. | Whose. Refuses to guess. | Patient, exact, gently immovable. |
| **Mara Fenholt** [CANON] | Where it lay; the stitch on bones. | Whose. | Few words. |
| **Corra Sallis** | Bannerbearer sayings. | — | Earnest. |
| **Eskil Stenning** [NEW] | His company's stories. | Anything about this cloth. | Courteous, stubborn, homesick. Not the role-named Ridge Warden of MBO (Settlements and Combat): they are two different visitors. |
| **Tess Albery** [NEW] | Her grandmother's darning. | Anything about this cloth. | Warm, hurried, hopeful. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| MBS-B1.01 | Calwen | Available | *"Two people want the same banner. Neither has asked it anything."* |
| MBS-B1.02 | Calwen | Active, returns | *"It's still on the table. It'll still be on the table. That's what tables are for."* |
| MBS-B2.01 | Eskil | Available, Griefwatch | *"There's a banner at the reed sanctuary with our stitch on it. The binder won't let me have it."* |
| MBS-B3.01 | Eskil | `retired` | *"I held a corner. I'll tell them that at home. It's not proof. It's something."* |
| MBS-B3.02 | Tess | `kept` | *"I came back to look at it. Eskil was already there. We had tea. Don't tell anyone."* |

#### Nodes

```
MBS-D1 (sanctuary; S00)
MBS-D1.01 CALWEN: (not lifting the reed weight off the cloth) "Traveller. Two letters, one banner. A Ridge Warden at Griefwatch. A lady from the lowlands at Sorrowmere."
MBS-D1.02 CALWEN: "They both want it as proof. I don't keep proof. I keep cloth."
MBS-D1.03 CALWEN: "Look at it with me. Ask whoever can say anything. Then tell me what you'd do. I'll decide. I'd like your word first."
  > "Show me."                                               → MBS-D1.10
  > "Not now."                                               → MBS-D1.20
MBS-D1.10 CALWEN: (hands over a lens on a cord) "Look at how. Never whose."   {quest Active}
MBS-D1.20 CALWEN: "It's waited in the mud. It can wait on a table."   {Inactive}
MBS-D1.30 [after 3 lens inspects] CALWEN: "Ground seams, high-pass manner. Darns, lowland manner. And that corner." (beat) "That one's neither. Ask Mara about that one."
```

```
MBS-D2 (Mara at the causeway site)
MBS-D2.01 MARA: "Here. Face down. Shallow. Nothing with it."
MBS-D2.02 MARA: (lens on the lower corner) "That's how they stitched people. Linen thread, close, tied off twice."
MBS-D2.03 MARA: "I've seen it on bones. Both kinds of bones." (beat) "That's all I've seen. That's all I'll say."
```

```
MBS-D3 (Corra)
MBS-D3.01 CORRA: "Bannerbearers say a banner mended by the other side belongs to both." (beat) "It's a saying. Calwen says sayings aren't rules."
MBS-D3.02 [MBR_CORRA_CORNER] CORRA: "If it's folded, I'll take a corner. I always take a corner."
```

```
MBS-D4 (Eskil, Griefwatch)
MBS-D4.01 ESKIL: "That's our seam. Double running, cord at the hoist. My grandmother stitched it on everything, even sacks."
MBS-D4.02 ESKIL: "Our grandfathers said companies held this ground. Nobody believes them at home. This would be something to show."
MBS-D4.03 [TH_STANDING] ESKIL: "The Assembly keeps honest accounts now. Let me take an honest one home."
  > [lens done] "The mends are lowland. And one is a field-dressing stitch."   → MBS-D4.10
  > "I'll tell Calwen."                                                        → end
MBS-D4.10 ESKIL: (a long look) "...Then somebody else had it after us." (beat) "Or before."
```

```
MBS-D5 (Tess, Sorrowmere)
MBS-D5.01 TESS: "Those darns. Long, flat, reed thread. My grandmother taught me that. She mended for the lowland companies."
MBS-D5.02 TESS: "She never said where they went. I thought if I found something she'd touched..."
  > [lens done] "The ground seams are high-pass. And one mend is how treatment crews stitched people."   → MBS-D5.10
MBS-D5.10 TESS: "She did that too. Sometimes. People and cloth." (beat) "So did everyone, I suppose. By the end."
```

```
MBS-D6 (sanctuary; S05)
MBS-D6.01 CALWEN: (Eskil at one end of the fold table, Tess at the other) "Witness. Say what we found. Not what it means."
  > "High-pass seams. Lowland darns. One field-dressing mend at the corner. The book says two hands. Mara found it face down, nothing with it."   → MBS-D6.02
MBS-D6.02 CALWEN: "That's not a second channel. That's a mend." (beat) "What would you do?"
  > "Lay it down. On its own, not in a row."               → MBS-D6.10
  > "Keep it unsorted. Write what we know."                → MBS-D6.20
MBS-D6.10 CALWEN: "Wash first. Then fold. You two take a corner each." {set MBS_FATE = retired}   → MBS-D6.30
MBS-D6.20 CALWEN: "Wash first. Then the chest. I'll write the strip." {set MBS_FATE = kept}   → MBS-D6.30
MBS-D6.30 {wash; wonder moment}
MBS-D6.31 TESS: "Oh."
MBS-D6.32 CALWEN: "Dye does that. Old dye." (beat) "I've washed a thousand. I don't remember it doing that."
MBS-D6.40 [retired] CALWEN: (at the pool) "We put you down. Rest." / [kept] CALWEN: (writes) "'Two hands. One mend. Not known.'"
MBS-D6.41 ESKIL: "I'll say I saw it." TESS: "So will I."
MBS-D6.42 CALWEN: "One more thing. Marshfall jetty. Someone's selling banner cloth by the strip." (beat) "Go and look. Don't buy any."
      {event: S05 → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| MBS-I1.01 | Ground seams (lens) | *"Double running stitch, very tight. The hoist is wrapped in cord. Calwen calls it the high-pass manner."* |
| MBS-I1.02 | Darns (lens) | *"Long, flat darns in reed thread, laid across the tears. Calwen calls it the lowland manner."* |
| MBS-I1.03 | Corner mend (lens) | *"A small tear closed with linen thread, close stitches, tied off twice. Neither manner. It looks like the stitch on a wound."* |
| MBS-I2.01 | Store book | *"'Morning after the Colour. Causeway, middle site. Cloth sound. Tabs rotten. Two hands of mending.' Nothing about whose."* |
| MBS-I2.02 | Strip (kept) | *"'Two hands. One mend. Not known.'"* |

---

## MCF — Cloth for Sale

### MCF.1 The quest in one paragraph

At the **Marshfall jetty**, **Gethin Scarth** has a stall of "commemorative goods": strips of old banner cloth folded into little squares, tied with reed, sold to anyone who wants a piece of the Field. He is polite, evasive and plainly frightened of whoever supplies him. Calwen knows the cloth by its weave: it is coming off standards on the Field. The player reads **Gethin's ledger** at the stall (he lets them; he is relieved someone asked), which records lots by marks, never names. Then the player **tracks** the cloth to its source (Hunting): reed cut at shoulder height, threads snagged on stems, boots in silt, off the causeway to the **Reed Hide**, a Rootshadow cutters' camp in a drowned trench where risen standards are being stripped bare on frames. The cutters work by day because the risen walk at dusk; they say stripping a standard stops it rising, and they are wrong (the bare poles still lean). The player assaults the Hide in three stages and brings the cloth out: three bundles, carried. Then the choice: **return** it to Calwen to be washed and laid, or **burn** it on the jetty in front of Gethin so that no strip of it can ever be sold.

**Remember:** reeds lying flat in a ring round a stack of stolen cloth. **Want next:** Bannerline, where Calwen will lay it at his stone if it came home.

### MCF.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. Gethin is the villain and fights.** | Rejected. Bible: Gethin never fights; no Rootshadow leader is named (MD-12). |
| **B. Night raid against Wraiths and cutters together.** | Rejected. Contract lists cutters only; and a day assault makes the cutters' logic readable (they work while the risen sleep). |
| **C. Stall → ledger → track → three-stage day assault → carry → return or burn** (selected). | **Selected.** Track, assault, recover; the Mire's Rootshadow combat-core content. |

| Element | Source | Status |
|---|---|---|
| Rootshadow Syndicate: fragmented, avoids large conflict; poisons | Dossier; Factions §17; bible MD-12 | [CANON] |
| Cutters strip risen standards; they worsen it, did not cause it | Bible §2.3 | [NEW] |
| Gethin Scarth, go-between at the Marshfall jetty; never fights | Bible §5.2 | [NEW] |
| The Reed Hide (MP23): cutters' camp in a drowned trench | Bible §4.2 | [NEW on CANON group] |
| Rootshadow Cutters (cutter, poisoner); no elite by design | Bible §10 | [NEW] |
| Hob Merrit, Marshfall fowler | Bible §5.2 | [NEW] |

### MCF.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.cloth_for_sale` |
| Series | *Cloth and Colour*, part 2 of 2 |
| Type | Combat challenge |
| Unlock | MBS Completed (`MBS-D6.42`). Gethin's stall is visible earlier as ambience; talking to him before MBS gives only `MCF-B1.01`. |
| Length | 35–45 minutes |
| Combat share | ~55% |
| Skills | **Hunting ~[GD: low–mid]**: read the trail sign from the jetty to the Hide (three sign inspects with the tracking interaction). Crew alternative: Hob Merrit tracks it with the player at his pace (keep watch one turn; he goes as far as the Hide's edge and no further). Melee or Ranged. |
| Choice | Return or burn the cloth (`MR_CLOTH`). |
| Outputs | **`MR_CLOTH`** (returned / burned); `MCF_LEDGER_READ`; the Reed Hide cleared (quiet); Gethin's stall closed |
| **Anchor** | Rootshadow (cutters; Gethin); the Marshfall jetty. |
| **World-truth row** | H25 (present pressure, local). |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | **Gethin's ledger** (read in place at the stall): marks for buyers and suppliers, no names, no route. |
| **State compliance** | Inactive → Active on `MCF-D1` accept; Completed on `MCF-D6` end. No fail. Cleared stages persist. Resume hook: Calwen (`MCF-B1.03`) or Gethin's empty stall. |
| **Combat compliance** | Rootshadow cutters (cutter, poisoner) fight to 0 HP with the ordinary defeat presentation. Gethin never fights and is never targetable. Melee or ranged in every stage; ranged is useful on poisoners, never required. No Wraiths: the assault is by day and Wraiths walk only at dusk. |

### MCF.4 The places

**MAP VERIFICATION REQUIRED.** Bible §4.2: Nine Stakes and the Reed Hide lie off the causeway; Marshfall at the causeway's far end.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Marshfall jetty** (MP02) | Gethin; ledger; burn site | A trestle stall under a reed awning: squares of old cloth tied with reed, a painted board "COMMEMORATIVE GOODS — A PIECE OF THE FIELD". Gethin's ledger in a tin under the trestle. An iron brazier for eel smoking at the jetty end. |
| **B. The trail** | Tracking | Off the causeway into reed: stems cut at shoulder height; red and blue-grey threads on reed heads; boot-prints in silt that lead onto a plank way laid under water at Slack (quest-pinned). |
| **C1. Hide mouth** | Stage 1 | Where the drowned trench opens into reed: a lookout platform on stakes, a reed screen. |
| **C2. Stripping frames** | Stage 2 | The trench's long bay: three standards lashed upright in timber frames, stripped to bare poles. Cutting knives, cloth on drying lines. Poison pots on a plank. |
| **C3. The stack** | Stage 3; strange moment | The trench's end: cloth folded in bales under reed thatch, dry. Around the stack the reeds lie flat in a ring. |

### MCF.5 Player-facing sequence

**Beat 0 — A piece of the Field (`S00_offer`).** *Objective: Look at what's being sold at the Marshfall jetty.* Gethin (`MCF-D1`). Inspect a square (`MCF-I1.01`). Gethin is polite and nervous.

**Beat 1 — The ledger (`S01_ledger`).** *Objective: Read Gethin's ledger.* Gethin lets the player read it at the stall (`MCF-D1.20`). Two required inspects (`MCF-I1.02`, `.03`): lots in, lots out, marks for suppliers (a cut reed) and buyers (several unrelated marks). No names; no places beyond "the Hide" and "the jetty". Sets `MCF_LEDGER_READ`. Gethin will not say who the cut-reed mark is: "They'd know I said."

**Beat 2 — The trail (`S02_track`).** *Objective: Track the cloth to where it's cut.* **Hunting ~[GD: low–mid]**: three sign inspects with the tracking interaction (cut stems; snagged threads; boots onto the plank way). Each reveals the next stretch. **Crew alternative:** Hob Merrit (`MCF-D2`; keep watch one turn; `MCF_TRACK = hob`). The plank way is walkable at Slack (pinned for the step).

**Beat 3 — The mouth (`S03_mouth`).** *Objective: Clear the Hide's lookout.* **MCF-E1**. The assault steps (`S03`–`S05`) are pinned to day (noon) for the player: arriving at dusk or night sets noon on entering the Hide mouth, because the cutters work days (`MCF-D3.02`).

**Beat 4 — The frames (`S04_frames`).** *Objective: Clear the stripping frames.* **MCF-E2**. After: inspect the bare standards (`MCF-I2.01`): no cloth, and the poles still lean.

**Beat 5 — The stack (`S05_stack`).** *Objective: Take the cloth back.* **MCF-E3**. Then **the strange moment** (MCF.7). Lift three bales (carry-state; one at a time, slow walk while carrying).

**Beat 6 — Carry (`S06_carry`).** *Objective: Bring the cloth out of the Hide.* Three carries to the trench mouth, where Hob (if he came) or a Marshfall cart waits. No pressure: the Hide is cleared.

**Beat 7 — Return or burn (`S07_cloth`).** *Objective: Decide what happens to the cloth.* At the jetty, Gethin and, sent for, Calwen (`MCF-D5`). Choice (`MR_CLOTH`):
- **Returned:** Calwen takes the bales to the sanctuary to be washed and laid. "Every piece. Even the squares." Gethin hands over his stall stock without being asked.
- **Burned:** the player burns the bales in the jetty brazier (interaction, 3 × 3 s). Calwen says one line, "Burned is laid, too. Hotter.", and leaves before the fire is lit. Gethin tips his own stock in after the bales.

Gethin closes his stall either way (`MCF-D6`). Quest Completed. Sets `MR_CLOTH`.

### MCF.6 Encounters

Tuned for Competent-to-Advanced identity (after MR-M2; MD-10).

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MCF-E1** | 2 × cutter, 1 × poisoner | Lookout platform and reed screen at the Hide mouth | Cutters: Aggressive, close in pairs along the bank. Poisoner: Defensive at range on the platform; throws poisoned blades. Leashed to the mouth. | **Cutter hook-slash:** draws the reed-hook back across the body (~1.0 s), then a wide slash (2.5 m arc); step back. **Poisoner throw:** dips the blade in the pot at the hip, green-black drip visible (~1.2 s), then a thrown blade; sidestep or block. Hit applies a standard poison (damage over time, ~8 s; ordinary antidote cures). | Introduces the poisoner's dip tell somewhere open. | 40–60 s; player at 60–80% HP. |
| **MCF-E2** | 3 × cutter, 1 × poisoner | Among the stripping frames (narrow bay, the frames are cover) | Cutters use the frames to flank; the poisoner kneels behind the far frame. | As E1. Additionally, **frame cut** (hazard MCF-H1): a cutter slashes a lashing (~1.5 s, the rope creaks) and a bare pole swings down in a 2 m line; step out of its line. | Uses terrain; ranged players use frames as cover too. | 60–80 s; player at 50–70% HP. |
| **MCF-E3** | 2 × cutter, 2 × poisoner | The stack bay; poisoners on the stack top, cutters in front | Poisoners alternate throws; cutters hold the bay. | As E1. **Poisoners alternate:** the second dips as the first throws; reading both is the fight. | The challenge peak. Ranged clears the stack top; melee climbs the low bale step (walkable fallback: a ramp of bales). | 70–100 s; player at 40–65% HP. |

**Rules.** Every cutter fights to 0 HP with the ordinary defeat presentation (CDR-1); none yields, flees or surrenders. Nothing a cutter drops advances the quest: the evidence is the ledger and the cloth. Gethin is at the jetty throughout and never present at the Hide. Hob (crew track) stops at the Hide's edge and never enters a fight. A beaten player wakes at Marshfall with cleared stages kept.

**MD-7 swap note:** no Hollowfoot content.

### MCF.7 The strange moment: the flattened ring (Beat 5)

| Time | Element | Spec |
|---|---|---|
| 0 s | **E3 ends** | The last cutter is defeated. The bay goes quiet. |
| 0–4 s | **The ring** | Around the cloth stack the reeds lie flat in a clean ring about four paces across, all pointing outward, as if something heavy had sat there and gone. The thatch on the stack is undisturbed. |
| Inspect | Inner voice | *"Flattened outward, all round. Nothing walked here. Something sat."* |
| After | | Hob (if present), from the bank: "Deer lie like that." (beat) "Deer don't lie on cloth." |
| What it means | | Never explained. It is not evidence and identifies nothing. |

### MCF.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Look at what's being sold at the Marshfall jetty. | `MCF-D1` end with accept + square inspect | Yes |
| `S01_ledger` | Read Gethin's ledger. | 2 ledger inspects | Yes |
| `S02_track` | Track the cloth to where it's cut. | 3 sign inspects **or** keep watch (Hob) | Yes |
| `S03_mouth` | Clear the Hide's lookout. | MCF-E1 defeated | Yes |
| `S04_frames` | Clear the stripping frames. | MCF-E2 defeated + bare-standard inspect | Yes |
| `S05_stack` | Take the cloth back. | MCF-E3 defeated + ring presentation | Yes |
| `S06_carry` | Bring the cloth out of the Hide. | 3 carry-deposits at the mouth | Yes |
| `S07_cloth` | Decide what happens to the cloth. | `MCF-D5` choice + outcome interaction + `MCF-D6` end | Yes (→ Completed) |

### MCF.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `MCF_LEDGER_READ` | `S01` | Marshfall barks |
| `MCF_TRACK` = self / hob | `S02` | Hob bark |
| **`MR_CLOTH` = returned / burned** | `MCF-D5` | **MR-M5** circle placement (Calwen, `MBL-B7.2a`) |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Returned** — *"Calwen. Every piece, even the squares."* | Bales and stall stock go to the sanctuary; Calwen washes them over days and lays them in a new row. | Slow; the cloth exists, and a cutter could come back for it (they don't; bark). | MR-M5: Calwen lays a folded square at his stone (`MBL-B7.2a`). |
| **Burned** — *"Burn it here. Nobody sells it again."* | Burned in the jetty brazier; Gethin's stock with it. | Calwen leaves before it is lit; the cloth is not laid with the others. | MR-M5: no cloth line. Calwen still stands at S4. |

### MCF.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **A cutter's reed-hook** | Equipment (economy pass) | Ordinary weapon drop table per the encounters package; not a quest reward [GD]. |
| **Marshfall's thanks** | Currency | Small payment from the jetty households [GD]. |
| Skill XP | Actions only [GD] | Hunting, Melee or Ranged. |
| The Reed Hide | Access | A quiet place after. On MCF Completed the three bare poles are taken out of the frames and laid in the bay (standard state `laid`); nothing at the Hide leans or stirs afterwards. |

| Situation | Handling |
|---|---|
| Death in the Hide | Respawn at Marshfall; cleared stages persist; current stage resets. |
| No Hunting | Hob. |
| Poisoned with no antidote | Poison runs out (~8 s); Hob carries a spare and offers one at the mouth. |
| Walking away | Stays Active; Gethin's stall stays open until `S07`. |
| Fail state | None. |
| Co-op | Shared cutters (credit to all on the stage). Each player carries their own bales (fallback: shared count). Choice per player; the jetty brazier and Calwen's row are per player (fallback: host). |

### MCF.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Tracking sign interaction | Systems | Hunting tracking inspect that reveals the next sign volume. |
| Poison DoT and antidote | Systems | Standard status effect. |
| Frame-cut hazard | Encounters | Scripted prop swing on a telegraph. **Fallback:** remove; E2 gets one more cutter. |
| Carry-state bales with slow walk | Systems | Existing carry convention. |
| Brazier burn interaction | Systems | Channel on a prop; deposit consumed. |
| Creatures | Encounters package | Rootshadow cutter, poisoner. |

**Mystery ledger.** *Who the cut-reed mark is:* withheld (no Rootshadow leader named, MD-12). *The flattened ring:* never explained.
**Open decisions.** MAP VERIFICATION REQUIRED for the Hide and the plank way.

| Review finding | Revision |
|---|---|
| First draft had cutters surrender at the stack. | Removed (CDR-1). |
| The ledger listed buyers' places. | Marks only; no routes (MD-9). |
| Night assault would add Wraiths outside contract. | Day assault; Wraiths walk only at dusk. |
| Independent review (2026-11-09): "strip it bare and the risen don't come" made the cutters' trade a working fix, against bible §2.3 (they worsen it). | The cutters believe it; the bare poles still lean; Hob calls it a story. |

### MCF.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Gethin Scarth** [NEW] | His lots, his marks. | Where the buyers go; won't say the supplier. | Polite, evasive, frightened. Never fights. |
| **Calwen Reed-Binder** | The weave. | Whose. | Quiet anger, kept down. |
| **Hob Merrit** [NEW] | Sign in reed. | — | Cheerful, patient, swears at herons. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| MCF-B1.01 | Gethin | Before MBS | *"A piece of the Field, traveller? Something to remember it by. Very reasonable."* |
| MCF-B1.03 | Calwen | Active, returns | *"It's still being sold. Every day it's still being sold."* |
| MCF-B2.01 | Hob | Tracking | *"Cut at the shoulder. That's not a reed-cutter. Reed-cutters cut low and swear."* |
| MCF-B3.01 | Cutter | E1 start | *"Field's free. Help yourself — oh. Not that kind."* |
| MCF-B3.02 | Cutter | E2 | *"Cut the lashing!"* |
| MCF-B4.01 | Marshfall household | Completed, `returned` | *"Calwen's got a new row. All squares. He washed every one."* |
| MCF-B4.02 | Gethin | Completed | *"I'm smoking eel now. Eel doesn't have anybody's name on it."* |

#### Nodes

```
MCF-D1 (jetty stall; S00–S01)
MCF-D1.01 GETHIN: "A piece of the Field. Folded fresh. Tied with reed. People like to have something."
MCF-D1.02 GETHIN: (seeing the player's lens, or hearing Calwen's name) "Ah." (beat) "You've been to the binder."
  > "Where does it come from?"                              → MCF-D1.10
  > "Can I see your book?"                                  → MCF-D1.20
MCF-D1.10 GETHIN: "Suppliers. I buy it. I sell it. I don't cut it. I wouldn't know how."   → MCF-D1 options
MCF-D1.20 GETHIN: (a long breath; he pulls the tin from under the trestle) "Read it here. Don't take it. I need it to know who I owe."   {quest Active; ledger inspectable}
MCF-D1.30 [after ledger] GETHIN: "The cut reed. That's them. I'm not saying more than a mark. They'd know I said."
MCF-D1.31 GETHIN: (very quiet) "If someone stopped them, I'd stop selling. I'd be glad to."
```

```
MCF-D2 (Hob; S02 crew)
MCF-D2.01 HOB: "Track cutters? Into the Field? For Calwen?" (beat) "Yes. Give me till the turn."
MCF-D2.02 HOB: "I'll take you to the edge. I'm a fowler. I don't go into trenches with people in them."   {keep watch; MCF_TRACK = hob}
```

```
MCF-D3 (after E2; bare standards)
MCF-D3.01 (inner voice, prompt line) "Three standards in frames, stripped to the pole. The poles still lean."
MCF-D3.02 [MCF_TRACK = hob, Hob at the edge, shouting] HOB: "That's why they work days. The risen walk at dusk. They tell buyers a bare pole stays down." (beat) "Look at it leaning. Filthy story."
```

```
MCF-D5 (jetty; S07)
MCF-D5.01 GETHIN: (looking at the bales, not at the player) "That's all of it. That's more than I ever saw."
MCF-D5.02 CALWEN: (arriving, sent for) "Witness. It's yours to say. I'd like it home. I'll understand if not."
  > "Calwen. Every piece, even the squares."                 → MCF-D5.10
  > "Burn it here. Nobody sells it again."                   → MCF-D5.20
MCF-D5.10 CALWEN: "Thank you." (to Gethin) "And your table."
MCF-D5.11 GETHIN: (already folding the squares into a basket) "Take them. Please."   {set MR_CLOTH = returned}   → MCF-D6.01
MCF-D5.20 CALWEN: (a long pause) "...Burned is laid, too. Hotter." (he goes)
MCF-D5.21 GETHIN: (tips his stall stock into the brazier after the bales) "There. Nothing to sell."   {burn interaction; set MR_CLOTH = burned}   → MCF-D6.01
```

```
MCF-D6 (close)
MCF-D6.01 GETHIN: (takes down the painted board) "I'll smoke eel. Eel's honest."
MCF-D6.02 [returned] CALWEN: "I'll wash them. It'll take the wet season." (beat) "I've nothing else to do in the wet."
      {event: S07 → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| MCF-I1.01 | A square | *"Old banner cloth, cut to a hand's width, folded and tied with reed. The weave matches the standards that came off the causeway."* |
| MCF-I1.02 | Ledger: lots in | *"'Lot from the Hide. Twelve squares.' Beside each lot, a mark: a cut reed."* |
| MCF-I1.03 | Ledger: lots out | *"Squares sold to marks: a fish, a circle with a bar, a three-pronged sign. No names. No places."* |
| MCF-I2.01 | Bare standard | *"A standard pole in a timber frame, stripped to the wood. Knife marks where the cloth was cut from the hoist. It leans in its frame all the same."* |
| MCF-I2.02 | The ring | *"Reeds flattened outward all round the stack. Nothing walked here. Something sat."* |

---

# Memory in the Ground and Water (standalones)

---

## MFW — The Father at the Ford

### MFW.1 The quest in one paragraph

Travellers at the **Wading Ford** see, at dusk, a man standing knee-deep in the water calling names. He never answers. Ferry households at **Blackwater Landing** have stories; **Morwen Lusk** thinks he might be her father **Abner Lusk**, a war-years ferryman, dead since she was small, who, the family says, "kept asking after people"; her brother **Nye** thinks "might" is not a comfort and wants it left alone. Rowan will not take anyone to the ford at dusk ("I don't cross at night. Walk."). The player sets a **fowler's hide** on the ford's bank at dusk and watches: the figure stands, calls, turns, calls again. Some names carry: *"Wil..."*, *"the Coe girls..."*, *"Elspet..."*. Then the records. In Rowan's boat shed is the landing's **war-years ferry list**: evacuees taken over the Blackwater, with a mark beside some names in one hand, *"asked after"*, and the hand signs *A.L.* Coe, Wil Fennick, Elspet Rye: all marked. And in the Lusk house, the family's **naming board**: every Lusk child born since the war carved with the name they were "named for", and every one of them is a name from the list. Two holds that a ferryman kept asking. Neither says the figure is him. Morwen asks the player to tell Granny Lusk, Abner's widow and their mother. Nye asks the player not to.

**Remember:** the figure turning toward you and calling a word that might have been "here". **Want next:** nothing in particular; this one ends where it began.

### MFW.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. The figure identifies itself.** | Rejected. Impressions never answer and never identify (dossier; bible §11.3). |
| **B. A fight at the ford.** | Rejected. Contract: the figure is never hostile; no combat. |
| **C. Watch → hear names → ferry list → naming board → tell or keep** (selected). | **Selected.** Watch, read, ask. The figure is the hook; the holds are records. |

| Element | Source | Status |
|---|---|---|
| The Father Who Waits at the Ford: knee-deep, calls names, never answers; might be an imprint | Dossier §XII.2 | [CANON myth] |
| The Wading Ford (MP25) | Bible §4.2 | [NEW place on CANON myth] |
| Ferry households; Rowan refuses night crossings | Bible §5.1; anchors | [CANON] |
| The Lusks, the ferry list, the naming board | This package | [NEW] |

### MFW.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.the_father_at_the_ford` |
| Series | Standalone |
| Type | Memory/lore |
| Unlock | MR-M3 Completed. Morwen at Blackwater Landing (`MFW-D1`). |
| Length | 25–35 minutes |
| Combat share | 0% |
| Skills | **Hunting ~[GD: low]**: set a fowler's hide on the bank (the hunting hide interaction) so marrow herons don't lift and the ford stays still enough for the figure to stand. Crew alternative: watch from the open bank; the herons lift and the figure does not stand the first dusk; keep watch for a second dusk, when it does. |
| Choice | Tell Granny Lusk what the records show, or keep it in the ferry book (`MFW_TOLD`: told / kept). |
| Outputs | `MFW_TOLD`; the ford as a dusk place |
| **Anchor** | Ferry households (Lusk; the landing). |
| **World-truth row** | H23. |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | **Ferry list** (Rowan's boat shed; read in place) + **Lusk naming board** (the Lusk house; read in place). Two holds that Abner Lusk asked after evacuees. Neither holds who the figure is. |
| **State compliance** | Inactive → Active on `MFW-D1` accept; Completed on `MFW-D5` end. No fail; missed dusks re-offer. Resume hook: Morwen at the landing (`MFW-B1.02`). |
| **Combat compliance** | None. The figure is never hostile and has no HP. |

### MFW.4 The places

**MAP VERIFICATION REQUIRED.** The Wading Ford lies in the Blackwater (bible §4.2), reached on foot along the peat edge from the landing. The ferry list's "over to the Rootrest side" (`MFW-I1.01`) implies a ferry from the landing that the Zones crossing register (§6.2) does not show: MAP VERIFICATION REQUIRED (2026-11-13 audit, SS-27); geography unchanged.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Blackwater Landing** (MP06) | Hook; ferry list | Rowan's boat shed: the **war-years ferry list**, a long roll in a reed tube on the shed wall, brought down for the player. |
| **B. The Lusk house** | Naming board | A ferry household's longhouse by the landing. Over the hearth, a board of carved names in pairs: child and "named for". Granny Lusk by the fire. |
| **C. The Wading Ford** (MP25) | Watch | A wide shallow ford with a stake (Slack at dusk, pinned). Reed banks. A heron roost. A flat place for a hide. |

### MFW.5 Player-facing sequence

**Beat 0 — The man in the water (`S00_offer`).** *Objective: Hear Morwen out.* `MFW-D1` (Morwen, then Nye in the doorway). Rowan's one line (`MFW-B2.01`).

**Beat 1 — The hide (`S01_hide`).** *Objective: Set a hide at the Wading Ford before dusk.* **Hunting ~[GD: low]**: hide interaction (gather reed, set frame, 2 × 3 s). Crew alternative: watch from the open bank (herons lift; the first dusk is lost; keep watch for the next).

**Beat 2 — Watch (`S02_watch`).** *Objective: Watch the ford at dusk.* Keep watch to dusk in the hide. **The strange moment** (MFW.7). Three name-fragments become audible across about 40 seconds; each is a listen prompt (stay still; moving breaks the hide and ends the watch for the night, re-offered next dusk). The player can call out (*Call to him*): no answer, ever.

**Beat 3 — The list (`S03_list`).** *Objective: Read the landing's war-years ferry list.* Rowan lets the player read it in the shed (`MFW-D2`). Three required inspects: the list (`MFW-I1.01`), the marks (`MFW-I1.02`), the signature (`MFW-I1.03`). Match the names heard (dialogue recall).

**Beat 4 — The board (`S04_board`).** *Objective: Look at the Lusks' naming board.* At the Lusk house, inspect the board (`MFW-I2.01`): every "named for" is from the list. Granny Lusk, by the fire, says only that Abner "named ours for people he was still asking after. He said that way somebody would keep asking." (`MFW-D3`).

**Beat 5 — Tell or keep (`S05_choice`).** *Objective: Decide what to say to Granny Lusk.* `MFW-D4` (Morwen and Nye outside). Choice (`MFW_TOLD`): **told** (the player tells Granny Lusk what the list and the board say, and that the man at the ford calls those names, and that nobody can say who he is) or **kept** (the player writes it in the landing's ferry book for whoever looks, and tells Granny only that her father's list is still kept). Quest Completed (`MFW-D5`).

### MFW.6 Encounters

None. **MD-7 swap note:** no Hollowfoot content. `[MD-3]`: Rowan does not cross; the ford is reached on foot.

### MFW.7 The strange moment: "here" (Beat 2)

| Time | Element | Spec |
|---|---|---|
| Dusk | **Stand** | A man's figure stands up out of the ford's middle, knee-deep, as if he had always been there. Mud-coloured; no face to read. Herons on the roost do not move (with the hide). |
| 0–40 s | **Calls** | He calls toward the far bank in a voice like someone at the far end of a room. Fragments: *"Wil..."*, *"...the Coe girls..."*, *"Elspet..."*. Captions only for these; the rest is unintelligible. |
| 40–46 s | **Turn** | He turns, slowly, toward the player's hide. He opens his mouth. What comes is one word that sounds like the player's own voice saying *"here"*. Captioned: *"...here."* |
| 46–50 s | **Down** | He settles into the ford like water closing. The stake still shows ochre. |
| Inspect | Inner voice | *"He called names. Then he turned and said 'here'. In your voice, or near it."* |
| What it means | | Never explained. It identifies no one; Abner Lusk is not named by the figure and never will be. |

### MFW.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Hear Morwen out. | `MFW-D1` end with accept | Yes |
| `S01_hide` | Set a hide at the Wading Ford before dusk. | Hide interaction **or** (open bank + one lost dusk) | Yes |
| `S02_watch` | Watch the ford at dusk. | Strange-moment presentation end (3 listen prompts) | Yes |
| `S03_list` | Read the landing's war-years ferry list. | 3 inspects + `MFW-D2` end | Yes |
| `S04_board` | Look at the Lusks' naming board. | Board inspect + `MFW-D3` end | Yes (any order with S03) |
| `S05_choice` | Decide what to say to Granny Lusk. | `MFW-D4` choice + `MFW-D5` end | Yes (→ Completed) |

### MFW.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `MFW_CALLED` | *Call to him* during `S02` | `MFW-D4.03` |
| `MFW_TOLD` = told / kept | `MFW-D4` | Landing barks; Granny Lusk bark |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Told** | Granny Lusk listens, then asks to be carried to the ford one dusk. Morwen does. | Nye is angry; "may" hurts. He says so once, then helps carry her. | Bark: Granny went, saw him, said "That's a man asking. Good." |
| **Kept** | Written in the ferry book: *"A.L.'s list kept. His names called at the ford. Who calls them, not known."* | Morwen is disappointed; Granny is told less. | Bark: Nye reads the entry some nights, alone. |

### MFW.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **A ferry household's welcome** | Access | Rest point at the Lusk house. |
| Small payment | Currency | Morwen insists [GD]. |
| Skill XP | Actions only [GD] | Hunting. |

| Situation | Handling |
|---|---|
| Moves during the watch | The figure settles; re-offer next dusk. |
| Asks Rowan to cross at dusk | "I don't cross at night. Walk." |
| Walking away | Stays Active; Morwen at the landing. |
| Fail state | None. |
| Co-op | The figure appears per player (each hears the "here"); a partner who moves ends only their own watch. Choice per player. |

### MFW.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Hide interaction (Hunting) | Systems | Existing hunting hide, here with a "stay still" state. |
| Dusk impression figure | NPC / VFX | A non-combat animated figure spawned at dusk per player; despawns on movement. |
| Captioned fragments | Audio / UI | Positional audio with partial captions. |

**Mystery ledger.**

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Who waits at the ford** | An impression of someone asking; unidentified. | A soldier seeking his family (dossier). | The names; the list; the board. | It is Abner Lusk's ghost. | **Yes.** | Never. |

**Open decisions.** None consequential. MAP VERIFICATION REQUIRED for the ford.

| Review finding | Revision |
|---|---|
| The "here" in the player's voice risked implying the figure answers. | It is not an answer to anything asked; it is one word, captioned, unexplained. |
| The list risked a count of evacuees lost. | It lists names taken over; "asked after" marks only; no tally of the lost. |
| Independent review (2026-11-09): a ninety-year-old daughter and adult great-grandchildren of a man who ferried thirty years ago did not fit the Mire's thirty-year war distance; "Tamsin" collided with Lowmark and Thornfell NPCs. | Morwen and Nye are Abner's children; Granny Lusk is his widow; the board covers two generations. Tamsin Rye renamed **Elspet Rye**. |

### MFW.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Morwen Lusk** [NEW] | Family stories. | Who the figure is. | Hopeful, practical. |
| **Nye Lusk** [NEW] | That "may" hurts. | — | Short, protective. |
| **Granny Lusk** [NEW], Abner's widow | Why her children are named what they are. | — | Slow, clear, funny. |
| **Rowan Mirewake** | The list's place in his shed. | — | One line at a time. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| MFW-B1.01 | Morwen | Available | *"You've been out on the water with Rowan. Have you seen the man at the ford?"* |
| MFW-B1.02 | Morwen | Active, returns | *"Dusk, at the ford. Sit still. He doesn't like moving."* |
| MFW-B2.01 | Rowan | Active | *"I don't cross at night. Walk. Take a coat."* |
| MFW-B3.01 | Granny Lusk | `told` | *"That's a man asking. Good. Somebody should."* |
| MFW-B3.02 | Nye | `kept` | *"I read the ferry book. Your line. Most nights."* |

#### Nodes

```
MFW-D1 (landing; S00)
MFW-D1.01 MORWEN: "Travellers come back from the Wading Ford white. A man in the water at dusk, calling names. Never answers."
MFW-D1.02 MORWEN: "My father ferried in the war. Abner. I was small when he went. Mam says he kept asking after people. I think..." (beat) "I think it might be him."
MFW-D1.03 NYE: (from the doorway) "Might." (beat) "Leave it, Mor."
MFW-D1.04 MORWEN: "Will you watch? Just watch. Tell me what he says."
  > "I'll watch."                                            → MFW-D1.10
  > "Not now."                                               → MFW-D1.20
MFW-D1.10 MORWEN: "Dusk. Sit still. The herons go up if you don't, and then he doesn't come."   {quest Active}
MFW-D1.20 MORWEN: "He'll be there. He always is."   {Inactive}
```

```
MFW-D2 (boat shed; S03)
MFW-D2.01 ROWAN: (takes a reed tube off the wall, hands it over, says nothing)
MFW-D2.02 [after list inspects] ROWAN: "War list. Who went over. Somebody marked them." (beat) "Read the end."
MFW-D2.03 [after signature] (recall) "The names I heard at the ford are marked."
MFW-D2.04 ROWAN: "Hm." (he puts the tube back himself)
```

```
MFW-D3 (Lusk house; S04)
MFW-D3.01 GRANNY LUSK: "That's our board. Every Lusk child since the war and who they're named for. Morwen's for a Morwen Coe. The little one's Elspet, for an Elspet Rye."
MFW-D3.02 GRANNY LUSK: "Abner named ours for people he was still asking after. He said that way somebody would keep asking. We've kept on with theirs."
MFW-D3.03 GRANNY LUSK: "Did he find them? I don't know. He never said found. He never said lost."
```

```
MFW-D4 (outside; S05)
MFW-D4.01 MORWEN: "Well?"
MFW-D4.02 (the player tells: the names at the ford; the list; the marks signed A.L.; the board)
MFW-D4.03 [MFW_CALLED] (optional) "I called to him. He didn't answer. Then he said 'here'."
MFW-D4.04 NYE: "That's a ghost story with our name on it." (beat) "Mam's old and she's tired. Don't."
MFW-D4.05 MORWEN: "It's two records and a man in the water. Tell her. She'd want to know he's still asking."
  > "Tell her. All of it, and that nobody knows who he is."  → MFW-D4.10  {set MFW_TOLD = told}
  > "Write it in the ferry book. Tell her the list is kept."  → MFW-D4.20  {set MFW_TOLD = kept}
MFW-D4.10 MORWEN: "Thank you." NYE: "...I'll carry her, if she wants to go."
MFW-D4.20 NYE: "Thank you." MORWEN: (quiet) "It's written. That's something."
```

```
MFW-D5 (close)
MFW-D5.01 [told] GRANNY LUSK: "Still asking." (beat) "Good. Somebody should."
MFW-D5.01 [kept] GRANNY LUSK: "Abner's list is kept? Good. Somebody should keep it."
      {event: S05 → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| MFW-I1.01 | Ferry list | *"A long roll: names, households, 'over to the Rootrest side'. Many hands. No date, only weather: 'fog', 'rain', 'thaw'."* |
| MFW-I1.02 | The marks | *"Beside some names, in one hand: 'asked after'. Wil Fennick. The Coe girls. Elspet Rye. And more."* |
| MFW-I1.03 | Signature | *"At the foot of each marked stretch: 'A.L.'"* |
| MFW-I2.01 | Naming board | *"Carved pairs. 'Elspet, for Elspet Rye.' 'Wil, for Wil Fennick.' 'Nye, for Nye Coe.' 'Morwen, for Morwen Coe.' Two generations, Abner's children and theirs. Every 'for' is a name from the list."* |

---

## MMR — The Mud That Remembers

### MMR.1 The quest in one paragraph

**Lenna Coote**, a visiting Memorykeeper scholar from Griefwatch, has strung the landward side of the **Drowned Encampment** with survey lines and stakes. The mud there is full of prints that seem to move in columns, and she is sure they show a famous retreat, *the Long Wade*, when a column is said to have walked out through the Blackwater by night and escaped. She is mapping it for the register. The player helps, and notices first what the fenny does notice: they bolt from the camp edge several seconds before the ground does anything (canon: they flee long before humans sense anything). Then Earthen Echoes stand up along Lenna's strings and walk. Her survey is disturbing the camp. The player tracks the prints properly (Hunting): they do not go anywhere. They loop, the same twenty paces again and again, from a cookhouse to a water hole and back. Under silt in the camp's **landward cookhouse** is the **ration board**: what the camp drew, day by day, in words, not numbers: *full, half, half, quarter, water only.* The "retreat" was men carrying water while they waited for food that came short. The player pulls Lenna's stakes (ending the disturbance) and helps her correct her map.

**Remember:** prints filling with water one after another, walking the loop once more. **Want next:** nothing; this is a correction, not a door.

### MMR.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. The prints are a real retreat.** | Rejected. Bible: the prints repeat motions, nothing more; the ration board tells what happened. |
| **B. Include the Memorywarden shard (dossier questline 2).** | Rejected. The shard belongs to MR-M2 (bible §6.1); a second shard would duplicate it. Recorded deviation from the dossier element. |
| **C. Does as warning → Echoes along strings → track loops → ration board → pull stakes → correct the map** (selected). | **Selected.** Observe, track, correct. |

| Element | Source | Status |
|---|---|---|
| The Mud That Remembers: echoes of battle, imprints mimicking troop movements, animals behaving erratically, scholars misinterpreting | Dossier §XV questline 2 | [CANON] |
| Drowned Encampment (MP09): wagons, tents sunk; rusted weapons; repeating sounds | Dossier §VI.2 | [CANON] |
| Fenny does flee long before humans sense anything | Dossier §X | [CANON] |
| Earthen Echoes re-form while disturbed | Bible §2.6, §7.3 | [NEW] |
| The Long Wade story; Lenna; the cookhouse; the ration board | This package | [NEW] |

### MMR.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.the_mud_that_remembers` |
| Series | Standalone |
| Type | Environmental |
| Unlock | MR-M2 Completed. Ysolde mentions Lenna's request (`MMR-B1.01`), or Lenna at the camp's landward edge (`MMR-D1`). |
| Length | 30–40 minutes |
| Combat share | ~25% |
| Skills | **Hunting ~[GD: mid]**: read the prints with the tracking interaction (three loop points). Crew alternative: Hob Merrit reads them with the player (keep watch one turn; he comes, reads, and says the loop out loud). Melee or Ranged. |
| Choice | How the map is corrected (`MMR_MAP`: corrected / annotated). No fail. |
| Outputs | `MMR_MAP`; Lenna's map in the Sorrowmere register room |
| **Anchor** | Memorykeepers (Lenna; Ysolde). |
| **World-truth row** | H12 (the war broke the Mire's practice; here, what a waiting camp looked like). |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | **Ration board** (landward cookhouse; read in place). |
| **State compliance** | Inactive → Active on `MMR-D1` accept; Completed on `MMR-D5` end. No fail. Resume hook: Lenna (`MMR-B2.02`). |
| **Combat compliance** | Earthen Echoes (echo, file) to 0 HP; MMR-E1 and MMR-E2 fight once and do not re-form; MMR-E3 **re-forms only while `S04` is active and stakes remain** (one condition, MMR.11). Pulling the last stake ends the condition. Melee or ranged. |

### MMR.4 The places

**MAP VERIFICATION REQUIRED.** MR-M3 passes through the Drowned Encampment's cut by boat; MMR uses the camp's **landward side**, reachable on foot from the peat edge. The cookhouse here is a different structure from the field-kitchen stove MR-M3 shows in the cut.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Landward edge** | Lenna; does | Lenna's tent, a drawing board with a map of arrows, a basket of survey stakes. Fenny does grazing at the edge. |
| **B. The string field** | Echoes; prints | A grid of reed strings on stakes over a flat of grey mud covered in prints. Rusted things through the surface. |
| **C. The loop** | Tracking | The prints form a worn path between a sunk cookhouse and a water hole ringed with old barrel staves. |
| **D. The cookhouse** | Ration board | Half sunk; roof gone. A board on the wall under silt. |

### MMR.5 Player-facing sequence

**Beat 0 — The Long Wade (`S00_offer`).** *Objective: Hear what Lenna is mapping.* `MMR-D1`. Her map: arrows marching toward the water.

**Beat 1 — Help her measure (`S01_strings`).** *Objective: Set Lenna's last two survey stakes.* Two stake-placing interactions (2 s each). On the second, the does at the edge **bolt** (MMR.7 tell); 4–6 s later **MMR-E1** begins along the strings.

**Beat 2 — Read the prints (`S02_track`).** *Objective: Follow the prints.* **Hunting ~[GD: mid]**: three tracking inspects at loop points (`MMR-I1.01`–`.03`): the prints turn; they come back; they wear a path. **Crew alternative:** Hob (`MMR-D2`). Each loop point disturbs the ground; at the third, **MMR-E2** (a file walking the loop).

**Beat 3 — The cookhouse (`S03_board`).** *Objective: Search the sunk cookhouse.* Clear silt from the board (2 × 3 s channel). Read the **ration board** (`MMR-I2.01`).

**Beat 4 — Pull the stakes (`S04_stakes`).** *Objective: Pull Lenna's survey stakes.* `MMR-D3` (Lenna, reluctant, then helping). Pull six stakes (1 s each, any order; pulled stakes persist) while **MMR-E3** stands along the strings. The condition is the quest step, not each stake: Echoes re-form while any stake stands, and when the last is pulled they collapse and do not re-form. **The strange moment** (MMR.7).

**Beat 5 — Correct the map (`S05_map`).** *Objective: Help Lenna correct her map.* `MMR-D4`. Choice (`MMR_MAP`): **corrected** (she redraws the loop and writes "water carry; waiting; ration short" and strikes "Long Wade") or **annotated** (she keeps her arrows and writes beside them what the board says, "so people see how easy it was to be wrong"). Quest Completed (`MMR-D5`).

### MMR.6 Encounters

Tuned for Competent identity (after MR-M2).

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MMR-E1** | 3 × Earthen Echo (echo) | Stand up along the strings | Walk the string lines, repeating a motion (carrying, lifting a pail) | **Does bolt** 4–6 s before any spawn (the region's warning). **Stand-up:** mud hump holds ~1.5 s. **Swing:** arms lift ~1.2 s, then a 2 m swing. | Teaches the does' warning. | 40–60 s; 70–85% HP. |
| **MMR-E2** | 1 × Earthen Echo (file), 2 × echo | The loop path | The file walks the loop in a lane and strikes on its third step; echoes walk beside. | **File step:** the ground ripples on each step; on the third, a forward thrust (~1.0 s windup, 3 m line); step out of the lane. | Previews the file without the General's count. | 50–70 s; 60–80% HP. |
| **MMR-E3** | 4 × echo (2 at a time) | Along remaining strings during `S04` | Re-form 6 s after defeat while `S04` is active and stakes remain (one condition for the encounter; MMR-E1 and MMR-E2 never re-form) | As E1. | Pressure while the player pulls stakes; pulling is the win. | 60–90 s; 50–75% HP. |

**Rules.** Echoes fight to 0 HP, collapse into mud, and only MMR-E3 re-forms, while `S04` is active and stakes remain (bible §2.6; MMR.11). Lenna stays at her tent and is never targetable. Nothing dropped advances the quest. **MD-7 swap note:** no Hollowfoot content.

### MMR.7 The does and the loop (tell and strange moment)

| Moment | Spec |
|---|---|
| **The does (tell, every disturbance)** | Grazing does lift their heads together, freeze ~1 s, then bolt away from the strings. 4–6 s later the mud stirs. Inspect after: *"They knew before the ground did."* |
| **The loop (strange moment, after the last stake)** | 0–2 s: silence; strings slack. 2–10 s: the prints in the loop fill with water one after another, in walking order, from the cookhouse to the water hole and back, as if the loop were walked once more. 10 s: still. Lenna: "Seen: that. Thought: I'm going to be careful what I write for a while." Never explained. |

### MMR.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Hear what Lenna is mapping. | `MMR-D1` end with accept | Yes |
| `S01_strings` | Set Lenna's last two survey stakes. | 2 stakes + MMR-E1 defeated | Yes |
| `S02_track` | Follow the prints. | 3 tracking inspects **or** keep watch (Hob) + MMR-E2 defeated | Yes |
| `S03_board` | Search the sunk cookhouse. | 2 × `clear_silt` + board inspect | Yes |
| `S04_stakes` | Pull Lenna's survey stakes. | 6 × `pull_stake` | Yes |
| `S05_map` | Help Lenna correct her map. | `MMR-D4` choice + `MMR-D5` end | Yes (→ Completed) |

### MMR.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `MMR_TRACK` = self / hob | `S02` | Hob bark |
| `MMR_MAP` = corrected / annotated | `MMR-D4` | Register room map prop; Ysolde bark |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Corrected** | "Long Wade" struck; the loop drawn. | Lenna's work of a season is gone. She minds. | The map hangs in the register room as a water-carry plan. |
| **Annotated** | Arrows kept; the board's words beside them. | Someone may only read the arrows. | The map hangs with both; Ysolde: "It's honest about being wrong. I like that." |

### MMR.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **Does' warning** | Knowledge | Fenny does at Mire edges now carry an inspect noting what their bolting means. |
| Small payment | Currency | Lenna's survey fee, split [GD]. |
| Skill XP | Actions only [GD] | Hunting, Melee or Ranged. |

| Situation | Handling |
|---|---|
| Death | Respawn at the landward edge; pulled stakes and read loop points persist. |
| No Hunting | Hob. |
| Walking away | Stays Active; resume Lenna (`MMR-B2.02`). |
| Fail state | None. |
| Co-op | Shared Echoes; stakes pulled by any player count for all on `S04`; map choice per player. |

### MMR.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Fauna flee trigger before spawns | Encounters / AI | Ambient does with a scripted flee 4–6 s before an encounter spawn. |
| Re-forming by condition | Systems | **No new runtime:** Lowmark drift-site state model with one condition (`S04` active and stakes remaining), not per-prop re-forming (simplified in independent review 2026-11-09, CDR-4). |
| Print-filling VFX | VFX | Sequential decal swap. **Fallback:** inspect text. |

**Mystery ledger.**

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The marching prints** | Repeated motions of a camp that waited, short of food, carrying water. | The Long Wade, an escape. | Loop prints; ration board. | A famous retreat. | — | MMR. |

**Open decisions.** The dossier's "Memorywarden shard that reacts to emotional peaks" is not used here (owned by MR-M2); recorded deviation.

| Review finding | Revision |
|---|---|
| The ration board first carried counts of men. | Words only: full, half, quarter, water only. |
| Lenna first ignored the does. | She notices them second; the player first. |

### MMR.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Lenna Coote** [NEW] | Survey method; the Long Wade story. | That she is wrong. | Bright, quick, honest once shown. |
| **Hob Merrit** | Prints. | — | Cheerful. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| MMR-B1.01 | Ysolde | Available | *"A scholar from Griefwatch is mapping the Drowned Encampment for my register. I'd like someone with her who reads ground."* |
| MMR-B2.02 | Lenna | Active | *"The strings are still up. So is the mud, apparently."* |
| MMR-B3.01 | Hob | `MMR_TRACK = hob` | *"Round and round. That's not marching. That's chores."* |

#### Nodes

```
MMR-D1 (landward edge; S00)
MMR-D1.01 LENNA: (at her drawing board) "Look. Columns, all heading for the water. The Long Wade. They walked out through the Blackwater by night. It's all in the mud."
MMR-D1.02 LENNA: "Two more stakes and I've the whole grid. Help me?"
  > "Show me where."                                         → MMR-D1.10
MMR-D1.10 LENNA: "There and there. Mind the does, they're skittish today."   {quest Active}
MMR-D1.20 [does bolt, before E1] LENNA: "What's got into th—"
```

```
MMR-D2 (Hob; crew)
MMR-D2.01 HOB: "Prints? Give me till the turn. I'll read them out loud and you can write it."
```

```
MMR-D3 (stakes; S04)
MMR-D3.01 LENNA: (reading the board) "Full. Half. Half. Quarter. Water only." (long pause) "They weren't walking out. They were waiting."
MMR-D3.02 LENNA: "And my strings woke it up." (beat) "Pull them. I'll take that side."
```

```
MMR-D4 (map; S05)
MMR-D4.01 LENNA: "Seen: that. Thought: I'm going to be careful what I write for a while."
MMR-D4.02 LENNA: "The map. Do I strike it, or keep it and write the truth beside it?"
  > "Strike it. Draw the loop. Write what the board says."   → MMR-D4.10  {set MMR_MAP = corrected}
  > "Keep your arrows. Write the board beside them."         → MMR-D4.20  {set MMR_MAP = annotated}
MMR-D4.10 LENNA: (draws a line through 'Long Wade') "Water carry. Waiting. Ration short."
MMR-D4.20 LENNA: "So people see how easy it was to be wrong. All right."
```

```
MMR-D5 (close)
MMR-D5.01 LENNA: "A season of work and the truest thing on it is a cook's board." (beat) "Ysolde will like that."
      {event: S05 → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| MMR-I1.01 | Loop point 1 | *"The prints turn here. All of them. Nobody walked on."* |
| MMR-I1.02 | Loop point 2 | *"The same prints come back the other way, deeper. Carrying something."* |
| MMR-I1.03 | Loop point 3 | *"A path worn by the same feet, cookhouse to water hole and back, over and over."* |
| MMR-I2.01 | Ration board | *"Chalk on wood, under silt. One line a day, in words: 'Full.' 'Half.' 'Half.' 'Quarter.' 'Quarter.' 'Water only.' 'Water only.' Then nothing."* |

---

## MSG — The Singing Trench

### MSG.1 The quest in one paragraph

In storms, a drowned wartime trench at the Field's edge **hums**. **Ysolde** says airflow and mud compression; **Prue Calloway** says the earth is grieving. Both are partly right. **Ned Siskin**, a reed cutter, uses the trench as his shortcut to the cutting beds, and this season its timber **revetment** is bulging: one more storm and the wall will slump and bury the path. The player goes in during a storm (quest-pinned) and learns to listen: the trench has three plank-covered **vents** left from the war, and in the storm air runs through whichever are open. A bay with air running through it sings, and a singing bay draws water out of its mud; a silent bay is under pressure. The bay behind the bulge is silent. The player opens and closes vents until that bay sings, holds the arrangement through three rushes of Reedlurkers up out of the flooded sumps, then props the revetment with reclaimed timber (Woodcutting). After the storm drops, the trench keeps humming for a few seconds into still air.

**Remember:** a sound that went on after its cause stopped. **Want next:** nothing; Ned's path is open.

### MSG.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. The hum is proven to be grief.** | Rejected. Belief stays belief; the dossier keeps both readings. |
| **B. An Echo fight in the trench.** | Rejected. Bible §7.2: Echo-free puzzle. Reedlurkers only (contract). |
| **C. Listen → vents → hold through three waves → prop** (selected). | **Selected.** Listen, dig, prop. Distinct from MR-M4's sluice order (that reads stains for a sequence; this reads sound for a combination). |

| Element | Source | Status |
|---|---|---|
| The Singing Trench: drowned trenches hum in storms; Memorykeepers say airflow and mud compression; Tenders say grief | Dossier §XII.3 | [CANON myth] |
| MP19 at the Field's edge | Bible §4.2 | [CANON myth place] |
| Reedlurkers; reed-ripple telegraph | Bible §10 | [NEW] |
| Vents, revetment, Ned Siskin | This package | [NEW] |

### MSG.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.the_singing_trench` |
| Series | Standalone |
| Type | Environmental |
| Unlock | MR-M1 Completed. Ned at the Sorrowmere causeway head (`MSG-D1`), or Ysolde and Prue arguing on the raised way (`MSG-B1.01`). |
| Length | 25–35 minutes |
| Combat share | ~15% |
| Skills | **Woodcutting ~[GD: low–mid]**: cut three props from reclaimed trench timber and set them. Crew alternative: Ned brings props from his cutting-bed store (keep watch one turn; he sets them with the player). Melee or Ranged. |
| Choice | None. |
| Outputs | `MSG_LISTENED`; the trench path open; the trench as a storm place |
| **Anchor** | Memorykeepers and Tenders (Ysolde, Prue); a reed cutter. |
| **World-truth row** | None. |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive → Active on `MSG-D1` accept; Completed on `MSG-D4` end. No fail. Vent arrangement and props persist. Resume hook: Ned (`MSG-B2.02`). |
| **Combat compliance** | Reedlurkers (lurker, snapper) to 0 HP. Melee or ranged. |

### MSG.4 The places

**MAP VERIFICATION REQUIRED** (Field edge).

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Trench mouth** | Entry | Ned's path markers; a duckboard way along the trench floor, half under water. |
| **B. Bays 1–3** | Puzzle | Three bays separated by traverses. Each has a **vent**: a plank cover over a brick-lined shaft to the surface (open / closed). Bay 2's revetment bulges, planks bowed, mud weeping between them. |
| **C. Sumps** | Encounter | Flooded sumps at bays 1 and 3 where Reedlurkers lie. |
| **D. Timber pile** | Woodcutting | Fallen revetment posts at the far end; reclaimed wood. |

### MSG.5 Player-facing sequence

**Beat 0 — The shortcut (`S00_offer`).** *Objective: Hear Ned out.* `MSG-D1`. With Ysolde and Prue's argument heard (`MSG-B1.01`), one extra line.

**Beat 1 — Listen (`S01_listen`).** *Objective: Go into the trench in a storm and listen.* Keep watch to storm (pinned). The storm is ambient presentation (wind, flattened reeds, a rising whistle in the shafts); nothing is timed to it. In the trench, *Listen* in each bay (an inspect that plays and describes that bay's current note, `MSG-I1.01`–`.03`). Bay 2 is silent; its mud weeps.

**Beat 2 — The vents (`S02_vents`).** *Objective: Make the bulging bay sing.* Three vents, open/closed (interaction 2 s each, any time). The rule, learned by listening: air runs between the two open vents nearest each other (with all three open, the shortest run, A to B); every bay on that run sings. Vent A sits in bay 1, vent B in the traverse at the head of bay 2, vent C in bay 3. Starting state: A open, B closed, C open; the run goes A to C over the traverse tops, so bays 1 and 3 sing and bay 2 stays silent. Solution: **close A, open B, open C**: the run passes from B down through bay 2 to C, and bay 2 sings. Any other arrangement sings other bays; *Listen* in bay 2 to check. No penalty; change a plank and listen again.

**Beat 3 — Hold (`S03_hold`).** *Objective: Keep the bay singing while the sumps stir.* With the right arrangement set, the drawn water stirs the sumps: **MSG-E1** comes in three waves, each starting a few seconds after the last is defeated. If a lurker knocks a vent plank shut (1.0 s tell: it climbs the shaft lip), the player re-opens it. A wave counts when it is defeated with bay 2 singing; counted waves persist.

**Beat 4 — Prop (`S04_prop`).** *Objective: Prop the revetment.* **Woodcutting ~[GD: low–mid]**: cut three props from the timber pile (3 × 3 s), carry, set against the bulge (3 × 2 s). **Crew alternative:** Ned's props (`MSG-D2`).

**Beat 5 — After (`S05_after`).** The storm drops (pinned end). **The strange moment** (MSG.7). `MSG-D3` with Ned; then Ysolde and Prue (`MSG-D4`). Quest Completed.

### MSG.6 Encounters

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MSG-E1** | Wave 1: 2 × lurker; wave 2: 1 × lurker, 1 × snapper; wave 3: 2 × lurker, 1 × snapper | Flooded sumps, bays 1 and 3 | Lunge from water; snappers spit from the sump lip; lurkers may climb to a vent lip | **Reed-ripple** (~1.2 s) before a lunge; **snapper spit** (throat swells ~1.0 s); **vent climb** (claws on the lip, ~1.0 s) before knocking a plank shut | Pressure on the puzzle state; three short fights | 25–40 s per wave; ends at 55–75% HP |

**Rules.** Reedlurkers fight to 0 HP; they do not re-form. Ned waits at the mouth and is never a target. **MD-7 swap note:** no Hollowfoot content.

### MSG.7 The strange moment: the hum after (Beat 5)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Still** | The storm drops. Reeds stand up. No wind. |
| 0–5 s | **Hum** | The trench keeps humming, bay 2's note, steady, in still air. |
| 5–6 s | **Stop** | It stops, cleanly, mid-note. |
| After | | Ned: "Wind's gone." (beat) "It didn't know." Ysolde later: "Air in the shafts. Slow to settle." Prue: "Or not." Both are said; neither is chosen. |
| What it means | | Unexplained; plausibly air still moving in the shafts. |

### MSG.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Hear Ned out. | `MSG-D1` end with accept | Yes |
| `S01_listen` | Go into the trench in a storm and listen. | 3 bay *Listen* inspects | Yes |
| `S02_vents` | Make the bulging bay sing. | Arrangement A closed, B open, C open + *Listen* in bay 2 | Yes |
| `S03_hold` | Keep the bay singing while the sumps stir. | 3 MSG-E1 waves defeated with the arrangement held (persist) | Yes |
| `S04_prop` | Prop the revetment. | 3 props cut + set **or** keep watch (Ned) + set | Yes |
| `S05_after` | — | Strange moment + `MSG-D3` + `MSG-D4` end | Yes (→ Completed) |

### MSG.9 Flags

| Flag | Set by | Read by |
|---|---|---|
| `MSG_PROPS` = self / ned | `S04` | Ned bark |
| `MSG_LISTENED` | `S05` | Ysolde / Prue barks |

No choice; no region flag.

### MSG.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **Ned's shortcut** | Access | The trench path open between the Field edge and the cutting beds. |
| A reed cutter's bundle | Gift | Functional name; economy pass [GD]. |
| Skill XP | Actions only [GD] | Woodcutting, Melee or Ranged. |

| Situation | Handling |
|---|---|
| Wrong arrangement | *Listen* tells which bays sing; change a plank and listen again. |
| Death | Respawn at the mouth; arrangement and counted waves persist. |
| Walking away | Stays Active; storm pin persists for this player until `S05`. |
| Fail state | None. |
| Co-op | Vents are shared within the instance (fallback: host); wave count shared. |

### MSG.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Storm ambience | Audio | Looping storm and shaft-whistle ambience under the pinned storm; **no gameplay timing** (the first draft's timed gust cycle and gust-gated interactions were removed in independent review 2026-11-09, CDR-4). |
| Vent props with three states logic | Systems | Two-state props; a lookup of which bays sing per combination; audio per bay. **Fallback:** dialogue picks of arrangements. |
| Pinned storm | Systems | Per-player presentation weather. |

**Mystery ledger.** *Why it hums:* airflow and compression (Memorykeepers); grief (Tenders). Both kept. The after-hum: unexplained.
**Open decisions.** None consequential.

| Review finding | Revision |
|---|---|
| Puzzle risked repeating MR-M4's order puzzle. | Combination by sound; no order. |
| Independent review (2026-11-09): a timed gust cycle with interaction windows was a bespoke mechanic. | *Listen* inspects and ordinary waves; the storm is ambience only. |
| Prue's belief risked being proven wrong. | Ysolde's account explains the hum, not the after-hum; Prue's "Or not" stands. |

### MSG.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Ned Siskin** [NEW] | The path; the bulge. | Why it hums; doesn't care. | Practical, wry. |
| **Ysolde Haverel** | Airflow. | — | "That's my reading." |
| **Prue Calloway** | Tender belief. | — | Pious, brisk. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| MSG-B1.01 | Ysolde / Prue | Available, raised way | YSOLDE: *"Air in old shafts."* PRUE: *"Grief in old ground."* YSOLDE: *"Both, then."* PRUE: *"Both."* |
| MSG-B2.02 | Ned | Active | *"Storm's due. Trench sings. Wall bulges. In that order."* |
| MSG-B3.01 | Ned | Completed | *"Walked it in a gale. Sang like a choir. Didn't fall on me."* |

#### Nodes

```
MSG-D1 (causeway head; S00)
MSG-D1.01 NED: "Traveller. You read ground? There's a trench I cut through to the beds. It sings in storms. Fine. Now it's bulging."
MSG-D1.02 NED: "Memorykeepers say air. Tenders say grief. I say the wall's coming down on my path."
  > "I'll look in the next storm."                           → MSG-D1.10
MSG-D1.10 NED: "Next one's coming. Listen to it. It tells you which bit's in trouble. The quiet bit."   {quest Active}
```

```
MSG-D2 (props; crew)
MSG-D2.01 NED: "I've posts at the beds. Give me a turn. I'll carry; you hold."   {keep watch; MSG_PROPS = ned}
```

```
MSG-D3 (after)
MSG-D3.01 NED: "Wind's gone." (beat) "It didn't know."
MSG-D3.02 NED: "Wall's held. That's my bit. The singing's yours and theirs."
```

```
MSG-D4 (raised way; close)
MSG-D4.01 YSOLDE: "Air in the shafts. Slow to settle. That's my reading."
MSG-D4.02 PRUE: "Or not." (beat) "That's mine."
MSG-D4.03 YSOLDE: "Both, then. Written."   {set MSG_LISTENED; event: quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| MSG-I1.01 | Bay 1, listened (start state) | *"A low note, steady. The mud at the bay's foot is drier than the rest."* |
| MSG-I1.02 | Bay 2, listened (start state) | *"Silent. The revetment bows outward. Water weeps between the planks."* |
| MSG-I1.03 | Bay 3, listened (start state) | *"A higher note. The sump shivers."* |
| MSG-I1.04 | A vent | *"A plank cover over a brick shaft to the surface. Air pulls at your hand when it's open."* |

---

## Package review log (cross-quest)

| Check | Result |
|---|---|
| Bible §7.1/§7.2 rows | MBS, MCF, MFW, MMR, MSG match code, type, unlock, place and core verb. |
| §7.3 contracts | Six fields on every card as the bible lists them. MCF: cutters to 0 HP, Gethin never fights, ledger read in place. MFW: the figure is never hostile. MMR: only MMR-E3 re-forms, while `S04` is active and stakes remain (2026-11-13). MSG: Reedlurkers only. |
| Flags for the mains | `MR_CLOTH` returned / burned, set by MCF `S07`, read by MR-M5 exactly as Act III's input table states. No other `MR_` flag set. |
| Dating | No calendar dates; weather words only (ferry list). |
| R08 | No sides, units or figures of dead; the ration board in words; Calwen never names a side. |
| CDR-1/2 | Every enemy to 0 HP; no yields or retreat; ranged first-class, never required. No SX. |
| Deviation | MMR omits the dossier's Memorywarden shard element (owned by MR-M2). |
| MD-7 / MD-3 | No Hollowfoot content; Rowan never crosses at night. |
| **Independent review (2026-11-09)** | 7 findings fixed in place (0 high, 5 medium, 2 low). **Medium:** MCF said stripping cloth stops standards rising (a working fix, against bible §2.3 "they worsen it"; now the cutters' false belief, poles still lean); MCF burn branch had Calwen both absent and speaking (now he speaks and leaves); MFW generations did not fit the thirty-year war distance (ninety-year-old daughter, adult great-grandchildren; now Abner's widow and children) and "Tamsin" collided with Lowmark/Thornfell NPCs (now Elspet Rye); MSG's timed gust cycle with gust-gated interactions replaced by *Listen* inspects and three ordinary waves (storm is ambience only); MMR per-stake re-forming simplified to one step condition (drift-site model). **Low:** Eskil's "Stonewake keeps honest accounts" used a person's/quest's name as an institution (now "the Assembly"); MSG all-vents-open case defined. Checked and unchanged: `MR_CLOTH` returned / burned set at MCF `S07` as Act III `MBL-B7.2a` reads it; cutters to 0 HP, Gethin never fights, ledger read in place; MMR does not use the Memorywarden shard; no dates or casualty numbers; ranged first-class, never required; no Hollowfoot. |
| Batch 4 encounter alignment review, 2026-11-09 | Aligned with `Enemies/Caelmor_Mire_Encounter_and_Enemy_Requirements.md` §13.3 (numbers and text only; no id, step or flag renamed): MCF cutter hook-slash ~0.9 s → ~1.0 s (C-1, I-10); MCF-E2 frame cut ~1.0 s → ~1.5 s and labelled hazard MCF-H1 (I-12, I-23). MSG-E1 and MMR rows already match C-5 and C-3. |
| Playability audit fixes, 2026-11-13 | SS-01 (one MMR re-form condition), SS-07 (MBS hall scene held during MR-M5 until `S03`), SS-13 (Eskil and the MBO Warden are two people), SS-18 (MCF poles laid on completion; assault pinned to day), SS-27 (MAP VERIFICATION note only), CO-01 (co-op host fallback is provisional presentation only). Authored walkthrough only. |
| Playability audit fixes review, 2026-11-13 | Independent review of the same-day fixes. Package review table: MMR contract line updated to the SS-01 single re-form condition. Authored walkthrough only; text only; no id, step, flag or geography changed; no Director recommendation promoted. |
