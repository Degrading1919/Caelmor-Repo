using Caelmor.Economy.Crafting;
using Caelmor.Economy.Gathering;
using Caelmor.Economy.Inventory;
using Caelmor.Economy.ResourceNodes;
using Caelmor.Persistence;
using Caelmor.Systems;

// Test-only policy/content and storage adapters. All mutation, checkpoint, and
// hydration behavior runs through the existing production economy classes.
sealed class EconomyIntegrationFixture : IScenarioContext, ISaveCheckpointInvoker, IRestoreInvoker, IValidationLogger
{
    internal const int PlayerA = 1, PlayerB = 2, NodeId = 100, RespawnTicks = 4;
    internal const string Zone = "test_zone", World = "test_world", NodeType = "test_node";
    internal const string Resource = "test_resource", Output = "test_output", Skill = "test_gather";
    internal const string Recipe = "test_recipe", Station = "test_station";
    private readonly Queue<Action> _actions = new();
    private readonly FixtureClock _clock = new();
    private readonly FixtureStorage _storage = new();
    private readonly FixturePolicy _policy;
    private readonly ResourceNodePlacement[] _placements;
    private readonly SimplePlayerInventoryStore _inventory = new();
    private readonly ResourceNodeRuntimeSystem _nodes = new();
    private readonly SimpleInventoryPersistenceAdapter _inventoryAdapter;
    private readonly WorldNodePersistenceAdapter _nodeAdapter;
    private readonly SaveCheckpointCoordinator _coordinator;
    private readonly PersistenceRestoreOrchestrator _restore;
    private readonly GatheringResolutionSystem _gather;
    private readonly InventoryAndResourceGrantSystem _grant;
    private readonly CraftingExecutionSystem _craft;
    private bool _executingAction;
    private bool _completed;
    private int _passed;

    public EconomyIntegrationFixture()
    {
        _placements = new[] { new ResourceNodePlacement(NodeId, NodeType, default) };
        _inventory.MarkWritable(PlayerA);
        _inventory.MarkWritable(PlayerB);
        _nodes.InitializeForZone(Zone, _placements, null);
        _inventoryAdapter = new SimpleInventoryPersistenceAdapter(_inventory);
        _nodeAdapter = new WorldNodePersistenceAdapter(_nodes);
        _coordinator = new SaveCheckpointCoordinator(World, _storage, _storage, _inventoryAdapter, _nodeAdapter);
        _restore = new PersistenceRestoreOrchestrator(World, _storage, _storage, _inventoryAdapter, _nodeAdapter);
        _policy = new FixturePolicy(_nodes);
        _gather = new GatheringResolutionSystem(_policy, _policy);
        var mapping = new TableResourceGrantMapping(new Dictionary<(string, string), ResourceGrant[]>
        {
            [(NodeType, Skill)] = new[] { new ResourceGrant(Resource, 1) }
        });
        _grant = new InventoryAndResourceGrantSystem(_inventory, _policy, mapping, _policy, _nodes,
            new ResourceGrantPersistenceSink(_coordinator, _policy), _policy);
        _craft = new CraftingExecutionSystem(_inventory, _policy, _policy, _policy, _policy,
            new CraftingPersistenceSink(_coordinator, _policy), _policy);
        State = new AuthoritativeStateCapture(_inventory, _nodes);
        _coordinator.MarkPlayerDirty(PlayerA, "fixture_initial");
        _coordinator.MarkPlayerDirty(PlayerB, "fixture_initial");
        _coordinator.MarkWorldDirty("fixture_initial");
        _coordinator.RequestCheckpoint("fixture_initial");
        _coordinator.CommitCheckpointIfRequested();
    }

    public IAuthoritativeTickSource TickSource => _clock;
    public IAuthoritativeStateCapture State { get; }
    public ISaveCheckpointInvoker Save => this;
    public IRestoreInvoker Restore => this;
    public IValidationLogger Log => this;

    public ValidationScenarioDeps Dependencies => new(
        Gather, Craft, EmptyInventory, OneCraftInput, AvailableNode, DepletedNode,
        player => _inventoryAdapter.BuildPlayerSaveSnapshot(player),
        () => _nodeAdapter.BuildWorldSaveSnapshot(), PlayerA, PlayerB, NodeId, Recipe, Station);

    public void Execute(Caelmor.Systems.IValidationScenario scenario)
    {
        var harness = new ValidationHarness(this, new[] { scenario });
        harness.Start();
        for (var tick = 1; tick <= 100 && !_completed; tick++)
        {
            var before = _nodeAdapter.BuildWorldSaveSnapshot();
            _nodes.OnServerTick(tick);
            if (!before.NodeOverrides.SequenceEqual(_nodeAdapter.BuildWorldSaveSnapshot().NodeOverrides))
            {
                _coordinator.MarkWorldDirty("fixture_node_tick");
                _coordinator.RequestCheckpoint("fixture_node_tick");
            }
            _clock.Advance(tick);
            CommitCheckpointIfRequested();
        }
        Check(_completed && _passed == 1, "The real validation harness must complete and pass the injected scenario.");
    }

