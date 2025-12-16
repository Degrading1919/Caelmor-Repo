// ============================================================================
// Caelmor Vertical Slice Code Scaffolds v1.1
// Implements: MOVE_SPEED const, XP routing, HP sync, AI steering
// ============================================================================

namespace Caelmor.VS
{
    // ------------------------------------------------------------------------
    // 1. Shared Constants (Host + Client)
    // ------------------------------------------------------------------------
    public static class GameConstants
    {
        // 2.1 Movement Speed Unification
        public const float MOVE_SPEED      = 4.0f;  // m/s for players
        public const float MAX_LEASH_SPEED = 3.5f;  // m/s for AI return steering

        // HP sync cadence (2.3 HP Sync Strategy — periodic HP snapshot)
        public const float HP_SYNC_INTERVAL_SECONDS = 1.0f;
    }

    // ------------------------------------------------------------------------
    // 2. TickManager — add HP sync timer
    // ------------------------------------------------------------------------
    public class TickManager : MonoBehaviour
    {
        public const float TICK_INTERVAL_SECONDS = 0.1f;

        private float _accumulator;
        private long  _tickIndex;

        private float _timeSinceLastAutosave;
        private float _timeSinceLastHpSync;

        public WorldManager WorldManager { get; private set; }
        public CombatSystem CombatSystem { get; private set; }
        public StatsSystem  StatsSystem  { get; private set; }
        public SkillSystem  SkillSystem  { get; private set; }
        public CraftingSystem CraftingSystem { get; private set; }
        public SaveSystem   SaveSystem   { get; private set; }
        public NetworkManager NetworkManager { get; private set; }

        public bool IsRunning { get; private set; }

        public void StartAuthoritativeLoop()
        {
            IsRunning = true;
        }

        private void Update()
        {
            if (!IsRunning) return;

            float dt = Time.deltaTime;
            _accumulator               += dt;
            _timeSinceLastAutosave     += dt;
            _timeSinceLastHpSync       += dt;

            while (_accumulator >= TICK_INTERVAL_SECONDS)
            {
                _accumulator -= TICK_INTERVAL_SECONDS;
                RunTick();
            }

            // existing autosave logic (unchanged)
            if (_timeSinceLastAutosave >= 300f)
            {
                SaveSystem.SaveWorld();
                SaveSystem.SaveAllConnectedPlayers();
                _timeSinceLastAutosave = 0f;
            }

            // 2.3 HP Sync Strategy — periodic HP snapshot every 1s
            if (_timeSinceLastHpSync >= GameConstants.HP_SYNC_INTERVAL_SECONDS)
            {
                _timeSinceLastHpSync = 0f;
                var hpSnapshot = WorldManager.BuildHpSnapshot();
                NetworkManager.BroadcastHpSnapshot(hpSnapshot);
            }
        }

        private void RunTick()
        {
            _tickIndex++;

            // 1. Drain inputs
            var inputBatch = NetworkManager.DrainBufferedInputs();

            // 2. Movement
            WorldManager.ApplyPlayerMovementInputs(inputBatch.MovementCommands);

            // 3. AI tick
            WorldManager.UpdateAIControllers(_tickIndex, TICK_INTERVAL_SECONDS);

            // 4. Combat
            CombatSystem.ProcessAttackTimersAndIntents(_tickIndex, inputBatch.AttackCommands);

            // 5. Damage + XP happens inside CombatSystem

            // 6. World + crafting
            WorldManager.UpdateWorldState(_tickIndex);
            CraftingSystem.ProcessCraftingJobs(_tickIndex);

            // 7. Mark dirty
            SaveSystem.MarkDirtyFromWorld(WorldManager);
            SaveSystem.MarkDirtyFromPlayers(WorldManager.GetPlayerEntities());

            // 8. Transforms snapshot + other events (unchanged)
            var snapshot = WorldManager.BuildStateSnapshot();
            NetworkManager.BroadcastSnapshot(snapshot);
        }
    }

    // ------------------------------------------------------------------------
    // 3. WorldManager — movement & HP snapshot builder
    // ------------------------------------------------------------------------
    public class WorldManager
    {
        private readonly Dictionary<string, Entity> _entities =
            new Dictionary<string, Entity>();

