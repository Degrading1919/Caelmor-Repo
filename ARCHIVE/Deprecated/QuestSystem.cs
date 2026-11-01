// QuestSystem.cs
using System;
using System.Collections.Generic;

namespace Caelmor.VS
{
    /// <summary>
    /// Server-authoritative Quest System for the Vertical Slice.
    /// Watches world events (location, kill, interact, craft, equip),
    /// updates objectives, saves quest progress, and produces chain-level
    /// completion events.
    ///
    /// Each entity has its own QuestSystem instance.
    /// </summary>
    public class QuestSystem
    {
        // --------------------------------------------------------------------
        // Internal Structures
        // --------------------------------------------------------------------

        [Serializable]
        public class QuestProgress
        {
            public string questId;
            public int currentObjectiveIndex = 0;
            public bool completed = false;
        }

        [Serializable]
        public class QuestSaveData
        {
            public string questId;
            public int objectiveIndex;
            public bool completed;
        }

        /// <summary>
        /// Represents a single objective’s progress state.
        /// </summary>
        private class ObjectiveState
        {
            public int currentCount = 0;
            public bool completed = false;
        }

        // --------------------------------------------------------------------
        // Internal State
        // --------------------------------------------------------------------

        private readonly Entity _entity;
        private readonly Dictionary<string, QuestDefinition> _quests; // Provided by content load
        private readonly Dictionary<string, QuestProgress> _active = new();
        private readonly Dictionary<string, ObjectiveState> _objectiveStates = new();

        // --------------------------------------------------------------------
        // External Systems References
        // --------------------------------------------------------------------

        public InventorySystem InventorySystem { get; set; }
        public EquipmentSystem EquipmentSystem { get; set; }

        /// <summary>
        /// For kill tracking, location volumes, craft completion, etc.
        /// The world code calls into these as events occur.
        /// </summary>
        public event Action<string> OnQuestCompleted;
        public event Action<string, int> OnObjectiveCompleted;
        public event Action<string, int> OnObjectiveAdvanced;

        // --------------------------------------------------------------------
        // Constructor
        // --------------------------------------------------------------------

        public QuestSystem(Entity entity, IEnumerable<QuestDefinition> questDefs)
        {
            _entity = entity;
            _quests = new Dictionary<string, QuestDefinition>();

            foreach (var q in questDefs)
                _quests[q.id] = q;
        }

        // --------------------------------------------------------------------
        // Public API: Start a quest
        // --------------------------------------------------------------------

        public bool StartQuest(string questId)
        {
            if (!_quests.TryGetValue(questId, out var def))
                return false;

            if (_active.ContainsKey(questId))
                return true; // already started

            var p = new QuestProgress
            {
                questId = questId,
                currentObjectiveIndex = 0,
                completed = false
            };

            _active[questId] = p;
            _objectiveStates[questId] = new ObjectiveState();

            return true;
        }

        // --------------------------------------------------------------------
        // Objective Checking Helpers
        // --------------------------------------------------------------------

        private bool IsActive(string questId, out QuestProgress prog)
        {
            if (_active.TryGetValue(questId, out prog) && !prog.completed)
                return true;

            prog = null;
            return false;
        }

        private void MarkObjectiveCompleted(string questId)
        {
            var prog = _active[questId];
            var def = _quests[questId];

            _objectiveStates[questId].completed = true;

            OnObjectiveCompleted?.Invoke(questId, prog.currentObjectiveIndex);

            // Advance to next objective
            prog.currentObjectiveIndex++;

            if (prog.currentObjectiveIndex >= def.objectives.Length)
            {
                // Completed quest
                prog.completed = true;
                OnQuestCompleted?.Invoke(questId);
            }
            else
            {
                // Reset state for next objective
                _objectiveStates[questId] = new ObjectiveState();
                OnObjectiveAdvanced?.Invoke(questId, prog.currentObjectiveIndex);
            }
        }

        private ObjectiveState GetState(string questId)
        {
            return _objectiveStates.TryGetValue(questId, out var state)
                ? state
                : null;
        }

        // --------------------------------------------------------------------
        // Event Interfaces (Called by World/Game Systems)
        // --------------------------------------------------------------------
        // These are called from:
        //  • Trigger volumes (location)
        //  • Enemy death handlers (kill)
        //  • Item pickup (collect)
        //  • CraftingStation (craft complete)
        //  • EquipmentSystem (equip)
        //  • Interactables (interact)

