# Caelmor Creative Readiness Assessment

Nov 1, 2026 · @Collin

## Verdict

Caelmor's world foundation is coherent, original in its premise, and ready to build on, but nothing in the repo is yet playable as narrative. The lore has been reconciled into one causal history with clear magic rules. The Lowmark main arc has a sound architecture. But there are no quests, no dialogue, no voice guide, and no main-arc antagonist, and Lowmark has only 7 named characters, while Emberholt, which doesn't ship in v1, has 50.

The repo has spent its creative effort on getting the world right. The next phase needs to go into making Lowmark playable: the people, the words, and the moments the player will remember.

| Area | Readiness | Why |
| --- | --- | --- |
| Lore consistency | Ready, with a cleanup pass | C01–C16 are reconciled in live canon; about 11 smaller contradictions remain (see below) |
| World identity and theme | Ready | A postwar world 30 years on, elements tied to civic duty, and a rule that the supernatural can't testify |
| Lowmark places and culture | Partly ready | The dossier is rich, but its subzones disagree with Phase 1.5 and there is no POI-level map |
| Factions | Partly ready | The Remnant is deep; Lowmark's noble rivalry has only one named house |
| Characters (v1) | Not ready | 7 Lowmark anchors; the Last Field-Mage, the Act III figure, has no character entry |
| Main arc | Partly ready | 12 movements in 3 acts; no antagonist, boss, player stake, or reward |
| Side quests | Partly ready | 20 candidates; about 12 resolve through records, tallies, or hearings |
| Mystery and environmental storytelling | Partly ready | Excellent truth/belief controls; the dossier's strangest hooks were dropped from planning |
| NPC dialogue and voice | Not ready | No voice bible, dialogue schema, or sample lines |
| Authored quest content | None | `02_VERTICAL_SLICE/*` and `04_CONTENT_PRODUCTION/Quests` hold only `desktop.ini` |

## Canon status map

Very little of the narrative material is approved canon. Out of about 40 narrative reference documents (roughly 600 KB), only the reconciled `LORE/` files and Phase 1 hold canon authority. Everything in `00_ADMIN/Reference/Caelmor_Part2…Part6_*` and `Caelmor_Regional_Source_Process_*` says in its first lines that it is a proposal or an audit.

| Status | What it covers | Evidence |
| --- | --- | --- |
| **Approved canon** | Phase 1 vision, pillars, scope, content strategy | `00_ADMIN/Roadmaps/Caelmor_Roadmap.md` Stage 1 marked LOCKED |
| **Approved canon** | D01–D07 clusters, C09 layered water model, C16 retirement of "Long War", Director rulings C01–C15 | `Caelmor_Canon_Reconciliation_Audit.md` ("performed after approval of D01–D07…") |
| **Approved canon (reconciled text)** | Timeline, War History, Factions, four regional dossiers, merged overview, four character anchor files | Same audit, files 1–13; contradiction sweep marked PASS |
| **Pending approval** | Lore Foundation Lock itself | `Caelmor_Final_Lore_Foundation_Lock_Review.md` ends "READY FOR CREATIVE DIRECTOR APPROVAL"; no later file records the approval, although equipment/economy work started the same day (git log, 2026-09-19) |
| **Deliberately deferred** | C03 precursor name and Remnant transition; C06 Volkhari population; C07 Founder roster; S01 v1 ranged scope; the Lowmark main-arc antagonist; institution powers; map geometry | Decision Sheet §2, Reconciliation Audit "Intentionally deferred facts" |
| **Proposal pool (not canon)** | Seven-year campaign spine, named customs and sites (Drowsebank, Nine Stakes, Bridge of Seven Repairs, Half-Name Wall), the 12 historical braids, the side-story slate, mystery candidates, callbacks, future-region briefs, all regional source/process briefs | Decision Sheet §3; each file's Status line |
| **In-world belief only** | "Magic was outlawed", the Summit's Stonebound guardian, the General as a returned commander, Chapel Shades as souls, single-Founder hero stories, Glassed Hollow as a forge collapse | Decision Sheet §3 |
| **Rejected or superseded** | Great War 150+ years ago, prewar Dreamers, Volkhari Fire Titan, captive Kaelith, spirit as a fifth element, universal magic ban, speaking Stonebound, literal undead in the Mire, non-Lowmark v1 regions, legacy resource lists as catalogs | Decision Sheet §4 |
| **Missing** | Quest scripts, dialogue, NPC rosters for Lowmark, named antagonist, player-character origin, the actual quest/NPC/dialogue schemas | `02_VERTICAL_SLICE/*` and `04_CONTENT_PRODUCTION/Quests` contain only `desktop.ini`; Roadmap Stages 31.3, 31.5, 34, 35 all unchecked |

