using System.Collections.Generic;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.PlayerLifecycle;
using Caelmor.Runtime.Players;
using Caelmor.Runtime.ZoneResidency;
using Caelmor.Systems;
using Caelmor.Validation;

namespace Caelmor.Validation.PlayerLifecycle
{
    /// <summary>
    /// Validation-only scenarios for Stage 23.4.B2 — Player Lifecycle Validation Scenarios.
    /// Proves lifecycle transition gating, residency ordering, simulation eligibility boundaries, and mid-tick mutation safety.
    /// </summary>
    public static class PlayerLifecycleValidationScenarios
    {
        public static IReadOnlyList<IValidationScenario> GetScenarios()
        {
            return new IValidationScenario[]
            {
                new ValidationScenarioAdapter(new Scenario1_ActivationRequiresResidency()),
                new ValidationScenarioAdapter(new Scenario2_SimulationEligibilityOnlyWhileActive()),
                new ValidationScenarioAdapter(new Scenario3_InvalidTransitionsFailDeterministically()),
                new ValidationScenarioAdapter(new Scenario4_IdempotentTransitionsHoldInvariants()),
                new ValidationScenarioAdapter(new Scenario5_MutationForbiddenMidTick()),
                new ValidationScenarioAdapter(new Scenario6_SimulationRevokedBeforeSuspendOrDeactivate())
            };
        }

        private sealed class Scenario1_ActivationRequiresResidency : IValidationScenario
        {
            public string Name => "Scenario 1 — Activation Requires Residency";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var player = new PlayerHandle(1);
                var sessionId = new SessionId(System.Guid.NewGuid());
                var playerId = new PlayerId(System.Guid.NewGuid());

                a.True(rig.System.Register(sessionId, playerId, player).Ok, "Registration must succeed under server authority.");

                var activation = rig.System.Activate(player);
                a.False(activation.Ok, "Activation must fail without zone residency.");
                a.Equal(PlayerLifecycleFailureReason.MissingZoneResidency, activation.FailureReason, "Failure must cite missing residency.");

                a.True(rig.System.TryGetState(player, out var state), "Lifecycle state must be queryable after failed activation.");
                a.Equal(PlayerLifecycleState.Inactive, state, "State must remain inactive after failed activation.");
                a.False(rig.System.IsSimulationEligible(player), "Simulation must not be eligible when activation is rejected.");

                rig.Residency.Attach(player, new ZoneId(100));
                var secondActivation = rig.System.Activate(player);
                a.True(secondActivation.Ok, "Activation must succeed once residency exists.");
                a.Equal(PlayerLifecycleState.Active, secondActivation.State, "State must become Active after successful activation.");
            }
        }

        private sealed class Scenario2_SimulationEligibilityOnlyWhileActive : IValidationScenario
        {
            public string Name => "Scenario 2 — Simulation Eligibility Only While Active";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var player = new PlayerHandle(2);
                rig.RegisterWithResidency(player);

                var activate = rig.System.Activate(player);
                a.True(activate.Ok, "Activation must succeed when residency is valid.");
                a.True(rig.System.IsSimulationEligible(player), "Simulation eligibility must be granted in Active state.");

                var suspend = rig.System.Suspend(player);
                a.True(suspend.Ok, "Suspension must succeed from Active state.");
                a.False(rig.System.IsSimulationEligible(player), "Simulation eligibility must be revoked on suspension.");

                var resume = rig.System.Activate(player);
                a.True(resume.Ok, "Resume to Active must succeed from Suspended state.");
                a.True(rig.System.IsSimulationEligible(player), "Simulation eligibility must be re-granted on resume.");

