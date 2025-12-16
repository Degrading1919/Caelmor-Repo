# Caelmor — Phase 1.4 FULL Technical  
Foundation (Structured Edition)  
Prepared by: Game Director & Producer  
Includes fully structured outputs from:  
• Networking Architect  
• Engine-Agnostic Coding Assistant  
• Content Pipeline Assistant

---

# 1. Engine Selection — Unity Personal

Unity Personal is chosen as the foundation for Caelmor v1. It provides mature tooling,  
a huge medieval asset ecosystem, powerful 3D workflows, and stable long-term scaling toward  
MMO-like architectures. Costs remain zero until $200k annual revenue, making it ideal for a solo developer.

---

# 2. Module Architecture Overview

This chapter describes the complete high-level module architecture used in Caelmor. It defines ownership,  
responsibilities, and communication pathways between systems. The system is intentionally modular,  
data-driven, and aligned with scalable host-authoritative multiplayer.

---

## 2.1 Modules and Responsibilities

• GameManager — Bootstraps all systems and persists across scenes.  
• NetworkManager — Handles host/client roles, message flow, entity registration.  
• TickManager — 10 Hz authoritative simulation loop.  
• WorldManager — Zone loading/unloading, world spawning, static/active objects.  
• ZoneManager — Local zone instance manager.  
• EntitySystem — Base component for all living entities.  
• AIController — Simple tick-driven behavior.  
• PlayerController, InputController, CameraController — Local player systems.  
• CombatSystem — Attack timers, resolution, hit/miss, damage pipeline.  
• StatsSystem — HP, armor, regen (if used).  
• SkillSystem — XP, level-ups, effects.  
• InventorySystem — Slot-based inventory.  
• EquipmentSystem — Applies stat modifications.  
• CraftingSystem — Recipe resolution.  
• QuestSystem — Objective and progression tracking.  
• DialogueSystem — NPC text/dialogue handling.  
• SaveSystem — JSON-based persistence.  
• UIManager — HUD and menu orchestration.

---

## 2.2 Text-Based System Interaction Diagram

```
 GameManager
 ■
 ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
 ■        ■        ■
NetworkManager   WorldManager   UIManager
       ■              ■
   TickManager    ZoneManager
       ■              ■
      EntitySystem
       ■
   CombatSystem ■■■ StatsSystem ■■■ EquipmentSystem
                      ■
                 SkillSystem
```

---

# 3. Networking Architecture — Full Structured Edition

---

## 3.1 Tick Model (Full Detail)

Tick rate: **10 Hz (every 100 ms)**.  
The host executes all authoritative logic:

1. Gather inputs received since last tick.  
2. Apply validated movement for players.  
3. Move AI entities and perform decisions.  
4. Update attack timers and resolve hits/misses.  
5. Apply damage, deaths, and aggro.  
6. Award skill XP.  
7. Resolve crafting completions.  
8. Update world nodes/chests/bosses.  
9. Construct and send state snapshots.  

---

## 3.2 Host vs Client Responsibilities (Detailed Table)

### HOST (Authoritative):

• Movement validation + final position  
• Combat rules + RNG resolution  
• XP + level-ups  
• Inventory changes  
• Crafting resolution  
• AI behavior  
• World object state  
• Persistence (save/load)

### CLIENT:

• Sends input  
• Shows predicted movement  
• Animates attacks  
• Renders UI  
• Lerp-to-server movement correction  

---

## 3.3 Sync Categories (Complete)

Transforms: 10–20 Hz (unreliable)  
Combat state: On change (reliable)  
Inventory: On change (reliable)  
Skill XP: On XP gain (reliable)  
World objects: On change (reliable)

---

## 3.4 Error Correction (Full Strategy)

• Movement smoothing: interpolate toward host transforms.  
• Hard snap if difference exceeds threshold.  
• Combat is never predicted; only animations play locally.  
• Clients may send resync requests on impossible state.  

---

## 3.5 MMO Scaling Path (Structured)

The authoritative tick model lifts directly into:

• Dedicated server builds  
• Regional shards  
• Database-backed world states  

No structural rewrites required—only infrastructure upgrades.

---

# 4. Full Unity Folder Structure & Code Scaffolds

---

## 4.1 Folder Hierarchy (Complete)