One naming caution: the Reconciliation Audit says D01–D07 were approved, but the Decision Sheet that defines them still reads "does not make any choice." The Decision Sheet was never updated to record the outcome, so a new collaborator reading it alone would think nothing has been decided.

## Lore consistency and unresolved contradictions

The reconciliation pass worked. A search of `LORE/` and `01_PRE-PRODUCTION/` found no "Long War", 150-year war dates, fifth-element spirit, or universal magic ban outside text explicitly framed as belief. The issues below are what remains. None is large, but together they will mislead a writer who reads the files cold.

| # | Contradiction | Where | What needs deciding |
| --- | --- | --- | --- |
| 1 | How much the Flameward Speaker knows | `LORE/Regions/Caelmor_Region4_EmberholtHeights.md` §IV ("Privately, he fans the flame"); `LORE/Factions/Caelmor_Factions.md` §VII.A ("compliant Remnant instrument") vs §5 ("unknowingly") and the Emberholt character file #1 ("does not know the full scope") | Knowing conspirator or manipulated believer |
| 2 | Whether the Remnant authored civic embercraft | Factions §19 ("Remnant rebuilt this tradition into a civic embercraft doctrine") vs War History §V and §VII (public embercraft is ordinary; the Remnant "is not the universal cause") | Narrow the Factions line |
| 3 | Whether the player is special or prophesied | Emberholt characters #12 Serix Arden (visions "centered on the player"), #13, #17 ("identify the player early as someone special") vs Core Vision §6 ("ordinary wanderer") and the Dreamer evidence rule | Remove or frame as manipulation |
| 4 | Lowmark–Thornfell relations | Factions §VII.D ("mutually respectful… envies Lowmark's calm politics") vs Lowmark dossier §XIII ("respectful but strained") and §II (fractured noble claims) | Pick one |
| 5 | Lowmark subzones | Phase 1.5 §2.2 (Greyharrow Heartlands, Brackenford Woods, Ashenstead Fields, Riverglass Banks) vs dossier §IV (Whisperflow Run, Floodplain Orchards, Ashen Flats, Crestbridge Crossing, Stillwater Fen, Veilwater Falls). Brackenford Woods appears in no lore file | One subzone list |
| 6 | Two hidden Riverwarden places | Dossier §IV.6 Veilwater Oasis (home of the Riverwardens and the Field-Mage) vs §V.5 Warden's Hearth (archives and the Field-Mage's training pools) | Same place or two |
| 7 | Peoples with no ancestry canon | Dwarves (Lowmark §II, §XII; Thornfell anchor Kaldren) and Field Goblins (Lowmark §VIII); Timeline §I names only humans, "older peoples", and Volkhari; Factions calls Volkhari "dragonkin hybrids" | Which peoples exist, and are goblins in tone |
| 8 | Stale text in proposals | Main Arc movement 7 and Side Lattice "Source limits" say C09 "remains open" (it was approved); Phase 1.5 §8.1 still says "Water-magic arc"; Main Arc cites "Phase 1's symbolic magical artifact", which Phase 1.3 §7 no longer says | Editorial fix |
| 9 | Staff as reward | Lowmark §V.1 smugglers' cellar "anchors a quest chain about… staff acquisition" vs §XV ("not an approved v1 reward") | Remove the hook |
| 10 | "Dormant" Mire magic | Factions §23 and Mire dossier §XIX.1 ("Magic Must Remain Dormant") alongside two active major threats | Clarify: no practitioners, not no phenomena |
| 11 | Decision record | `Caelmor_Creative_Director_Canon_Selection_Decision_Sheet.md` still reads as undecided; the Lore Lock is "ready for approval" with no recorded approval | Record outcomes |

One smaller inconsistency: the Lowmark dossier gives the Last Field-Mage "his cloak" (§XI), while the Main Arc uses "they". That is fine if it's intentional, but it should be a choice.

## World identity, atmosphere, originality, and thematic cohesion