        // Called from TickManager with authoritative movement commands
        public void ApplyPlayerMovementInputs(List<PlayerInput_Move> moves)
        {
            foreach (var m in moves)
            {
                if (!_entities.TryGetValue(m.PlayerId, out var entity)) continue;
                if (!entity.IsPlayer) continue;

                // Convert 2D input to 3D and use unified MOVE_SPEED
                Vector3 dir = new Vector3(m.Direction.x, 0f, m.Direction.y);
                if (dir.sqrMagnitude <= float.Epsilon) continue;

                dir.Normalize();
                float distance = GameConstants.MOVE_SPEED * TickManager.TICK_INTERVAL_SECONDS;
                entity.Position += dir * distance;

                entity.MarkPositionDirty();
            }
        }

        // AI update called each tick
        public void UpdateAIControllers(long tickIndex, float tickDeltaSeconds)
        {
            foreach (var entity in _entities.Values)
            {
                if (entity.AIController == null) continue;
                entity.AIController.UpdateAI(tickIndex, this, tickDeltaSeconds);
            }
        }

        // Build transforms + HP snapshot structures for networking
        public HpSnapshot BuildHpSnapshot()
        {
            var hpList = new List<HpSnapshot.Entry>();

            foreach (var entity in _entities.Values)
            {
                if (entity.Stats == null) continue;

                hpList.Add(new HpSnapshot.Entry
                {
                    EntityId   = entity.EntityId,
                    CurrentHp  = entity.Stats.CurrentHp,
                    MaxHp      = entity.Stats.MaxHp
                });
            }

            return new HpSnapshot
            {
                Entries    = hpList,
                ServerTime = Time.time
            };
        }

        public TransformSnapshot BuildStateSnapshot()
        {
            // existing transform snapshot building; omitted for brevity
            return new TransformSnapshot();
        }

        // Utility
        public Entity GetEntity(string id)
        {
            _entities.TryGetValue(id, out var e);
            return e;
        }

        public IEnumerable<Entity> GetPlayerEntities()
        {
            foreach (var e in _entities.Values)
                if (e.IsPlayer) yield return e;
        }
    }

    // ------------------------------------------------------------------------
    // 4. Entity / Components (simplified)
    // ------------------------------------------------------------------------
    public class Entity
    {
        public string EntityId;
        public bool   IsPlayer;
        public Vector3 Position;
        public float   RotationY;

        public StatsComponent     Stats;
        public CombatComponent    Combat;
        public InventoryComponent Inventory;
        public EquipmentComponent Equipment;
        public SkillComponent     Skills;
        public AIController       AIController;

        public bool PositionDirty;

        public void MarkPositionDirty() => PositionDirty = true;
    }

    public class StatsComponent
    {
        public int MaxHp;
        public int CurrentHp;
        public int ArmorRating;
    }

    public class CombatComponent
    {
        public bool   IsAutoAttacking;
        public string TargetId;
        public string WeaponItemId;

        public int  AttackSpeedTicks;
        public long NextAttackTick;

        public int  AttackDamage;
        public float AttackRange;
    }

    // ------------------------------------------------------------------------
    // 5. AIController — steering-based return to leashCenter
    // ------------------------------------------------------------------------
    public class AIController
    {
        public Entity Owner;
        public Vector3 LeashCenter;
        public float   LeashRadius;
        public float   DetectionRadius;

        private enum AIState { Idle, Patrol, Chase, Attack, Return }
        private AIState _state = AIState.Idle;

        public void UpdateAI(long tickIndex, WorldManager world, float tickDeltaSeconds)
        {
            var player = world.FindNearestPlayerInRadius(Owner.Position, DetectionRadius);

            if (player == null)
            {
                HandleNoTarget(tickDeltaSeconds);
                return;
            }

            float distToPlayer = Vector3.Distance(Owner.Position, player.Position);
            if (distToPlayer > DetectionRadius || distToPlayer > LeashRadius)
            {
                _state = AIState.Return;
                HandleReturnToLeash(tickDeltaSeconds);
                return;
            }

            if (distToPlayer > Owner.Combat.AttackRange)
            {
                _state = AIState.Chase;
                SteerTowards(player.Position, tickDeltaSeconds);
            }
            else
            {
                _state = AIState.Attack;
                Owner.Combat.IsAutoAttacking = true;
                Owner.Combat.TargetId        = player.EntityId;
            }
        }

