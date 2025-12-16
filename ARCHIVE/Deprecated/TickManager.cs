using System;
using UnityEngine;

namespace Caelmor.VerticalSlice
{
    /// <summary>
    /// Host-only authoritative tick loop at fixed interval (10 Hz).
    /// Drives movement, AI, combat, world simulation, crafting, persistence hooks,
    /// and network snapshots according to TickManager_Design.md.
    /// </summary>
    public class TickManager : MonoBehaviour
    {
        public static TickManager Instance { get; private set; }

        /// <summary>
        /// Fired at the start of each tick, before any simulation runs.
        /// </summary>
        public event Action<long> OnBeforeTick;

        /// <summary>
        /// Fired at the end of each tick after simulation and snapshot generation.
        /// Primary hook for tick-driven systems.
        /// </summary>
        public event Action<long> OnTick;

        /// <summary>
        /// Fired after network snapshot broadcast, mainly for debug / tooling.
        /// </summary>
        public event Action<long> OnAfterSnapshot;

        private const float AUTOSAVE_INTERVAL_SECONDS = 300f; // 5 minutes

        private float _accumulator;
        private long  _tickIndex;

        private float _timeSinceLastAutosave;
        private float _timeSinceLastHpSync;

        /// <summary>
        /// True when the authoritative loop is running on the host.
        /// </summary>
        public bool IsRunning { get; private set; }

        // References (wired at bootstrap)
        public WorldManager    WorldManager    { get; set; }
        public CombatSystem    CombatSystem    { get; set; }
        public StatsSystem     StatsSystem     { get; set; }
        public SkillSystem     SkillSystem     { get; set; }
        public CraftingSystem  CraftingSystem  { get; set; }
        public SaveSystem      SaveSystem      { get; set; }
        public NetworkManager  NetworkManager  { get; set; }

        /// <summary>
        /// Current global tick index (monotonically increasing).
        /// </summary>
        public long CurrentTickIndex => _tickIndex;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
        }

        /// <summary>
        /// Called on host when ready to start server-authoritative simulation.
        /// </summary>
        public void StartAuthoritativeLoop()
        {
            IsRunning = true;
            _accumulator           = 0f;
            _timeSinceLastAutosave = 0f;
            _timeSinceLastHpSync   = 0f;
        }

        private void Update()
        {
            if (!IsRunning)
                return;

            float dt = Time.deltaTime;
            _accumulator           += dt;
            _timeSinceLastAutosave += dt;
            _timeSinceLastHpSync   += dt;

            // Fixed 10 Hz tick using accumulated delta time.
            while (_accumulator >= GameConstants.TICK_INTERVAL_SECONDS)
            {
                _accumulator -= GameConstants.TICK_INTERVAL_SECONDS;
                StepTick();
            }

            // Autosave (outside tick execution; SaveSystem must avoid blocking I/O).
            if (_timeSinceLastAutosave >= AUTOSAVE_INTERVAL_SECONDS)
            {
                _timeSinceLastAutosave = 0f;
                if (SaveSystem != null)
                {
                    SaveSystem.SaveWorld();
                    SaveSystem.SaveAllConnectedPlayers();
                }
            }

            // Periodic HP sync (coarser than transforms).
            if (_timeSinceLastHpSync >= GameConstants.HP_SYNC_INTERVAL_SECONDS)
            {
                _timeSinceLastHpSync = 0f;

                if (WorldManager != null && NetworkManager != null)
                {
                    var hpSnapshot = WorldManager.BuildHpSnapshot();
                    NetworkManager.BroadcastHpSnapshot(hpSnapshot);
                }
            }
        }

        /// <summary>
        /// Executes a single deterministic simulation tick.
        /// Order matches TickManager_Design.md:
        /// 1) Input, 2) Movement, 3) AI, 4) Combat, 5) HP/XP, 6) World, 7) Persistence flags,
        /// 8) Network snapshot, 9) Tick events.
        /// </summary>
        private void StepTick()
        {
            _tickIndex++;

            // 0. Pre-tick hook
            OnBeforeTick?.Invoke(_tickIndex);

            // 1. Input collection
            InputBatch inputBatch = NetworkManager != null
                ? NetworkManager.DrainBufferedInputs()
                : new InputBatch();

            // 2. Movement simulation (players)
            if (WorldManager != null)
            {
                WorldManager.ApplyPlayerMovementInputs(inputBatch.MovementCommands);
            }

            // 3. AI behavior execution
            if (WorldManager != null)
            {
                WorldManager.UpdateAIControllers(_tickIndex, GameConstants.TICK_INTERVAL_SECONDS);
            }

            // 4 & 5. Combat timers, attack resolution, HP/Death/XP
            // (CombatSystem encapsulates StatsSystem + SkillSystem interactions).
            if (CombatSystem != null)
            {
                CombatSystem.ProcessAttackTimersAndIntents(_tickIndex, inputBatch.AttackCommands);
            }

            // 6. World state updates (nodes, crafting, flags)
            if (WorldManager != null)
            {
                WorldManager.UpdateWorldState(_tickIndex);
            }

            if (CraftingSystem != null)
            {
                CraftingSystem.ProcessCraftingJobs(_tickIndex);
            }

            // 7. Persistence hooks (dirty flags only; no I/O)
            if (SaveSystem != null && WorldManager != null)
            {
                SaveSystem.MarkDirtyFromWorld(WorldManager);
                SaveSystem.MarkDirtyFromPlayers(WorldManager.GetPlayerEntities());
            }

            // 8. Network snapshot generation & broadcast
            if (WorldManager != null && NetworkManager != null)
            {
                TransformSnapshot transformSnapshot = WorldManager.BuildTransformSnapshot();
                NetworkManager.BroadcastTransformSnapshot(transformSnapshot);
            }

            // 9. Tick events for subsystems & debug
            OnTick?.Invoke(_tickIndex);
            OnAfterSnapshot?.Invoke(_tickIndex);
        }
    }
}
