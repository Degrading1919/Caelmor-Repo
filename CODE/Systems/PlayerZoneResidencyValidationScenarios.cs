using System.Collections.Generic;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Players;
using Caelmor.Runtime.ZoneResidency;
using Caelmor.Systems;
using Caelmor.Validation;

namespace Caelmor.Validation.ZoneResidency
{
    /// <summary>
    /// Validation-only scenarios for Stage 23.3.B2 — Player Zone Residency Validation.
    /// Proves single-zone residency enforcement, deterministic rejection, and idempotent detachment.
    /// </summary>
    public static class PlayerZoneResidencyValidationScenarios
    {
        /// <summary>
        /// Returns scenarios in deterministic order.
        /// </summary>
        public static IReadOnlyList<IValidationScenario> GetScenarios()
        {
            return new IValidationScenario[]
            {
                new ValidationScenarioAdapter(new Scenario1_AttachmentsAreAcceptedOnce()),
                new ValidationScenarioAdapter(new Scenario2_AttachRejectedWhenAlreadyResident()),
                new ValidationScenarioAdapter(new Scenario3_DetachIsIdempotentAndSafe()),
                new ValidationScenarioAdapter(new Scenario4_NonResidentReporting()),
                new ValidationScenarioAdapter(new Scenario5_InvalidOperationsLeaveNoState()),
                new ValidationScenarioAdapter(new Scenario6_DetachWithMismatchedZoneIsRejected())
            };
        }

        private sealed class Scenario1_AttachmentsAreAcceptedOnce : IValidationScenario
        {
            public string Name => "Scenario 1 — Attachments Are Accepted Once";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateAuthoritative();
                var player = new PlayerHandle(1);
                var zone = new ZoneId(1001);

                var attach = rig.System.AttachPlayerToZone(player, zone);

                a.True(attach.Ok, "Attach must succeed under server authority when no residency exists.");
                a.Equal(zone, attach.ExistingZone.Value, "Success result must expose the attached zone.");

                a.True(rig.System.IsResident(player), "Player must be resident after attach.");
                a.True(rig.System.IsResident(player, zone), "Player must be resident in the attached zone.");
                a.True(rig.System.TryGetResidentZone(player, out var resolvedZone), "Resident zone must be queryable.");
                a.Equal(zone, resolvedZone, "Resolved zone must match attached zone.");
            }
        }

        private sealed class Scenario2_AttachRejectedWhenAlreadyResident : IValidationScenario
        {
            public string Name => "Scenario 2 — Attach Rejected When Already Resident";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateAuthoritative();
                var player = new PlayerHandle(2);
                var firstZone = new ZoneId(2001);
                var secondZone = new ZoneId(2002);

                var firstAttach = rig.System.AttachPlayerToZone(player, firstZone);
                a.True(firstAttach.Ok, "Precondition: first attach must succeed.");

                var secondAttach = rig.System.AttachPlayerToZone(player, secondZone);

                a.False(secondAttach.Ok, "Attach must be rejected when player is already resident.");
                a.Equal(AttachPlayerToZoneFailureReason.AlreadyResident, secondAttach.FailureReason, "Failure reason must state already resident.");
                a.Equal(firstZone, secondAttach.ExistingZone, "Existing zone must be reported deterministically.");