        private void HandleNoTarget(float tickDeltaSeconds)
        {
            // If previously chasing/attacking, steer back to leash
            if (_state == AIState.Chase || _state == AIState.Attack)
                _state = AIState.Return;

            if (_state == AIState.Return)
            {
                HandleReturnToLeash(tickDeltaSeconds);
            }
            else if (_state == AIState.Idle)
            {
                // remain idle in place for now
            }
        }

        private void HandleReturnToLeash(float tickDeltaSeconds)
        {
            Vector3 toCenter = LeashCenter - Owner.Position;
            float distance   = toCenter.magnitude;

            if (distance < 0.05f)
            {
                Owner.Position   = LeashCenter;
                _state           = AIState.Idle;
                Owner.Combat.IsAutoAttacking = false;
                Owner.Combat.TargetId        = null;
                return;
            }

            // 2.4 AI Steering: directional steering back toward leash center
            Vector3 dir = toCenter / distance; // normalized
            float moveDistance = GameConstants.MAX_LEASH_SPEED * tickDeltaSeconds;
            if (moveDistance > distance) moveDistance = distance;

            Owner.Position += dir * moveDistance;
            Owner.MarkPositionDirty();
        }

        private void SteerTowards(Vector3 targetPos, float tickDeltaSeconds)
        {
            Vector3 toTarget = targetPos - Owner.Position;
            float  distance  = toTarget.magnitude;
            if (distance < 0.01f) return;

            Vector3 dir = toTarget / distance;
            float moveDistance = GameConstants.MOVE_SPEED * tickDeltaSeconds;
            Owner.Position += dir * moveDistance;
            Owner.MarkPositionDirty();
        }
    }

    // ------------------------------------------------------------------------
    // 6. CombatSystem — melee vs ranged XP routing
    // ------------------------------------------------------------------------
    public class CombatSystem
    {
        public WorldManager   WorldManager   { get; set; }
        public StatsSystem    StatsSystem    { get; set; }
        public SkillSystem    SkillSystem    { get; set; }
        public NetworkManager NetworkManager { get; set; }

        public void ProcessAttackTimersAndIntents(long tickIndex, List<PlayerInput_Attack> attackCommands)
        {
            // 1) Apply new intents
            foreach (var cmd in attackCommands)
            {
                var entity = WorldManager.GetEntity(cmd.PlayerId);
                if (entity == null) continue;

                if (cmd.IsStart)
                {
                    StartAutoAttackOrAbility(entity, cmd.TargetEntityId, cmd.AbilityId, tickIndex);
                }
                else
                {
                    StopAutoAttack(entity);
                }
            }

            // 2) Timer-based resolution for all entities
            foreach (var entity in WorldManager.GetAllEntities())
            {
                var combat = entity.Combat;
                if (combat == null || !combat.IsAutoAttacking) continue;
                if (tickIndex < combat.NextAttackTick) continue;

                TryResolveAttack(entity, tickIndex);
            }
        }

        private void StartAutoAttackOrAbility(Entity attacker, string targetId, string abilityId, long tickIndex)
        {
            var target = WorldManager.GetEntity(targetId);
            if (!ValidateTarget(attacker, target)) return;

            if (string.IsNullOrEmpty(abilityId))
            {
                // basic auto attack
                attacker.Combat.IsAutoAttacking = true;
                attacker.Combat.TargetId        = targetId;
                attacker.Combat.AttackSpeedTicks = GetWeaponAttackSpeedTicks(attacker);
                attacker.Combat.NextAttackTick   = tickIndex + attacker.Combat.AttackSpeedTicks;
            }
            else
            {
                ScheduleSpecialAttack(attacker, targetId, abilityId, tickIndex);
            }
        }

        private void StopAutoAttack(Entity attacker)
        {
            attacker.Combat.IsAutoAttacking = false;
            attacker.Combat.TargetId        = null;
        }

        private void TryResolveAttack(Entity attacker, long tickIndex)
        {
            var target = WorldManager.GetEntity(attacker.Combat.TargetId);
            if (!ValidateTarget(attacker, target))
            {
                attacker.Combat.IsAutoAttacking = false;
                return;
            }

            if (!InAttackRange(attacker, target)) return;

            // hit / miss
            if (!CheckHit(attacker, target))
            {
                BroadcastMiss(attacker, target, tickIndex);
                attacker.Combat.NextAttackTick += attacker.Combat.AttackSpeedTicks;
                return;
            }

            int damage = ComputeDamage(attacker, target);
            ApplyDamageAndXp(attacker, target, damage, tickIndex);

            attacker.Combat.NextAttackTick += attacker.Combat.AttackSpeedTicks;
        }

