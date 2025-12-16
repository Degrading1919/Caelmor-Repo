// CombatPresentationHookSystem.cs
// NOTE: Save location must follow existing project structure.
// Implements CombatPresentationHookSystem only.
// Client-side presentation hooks ONLY: animation/VFX/audio/UI callbacks.
// No gameplay state, no prediction, no networking, no persistence.

using System;
using System.Collections.Generic;

namespace Caelmor.Combat.Client
{
    /// <summary>
    /// CombatPresentationHookSystem
    ///
    /// Responsibilities:
    /// - Subscribe to replicated CombatEvents (delivered client-side)
    /// - Consume events immediately in the exact order received
    /// - Dispatch presentation hooks (animation/VFX/audio/UI) by event type
    /// - Never block event consumption (fail-silent per hook)
    /// - Maintain no authoritative state
    /// - Expose a presentation log for validation (event_id + hook_id only)
    ///
    /// Hard non-responsibilities:
    /// - No combat decisions, prediction, reconciliation
    /// - No gameplay state mutation
    /// - No event buffering/reordering/delaying/suppressing
    /// - No visibility gating
    /// </summary>
    public sealed class CombatPresentationHookSystem : IDisposable
    {
        private readonly IReplicatedCombatEventStream _eventStream;
        private readonly IPresentationHookBus _hookBus;
        private readonly IPresentationValidationLogSink _validationLogSink;

        private bool _isSubscribed;

        public CombatPresentationHookSystem(
            IReplicatedCombatEventStream eventStream,
            IPresentationHookBus hookBus,
            IPresentationValidationLogSink validationLogSink)
        {
            _eventStream = eventStream ?? throw new ArgumentNullException(nameof(eventStream));
            _hookBus = hookBus ?? throw new ArgumentNullException(nameof(hookBus));
            _validationLogSink = validationLogSink ?? throw new ArgumentNullException(nameof(validationLogSink));
        }

        /// <summary>
        /// Subscribes to the replicated combat event stream.
        /// MUST be called on the client only.
        /// </summary>
        public void Start()
        {
            if (_isSubscribed) return;

            _eventStream.OnEventReceived += HandleEventReceived;
            _isSubscribed = true;
        }

        public void Dispose()
        {
            if (!_isSubscribed) return;

            _eventStream.OnEventReceived -= HandleEventReceived;
            _isSubscribed = false;
        }

        // ------------------------------------------------------------
        // Subscription handler: MUST NOT buffer, reorder, or delay
        // ------------------------------------------------------------

        private void HandleEventReceived(CombatEventPayload payload)
        {
            // Consume immediately, in the order invoked by the stream.
            // No buffering, no async scheduling, no reordering.

            if (payload == null)
                return; // fail-silent: missing payload

            // Dispatch presentation hooks. Failures must not block.
            switch (payload.EventType)
            {
                case CombatEventType.IntentResult:
                    DispatchIntentResultHooks(payload);
                    break;

                case CombatEventType.DamageOutcome:
                    DispatchDamageOutcomeHooks(payload);
                    break;

                case CombatEventType.MitigationOutcome:
                    DispatchMitigationOutcomeHooks(payload);
                    break;

                case CombatEventType.StateChange:
                    DispatchStateChangeHooks(payload);
                    break;

                default:
                    // Unknown event type: fail silent
                    break;
            }
        }

        // ------------------------------------------------------------
        // Dispatch: IntentResult
        // ------------------------------------------------------------

        private void DispatchIntentResultHooks(CombatEventPayload payload)
        {
            // Minimal required data: event_id + intent result summary
            var ir = payload.IntentResult;
            if (ir == null) return;

            // 1) UI notification hook (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Ui_IntentResult, () =>
            {
                _hookBus.Publish(new UiIntentResultHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    actorEntityId: ir.ActorEntityId,
                    intentType: ir.IntentType,
                    status: ir.ResultStatus));
            });

