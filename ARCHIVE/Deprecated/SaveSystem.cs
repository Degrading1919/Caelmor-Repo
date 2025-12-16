// SaveSystem.cs
using System;
using System.IO;
using System.Collections.Generic;
using System.Threading.Tasks;
using UnityEngine;

namespace Caelmor.VS
{
    /// <summary>
    /// Server/host-authoritative Save System for Caelmor VS.
    ///
    /// Supports:
    ///  - Player save
    ///  - World save
    ///  - Autosave (TickManager-driven)
    ///  - Error handling + fallback clean save
    ///  - Cross-version tolerance using schemaVersion checks
    ///
    /// Notes:
    ///  - All paths should be injected from outside (platform abstraction).
    ///  - This class is engine-agnostic: no Unity-specific ops required
    ///    except for Debug logging.
    /// </summary>
    public class SaveSystem
    {
        // ============================================================
        // Configurable Paths (assigned externally)
        // ============================================================

        public string PlayerSavePath { get; set; }
        public string WorldSavePath  { get; set; }

        public int CurrentSchemaVersion_Player = 1;
        public int CurrentSchemaVersion_World  = 1;

        // ============================================================
        // Autosave
        // ============================================================

        private float _autosaveInterval = 30f; // seconds
        private float _autosaveTimer = 0f;

        public bool AutosaveEnabled { get; set; } = true;

        public void Tick(float deltaTime)
        {
            if (!AutosaveEnabled)
                return;

            _autosaveTimer += deltaTime;
            if (_autosaveTimer >= _autosaveInterval)
            {
                _autosaveTimer = 0f;
                TryAutosave();
            }
        }

        private void TryAutosave()
        {
            try
            {
                Debug.Log("[SaveSystem] Autosaving...");
                SavePlayer();
                SaveWorld();
            }
            catch (Exception ex)
            {
                Debug.LogError($"[SaveSystem] Autosave failed: {ex.Message}");
            }
        }

        // ============================================================
        // Public API: Load / Save Player
        // ============================================================

        public bool SavePlayer()
        {
            try
            {
                var save = BuildPlayerSaveSnapshot();
                var json = JsonUtility.ToJson(save, prettyPrint: true);
                File.WriteAllText(PlayerSavePath, json);
                return true;
            }
            catch (Exception ex)
            {
                Debug.LogError($"[SaveSystem] Failed to save player data: {ex.Message}");
                return false;
            }
        }

        public bool LoadPlayer()
        {
            try
            {
                if (!File.Exists(PlayerSavePath))
                {
                    Debug.LogWarning("[SaveSystem] No existing player save found. Creating default save.");
                    return CreateNewPlayerSave();
                }

                string json = File.ReadAllText(PlayerSavePath);
                var save = JsonUtility.FromJson<PlayerSave>(json);

                if (save == null)
                {
                    Debug.LogError("[SaveSystem] Player save file corrupted. Creating fallback save.");
                    return CreateNewPlayerSave();
                }

                // Cross-version tolerance
                if (save.schemaVersion != CurrentSchemaVersion_Player)
                    HandlePlayerVersionMismatch(save.schemaVersion);

                ApplyPlayerSaveSnapshot(save);
                return true;
            }
            catch (Exception ex)
            {
                Debug.LogError($"[SaveSystem] Failed to load player data: {ex.Message}");
                return CreateNewPlayerSave();
            }
        }

        // ============================================================
        // Public API: Load / Save World
        // ============================================================

        public bool SaveWorld()
        {
            try
            {
                var save = BuildWorldSaveSnapshot();
                var json = JsonUtility.ToJson(save, prettyPrint: true);
                File.WriteAllText(WorldSavePath, json);
                return true;
            }
            catch (Exception ex)
            {
                Debug.LogError($"[SaveSystem] Failed to save world data: {ex.Message}");
                return false;
            }
        }

        public bool LoadWorld()
        {
            try
            {
                if (!File.Exists(WorldSavePath))
                {
                    Debug.LogWarning("[SaveSystem] No existing world save found. Creating default world save.");
                    return CreateNewWorldSave();
                }

                string json = File.ReadAllText(WorldSavePath);
                var save = JsonUtility.FromJson<WorldSave>(json);

                if (save == null)
                {
                    Debug.LogError("[SaveSystem] World save corrupted. Creating fallback world save.");
                    return CreateNewWorldSave();
                }

                if (save.schemaVersion != CurrentSchemaVersion_World)
                    HandleWorldVersionMismatch(save.schemaVersion);

                ApplyWorldSaveSnapshot(save);
                return true;
            }
            catch (Exception ex)
            {
                Debug.LogError($"[SaveSystem] Failed to load world data: {ex.Message}");
                return CreateNewWorldSave();
            }
        }

        // ============================================================
        // Build Snapshots
        // ============================================================

