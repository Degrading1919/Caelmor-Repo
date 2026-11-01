# Caelmor workspace reconciliation

Inspected and reconciled on 2026-11-01. This is a technical inventory record; it does not change project canon, schemas, or the Master Assistant Protocol.

## Active workspace

| Location | Purpose |
|---|---|
| `Degrading1919/Caelmor-Repo` on GitHub | Authoritative shared source repository |
| `C:\Users\CK\Documents\Caelmor-Repo` | Authoritative local checkout; edit source/content here |
| `Caelmor-Repo\UNITY` | Current Unity 6000.5.5f1 project |
| `C:\Users\CK\Documents\Caelmor-Build` | Generated Windows player, logs, and audit outputs; rebuild from checkout |
| `C:\Users\CK\Documents\Caelmor` | Retained legacy workspace; originals untouched |

The File Manifest's historical project-root string names the legacy workspace. Its category organization was used for archival placement; the Director's current instruction identifies the repository checkout as the active source. No governance file or legacy file was rewritten to change that string.

## Inspection results

The legacy tree contained 29,907 files totaling approximately 1.93 GB. Approximately 1.927 GB was generated Unity `Library`, `Logs`, and `UserSettings` data. Excluding generated directories and four Unity VCS metadata files left 365 non-generated files totaling 7,360,098 bytes.

| Comparison before reconciliation | Files |
|---|---:|
| Identical at the same repository-relative path | 147 |
| Identical under another repository-relative path | 4 |
| Different bytes at an existing relative path | 48 |
| Legacy-only paths with distinct bytes | 166 |

Path and SHA-256 comparisons covered on-disk files. The legacy directory had no Git working-tree metadata. Filesystem differences were therefore treated as potential local work, rather than assuming they were disposable. No Git configuration or VCS internals were inspected.

The old `UNITY/Caelmor_VS` project contains the stock URP template: its sample scene has a camera, directional light, and global volume; its `Assets/Caelmor` directory is empty and its scripts are the template Readme tutorial. No unique authored models, textures, gameplay scenes, or gameplay scripts were found there.

## Additive preservation

152 files totaling 2,190,822 bytes were copied without overwriting any existing destination:

- 98 missing historical files from legacy `ARCHIVE/` retain their original archive-relative paths in the repository.
- Six distinct reference/test documents are under `ARCHIVE/LegacyWorkspace/` with their original category-relative paths.
- 48 differing historical versions are preserved under the same archive root, leaving current runtime, lore, schemas, and governance unchanged.

Every copied file was checked against its source SHA-256. All 365 inventoried legacy file hashes were rechecked afterward. No legacy file was edited, moved, or deleted. The [preserved-file inventory](../../ARCHIVE/LegacyWorkspace/SourceInventory.json) records source paths, archive paths, sizes, hashes, and classifications. The [archive README](../../ARCHIVE/LegacyWorkspace/README.md) explains its historical status. Archived C# remains outside the current runtime project's compilation globs.

Identical files and renamed equivalents were not duplicated. The legacy MMO compilation brief matches the current renamed brief after outer-whitespace trimming. Windows `desktop.ini`, Unity VCS metadata, generated caches, and the old stock Unity template remain in place and were not imported into the active project. Full inspection evidence is generated output in `Caelmor-Build/WorkspaceAudit/`.

The build directory also retains the previous source-check scratch paths `bin/`, `obj/`, and `AdapterCompile.csproj`. Automatic approval review blocked their deletion with no explanation beyond "blocked by policy". They remain classified as generated output and are excluded from the playable ZIP; they are not another source workspace.

## Remaining approval boundary

No destructive cleanup was required for reconciliation. Deleting or relocating the legacy folder, its old Unity project, or its caches requires explicit Director approval. Until then, use only the repository checkout for current development and treat the old folder as retained historical material.
