using System;
using System.Collections.Generic;
using Caelmor.Runtime.Players;
using Caelmor.Runtime.Quests;
using Caelmor.Systems;
using Caelmor.Validation;

namespace Caelmor.Validation.Quests
{
    /// <summary>
    /// Validation-only scenarios for Stage 27.B2 — Quest Validation Scenarios.
    /// Proves deterministic progression, invalid transition rejection, mid-tick mutation safety,
    /// and lifecycle-based eligibility gating without mutating simulation state.
    /// </summary>
    public static class QuestRuntimeValidationScenarios
    {
        public static IReadOnlyList<IValidationScenario> GetScenarios()
        {
            return new IValidationScenario[]
            {
                new ValidationScenarioAdapter(new Scenario1_DeterministicProgression()),
                new ValidationScenarioAdapter(new Scenario2_InvalidTransitionsRejected()),
                new ValidationScenarioAdapter(new Scenario3_MidTickMutationBlocked()),
                new ValidationScenarioAdapter(new Scenario4_LifecycleEligibilityRequired())
            };
        }

        private sealed class Scenario1_DeterministicProgression : IValidationScenario
        {
            public string Name => "Scenario 1 — Deterministic Progression";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var questId = new QuestInstanceId(Guid.Parse("aaaaaaaa-1111-1111-1111-aaaaaaaaaaaa"));

                rig.Lifecycle.SetActive(rig.Player, true);

                var registration = rig.System.RegisterQuest(questId, rig.Player, "quest_def_alpha");
                a.True(registration.Ok, "Registration must succeed under server authority.");
                a.True(rig.System.ActivateQuest(questId).Ok, "Activation must succeed when lifecycle is active.");

                rig.Evaluator.EnqueueDecision(QuestProgressionDecision.Complete);
                var progress = rig.System.ProcessProgression(questId, Rig.EmptyEvents);
                a.True(progress.Ok, "Progression must succeed deterministically when evaluator signals completion.");
                a.Equal(QuestState.Completed, progress.State!.Value, "Quest must reach Completed state.");
                a.True(progress.WasStateChanged, "Progression must record state change when completing.");

                var second = rig.System.ProcessProgression(questId, Rig.EmptyEvents);
                a.False(second.Ok, "Additional progression attempts must be rejected once quest is terminal.");
                a.Equal(QuestProgressionFailureReason.InvalidState, second.FailureReason, "Failure reason must cite invalid state for terminal quest.");
                a.Equal(1, rig.Evaluator.Contexts.Count, "Evaluator must be invoked exactly once to prove determinism.");
            }
        }

        private sealed class Scenario2_InvalidTransitionsRejected : IValidationScenario
        {
            public string Name => "Scenario 2 — Invalid Transitions Rejected";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var questId = new QuestInstanceId(Guid.Parse("bbbbbbbb-2222-2222-2222-bbbbbbbbbbbb"));

                rig.Lifecycle.SetActive(rig.Player, true);
                rig.System.RegisterQuest(questId, rig.Player, "quest_def_beta");

                var prematureComplete = rig.System.CompleteQuest(questId);
                a.False(prematureComplete.Ok, "Completion must be rejected from inactive state.");
                a.Equal(QuestStateTransitionFailureReason.InvalidTransition, prematureComplete.FailureReason, "Failure must cite invalid transition.");

                var activation = rig.System.ActivateQuest(questId);
                a.True(activation.Ok, "Activation must succeed from inactive state.");
                a.True(activation.WasStateChanged, "Activation must change state from Inactive to Active.");

                var duplicateActivation = rig.System.ActivateQuest(questId);
                a.True(!duplicateActivation.WasStateChanged, "Duplicate activation must be idempotent with no state change.");
                a.True(duplicateActivation.Ok, "Duplicate activation must return success without mutation.");

                var complete = rig.System.CompleteQuest(questId);
                a.True(complete.Ok, "Completion must succeed from active state.");
                a.Equal(QuestState.Completed, complete.State!.Value, "Quest must become Completed after explicit completion.");