        public void NotifyLocationReached(string triggerId)
        {
            foreach (var (questId, prog) in _active)
            {
                if (prog.completed)
                    continue;

                var obj = GetCurrentObjective(questId);
                if (obj.type != "location") continue;

                if (obj.target == triggerId)
                    MarkObjectiveCompleted(questId);
            }
        }

        public void NotifyInteraction(string interactId)
        {
            foreach (var (questId, prog) in _active)
            {
                if (prog.completed)
                    continue;

                var obj = GetCurrentObjective(questId);
                if (obj.type != "interact") continue;

                if (obj.target == interactId)
                    MarkObjectiveCompleted(questId);
            }
        }

        public void NotifyKill(string enemyId)
        {
            foreach (var (questId, prog) in _active)
            {
                if (prog.completed)
                    continue;

                var obj = GetCurrentObjective(questId);
                if (obj.type != "kill") continue;

                if (obj.target != enemyId)
                    continue;

                var state = GetState(questId);
                state.currentCount++;

                if (state.currentCount >= obj.count)
                    MarkObjectiveCompleted(questId);
            }
        }

        public void NotifyItemCollected(string itemId, int quantity)
        {
            foreach (var (questId, prog) in _active)
            {
                if (prog.completed)
                    continue;

                var obj = GetCurrentObjective(questId);
                if (obj.type != "collect") continue;

                if (obj.target != itemId)
                    continue;

                var state = GetState(questId);
                state.currentCount += quantity;

                if (state.currentCount >= obj.count)
                    MarkObjectiveCompleted(questId);
            }
        }

        public void NotifyCrafted(string itemId, int quantity)
        {
            foreach (var (questId, prog) in _active)
            {
                if (prog.completed)
                    continue;

                var obj = GetCurrentObjective(questId);
                if (obj.type != "craft") continue;

                if (obj.target != itemId)
                    continue;

                var state = GetState(questId);
                state.currentCount += quantity;

                if (state.currentCount >= obj.count)
                    MarkObjectiveCompleted(questId);
            }
        }

        public void NotifyEquipped(string itemId)
        {
            foreach (var (questId, prog) in _active)
            {
                if (prog.completed)
                    continue;

                var obj = GetCurrentObjective(questId);
                if (obj.type != "equip") continue;

                if (obj.target == itemId)
                    MarkObjectiveCompleted(questId);
            }
        }

        // --------------------------------------------------------------------
        // Retrieve Current Objective Definition
        // --------------------------------------------------------------------

        private QuestObjective GetCurrentObjective(string questId)
        {
            var prog = _active[questId];
            return _quests[questId].objectives[prog.currentObjectiveIndex];
        }

        // --------------------------------------------------------------------
        // TickManager Integration
        // The VS quest chain does not have timed objectives,
        // but this hook allows future expansion.
        // --------------------------------------------------------------------

        public void Tick(float deltaTime)
        {
            // Reserved for future use (time-based quests)
        }

        // --------------------------------------------------------------------
        // Save / Load
        // --------------------------------------------------------------------

        public List<QuestSaveData> ToSaveData()
        {
            var data = new List<QuestSaveData>();

            foreach (var (questId, prog) in _active)
            {
                data.Add(new QuestSaveData
                {
                    questId = questId,
                    completed = prog.completed,
                    objectiveIndex = prog.currentObjectiveIndex
                });
            }

            return data;
        }

        public void LoadFromSaveData(IEnumerable<QuestSaveData> saveData)
        {
            _active.Clear();
            _objectiveStates.Clear();

            foreach (var entry in saveData)
            {
                if (!_quests.ContainsKey(entry.questId))
                    continue;

                _active[entry.questId] = new QuestProgress
                {
                    questId = entry.questId,
                    completed = entry.completed,
                    currentObjectiveIndex = entry.objectiveIndex
                };

                _objectiveStates[entry.questId] = new ObjectiveState
                {
                    completed = entry.completed
                };
            }
        }
    }

    // ------------------------------------------------------------------------
    // Quest Definition Structures (Loaded from JSON or Markdown → JSON)
    // ------------------------------------------------------------------------

    [Serializable]
    public class QuestDefinition
    {
        public string id;
        public string title;
        public string description;
        public QuestObjective[] objectives;
    }

    [Serializable]
    public class QuestObjective
    {
        /// <summary>Types: location, interact, kill, collect, craft, equip</summary>
        public string type;
        public string target;
        public int count = 1;
        public bool optional = false;
    }
}