        // 2.2 XP Routing Logic — melee vs ranged
        private void ApplyDamageAndXp(Entity attacker, Entity target, int damage, long tickIndex)
        {
            int newHp = StatsSystem.ApplyDamage(target, damage);
            bool isKill = newHp <= 0;

            if (isKill)
            {
                HandleDeath(attacker, target);
            }

            // Determine which combat skill gets XP
            string skillId = IsRangedWeapon(attacker) ? "ranged" : "melee";
            int xpAmount   = GetXpValueForTarget(target);

            SkillSystem.AwardXp(attacker, skillId, xpAmount);

            // Emit combat event (still includes HP delta)
            var evt = new Event_CombatResult
            {
                TickIndex      = tickIndex,
                SourceEntityId = attacker.EntityId,
                TargetEntityId = target.EntityId,
                Damage         = damage,
                NewHp          = newHp,
                IsKill         = isKill,
                IsCrit         = false
            };
            NetworkManager.BroadcastEvent(evt);
        }

        private bool IsRangedWeapon(Entity attacker)
        {
            if (attacker.Equipment == null) return false;
            string weaponItemId = attacker.Combat.WeaponItemId;
            if (string.IsNullOrEmpty(weaponItemId)) return false;

            ItemDef def = ContentDatabase.Items[weaponItemId];
            return def.IsRanged; // uses existing item data field; no schema change
        }

        // Stub helpers
        private bool ValidateTarget(Entity attacker, Entity target) => target != null && target.Stats != null;
        private bool InAttackRange(Entity attacker, Entity target) => 
            Vector3.Distance(attacker.Position, target.Position) <= attacker.Combat.AttackRange;
        private bool CheckHit(Entity attacker, Entity target) => true;
        private int  ComputeDamage(Entity attacker, Entity target) => attacker.Combat.AttackDamage;
        private void BroadcastMiss(Entity attacker, Entity target, long tickIndex) { }
        private void HandleDeath(Entity attacker, Entity target) { }
        private int  GetXpValueForTarget(Entity target) => 10;
        private int  GetWeaponAttackSpeedTicks(Entity attacker) => 10;
        private void ScheduleSpecialAttack(Entity attacker, string targetId, string abilityId, long tickIndex) { }
    }

    // ------------------------------------------------------------------------
    // 7. StatsSystem — unchanged core logic
    // ------------------------------------------------------------------------
    public class StatsSystem
    {
        public int ApplyDamage(Entity target, int damage)
        {
            int mitigated = Mathf.Max(0, damage - target.Stats.ArmorRating);
            target.Stats.CurrentHp = Mathf.Max(0, target.Stats.CurrentHp - mitigated);
            return target.Stats.CurrentHp;
        }
    }

    // ------------------------------------------------------------------------
    // 8. SkillSystem — AwardXp entry for combat routing
    // ------------------------------------------------------------------------
    public class SkillSystem
    {
        public void AwardXp(Entity entity, string skillId, int amount)
        {
            if (entity.Skills == null) return;
            entity.Skills.AddXp(skillId, amount);
        }
    }

    // ------------------------------------------------------------------------
    // 9. Networking — HP snapshot message + broadcast
    // ------------------------------------------------------------------------
    public struct HpSnapshot
    {
        public struct Entry
        {
            public string EntityId;
            public int    CurrentHp;
            public int    MaxHp;
        }

        public List<Entry> Entries;
        public float       ServerTime;
    }

    public class NetworkManager
    {
        public bool IsHost { get; private set; }

        // existing snapshot/events API omitted

        public void BroadcastSnapshot(TransformSnapshot snapshot)
        {
            // Transforms + core events
        }

        public void BroadcastHpSnapshot(HpSnapshot snapshot)
        {
            // Reliable or semi-reliable channel; everyone gets HP data every 1s
            SendToAll(snapshot, reliable: true);
        }

        public void SendToAll(object message, bool reliable)
        {
            // transport implementation
        }

        public HpSnapshot DrainPendingHpSnapshots() => default;

