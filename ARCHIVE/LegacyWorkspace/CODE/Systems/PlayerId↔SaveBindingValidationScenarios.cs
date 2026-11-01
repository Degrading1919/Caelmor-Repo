using System;
using System.Collections.Generic;
using Caelmor.Runtime.Persistence;

namespace Caelmor.Validation.Persistence
{
    /// <summary>
    /// Validation-only scenarios proving PlayerId ↔ SaveId binding correctness (Stage 23.1),
    /// including hard guardrails rejecting client-provided identifiers (Stage 23.1.B2).
    /// No runtime behavior is introduced here.
    /// </summary>
    public static class PlayerSaveBindingValidationScenarios
    {
        /// <summary>
        /// Returns scenarios in deterministic order.
        /// </summary>
        public static IReadOnlyList<IValidationScenario> GetScenarios()
        {
            return new IValidationScenario[]
            {
                new Scenario1_SuccessfulServerBinding(),
                new Scenario2_IdempotentRebind(),
                new Scenario3_ClientProvidedPlayerIdRejection(),
                new Scenario4_ClientProvidedSaveSelectionRejection()
            };
        }

        private sealed class Scenario1_SuccessfulServerBinding : IValidationScenario
        {
            public string Name => "Scenario 1 — Successful Server Binding";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateServerAuthoritative();

                // "Server generates PlayerId" is an upstream guarantee; here we validate that binding
                // accepts only valid server-side PlayerId and produces/returns a SaveId deterministically.
                var playerId = new PlayerId(Guid.Parse("11111111-1111-1111-1111-111111111111"));

                a.False(rig.Binding.HasBinding(playerId), "Precondition: no binding exists.");

                var r1 = rig.Binding.BindOrGetSaveForPlayer(playerId);
                a.True(r1.Ok, "Bind should succeed under server authority.");
                a.True(r1.SaveId.IsValid, "SaveId should be valid.");
                a.True(r1.WasCreated, "First bind should create the binding.");

                a.True(rig.Binding.HasBinding(playerId), "Binding should exist after successful bind.");

                a.True(rig.Binding.TryGetSaveForPlayer(playerId, out var queried), "Query by PlayerId should succeed.");
                a.Equal(r1.SaveId, queried, "Query must return the bound SaveId.");

                // Determinism: allocator is deterministic; binding must return allocator-chosen SaveId.
                a.Equal(rig.Allocator.ExpectedSaveIdFor(playerId), r1.SaveId, "Binding must use server allocator deterministically.");
            }
        }

        private sealed class Scenario2_IdempotentRebind : IValidationScenario
        {
            public string Name => "Scenario 2 — Idempotent Rebind";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateServerAuthoritative();

                var playerId = new PlayerId(Guid.Parse("22222222-2222-2222-2222-222222222222"));

                var r1 = rig.Binding.BindOrGetSaveForPlayer(playerId);
                a.True(r1.Ok, "First bind should succeed.");
                a.True(r1.WasCreated, "First bind should create binding.");

                var r2 = rig.Binding.BindOrGetSaveForPlayer(playerId);
                a.True(r2.Ok, "Second bind should succeed deterministically.");
                a.False(r2.WasCreated, "Second bind should not create a new binding.");
                a.Equal(r1.SaveId, r2.SaveId, "SaveId must remain unchanged across idempotent rebinding.");