Caelmor has a genuine identity: a world 30 years after a short, catastrophic war that everyone over 40 remembers, where each element is bound to a civic duty rather than a power fantasy. Three choices make it distinctive.

- **The war is recent.** The 5–10-year Great War ended about 30 years ago (`LORE/Timeline/Caelmor_Timeline.md` §V), so veterans, refugees, and their grown children are the population. Most fantasy RPGs put their catastrophe centuries back.
- **Elements are obligations.** Water means shared duty, air means access and shelter, earth means testimony, and fire means useful heat with accountability (Decision Sheet D03). That gives every region a moral question, not just a palette.
- **The supernatural cannot testify.** Wraiths, Stonebound, and Dreamers cannot name the dead or settle guilt (War History §VI). This reverses the "ghost tells you who did it" convention and is the most original rule in the canon.

Lowmark's atmosphere is strong: a bell silent since the armistice, wells that taste sweet, fog that thickens after arguments (Lowmark dossier §III, §XI). It fits Pillar C and Tenet 15 well.

### Risks to the identity

1. **Emberholt reads like a different game.** Its cast has "molten-amber eyes", "skin like cracked basalt", secret inner circles, a "Perfect Flame" project, and a "mana-surge" (Emberholt character file #1, #5, #13). That is dark-fantasy court intrigue next to Lowmark's quiet realism. It needs a tone pass before Emberholt is produced.
2. **Canon now reads like legal text.** After repeated reconciliation, much of the live canon is a list of what is unresolved (Timeline §VIII; Factions keeps its "Canon Fix" and "Correction" notes inline). That is correct but uninspiring source material for writers.
3. **Mythic wonder is underused.** The Forgotten God appears in Timeline §I and in one character's beliefs, and nowhere else. Lowmark has no described faith beyond "understated faith in simple work" (§III). The vision promises "mythic"; the canon mostly delivers "grounded".
4. **Names collide.** Kaelith, Kaelen, Kalen the Ashwalker, and Kael'Vorra; Thalos, Cael'Thalos, Thalan, and Thaliax; "Hearthveil" is both a Remnant division and the Ember-Priestess's surname; Thalan Veyr and Deepbrand engineer Kharos Veyr share a surname. Compounds such as Ashfall, Deepbrand, Cinderwall, and Emberholt also lean generic.
5. **The evidence rule can flatten payoffs.** If every mystery ends with "the record is incomplete", players lose the satisfaction of a reveal. The main arc needs at least a few moments where the truth lands cleanly.

## Regions, history, factions, and characters

History and regional identity are the strongest material in the repo; v1's cast and Lowmark's factions are the weakest. The creative investment runs opposite to the release plan.

**History.** The Timeline and War History give a single causal chain from the Mythic Age to the present, with each region's wartime role tied to its civic duty (War History §IV). The Part 4 Shared Events proposal adds civilian evidence chains. This is ready.

**Regions.** All four dossiers are 26–28 KB with settlements, social roles, enemy ecology, myths, and quest frameworks. Lowmark has 5 settlements, 6 subregions, 5 named social roles (Flow-Menders, Crestbridge Keepers, Wraithwatchers, Glasswrights, Watergarden Keepers), and about 15 enemy types. That is enough for one region. The regional source/process briefs now explain how ordinary life works economically.

**Factions.** The Remnant has four divisions with named leaders. Lowmark has two factions, the Shadeweavers and the Lensemasters, with no named members (Factions §15). The dossier's "primary political question" is "which family truly should rule Lowmark" (§II), but only House Fenmere is named anywhere.

**Characters.**

| Region | Named characters | Ships in v1 | Source |
| --- | --: | --- | --- |
| Lowmark | 7 + 1 rumored | Yes | `LORE/Characters/Caelmore_Characters_Region1_Lowmark_Anchors (Not Full List).txt` |
| Thornfell | 9 | No | `…Region2_Thornfell_Anchors (Not Full List).txt` |
| Mire | 8 | No | `…Region3_Mire_Of_Fallen_Banners_Anchors (Not Full List).txt` |
| Emberholt | 50 | No | `LORE/Characters/Caelmor_Characters_Region4_Emberholt.txt` (59 KB) |

The seven Lowmark anchors (Aldric Fenmere, Maelin Rowe, Corvin Tath, Lessa Mirepath, Joric Fen, Annelise Reed, Tovin Pell) are well conceived. Each has a private weight and a hook, and Tovin as the "quiet anomaly witness" is a lovely device. But the main arc and 20 side stories lean on these seven repeatedly, and the Part 4 Character Ledger forbids giving them ages, kinship, wartime service, or travel. That protects canon but leaves them thin.

Characters that v1 needs and the repo lacks: the Last Field-Mage (no character entry in any file), any Riverwarden, the main-arc antagonists, a rival noble house, and a named Wraithwatcher, Flow-Mender, Lensemaster, Shadeweaver, and Crestbridge Keeper.

## Narrative depth, mysteries, and environmental storytelling

The mystery controls are excellent, but the planning layer has filtered out most of the wonder the canon already contains.

**Mystery discipline.** `Caelmor_Part5_Long_Form_Mystery_and_Reveal_Ledger.md` tracks six threads. Each has an author truth, a public belief, the evidence a player can observe, a plausible wrong reading, what is withheld, and who owns the reveal. Only Thread 1 (Lowmark's water wounds) pays off in v1, which is the right scope. This is a professional authoring tool and should be kept as the template for every substantial mystery.

**Lost hooks.** The Lowmark dossier §XI lists ten evocative secrets. None of the following appears in any Part 5 planning file (a search of all `Caelmor_Part5_*.md` and the Part 3 Lowmark proposal):

- the Uphill Canal, where water seems to forget gravity when unobserved
- the Twice-Burned Tree, whose fruit causes intense dreams
- the Whispering Door that creaks before Wraith attacks
- the Flood Calendar Stones that predict floods better than modern charts
- the Riverwarden Lullaby heard in the reeds
- the Hidden Ledger pages surfacing in markets
- the Hollowed Current, Wraith Lords, and Wraithwatchers Gone Wrong from the enemy ecology (§VIII)
- the Brookhollow smugglers' cellar and the Shadeweavers

Instead, the ten optional discoveries in `Caelmor_Part5_Environmental_Optional_Discovery_Framework.md` are lunch tallies, a polite cup, a handprint, a knot, and similar humane details. Its own tone guidance asks for only "one or two bounded uncanny observations". For a game whose Core Vision lists Wonder as the first emotional beat (§6) and calls itself discovery-driven, that ratio is too low.

**Environmental storytelling.** Phase 1.5 §2.3 asks for 15–20 environmental storytelling elements and §3 asks for 24–32 POIs. The dossier plus the framework's place palette supply more than enough candidates. What blocks them is placement: the only map is `LORE/Regions/Caelmor_Map_Concept.png`, which the Part 4 Map Audit says cannot support routes or sites, and the POI catalog (Roadmap 32.6) is unstarted.

## Quest foundations and memorable-story opportunities

The main arc's structure is sound and fits Phase 1, but it is missing the parts that make a quest line feel like a game: a face to oppose, a fight to build toward, and a reason the player personally cares.

### Main arc (`Caelmor_Part5_Lowmark_Main_Arc_Architecture.md`)

Strengths: 12 movements across 3 acts fit Phase 1.5's 10–14-step envelope. The thesis is strong: a present human decision, damaged postwar waterworks, and real but bounded resonance combine at Stillwater Fen. The Last Field-Mage as "a limit, not an answer" (movement 8) avoids the mentor-grants-power cliché.

Gaps:

1. **No antagonist.** The "coalition of local profiteers and frightened officials" stays "role-based until the Director selects its social placement" (movement 4). Writers cannot draft a single scene of Acts I or III without this.
2. **No boss.** Phase 1.5 §4.3 requires 1 Act III boss and 2 minibosses. The arc avoids killing manifestations ("no option kills grief", movement 11), while the dossier offers Wraith Lords, the Hollowed Current, and Wraithwatchers Gone Wrong as high-tier enemies. Someone has to decide what fighting a memory manifestation means: dispersing it, containing it, or something else. Until then, Pillar B combat and the main story don't meet.
3. **Player verbs lean on talk and paperwork.** Movements 2, 7, and 10 are a tally, an argument, and a hearing. With no cutscenes (Core Vision §8), concise dialogue (Tenet 18), and "stories through space, not text" (Tenet 11), those beats risk becoming long dialogue trees. Each movement should name where the player explores, fights, repairs, or uses a skill.
4. **No personal stake.** The arc never says who the player is or why Lowmark's water matters to them beyond being present.
5. **Reward is open.** The end-state is "a non-mechanical sign of trust", pending a later reward pass. That is fine for now but needs a decision before quest data.

### Side stories (`Caelmor_Part5_Lowmark_Side_Story_Lattice.md`)

Twenty candidates and eight micro-events cover every Phase 1.5 category, and each closes locally without a fetch structure. That is a real achievement. Three problems:

- **Sameness.** About 12 of 20 resolve through records, tallies, hearings, or memorial wording (L-S02, S03, S05, S06, S07, S09, S10, S11, S12, S17, S18, S20). Played back-to-back, they will feel like one quest type.
- **Skill intros don't teach skills.** Phase 1.3 §7 says skill-introduction quests cover Mining, Woodcutting, Hunting, and crafting. The six "work obligation" candidates are a bank inspection, a barge, a tally, a guide refusal, a mill dispute, and a job reference. None introduces a v1 skill.
- **The region's own conflict is missing.** No side story uses the bandits, smugglers, Field Goblins, Wraithwatchers, or noble-house rivalry the dossier describes, and only 2 of 20 are combat challenges.

### Opportunities already in canon

The most memorable stories are probably already written as one-line hooks in the Lowmark dossier: the Uphill Canal and the Twice-Burned Tree (whose dream-fruit could test the Dreamer evidence rule from the player's side), the Whispering Door, Wraithwatchers Gone Wrong (patrol members changed by long exposure), the Hollowed Current as a roaming event, and "Stillwater's Vigil"'s purge-versus-preserve choice (§XVI.5). These need selection and development, not new lore.

## NPC dialogue readiness and character voice

Dialogue is the least-prepared part of the project: there is no voice guide, no dialogue schema, and almost no sample speech for v1 characters.

- **No dialogue format.** The Dialogue/Interaction Content Schema (Roadmap 31.5) is unstarted. `DESIGNS/Systems Design/Stage 16.3 — NPC Interaction Contracts.md` explicitly excludes "dialogue systems, text, or writing" (lines 7, 18, 122).
- **Almost no sample speech.** The Lowmark anchor file has six quoted fragments, mostly scare-quoted phrases such as "just in case" and "light enough to carry". The Emberholt file has 52. No v1 character has a sample line of dialogue.
- **Voice guidance exists only as hints.** The Lowmark dossier gives a register ("speak slowly and think in seasons, not days", §XII) and a few proverbs ("Rivers carve stone by waiting", §III). The Thornfell anchors add horn and stone idiom. There is no list of regional vocabulary, oaths, naming conventions, or how each group talks about magic and Wraiths.
- **The main arc depends on voice more than most.** Its key scenes are disagreements: Maelin versus a clerk, workers versus a Lensemaster, households at a hearing. Those only work if the characters sound distinct and say a lot in few words (Tenet 18).

One useful input already exists. The Part 4 Character Ledger and the Part 5 mystery ledger record what each character knows versus believes. That is the backbone of a voice bible, because it tells a writer what a character can truthfully say.

## Missing creative decisions and unnecessary scope

Nine decisions block narrative production, and roughly a third of the reference material can be parked until after v1.

### Decisions only the Creative Director can make

| # | Decision | Blocks | Evidence it's open |
| --- | --- | --- | --- |
| 1 | Who exploits the emergency channels (the main-arc antagonist) | Acts I and III, movement 4 and 10 | Main Arc "Proposed author truth"; Reconciliation Audit deferred list |
| 2 | Who the player is: origin, ancestry, why they're in Lowmark, and whether origins are selectable | Act I opening, dialogue address, the dossiers' "Starting Faction Flavor" sections | Core Vision §6 says only "ordinary wanderer" |
| 3 | Which peoples exist (dwarves, goblins, Volkhari, Riverwardens as a people or a culture) | Enemy roster, NPC art, Thornfell | Contradiction #7 above |
| 4 | What defeating a Wraith means, plus the Act III boss and two minibosses | Combat content, Stillwater climax | Phase 1.5 §4.3; Main Arc movement 11 |
| 5 | The Lowmark subzone list and a POI-level map | POI catalog, quest placement, node placement | Contradiction #5; Part 4 Map Audit |
| 6 | The Last Field-Mage as a character (voice, history, limits) | Act II and III | No entry in any character file |
| 7 | The rival noble houses | The "which family should rule" political thread | Lowmark §II; only House Fenmere named |
| 8 | Lowmark faith and the Forgotten God's present-day role | Memorial and shrine content, Watergarden Keepers | Only Timeline §I mentions the god |
| 9 | Formal approval of the Lore Foundation Lock | Signals to every collaborator what is frozen | Lock Review ends "ready for approval" |

C03, C06, C07, and S01 remain safely deferrable for narrative, as the Decision Sheet says, because Lowmark doesn't depend on them.

### Scope to park until after v1

- **Emberholt's 50-character roster and the Remnant's four-division structure.** These are post-v1 and shouldn't receive more work until Emberholt enters production.
- **Cross-region scaffolding.** The 12 historical braids, 9 cultural-borrowing candidates, the callback lattice, and the future-region briefs (`Caelmor_Part4_*`, `Caelmor_Part5_Cross_Region_Callback_Lattice.md`, `…Future_Region_Narrative_Continuation_Briefs.md`). v1 can't pay these off and the Main Arc already says none is required.
- **Non-Lowmark source/process briefs** for Thornfell, the Mire, and Emberholt (about 50 KB).
- **More audit layers.** The repo has at least eight successive audit passes (Stage A, Part 2 gap, Part 3 gap, Part 4 second pass, Part 5 second pass, Part 6 cohesion, the source/process readiness audit, and the Lock Review). Each is careful, but further audits before any quest exists have diminishing returns.
- **Skill count versus quest budget.** `03_CORE_SYSTEMS/Skills & XP v1/Stage 3.1 — Non-Combat Skills Overview.md` defines 14 non-combat skills (approved), while Phase 1.5 budgets 5–6 skill-intro quests against 9 total skills. I didn't verify which of the 14 are v1 versus extension, but the intro-quest budget should be reconciled with whatever ships.

## Prioritized recommendations

Stop broadening the world and start making one quest playable end to end. In order:

### Now: unblock writing

1. **Make the nine decisions in the table above,** starting with the antagonist (#1), the player's identity (#2), and what defeating a Wraith means (#4). These three shape every Act I scene.
2. **Record what is already decided.** Mark the Lore Foundation Lock approved or not, add outcomes to the Decision Sheet, and move the "Canon Fix" and "Correction" notes out of `Caelmor_Factions.md` into a changelog so the file reads as reference.
3. **Run one cleanup pass on the 11 contradictions** in the consistency section. Most are a sentence each; #1 (the Speaker), #5 (subzones), and #7 (peoples) need a decision first.

### Next: make Lowmark playable

4. **Write a Lowmark voice bible.** Cover speech register by group (farmers, keepers, river crews, Lensemasters, Riverwardens), proverbs and oaths, how each group talks about water practice and Wraiths, naming conventions, line-length rules, and 3–5 sample lines per anchor. Build it from the existing knowledge/belief ledgers.
5. **Do a Lowmark cast pass sized to the stories.** Define the Last Field-Mage, the antagonists, one rival house, and the role NPCs the selected side stories need. Aim for the count the quests require, not a regional census.
6. **Turn the 12 movements into a beat sheet with player verbs.** For each movement, name where the player explores, fights, repairs, uses a skill, or makes a choice, and where the boss and minibosses fall. Cap the number of talk-only beats.
7. **Select 16–18 side stories and rebalance them.** Keep the best of the 20, cut about four of the record-and-hearing stories, and replace them with stories that use the dossier's own material: the smugglers' cellar, Wraithwatchers, bandits, the noble rivalry, and skill introductions for the skills that actually ship.
8. **Restore a wonder budget.** Choose 4–6 of the dossier's uncanny hooks (§XI) for v1 and give each a row in the mystery ledger so the evidence rule still holds.

### Then: prove the pipeline

9. **Write one complete quest as a vertical slice,** for example movement 1 plus one side story, with dialogue, placement, and triggers. This validates the quest template (Roadmap 34.1) before mass authoring. Note that the Roadmap currently puts Lowmark quest data (33.3) before the quest template set (34.1); that order should flip.
10. **Archive post-v1 material** (Emberholt roster, cross-region braids, future-region briefs, non-Lowmark source/process) under a clear "post-v1" label and pause new audit layers until v1 quest content exists.
11. **Do an Emberholt tone and naming pass** when that region enters production, covering the collisions and the dark-fantasy register noted above.

I didn't change any repository files, write new lore, or open a PR. Every claim above cites the file it comes from.
