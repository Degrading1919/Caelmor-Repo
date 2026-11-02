# Caelmor Lowmark gameplay build

Unity 6000.5.5f1, Windows x64, built-in rendering. This is a playable greybox of authored content, with reusable RPG runtime integration; it is not the finished Lowmark v1 release.

## Reproduce and play

Activate the installed Unity Editor license in Unity Hub, then run from the repository root in PowerShell 7:

```powershell
./CODE/Build-And-Validate.ps1 -Configuration Release
./UNITY/Tools/Compile-Source.ps1
./UNITY/Build.ps1 -OutputDirectory 'C:/Users/CK/Documents/Caelmor-Build/Lowmark'
& 'C:/Users/CK/Documents/Caelmor-Build/Lowmark/Caelmor.exe'
```

Build.ps1 validates GameplayContent.schema.json, copies the authoritative 04_CONTENT_PRODUCTION/Quests/LowmarkGameplay.json into the Unity Resources staging asset, compiles/stages the canonical runtime DLL, generates/bakes/reopens the scene, executes foundation checks, builds Windows, then runs standalone engine checks. Nonzero exit or a missing success marker fails the script. Logs are unity-build.log and standalone-smoke.log beside the executable. Default output without the override remains Caelmor-Build/Caelmor.exe. Generated output is never an authored source. No paid art or additional NuGet dependency is needed.

For editor play, run ./UNITY/Build.ps1 -StageOnly, open UNITY in Unity Hub and the saved Assets/_Project/World/PlayableFoundation.unity scene. Restage after changing CODE or production content. The SDK source check verifies real Unity API compilation only; it does not replace Editor import or engine execution.

## Controls and connected gameplay

- Left-click terrain to navigate around obstacles; click a person or prop to select it. Choose an action in the right panel to approach and interact. E selects a nearby available interaction. Hold Shift to sprint, including while carrying.
- RMB orbits; wheel zooms. The camera remains yours during dialogue and the stone discovery. Escape stops movement/actions and opens help. Focus changes clear queued input, movement, channels and combat; a carried load is retained. F3 enables optional WASD debugging, off initially.
- I opens the pack and skills. Eat prepared strips from the pack when wounded. Orange ground tells mark incoming enemy attacks; move off them. Standing still through a strike causes host damage; enemy misses create recovery time. Moving or taking a hit interrupts timed work before resource/XP application.
- F5 writes an explicit local checkpoint. F9 validates it and reloads the scene at the road head. The pack also has save/reload buttons. There is no automatic save or overwrite on exit.

The True Line now connects NPC dialogue and optional leads, marker inspection, tracking, shallow-water melee, Woodcutting/tool lending, timed repair, the stone event, two distinct proofs, sacks/trunk carries, boar defense, evidence/stone choices, payment, marker knowledge and authored epilogue lines. Choices and inventory survive checkpoints. The dispatch order transfers automatically at D7 when its lead was found. Carry objects never enter inventory and can be collected again after death or reload.

After The True Line, The Bank Walk becomes available from Tamsin in the southwest bank area. It connects measurements, wrack inspection, River Skitters, a timber jam, telegraphed environmental damage/push, tree assessment/felling, and all three keep/cut/build decisions. The landing-building route consumes timber and uses timed construction. Persistent props and follow-up dialogue reflect the outcome. These remain authored proposals, not promoted canon.

Ordinary coppice timber, repeatable boar Hunting, Cooking with timber fuel, prepared food, healing and fixed-base action XP remain useful beyond both quests. All 99 skill thresholds match the approved CSV. Numerical tuning is provisional and recorded in LowmarkGameplay_Integration.md; no lump quest XP or invented currency name is introduced.

## Authority and persistence

PlayableHost retains WorldSimulationCore's 100 ms clock, actual session/save-binding/restore/lifecycle/residency gates, command ingestion/freeze/consume, host NavMesh path calculation and swept capsule collision. UI submits numeric action/target indexes; it cannot grant items, report player position or advance quest stages. The host resolves range, line of sight, conditions, tools, channel duration and combat. GameplaySession prepares a private draft during Simulation Execution, then commits before movement snapshot publication. Failed ticks discard the draft. Inactive players receive no gameplay execution or snapshots.

The composition reuses SimplePlayerInventoryStore, QuestRuntimeSystem, CombatStateAuthoritySystem/CombatResolutionEngine, GatheringResolutionSystem and CraftingExecutionSystem. Existing combat proposals intentionally own no HP; the new bounded melee effect sink supplies health, cooldowns, tells and death recovery. All action deltas are atomic. Authored gather placements have explicit numeric node identities. The existing shared-world resource node, full NPC lifecycle and replication systems are not all bound into this single-host composition.

Gameplay checkpoints are an additive local envelope, not a migration of the established PlayerSave/network contracts. They contain inventory, XP, objective stages, receipts/choices, enemies, cooldowns and hazards; raw content SHA-256 identity and structural/invariant checks run before restore. A rejected checkpoint preserves the running game. Atomic replacement retains a .previous backup and flushes file contents. There is no automatic corruption repair. A checkpoint from changed content is deliberately rejected pending a future migration policy.

The file is Application.persistentDataPath/lowmark-gameplay.checkpoint.json, currently C:/Users/CK/AppData/LocalLow/Caelmor/Caelmor Playable Foundation/lowmark-gameplay.checkpoint.json. Reload starts at the road head and clears transient channels, combat and carries. Death restores health at the crew fire and retains progress/items. World position, multiplayer membership and wall-clock simulation are not persisted here. Checkpoints are synchronous between ticks; serialization performance and crash/power-loss fault injection are not established.

## Executed validation and limits

The C# runner exercises the original 88 checks plus connected quest/economy/restore regressions, all True Line evidence choices and all Bank Walk branches. It performs actual atomic disk writes/reads as well as in-memory state tests. See CODE/README.md for the baseline scope.

The licensed Unity build runs native NavMesh/physics movement/collision/authority checks. Standalone LowmarkValidation drives real queued commands through The True Line, a repeatable economy cycle and The Bank Walk's building branch, including incoming melee damage, movement dodge, interruption, hazards with collision-validated push, independent quest state and JsonUtility/disk restore. It asserts gameplay is committed before movement snapshots and suspended lifecycle blocks it. The separate scheduler sample checks elapsed wall time against 10 Hz after draining the synchronous test frame; simulation checks still use fixed 100 ms deltas. Success markers: CAELMOR_GAMEPLAY_CHECKS_PASSED, CAELMOR_LOWMARK_PASSED, CAELMOR_SMOKE_PASSED.

Visual input checks verified world selection, automatic approach, committed Maelin dialogue, pack/skills and F5 saving. The user stopped Computer Use with physical Escape during F9, so UI-driven reload was not verified. Automated disk restoration passed. Subsequent label readability/NPC scale corrections were rebuilt and engine-tested, but not visually rechecked after that stop. This is not a human end-to-end quest usability or long-session playtest.

Remaining production work: mobile enemy pursuit/physical boar charge, complete NPC lifecycle/escort and inspection walks, production art/animation/audio, the full quiet-water/reflection/far-bank-figure presentation, more spacious approved POI layout, connected far-bank destination, authored water-state scheduling, abandon/co-op behavior and full legacy PlayerSave/network binding. Enemy bodies are anchored greybox encounters; their windup/damage/dodge timing is authoritative. The current flat navigation scene has no multi-level or off-mesh traversal. See the content integration record for fidelity details and the next authored activity dependencies. No claim of complete Lowmark v1, multiplayer playtesting or production persistence follows from this milestone.
