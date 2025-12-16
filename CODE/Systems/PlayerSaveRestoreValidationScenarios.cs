using System;
using System.Collections.Generic;
using Caelmor.Runtime.Persistence;
using Caelmor.Systems;
using Caelmor.Validation;

namespace Caelmor.Validation.PersistenceRestore
{
    /// <summary>
    /// Validation-only scenarios for Stage 23.5.B2 — Save Restore Validation Scenarios.
    /// Proves restore sequencing gates lifecycle activation, residency, and simulation eligibility
    /// until completion; rejects mid-tick restore attempts; enforces idempotency; and blocks
    /// activation after deterministic failure.
    /// </summary>
    public static class PlayerSaveRestoreValidationScenarios
    {
        public static IReadOnlyList<IValidationScenario> GetScenarios()
        {
            return new IValidationScenario[]
            {
                new ValidationScenarioAdapter(new Scenario1_RestoreGatesActivationResidencyAndSimulation()),
                new ValidationScenarioAdapter(new Scenario2_RestoreRejectedMidTick()),
                new ValidationScenarioAdapter(new Scenario3_IdempotentRestoreRequests()),
                new ValidationScenarioAdapter(new Scenario4_FailedRestorePreventsActivation())
            };
        }

        private sealed class Scenario1_RestoreGatesActivationResidencyAndSimulation : IValidationScenario
        {
            public string Name => "Scenario 1 — Restore Gates Activation, Residency, And Simulation";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var saveId = rig.SaveId;

                a.False(rig.Lifecycle.TryActivate(saveId), "Lifecycle activation must be blocked until restore completes.");
                a.False(rig.Residency.TryAttach(saveId), "Zone residency must be blocked until restore completes.");
                a.False(rig.Simulation.TryEnable(saveId), "Simulation eligibility must be blocked until restore completes.");

                var request = rig.Restore.RequestRestore(saveId);
                a.True(request.Ok, "Restore must succeed under authority and open gate.");
                a.True(rig.Restore.IsRestoreCompleted(saveId), "Restore completion must be visible for gating checks.");

                a.True(rig.Lifecycle.TryActivate(saveId), "Lifecycle activation must succeed after restore completion.");
                a.True(rig.Residency.TryAttach(saveId), "Zone residency must succeed after restore completion.");
                a.True(rig.Simulation.TryEnable(saveId), "Simulation eligibility must succeed after restore completion.");
            }
        }

        private sealed class Scenario2_RestoreRejectedMidTick : IValidationScenario
        {
            public string Name => "Scenario 2 — Restore Rejected Mid-Tick";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                rig.Gate.Allow = false;

                var result = rig.Restore.RequestRestore(rig.SaveId);

                a.False(result.Ok, "Restore must be rejected when mutation gate is closed.");
                a.Equal(RestoreRequestFailureReason.MidTickRestoreForbidden, result.FailureReason, "Mid-tick guard must report forbidden restore.");
                a.False(rig.Restore.TryGetStatus(rig.SaveId, out _), "Failed mid-tick restore must leave no tracked state.");
                a.Equal(0, rig.Rehydration.Calls, "Persistence executor must not run when restore is rejected mid-tick.");

                rig.Gate.Allow = true;
                var second = rig.Restore.RequestRestore(rig.SaveId);

