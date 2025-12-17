using System;
using System.Collections.Generic;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.WorldSimulation;

namespace Caelmor.Runtime.WorldState
{
    /// <summary>
    /// Deterministic runtime entity registry shared by TickSystem and WorldSimulationCore.
    /// Provides explicit register/unregister/despawn flows and prevents entity leakage across zone unloads.
    /// </summary>
    public sealed class DeterministicEntityRegistry : IEntityRegistry, ISimulationEntityIndex, IDisposable
    {
        private readonly object _gate = new object();
        private readonly Dictionary<EntityHandle, ZoneId> _zoneByEntity = new Dictionary<EntityHandle, ZoneId>(256);
        private readonly Dictionary<ZoneId, List<EntityHandle>> _entitiesByZone = new Dictionary<ZoneId, List<EntityHandle>>(32);
        private readonly List<EntityHandle> _ordered = new List<EntityHandle>(256);

        private EntityHandle[] _snapshot = Array.Empty<EntityHandle>();
        private bool _dirty = true;

        /// <summary>
        /// Registers a new entity in a specific zone. Deterministic and idempotent: returns false when already registered.
        /// </summary>
        public bool Register(EntityHandle entity, ZoneId zone)
        {
            if (!entity.IsValid || zone.Value <= 0)
                return false;

            lock (_gate)
            {
                if (_zoneByEntity.ContainsKey(entity))
                    return false;

                _zoneByEntity[entity] = zone;
                AddToZone(zone, entity);
                _ordered.Add(entity);
                _dirty = true;
                return true;
            }
        }

        /// <summary>
        /// Removes a single entity from the registry. Returns false if not present.
        /// </summary>
        public bool Unregister(EntityHandle entity)
        {
            lock (_gate)
            {
                if (!_zoneByEntity.TryGetValue(entity, out var zone))
                    return false;

                _zoneByEntity.Remove(entity);
                RemoveFromZone(zone, entity);
                _ordered.Remove(entity);
                _dirty = true;
                return true;
            }
        }

        /// <summary>
        /// Despawns all entities for a specific zone. Returns the number removed.
        /// </summary>
        public int DespawnZone(ZoneId zone)
        {
            if (zone.Value <= 0)
                return 0;

            lock (_gate)
            {
                if (!_entitiesByZone.TryGetValue(zone, out var list))
                    return 0;

                var removed = 0;
                for (int i = list.Count - 1; i >= 0; i--)
                {
                    var entity = list[i];
                    _zoneByEntity.Remove(entity);
                    _ordered.Remove(entity);
                    removed++;
                }

                _entitiesByZone.Remove(zone);
                _dirty = true;
                return removed;
            }
        }

        /// <summary>
        /// Clears all entities from the registry (server shutdown).
        /// </summary>
        public void ClearAll()
        {
            lock (_gate)
            {
                _zoneByEntity.Clear();
                _entitiesByZone.Clear();
                _ordered.Clear();
                _snapshot = Array.Empty<EntityHandle>();
                _dirty = true;
            }
        }

        public EntityHandle[] SnapshotEntitiesDeterministic()
        {
            lock (_gate)
            {
                if (_dirty)
                    RebuildSnapshot();

                return _snapshot;
            }
        }

        public void Dispose()
        {
            ClearAll();
        }

        private void AddToZone(ZoneId zone, EntityHandle entity)
        {
            if (!_entitiesByZone.TryGetValue(zone, out var list))
            {
                list = new List<EntityHandle>(8);
                _entitiesByZone[zone] = list;
            }

            list.Add(entity);
        }

        private void RemoveFromZone(ZoneId zone, EntityHandle entity)
        {
            if (_entitiesByZone.TryGetValue(zone, out var list))
            {
                list.Remove(entity);
                if (list.Count == 0)
                    _entitiesByZone.Remove(zone);
            }
        }

        private void RebuildSnapshot()
        {
            _ordered.Sort((a, b) => a.Value.CompareTo(b.Value));
            if (_snapshot.Length != _ordered.Count)
                _snapshot = new EntityHandle[_ordered.Count];

            for (int i = 0; i < _ordered.Count; i++)
                _snapshot[i] = _ordered[i];

            _dirty = false;
        }
    }
}
