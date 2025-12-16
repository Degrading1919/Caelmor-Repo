// File: Economy/ResourceNodes/ResourceNodeRuntimeSystem.cs
// Stage 8.3 — Resource Node Runtime (Stage 7.1)
// NOTE:
// - ResourceNodeInstance is a CLASS (not struct) to avoid mutation foot-guns.
// - RespawnTicksRemaining is PROVIDED by caller (policy/tuning provider upstream).
// - Duplicate NodeInstanceId in placements FAILS LOUD.
// - Uses UnityEngine.Vector3 assuming Unity-hosted server; swap to engine-agnostic
//   position type if server runtime is decoupled later.

using System;
using System.Collections.Generic;
using UnityEngine;
using Caelmor.Engine;

namespace Caelmor.Economy.ResourceNodes
{
    public enum ResourceNodeAvailability : byte
    {
        Available = 0,
        Depleted = 1
    }

    /// <summary>
    /// Stable placement data supplied by world/zone content.
    /// NodeInstanceId MUST originate from content placement.
    /// Runtime must never generate NodeInstanceIds.
    /// </summary>
    public readonly struct ResourceNodePlacement
    {
        public readonly int NodeInstanceId;
        public readonly string ResourceNodeKey;
        public readonly Vector3 WorldPosition;

        public ResourceNodePlacement(int nodeInstanceId, string resourceNodeKey, Vector3 worldPosition)
        {
            NodeInstanceId = nodeInstanceId;
            ResourceNodeKey = resourceNodeKey ?? throw new ArgumentNullException(nameof(resourceNodeKey));
            WorldPosition = worldPosition;
        }
    }

    /// <summary>
    /// Persisted runtime override (no I/O here).
    /// RespawnTicksRemaining is persisted as ticks-remaining (Stage 7.5 locked decision).
    /// </summary>
    public readonly struct PersistedNodeOverride
    {
        public readonly int NodeInstanceId;
        public readonly ResourceNodeAvailability Availability;
        public readonly int RespawnTicksRemaining;

        public PersistedNodeOverride(int nodeInstanceId, ResourceNodeAvailability availability, int respawnTicksRemaining)
        {
            NodeInstanceId = nodeInstanceId;
            Availability = availability;
            RespawnTicksRemaining = respawnTicksRemaining;
        }
    }

    /// <summary>
    /// Runtime node instance (world-owned).
    /// Implemented as a class to avoid copy-on-write errors.
    /// </summary>
    internal sealed class ResourceNodeInstance
    {
        public int NodeInstanceId;
        public string ResourceNodeKey;
        public Vector3 WorldPosition;

        public ResourceNodeAvailability Availability;
        public int RespawnTicksRemaining;

        // Index into _depletedNodeIds for O(1) removal; -1 if not depleted.
        public int DepletedListIndex = -1;
    }

