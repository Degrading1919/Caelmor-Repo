// File: Persistence/ISaveStorageInterfaces.cs
// Stage 8.7 — storage interfaces only (no I/O details, no formats)

using System;

namespace Caelmor.Persistence
{
    public interface IPlayerSaveStorage
    {
        PersistedPlayerSave LoadPlayer(int playerId);  // may throw on corruption/missing
        void SavePlayer(PersistedPlayerSave save);      // may throw on write failure
    }

    public interface IWorldSaveStorage
    {
        PersistedWorldSave LoadWorld(string worldId);   // may throw on corruption/missing
        void SaveWorld(string worldId, PersistedWorldSave save); // may throw on write failure
    }
}
