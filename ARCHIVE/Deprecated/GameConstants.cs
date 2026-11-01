using UnityEngine;

namespace Caelmor.VerticalSlice
{
    /// <summary>
    /// Shared tuneable constants for the vertical slice.
    /// Used by both host- and client-side systems.
    /// </summary>
    public static class GameConstants
    {
        // 2.1 Movement Speed Unification
        public const float MOVE_SPEED      = 4.0f;  // m/s for players
        public const float MAX_LEASH_SPEED = 3.5f;  // m/s for AI return steering

        // 2.3 HP Sync Strategy — periodic HP sync every 1s
        public const float HP_SYNC_INTERVAL_SECONDS = 1.0f;

        // Tick interval (authoritative simulation)
        public const float TICK_INTERVAL_SECONDS = 0.1f;
    }
}
