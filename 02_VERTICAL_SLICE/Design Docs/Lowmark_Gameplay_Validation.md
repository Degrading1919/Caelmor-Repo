# Lowmark gameplay integration milestone — 2026-11-01

Playable artifact: C:/Users/CK/Documents/Caelmor-Build/Lowmark/Caelmor.exe. Portable package: C:/Users/CK/Documents/Caelmor-Lowmark-Playable.zip (64,355,809 bytes). ZIP SHA-256: 5E4CF913F8207DDE88AC12571AC4F0A7487B5723070B0C935130B93334FA00DB. Run the executable with its adjacent data and Mono folders intact. The earlier build in the parent directory was retained.

## Delivered player loop

The True Line now joins dialogue, inspections, combat, a loaned tool, Woodcutting, repair/discovery, distinct evidence, carries, boar defense, exclusive choices, action XP, payment and saved world state. The Bank Walk extends that loop through measurements, tree assessment, Skitter combat, environmental telegraphs with host-validated push, felling and keep/cut/build outcomes. Ordinary timber, hunting, cooking, food and healing form a repeatable connected activity chain. Neither quest is implemented by a quest-ID switch in C#.

The data projection preserves Opus's authored material as proposals. New Bank Walk source was read from the live repository; Opus's newly published narrative documents were not overwritten or copied over local work. The projection's contract, source provenance, provisional calibration, geographic compression and fidelity gaps are recorded in 04_CONTENT_PRODUCTION/Quests/LowmarkGameplay_Integration.md. Existing schema/network/PlayerSave formats were not changed.

## Executed evidence

- PowerShell 7 JSON Schema validation passed. Content reference and unique placement checks passed; skill thresholds match the approved 99-level CSV.
- CODE/Build-And-Validate.ps1 -Configuration Release: 97 passed, zero failed. Includes all three evidence custody choices, all three Bank Walk branches, phase/gate/LOS/range tests, atomic item changes, interrupted carries/channels, fixed-base XP, real disk replacement/backup/read, corrupt saves and repeatable activities.
- UNITY/Tools/Compile-Source.ps1: passed with zero warnings/errors against installed engine assemblies.
- Licensed Unity 6000.5.5f1 scene import, foundation/NavMesh/physics checks and Windows x64 build passed.
- Final standalone: CAELMOR_GAMEPLAY_CHECKS_PASSED, CAELMOR_LOWMARK_PASSED and CAELMOR_SMOKE_PASSED. The actual executable completed The True Line and Bank Walk's building branch through real queued host commands and native paths. It verified melee retaliation/dodge, channel interruption, hazard damage and capsule/NavMesh-validated displacement, gathering/crafting, checkpoint rehydration and lifecycle suspension. The independent live scheduler sample advanced 11 ticks in 1.150 seconds. Logs contain no exception marker.
- Visual/input pass: actor selection, automatic approach, committed Maelin dialogue, pack/skills display and F5 checkpoint save succeeded. Physical Escape stopped Computer Use during F9; no further app input followed. UI reload was not verified. Automated disk restore passed. Later NPC scale/name readability corrections were rebuilt, not visually rechecked.
- Independent Systems Engineer review found the initial safe attack-distance exploit, final-tick channel reward race, carry/input cancellation, near-target route, hidden HUD hit-test, repeated hydration and content-fidelity defects. These were corrected and checked again; final review reported no blocking defect.

## Reproduce

From the checkout in PowerShell 7:

```powershell
./CODE/Build-And-Validate.ps1 -Configuration Release
./UNITY/Tools/Compile-Source.ps1
./UNITY/Build.ps1 -OutputDirectory 'C:/Users/CK/Documents/Caelmor-Build/Lowmark'
& 'C:/Users/CK/Documents/Caelmor-Build/Lowmark/Caelmor.exe'
```

The Unity license must be active. Keep logs beside the generated build. See UNITY/README.md for controls, staging, checkpoint location and exact persistence semantics.

## Remaining production dependencies

This is a cohesive greybox milestone, not complete Lowmark v1. Enemy anchors do not yet pursue or physically charge. Full NPC lifecycle/escort walks, production art/animation/audio, reflected/quiet-water wonder, an approved expanded POI layout and far-bank connection remain. Shared-world node contention/depletion, full multiplayer replication, co-op quest credit, abandon/re-offer, water scheduling and complete binding into established durable PlayerSave are not proven by this single-host adapter. Local checkpoints are explicit, synchronous between ticks and content-fingerprint specific; content migrations, power-loss fault injection and serialization budgets remain work.