    public void EnqueueSerializedAction(string actionLabel, Action action) => _actions.Enqueue(action);
    private void DrainActions()
    {
        if (_executingAction) return;
        try
        {
            _executingAction = true;
            while (_actions.Count > 0) _actions.Dequeue()();
        }
        finally { _executingAction = false; }
    }
    public void RequestCheckpoint(string reasonCode) => _coordinator.RequestCheckpoint(reasonCode);
    public void CommitCheckpointIfRequested()
    {
        // An action is indivisible: a callback can request a checkpoint, but only
        // the surrounding serialized-action boundary may perform the commit.
        if (_executingAction) return;
        DrainActions();
        _coordinator.CommitCheckpointIfRequested();
    }
    public void CommitCheckpointNow() => CommitCheckpointIfRequested();
    public void RestorePlayerInventory(int playerId) => _restore.RestorePlayerInventory(playerId);
    public void RestoreWorldAndZone(string zoneId)
    {
        var saved = _restore.LoadWorldSaveForStartup();
        _nodes.OnZoneUnloading(Zone);
        _nodes.InitializeForZone(zoneId, _placements, _restore.BuildZoneNodeOverrides(saved));
    }
    public void Info(string message) { if (message == "VALIDATION: Harness complete.") _completed = true; }
    public void Fail(string scenarioId, string reason) => throw new InvalidOperationException($"{scenarioId}: {reason}");
    public void Pass(string scenarioId) => _passed++;

    private void EmptyInventory() => SetInventory(PlayerA, Array.Empty<PersistedInventoryEntry>());
    private void OneCraftInput() => SetInventory(PlayerA, new[] { new PersistedInventoryEntry(Resource, 1) });
    private void SetInventory(int player, IEnumerable<PersistedInventoryEntry> entries)
    {
        _inventoryAdapter.ApplyPlayerSaveSnapshot(new PersistedPlayerSave { PlayerId = player, Inventory = entries.ToList() });
        _coordinator.MarkPlayerDirty(player, "fixture_setup");
        _coordinator.RequestCheckpoint("fixture_setup");
    }
    private void AvailableNode()
    {
        _nodes.InitializeForZone(Zone, _placements, null);
        _coordinator.MarkWorldDirty("fixture_setup");
        _coordinator.RequestCheckpoint("fixture_setup");
    }
    private void DepletedNode()
    {
        AvailableNode();
        Check(_nodes.TryDepleteNode(NodeId, RespawnTicks), "Fixture setup must deplete the real resource node.");
    }
    private void Gather(int playerId, int nodeId)
    {
        var result = _gather.ResolveAttempt(playerId, nodeId, Skill, default);
        var grant = _grant.ProcessGatheringResult(playerId, result);
        if (grant.Status == GrantProcessStatus.Failed) throw new InvalidOperationException(grant.FailureReason);
    }
    private void Craft(int playerId, string recipe, string station) => _craft.ExecuteCraft(new CraftingRequest(playerId, recipe, station));

    public void VerifyMutationAndHydration()
    {
        EnqueueSerializedAction("contention", () => { Gather(PlayerA, NodeId); Gather(PlayerB, NodeId); });
        CommitCheckpointIfRequested();
        Check(_policy.GrantEvents == 1, "Only one contender may receive a grant.");
        Check(_storage.LoadPlayer(PlayerA).Inventory.Single().Count == 1, "Gather must persist one resource for the winning player.");
        Check(_storage.LoadPlayer(PlayerB).Inventory.Count == 0, "Rejected contender must remain empty.");
        Check(_storage.LoadWorld(World).NodeOverrides.Single().TicksRemaining == RespawnTicks, "Gather must persist depleted node and respawn duration in the same checkpoint cycle.");

        EnqueueSerializedAction("craft_burst", () => { Craft(PlayerA, Recipe, Station); Craft(PlayerA, Recipe, Station); });
        CommitCheckpointIfRequested();
        Check(_policy.CraftSuccessEvents == 1 && _policy.CraftFailureEvents == 1, "One input must permit one successful craft and one rejection.");
        var saved = _storage.LoadPlayer(PlayerA);
        Check(saved.Inventory.Single().ResourceItemKey == Output && saved.Inventory.Single().Count == 1, "Craft must consume the resource and persist exactly one output.");

        Check(_inventory.TryApplyDeltasAtomic(PlayerA, new[] { (Output, 7) }, out _), "Perturb live inventory before hydration.");
        for (int tick = 0; tick < RespawnTicks; tick++) _nodes.OnServerTick(tick);
        Check(State.CaptureNode(NodeId).Available, "Perturb live world by allowing the node to respawn.");
        var eventsBefore = _policy.GrantEvents + _policy.CraftSuccessEvents + _policy.CraftFailureEvents;
        RestorePlayerInventory(PlayerA);
        RestoreWorldAndZone(Zone);
        Check(_inventoryAdapter.BuildPlayerSaveSnapshot(PlayerA).Inventory.Single().Count == 1, "Hydration must replace perturbed inventory with its saved counts.");
        Check(!State.CaptureNode(NodeId).Available && _nodeAdapter.BuildWorldSaveSnapshot().NodeOverrides.Single().TicksRemaining == RespawnTicks, "Hydration must restore depleted node and saved remaining ticks.");
        Check(eventsBefore == _policy.GrantEvents + _policy.CraftSuccessEvents + _policy.CraftFailureEvents, "Hydration must not emit gameplay events.");

        var writesBefore = _storage.PlayerWrites + _storage.WorldWrites;
        EnqueueSerializedAction("checkpoint_during_action", () =>
        {
            AvailableNode();
            Gather(PlayerA, NodeId);
            RequestCheckpoint("fixture_mid_action");
            CommitCheckpointIfRequested();
            Check(writesBefore == _storage.PlayerWrites + _storage.WorldWrites, "Checkpoint requests must not flush partial serialized actions.");
        });
        CommitCheckpointIfRequested();
        Check(_storage.PlayerWrites + _storage.WorldWrites >= writesBefore + 2,
            "The completed action boundary must flush both dirty player and world snapshots.");
    }

