# Caelmor — RuneScape Quest Architecture Study

**Status:** Comparative design research for the narrative architecture package (`04_CONTENT_PRODUCTION/Quests/Caelmor_Narrative_Architecture.md`), 2026-11-02. Structural research only, under Master Protocol §5.4 and the AGENTS.md design-identity guardrail: no RuneScape characters, plots, dialogue, puzzles, quests, or setting are adapted. Titles and counts appear only as citations.

**Dataset access.** The Creative Director's local extraction at `C:\Users\CK\Documents\osrs-db\parsed-osrs` was **not reachable** from this cloud session (no device connection was available when the study ran). The study instead read the public `Flipping-Utilities/parsed-osrs` repository and its committed OSRS quest output, and the OSRS and RS3 wikis through page summaries. Field-level findings below are verified against that public code and sample; RS3 extraction and the NPC, monster, location, and item extractors were not inspected. Wiki figures come from summarized page fetches and are marked as such in the verification notes. If the local dataset is later connected, §1.3 (what relationships the extraction does and does not hold) should be re-checked against it, particularly any RS3 output.

**Edge names are illustrative.** The edge labels used below (`requires`, `continues`, `features`, `echoes`, and the rest) and the suggested CI check are research vocabulary, not a schema or a contract. The architecture's own edge types are in `Caelmor_Narrative_Architecture_Arcs_and_Milestones.md` §6.1; any data model belongs to the Schema & Content Engineer under the Roadmap.

**How the architecture uses this study.** Principles adopted, adapted, or rejected are recorded in `Caelmor_Narrative_Architecture.md` §4.

---

*Design-research memo, compiled 2026-11-02. This is structural research only. RuneScape quest and series titles and requirement counts appear only as citations. Plots, characters, dialogue and puzzles are deliberately left out.*

---

## 0. Executive summary

- Both games tell long-form stories through a **requirement graph**, not a linear campaign. In OSRS, 133 of the 195 quest entries in the public parsed dataset are a prerequisite of at least one other quest. 93 entries need no quest at all. The result is a wide, shallow base under a few very deep capstones.
- **Capstones converge breadth, not depth.** The OSRS grandmaster quests have a transitive quest-requirement chain only **4 to 6 levels deep**, but they draw on **14 to 41 quests** from many unrelated series. Examples: Desert Treasure II has 37 quests plus 4 miniquests; While Guthix Sleeps has 41; Dragon Slayer II has 33; Song of the Elves has 14.
- **Series are the spine; "related" quests are the braid.** The OSRS wiki defines a series as quests that "share a common and continuing plotline". It lists about 24 series, and many quests sit outside any series. Cross-series links are recorded separately as "related" quests, which are thematic links rather than hard requirements.
- **Gameplay gates mirror narrative gates.** Gates come in three kinds: skill thresholds (Song of the Elves needs 70 in eight skills), quest-point thresholds (12 to 343 QP unlock quests, guilds and areas), and world access (diaries and area tasks gate on quests, then unlock travel, gear and areas).
- **Completion structures are retroactive.** In both games the quest cape is unequipped when a new quest ships, which makes "has the player seen the whole story" a live state. RS3 adds a Master quest cape (312 achievements, including lore books and post-quest content), which effectively rewards optional lore.
- **The production lessons are real and documented.** OSRS reworked A Night at the Theatre because the original did not "match what was polled". It had also autocompleted, so players missed its dialogue, yet it was required by the Myreque finale. Series are often left unfinished, with placeholder entries for later parts. Requirement walls hundreds of QP high gate the endgame.
- **What Caelmor should take:** series spines per region, a small number of cross-region braids, capstones that converge on breadth, and gameplay gates with a story reason.
- **What Caelmor should avoid:** QP-total walls, flattened mega-requirement lists, retroactive cape revocation, and autocompleted story content.

---

## 1. Task 1: Is the `parsed-osrs` pipeline publicly findable?

**Yes.** A GitHub repository search for `parsed-osrs` returns **`Flipping-Utilities/parsed-osrs`**, described as "Tools and data from the parsed osrs wiki". It is the only repository whose name matches `"parsed-osrs" in:name`.

The GitHub REST API refused access to this repository in this session (HTTP 403, "access not enabled"), but `raw.githubusercontent.com` served the files. I read these files on branch `main`:

- `README.md`
- `src/modules/app/dev.service.ts`
- `src/modules/extractors/quests.extractor.ts`
- `src/types/quest.ts`
- `src/constants/paths.ts`
- `.gitignore`
- the committed output sample `data/quests/all-quests.json` (3.37 MB, 195 entries)