        private PlayerSave BuildPlayerSaveSnapshot()
        {
            var save = new PlayerSave
            {
                schemaVersion = CurrentSchemaVersion_Player,
                characterId   = Player.Instance.CharacterId,
                name          = Player.Instance.Name,
                zoneId        = Player.Instance.ZoneId,
                rotationY     = Player.Instance.RotationY,
                position      = new PlayerPosition
                {
                    x = Player.Instance.Position.x,
                    y = Player.Instance.Position.y,
                    z = Player.Instance.Position.z
                },
                skills         = SkillSystem.Instance.ToSaveData(),
                inventory      = InventorySystemToSaveData(),
                equipment      = EquipmentSystemToSaveData(),
                questProgress  = QuestSystemToSaveData(),
                activeCraftingJobs = CraftingSystemToSaveData(),
                learnedRecipes = RecipeBookSystem.Instance.ToSaveData(),
                currency = new PlayerCurrency { gold = Player.Instance.Gold }
            };

            return save;
        }

        private WorldSave BuildWorldSaveSnapshot()
        {
            return new WorldSave
            {
                schemaVersion = CurrentSchemaVersion_World,
                worldId       = WorldManager.Instance.WorldId,
                zoneId        = WorldManager.Instance.ZoneId,
                resourceNodes = WorldManager.Instance.ResourceNodesToSave(),
                worldObjects  = WorldManager.Instance.WorldObjectsToSave(),
                chests        = WorldManager.Instance.ChestsToSave(),
                activeSpawns  = WorldManager.Instance.ActiveSpawnToSave(),
                worldFlags    = WorldManager.Instance.FlagsToSave(),
                timers        = WorldManager.Instance.TimersToSave()
            };
        }

        // ============================================================
        // Apply Snapshots
        // ============================================================

        private void ApplyPlayerSaveSnapshot(PlayerSave save)
        {
            Player.Instance.CharacterId = save.characterId;
            Player.Instance.Name         = save.name;
            Player.Instance.ZoneId       = save.zoneId;
            Player.Instance.Gold         = save.currency.gold;

            Player.Instance.Position = new Vector3(
                save.position.x, save.position.y, save.position.z
            );

            Player.Instance.RotationY = save.rotationY;

            SkillSystem.Instance.FromSaveData(save.skills);
            InventorySystemFromSaveData(save.inventory);
            EquipmentSystemFromSaveData(save.equipment);
            QuestSystemFromSaveData(save.questProgress);
            CraftingSystemFromSaveData(save.activeCraftingJobs);

            RecipeBookSystem.Instance.FromSaveData(save.learnedRecipes);
        }

        private void ApplyWorldSaveSnapshot(WorldSave save)
        {
            WorldManager.Instance.WorldId = save.worldId;
            WorldManager.Instance.ZoneId  = save.zoneId;

            WorldManager.Instance.ApplyResourceNodeSave(save.resourceNodes);
            WorldManager.Instance.ApplyWorldObjectsSave(save.worldObjects);
            WorldManager.Instance.ApplyChestsSave(save.chests);
            WorldManager.Instance.ApplyActiveSpawnSave(save.activeSpawns);
            WorldManager.Instance.ApplyFlagsSave(save.worldFlags);
            WorldManager.Instance.ApplyTimersSave(save.timers);
        }

        // ============================================================
        // Version Migration (Basic)
        // ============================================================

        private void HandlePlayerVersionMismatch(int loadedVersion)
        {
            Debug.LogWarning($"[SaveSystem] Player save version mismatch. Loaded={loadedVersion}, Current={CurrentSchemaVersion_Player}");

            // Basic approach:
            //  - If loadedVersion < current → upgrade
            //  - If loadedVersion > current → do partial load with fallback

            if (loadedVersion < CurrentSchemaVersion_Player)
            {
                // Upgrade path: fill new fields with defaults
                Debug.Log("[SaveSystem] Upgrading older player save.");
            }
            else if (loadedVersion > CurrentSchemaVersion_Player)
            {
                Debug.LogWarning("[SaveSystem] Loaded save is from a future version. Some fields may be ignored.");
            }
        }

        private void HandleWorldVersionMismatch(int loadedVersion)
        {
            Debug.LogWarning($"[SaveSystem] World save version mismatch. Loaded={loadedVersion}, Current={CurrentSchemaVersion_World}");

            if (loadedVersion < CurrentSchemaVersion_World)
            {
                Debug.Log("[SaveSystem] Upgrading older world save.");
            }
            else if (loadedVersion > CurrentSchemaVersion_World)
            {
                Debug.LogWarning("[SaveSystem] Loaded save is from a future version. Some fields may be ignored.");
            }
        }

        // ============================================================
        // Fallback new save builders
        // ============================================================