        public InputBatch DrainBufferedInputs() => new InputBatch();
    }

    public class InputBatch
    {
        public List<PlayerInput_Move>   MovementCommands   = new List<PlayerInput_Move>();
        public List<PlayerInput_Attack> AttackCommands     = new List<PlayerInput_Attack>();
        // others omitted
    }

    // ------------------------------------------------------------------------
    // 10. ClientWorld — apply HP snapshots + movement smoothing
    // ------------------------------------------------------------------------
    public class ClientWorld : MonoBehaviour
    {
        private readonly Dictionary<string, ClientEntity> _entities =
            new Dictionary<string, ClientEntity>();

        public void ApplyTransformSnapshot(TransformSnapshot snapshot)
        {
            foreach (var t in snapshot.Transforms)
            {
                if (!_entities.TryGetValue(t.EntityId, out var ce)) continue;
                ce.TargetPosition = t.Position;
                ce.RotationY      = t.RotationY;
            }
        }

        // 2.3 HP Sync Strategy — apply periodic HP snapshot
        public void ApplyHpSnapshot(HpSnapshot snapshot)
        {
            foreach (var e in snapshot.Entries)
            {
                if (!_entities.TryGetValue(e.EntityId, out var ce)) continue;
                ce.CurrentHp = e.CurrentHp;
                ce.MaxHp     = e.MaxHp;
                ce.MarkHpDirty();
            }
        }

        private void Update()
        {
            float dt = Time.deltaTime;
            foreach (var ce in _entities.Values)
            {
                ce.Position = Vector3.Lerp(ce.Position, ce.TargetPosition, 10f * dt);
            }
        }
    }

    public class ClientEntity
    {
        public string EntityId;
        public Vector3 Position;
        public Vector3 TargetPosition;
        public float   RotationY;
        public int     CurrentHp;
        public int     MaxHp;

        public void MarkHpDirty()
        {
            // UI refresh hook
        }
    }

    // ------------------------------------------------------------------------
    // 11. ClientPlayerController — uses shared MOVE_SPEED for prediction
    // ------------------------------------------------------------------------
    public class ClientPlayerController : MonoBehaviour
    {
        public ClientEntity LocalEntity;
        public NetworkManager NetworkManager;

        private void Update()
        {
            Vector2 input = ReadMovementInput();
            float dt = Time.deltaTime;

            if (input.sqrMagnitude > float.Epsilon)
            {
                Vector3 dir = new Vector3(input.x, 0f, input.y).normalized;
                LocalEntity.Position += dir * GameConstants.MOVE_SPEED * dt;
            }

            var msg = new PlayerInput_Move
            {
                PlayerId   = LocalEntity.EntityId,
                Direction  = input,
                ClientTime = Time.time
            };

            NetworkManager.SendToHost(msg);
        }

        private Vector2 ReadMovementInput()
        {
            // WASD / stick / etc.
            return new Vector2(Input.GetAxisRaw("Horizontal"), Input.GetAxisRaw("Vertical"));
        }
    }

    // ------------------------------------------------------------------------
    // 12. Message DTOs (simplified)
    // ------------------------------------------------------------------------
    public struct PlayerInput_Move
    {
        public string PlayerId;
        public Vector2 Direction;
        public float   ClientTime;
    }

    public struct PlayerInput_Attack
    {
        public string PlayerId;
        public string TargetEntityId;
        public string AbilityId;   // null/empty for auto
        public bool   IsStart;
    }

    public struct TransformSnapshot
    {
        public struct Entry
        {
            public string EntityId;
            public Vector3 Position;
            public float   RotationY;
        }

        public List<Entry> Transforms;
    }

    public struct Event_CombatResult
    {
        public long   TickIndex;
        public string SourceEntityId;
        public string TargetEntityId;
        public int    Damage;
        public int    NewHp;
        public bool   IsKill;
        public bool   IsCrit;
    }

    // ------------------------------------------------------------------------
    // 13. ItemDef stub for IsRanged check
    // ------------------------------------------------------------------------
    public class ItemDef
    {
        public string ItemId;
        public bool   IsRanged;
        public int    ArmorBonus;
        public int    WeaponDamage;
    }

    public static class ContentDatabase
    {
        public static readonly Dictionary<string, ItemDef> Items =
            new Dictionary<string, ItemDef>();
    }
}