                a.True(second.Ok, "Restore must succeed once mutation gate is reopened.");
                a.Equal(1, rig.Rehydration.Calls, "Persistence executor must run exactly once after gate opens.");
                a.True(rig.Restore.IsRestoreCompleted(rig.SaveId), "Restore completion must be recorded after successful retry.");
            }
        }

        private sealed class Scenario3_IdempotentRestoreRequests : IValidationScenario
        {
            public string Name => "Scenario 3 — Idempotent Restore Requests";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var first = rig.Restore.RequestRestore(rig.SaveId);

                a.True(first.Ok, "First restore attempt must succeed under normal conditions.");
                a.Equal(1, rig.Rehydration.Calls, "Restore executor must be invoked exactly once on first request.");
                a.True(first.WasStateChanged, "First restore must perform state transition to completed.");

                var second = rig.Restore.RequestRestore(rig.SaveId);

                a.True(second.Ok, "Second restore attempt must be idempotent success.");
                a.False(second.WasStateChanged, "Idempotent restore must report no additional state change.");
                a.Equal(1, rig.Rehydration.Calls, "Idempotent restore must not re-run the executor.");
                a.True(rig.Restore.IsRestoreCompleted(rig.SaveId), "Restore must remain completed after idempotent call.");
            }
        }

        private sealed class Scenario4_FailedRestorePreventsActivation : IValidationScenario
        {
            public string Name => "Scenario 4 — Failed Restore Prevents Activation";

            public void Run(IAssert a)
            {
                var rig = Rig.Create(restoreSucceeds: false);

                var result = rig.Restore.RequestRestore(rig.SaveId);

                a.False(result.Ok, "Restore must fail deterministically when persistence executor fails.");
                a.Equal(RestoreRequestFailureReason.RestoreExecutionFailed, result.FailureReason, "Failure reason must surface restore failure.");
                a.Equal(RestoreStatus.Failed, result.Status, "Failed restore must be recorded deterministically.");
                a.False(rig.Restore.IsRestoreCompleted(rig.SaveId), "Failed restore must not mark completion.");
                a.False(rig.Lifecycle.TryActivate(rig.SaveId), "Lifecycle activation must remain blocked after failed restore.");
                a.False(rig.Residency.TryAttach(rig.SaveId), "Zone residency must remain blocked after failed restore.");
                a.False(rig.Simulation.TryEnable(rig.SaveId), "Simulation eligibility must remain blocked after failed restore.");

                var retry = rig.Restore.RequestRestore(rig.SaveId);

                a.False(retry.Ok, "Subsequent restores must not proceed after a recorded failure.");
                a.Equal(RestoreRequestFailureReason.PreviousRestoreFailed, retry.FailureReason, "Retry must report previous failure state deterministically.");
                a.Equal(1, rig.Rehydration.Calls, "Failed restore must not execute the executor more than once.");
            }
        }

        private sealed class Rig
        {
            public PlayerSaveRestoreSystem Restore { get; private set; } = null!;
            public FakeAuthority Authority { get; private set; } = null!;
            public FakeRestoreGate Gate { get; private set; } = null!;
            public FakeRehydration Rehydration { get; private set; } = null!;
            public LifecycleActivationGate Lifecycle { get; private set; } = null!;
            public ResidencyAttachmentGate Residency { get; private set; } = null!;
            public SimulationEligibilityGate Simulation { get; private set; } = null!;
            public SaveId SaveId { get; private set; }

            public static Rig Create(bool restoreSucceeds = true)
            {
                var authority = new FakeAuthority(true);
                var gate = new FakeRestoreGate { Allow = true };
                var rehydration = new FakeRehydration { ShouldSucceed = restoreSucceeds };
                var system = new PlayerSaveRestoreSystem(authority, gate, rehydration);
                var saveId = new SaveId(Guid.NewGuid());
                var restoreQuery = (IPersistenceRestoreQuery)system;

                return new Rig
                {
                    Authority = authority,
                    Gate = gate,
                    Rehydration = rehydration,
                    Restore = system,
                    SaveId = saveId,
                    Lifecycle = new LifecycleActivationGate(restoreQuery),
                    Residency = new ResidencyAttachmentGate(restoreQuery),
                    Simulation = new SimulationEligibilityGate(restoreQuery)
                };
            }
        }

        private sealed class FakeAuthority : IServerAuthority
        {
            public FakeAuthority(bool isServerAuthoritative)
            {
                IsServerAuthoritative = isServerAuthoritative;
            }

            public bool IsServerAuthoritative { get; }
        }

        private sealed class FakeRestoreGate : IRestoreMutationGate
        {
            public bool Allow { get; set; }

            public bool CanRestoreNow() => Allow;
        }

        private sealed class FakeRehydration : IPersistenceRehydration
        {
            public bool ShouldSucceed { get; set; } = true;
            public int Calls { get; private set; }
            public RestoreOperationFailureReason FailureReason { get; set; } = RestoreOperationFailureReason.PersistenceUnavailable;

            public RestoreOperationResult PerformRestore(SaveId saveId)
            {
                Calls++;

                if (!ShouldSucceed)
                    return RestoreOperationResult.Failed(FailureReason);

                return RestoreOperationResult.Success();
            }
        }

        private sealed class LifecycleActivationGate
        {
            private readonly IPersistenceRestoreQuery _restore;

            public LifecycleActivationGate(IPersistenceRestoreQuery restore)
            {
                _restore = restore;
            }

            public int Attempts { get; private set; }
            public bool Activated { get; private set; }

            public bool TryActivate(SaveId saveId)
            {
                Attempts++;

                if (!_restore.IsRestoreCompleted(saveId))
                    return false;

                Activated = true;
                return true;
            }
        }

        private sealed class ResidencyAttachmentGate
        {
            private readonly IPersistenceRestoreQuery _restore;

            public ResidencyAttachmentGate(IPersistenceRestoreQuery restore)
            {
                _restore = restore;
            }

            public int Attempts { get; private set; }
            public bool Attached { get; private set; }

            public bool TryAttach(SaveId saveId)
            {
                Attempts++;

                if (!_restore.IsRestoreCompleted(saveId))
                    return false;

                Attached = true;
                return true;
            }
        }

        private sealed class SimulationEligibilityGate
        {
            private readonly IPersistenceRestoreQuery _restore;

            public SimulationEligibilityGate(IPersistenceRestoreQuery restore)
            {
                _restore = restore;
            }

            public int Attempts { get; private set; }
            public bool Enabled { get; private set; }

            public bool TryEnable(SaveId saveId)
            {
                Attempts++;

                if (!_restore.IsRestoreCompleted(saveId))
                    return false;

                Enabled = true;
                return true;
            }
        }
    }
}