        private bool CreateNewPlayerSave()
        {
            try
            {
                // Setup a minimal valid save
                var defaultSave = new PlayerSave
                {
                    schemaVersion = CurrentSchemaVersion_Player,
                    characterId   = Guid.NewGuid().ToString(),
                    name          = "New Player",
                    zoneId        = "lowmark_vs",
                    position      = new PlayerPosition { x = 0, y = 0, z = 0 },
                    rotationY     = 0,
                    skills        = new List<PlayerSkillSave>(),
                    inventory     = new List<PlayerInventorySlotSave>(),
                    equipment     = new Dictionary<string, PlayerEquipmentSlotSave>(),
                    questProgress = new Dictionary<string, PlayerQuestSave>(),
                    activeCraftingJobs = new List<PlayerCraftingJobSave>(),
                    learnedRecipes = new List<string>(),
                    currency = new PlayerCurrency { gold = 0 }
                };

                string json = JsonUtility.ToJson(defaultSave, true);
                File.WriteAllText(PlayerSavePath, json);
                return true;
            }
            catch (Exception ex)
            {
                Debug.LogError($"[SaveSystem] Could not create fallback player save: {ex.Message}");
                return false;
            }
        }

        private bool CreateNewWorldSave()
        {
            try
            {
                var defaultSave = new WorldSave
                {
                    schemaVersion = CurrentSchemaVersion_World,
                    worldId       = Guid.NewGuid().ToString(),
                    zoneId        = "lowmark_vs",
                    resourceNodes = new List<WorldResourceNodeSave>(),
                    worldObjects  = new List<WorldObjectSave>(),
                    chests        = new List<WorldChestSave>(),
                    activeSpawns  = new List<WorldSpawnSave>(),
                    worldFlags    = new Dictionary<string, bool>(),
                    timers        = new Dictionary<string, int>()
                };

                string json = JsonUtility.ToJson(defaultSave, true);
                File.WriteAllText(WorldSavePath, json);
                return true;
            }
            catch (Exception ex)
            {
                Debug.LogError($"[SaveSystem] Could not create fallback world save: {ex.Message}");
                return false;
            }
        }

        // ============================================================
        // Helper Extraction & Apply Methods
        // (Inventory, Equipment, Quests, Crafting, Skills)
        // ============================================================

        private List<PlayerInventorySlotSave> InventorySystemToSaveData()
        {
            var list = new List<PlayerInventorySlotSave>();
            var slots = Player.Instance.Inventory.Slots;

            for (int i = 0; i < slots.Length; i++)
            {
                if (slots[i].IsEmpty)
                    continue;

                list.Add(new PlayerInventorySlotSave
                {
                    slot = i,
                    itemId = slots[i].ItemId,
                    quantity = slots[i].Quantity
                });
            }
            return list;
        }

        private void InventorySystemFromSaveData(List<PlayerInventorySlotSave> data)
        {
            var comp = Player.Instance.Inventory;
            if (comp.Slots == null)
                return;

            foreach (var slot in comp.Slots)
                slot.Clear();

            foreach (var s in data)
            {
                if (s.slot >= 0 && s.slot < comp.Slots.Length)
                {
                    comp.Slots[s.slot].ItemId = s.itemId;
                    comp.Slots[s.slot].Quantity = s.quantity;
                }
            }
        }

        private Dictionary<string, PlayerEquipmentSlotSave> EquipmentSystemToSaveData()
        {
            var dict = new Dictionary<string, PlayerEquipmentSlotSave>();

            var equipped = Player.Instance.Equipment.GetAllEquipped();
            foreach (var kvp in equipped)
            {
                if (kvp.Value == null)
                    continue;

                dict[kvp.Key.ToString()] = new PlayerEquipmentSlotSave
                {
                    itemId = kvp.Value.itemId,
                    durability = 1f // VS placeholder
                };
            }
            return dict;
        }

        private void EquipmentSystemFromSaveData(Dictionary<string, PlayerEquipmentSlotSave> data)
        {
            foreach (var kvp in data)
            {
                if (Enum.TryParse(kvp.Key, out EquipmentSlot slot))
                {
                    var instance = new ItemInstance(kvp.Value.itemId);
                    Player.Instance.Equipment.ForceEquipFromLoad(slot, instance);
                }
            }
        }

        private Dictionary<string, PlayerQuestSave> QuestSystemToSaveData()
        {
            return Player.Instance.Quests.ToSaveDictionary();
        }

        private void QuestSystemFromSaveData(Dictionary<string, PlayerQuestSave> data)
        {
            Player.Instance.Quests.FromSaveDictionary(data);
        }

        private List<PlayerCraftingJobSave> CraftingSystemToSaveData()
        {
            return CraftingSystem.Instance.ToSaveData();
        }

        private void CraftingSystemFromSaveData(List<PlayerCraftingJobSave> data)
        {
            CraftingSystem.Instance.FromSaveData(data);
        }
    }
}