/Assets/_Project  
 /Bootstrap  
 /Core  
 /Tick  
 /Networking  
 /World  
 /Player  
 /Combat  
 /Stats  
 /Inventory  
 /Quests  
 /Persistence  
 /UI  
 /Content  
 /Tools  

---

## 4.2 Scaffold Example — GameManager

```csharp
public class GameManager : MonoBehaviour {
    public static GameManager Instance { get; private set; }
    public NetworkManager Network { get; private set; }
    public TickManager Tick { get; private set; }
    public WorldManager World { get; private set; }
    public UIManager UI { get; private set; }
}
```

---

## 4.3 Scaffold Example — TickManager

```csharp
public class TickManager : MonoBehaviour {
    public const float TICK_INTERVAL = 0.1f;
    private float accumulator;
    public long TickIndex;
    public event Action<long> OnTick;
}
```

---

## 4.4 Scaffold Example — Networking Classes

```csharp
public class NetworkManager : MonoBehaviour {
    public bool IsHost;
    public void StartHost() {}
    public void StartClient(string address) {}
}
```

---

## 4.5 Scaffold Examples — Core Systems

```csharp
public class PlayerController : MonoBehaviour { }
public class CombatSystem : MonoBehaviour { }
public class StatsSystem : MonoBehaviour { }
public class InventorySystem : MonoBehaviour { }
```

---

# 5. Content Pipeline — Structured Full Integration

---

## 5.1 Schema Adjustments (All Applied Fields)

Items: stackable, maxStack  
Enemies: is_boss_family, is_unique  
Skills: max_level  
Zones: is_starting_zone  
Quests: repeatable, prerequisites  
NPCs: trainerSkillId  

---

## 5.2 ScriptableObject Storage Strategy

All immutable game content stored as ScriptableObjects:

• Items  
• Skills  
• Recipes  
• Families + Variants  
• Quests  
• Zones  
• NPCs  

Runtime state stored as JSON only.

---

## 5.3 Boot Pipeline (Formalized)

1. Load ScriptableObject Databases:  
 - ItemDatabase  
 - SkillDatabase  
 - RecipeDatabase  
 - EnemyDatabase  
 - ZoneDatabase  
 - QuestDatabase  

2. Load Save Files:  
 - PlayerSave.json  
 - WorldSave.json  

3. Resolve IDs:  
 Database.Get(itemId)  
 Database.Get(skillId)  
 Database.Get(zoneId)  

4. Begin Simulation Loop  

---

# 6. Persistence — Full Structured Version

---

## 6.1 Player Save Structure

```json
{
  "schemaVersion": 1,
  "characterId": "...",
  "name": "...",
  "zoneId": "lowmark_vale",
  "position": { "x":0,"y":0,"z":0 },
  "skills": [...],
  "inventory": [...],
  "equipment": {...},
  "knownRecipes": [...],
  "gold": 0
}
```

---

## 6.2 World Save Structure

```json
{
  "schemaVersion": 1,
  "worldId": "lowmark_vale",
  "resourceNodes": [...],
  "chests": [...],
  "questObjects": [...],
  "bossStates": [...],
  "worldFlags": {...}
}
```

---

## 6.3 Save Pipeline (Full)

Host saves:  
• On player disconnect  
• On shutdown  
• Every 5 minutes  
• On major world events  

Atomic save strategy prevents corruption.

---

# 7. Architectural Diagrams

---

## 7.1 Tick Flow Diagram

```
[Tick Start]
 ↓ Collect Inputs
 ↓ Movement Simulation
 ↓ AI Decisions
 ↓ Combat Timers
 ↓ Resolve Combat
 ↓ XP Awards
 ↓ World Updates
 ↓ Send State Snapshot
[Tick End]
```

---

## 7.2 Save/Load Flow

```
PlayerSave.json → SkillSystem ← SkillDatabase
               → InventorySystem ← ItemDatabase
               → QuestSystem ← QuestDatabase

WorldSave.json → WorldManager ← ZoneDatabase
```

---

# 8. Technical Risk & Mitigation (Structured Edition)

• Architectural Drift → Enforce folder hierarchy and modularity.  
• Tick Desync → Fixed 10 Hz + smoothing.  
• Save Corruption → Atomic writes + versioning.  
• Entity Overload → Distance-based culling.  
• Feature Creep → Strict v1 content boundaries.  

---

# END OF FULL STRUCTURED DOCUMENT
