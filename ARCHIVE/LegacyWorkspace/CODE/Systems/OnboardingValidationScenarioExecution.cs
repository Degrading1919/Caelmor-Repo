using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Caelmor.Runtime.Onboarding;

namespace Caelmor.Validation.Onboarding
{
    /// <summary>
    /// Validation-only scenarios for proving onboarding correctness, determinism, and atomic rollback.
    /// Exercises: OnboardingSystem, OnboardingHandoffService, tick eligibility gating.
    /// </summary>
    public static class OnboardingValidationScenarios
    {
        /// <summary>
        /// Returns the validation scenarios in deterministic order.
        /// </summary>
        public static IReadOnlyList<IValidationScenario> GetScenarios()
        {
            return new IValidationScenario[]
            {
                new Scenario1_SuccessfulOnboarding(),
                new Scenario2_IdentityBindingFailure(),
                new Scenario3_ZoneAttachmentFailure(),
                new Scenario4_DuplicateInFlightOnboarding()
            };
        }

        private sealed class Scenario1_SuccessfulOnboarding : IValidationScenario
        {
            public string Name => "Scenario 1 — Successful Onboarding";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();

                // Preconditions: not authorized.
                a.False(rig.Handoff.IsClientAuthorized(rig.Session.Id), "Client must start unauthorized.");

                rig.Onboarding.HandleClientJoin(rig.Session);

                a.True(rig.Events.SuccessCount == 1, "Onboarding should report exactly one success.");
                a.True(rig.Events.FailureCount == 0, "Onboarding should report zero failures.");

                // Verify identity is server-generated (deterministic from session, not client-provided).
                a.True(rig.Identity.BindOrCreateCalls == 1, "Identity binding should be called exactly once.");
                a.True(rig.Identity.LastBoundPlayerId.HasValue, "PlayerId should be created server-side.");
                a.Equal(rig.Identity.ExpectedPlayerIdFromSession(rig.Session.Id), rig.Identity.LastBoundPlayerId.Value, "PlayerId must be server-generated/deterministic.");

                // Verify runtime player instance created.
                a.True(rig.Lifecycle.CreateCalls == 1, "Runtime player instance must be created exactly once.");
                a.True(rig.Lifecycle.LastCreatedPlayerHandle.HasValue, "Runtime player handle must exist.");

                // Verify attached to exactly one zone.
                a.True(rig.Zones.AttachCalls == 1, "Zone attachment should be attempted exactly once.");
                a.True(rig.Zones.AttachedZoneId.HasValue, "Player must be attached to a zone.");
                a.Equal(rig.World.DefaultZone, rig.Zones.AttachedZoneId.Value, "Player must attach to deterministic default zone.");
                a.True(rig.Zones.AttachedCountForPlayer(rig.Lifecycle.LastCreatedPlayerHandle.Value) == 1, "Player must be attached to exactly one zone.");

                // Verify tick eligibility gating occurred (only after successful attach).
                a.True(rig.Tick.SetCalls.Count == 1, "Tick eligibility should be set exactly once during successful onboarding.");
                a.True(rig.Tick.SetCalls[0].isEligible, "Tick eligibility should be granted on success.");
                a.True(rig.Tick.SetCalls[0].whenAfterZoneAttach, "Tick eligibility must be granted only after zone attachment.");

                // Verify client control authorization: not authorized until completion; then authorized.
                a.True(rig.ClientChannel.AuthorizeCalls == 1, "Client control authorization must be emitted exactly once.");
                a.True(rig.Handoff.IsClientAuthorized(rig.Session.Id), "Client must be authorized after successful onboarding.");
            }
        }

        private sealed class Scenario2_IdentityBindingFailure : IValidationScenario
        {
            public string Name => "Scenario 2 — Identity Binding Failure";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                rig.Identity.ForceBindFailure = true;

                rig.Onboarding.HandleClientJoin(rig.Session);

                a.True(rig.Events.SuccessCount == 0, "Onboarding should report zero successes.");
                a.True(rig.Events.FailureCount == 1, "Onboarding should report exactly one failure.");

