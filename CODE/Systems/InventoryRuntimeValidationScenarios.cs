using System;
using System.Collections.Generic;
using Caelmor.Systems;

namespace Caelmor.Economy.Inventory
{
    /// <summary>
    /// Stage 26.B2 — Validation scenarios for inventory runtime invariants.
    /// </summary>
    public static class InventoryRuntimeValidationMatrix
    {
        public static IReadOnlyList<IValidationScenario> BuildAll()
        {
            return new IValidationScenario[]
            {
                new OwnershipInvariantScenario(),
                new AtomicMutationScenario(),
                new IdempotentInventoryCreationScenario(),
                new MidTickMutationRejectionScenario(),
                new DeterministicOrderingScenario(),
            };
        }
    }

    internal abstract class InventoryRuntimeScenarioBase : IValidationScenario
    {
        protected InventoryRuntimeSystem Runtime = default!;
        protected StubAuthority Authority = default!;

        public abstract string ScenarioId { get; }

        public virtual void Reset(IScenarioContext ctx)
        {
            Authority = new StubAuthority();
            Runtime = new InventoryRuntimeSystem(Authority);
        }

        public abstract ScenarioStepResult OnTick(IScenarioContext ctx, int tick);

        protected ScenarioStepResult Pass() => ScenarioStepResult.Passed();
        protected ScenarioStepResult Fail(string reason) => ScenarioStepResult.Failed(reason);
    }

    internal sealed class OwnershipInvariantScenario : InventoryRuntimeScenarioBase
    {
        public override string ScenarioId => "26.B2.1_OwnershipEnforced";

        public override ScenarioStepResult OnTick(IScenarioContext ctx, int tick)
        {
            Runtime.EnsureInventory(1, out _, out _);
            Runtime.EnsureInventory(2, out _, out _);

            if (!Runtime.TryCreateItem(1, "item.sword", out var itemId, out var createFail))
                return Fail(createFail ?? "create_failed");

            if (Runtime.TryTransferItem(itemId, 2, 1, out var transferFail))
                return Fail("ownership_not_enforced");

            if (transferFail != "ownership_mismatch")
                return Fail("unexpected_failure_reason");

            if (!Runtime.TryGetOwner(itemId, out var owner) || owner != 1)
                return Fail("owner_changed_erroneously");

            var inv1 = Runtime.GetInventorySnapshot(1);
            var inv2 = Runtime.GetInventorySnapshot(2);
            if (inv1.Count != 1 || inv2.Count != 0)
                return Fail("inventory_contents_incorrect");

            return Pass();
        }
    }

    internal sealed class AtomicMutationScenario : InventoryRuntimeScenarioBase
    {
        public override string ScenarioId => "26.B2.2_AtomicMutations";

        public override ScenarioStepResult OnTick(IScenarioContext ctx, int tick)
        {
            Runtime.EnsureInventory(10, out _, out _);

            if (!Runtime.TryCreateItem(10, "item.branch", out var itemId, out var createFail))
                return Fail(createFail ?? "create_failed");

            if (Runtime.TryTransferItem(itemId, 10, 999, out var transferFail))
                return Fail("unexpected_transfer_success");

            if (transferFail != "destination_inventory_missing")
                return Fail("transfer_reason_incorrect");

            if (!Runtime.TryGetOwner(itemId, out var owner) || owner != 10)
                return Fail("owner_mutated_on_failure");

            var snapshot = Runtime.GetInventorySnapshot(10);
            if (snapshot.Count != 1 || snapshot[0].ItemId != itemId)
                return Fail("inventory_not_atomic");

            return Pass();
        }
    }

    internal sealed class IdempotentInventoryCreationScenario : InventoryRuntimeScenarioBase
    {
        public override string ScenarioId => "26.B2.3_IdempotentOperations";

        public override ScenarioStepResult OnTick(IScenarioContext ctx, int tick)
        {
            if (!Runtime.EnsureInventory(42, out var createdFirst, out var firstFail))
                return Fail(firstFail ?? "ensure_failed_first");

            if (!createdFirst)
                return Fail("first_creation_not_reported");

            if (!Runtime.EnsureInventory(42, out var createdSecond, out var secondFail))
                return Fail(secondFail ?? "ensure_failed_second");

            if (createdSecond)
                return Fail("idempotent_creation_not_respected");

            return Pass();
        }
    }

    internal sealed class MidTickMutationRejectionScenario : InventoryRuntimeScenarioBase
    {
        public override string ScenarioId => "26.B2.4_NoMidTickMutation";

        public override ScenarioStepResult OnTick(IScenarioContext ctx, int tick)
        {
            Runtime.EnsureInventory(7, out _, out _);

            Runtime.EnterSimulation();
            try
            {
                if (Runtime.TryCreateItem(7, "item.ore", out _, out var fail))
                    return Fail("mutation_allowed_mid_tick");

                if (fail != "mid_tick_mutation_blocked")
                    return Fail("incorrect_mid_tick_reason");
            }
            finally
            {
                Runtime.ExitSimulation();
            }

            if (!Runtime.TryCreateItem(7, "item.ore", out _, out var postFail))
                return Fail(postFail ?? "mutation_blocked_after_tick");

            return Pass();
        }
    }

    internal sealed class DeterministicOrderingScenario : InventoryRuntimeScenarioBase
    {
        public override string ScenarioId => "26.B2.5_DeterministicOrdering";

        public override ScenarioStepResult OnTick(IScenarioContext ctx, int tick)
        {
            Runtime.EnsureInventory(5, out _, out _);

            if (!Runtime.TryCreateItem(5, "item.delta", out var a, out var failA))
                return Fail(failA ?? "create_a_failed");
            if (!Runtime.TryCreateItem(5, "item.alpha", out var b, out var failB))
                return Fail(failB ?? "create_b_failed");
            if (!Runtime.TryCreateItem(5, "item.charlie", out var c, out var failC))
                return Fail(failC ?? "create_c_failed");

            var snapshot = Runtime.GetInventorySnapshot(5);
            if (snapshot.Count != 3)
                return Fail("snapshot_count_incorrect");

            if (snapshot[0].ItemId.Value != Math.Min(a.Value, Math.Min(b.Value, c.Value)))
                return Fail("ordering_not_deterministic");

            var snapshot2 = Runtime.GetInventorySnapshot(5);
            for (int i = 0; i < snapshot.Count; i++)
            {
                if (snapshot[i].ItemId != snapshot2[i].ItemId)
                    return Fail("ordering_not_stable");
            }

            return Pass();
        }
    }

    internal sealed class StubAuthority : IServerAuthority
    {
        public bool IsServerAuthoritative => true;
    }
}