                var failAfterComplete = rig.System.FailQuest(questId);
                a.False(failAfterComplete.Ok, "Failure transition must be rejected from terminal state.");
                a.Equal(QuestStateTransitionFailureReason.InvalidTransition, failAfterComplete.FailureReason, "Invalid transition must be reported when attempting to fail a completed quest.");
            }
        }

        private sealed class Scenario3_MidTickMutationBlocked : IValidationScenario
        {
            public string Name => "Scenario 3 — Mid-Tick Mutation Blocked";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var questId = new QuestInstanceId(Guid.Parse("cccccccc-3333-3333-3333-cccccccccccc"));

                rig.Lifecycle.SetActive(rig.Player, true);
                rig.System.RegisterQuest(questId, rig.Player, "quest_def_gamma");

                rig.MutationGate.Allow = false;
                var activation = rig.System.ActivateQuest(questId);
                a.False(activation.Ok, "Activation must be rejected when mid-tick mutation guard is closed.");
                a.Equal(QuestStateTransitionFailureReason.MidTickMutationForbidden, activation.FailureReason, "Failure must cite mid-tick mutation guard.");

                rig.MutationGate.Allow = true;
                a.True(rig.System.ActivateQuest(questId).Ok, "Activation must succeed once mutation gate opens.");

                rig.MutationGate.Allow = false;
                var progression = rig.System.ProcessProgression(questId, Rig.EmptyEvents);
                a.False(progression.Ok, "Progression must be rejected mid-tick.");
                a.Equal(QuestProgressionFailureReason.MidTickMutationForbidden, progression.FailureReason, "Mid-tick guard must be enforced for progression.");
                a.Equal(0, rig.Evaluator.Contexts.Count, "Evaluator must not be invoked when mid-tick guard blocks progression.");
            }
        }

        private sealed class Scenario4_LifecycleEligibilityRequired : IValidationScenario
        {
            public string Name => "Scenario 4 — Lifecycle Eligibility Required";

            public void Run(IAssert a)
            {
                var rig = Rig.Create();
                var questId = new QuestInstanceId(Guid.Parse("dddddddd-4444-4444-4444-dddddddddddd"));

                rig.System.RegisterQuest(questId, rig.Player, "quest_def_delta");

                var activation = rig.System.ActivateQuest(questId);
                a.False(activation.Ok, "Activation must be rejected when lifecycle is not active.");
                a.Equal(QuestStateTransitionFailureReason.LifecycleNotEligible, activation.FailureReason, "Lifecycle gate must block activation for inactive players.");

                rig.Lifecycle.SetActive(rig.Player, true);
                a.True(rig.System.ActivateQuest(questId).Ok, "Activation must succeed once lifecycle is active.");

                rig.Lifecycle.SetActive(rig.Player, false);
                var progression = rig.System.ProcessProgression(questId, Rig.EmptyEvents);
                a.False(progression.Ok, "Progression must be rejected for non-active lifecycle state.");
                a.Equal(QuestProgressionFailureReason.LifecycleNotEligible, progression.FailureReason, "Lifecycle gate must block progression when player is not active.");
                a.Equal(0, rig.Evaluator.Contexts.Count, "Evaluator must not be invoked when lifecycle eligibility fails.");
            }
        }

        private sealed class Rig
        {
            public FakeAuthority Authority { get; private set; }
            public FakeLifecycle Lifecycle { get; private set; }
            public FakeMutationGate MutationGate { get; private set; }
            public FakeEvaluator Evaluator { get; private set; }
            public QuestRuntimeSystem System { get; private set; }
            public PlayerHandle Player { get; private set; }

            public static QuestProgressionEvents EmptyEvents { get; } = new QuestProgressionEvents(Array.Empty<WorldEvent>(), Array.Empty<CombatEvent>(), Array.Empty<InventoryEvent>());

            public static Rig Create()
            {
                var rig = new Rig
                {
                    Authority = new FakeAuthority(true),
                    Lifecycle = new FakeLifecycle(),
                    MutationGate = new FakeMutationGate(),
                    Evaluator = new FakeEvaluator(),
                    Player = new PlayerHandle(1)
                };

                rig.System = new QuestRuntimeSystem(rig.Authority, rig.MutationGate, rig.Lifecycle, rig.Evaluator);
                return rig;
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

        private sealed class FakeLifecycle : IPlayerLifecycleQuery
        {
            private readonly HashSet<PlayerHandle> _active = new HashSet<PlayerHandle>();

            public void SetActive(PlayerHandle player, bool active)
            {
                if (!player.IsValid) return;

                if (active)
                    _active.Add(player);
                else
                    _active.Remove(player);
            }

            public bool IsPlayerActive(PlayerHandle player)
            {
                return _active.Contains(player);
            }
        }

        private sealed class FakeMutationGate : IQuestMutationGate
        {
            public bool Allow { get; set; } = true;

            public bool CanMutateQuestsNow() => Allow;
        }

        private sealed class FakeEvaluator : IQuestProgressionEvaluator
        {
            private readonly Queue<QuestProgressionDecision> _decisions = new Queue<QuestProgressionDecision>();

            public List<QuestProgressionContext> Contexts { get; } = new List<QuestProgressionContext>();

            public void EnqueueDecision(QuestProgressionDecision decision)
            {
                _decisions.Enqueue(decision);
            }

            public QuestProgressionDecision Evaluate(QuestProgressionContext context)
            {
                Contexts.Add(context);
                if (_decisions.Count == 0)
                    return QuestProgressionDecision.NoChange;

                return _decisions.Dequeue();
            }
        }
    }
}