                a.True(rig.System.IsResident(player, firstZone), "Player must remain resident in the first zone.");
                a.False(rig.System.IsResident(player, secondZone), "Player must not be auto-moved to the requested zone.");
                a.True(rig.System.TryGetResidentZone(player, out var resolvedZone), "Existing residency must remain queryable.");
                a.Equal(firstZone, resolvedZone, "Resolved zone must remain unchanged after rejected attach.");
            }
        }

        private sealed class Scenario3_DetachIsIdempotentAndSafe : IValidationScenario
        {
            public string Name => "Scenario 3 — Detach Is Idempotent And Safe";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateAuthoritative();
                var player = new PlayerHandle(3);
                var zone = new ZoneId(3001);

                var attach = rig.System.AttachPlayerToZone(player, zone);
                a.True(attach.Ok, "Precondition: attach must succeed.");

                var detach = rig.System.DetachPlayerFromZone(player, zone);
                a.True(detach.Ok, "Detach must succeed for resident player.");
                a.Equal(zone, detach.PreviousZone, "Detach result must report previous zone.");

                a.False(rig.System.IsResident(player), "Player must no longer be resident after detach.");

                var secondDetach = rig.System.DetachPlayerFromZone(player, zone);
                a.False(secondDetach.Ok, "Repeated detach must be rejected deterministically.");
                a.Equal(DetachPlayerFromZoneFailureReason.NotResident, secondDetach.FailureReason, "Failure reason must indicate non-residency.");
                a.False(secondDetach.PreviousZone.HasValue, "No previous zone must be reported when not resident.");
            }
        }

        private sealed class Scenario4_NonResidentReporting : IValidationScenario
        {
            public string Name => "Scenario 4 — Non-Resident Reporting";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateAuthoritative();
                var player = new PlayerHandle(4);
                var zone = new ZoneId(4001);

                a.False(rig.System.IsResident(player), "Player with no attachments must not be resident.");
                a.False(rig.System.IsResident(player, zone), "Player with no attachments must not be resident in any zone.");
                a.False(rig.System.TryGetResidentZone(player, out _), "Resident zone query must fail for non-resident player.");
            }
        }

        private sealed class Scenario5_InvalidOperationsLeaveNoState : IValidationScenario
        {
            public string Name => "Scenario 5 — Invalid Operations Leave No State";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateAuthoritative();
                var player = new PlayerHandle(0); // invalid
                var zone = new ZoneId(0); // invalid

                var attach = rig.System.AttachPlayerToZone(player, zone);
                a.False(attach.Ok, "Attach with invalid identifiers must fail deterministically.");
                a.Equal(AttachPlayerToZoneFailureReason.InvalidPlayerHandle, attach.FailureReason, "Player handle validity must be enforced.");
                a.False(rig.System.IsResident(player), "Invalid attach must not create residency state.");

                var validPlayer = new PlayerHandle(5);
                var invalidZone = new ZoneId(-10);
                var attachInvalidZone = rig.System.AttachPlayerToZone(validPlayer, invalidZone);
                a.False(attachInvalidZone.Ok, "Attach with invalid zone must fail deterministically.");
                a.Equal(AttachPlayerToZoneFailureReason.InvalidZoneId, attachInvalidZone.FailureReason, "Zone validity must be enforced.");
                a.False(rig.System.IsResident(validPlayer), "Invalid zone attach must leave no partial state.");
            }
        }

        private sealed class Scenario6_DetachWithMismatchedZoneIsRejected : IValidationScenario
        {
            public string Name => "Scenario 6 — Detach With Mismatched Zone Is Rejected";

            public void Run(IAssert a)
            {
                var rig = Rig.CreateAuthoritative();
                var player = new PlayerHandle(6);
                var initialZone = new ZoneId(6001);
                var otherZone = new ZoneId(6002);

                var attach = rig.System.AttachPlayerToZone(player, initialZone);
                a.True(attach.Ok, "Precondition: attach must succeed.");

                var detachWrongZone = rig.System.DetachPlayerFromZone(player, otherZone);

                a.False(detachWrongZone.Ok, "Detach must be rejected when zone does not match residency.");
                a.Equal(DetachPlayerFromZoneFailureReason.ResidentInDifferentZone, detachWrongZone.FailureReason, "Failure reason must identify differing zone.");
                a.Equal(initialZone, detachWrongZone.PreviousZone, "Existing residency must be reported deterministically.");

                a.True(rig.System.IsResident(player, initialZone), "Player must remain resident in the original zone after failed detach.");
            }
        }

        private sealed class Rig
        {
            public PlayerZoneResidencySystem System { get; private set; }
            public FakeServerAuthority Authority { get; private set; }

            public static Rig CreateAuthoritative()
            {
                var rig = new Rig
                {
                    Authority = new FakeServerAuthority(isServerAuthoritative: true)
                };

                rig.System = new PlayerZoneResidencySystem(rig.Authority);
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