            // 2) Animation trigger hook (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Anim_IntentResult, () =>
            {
                _hookBus.Publish(new AnimationTriggerHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    subjectEntityId: ir.ActorEntityId,
                    trigger: AnimationTrigger.FromIntentResult(ir.IntentType, ir.ResultStatus)));
            });

            // 3) Audio cue hook (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Audio_IntentResult, () =>
            {
                _hookBus.Publish(new AudioCueHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    subjectEntityId: ir.ActorEntityId,
                    cue: AudioCue.FromIntentResult(ir.IntentType, ir.ResultStatus)));
            });
        }

        // ------------------------------------------------------------
        // Dispatch: DamageOutcome
        // ------------------------------------------------------------

        private void DispatchDamageOutcomeHooks(CombatEventPayload payload)
        {
            var d = payload.DamageOutcome;
            if (d == null) return;

            // 1) VFX spawn request (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Vfx_Damage, () =>
            {
                _hookBus.Publish(new VfxSpawnHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    sourceEntityId: d.SourceEntityId,
                    targetEntityId: d.TargetEntityId,
                    effect: VfxEffect.DamageImpact));
            });

            // 2) UI damage number (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Ui_Damage, () =>
            {
                _hookBus.Publish(new UiDamageNumberHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    targetEntityId: d.TargetEntityId));
            });

            // 3) Audio cue (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Audio_Damage, () =>
            {
                _hookBus.Publish(new AudioCueHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    subjectEntityId: d.TargetEntityId,
                    cue: AudioCue.DamageHit));
            });
        }

        // ------------------------------------------------------------
        // Dispatch: MitigationOutcome
        // ------------------------------------------------------------

        private void DispatchMitigationOutcomeHooks(CombatEventPayload payload)
        {
            var m = payload.MitigationOutcome;
            if (m == null) return;

            // 1) VFX shield / parry flash (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Vfx_Mitigation, () =>
            {
                _hookBus.Publish(new VfxSpawnHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    sourceEntityId: m.SourceEntityId,
                    targetEntityId: m.TargetEntityId,
                    effect: VfxEffect.MitigationFlash));
            });

            // 2) Audio cue (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Audio_Mitigation, () =>
            {
                _hookBus.Publish(new AudioCueHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    subjectEntityId: m.TargetEntityId,
                    cue: AudioCue.Mitigation));
            });
        }

        // ------------------------------------------------------------
        // Dispatch: StateChange
        // ------------------------------------------------------------

        private void DispatchStateChangeHooks(CombatEventPayload payload)
        {
            var s = payload.StateSnapshot;
            if (s == null) return;

            // 1) Animation state hook (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Anim_StateChange, () =>
            {
                _hookBus.Publish(new AnimationStateHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    subjectEntityId: s.EntityId,
                    state: s.State));
            });

            // 2) UI status indicator update (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Ui_StateChange, () =>
            {
                _hookBus.Publish(new UiCombatStateHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    subjectEntityId: s.EntityId,
                    state: s.State));
            });
        }

        // ------------------------------------------------------------
        // Non-blocking safety wrapper + validation mirror
        // ------------------------------------------------------------

        private void SafeInvokeHook(string eventId, string hookId, Action invoke)
        {
            // Validation mirror logs ONLY event_id + hook_id (no gameplay data).
            _validationLogSink.Record(eventId, hookId);

            try
            {
                invoke();
            }
            catch
            {
                // Fail silently: missing assets, animation exceptions, etc. must not block consumption.
            }
        }
    }

    // ====================================================================
    // Presentation Hook Bus + Stream Interfaces
    // ====================================================================

    public interface IReplicatedCombatEventStream
    {
        // Called by replication layer on the client, in receive order.
        event Action<CombatEventPayload> OnEventReceived;
    }

    public interface IPresentationHookBus
    {
        // Type-safe publication
        void Publish<T>(T hookMessage) where T : class;
    }

    public interface IPresentationValidationLogSink
    {
        // Logs event_id + hook_id only.
        void Record(string eventId, string hookId);
    }

    // ====================================================================
    // Hook IDs (stable, deterministic identifiers for validation)
    // ====================================================================

    public static class PresentationHookId
    {
        public const string Ui_IntentResult = "ui.intent_result";
        public const string Anim_IntentResult = "anim.intent_result";
        public const string Audio_IntentResult = "audio.intent_result";

        public const string Vfx_Damage = "vfx.damage";
        public const string Ui_Damage = "ui.damage";
        public const string Audio_Damage = "audio.damage";

        public const string Vfx_Mitigation = "vfx.mitigation";
        public const string Audio_Mitigation = "audio.mitigation";

        public const string Anim_StateChange = "anim.state_change";
        public const string Ui_StateChange = "ui.state_change";
    }

    // ====================================================================
    // Hook Message Types (type-safe, data-driven)
    // ====================================================================

    public sealed class AnimationTriggerHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public string SubjectEntityId { get; }
        public AnimationTrigger Trigger { get; }

        public AnimationTriggerHook(string eventId, int authoritativeTick, string combatContextId, string subjectEntityId, AnimationTrigger trigger)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            SubjectEntityId = subjectEntityId;
            Trigger = trigger;
        }
    }

    public sealed class AnimationStateHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public string SubjectEntityId { get; }
        public CombatState State { get; }

        public AnimationStateHook(string eventId, int authoritativeTick, string combatContextId, string subjectEntityId, CombatState state)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            SubjectEntityId = subjectEntityId;
            State = state;
        }
    }

    public sealed class VfxSpawnHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public string SourceEntityId { get; }
        public string TargetEntityId { get; }
        public VfxEffect Effect { get; }

        public VfxSpawnHook(string eventId, int authoritativeTick, string combatContextId, string sourceEntityId, string targetEntityId, VfxEffect effect)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            SourceEntityId = sourceEntityId;
            TargetEntityId = targetEntityId;
            Effect = effect;
        }
    }

    public sealed class AudioCueHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public string SubjectEntityId { get; }
        public AudioCue Cue { get; }

        public AudioCueHook(string eventId, int authoritativeTick, string combatContextId, string subjectEntityId, AudioCue cue)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            SubjectEntityId = subjectEntityId;
            Cue = cue;
        }
    }

    public sealed class UiIntentResultHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public string ActorEntityId { get; }
        public CombatIntentType IntentType { get; }
        public IntentResultStatus Status { get; }

        public UiIntentResultHook(string eventId, int authoritativeTick, string combatContextId, string actorEntityId, CombatIntentType intentType, IntentResultStatus status)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            ActorEntityId = actorEntityId;
            IntentType = intentType;
            Status = status;
        }
    }

    public sealed class UiDamageNumberHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public string TargetEntityId { get; }

        public UiDamageNumberHook(string eventId, int authoritativeTick, string combatContextId, string targetEntityId)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            TargetEntityId = targetEntityId;
        }
    }

    public sealed class UiCombatStateHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public string SubjectEntityId { get; }
        public CombatState State { get; }

        public UiCombatStateHook(string eventId, int authoritativeTick, string combatContextId, string subjectEntityId, CombatState state)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            SubjectEntityId = subjectEntityId;
            State = state;
        }
    }

    // ====================================================================
    // Data enums (presentation-facing, deterministic)
    // ====================================================================

    public enum AnimationTrigger
    {
        None,
        AttackResolved,
        DefendResolved,
        AbilityResolved,
        MovementResolved,
        InteractResolved,
        CancelResolved,
        IntentRejected
    }

    public static class AnimationTriggerExtensions
    {
        public static AnimationTrigger FromIntentResult(CombatIntentType intentType, IntentResultStatus status)
        {
            if (status == IntentResultStatus.Rejected)
                return AnimationTrigger.IntentRejected;

            if (status == IntentResultStatus.Canceled)
                return AnimationTrigger.CancelResolved;

            if (status != IntentResultStatus.Resolved)
                return AnimationTrigger.None;

            switch (intentType)
            {
                case CombatIntentType.CombatAttackIntent: return AnimationTrigger.AttackResolved;
                case CombatIntentType.CombatDefendIntent: return AnimationTrigger.DefendResolved;
                case CombatIntentType.CombatAbilityIntent: return AnimationTrigger.AbilityResolved;
                case CombatIntentType.CombatMovementIntent: return AnimationTrigger.MovementResolved;
                case CombatIntentType.CombatInteractIntent: return AnimationTrigger.InteractResolved;
                case CombatIntentType.CombatCancelIntent: return AnimationTrigger.CancelResolved;
                default: return AnimationTrigger.None;
            }
        }
    }

    public enum VfxEffect
    {
        DamageImpact,
        MitigationFlash
    }

    public enum AudioCue
    {
        None,
        IntentAccepted,
        IntentRejected,
        DamageHit,
        Mitigation
    }

    public static class AudioCueExtensions
    {
        public static AudioCue FromIntentResult(CombatIntentType intentType, IntentResultStatus status)
        {
            // Minimal mapping; no gameplay meaning inferred.
            if (status == IntentResultStatus.Rejected) return AudioCue.IntentRejected;
            if (status == IntentResultStatus.Resolved || status == IntentResultStatus.Canceled) return AudioCue.IntentAccepted;
            return AudioCue.None;
        }
    }

    // ====================================================================
    // Replicated event payload shapes (from Stage 12.5)
    // ====================================================================

    public sealed class CombatEventPayload
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public CombatEventType EventType { get; }

        public string? SubjectEntityId { get; }

        public IntentResult? IntentResult { get; }
        public DamageOutcome? DamageOutcome { get; }
        public MitigationOutcome? MitigationOutcome { get; }
        public CombatEntityState? StateSnapshot { get; }

        public CombatEventPayload(
            string eventId,
            int authoritativeTick,
            string combatContextId,
            CombatEventType eventType,
            string? subjectEntityId,
            IntentResult? intentResult,
            DamageOutcome? damageOutcome,
            MitigationOutcome? mitigationOutcome,
            CombatEntityState? stateSnapshot)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            EventType = eventType;
            SubjectEntityId = subjectEntityId;
            IntentResult = intentResult;
            DamageOutcome = damageOutcome;
            MitigationOutcome = mitigationOutcome;
            StateSnapshot = stateSnapshot;
        }
    }

    public enum CombatEventType
    {
        IntentResult,
        DamageOutcome,
        MitigationOutcome,
        StateChange
    }

    public sealed class IntentResult
    {
        public string IntentId { get; }
        public CombatIntentType IntentType { get; }
        public string ActorEntityId { get; }
        public IntentResultStatus ResultStatus { get; }

        public IntentResult(string intentId, CombatIntentType intentType, string actorEntityId, IntentResultStatus resultStatus)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntityId = actorEntityId;
            ResultStatus = resultStatus;
        }
    }

    public enum IntentResultStatus
    {
        Accepted,
        Rejected,
        Resolved,
        Canceled
    }

    public enum CombatIntentType
    {
        CombatAttackIntent,
        CombatDefendIntent,
        CombatAbilityIntent,
        CombatMovementIntent,
        CombatInteractIntent,
        CombatCancelIntent
    }

    public sealed class DamageOutcome
    {
        public string SourceEntityId { get; }
        public string TargetEntityId { get; }

        public DamageOutcome(string sourceEntityId, string targetEntityId)
        {
            SourceEntityId = sourceEntityId;
            TargetEntityId = targetEntityId;
        }
    }

    public sealed class MitigationOutcome
    {
        public string SourceEntityId { get; }
        public string TargetEntityId { get; }

        public MitigationOutcome(string sourceEntityId, string targetEntityId)
        {
            SourceEntityId = sourceEntityId;
            TargetEntityId = targetEntityId;
        }
    }

    public sealed class CombatEntityState
    {
        public string EntityId { get; }
        public CombatState State { get; }

        public CombatEntityState(string entityId, CombatState state)
        {
            EntityId = entityId;
            State = state;
        }
    }

    public enum CombatState
    {
        CombatIdle,
        CombatEngaged,
        CombatActing,
        CombatDefending,
        CombatRestricted,
        CombatIncapacitated
    }
}
