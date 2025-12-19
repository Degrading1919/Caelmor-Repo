// CombatPresentationHookSystem.cs
// NOTE: Save location must follow existing project structure.
// Implements CombatPresentationHookSystem only.
// Client-side presentation hooks ONLY: animation/VFX/audio/UI callbacks.
// No gameplay state, no prediction, no networking, no persistence.

using System;
using System.Collections.Generic;
using Caelmor.Runtime.Tick;

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
                    actorEntity: ir.ActorEntity,
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
                    subjectEntity: ir.ActorEntity,
                    trigger: AnimationTrigger.FromIntentResult(ir.IntentType, ir.ResultStatus)));
            });

            // 3) Audio cue hook (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Audio_IntentResult, () =>
            {
                _hookBus.Publish(new AudioCueHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    subjectEntity: ir.ActorEntity,
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
                    sourceEntity: d.SourceEntity,
                    targetEntity: d.TargetEntity,
                    effect: VfxEffect.DamageImpact));
            });

            // 2) UI damage number (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Ui_Damage, () =>
            {
                _hookBus.Publish(new UiDamageNumberHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    targetEntity: d.TargetEntity));
            });

            // 3) Audio cue (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Audio_Damage, () =>
            {
                _hookBus.Publish(new AudioCueHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    subjectEntity: d.TargetEntity,
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
                    sourceEntity: m.SourceEntity,
                    targetEntity: m.TargetEntity,
                    effect: VfxEffect.MitigationFlash));
            });

            // 2) Audio cue (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Audio_Mitigation, () =>
            {
                _hookBus.Publish(new AudioCueHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    subjectEntity: m.TargetEntity,
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
                    subjectEntity: s.Entity,
                    state: s.State));
            });

            // 2) UI status indicator update (non-blocking)
            SafeInvokeHook(payload.EventId, PresentationHookId.Ui_StateChange, () =>
            {
                _hookBus.Publish(new UiCombatStateHook(
                    eventId: payload.EventId,
                    authoritativeTick: payload.AuthoritativeTick,
                    combatContextId: payload.CombatContextId,
                    subjectEntity: s.Entity,
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
        public EntityHandle SubjectEntity { get; }
        public AnimationTrigger Trigger { get; }

        public AnimationTriggerHook(string eventId, int authoritativeTick, string combatContextId, EntityHandle subjectEntity, AnimationTrigger trigger)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            SubjectEntity = subjectEntity;
            Trigger = trigger;
        }
    }

    public sealed class AnimationStateHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public EntityHandle SubjectEntity { get; }
        public CombatState State { get; }

        public AnimationStateHook(string eventId, int authoritativeTick, string combatContextId, EntityHandle subjectEntity, CombatState state)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            SubjectEntity = subjectEntity;
            State = state;
        }
    }

    public sealed class VfxSpawnHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public EntityHandle SourceEntity { get; }
        public EntityHandle TargetEntity { get; }
        public VfxEffect Effect { get; }

        public VfxSpawnHook(string eventId, int authoritativeTick, string combatContextId, EntityHandle sourceEntity, EntityHandle targetEntity, VfxEffect effect)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            SourceEntity = sourceEntity;
            TargetEntity = targetEntity;
            Effect = effect;
        }
    }

    public sealed class AudioCueHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public EntityHandle SubjectEntity { get; }
        public AudioCue Cue { get; }

        public AudioCueHook(string eventId, int authoritativeTick, string combatContextId, EntityHandle subjectEntity, AudioCue cue)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            SubjectEntity = subjectEntity;
            Cue = cue;
        }
    }

    public sealed class UiIntentResultHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public EntityHandle ActorEntity { get; }
        public CombatIntentType IntentType { get; }
        public IntentResultStatus Status { get; }

        public UiIntentResultHook(string eventId, int authoritativeTick, string combatContextId, EntityHandle actorEntity, CombatIntentType intentType, IntentResultStatus status)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            ActorEntity = actorEntity;
            IntentType = intentType;
            Status = status;
        }
    }

    public sealed class UiDamageNumberHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public EntityHandle TargetEntity { get; }

        public UiDamageNumberHook(string eventId, int authoritativeTick, string combatContextId, EntityHandle targetEntity)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            TargetEntity = targetEntity;
        }
    }

    public sealed class UiCombatStateHook
    {
        public string EventId { get; }
        public int AuthoritativeTick { get; }
        public string CombatContextId { get; }
        public EntityHandle SubjectEntity { get; }
        public CombatState State { get; }

        public UiCombatStateHook(string eventId, int authoritativeTick, string combatContextId, EntityHandle subjectEntity, CombatState state)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            SubjectEntity = subjectEntity;
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

        public EntityHandle SubjectEntity { get; }

        public IntentResult? IntentResult { get; }
        public DamageOutcome? DamageOutcome { get; }
        public MitigationOutcome? MitigationOutcome { get; }
        public CombatEntityState? StateSnapshot { get; }

        public CombatEventPayload(
            string eventId,
            int authoritativeTick,
            string combatContextId,
            CombatEventType eventType,
            EntityHandle subjectEntity,
            IntentResult? intentResult,
            DamageOutcome? damageOutcome,
            MitigationOutcome? mitigationOutcome,
            CombatEntityState? stateSnapshot)
        {
            EventId = eventId;
            AuthoritativeTick = authoritativeTick;
            CombatContextId = combatContextId;
            EventType = eventType;
            SubjectEntity = subjectEntity;
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
        public EntityHandle ActorEntity { get; }
        public IntentResultStatus ResultStatus { get; }

        public IntentResult(string intentId, CombatIntentType intentType, EntityHandle actorEntity, IntentResultStatus resultStatus)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntity = actorEntity;
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
        public EntityHandle SourceEntity { get; }
        public EntityHandle TargetEntity { get; }

        public DamageOutcome(EntityHandle sourceEntity, EntityHandle targetEntity)
        {
            SourceEntity = sourceEntity;
            TargetEntity = targetEntity;
        }
    }

    public sealed class MitigationOutcome
    {
        public EntityHandle SourceEntity { get; }
        public EntityHandle TargetEntity { get; }

        public MitigationOutcome(EntityHandle sourceEntity, EntityHandle targetEntity)
        {
            SourceEntity = sourceEntity;
            TargetEntity = targetEntity;
        }
    }

    public sealed class CombatEntityState
    {
        public EntityHandle Entity { get; }
        public CombatState State { get; }

        public CombatEntityState(EntityHandle entity, CombatState state)
        {
            Entity = entity;
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
