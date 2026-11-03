# Isolated publication record

The original mixed commit `9eaaf1d58f464630b9d68fbaf01f6fdf08890679` remains preserved in the original checkout and at local branch `codex/preserve-mixed-9eaaf1d`. No reset, force push, or deletion of unrelated work was used.

A separate worktree on `codex/architectural-generator` was created from remote main `9b84c32d0fe0c6f17568a11a70e3ee29a1ffb6ec`. Only `CODE/Scripts/architectural_generator/` was restored from the mixed commit. Its 34 prototype files were byte-for-byte identical before subsequent exterior improvements. The PR does not cherry-pick the mixed commit or include its other changes.

The 0.3 regional expansion continues in this isolated worktree and [PR #85](https://github.com/Degrading1919/Caelmor-Repo/pull/85). Remote main `bcc60d91bd5164e7a8bf572ef9673859a24a27d3` was incorporated without overwriting local or concurrent work; the final fetch found no newer main. The expansion changes remain confined to this generator directory. No Unity/C#, gameplay, schema, or regional dossier changes form part of the generator diff.

## Excluded unrelated files

The following 32 files were left in the original mixed commit and were not imported into the generator branch. This is a scope inventory, not a review or endorsement of their contents.

- `00_ADMIN/Roadmaps/Caelmor_Roadmap.md`
- `02_VERTICAL_SLICE/Design Docs/Lowmark_Gameplay_Validation.md`
- `04_CONTENT_PRODUCTION/Quests/Caelmor_Lowmark_Main_Act_I.md`
- `04_CONTENT_PRODUCTION/Quests/Caelmor_Lowmark_Main_Act_II.md`
- `04_CONTENT_PRODUCTION/Quests/Caelmor_Lowmark_Quest_The_True_Line.md`
- `04_CONTENT_PRODUCTION/Quests/Caelmor_Lowmark_Side_Quests_Discovery_and_Memory.md`
- `04_CONTENT_PRODUCTION/Quests/Caelmor_Lowmark_Side_Quests_Settlements_and_Combat.md`
- `04_CONTENT_PRODUCTION/Quests/Caelmor_Lowmark_v1_Integration_Requirements.md`
- `04_CONTENT_PRODUCTION/Quests/Caelmor_Lowmark_v1_Narrative_Production_Bible.md`
- `04_CONTENT_PRODUCTION/Quests/LowmarkGameplay.json`
- `04_CONTENT_PRODUCTION/Quests/LowmarkGameplay_Integration.md`
- `CODE/Systems/Gameplay/GameplayContent.cs`
- `CODE/Systems/Gameplay/GameplayDungeon.cs`
- `CODE/Systems/Gameplay/GameplayOpportunities.cs`
- `CODE/Systems/Gameplay/GameplaySaveCompatibility.cs`
- `CODE/Systems/Gameplay/GameplaySession.cs`
- `CODE/Systems/QuestRuntimeSystem.cs`
- `CODE/Systems/QuestRuntimeValidationScenarios.cs`
- `CODE/Validation/GameplayIntegrationFixture.cs`
- `CODE/Validation/Program.cs`
- `DESIGNS/Systems Design/Stage 15.2 — Quest State & Progression Rules.md`
- `DESIGNS/Systems Design/Stage 15.4 — Quest Save, Restore & Validation.md`
- `DESIGNS/Systems Design/Stage 27 — Quest Runtime Integration Definition.md`
- `DESIGNS/Templates & Schemas/GameplayContent.schema.json`
- `UNITY/Assets/_Project/Bootstrap/PlayableBootstrap.cs`
- `UNITY/Assets/_Project/Core/CheckpointJsonShape.cs`
- `UNITY/Assets/_Project/Core/GameplayCheckpointService.cs`
- `UNITY/Assets/_Project/Core/LowmarkGame.cs`
- `UNITY/Assets/_Project/Core/PlayableHost.cs`
- `UNITY/Assets/_Project/Core/PlayableValidation.cs`
- `UNITY/Assets/_Project/Tools/Editor/CaelmorBuild.cs`
- `UNITY/Assets/_Project/World/TerrainNavigation.cs`
