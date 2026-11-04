# Caelmor repository consolidation

## Current development policy

The Creative Director has authorized direct work on `main` in the sole checkout `C:/Users/CK/Documents/Caelmor-Repo`. PR #85 was merged into `main`. The distinct lore proposal was preserved as a proposal-only file without reverting the newer approved balance decisions. The historical lore-proposal and rejected-contract branch commit ancestry was also incorporated into `main` while retaining the reconciled `main` file tree. Old branch names are historical and no longer implementation targets; the work policy is defined by root `AGENTS.md` and the Master Assistant Protocol. The inventory below records the earlier consolidation stages, not active development instructions.

## Authority and implementation target

GitHub `Degrading1919/Caelmor-Repo` is the project authority. `C:/Users/CK/Documents/Caelmor-Repo` is the sole designated working checkout on this machine. See the [agent workflow](../../AGENTS.md) for feature branches, PR review and cleanup gates.

The architecture target is [`codex/architectural-generator`, PR #85](https://github.com/Degrading1919/Caelmor-Repo/pull/85). At inspection the PR was open and unmerged, with head `22e4185` and base `main` at `eb66ef8`. Source revision 0.12.2 has the regional, World and function-first paths and the latest Thornfell curtain return study. The PR description describes an earlier milestone. Read the head source and study manifests for current behavior. The [engine contract](../../CODE/Scripts/architectural_generator/ENGINE_CONTRACT.md) separates this baseline from legacy compatibility and the proposed seven-treatment interface.

## Local inventory and preservation

### Physical consolidation handoff

The Creative Director authorized removal of the redundant copies after GitHub verification. The [consolidation inventory](../../ARCHIVE/LegacyWorkspace/Consolidation_Inventory.json) records the original paths, SHA-256 values and dispositions. Where content already existed in GitHub history, the inventory records the blob ID. For retained archive members it records the repository path and member name. The prior inventory below describes the state before physical cleanup.

| Recovered material | Repository destination |
| --- | --- |
| Architecture evidence | Existing [generator evidence directory](../../CODE/Scripts/architectural_generator/evidence). The recovery archives contain editable Blender scenes and backups, a Blender regression script, the local add-on package, validation logs, original Caelmor renders and export evidence. Three sidecars are beside their existing studies. Exact extracted image copies are recoverable from the retained GLBs. The archives preserve historical bytes and do not replace current code or `dist/`. Blender opened the three editable scenes and found original Caelmor packed maps and no linked libraries. |
| Art direction, historical source and build validation | Existing [legacy archive](../../ARCHIVE/LegacyWorkspace). Retained authored plugin staging source, art research and validation, one earlier schema report, build and smoke logs, the workspace audit, and unique text metadata from the old playable packages. Build binaries, stock Unity template, Unity caches and bytecode are disposable. |
| Material research | The [Caelmor research workbook](Caelmor_Material_Research_Review.xlsx) and [material reuse workbook](RS3_Material_Reuse_Research.xlsx) are retained in `00_ADMIN/Reference/`. The legacy archive contains the project-authored scanner and resolver scripts and their factual CSV/JSON observations. The helpers depend on a separately supplied RSMV environment. No raw cache or third-party meshes, images or textures are retained. |

The original rejected contract and its mixed parent remain reachable on GitHub through `codex/preserve-rejected-contract`. The local architecture recovery snapshot at `4efa0205` was reconciled file by file. Its raw history is superseded by the indexed artifacts above and the existing source history on PR #85.

### Cleanup completed

GitHub's tree for `63068b4` matched the local blob IDs for all 22 changed files. Before removing the originals, the cleanup rechecked their SHA-256 values against the inventory and verified the architecture branch, PR head and rejected-contract recovery ref on GitHub.

- Git removed the detached `Caelmor-Architecture` worktree and its directory. The cleanup also removed `Caelmor`, `Caelmor-Build`, `Caelmor Art Director Support`, `RS3-Material-Usage`, the Fort Forinthry extracts directory and four research-tool staging directories.
- The cleanup removed 15 loose files, including old playable ZIPs, two generated research bundles, duplicate research downloads and third-party reference images. Their retained project-owned content or provenance is recorded above.
- The three obsolete local recovery branches were removed. The final filesystem sweep found only the designated checkout among the inspected project locations. Git reported a single registered worktree.

### Inventory before cleanup

| Location | Finding and disposition |
| --- | --- |
| `Documents/Caelmor-Repo` | Clean before the transition. Former local `main` at `4ae1d62` had two local commits and was eight commits behind GitHub `main`. The preserved branch `codex/preserve-rejected-contract` points at the original commit and retains its mixed parent `9eaaf1d`. It is a recovery branch. The contract's unique change was applied by file to the architecture branch. Local `main` now tracks `origin/main`. |
| `Documents/Caelmor-Architecture` | Linked worktree of the same repository and remote. Detached at `22e4185`, releasing the feature branch to the designated checkout. It held one modified distribution ZIP and 391 untracked evidence files, about 391 MB. A separate local Git recovery ref, `codex/preserve-architecture-worktree` at `4efa0205`, preserves 643 changed or added files, including the ZIP, raw exports, renders, validation logs, one ignored script and editable Blender files. Python bytecode was excluded. The modified ZIP differs from both the tracked ZIP and the current source. Neither ZIP establishes the current implementation. Original files remain in place. |
| Other local branches | Feature and historical branches were inventoried against fetched `origin` refs. `codex/preserve-mixed-9eaaf1d` is covered by the rejected-contract preservation ref. `codex/equipment-component-functions` points at `eb66ef8`, also reachable on `origin/main`. No stash was listed. |
| `Documents/Caelmor` | Non-Git legacy copy. Excluding caches and local metadata, 295 file contents matched Git blobs after checking raw and newline-normalized bytes. The 61 unmatched files comprise the old Unity template/settings and one renamed technical brief that matched the tracked text after normalization. Prior project-owned source variants are recorded in [the legacy archive](../../ARCHIVE/LegacyWorkspace/README.md). |
| `Documents/Caelmor-Build` and three `Documents/Caelmor-*.zip` builds | Generated Unity builds, logs, a workspace audit and packaging outputs. `Caelmor-Build/README.txt` identifies the repo build entry points. The outputs remain in place pending retention and cleanup review. |
| `Documents/Caelmor Art Director Support` | Separate non-Git plugin staging and research/validation pack. Preserved the project-facing [art methodology](Caelmor_Artistic_Methodology.md) in the repository as a working reference. The plugin package, source bundle, validation and research originals remain in place. |
| Caelmor files in `Downloads` | Generator research matched a Git blob in the architectural branch. Preserved the [creative readiness assessment](../../ARCHIVE/LegacyWorkspace/Caelmor_Creative_Readiness_Assessment.md) as a historical snapshot. The material workbook is a supporting research source recorded below. |

The curated studies under `evidence/` remain the first point of reference. Keep recovery branches and archives out of active implementation inputs.

## Artifact placement and external provenance

The [File Manifest](Caelmor_File_Manifest.txt) lists the existing placement roots. Use `CODE/Scripts/architectural_generator/` for the add-on and contracts, its `evidence/` for accepted, reproducible evidence and `dist/` for the checked package. Use `00_ADMIN/Reference/` for governance and project reference notes and `ARCHIVE/LegacyWorkspace/` for preserved historical sources. The manifest inventory helper lists tracked paths in the checkout and writes no manifest copies.

Accepted evidence should include source commit, tool version, settings/seed, what was verified and the boundary of that evidence. Keep temporary renders, cache files, unpacked images and rebuild intermediates disposable unless they carry unique work. Record external datasets by provenance and review their rights before importing any third-party assets.

| External source | Provenance and use |
| --- | --- |
| `Caelmor_Material_Research_Review.xlsx` | Originally in `Downloads`. SHA-256 `7f8bccd9bc9a00fb6bc9b4184a9daa1a8da7bfd5807529313d9677eae4898f14`. Starter Library and Shared Surface Maps informed reuse of surface families across treatments. |
| RS3 named material usage | Originally `Documents/RS3-Material-Usage/material_usage_named.csv`. SHA-256 `db3cb36ea80e22cecebf4267fc2e9a2d091b7cb1c77291002a42ae2b6a676159`. Counts are scan observations, with mixed naming provenance. The source informed material reuse. It supplies no Caelmor assets, names or regional defaults. |
| Fort Forinthry and extracted visual references | The [curtain study](../../CODE/Scripts/architectural_generator/evidence/curtain_masonry/README.md) and [pigment study](../../CODE/Scripts/architectural_generator/evidence/painted_materials/README.md) describe the supplied captures and sampled material evidence. The inventory records fingerprints for the excluded extracts. |
