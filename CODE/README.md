# Runtime build and validation

## Workspace locations

`C:\Users\CK\Documents\Caelmor-Repo` is the authoritative local checkout of `Degrading1919/Caelmor-Repo`. Edit runtime source here and open its `UNITY/` folder in Unity Hub. `C:\Users\CK\Documents\Caelmor-Build` contains generated executables, logs, and audit outputs; regenerate these with `UNITY/Build.ps1` rather than editing them.

`C:\Users\CK\Documents\Caelmor` is the retained legacy workspace. Its unique historical material has been copied into repository archives without changing the originals. Do not open its old Unity project for current development or treat its older protocols, schemas, and runtime code as current authority. See the [workspace reconciliation](../00_ADMIN/Reference/Caelmor_Workspace_Reconciliation.md) and [preserved-file inventory](../ARCHIVE/LegacyWorkspace/SourceInventory.json). Legacy deletion or relocation requires explicit Director approval.

## Validation command

From the repository root in PowerShell:

```powershell
.\CODE\Build-And-Validate.ps1
```

The script uses the .NET SDK bundled with Unity 6000.5.5f1, falling back to an installed `dotnet`. Pass `-UnityEditorRoot 'C:\path\to\Editor'` for another installation, or `-Configuration Release` for the release build. No NuGet packages are required.

`Caelmor.Runtime.csproj` compiles every C# source under `CODE/Systems` and `DESIGNS/Networking & Persistence` into a .NET Standard 2.1 library. It references the actual installed Unity CoreModule; no substitute Unity API is used. The output is `CODE/bin/Debug/netstandard2.1/Caelmor.Runtime.dll` (or `Release`). Unity should import only Caelmor's DLL, using its own engine assemblies.

The validation executable retains the original 88 checks: 71 registered scenarios across 13 required suites, all 12 injected Stage 9 matrix scenarios, an economy mutation/hydration regression, inventory atomicity/restore regressions, a suite coverage check, and the threaded in-process host/session/transport proof. It now adds nine connected gameplay checks (97 total), including all three True Line evidence choices, all three Bank Walk branches, phase/range/LOS/lifecycle boundaries, interrupted carry/channel recovery, repeatable gathering/hunting/cooking, XP, rewards, corrupt checkpoints and actual atomic disk I/O. Onboarding checks force duplicate rejection before successful completion and race concurrent completion notifications. A failed assertion or missing required suite exits nonzero.

Gameplay schemas are validated with PowerShell 7 Test-Json before compilation. Runtime DTO/reference checks and the complete action replay use the actual production pack; the new gameplay checks also reuse the existing inventory, quest, melee proposal, crafting and gathering implementations. Source presence or this C# runner alone does not establish a playable Unity experience. See [Unity build and controls](../UNITY/README.md) for actual licensed engine/standalone checks and current limitations.

Coverage includes combat, NPCs, onboarding, identity/save binding, restore gating, lifecycle, player instances, zone residency, inventory, quests, world tick phases, transport, and replication (including deferred snapshot consistency). The Stage 9 fixture uses the existing production resource node, gathering, grant, crafting, checkpoint, persistence adapter, restore, and validation harness classes with test-only policy/content, serialized actions, a test clock, and cloned in-memory storage. It checks actual mutations, contention, respawn timing, checkpoint ordering, and hydration after perturbing live state; it does not establish durable disk saves or a complete game. Snapshot capture/copy/sort work remains synchronous; the scheduler does not yet provide a complete CPU budget for serialization. Existing nullable-reference warnings remain visible in the build.