                // No runtime instance, no zone, no tick eligibility, no client auth.
                a.True(rig.Lifecycle.CreateCalls == 0, "Runtime player instance must not be created on identity failure.");
                a.True(rig.Zones.AttachCalls == 0, "Zone attachment must not be attempted on identity failure.");
                a.True(rig.Tick.SetCalls.Count == 0, "Tick eligibility must not be modified on identity failure.");
                a.True(rig.ClientChannel.AuthorizeCalls == 0, "Client control must not be authorized on failure.");
                a.False(rig.Handoff.IsClientAuthorized(rig.Session.Id), "Client must remain unauthorized on failure.");

                // Atomic rollback: ensure no residual state.
                a.True(rig.Identity.UnbindCalls == 0, "Identity unbind should not be required when bind returns null (no bind occurred).");
                a.True(rig.Zones.AttachedZoneId.HasValue == false, "No zone residency must remain after failure.");
                a.True(rig.Lifecycle.DestroyCalls == 0, "No runtime destruction should occur if runtime was never created.");
            }
        }

        private sealed class Scenario3_ZoneAttachmentFailure : IValidationScenario
        {
            public string Name => "Scenario 3 — Zone Attachment Failure";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                rig.Zones.ForceAttachFailure = true;

                rig.Onboarding.HandleClientJoin(rig.Session);

                a.True(rig.Events.SuccessCount == 0, "Onboarding should report zero successes.");
                a.True(rig.Events.FailureCount == 1, "Onboarding should report exactly one failure.");

                // Bind happened, runtime created, then attach failed -> rollback must remove all.
                a.True(rig.Identity.BindOrCreateCalls == 1, "Identity bind should occur.");
                a.True(rig.Lifecycle.CreateCalls == 1, "Runtime player should be created prior to zone attach attempt.");
                a.True(rig.Zones.AttachCalls == 1, "Zone attachment should be attempted exactly once.");

                // No tick eligibility remains.
                a.True(rig.Tick.SetCalls.Count == 0, "Tick eligibility must not be granted if zone attach fails.");

                // Rollback must destroy runtime player and unbind identity.
                a.True(rig.Lifecycle.DestroyCalls == 1, "Runtime player must be destroyed on onboarding failure.");
                a.True(rig.Identity.UnbindCalls == 1, "Identity must be unbound on onboarding failure.");

                // No zone residency and no client auth.
                a.True(rig.Zones.AttachedZoneId.HasValue == false, "No zone residency must remain after attach failure.");
                a.True(rig.ClientChannel.AuthorizeCalls == 0, "Client control must not be authorized on failure.");
                a.False(rig.Handoff.IsClientAuthorized(rig.Session.Id), "Client must remain unauthorized on failure.");
            }
        }

        private sealed class Scenario4_DuplicateInFlightOnboarding : IValidationScenario
        {
            public string Name => "Scenario 4 — Duplicate / In-Flight Onboarding";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();

                // Run two concurrent onboarding attempts for the same session.
                var start = new ManualResetEventSlim(false);
                Exception ex1 = null, ex2 = null;

                var t1 = Task.Run(() =>
                {
                    try { start.Wait(); rig.Onboarding.HandleClientJoin(rig.Session); }
                    catch (Exception ex) { ex1 = ex; }
                });

                var t2 = Task.Run(() =>
                {
                    try { start.Wait(); rig.Onboarding.HandleClientJoin(rig.Session); }
                    catch (Exception ex) { ex2 = ex; }
                });

                start.Set();
                Task.WaitAll(t1, t2);

                a.True(ex1 == null && ex2 == null, "Validation should not throw exceptions.");

                // Deterministic: exactly one onboarding should succeed; the other rejected.
                a.True(rig.Events.SuccessCount == 1, "Exactly one onboarding attempt must succeed.");
                a.True(rig.Events.FailureCount == 1, "Exactly one onboarding attempt must fail due to duplicate/in-flight.");

                // No duplicate runtime state.
                a.True(rig.Lifecycle.CreateCalls == 1, "Runtime player should be created at most once.");
                a.True(rig.Zones.AttachCalls == 1, "Zone attachment should be performed at most once.");
                a.True(rig.Tick.SetCalls.Count == 1, "Tick eligibility should be granted at most once.");

                // Client control authorization emitted at most once.
                a.True(rig.ClientChannel.AuthorizeCalls == 1, "Client control authorization must be emitted at most once.");
                a.True(rig.Handoff.IsClientAuthorized(rig.Session.Id), "Client must be authorized after the single successful onboarding.");
            }
        }

        private sealed class Rig
        {
            public FakeServerSession Session { get; private set; }
            public FakeIdentitySystem Identity { get; private set; }
            public FakeLifecycleSystem Lifecycle { get; private set; }
            public FakeWorldManager World { get; private set; }
            public FakeZoneManager Zones { get; private set; }
            public FakeTickEligibilityRegistry Tick { get; private set; }
            public FakeClientControlChannel ClientChannel { get; private set; }
            public OnboardingHandoffService Handoff { get; private set; }
            public BridgeOnboardingEvents Events { get; private set; }
            public OnboardingSystem Onboarding { get; private set; }

            public static Rig Create()
            {
                var rig = new Rig();

                rig.Session = new FakeServerSession(new SessionId(Guid.Parse("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")));
                rig.Identity = new FakeIdentitySystem();
                rig.Lifecycle = new FakeLifecycleSystem();
                rig.World = new FakeWorldManager();
                rig.Zones = new FakeZoneManager();
                rig.Tick = new FakeTickEligibilityRegistry(rig.Zones);
                rig.ClientChannel = new FakeClientControlChannel();
                rig.Handoff = new OnboardingHandoffService(rig.ClientChannel);

                rig.Events = new BridgeOnboardingEvents(rig.Handoff);

                rig.Onboarding = new OnboardingSystem(
                    rig.Identity,
                    rig.Lifecycle,
                    rig.World,
                    rig.Zones,
                    rig.Tick,
                    rig.Events);

                return rig;
            }
        }

        private sealed class FakeServerSession : IServerSession
        {
            public FakeServerSession(SessionId id)
            {
                Id = id;
            }

            public SessionId Id { get; }
            public bool IsServerAuthoritative => true;
        }

        private sealed class FakeIdentitySystem : IPlayerIdentitySystem
        {
            public bool ForceBindFailure;
            public int BindOrCreateCalls;
            public int UnbindCalls;
            public PlayerId? LastBoundPlayerId;

            public PlayerId ExpectedPlayerIdFromSession(SessionId sessionId)
            {
                // Deterministic "server-generated" mapping for validation (not client-provided).
                // Uses a stable transform of the session Guid to produce a PlayerId Guid.
                var bytes = sessionId.Value.ToByteArray();
                bytes[0] ^= 0x5A;
                bytes[1] ^= 0xC3;
                bytes[2] ^= 0x11;
                bytes[3] ^= 0x9F;
                return new PlayerId(new Guid(bytes));
            }

            public PlayerId? BindOrCreateIdentity(IServerSession session)
            {
                BindOrCreateCalls++;

                if (ForceBindFailure)
                    return null;

                var pid = ExpectedPlayerIdFromSession(session.Id);
                LastBoundPlayerId = pid;
                return pid;
            }

            public void UnbindIdentity(IServerSession session)
            {
                UnbindCalls++;
                LastBoundPlayerId = null;
            }
        }

        private sealed class FakeLifecycleSystem : IPlayerLifecycleSystem
        {
            public int CreateCalls;
            public int DestroyCalls;
            public PlayerHandle? LastCreatedPlayerHandle;

            public PlayerHandle? CreateRuntimePlayer(PlayerId playerId)
            {
                CreateCalls++;

                // Deterministic handle from PlayerId for validation.
                var h = Math.Abs(playerId.Value.GetHashCode());
                if (h == 0) h = 1;

                var handle = new PlayerHandle(h);
                LastCreatedPlayerHandle = handle;
                return handle;
            }

            public void SetActive(PlayerHandle handle, bool isActive)
            {
                // No-op for validation. Onboarding tests do not rely on activation behavior here.
            }

            public void DestroyRuntimePlayer(PlayerHandle handle)
            {
                DestroyCalls++;
                if (LastCreatedPlayerHandle.HasValue && LastCreatedPlayerHandle.Value.Equals(handle))
                    LastCreatedPlayerHandle = null;
            }
        }

        private sealed class FakeWorldManager : IWorldManager
        {
            public readonly WorldId ActiveWorld = new WorldId(1);
            public readonly ZoneId DefaultZone = new ZoneId(100);

            public WorldId? GetActiveWorldId() => ActiveWorld;
            public ZoneId? GetDefaultInitialZone(WorldId worldId) => DefaultZone;
        }

        private sealed class FakeZoneManager : IZoneManager
        {
            public bool ForceAttachFailure;

            public int AttachCalls;
            public int DetachCalls;

            public ZoneId? AttachedZoneId;

            private readonly object _gate = new object();
            private readonly Dictionary<int, ZoneId> _playerToZone = new Dictionary<int, ZoneId>();

            public bool IsZoneKnown(ZoneId zoneId) => zoneId.Value > 0;
            public bool IsZoneAuthoritativeHere(ZoneId zoneId) => true;

            public bool AttachPlayerToZone(PlayerHandle player, ZoneId zoneId)
            {
                AttachCalls++;

                if (ForceAttachFailure)
                    return false;

                lock (_gate)
                {
                    _playerToZone[player.Value] = zoneId;
                    AttachedZoneId = zoneId;
                }

                return true;
            }

            public void DetachPlayerFromZone(PlayerHandle player, ZoneId zoneId)
            {
                DetachCalls++;

                lock (_gate)
                {
                    _playerToZone.Remove(player.Value);
                    if (AttachedZoneId.HasValue && AttachedZoneId.Value.Equals(zoneId))
                        AttachedZoneId = null;
                }
            }

            public bool IsPlayerAttached(PlayerHandle player)
            {
                lock (_gate)
                {
                    return _playerToZone.ContainsKey(player.Value);
                }
            }

            public int AttachedCountForPlayer(PlayerHandle player)
            {
                lock (_gate)
                {
                    return _playerToZone.ContainsKey(player.Value) ? 1 : 0;
                }
            }
        }

        private sealed class FakeTickEligibilityRegistry : ITickEligibilityRegistry
        {
            private readonly FakeZoneManager _zones;
            private readonly Dictionary<int, bool> _eligible = new Dictionary<int, bool>();
            public readonly List<(EntityHandle entity, bool isEligible, bool whenAfterZoneAttach)> SetCalls = new List<(EntityHandle, bool, bool)>();

            public FakeTickEligibilityRegistry(FakeZoneManager zones)
            {
                _zones = zones;
            }

            public bool TrySetTickEligible(EntityHandle entity, bool isEligible)
            {
                if (entity.Value <= 0) return false;

                var afterAttach = _zones.IsPlayerAttached(new PlayerHandle(entity.Value));
                SetCalls.Add((entity, isEligible, afterAttach));

                _eligible[entity.Value] = isEligible;
                return true;
            }
        }

        private sealed class FakeClientControlChannel : IClientControlChannel
        {
            public int AuthorizeCalls;

            public void AuthorizeClientControl(SessionId sessionId)
            {
                AuthorizeCalls++;
            }
        }

        private sealed class BridgeOnboardingEvents : IOnboardingEvents
        {
            private readonly IOnboardingHandoffService _handoff;

            public int SuccessCount;
            public int FailureCount;

            public BridgeOnboardingEvents(IOnboardingHandoffService handoff)
            {
                _handoff = handoff;
            }

            public void OnboardingCompleted(IServerSession session, PlayerId playerId, PlayerHandle playerHandle, ZoneId zoneId)
            {
                SuccessCount++;
                _handoff.NotifyOnboardingSuccess(session);
            }

            public void OnboardingFailed(IServerSession session, OnboardingFailureReason reason, string message)
            {
                FailureCount++;
                _handoff.NotifyOnboardingFailure(session);
            }
        }
    }

    /// <summary>
    /// Minimal validation scenario contract. Adapter-friendly for existing harnesses.
    /// </summary>
    public interface IValidationScenario
    {
        string Name { get; }
        void Run(IAssert assert);
    }

    /// <summary>
    /// Minimal assertion surface used by validation scenarios.
    /// Existing harnesses can adapt by providing an implementation.
    /// </summary>
    public interface IAssert
    {
        void True(bool condition, string message);
        void False(bool condition, string message);
        void Equal<T>(T expected, T actual, string message) where T : IEquatable<T>;
    }
}