    /// <summary>
    /// Stage 7.1 implementation:
    /// - Tracks node availability
    /// - Tick-based respawn using ticks-remaining
    /// - Server-only depletion API
    /// - Persistence apply/export (no I/O)
    /// </summary>
    public sealed class ResourceNodeRuntimeSystem :
        IServerTickListener,
        IZoneLifecycleListener
    {
        private readonly Dictionary<int, ResourceNodeInstance> _nodesById;
        private readonly List<int> _depletedNodeIds;

        private string? _activeZoneId;

        public ResourceNodeRuntimeSystem(int initialCapacity = 512)
        {
            _nodesById = new Dictionary<int, ResourceNodeInstance>(initialCapacity);
            _depletedNodeIds = new List<int>(Math.Max(32, initialCapacity / 4));
        }

        /// <summary>
        /// Initialize runtime state for a zone.
        /// Placements must contain unique NodeInstanceIds or initialization fails loudly.
        /// </summary>
        public void InitializeForZone(
            string zoneId,
            IReadOnlyList<ResourceNodePlacement> placements,
            IReadOnlyList<PersistedNodeOverride>? persistedOverrides)
        {
            if (zoneId == null) throw new ArgumentNullException(nameof(zoneId));
            if (placements == null) throw new ArgumentNullException(nameof(placements));

            _activeZoneId = zoneId;
            _nodesById.Clear();
            _depletedNodeIds.Clear();

            // Build instances from placements (stable identity).
            for (int i = 0; i < placements.Count; i++)
            {
                var p = placements[i];

                if (_nodesById.ContainsKey(p.NodeInstanceId))
                {
                    throw new InvalidOperationException(
                        $"Duplicate NodeInstanceId detected during zone init. " +
                        $"Zone='{zoneId}', NodeInstanceId={p.NodeInstanceId}");
                }

                _nodesById.Add(
                    p.NodeInstanceId,
                    new ResourceNodeInstance
                    {
                        NodeInstanceId = p.NodeInstanceId,
                        ResourceNodeKey = p.ResourceNodeKey,
                        WorldPosition = p.WorldPosition,
                        Availability = ResourceNodeAvailability.Available,
                        RespawnTicksRemaining = 0,
                        DepletedListIndex = -1
                    });
            }

            // Apply persisted runtime overrides (if any).
            if (persistedOverrides != null)
            {
                for (int i = 0; i < persistedOverrides.Count; i++)
                {
                    ApplyOverrideInternal(persistedOverrides[i]);
                }
            }
        }

        /// <summary>
        /// Export runtime overrides for persistence snapshots.
        /// Only depleted nodes require persistence.
        /// </summary>
        public void GetSaveSnapshot(List<PersistedNodeOverride> outOverrides)
        {
            if (outOverrides == null) throw new ArgumentNullException(nameof(outOverrides));
            outOverrides.Clear();

            for (int i = 0; i < _depletedNodeIds.Count; i++)
            {
                int nodeId = _depletedNodeIds[i];
                if (_nodesById.TryGetValue(nodeId, out var node) &&
                    node.Availability == ResourceNodeAvailability.Depleted)
                {
                    outOverrides.Add(
                        new PersistedNodeOverride(
                            node.NodeInstanceId,
                            ResourceNodeAvailability.Depleted,
                            node.RespawnTicksRemaining));
                }
            }
        }

        /// <summary>
        /// Server-only depletion API.
        /// Caller supplies respawnTicksRemaining from tuning/policy provider.
        /// </summary>
        public bool TryDepleteNode(int nodeInstanceId, int respawnTicksRemaining)
        {
            if (respawnTicksRemaining <= 0)
                throw new ArgumentOutOfRangeException(
                    nameof(respawnTicksRemaining),
                    "respawnTicksRemaining must be > 0.");

            if (!_nodesById.TryGetValue(nodeInstanceId, out var node))
                return false;

            if (node.Availability == ResourceNodeAvailability.Depleted)
                return false;

            node.Availability = ResourceNodeAvailability.Depleted;
            node.RespawnTicksRemaining = respawnTicksRemaining;

            AddToDepletedList(node);
            return true;
        }

        /// <summary>
        /// Read-only availability query for downstream systems.
        /// </summary>
        public bool TryGetNodeAvailability(
            int nodeInstanceId,
            out ResourceNodeAvailability availability)
        {
            if (_nodesById.TryGetValue(nodeInstanceId, out var node))
            {
                availability = node.Availability;
                return true;
            }

            availability = ResourceNodeAvailability.Available;
            return false;
        }

        /// <summary>
        /// Authoritative 10 Hz tick update.
        /// Decrements respawn ticks for depleted nodes only.
        /// </summary>
        public void OnServerTick(int tick)
        {
            for (int i = _depletedNodeIds.Count - 1; i >= 0; i--)
            {
                int nodeId = _depletedNodeIds[i];

                if (!_nodesById.TryGetValue(nodeId, out var node))
                {
                    _depletedNodeIds.RemoveAt(i);
                    continue;
                }

                if (node.Availability != ResourceNodeAvailability.Depleted)
                {
                    RemoveFromDepletedList(node, i);
                    continue;
                }

                node.RespawnTicksRemaining--;

                if (node.RespawnTicksRemaining <= 0)
                {
                    node.Availability = ResourceNodeAvailability.Available;
                    node.RespawnTicksRemaining = 0;
                    RemoveFromDepletedList(node, i);
                }
            }
        }

        // ---- Zone lifecycle hooks ----

        public void OnZoneLoaded(string zoneId)
        {
            // Intentionally empty.
            // Engine must call InitializeForZone with placements + overrides.
        }

        public void OnZoneUnloading(string zoneId)
        {
            if (_activeZoneId == zoneId)
            {
                _activeZoneId = null;
                _nodesById.Clear();
                _depletedNodeIds.Clear();
            }
        }

        // ---- Internal helpers ----

        private void ApplyOverrideInternal(in PersistedNodeOverride ov)
        {
            if (!_nodesById.TryGetValue(ov.NodeInstanceId, out var node))
                return; // Safe ignore: content mismatch

            if (ov.Availability == ResourceNodeAvailability.Depleted &&
                ov.RespawnTicksRemaining > 0)
            {
                node.Availability = ResourceNodeAvailability.Depleted;
                node.RespawnTicksRemaining = ov.RespawnTicksRemaining;
                AddToDepletedList(node);
            }
            else
            {
                node.Availability = ResourceNodeAvailability.Available;
                node.RespawnTicksRemaining = 0;
                RemoveFromDepletedListIfPresent(node);
            }
        }

        private void AddToDepletedList(ResourceNodeInstance node)
        {
            if (node.DepletedListIndex != -1)
                return;

            node.DepletedListIndex = _depletedNodeIds.Count;
            _depletedNodeIds.Add(node.NodeInstanceId);
        }

        private void RemoveFromDepletedListIfPresent(ResourceNodeInstance node)
        {
            if (node.DepletedListIndex == -1)
                return;

            RemoveFromDepletedList(node, node.DepletedListIndex);
        }

        private void RemoveFromDepletedList(ResourceNodeInstance node, int index)
        {
            int lastIndex = _depletedNodeIds.Count - 1;
            int lastNodeId = _depletedNodeIds[lastIndex];

            _depletedNodeIds[index] = lastNodeId;
            _depletedNodeIds.RemoveAt(lastIndex);

            if (_nodesById.TryGetValue(lastNodeId, out var swapped))
            {
                swapped.DepletedListIndex = index;
            }

            node.DepletedListIndex = -1;
        }
    }
}
