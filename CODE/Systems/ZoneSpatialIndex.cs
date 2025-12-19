using System;
using System.Collections.Generic;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Tick;

namespace Caelmor.Runtime.InterestManagement
{
    /// <summary>
    /// Integer grid position for zone-local spatial indexing. Coordinates are deterministic
    /// and tick-thread only; no floating point math is performed in the index.
    /// </summary>
    public readonly struct ZonePosition : IEquatable<ZonePosition>
    {
        public readonly int X;
        public readonly int Y;

        public ZonePosition(int x, int y)
        {
            X = x;
            Y = y;
        }

        public bool Equals(ZonePosition other) => X == other.X && Y == other.Y;
        public override bool Equals(object obj) => obj is ZonePosition other && Equals(other);
        public override int GetHashCode() => HashCode.Combine(X, Y);
    }

    /// <summary>
    /// Immutable interest query used for AOI and nearby target selection.
    /// </summary>
    public readonly struct ZoneInterestQuery
    {
        public ZoneInterestQuery(ZoneId zone, ZonePosition center, int range)
        {
            Zone = zone;
            Center = center;
            Range = Math.Max(0, range);
        }

        public ZoneId Zone { get; }
        public ZonePosition Center { get; }
        public int Range { get; }
    }

    /// <summary>
    /// Deterministic spatial hash/grid for per-zone entity lookups.
    /// </summary>
    public sealed class ZoneSpatialIndex
    {
        private readonly int _cellSize;
        private readonly Dictionary<CellCoord, CellBucket> _cells;
        private readonly Dictionary<EntityHandle, CellCoord> _locations;

        public ZoneSpatialIndex(int cellSize, int initialCapacity = 128)
        {
            if (cellSize <= 0) throw new ArgumentOutOfRangeException(nameof(cellSize));
            _cellSize = cellSize;
            _cells = new Dictionary<CellCoord, CellBucket>(initialCapacity);
            _locations = new Dictionary<EntityHandle, CellCoord>(initialCapacity);
        }

        /// <summary>
        /// Adds a new entity or updates its zone/position deterministically.
        /// </summary>
        public void Upsert(EntityHandle entity, ZoneId zone, ZonePosition position)
        {
            TickThreadAssert.AssertTickThread();
            if (!entity.IsValid)
                throw new ArgumentOutOfRangeException(nameof(entity));
            if (zone.Value <= 0)
                throw new ArgumentOutOfRangeException(nameof(zone));

            var cell = GetCellCoord(zone, position);
            if (_locations.TryGetValue(entity, out var existingCell))
            {
                if (existingCell.Equals(cell))
                    return;

                if (_cells.TryGetValue(existingCell, out var existingBucket))
                {
                    existingBucket.Remove(entity);
                    _cells[existingCell] = existingBucket;
                }
            }

            if (!_cells.TryGetValue(cell, out var bucket))
                bucket = new CellBucket(initialCapacity: 4);

            bucket.Add(entity);
            _cells[cell] = bucket;
            _locations[entity] = cell;
        }

        /// <summary>
        /// Removes an entity from the spatial index. No-op if not present.
        /// </summary>
        public void Remove(EntityHandle entity)
        {
            TickThreadAssert.AssertTickThread();
            if (!_locations.TryGetValue(entity, out var cell))
                return;

            if (_cells.TryGetValue(cell, out var bucket))
            {
                bucket.Remove(entity);
                _cells[cell] = bucket;
            }

            _locations.Remove(entity);
        }

        /// <summary>
        /// Removes all entities tracked in the specified zone. Intended for zone unload cleanup.
        /// </summary>
        public void RemoveZone(ZoneId zone)
        {
            TickThreadAssert.AssertTickThread();
            if (zone.Value <= 0)
                return;

            var toRemove = new List<EntityHandle>();

            foreach (var kvp in _locations)
            {
                if (kvp.Value.Zone.Equals(zone))
                    toRemove.Add(kvp.Key);
            }

            for (int i = 0; i < toRemove.Count; i++)
                Remove(toRemove[i]);
        }

        /// <summary>
        /// Clears all zones and entities from the spatial index. Used on server shutdown.
        /// </summary>
        public void Clear()
        {
            TickThreadAssert.AssertTickThread();
            _cells.Clear();
            _locations.Clear();
        }

        /// <summary>
        /// Queries entities within range of a position in the same zone. Results are appended to the
        /// provided list to avoid per-tick allocations; caller is responsible for clearing when appropriate.
        /// </summary>
        public void Query(ZoneInterestQuery query, List<EntityHandle> results)
        {
            if (results is null) throw new ArgumentNullException(nameof(results));
            if (query.Zone.Value <= 0)
                return;

            var cellCenter = GetCellCoord(query.Zone, query.Center);
            var cellRange = (query.Range + _cellSize - 1) / _cellSize; // ceil

            for (int x = cellCenter.CellX - cellRange; x <= cellCenter.CellX + cellRange; x++)
            {
                for (int y = cellCenter.CellY - cellRange; y <= cellCenter.CellY + cellRange; y++)
                {
                    var key = new CellCoord(query.Zone, x, y);
                    if (_cells.TryGetValue(key, out var bucket))
                    {
                        bucket.AppendTo(results);
                    }
                }
            }
        }

        private CellCoord GetCellCoord(ZoneId zone, ZonePosition position)
        {
            var cellX = position.X / _cellSize;
            var cellY = position.Y / _cellSize;
            return new CellCoord(zone, cellX, cellY);
        }

        private readonly struct CellCoord : IEquatable<CellCoord>
        {
            public readonly ZoneId Zone;
            public readonly int CellX;
            public readonly int CellY;

            public CellCoord(ZoneId zone, int cellX, int cellY)
            {
                Zone = zone;
                CellX = cellX;
                CellY = cellY;
            }

            public bool Equals(CellCoord other) => Zone.Equals(other.Zone) && CellX == other.CellX && CellY == other.CellY;
            public override bool Equals(object obj) => obj is CellCoord other && Equals(other);
            public override int GetHashCode() => HashCode.Combine(Zone, CellX, CellY);
        }

        private struct CellBucket
        {
            private EntityHandle[] _entities;
            private int _count;

            public CellBucket(int initialCapacity)
            {
                _entities = initialCapacity > 0 ? new EntityHandle[initialCapacity] : Array.Empty<EntityHandle>();
                _count = 0;
            }

            public void Add(EntityHandle entity)
            {
                EnsureCapacity(_count + 1);
                _entities[_count++] = entity;
            }

            public void Remove(EntityHandle entity)
            {
                for (int i = 0; i < _count; i++)
                {
                    if (_entities[i].Equals(entity))
                    {
                        for (int j = i + 1; j < _count; j++)
                            _entities[j - 1] = _entities[j];

                        _entities[--_count] = default;
                        return;
                    }
                }
            }

            public void AppendTo(List<EntityHandle> destination)
            {
                for (int i = 0; i < _count; i++)
                    destination.Add(_entities[i]);
            }

            private void EnsureCapacity(int required)
            {
                if (_entities.Length >= required)
                    return;

                var next = _entities.Length == 0 ? required : _entities.Length;
                while (next < required)
                    next *= 2;

                Array.Resize(ref _entities, next);
            }
        }
    }

    internal sealed class EntityHandleComparer : IComparer<EntityHandle>
    {
        public static readonly EntityHandleComparer Instance = new EntityHandleComparer();

        public int Compare(EntityHandle x, EntityHandle y) => x.Value.CompareTo(y.Value);
    }
}
