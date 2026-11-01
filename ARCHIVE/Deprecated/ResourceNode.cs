using System;
using UnityEngine;

namespace Caelmor.VerticalSlice
{
    /// <summary>
    /// Server-authoritative resource node for the Vertical Slice.
    ///
    /// Responsibilities:
    /// - Handles gather interactions from players
    /// - Enforces skill requirements
    /// - Generates yields (min/max RNG)
    /// - Awards XP based on node type (per VS balance spec)
    /// - Handles respawn timers (host-clock or tick-based)
    /// - Provides persistence-ready state (isDepleted, respawnTick)
    ///
    /// NOTE:
    /// Must only run on HOST. Clients only receive visuals via snapshot or RPC.
    /// </summary>
    public class ResourceNode : MonoBehaviour
    {
        // --------------------------------------------------------------------
        // Node Definition (loaded from VS_ResourceNodes.json)
        // --------------------------------------------------------------------
        public string NodeId;
        public string ResourceItemId;
        public string ResourceType;     // ore, wood, special (wildlife), etc.
        public int YieldMin;
        public int YieldMax;
        public int RespawnSeconds;
        public string SkillId;          // mining, woodcutting, hunting
        public int SkillMinLevel;

        // --------------------------------------------------------------------
        // Node State (host authoritative)
        // --------------------------------------------------------------------
        public bool IsDepleted { get; private set; }
        private long _respawnTick;      // Tick index when node becomes available again
        private float _cooldownEndTime; // Real-time option (fallback)
        private float _lastInteractTime; // Anti-macro debounce

        private const float INTERACT_DEBOUNCE_SEC = 1.0f;

        // External systems
        public InventorySystem InventorySystem { get; set; }
        public SkillSystem SkillSystem { get; set; }
        public WorldManager WorldManager { get; set; }

        // XP table per VS balance spec
        private const int XP_MINING = 3;        // Iron Vein
        private const int XP_WOODCUTTING = 2;   // Tree
        private const int XP_HUNTING = 2;       // Wildlife harvest

        private long RespawnTick => _respawnTick;
        private TickManager TickMgr => TickManager.Instance;

        // --------------------------------------------------------------------
        // Host-only update (TickManager integration)
        // --------------------------------------------------------------------
        private void Update()
        {
            if (TickMgr == null || !TickMgr.IsRunning)
                return;

            if (IsDepleted && TickMgr.CurrentTickIndex >= _respawnTick)
            {
                Respawn();
            }
        }

        // --------------------------------------------------------------------
        // Host-side gather attempt
        // --------------------------------------------------------------------
        public void TryHarvest(string playerId)
        {
            if (!IsHost())
                return;

            // Anti-macro debounce
            if (Time.time - _lastInteractTime < INTERACT_DEBOUNCE_SEC)
                return;

            _lastInteractTime = Time.time;

            if (IsDepleted)
                return;

            var entity = WorldManager.GetEntity(playerId);
            if (entity == null)
                return;

            if (!MeetsSkillRequirement(entity))
                return;

            // Generate random yield
            int amount = UnityEngine.Random.Range(YieldMin, YieldMax + 1);

            // Try to add to inventory
            bool added = InventorySystem.TryAddItem(entity, ResourceItemId, amount, out int leftover);

            // If overflow, drop into the world (optional)
            if (leftover > 0)
            {
                // Future: spawn world drop entity
            }

            // Award XP
            AwardGatherXP(entity);

            // Mark node depleted
            Deplete();
        }

        // --------------------------------------------------------------------
        // Skill requirement enforcement
        // --------------------------------------------------------------------
        private bool MeetsSkillRequirement(Entity entity)
        {
            if (entity == null || entity.Skills == null)
                return false;

            // VS skills exist in SkillComponent as map skillId → level
            int level = entity.Skills.GetLevel(SkillId);

            return level >= SkillMinLevel;
        }

        // --------------------------------------------------------------------
        // XP awarding
        // --------------------------------------------------------------------
        private void AwardGatherXP(Entity entity)
        {
            switch (SkillId)
            {
                case "mining":
                    SkillSystem.AwardXp(entity, "mining", XP_MINING);
                    break;

                case "woodcutting":
                    SkillSystem.AwardXp(entity, "woodcutting", XP_WOODCUTTING);
                    break;

                case "hunting":
                    SkillSystem.AwardXp(entity, "hunting", XP_HUNTING);
                    break;
            }
        }

        // --------------------------------------------------------------------
        // Depletion + respawn
        // --------------------------------------------------------------------
        private void Deplete()
        {
            IsDepleted = true;

            if (TickMgr != null && TickMgr.IsRunning)
            {
                long now = TickMgr.CurrentTickIndex;
                int respawnTicks = Mathf.RoundToInt(RespawnSeconds / GameConstants.TICK_INTERVAL_SECONDS);
                _respawnTick = now + respawnTicks;
            }

            // Real-time fallback (only used if TickManager not available)
            _cooldownEndTime = Time.time + RespawnSeconds;

            UpdateNodeVisual(false);
        }

        private void Respawn()
        {
            IsDepleted = false;
            _respawnTick = -1;
            UpdateNodeVisual(true);
        }

        // --------------------------------------------------------------------
        // Persistence Support
        // --------------------------------------------------------------------
        public ResourceNodeSaveData ToSaveData()
        {
            return new ResourceNodeSaveData
            {
                NodeId = this.NodeId,
                IsDepleted = this.IsDepleted,
                RespawnTick = this._respawnTick,
                CooldownEndTime = this._cooldownEndTime
            };
        }

        public void LoadFromSave(ResourceNodeSaveData data)
        {
            if (data == null)
                return;

            IsDepleted = data.IsDepleted;
            _respawnTick = data.RespawnTick;
            _cooldownEndTime = data.CooldownEndTime;

            UpdateNodeVisual(!IsDepleted);
        }

        // --------------------------------------------------------------------
        // Visual toggle (placeholder for VS)
        // --------------------------------------------------------------------
        private void UpdateNodeVisual(bool visible)
        {
            // Simple VS implementation: enable/disable mesh renderer
            var mesh = GetComponentInChildren<MeshRenderer>();
            if (mesh != null)
                mesh.enabled = visible;
        }

        // Host check
        private bool IsHost()
        {
            return NetworkManager.Instance != null &&
                   NetworkManager.Instance.IsHost;
        }
    }

    // ------------------------------------------------------------------------
    // Save Data Struct
    // ------------------------------------------------------------------------
    [Serializable]
    public class ResourceNodeSaveData
    {
        public string NodeId;
        public bool IsDepleted;
        public long RespawnTick;
        public float CooldownEndTime;
    }
}