### 1.1 What the pipeline is

- A NestJS/TypeScript wiki scraper. The README says: "Project to download all of the wiki page, and extract a lot of metadata from it… THIS IS A WORK IN PROGRESS!"
- It dumps wiki page lists and wikitext into a SQLite database (`data/database.sqlite`), then runs one extractor per entity type.
- The extractors listed in `dev.service.ts` are: items, sets, recipes, shops, skill resources, monsters, spawns, prayers, spells, locations, NPCs, scenery, **quests**, activities, news, music and templates.
- `.gitignore` also mentions `wiki-data-rs3/` and `database-rs3.sqlite`, which suggests an RS3 variant exists. I did not verify it.

### 1.2 Exact quest fields (from `src/types/quest.ts`, confirmed in the output sample)

`Quest` fields:

- `name`
- `aliases` (page redirects)
- `number` (commented "release order")
- `members`
- `series` (a raw string such as `"Dragonkin, #3"`)
- `difficulty`
- `length`
- `start` (prose)
- `startCoords?` (`{x,y}`)
- `description`
- `itemRequirements[]`
- `recommendedItems[]`
- `requirements[]` (commented "Skill / quest / combat requirements")
- `enemiesToDefeat[]`
- `ironmanConcerns?`
- `leagueRegion?`
- `questPoints`
- `rewards[]`
- `requiredFor[]` (from `==Required for completing==`)
- `walkthrough?[]` as `{heading, body}`
- `quickGuide?[]` as `{section, itemsNeeded?, steps[]}`
- `image?`, `release?`, `update?`, `developer?`

All of these come from the `{{Infobox Quest}}`, `{{Quest details}}` and `{{Quest rewards}}` templates, plus the section text.

How fields appear in the sample (counts out of 195 entries):

| Field | Present in |
|---|---|
| Core fields | 195 |
| `walkthrough` | 195 |
| `leagueRegion` | 193 |
| `startCoords` | 187 |
| `developer` | 182 |
| `quickGuide` | 138 |
| `ironmanConcerns` | 64 |

### 1.3 Narrative relationships that are **not** present (verified against the code and sample)

- **Requirement edges have no type and no hierarchy.**
  - `requirements[]` is a flat array of cleaned strings. Quest names, skill lines like `"Magic 75 (boostable)"`, `"Quest 200"` (the QP gate), miniquest or activity prose, and header lines like `"Completion of the following quests:"` are all mixed together.
  - The code comment says nested bullets are deliberately flattened: "Each bullet — top-level or nested — becomes its own entry." So **direct versus transitive prerequisites is lost**, and so is requirement depth.
  - There is no "partial completion" flag; a "started X" requirement survives only as prose.
- **`series` is an unnormalised string.** There is no series entity, ordering edge, or "related quests" (thematic) link.
- **No NPC, organisation, faction, deity or location links on quests.** These names appear only inside prose (`start`, `walkthrough`, `description`).
  - The pipeline does have separate NPC and location extractors. I did not read them, and nothing in the quest type references them.
  - The only spatial fields are `startCoords` and `leagueRegion`, which is a Leagues game-mode unlock note rather than a story region.
- **No timeline.** Nothing records an in-world chronology or historical event. `number` and `release` are release order, not story order.
- **No revelation or knowledge model.** Nothing records which facts a quest establishes or which later quests depend on them.
- **Miniquests, diaries, lore books and post-quest content are not linked.**
  - The sample's 195 entries are 184 quests plus 11 Recipe for Disaster sub-entries. No other miniquests appear.
  - So miniquest prerequisites, such as the four that Desert Treasure II needs, disappear when you resolve names against the quest set.
- **`requiredFor[]` is the inverse edge as prose bullets.** Some of those bullets are non-quest unlocks.

**Implication for Caelmor tooling.** The public pipeline is a good source of requirement and series raw strings. Any narrative graph (characters, factions, places, events, reveals, thematic links) would have to be hand-modelled.

---

## 2. Task 2: Verified structural data

### 2.1 Scale and completion structures