    private static void Check(bool condition, string message) { if (!condition) throw new InvalidOperationException(message); }

    private sealed class FixtureClock : IAuthoritativeTickSource
    {
        public int CurrentTick { get; private set; }
        public event Action<int>? Tick;
        public void Advance(int tick) { CurrentTick = tick; Tick?.Invoke(tick); }
    }

    private sealed class FixtureStorage : IPlayerSaveStorage, IWorldSaveStorage
    {
        private readonly Dictionary<int, PersistedPlayerSave> _players = new();
        private readonly Dictionary<string, PersistedWorldSave> _worlds = new();
        public int PlayerWrites, WorldWrites;
        public PersistedPlayerSave LoadPlayer(int playerId) => Clone(_players[playerId]);
        public void SavePlayer(PersistedPlayerSave save) { _players[save.PlayerId] = Clone(save); PlayerWrites++; }
        public PersistedWorldSave LoadWorld(string worldId) => Clone(_worlds[worldId]);
        public void SaveWorld(string worldId, PersistedWorldSave save) { _worlds[worldId] = Clone(save); WorldWrites++; }
        private static PersistedPlayerSave Clone(PersistedPlayerSave source) => new() { PlayerId = source.PlayerId, Inventory = source.Inventory.ToList() };
        private static PersistedWorldSave Clone(PersistedWorldSave source) => new() { NodeOverrides = source.NodeOverrides.ToList() };
    }

    private sealed class FixturePolicy : IGatheringNodeQuery, IPlayerGatheringSkillProvider,
        INodeInstanceTypeResolver, INodeRespawnTicksProvider, IResourceGrantEventSink,
        Caelmor.Economy.Inventory.IServerDiagnosticsSink, IRecipeRepository, IRecipeDefinition,
        IPlayerRecipeKnowledge, IPlayerSkillFlags, ICraftingStationContext,
        ICraftingExecutionEventSink, Caelmor.Economy.Crafting.IServerDiagnosticsSink
    {
        private readonly ResourceNodeRuntimeSystem _nodes;
        public int GrantEvents, CraftSuccessEvents, CraftFailureEvents;
        public FixturePolicy(ResourceNodeRuntimeSystem nodes) => _nodes = nodes;
        public bool TryGetNodeContext(int id, out string nodeType, out NodeAvailability availability,
            out IReadOnlyList<string> skills, out IReadOnlyList<string> risks)
        {
            bool exists = _nodes.TryGetNodeAvailability(id, out var state);
            nodeType = NodeType;
            availability = state == ResourceNodeAvailability.Available ? NodeAvailability.Available : NodeAvailability.Depleted;
            skills = new[] { Skill };
            risks = Array.Empty<string>();
            return exists;
        }
        public bool PlayerHasGatheringSkill(int player, string skill) => (player == PlayerA || player == PlayerB) && skill == Skill;
        public bool TryGetNodeTypeKey(int id, out string nodeType) { nodeType = NodeType; return id == NodeId; }
        public int GetRespawnTicksRemaining(string nodeType) => RespawnTicks;
        public void Emit(ResourceGrantedEvent evt) => GrantEvents++;
        public void Emit(CraftingExecutionResult evt) { if (evt.Success) CraftSuccessEvents++; else CraftFailureEvents++; }
        public void Emit(string code, string message) { }
        public bool TryGetRecipe(string key, out IRecipeDefinition recipe) { recipe = this; return key == Recipe; }
        public bool PlayerKnowsRecipe(int player, string key) => key == Recipe;
        public bool PlayerHasSkillFlag(int player, string skill) => true;
        public bool IsStationUsable(int player, string station, out string? failureReason) { failureReason = null; return station == Station; }
        public string RecipeKey => Recipe;
        public string RequiredCraftingStationKey => Station;
        public string? RequiredSkillFlagKey => null;
        public IReadOnlyList<CraftItemDelta> Inputs { get; } = new[] { new CraftItemDelta(Resource, 1) };
        public IReadOnlyList<CraftItemDelta> Outputs { get; } = new[] { new CraftItemDelta(Output, 1) };
    }
}