                // No duplicate bindings: validate one-to-one invariant.
                a.True(rig.Binding.ValidateOneToOneBinding(out var error), $"One-to-one binding invariant must hold. Error: {error}");
            }
        }

        private sealed class Scenario3_ClientProvidedPlayerIdRejection : IValidationScenario
        {
            public string Name => "Scenario 3 — Client-Provided PlayerId Rejection";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateServerAuthoritative();

                // Client attempts to provide a PlayerId in a join request: must be rejected.
                var clientProvidedPlayerId = new PlayerId(Guid.Parse("33333333-3333-3333-3333-333333333333"));
                var request = new ClientJoinRequest(
                    clientProvidedPlayerId,
                    default,
                    default);

                var guard = ClientIdentifierRejectionGuards.RejectIfClientProvidedIdentifiersPresent(request);
                a.False(guard.Ok, "Guardrails must reject client-provided PlayerId.");
                a.Equal(GuardFailureReason.ClientProvidedPlayerId, guard.FailureReason, "Failure reason must indicate client-provided PlayerId.");

                // No binding created (server must not proceed).
                a.False(rig.Binding.HasBinding(clientProvidedPlayerId), "No binding must exist for rejected client-provided PlayerId.");

                // Prove no residual state exists.
                a.True(rig.Binding.ValidateOneToOneBinding(out var error), $"Binding maps must remain consistent. Error: {error}");
            }
        }

        private sealed class Scenario4_ClientProvidedSaveSelectionRejection : IValidationScenario
        {
            public string Name => "Scenario 4 — Client-Provided SaveId / Binding Token Rejection";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateServerAuthoritative();

                // Client attempts to select a save via SaveId or binding token: must be rejected.
                var playerId = new PlayerId(Guid.Parse("44444444-4444-4444-4444-444444444444"));

                var clientSaveId = new SaveId(Guid.Parse("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"));
                var clientToken = new BindingToken(Guid.Parse("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"));

                // SaveId selection rejection.
                var g1 = ClientIdentifierRejectionGuards.RejectIfClientProvidedSaveSelection(clientSaveId, default);
                a.False(g1.Ok, "Guardrails must reject client-provided SaveId.");
                a.Equal(GuardFailureReason.ClientProvidedSaveId, g1.FailureReason, "Failure reason must indicate client-provided SaveId.");
                a.False(rig.Binding.HasBinding(playerId), "No binding must be created after rejection.");

                // Binding token rejection.
                var g2 = ClientIdentifierRejectionGuards.RejectIfClientProvidedSaveSelection(default, clientToken);
                a.False(g2.Ok, "Guardrails must reject client-provided binding token.");
                a.Equal(GuardFailureReason.ClientProvidedBindingToken, g2.FailureReason, "Failure reason must indicate client-provided binding token.");
                a.False(rig.Binding.HasBinding(playerId), "No binding must be created after rejection.");

                // Prove no residual state exists.
                a.True(rig.Binding.ValidateOneToOneBinding(out var error), $"Binding maps must remain consistent. Error: {error}");
            }
        }

        private sealed class Rig
        {
            public FakeServerAuthority Authority { get; private set; }
            public FakeSaveIdAllocator Allocator { get; private set; }
            public PlayerSaveBindingSystem Binding { get; private set; }

            public static Rig CreateServerAuthoritative()
            {
                var rig = new Rig
                {
                    Authority = new FakeServerAuthority(isServerAuthoritative: true),
                    Allocator = new FakeSaveIdAllocator()
                };

                rig.Binding = new PlayerSaveBindingSystem(rig.Authority, rig.Allocator);
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

        private sealed class FakeSaveIdAllocator : ISaveIdAllocator
        {
            public SaveId AllocateForPlayer(PlayerId playerId)
            {
                return ExpectedSaveIdFor(playerId);
            }

            public SaveId ExpectedSaveIdFor(PlayerId playerId)
            {
                // Deterministic transform of PlayerId Guid into SaveId Guid (server-only).
                var bytes = playerId.Value.ToByteArray();
                bytes[0] ^= 0x2D;
                bytes[1] ^= 0x7A;
                bytes[2] ^= 0xC0;
                bytes[3] ^= 0x19;
                bytes[8] ^= 0x55;
                bytes[9] ^= 0xAA;
                return new SaveId(new Guid(bytes));
            }
        }
    }

    /// <summary>
    /// Minimal validation scenario contract (validation-only scaffolding).
    /// </summary>
    public interface IValidationScenario
    {
        string Name { get; }
        void Run(IAssert assert);
    }

    /// <summary>
    /// Minimal assertion surface used by these validation scenarios.
    /// A harness can supply an implementation matching its conventions.
    /// </summary>
    public interface IAssert
    {
        void True(bool condition, string message);
        void False(bool condition, string message);
        void Equal<T>(T expected, T actual, string message) where T : IEquatable<T>;
    }
}