The next authored activity is The Flood Kitchen: integrate the reusable non-combat flock behavior, shelter layout and food-portion recipe, then project/test its content. Short Measure supplies the next main-arc/dungeon connection once its layout and encounter/item data are ready. No foundational canon ruling is needed for the delivered technical mechanics; new authored material still awaits Director canon promotion through the existing production process.

## Flood Kitchen integration — 2026-11-02

The approved local milestone 3436451 was merged with Opus's production acts, side quests and dialogue without conflicts and published in 22e48960bfa455f0b7f2b67b84d78ab2000e834c. No local gameplay or remote creative work was discarded. Development continued into a third authored quest.

New executable: C:/Users/CK/Documents/Caelmor-Build/FloodKitchen/Caelmor.exe. Portable package: C:/Users/CK/Documents/Caelmor-Flood-Kitchen-Playable.zip (64,375,071 bytes). SHA-256: 7EC645F169ADA1BBF9522618A2E0963753D6C4704EC74598948EEADC591F30FF. Earlier build folders and packages are retained.

The Flood Kitchen connects shelter/Nan dialogue, both fuel routes, timed fire-lighting, non-combat flock preparation/warning/scatter and separate recovery, Cooking, four household deliveries, all three last-pot choices, a bowl/payment, persistent choice props and public hunting/cooking. Food from previous activities is accepted through tags. Hunting food and XP come only from recovery. Generic production totals allow two public cooks or Nan's batch to satisfy the same objective. No quest-ID branch is added to runtime code.

Native navigation connects the original test space to an eastern shelter/margin hub. Dynamic flock positions drive display, selection, approach, nearest interaction and host LOS/reach. Rushing/unprepared approach warns; withdrawal cancels it; scatter immediately selects the other open point. Pending recovery cannot create a second corpse or hidden scatter cycle. Nesting boundaries reject takes and one-way combat. Actual movement noise is preserved on a sprint's final tick even when presentation becomes idle.

The stone event and shelter hush share committed presentation state. Restoration preserves the higher waterline without replaying the hush. Shelter recovery is validated by host navigation. Production counters clone/save/restore with exact identities and quest history; overflow is rejected before spending inventory or awarding XP.

Executed verification:

- Schema, references, unique gathering identities and approved XP thresholds passed.
- 104 C# checks passed, zero failed: all quest choices, both fuel routes, flock/closure/recovery, tagged-input overlap, replenishment, counter progress/restore/overflow and the existing baseline.
- Unity SDK source compilation passed with zero warnings/errors. Licensed scene import, native NavMesh/physics checks and Windows x64 build succeeded.
- Standalone completed The True Line, Bank Walk's building route and Flood Kitchen's own-food/crate route through real queued commands. It also proved public-only Cooking progression, flock relocation, tagged meals, mid-hush/final disk restoration, live damage/death/shelter recovery and retained inventory/progress. All three success markers passed; the final scheduler sample was 11 ticks in 1.150 seconds, with no exception marker.
- Independent review found no remaining blocker, independently reran all 104 checks and read final engine logs.
- No Computer Use, mouse/keyboard injection, window focus or screen capture was used. New verification is compilation, batch-mode engine assertions and logs. Headless startup ignores user load preferences and activity input polling. Rendering/readability and end-to-end usability remain unverified manually.

Reproduce with UNITY/README.md using output directory Caelmor-Build/FloodKitchen. Logs are beside the executable. Existing content-fingerprinted checkpoints are retained but not migrated; tests do not overwrite the user's checkpoint. Full established PlayerSave/network binding remains separate.

Remaining work includes authored loft stairs (current crates use flat access), production animation/audio, complete NPC lifecycle/escort, shared co-op disturbance, mobile enemies, detailed water/reflection presentation, actual regional geography and broader persistent world simulation. The next main-arc milestone is Short Measure: reusable interior/vertical navigation, persistent one-sided doors, disarmable/rearming traps and boss arena reset/ground hazards, followed by faithful dungeon content integration.

Publication reconciliation: Opus advanced main again before the kitchen push. The subsequent merge preserved the new Integration Requirements, Encounter/Enemy Requirements and POI/Zone Requirements, plus revised narrative/dialogue. The implemented quests were checked against that delta. The new pre-MQ4 bottom-step inspection is projected and exercised in the final standalone; the later backwater variant and typed LM_TL_EVIDENCE region bridge remain future quest/region bindings. The handoff's D-INT-7 requests a breaking approved quest-state change to add Abandoned/re-offer; that proposal was preserved without modifying the Stage 27 contract or project governance. It needs a Director ruling before that feature is implemented.