| Metric | OSRS | RS3 |
|---|---|---|
| Quests | 184: 24 F2P (46 QP) + 160 members (297 QP) [Quests/List] | "There are currently 277 quests" [List of quests] |
| Max quest points | 343 [Quest point cape; Quest points] | 476, as of 28 Sep 2026 [Quest cape] |
| Quest cape requirement | "completed all quests (excluding miniquests)" | "Complete all quests". Changed on 13 Feb 2023 from max QP to all quests; several miniquests were converted to 0-QP quests to fold them in |
| On a new quest release | Cape unequipped until the new quest is done | Same; the cape goes to inventory or bank |
| Miniquests | Page says 19; its table has 20. They give no QP and no map icon, and none is stated as needed for the cape [Miniquests] | Separate list; some folded into quests in 2023 |
| Higher completion tier | Achievement diary cape (all diaries) [Achievement Diary] | Master quest cape: 312 achievements, covering all quests and miniquests, post-quest rewards, most lore books, and skill minimums (most 90, up to 120). Completionist cape: all quests, all Area Tasks, music, and more |

### 2.2 Quest-point thresholds as gates (OSRS) [Quest points]

| QP | Unlocks |
|---|---|
| 10 | F2P trade |
| 12 | Black Knights' Fortress |
| 16 | Below Ice Mountain |
| 20 | Enlightened Journey |
| 32 | Champions' Guild (and so Dragon Slayer I), Wanted! |
| 43 | Tears of Guthix |
| 55 | Heroes' Guild and Heroes' Quest |
| 100 | Swan Song and an area |
| 107 | Legends' Guild and Legends' Quest |
| 175 | Recipe for Disaster finale (also needs a diary tier) |
| 180 | While Guthix Sleeps |
| 200 | Dragon Slayer II |
| 343 | Cape and an elite diary |
| Every 50 | A Slayer utility slot |

**Pattern.** QP acts as a *proxy for world experience*. It lets designers gate a capstone on "has seen enough of the world" without listing specific quests.

### 2.3 Series (OSRS) [oldschool.runescape.wiki/w/Quests/Series]

**Definition:** quests "recognised to share a common and continuing plotline". Series are ordered by the in-game "Storyline" sort, and unlisted quests are standalone. Entry counts below include upcoming or placeholder entries.

| Series | Entries | Status |
|---|---|---|
| Mahjarrat | 17 | Unfinished; finale is a placeholder |
| Elf | 8 | Finished; capstone Song of the Elves |
| Kourend | 8 | Unfinished |
| Kharidian | 7 | Unfinished; includes a placeholder |
| Myreque | 6 | Finished |
| Dorgeshuun | 5 | Unfinished; includes upcoming |
| Fremennik | 5 | Unfinished; includes upcoming |
| Gnome | 5 | Unfinished |
| Pirate | 5 | Unfinished |
| Troll | 5 | Unfinished |
| Dragonkin | 4 | Unfinished; includes a placeholder |
| Temple Knight | 4 | Unfinished |
| Twilight Emissaries | 4 | Finished |
| Camelot | 3 | Unfinished |
| Order of Wizards | 3 | Unfinished |
| Fairytale | 3 | Unfinished; part III upcoming |
| Tortugan | 3 | Unfinished; finale unnamed |
| Demon Slayer, Elemental Workshop, Miscellania, Rag and Bone Man, Red Axe | 2 each | Mostly unfinished |
| Penguin | 1 | Unfinished |
| Twisted Tales | Anthology | Treated as standalone |

**Cross-links.** The page records "related" quests across series. While Guthix Sleeps is numbered in Mahjarrat but related to Dragonkin and Gnome. Desert Treasure II is numbered in Mahjarrat but related to Order of Wizards. Fremennik is related to Miscellania. In other words, the wiki distinguishes **numbered membership** from **thematic adjacency**.

**Dataset cross-check.** In the parsed sample, 101 of 195 entries have `series = "None"`. Roughly half of all quests are standalone, which makes them the "texture" layer of the world.

### 2.4 Series (RS3) [runescape.wiki/w/Quests/Series]

The page is split into "Standard" and "Seasonal" series. Counts below include miniquests or sagas where the page lists them.

| Series | Entries | Notes |
|---|---|---|
| Desert | 13 | |
| Tales of the Arc | 11 | Includes a miniquest |
| Fremennik | 10 | Plus a separate Fremennik Sagas series of 5 |
| Elf (Prifddinas) | 9 | |
| Myreque | 9 | |
| Doric's Tasks | 8 | Miniquests |
| Gnome | 7 | Last entry dated "Summer 2027" |
| Pirate | 7 | |
| Temple Knight | 6 | |
| Troll | 5 | |
| Cave Goblin | 5 | |
| Dwarf (Red Axe) | 5 | |
| Fairy | 4 | |
| Elemental Workshop | 4 | |
| Thieves' Guild | 4 | Ends in a miniquest |
| Penguin | 4 | |
| Camelot | 3 | |
| Ogre | 3 | |
| Void Knight | 3 | |
| Ozan | 3 | |
| TzHaar | 3 | |
| Boric's Tasks | 3 | |
| Others | 2 each | Includes "Ariane" and "Wise Old Man" |

