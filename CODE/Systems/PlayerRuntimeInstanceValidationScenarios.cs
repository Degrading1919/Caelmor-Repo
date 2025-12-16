using System;
using System.Collections.Generic;
using Caelmor.Runtime.Players;
using Caelmor.Systems;
using Caelmor.Validation;

namespace Caelmor.Validation.Players
{
    /// <summary>
    /// Validation-only scenarios for Player Runtime Instance Management (Stage 23.2.B).
    /// Proves server authority enforcement, idempotent creation, deterministic handle assignment,
    /// and safe destruction with no residual state.
    /// </summary>
    public static class PlayerRuntimeInstanceValidationScenarios
    {
        /// <summary>
        /// Returns scenarios in deterministic order.
        /// </summary>
        public static IReadOnlyList<Caelmor.Systems.IValidationScenario> GetScenarios()
        {
            return new Caelmor.Systems.IValidationScenario[]
            {
                new ValidationScenarioAdapter(new Scenario1_SuccessfulPlayerCreation()),
                new ValidationScenarioAdapter(new Scenario2_IdempotentCreation()),
                new ValidationScenarioAdapter(new Scenario3_InvalidPlayerIdRejection()),
                new ValidationScenarioAdapter(new Scenario4_DeterministicDestruction())
            };
        }

        private sealed class Scenario1_SuccessfulPlayerCreation : IValidationScenario
        {
            public string Name => "Scenario 1 — Successful Player Creation";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateServerAuthoritative();
                var playerId = new PlayerId(Guid.Parse("aaaaaaaa-1111-1111-1111-111111111111"));

                var r = rig.Manager.CreatePlayer(playerId);

                a.True(r.Ok, "Creation must succeed under server authority with valid PlayerId.");
                a.True(r.Handle.IsValid, "Handle must be valid and non-zero.");
                a.True(r.Instance.Handle.Equals(r.Handle), "Returned instance must match returned handle.");
                a.True(r.Instance.PlayerId.Equals(playerId), "Returned instance must match input PlayerId.");

                a.True(rig.Manager.Exists(playerId), "Instance must exist after creation.");

                a.True(rig.Manager.TryGetHandle(playerId, out var h), "Query by PlayerId must return a handle.");
                a.Equal(r.Handle, h, "Queried handle must match created handle.");

                a.True(rig.Manager.TryGetInstance(playerId, out var instById), "Query by PlayerId must return instance.");
                a.Equal(r.Instance, instById, "Instance queried by PlayerId must match created instance.");

                a.True(rig.Manager.TryGetInstance(r.Handle, out var instByHandle), "Query by Handle must return instance.");
                a.Equal(r.Instance, instByHandle, "Instance queried by Handle must match created instance.");
            }
        }

        private sealed class Scenario2_IdempotentCreation : IValidationScenario
        {
            public string Name => "Scenario 2 — Idempotent Creation";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateServerAuthoritative();
                var playerId = new PlayerId(Guid.Parse("bbbbbbbb-2222-2222-2222-222222222222"));

                var r1 = rig.Manager.CreatePlayer(playerId);
                a.True(r1.Ok, "First create must succeed.");

                var r2 = rig.Manager.CreatePlayer(playerId);
                a.True(r2.Ok, "Second create must succeed deterministically.");
                a.False(r2.WasCreated, "Second create must not create a new instance.");
                a.Equal(r1.Handle, r2.Handle, "Handle must remain unchanged across idempotent creation.");
                a.Equal(r1.Instance, r2.Instance, "Instance must remain unchanged across idempotent creation.");

                a.True(rig.Manager.TryGetInstance(playerId, out var inst), "Manager must still return the instance.");
                a.Equal(r1.Instance, inst, "Stored instance must match.");
            }
        }

        private sealed class Scenario3_InvalidPlayerIdRejection : IValidationScenario
        {
            public string Name => "Scenario 3 — Invalid PlayerId Rejection";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateServerAuthoritative();
                var invalid = new PlayerId(Guid.Empty);

                var r = rig.Manager.CreatePlayer(invalid);

                a.False(r.Ok, "Creation must fail for invalid PlayerId.");
                a.Equal(CreatePlayerFailureReason.InvalidPlayerId, r.FailureReason, "Failure reason must be InvalidPlayerId.");

                a.False(rig.Manager.Exists(invalid), "No instance must exist for invalid PlayerId.");
                a.False(rig.Manager.TryGetHandle(invalid, out _), "No handle must exist for invalid PlayerId.");
                a.False(rig.Manager.TryGetInstance(invalid, out _), "No instance must exist for invalid PlayerId.");
            }
        }

        private sealed class Scenario4_DeterministicDestruction : IValidationScenario
        {
            public string Name => "Scenario 4 — Deterministic Destruction";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateServerAuthoritative();
                var playerId = new PlayerId(Guid.Parse("cccccccc-3333-3333-3333-333333333333"));

                var created = rig.Manager.CreatePlayer(playerId);
                a.True(created.Ok, "Precondition: create must succeed.");

                var destroyed = rig.Manager.DestroyPlayer(playerId);
                a.True(destroyed, "Destroy by PlayerId must succeed for existing instance.");

                a.False(rig.Manager.Exists(playerId), "Instance must no longer exist after destroy.");
                a.False(rig.Manager.TryGetHandle(playerId, out _), "Handle mapping must be removed after destroy.");
                a.False(rig.Manager.TryGetInstance(playerId, out _), "Instance mapping must be removed after destroy.");
                a.False(rig.Manager.TryGetInstance(created.Handle, out _), "Handle lookup must fail after destroy.");

                var reDestroy = rig.Manager.DestroyPlayer(playerId);
                a.False(reDestroy, "Re-destroy by PlayerId must be safely rejected (idempotent false).");

                var reDestroyHandle = rig.Manager.DestroyPlayer(created.Handle);
                a.False(reDestroyHandle, "Re-destroy by Handle must be safely rejected (idempotent false).");
            }
        }

        private sealed class Rig
        {
            public FakeServerAuthority Authority { get; private set; }
            public PlayerRuntimeInstanceManager Manager { get; private set; }

            public static Rig CreateServerAuthoritative()
            {
                var rig = new Rig
                {
                    Authority = new FakeServerAuthority(isServerAuthoritative: true)
                };

                rig.Manager = new PlayerRuntimeInstanceManager(rig.Authority);
                return rig;
            }
        }

        private sealed class FakeServerAuthority : IServerAuthority
        {
            public FakeServerAuthority(bool isServerAuthoritative)
            {
                IsServerAuthoritative = isServerAuthoritative;
            }

            public bool IsServerAuthoritative { get; }
        }
    }
}
