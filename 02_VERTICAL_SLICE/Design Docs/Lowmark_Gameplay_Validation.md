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