                var deactivate = rig.System.Deactivate(player, LifecycleTerminationReason.Explicit);
                a.True(deactivate.Ok, "Deactivation must succeed from Active state.");
                a.False(rig.System.IsSimulationEligible(player), "Simulation eligibility must be revoked before deactivation completes.");
            }
        }

        private sealed class Scenario3_InvalidTransitionsFailDeterministically : IValidationScenario
        {
            public string Name => "Scenario 3 — Invalid Transitions Fail Deterministically";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var player = new PlayerHandle(3);
                rig.RegisterWithResidency(player);

                var suspend = rig.System.Suspend(player);
                a.False(suspend.Ok, "Suspension must be rejected when player is inactive.");
                a.Equal(PlayerLifecycleFailureReason.InvalidTransition, suspend.FailureReason, "Failure reason must state invalid transition.");

                var deactivate = rig.System.Deactivate(player, LifecycleTerminationReason.Explicit);
                a.True(deactivate.Ok, "Deactivation from inactive state must be idempotent success.");

                rig.System.Activate(player);
                rig.Residency.Detach(player);

                var resume = rig.System.Activate(player);
                a.False(resume.Ok, "Activation attempt must fail once residency is removed while suspended/inactive.");
                a.Equal(PlayerLifecycleFailureReason.MissingZoneResidency, resume.FailureReason, "Missing residency must be reported deterministically.");
            }
        }

        private sealed class Scenario4_IdempotentTransitionsHoldInvariants : IValidationScenario
        {
            public string Name => "Scenario 4 — Idempotent Transitions Hold Invariants";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var player = new PlayerHandle(4);
                rig.RegisterWithResidency(player);

                a.True(rig.System.Activate(player).Ok, "Initial activation must succeed.");
                a.True(rig.System.Activate(player).Ok, "Repeated activation must be idempotent.");
                a.True(rig.System.IsSimulationEligible(player), "Simulation eligibility must remain granted while active.");

                a.True(rig.System.Suspend(player).Ok, "Suspension must succeed from Active.");
                a.True(rig.System.Suspend(player).Ok, "Repeated suspension must be idempotent and keep simulation disabled.");
                a.False(rig.System.IsSimulationEligible(player), "Simulation eligibility must stay revoked while suspended.");

                a.True(rig.System.Deactivate(player, LifecycleTerminationReason.Explicit).Ok, "Deactivation must succeed.");
                a.True(rig.System.Deactivate(player, LifecycleTerminationReason.Explicit).Ok, "Repeated deactivation must succeed deterministically.");
                a.False(rig.System.IsSimulationEligible(player), "Simulation eligibility must remain revoked after deactivation.");
            }
        }

        private sealed class Scenario5_MutationForbiddenMidTick : IValidationScenario
        {
            public string Name => "Scenario 5 — Mutation Forbidden Mid-Tick";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var player = new PlayerHandle(5);
                rig.RegisterWithResidency(player);

                rig.MutationGate.Allow = false;
                var activation = rig.System.Activate(player);
                a.False(activation.Ok, "Activation must be rejected when mutation gate is closed.");
                a.Equal(PlayerLifecycleFailureReason.MidTickMutationForbidden, activation.FailureReason, "Failure must cite mid-tick mutation guard.");

                rig.MutationGate.Allow = true;
                a.True(rig.System.Activate(player).Ok, "Activation must succeed once gate is reopened.");

                rig.MutationGate.Allow = false;
                var suspend = rig.System.Suspend(player);
                a.False(suspend.Ok, "Suspension must be rejected mid-tick.");
                a.Equal(PlayerLifecycleFailureReason.MidTickMutationForbidden, suspend.FailureReason, "Mid-tick guard must apply to suspension.");
                a.True(rig.System.IsSimulationEligible(player), "Simulation eligibility must remain unchanged after rejected mid-tick transition.");
            }
        }

        private sealed class Scenario6_SimulationRevokedBeforeSuspendOrDeactivate : IValidationScenario
        {
            public string Name => "Scenario 6 — Simulation Revoked Before Suspend Or Deactivate";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var player = new PlayerHandle(6);
                rig.RegisterWithResidency(player);
                rig.System.Activate(player);

                rig.Simulation.Log.Clear();
                var suspend = rig.System.Suspend(player);
                a.True(suspend.Ok, "Suspension must succeed from Active state.");
                a.SequenceEqual(new[] {"revoke"}, rig.Simulation.Log, "Simulation eligibility must be revoked before suspension completes.");

                rig.System.Activate(player);
                rig.Simulation.Log.Clear();
                var deactivate = rig.System.Deactivate(player, LifecycleTerminationReason.Disconnect);
                a.True(deactivate.Ok, "Deactivation must succeed from Active state.");
                a.SequenceEqual(new[] {"revoke"}, rig.Simulation.Log, "Simulation eligibility must be revoked before deactivation completes.");
            }
        }

        private sealed class Rig
        {
            public PlayerLifecycleSystem System { get; private set; }
            public FakeAuthority Authority { get; private set; }
            public FakeResidency Residency { get; private set; }
            public FakeSimulationEligibility Simulation { get; private set; }
            public FakeMutationGate MutationGate { get; private set; }
            public FakeLifecycleEvents Events { get; private set; }

            public static Rig Create()
            {
                var rig = new Rig
                {
                    Authority = new FakeAuthority(true),
                    Residency = new FakeResidency(),
                    Simulation = new FakeSimulationEligibility(),
                    MutationGate = new FakeMutationGate { Allow = true },
                    Events = new FakeLifecycleEvents()
                };

                rig.System = new PlayerLifecycleSystem(rig.Authority, rig.Residency, rig.Simulation, rig.MutationGate, rig.Events);
                return rig;
            }

            public void RegisterWithResidency(PlayerHandle player)
            {
                var sessionId = new SessionId(System.Guid.NewGuid());
                var playerId = new PlayerId(System.Guid.NewGuid());

                System.Register(sessionId, playerId, player);
                Residency.Attach(player, new ZoneId(99));
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

        private sealed class FakeResidency : IPlayerZoneResidencyQuery
        {
            private readonly Dictionary<PlayerHandle, ZoneId> _zoneByPlayer = new Dictionary<PlayerHandle, ZoneId>();

            public void Attach(PlayerHandle player, ZoneId zone) => _zoneByPlayer[player] = zone;

            public void Detach(PlayerHandle player) => _zoneByPlayer.Remove(player);

            public bool IsResident(PlayerHandle player) => _zoneByPlayer.ContainsKey(player);
        }

        private sealed class FakeSimulationEligibility : IPlayerSimulationEligibility
        {
            private readonly HashSet<PlayerHandle> _eligible = new HashSet<PlayerHandle>();
            public List<string> Log { get; } = new List<string>();

            public bool TrySetSimulationEligible(PlayerHandle player, bool isEligible)
            {
                if (!player.IsValid)
                    return false;

                if (isEligible)
                {
                    _eligible.Add(player);
                    Log.Add("grant");
                }
                else
                {
                    _eligible.Remove(player);
                    Log.Add("revoke");
                }

                return true;
            }

            public bool IsEligible(PlayerHandle player) => _eligible.Contains(player);
        }

        private sealed class FakeMutationGate : ILifecycleMutationGate
        {
            public bool Allow { get; set; }

            public bool CanMutateLifecycleNow() => Allow;
        }

        private sealed class FakeLifecycleEvents : IPlayerLifecycleEvents
        {
            public void OnPlayerActivated(SessionId sessionId, PlayerId playerId, PlayerHandle player)
            {
            }

            public void OnPlayerSuspended(SessionId sessionId, PlayerId playerId, PlayerHandle player)
            {
            }

            public void OnPlayerDeactivated(SessionId sessionId, PlayerId playerId, PlayerHandle player, LifecycleTerminationReason reason)
            {
            }
        }
    }
}