**Also listed but not counted:** Violet Tendencies, Mahjarrat Mysteries, Sliske's Game, The Elder God Wars, Legacy of Zamorak, Fort Forinthry, The First Necromancer, City of Um, Sanguine, plus three seasonal series. The fetch was truncated before these, and their individual pages returned errors.

**Structural observations:**
- RS3 has more series per region.
- It has **character-anchored series**, named after a mentor or NPC rather than a place (Ariane, Ozan, Wise Old Man, Odd Old Man).
- It has **miniquest-only series**.
- It has **seasonal series**, which are event content.
- It has an explicit **saga** format.

### 2.5 Capstone requirement structure

Where the wiki shows only flat lists, I computed depth and direct-requirement counts from the parsed dataset. The method: build the transitive closure over quest names, then take its transitive reduction. Miniquests are excluded, so these figures are lower bounds.

| Capstone | Skill gates (to start) | Wiki-listed requirements | Transitive quests (dataset) | Direct after reduction | Max depth |
|---|---|---|---|---|---|
| OSRS **Desert Treasure II** (GM, Mahjarrat #14, 2023) | FM 75, Mag 75, Thiev 70, Herb 62, RC 60, Con 60 | 41 unique, including 4 miniquests | 37 | 6 | 6 |
| OSRS **While Guthix Sleeps** (GM; 180 QP) | (7 in dataset) | not fetched | 41 | 10 | 4 |
| OSRS **Dragon Slayer II** (GM, Dragonkin #3, 2018) | 200 QP; Mag 75, Smith 70, Mine 68, Craft 62, Agi 60, Thiev 60, Con 50, HP 50 | 33 quests + 100 Kudos + a partial miniquest | 33 | 7 | 4 |
| OSRS **Song of the Elves** (GM, Elf #8 finale, 2019) | 70 in Agi, Con, Farm, Herb, Hunt, Mine, Smith, WC | 14 | 14 | 3 | 6 |
| OSRS **Recipe for Disaster** (multi-part) | 14 skill lines; finale needs 175 QP | not fetched | 35 | 16 | 2 |
| OSRS **The Blood Moon Rises** (GM, Myreque finale) | 10 skill lines | not fetched | 10 | 2 | 6 |
| RS3 **Sliske's Endgame** (GM, Sliske's Game #15, 2016) | none listed | 18 distinct, flat, several marked "…" (further prerequisites); plus Ancient Cavern access | n/a | n/a | n/a |

**Two capstone shapes:**

- **Deep spine.** Song of the Elves and The Blood Moon Rises have 2 to 3 direct requirements, depth 6, and a small transitive set. The prerequisite set *is* the series.
- **Wide convergence.** Desert Treasure II, While Guthix Sleeps and Dragon Slayer II have 6 to 10 direct requirements, depth 4 to 6, and 33 to 41 transitive quests. Desert Treasure II's six direct parents come from at least three different series or regions. Recipe for Disaster is the extreme case: 16 direct parents at depth 2, a pure "tour of the world".

**Hub quests** (OSRS dataset, number of quests that transitively require each):

| Quest | Required by |
|---|---|
| Priest in Peril | 33 |
| Druidic Ritual | 29 |
| The Restless Ghost | 24 |
| Rune Mysteries | 23 |
| Jungle Potion | 23 |
| Shilo Village | 16 |
| Lost City, Troll Stronghold, Death Plateau | 15 each |

These are mostly short, early quests that act as **regional keys**: they open an area or a skill, or they introduce an organisation.

### 2.6 Diaries and area tasks

- **OSRS Achievement Diaries.**
  - 12 areas with 4 tiers each, giving 48 tiers and 492 tasks [Achievement Diary].
  - Tasks can be done in any order, but a tier's reward needs all lower tiers of that area.
  - Rewards are an equippable item, a lamp, and area perks or access.
  - Tasks carry quest requirements, and elite tiers carry heavy ones. The fetched summary said "all quests"; I did not verify that wording.
- **RS3 Area Tasks.**
  - 13 areas with Beginner (Lumbridge only), Easy, Medium, Hard and Elite tiers [Area tasks].
  - Each tier lists required quests (Beginner Lumbridge needs The Restless Ghost) and skills.
  - Rewards are area equipment sets.
  - Completing all of them unlocks an achievement and an emote.
- **Structural role.** Diaries are a *regional completion layer*. They tie exploration and skill use to quest completion inside a region, and they pay out mobility or gear that eases further exploration there.

### 2.7 Optional lore versus mandatory chains

- **Miniquests** give no QP, are not cape-required in OSRS, and are lightly signposted. However, some are hard prerequisites of grandmasters: four for Desert Treasure II, and a partial miniquest plus Kudos for Dragon Slayer II.
- **RS3** formalised optional lore as completion content. The Master quest cape requires most lore books (achievement categories "Lore→Books/Experience") and all post-quest rewards. Lore stays optional for *progression* but is required for *prestige*.
- **Autocomplete hazard.** A Night at the Theatre originally autocompleted, so players missed its dialogue, yet it was required for the Myreque finale. The rework made it a real quest and added Taste of Hope as a requirement [Update: A Night At The Theatre Rework].

---

## 3. Task 3: Structural analysis

### (a) Independent regional and faction questlines

- Most OSRS series are named for a **people or place**: Elf, Gnome, Troll, Fremennik, Kourend, Kharidian, Myreque, Dorgeshuun, Tortugan. A few are named for an **organisation**: Temple Knight, Order of Wizards, Camelot.
- RS3 adds **mentor-NPC series**: Ariane, Ozan, Wise Old Man.
- Each regional series starts with a low-requirement entry. In the dataset, 93 of 195 quests need no quest at all. So a player can enter any region's story independently, and regions stay readable without cross-knowledge.
- **Strength:** parallel production, with regional teams or eras shipping series independently.
- **Weakness:** series stall. Most OSRS series are marked "Unfinished", and several have placeholder finales.

### (b) Major chains with escalating revelations

- Long series (Mahjarrat at 17 entries; RS3 Desert at 13, Tales of the Arc at 11, Sliske's Game at 15 or more) escalate **in stakes and in difficulty tier together**. In OSRS the difficulty ladder runs Novice, Intermediate, Experienced, Master, Grandmaster. In the dataset the counts are 46, 79, 35, 18 and 6, plus 11 "Special".
- Revelations are released across years, and early entries are cheap. That makes the **early entries do double duty**: they are tutorials for a region and setups for payoffs a decade later.
- No formal "revelation" data exists in the sources I fetched. Escalation is visible only through ordering and difficulty.

### (c) Recurring characters, locations, organisations and historical events

- The series page's **"related quests"** columns are the explicit record of cross-series recurrence. One example: a Mahjarrat-numbered quest is related to Order of Wizards.
- RS3's naming of series after recurring NPCs (Ariane, Ozan, Wise Old Man, Sliske) makes **the character itself the through-line** across regions.
- Organisations recur as hubs. For example, the guild quests are gated at 32, 55 and 107 QP, and these serve as story-and-prestige milestones.
- No fetched source formalises historical events. That is consistent with the parsed-osrs gap noted in §1.3.

### (d) Prerequisites versus thematic links

The games use at least four distinct relation types:

1. **Hard quest requirement.** Must be Completed.
2. **Partial requirement.** "Started the X portion of…", as in Dragon Slayer II's Barbarian Training line. RS3 area tasks mark some quests as "partial".
3. **Aggregate gate.** A QP threshold, a skill threshold, Kudos, or diary tiers.
4. **Thematic link.** "Related quests" on the series page, which carry no mechanical dependency.

**Lesson:** the deep-spine capstones (Song of the Elves) rely on type 1 inside one series. The convergence capstones (Desert Treasure II, Dragon Slayer II) use type 1 across series *plus* type 3. That is where requirement walls come from.

### (e) Gameplay progression tied to narrative progression

| Lever | How it ties to story | Evidence |
|---|---|---|
| Skill gates | Capstones demand broad skill levels: 70 in eight skills for Song of the Elves; six skills from 60 to 75 for Desert Treasure II | Quest pages |
| QP thresholds | Narrative milestones double as guild and area keys | Quest points page |
| World access | Hub quests (Priest in Peril, Druidic Ritual, Lost City) open regions or skills; Dragon Slayer II rewards travel infrastructure | Dataset hubs; DS2 page |
| Encounters | Grandmasters unlock repeatable bosses (Desert Treasure II: four bosses), so story completion becomes endgame access | DT2 page |
| Regional completion | Diary and area-task tiers require quests and pay out regional mobility | Diary and area-task pages |

### (f) Optional stories that enrich without mandatory exposition

- About half of OSRS quests are standalone (`series = None`). They supply world texture and are sometimes pulled into capstones as prerequisites.
- **Miniquests** are low-signpost side content. They are usually optional, but occasionally a hidden hard gate. Making them a hard gate is a known pain point, since they are invisible in QP terms.
- **RS3 lore books and post-quest content** are optional for progression but required for the Master cape.

### Weaknesses and production lessons (observed)

1. **Requirement walls.** A 200-QP start gate plus 33 quests for Dragon Slayer II. The flat lists of 41 or more items on the wiki are how players actually experience it.
2. **Retroactive invalidation.** Quest capes are unequipped whenever a quest ships, and RS3 redefined "all quests" in 2023. Completion is never stable.
3. **Autocomplete and rework debt.** A Night at the Theatre's original autocomplete meant players skipped its story, even though it was load-bearing for a finale. Fixing it required a rework and a retroactive replay.
4. **Stalled series.** Placeholder finales exist in Mahjarrat, Dragonkin, Kharidian and Tortugan, and most series are "Unfinished".
5. **Out-of-order discovery.** Because 93 or more quests are entry points and capstones converge from many series, players reach late revelations through unrelated paths. Release order (`number`) is not story order.
6. **Opaque gates.** Miniquests and partial-progress requirements are hidden from QP accounting but still block capstones.
7. **Two-decade continuity drift** (general knowledge, not verified this session). RS3 in particular has reworked or retconned older quests to fit later lore.

---

## 4. Task 4: Distilled design principles for Caelmor

**Caelmor context:** four regions released over time, handcrafted content, strong continuity, quest states Inactive/Active/Completed only (no failing or abandoning), solo-first.

### 4.1 Reusable principles (13)

1. **Every region has a low-requirement entry quest.**
   - *Source:* 93 of 195 OSRS quests need no quest at all.
   - *For Caelmor:* each region's first quest is Inactive and becomes Active from in-region discovery alone, so a late-released region is never locked behind old content.
2. **A small set of "key" quests per region.**
   - *Source:* hubs such as Priest in Peril (33 dependants) and Druidic Ritual (29) introduce a place, skill or organisation that many later quests reuse.
   - *For Caelmor:* designate 1 or 2 keystone quests per region and keep them short and evergreen.
3. **Separate numbered series membership from thematic links.**
   - *Source:* the wiki's "related quests" versus series numbering.
   - *For Caelmor:* the data model gets distinct edge types, `requires` and `continues` as hard links versus `echoes` and `features` as soft links. Only hard edges affect state.
4. **Deep spines for regional arcs, wide convergence only for cross-region capstones.**
   - *Source:* Song of the Elves (depth 6, 3 direct) versus Desert Treasure II (6 direct across series, 37 transitive).
   - *For Caelmor:* regional finales require only their own series. A cross-region capstone requires each region's finale plus a few named side quests, never dozens.
5. **Cap requirement breadth explicitly.**
   - *Source:* the 33 to 41 transitive prerequisites are the main OSRS complaint vector.
   - *For Caelmor:* set a budget such as at most 4 direct and about 12 transitive prerequisites for the largest capstone, shown as a readable tree rather than a flat list.
6. **Gameplay gates need an in-fiction reason.**
   - *Source:* skill gates on capstones work when the skill is used in the quest.
   - *For Caelmor:* every skill or exploration gate maps to a scene that uses it. Avoid abstract aggregate thresholds.
7. **Use world access as the reward for story progress.**
   - *Source:* Dragon Slayer II travel infrastructure; diary mobility perks.
   - *For Caelmor:* Completing a quest unlocks routes, shortcuts or regions. This is the most natural fit for a 3-state model, since it is a one-way door.
8. **Regional completion layer.**
   - *Source:* Diaries and Area Tasks (4 or 5 tiers per region, quest-gated, mobility rewards).
   - *For Caelmor:* a per-region "deeds" layer that reflects which quests, places and encounters the player has completed, with no failure states.
9. **Design early quests as setup for later payoffs.**
   - *Source:* long series escalate across years.
   - *For Caelmor:* each region's early quests should seed 1 or 2 facts that a later region pays off. Track these as explicit "established fact" nodes, which RuneScape's data lacks.
10. **Recurring characters as cross-region braids.**
    - *Source:* RS3 mentor-named series (Ariane, Ozan).
    - *For Caelmor:* 2 to 4 travelling characters whose arcs span regions, each appearance a separate quest with soft `features` links. They should be hard-linked only at the capstone.
11. **Optional lore is rewarded but never required for comprehension.**
    - *Source:* RS3 Master cape lore books; OSRS standalone quests.
    - *For Caelmor:* lore finds and side stories feed a codex or prestige layer. Mandatory chains must stand alone.
12. **Escalate difficulty and stakes together.**
    - *Source:* the Novice-to-Grandmaster ladder tracks series progression.
    - *For Caelmor:* within each regional spine, encounter difficulty and revelation weight rise in step.
13. **Encounters as post-story access.**
    - *Source:* Desert Treasure II unlocking four repeatable bosses.
    - *For Caelmor:* completing a story turns its climax area into revisitable solo content. This gives Completed a gameplay meaning without adding states.

### 4.2 Graph structures

**1. Hub-and-spoke regional series**
- *Nodes:* a keystone quest (hub), series quests, and standalone quests within the region.
- *Edges:* `requires` from spokes to the hub; `continues` along the series.
- *Use:* the default shape for each Caelmor region.
- *RuneScape analogue:* Priest in Peril into Morytania and the Myreque series.

**2. Deep linear spine (finale-terminated)**
- *Nodes:* series quests 1 to N.
- *Edges:* `continues` with `requires` along a single path, plus at most 1 or 2 side entries.
- *Use:* each regional main arc. Depth up to about 6 is fine because each step is in the same region and story.
- *RuneScape analogue:* the Elf and Myreque series.

**3. Braided cross-region threads**
- *Nodes:* quests in different regions sharing a recurring character, organisation or event.
- *Edges:* soft `features` or `echoes` links between them; optional `requires` only where an established fact is genuinely load-bearing.
- *Use:* stitching regions released at different times. A thread can be extended when a new region ships without touching old quests.
- *RuneScape analogue:* "related quests" across series; RS3 NPC-named series.

**4. Capstone convergence (bounded breadth)**
- *Nodes:* the capstone, each region's finale, and a small number of named side quests.
- *Edges:* `requires` from the capstone to K finales (K at most 4), each finale having its own spine beneath it.
- *Use:* a world-level climax once all four regions exist.
- *Explicitly reject:* the OSRS form of 6 to 16 direct and 33 to 41 transitive parents plus a QP threshold.

**5. Regional completion lattice (diary-like)**
- *Nodes:* tier nodes per region, plus deeds (quests, places, encounters).
- *Edges:* `counts_toward` from deeds to tiers; tier-to-tier ordering.
- *Use:* exploration, skill and quest integration without exposition. Rewards are traversal or utility.

**6. Satellite lore cloud**
- *Nodes:* optional lore items and short side stories.
- *Edges:* `illuminates` pointing at spine quests or facts, read-only, never `requires`.
- *Use:* depth for completionists, with zero gating.

### 4.3 Production lessons

| RuneScape lesson | Caelmor translation |
|---|---|
| Stalled series and placeholder finales | Plan each regional spine to completion before release. Ship a region's arc as a closed set; extend only through braids. |
| Autocompleted content later load-bearing (A Night at the Theatre) | Never autocomplete story quests. If a quest must be skippable, carry its key facts forward in the next quest's Active entry. |
| Retroactive cape revocation, redefinition of "all quests" | Completion badges are per region and per release. A new region never revokes an old badge. |
| Release order differs from story order | Keep an authored in-world chronology separate from release order, and validate continuity against it at each region release. |
| Hidden gates (miniquests, partial steps) | Every prerequisite must be a visible quest in the 3-state model. No hidden "started X" or partial-progress gates. |
| The pipeline loses typed edges and depth | Author the narrative graph natively with typed edges (`requires`, `continues`, `features`, `echoes`, `establishes_fact`, `unlocks_access`), and CI-check depth and breadth budgets. |
| Two-decade continuity drift and reworks | Write a lore bible per region before content lock; do a canon review when each new region is planned. |

### 4.4 What NOT to copy

- **QP-total gates.** "Has done enough quests" without saying which. This conflicts with handcrafted continuity and solo pacing.
- **Flat mega-requirement lists** (33 or more quests, plus Kudos, plus a partial miniquest).
- **Wide skill walls on story content** (70 in eight skills). They gate the narrative behind unrelated grinds.
- **Retroactive invalidation of completion rewards** whenever a region ships.
- **Fail-and-retry or abandonment structures.** These are not needed and are incompatible with the 3-state model, so the RuneScape mechanics that rely on them are left out of this study.
- **Placeholder or open-ended series** with no planned finale.
- **Miniquests as hidden hard gates.**
- **RuneScape's specific content.** None of its characters, factions, plots, places or puzzles should be borrowed; only the structures above.

---

## 5. Sources

**Repository (parsed-osrs):**
- https://github.com/Flipping-Utilities/parsed-osrs (found by GitHub search; read through raw.githubusercontent.com)
- https://raw.githubusercontent.com/Flipping-Utilities/parsed-osrs/main/README.md
- https://raw.githubusercontent.com/Flipping-Utilities/parsed-osrs/main/src/modules/app/dev.service.ts
- https://raw.githubusercontent.com/Flipping-Utilities/parsed-osrs/main/src/modules/extractors/quests.extractor.ts
- https://raw.githubusercontent.com/Flipping-Utilities/parsed-osrs/main/src/types/quest.ts
- https://raw.githubusercontent.com/Flipping-Utilities/parsed-osrs/main/src/constants/paths.ts
- https://raw.githubusercontent.com/Flipping-Utilities/parsed-osrs/main/data/quests/all-quests.json

**OSRS Wiki:**
- https://oldschool.runescape.wiki/w/Quests/Series
- https://oldschool.runescape.wiki/w/Quests/List
- https://oldschool.runescape.wiki/w/Quest_point_cape
- https://oldschool.runescape.wiki/w/Quest_points
- https://oldschool.runescape.wiki/w/Miniquests
- https://oldschool.runescape.wiki/w/Achievement_Diary
- https://oldschool.runescape.wiki/w/Dragon_Slayer_II
- https://oldschool.runescape.wiki/w/Song_of_the_Elves
- https://oldschool.runescape.wiki/w/Desert_Treasure_II_-_The_Fallen_Empire
- https://oldschool.runescape.wiki/w/Update:A_Night_At_The_Theatre_Rework

**RuneScape Wiki (RS3):**
- https://runescape.wiki/w/Quests/Series
- https://runescape.wiki/w/List_of_quests
- https://runescape.wiki/w/Quest_cape
- https://runescape.wiki/w/Master_quest_cape
- https://runescape.wiki/w/Completionist_cape
- https://runescape.wiki/w/Area_tasks
- https://runescape.wiki/w/Sliske%27s_Endgame
- https://runescape.wiki/w/Transcript:RuneScape_in_2019_-_an_introduction (checked; only marginally relevant)

## 6. Verification notes

- **Fetched and read directly:**
  - Every parsed-osrs file listed above. Field names in §1 are quoted from `src/types/quest.ts` and `quests.extractor.ts` and checked against the output sample's key counts.
  - The GitHub API returned 403 for the repository itself. The search API and raw file hosting worked.
  - I did **not** read the NPC or location extractors, nor any RS3 variant.
- **Wiki pages:**
  - Direct curl to the MediaWiki API was refused by the egress proxy (connect_rejected), so every wiki page was read with WebFetch.
  - WebFetch returns a model-generated summary of the page, and long pages were cut off at about 100k characters.
  - Figures from those summaries are as reported, not hand-checked against wikitext. Specifically: series counts, the 184/343 OSRS totals, 277 quests and 476 QP for RS3, capstone skill gates and requirement lists, QP thresholds, diary and area-task structure, and the Master cape's 312 achievements.
  - Known inconsistencies:
    - The OSRS Miniquests page says 19 but lists 20.
    - The RS3 Quests/Series page was truncated, so the Mahjarrat Mysteries, Sliske's Game and Elder God Wars counts were not obtained. Their individual pages returned client errors.
    - The claim that "elite diary tasks require completing all quests" came from a summary and is unverified.
- **Computed by me** from `all-quests.json` (a snapshot of 2026-11-02 that includes quests released through September 2026):
  - Transitive and direct prerequisite counts, depths, hub counts, standalone counts, and the difficulty and length distributions.
  - These are matched on quest names only, so they **exclude miniquests and non-quest gates** and are lower bounds. Desert Treasure II's wiki list of 41 equals the dataset's 37 plus the 4 miniquests that are absent from the dataset.
  - The "direct" counts come from a transitive reduction, not from the wiki's nesting, which the pipeline does not keep.
- **General knowledge, not verified this session:**
  - That RS3 has reworked or retconned older quest lore over two decades.
  - The characterisation of RS3 "sagas" beyond their presence on the series page.
  - Player-sentiment claims about requirement walls. These are inferred from the requirement data but not sourced.
