using System.Reflection;
using Caelmor.Economy.Inventory;
using Caelmor.Persistence;
using Caelmor.Systems;

var failures = new List<string>();
var passed = 0;
var context = new ScenarioContext();
var suites = new HashSet<string>(StringComparer.Ordinal);
var originalScenarios = 0;
foreach (var suite in typeof(InventoryRuntimeSystem).Assembly.GetTypes().OrderBy(t => t.FullName, StringComparer.Ordinal))
{
    var factory = suite.GetMethod("GetScenarios", BindingFlags.Public | BindingFlags.Static, Type.EmptyTypes);
    if (suite == typeof(InventoryRuntimeValidationMatrix))
        factory = suite.GetMethod("BuildAll", Type.EmptyTypes);
    if (factory == null) continue;
    suites.Add(suite.Name);
    foreach (var entry in (System.Collections.IEnumerable)factory.Invoke(null, null)!)
    {
        originalScenarios++;
        var scenario = entry as Caelmor.Systems.IValidationScenario
            ?? new ValidationScenarioAdapter((Caelmor.Validation.IValidationScenario)entry);
        Run(scenario.ScenarioId, () =>
        {
            scenario.Reset(context);
            for (var tick = 1; tick <= 100; tick++)
            {
                var result = scenario.OnTick(context, tick);
                if (result.Status == ScenarioStepStatus.Failed) throw new Exception(result.FailureReason);
                if (result.Status == ScenarioStepStatus.Passed) return;
            }
            throw new Exception("Scenario exceeded 100 ticks.");
        });
    }
}

var injectedEconomyScenarios = 0;
for (var scenarioIndex = 0; scenarioIndex < 12; scenarioIndex++)
{
    var fixture = new EconomyIntegrationFixture();
    var matrix = ValidationScenario_Stage9Matrix.BuildAll(fixture.Dependencies);
    Require(matrix.Count == 12, "The injected Stage 9 matrix must contain all 12 scenarios.");
    var scenario = matrix[scenarioIndex];
    injectedEconomyScenarios++;
    Run(scenario.ScenarioId, () => fixture.Execute(scenario));
}
Run("economy_real_mutation_checkpoint_and_hydration", () => new EconomyIntegrationFixture().VerifyMutationAndHydration());

Run("validation_suite_coverage", () =>
{
    var required = new[] { "InventoryRuntimeValidationMatrix", "CombatRuntimeValidationScenarios", "NpcRuntimeValidationScenarios",
        "OnboardingValidationScenarios", "PlayerSaveBindingValidationScenarios", "PlayerSaveRestoreValidationScenarios",
        "PlayerLifecycleValidationScenarios", "PlayerRuntimeInstanceValidationScenarios", "PlayerZoneResidencyValidationScenarios",
        "QuestRuntimeValidationScenarios", "ClientReplicationSnapshotValidationScenarios", "InboundTransportValidationScenarios",
        "WorldSimulationCoreValidationScenarios" };
    foreach (var suite in required) Require(suites.Contains(suite), $"Required suite missing: {suite}.");
    Require(originalScenarios >= 71, $"Expected at least 71 registered scenarios, found {originalScenarios}.");
});

Run("headless_in_process_transport_proof", () =>
    Require(Caelmor.Runtime.Host.HeadlessServerEntryPoint.Main(new[] { "--transport-proof" }) == 0,
        "Threaded host must accept a session, ingest/freeze/consume a command, mutate authoritative state, and shut down."));

Run("inventory_repeated_keys_are_atomic", () =>
{
    var store = new SimplePlayerInventoryStore();
    store.MarkWritable(1);
    Require(store.TryApplyDeltasAtomic(1, new[] { ("ore", 5) }, out _), "Seed inventory.");
    Require(!store.TryApplyDeltasAtomic(1, new[] { ("ore", -4), ("ore", -4) }, out var reason), "Repeated removals must fail.");
    Require(reason == "insufficient_items", "Return insufficient_items.");
    Require(store.DebugEnumerate(1).Single().Value == 5, "Failure must preserve original inventory.");
    Require(store.TryApplyDeltasAtomic(1, new[] { ("ore", -4), ("ore", 2) }, out _), "Valid sequential totals must commit.");
    Require(store.DebugEnumerate(1).Single().Value == 3, "Repeated valid deltas must apply exactly once.");
    Require(!store.TryApplyDeltasAtomic(1, new[] { ("ore", int.MaxValue), ("other", 1) }, out reason), "Overflow must fail.");
    Require(reason == "count_overflow" && store.DebugEnumerate(1).Single().Value == 3, "Overflow preserves all state.");
});

Run("inventory_invalid_restore_preserves_state", () =>
{
    var store = new SimplePlayerInventoryStore();
    store.MarkWritable(1);
    store.TryApplyDeltasAtomic(1, new[] { ("ore", 5) }, out _);
    try
    {
        store.DebugSetExact(1, new List<PersistedInventoryEntry> { new PersistedInventoryEntry("wood", 2), new PersistedInventoryEntry("bad", -1) });
        throw new Exception("Corrupt restore must throw.");
    }
    catch (InvalidOperationException) { }
    Require(store.DebugEnumerate(1).Single().Key == "ore" && store.DebugEnumerate(1).Single().Value == 5, "Invalid snapshot must preserve original state.");
});

Console.WriteLine($"Validation: {passed} passed, {failures.Count} failed.");
Console.WriteLine($"Executed {originalScenarios} registered scenarios in {suites.Count} suites plus focused regressions and the threaded transport proof.");
Console.WriteLine($"Also executed all {injectedEconomyScenarios} injected Stage 9 economy/save/restore scenarios and a mutation/hydration regression using cloned in-memory storage; this does not prove durable disk saves.");
return failures.Count == 0 ? 0 : 1;

void Run(string name, Action action)
{
    try { action(); passed++; Console.WriteLine($"PASS {name}"); }
    catch (Exception ex) { failures.Add(name); Console.WriteLine($"FAIL {name}: {ex}"); }
}
static void Require(bool condition, string message) { if (!condition) throw new Exception(message); }

sealed class ScenarioContext : IScenarioContext, IValidationLogger
{
    public IAuthoritativeTickSource TickSource => throw new NotSupportedException();
    public IAuthoritativeStateCapture State => throw new NotSupportedException();
    public ISaveCheckpointInvoker Save => throw new NotSupportedException();
    public IRestoreInvoker Restore => throw new NotSupportedException();
    public IValidationLogger Log => this;
    public void EnqueueSerializedAction(string actionLabel, Action action) => action();
    public void Info(string message) { }
    public void Fail(string scenarioId, string reason) { }
    public void Pass(string scenarioId) { }
}
