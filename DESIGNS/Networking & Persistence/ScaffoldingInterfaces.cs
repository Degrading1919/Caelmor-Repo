// File: Engine/ScaffoldingInterfaces.cs
// Stage 8.2 — Engine Scaffolding Interfaces
// NOTE:
// - These are PURE scaffolding contracts.
// - No gameplay logic.
// - No persistence logic.
// - Designed to unblock Stage 7 system implementations only.

using System;

namespace Caelmor.Engine
{
    /// <summary>
    /// Read-only authoritative tick source.
    /// Owns the global simulation tick (10 Hz).
    /// </summary>
    public interface IServerTickSource
    {
        int CurrentTick { get; }
    }

    /// <summary>
    /// Implemented by systems that need deterministic per-tick updates.
    /// </summary>
    public interface IServerTickListener
    {
        void OnServerTick(int tick);
    }

    /// <summary>
    /// World-level lifecycle hooks.
    /// Used for boot/shutdown ordering only.
    /// </summary>
    public interface IWorldLifecycleListener
    {
        void OnWorldBoot();
        void OnWorldShutdown();
    }

    /// <summary>
    /// Zone-level lifecycle hooks.
    /// Used to safely initialize and teardown world-owned runtime systems.
    /// </summary>
    public interface IZoneLifecycleListener
    {
        void OnZoneLoaded(string zoneId);
        void OnZoneUnloading(string zoneId);
    }

    /// <summary>
    /// Minimal server-side player session abstraction.
    /// Stable identity only — no gameplay state.
    /// </summary>
    public interface IPlayerSession
    {
        int PlayerId { get; }
    }

    /// <summary>
    /// Session lifecycle notifications.
    /// </summary>
    public interface IPlayerSessionListener
    {
        void OnPlayerSessionStart(IPlayerSession session);
        void OnPlayerSessionEnd(IPlayerSession session);
    }

    /// <summary>
    /// Marker interface for save scopes (PlayerSave / WorldSave).
    /// Flush is atomic at the scope level.
    /// </summary>
    public interface ISaveScope
    {
        void Flush();
    }
}
