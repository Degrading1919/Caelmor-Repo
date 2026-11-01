# Preserved legacy workspace material

This folder preserves historical project files from `C:/Users/CK/Documents/Caelmor` that were absent from, or different to, the authoritative repository at `C:/Users/CK/Documents/Caelmor-Repo`.

The GitHub repository `Degrading1919/Caelmor-Repo` and its local checkout remain the source of truth. These archived documents, schemas, code, and assistant instructions are **historical reference only**. They do not replace current canon, governance, approved schemas, or runtime implementations. A file calling itself authoritative inside this archive does not grant it current authority.

`SourceInventory.json` records all 152 preserved legacy files, original relative paths, archived paths, byte sizes, classifications, and SHA-256 hashes. It includes 98 previously missing files copied into their existing `ARCHIVE/Deprecated` or `ARCHIVE/Experimental` categories, six distinct reference/test documents preserved here, and 48 same-path historical variants preserved here instead of overwriting the current files. Original filenames, including historical version suffixes, are retained verbatim for provenance.

Every copied file was checked byte-for-byte by SHA-256 against its legacy source. No original legacy file was deleted, overwritten, moved, renamed, or edited. Existing active repository files were not replaced. No archive destination was overwritten with different bytes.

The active .NET runtime compiles only `CODE/Systems/**/*.cs` and `DESIGNS/Networking & Persistence/*.cs`; the Unity project imports its own `UNITY/Assets`. This archive is outside those paths. Do not move these obsolete C# implementations or schemas into active build/content paths merely to fill a perceived dependency.

The old Unity project was a stock URP template (camera, light, global volume, tutorial assets), so it was left intact in the legacy workspace. Generated Unity caches, logs, user settings, VCS metadata, `desktop.ini`, exact duplicates, and the renamed whitespace-equivalent MMO brief were not imported. Legacy cleanup or relocation remains a separate Director-approved action.
