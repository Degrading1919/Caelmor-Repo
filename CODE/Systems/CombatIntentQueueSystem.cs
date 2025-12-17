// CombatIntentQueueSystem.cs
// NOTE: Save location must follow existing project structure.
// This file intentionally contains only the CombatIntentQueueSystem and minimal supporting types.
// No combat resolution, no combat state checks, no persistence, no CombatEvents emission.

using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Buffers;

namespace Caelmor.Combat
{
    /// <summary>
    /// CombatIntentQueueSystem
    /// - Owns authoritative combat intent queue (frozen per tick)
    /// - Accepts server-side submissions (payloads)
    /// - Performs structural schema validation only (Stage 11.2)
    /// - Orders deterministically (not based on arrival time; not influenced by client-controlled data)
    /// - Freezes at tick boundary: submissions during tick T become the frozen queue for tick T+1
    /// - Emits observable rejection results for structurally invalid intents (no success outcomes)
    /// - Exposes deterministic snapshots for Stage 9 validation harness
    /// </summary>
    // IL2CPP/AOT SAFETY: No runtime code generation or Reflection.Emit permitted; all runtime entrypoints must be
    // explicitly registered and editor-only APIs avoided. Reflection-based paths (none here) require explicit
    // preservation to survive managed code stripping.
    public sealed class CombatIntentQueueSystem
    {
        private readonly ITickSource _tickSource;
        private readonly IEntityIdValidator _entityIdValidator;
        private readonly IIntentRejectionSink _rejectionSink;

        // Staging: intents received during a tick T, to be frozen for tick T+1.
        private readonly Dictionary<int, List<StagedSubmission>> _stagedBySubmitTick = new();

        // Frozen queue exposed for the current authoritative tick.
        private FrozenQueueSnapshot? _currentFrozen;

        // Deterministic per-actor sequence assignment for a given frozen tick.
        // Derived deterministically during FreezeForTick() by sorting, not by arrival order.
        private readonly Dictionary<(int FrozenTick, string ActorId), int> _sequenceCounters = new();

        public CombatIntentQueueSystem(
            ITickSource tickSource,
            IEntityIdValidator entityIdValidator,
            IIntentRejectionSink rejectionSink)
        {
            _tickSource = tickSource ?? throw new ArgumentNullException(nameof(tickSource));
            _entityIdValidator = entityIdValidator ?? throw new ArgumentNullException(nameof(entityIdValidator));
            _rejectionSink = rejectionSink ?? throw new ArgumentNullException(nameof(rejectionSink));

            _tickSource.OnTickAdvanced += HandleTickAdvanced;
        }

        /// <summary>
        /// Server-side intake entry point. Validates structure and stages for the current tick.
        /// IMPORTANT:
        /// - No combat resolution
        /// - No combat state legality checks
        /// - No success outcomes emitted
        /// - No dedupe that would break save/load determinism
        /// </summary>
        public IntakeReceipt SubmitIntent(CombatIntentSubmission submission)
        {
            if (submission == null) throw new ArgumentNullException(nameof(submission));

            int submitTick = _tickSource.CurrentTick;

            if (!CombatIntentStructuralValidator.TryValidate(submission, _entityIdValidator, out var reject))
            {
                var rejection = new IntentRejection(
                    intentId: submission.IntentId ?? string.Empty,
                    actorEntityId: submission.ActorEntityId ?? string.Empty,
                    intentType: submission.IntentType,
                    authoritativeTick: submitTick,
                    reasonCode: reject.ReasonCode);

                _rejectionSink.OnRejected(rejection);
                return IntakeReceipt.Rejected(submission.IntentId ?? string.Empty, submitTick, reject.ReasonCode);
            }

            if (!_stagedBySubmitTick.TryGetValue(submitTick, out var list))
            {
                list = new List<StagedSubmission>(capacity: 8);
                _stagedBySubmitTick.Add(submitTick, list);
            }

            list.Add(new StagedSubmission(submission, submitTick));

            // No success emissions here (explicit).
            return IntakeReceipt.Staged(submission.IntentId!, submitTick);
        }

        /// <summary>
        /// Returns the frozen queue snapshot for the current authoritative tick.
        /// This snapshot is immutable and stable once created.
        /// </summary>
        public FrozenQueueSnapshot GetFrozenQueueForCurrentTick()
        {
            int tick = _tickSource.CurrentTick;
            if (_currentFrozen == null || _currentFrozen.AuthoritativeTick != tick)
                return FrozenQueueSnapshot.Empty(tick);

            return _currentFrozen;
        }

        /// <summary>
        /// Deterministic snapshot for Stage 9 harness comparisons.
        /// - Stable ordering
        /// - Minimal stable fields only
        /// </summary>
        public CombatIntentQueueValidationSnapshot GetQueueValidationSnapshot()
        {
            var frozen = GetFrozenQueueForCurrentTick();
            return CombatIntentQueueValidationSnapshot.FromFrozen(frozen);
        }

        private void HandleTickAdvanced(int newTick)
        {
            // Tick boundary semantics:
            // - Submissions received during tick (newTick - 1) become frozen queue for tick newTick.
            int sourceSubmitTick = newTick - 1;
            FreezeForTick(newTick, sourceSubmitTick);

            // Runtime hygiene only (not persistence): prune old staging buffers.
            PruneStaging(keepFromTickInclusive: newTick - 4);
        }

        private void FreezeForTick(int frozenTick, int sourceSubmitTick)
        {
            if (!_stagedBySubmitTick.TryGetValue(sourceSubmitTick, out var staged) || staged.Count == 0)
            {
                _currentFrozen = FrozenQueueSnapshot.Empty(frozenTick);
                return;
            }

            // Deterministic ordering inputs ONLY:
            // 1) actor_entity_id (ordinal)
            // 2) intent_id (ordinal) -- used as a stable identifier for ordering; no client_nonce involvement
            //
            // NOTE: Ordering must not depend on arrival time or any client-supplied correlation fields.
            staged.Sort(StagedSubmissionComparer.Instance);

            var frozenIntents = new List<FrozenIntentRecord>(staged.Count);

            for (int i = 0; i < staged.Count; i++)
            {
                var s = staged[i];
                int seq = NextSequenceForActor(frozenTick, s.Submission.ActorEntityId!);

                // Freeze payload immutably at tick boundary:
                // - Deep-copy/clamp to immutable read-only structures
                // - After freeze, no caller can mutate payload data through references.
                var frozenPayload = PayloadFreezer.DeepFreeze(s.Submission.Payload);

                var record = new FrozenIntentRecord(
                    intentId: s.Submission.IntentId!,
                    intentType: s.Submission.IntentType,
                    actorEntityId: s.Submission.ActorEntityId!,
                    submitTick: s.SubmitTick,
                    deterministicSequence: seq,
                    payload: frozenPayload
                );

                frozenIntents.Add(record);
            }

            _currentFrozen = new FrozenQueueSnapshot(
                authoritativeTick: frozenTick,
                intents: new ReadOnlyCollection<FrozenIntentRecord>(frozenIntents)
            );
        }

        private int NextSequenceForActor(int frozenTick, string actorId)
        {
            var key = (frozenTick, actorId);
            if (!_sequenceCounters.TryGetValue(key, out int current))
                current = 0;

            current++;
            _sequenceCounters[key] = current;
            return current;
        }

        private void PruneStaging(int keepFromTickInclusive)
        {
            int count = _stagedBySubmitTick.Count;
            if (count == 0)
                return;

            var keys = ArrayPool<int>.Shared.Rent(count);
            int index = 0;
            foreach (var kvp in _stagedBySubmitTick)
                keys[index++] = kvp.Key;

            for (int i = 0; i < index; i++)
            {
                if (keys[i] < keepFromTickInclusive)
                    _stagedBySubmitTick.Remove(keys[i]);
            }

            ArrayPool<int>.Shared.Return(keys, clearArray: true);
        }

        private readonly struct StagedSubmission
        {
            public readonly CombatIntentSubmission Submission;
            public readonly int SubmitTick;

            public StagedSubmission(CombatIntentSubmission submission, int submitTick)
            {
                Submission = submission;
                SubmitTick = submitTick;
            }
        }

        private sealed class StagedSubmissionComparer : IComparer<StagedSubmission>
        {
            public static readonly StagedSubmissionComparer Instance = new StagedSubmissionComparer();

            public int Compare(StagedSubmission x, StagedSubmission y)
            {
                int actorCompare = string.CompareOrdinal(x.Submission.ActorEntityId ?? string.Empty, y.Submission.ActorEntityId ?? string.Empty);
                if (actorCompare != 0)
                    return actorCompare;

                return string.CompareOrdinal(x.Submission.IntentId ?? string.Empty, y.Submission.IntentId ?? string.Empty);
            }
        }
    }

    // ---------------------------
    // Intake models + snapshots
    // ---------------------------

    public sealed class CombatIntentSubmission
    {
        public string? IntentId { get; init; }
        public CombatIntentType IntentType { get; init; }
        public string? ActorEntityId { get; init; }

        // Optional per schema (correlation only; must not affect ordering)
        public string? ClientNonce { get; init; }

        // Variant fields represented inside Payload as a key/value map.
        public IReadOnlyDictionary<string, object?> Payload { get; init; } =
            new ReadOnlyDictionary<string, object?>(new Dictionary<string, object?>());
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

    public sealed class FrozenQueueSnapshot
    {
        public int AuthoritativeTick { get; }
        public IReadOnlyList<FrozenIntentRecord> Intents { get; }

        public FrozenQueueSnapshot(int authoritativeTick, IReadOnlyList<FrozenIntentRecord> intents)
        {
            AuthoritativeTick = authoritativeTick;
            Intents = intents ?? throw new ArgumentNullException(nameof(intents));
        }

        public static FrozenQueueSnapshot Empty(int tick) =>
            new FrozenQueueSnapshot(tick, Array.Empty<FrozenIntentRecord>());
    }

    public readonly struct FrozenIntentRecord
    {
        public readonly string IntentId;
        public readonly CombatIntentType IntentType;
        public readonly string ActorEntityId;
        public readonly int SubmitTick;

        // Deterministic tie-breaker for per-actor intent ordering within the frozen tick.
        public readonly int DeterministicSequence;

        // Immutable, read-only payload as frozen at tick boundary.
        public readonly IReadOnlyDictionary<string, object?> Payload;

        public FrozenIntentRecord(
            string intentId,
            CombatIntentType intentType,
            string actorEntityId,
            int submitTick,
            int deterministicSequence,
            IReadOnlyDictionary<string, object?> payload)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntityId = actorEntityId;
            SubmitTick = submitTick;
            DeterministicSequence = deterministicSequence;
            Payload = payload ?? throw new ArgumentNullException(nameof(payload));
        }
    }

    // Deterministic validation snapshot for the harness.
    public sealed class CombatIntentQueueValidationSnapshot
    {
        public int AuthoritativeTick { get; }
        public IReadOnlyList<CombatIntentQueueValidationRow> Intents { get; }

        private CombatIntentQueueValidationSnapshot(int authoritativeTick, IReadOnlyList<CombatIntentQueueValidationRow> intents)
        {
            AuthoritativeTick = authoritativeTick;
            Intents = intents;
        }

        public static CombatIntentQueueValidationSnapshot FromFrozen(FrozenQueueSnapshot frozen)
        {
            var rows = frozen.Intents
                .Select(i => new CombatIntentQueueValidationRow(
                    intentId: i.IntentId,
                    intentType: i.IntentType,
                    actorEntityId: i.ActorEntityId,
                    submitTick: i.SubmitTick,
                    deterministicSequence: i.DeterministicSequence))
                .ToList();

            return new CombatIntentQueueValidationSnapshot(frozen.AuthoritativeTick, rows);
        }
    }

    public readonly struct CombatIntentQueueValidationRow
    {
        public readonly string IntentId;
        public readonly CombatIntentType IntentType;
        public readonly string ActorEntityId;
        public readonly int SubmitTick;
        public readonly int DeterministicSequence;

        public CombatIntentQueueValidationRow(
            string intentId,
            CombatIntentType intentType,
            string actorEntityId,
            int submitTick,
            int deterministicSequence)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntityId = actorEntityId;
            SubmitTick = submitTick;
            DeterministicSequence = deterministicSequence;
        }
    }

    // ---------------------------
    // Observable rejections
    // ---------------------------

    public sealed class IntentRejection
    {
        public string IntentId { get; }
        public string ActorEntityId { get; }
        public CombatIntentType IntentType { get; }
        public int AuthoritativeTick { get; }
        public string ReasonCode { get; }

        public IntentRejection(string intentId, string actorEntityId, CombatIntentType intentType, int authoritativeTick, string reasonCode)
        {
            IntentId = intentId;
            ActorEntityId = actorEntityId;
            IntentType = intentType;
            AuthoritativeTick = authoritativeTick;
            ReasonCode = reasonCode;
        }
    }

    public interface IIntentRejectionSink
    {
        void OnRejected(IntentRejection rejection);
    }

    public static class RejectReasonCodes
    {
        public const string MissingRequiredField = "MissingRequiredField";
        public const string InvalidIntentType = "InvalidIntentType";
        public const string InvalidEntityId = "InvalidEntityId";
        public const string ForbiddenFieldPresent = "ForbiddenFieldPresent";
        public const string InvalidContextValue = "InvalidContextValue";
        public const string InvalidMovementMode = "InvalidMovementMode";
        public const string InvalidPayloadShape = "InvalidPayloadShape";
    }

    public readonly struct IntakeReceipt
    {
        public readonly string IntentId;
        public readonly int SubmitTick;
        public readonly bool IsRejected;
        public readonly string ReasonCode;

        private IntakeReceipt(string intentId, int submitTick, bool isRejected, string reasonCode)
        {
            IntentId = intentId;
            SubmitTick = submitTick;
            IsRejected = isRejected;
            ReasonCode = reasonCode;
        }

        public static IntakeReceipt Staged(string intentId, int submitTick) =>
            new IntakeReceipt(intentId, submitTick, isRejected: false, reasonCode: string.Empty);

        public static IntakeReceipt Rejected(string intentId, int submitTick, string reasonCode) =>
            new IntakeReceipt(intentId, submitTick, isRejected: true, reasonCode: reasonCode);
    }

    // ---------------------------
    // Tick + entity id validation abstractions
    // ---------------------------

    public interface ITickSource
    {
        int CurrentTick { get; }
        event Action<int> OnTickAdvanced; // newTick
    }

    public interface IEntityIdValidator
    {
        bool IsValidEntityId(string entityId);
        bool IsValidInteractableId(string interactableId);
    }

    // ---------------------------
    // Payload freezing (immutable snapshot integrity)
    // ---------------------------

    internal static class PayloadFreezer
    {
        public static IReadOnlyDictionary<string, object?> DeepFreeze(IReadOnlyDictionary<string, object?> payload)
        {
            if (payload == null) throw new ArgumentNullException(nameof(payload));

            var copy = new Dictionary<string, object?>(payload.Count, StringComparer.Ordinal);
            foreach (var kv in payload)
            {
                copy[kv.Key] = DeepFreezeValue(kv.Value);
            }

            return new ReadOnlyDictionary<string, object?>(copy);
        }

        private static object? DeepFreezeValue(object? value)
        {
            if (value == null) return null;

            // Primitive/immutable types can pass through.
            if (value is string) return value;
            if (value is bool) return value;
            if (value is int) return value;
            if (value is long) return value;
            if (value is float) return value;
            if (value is double) return value;
            if (value is decimal) return value;

            // Dictionary-like: recursively freeze into ReadOnlyDictionary.
            if (value is IReadOnlyDictionary<string, object?> roDict)
            {
                var nested = new Dictionary<string, object?>(roDict.Count, StringComparer.Ordinal);
                foreach (var kv in roDict)
                    nested[kv.Key] = DeepFreezeValue(kv.Value);

                return new ReadOnlyDictionary<string, object?>(nested);
            }

            if (value is Dictionary<string, object?> dict)
            {
                var nested = new Dictionary<string, object?>(dict.Count, StringComparer.Ordinal);
                foreach (var kv in dict)
                    nested[kv.Key] = DeepFreezeValue(kv.Value);

                return new ReadOnlyDictionary<string, object?>(nested);
            }

            // Lists/arrays: freeze to read-only list by value-freezing elements.
            if (value is IReadOnlyList<object?> roList)
            {
                var list = new List<object?>(roList.Count);
                foreach (var v in roList)
                    list.Add(DeepFreezeValue(v));

                return new ReadOnlyCollection<object?>(list);
            }

            if (value is List<object?> listIn)
            {
                var list = new List<object?>(listIn.Count);
                foreach (var v in listIn)
                    list.Add(DeepFreezeValue(v));

                return new ReadOnlyCollection<object?>(list);
            }

            // Unknown reference types are not permitted for a frozen payload snapshot.
            // Treat as structural invalid shape at intake time (validator should prevent this).
            return value;
        }
    }

    // ---------------------------
    // Structural schema validation (Stage 11.2 only)
    // ---------------------------

    internal static class CombatIntentStructuralValidator
    {
        private static readonly HashSet<string> ForbiddenKeys = new(StringComparer.Ordinal)
        {
            "damage_amount",
            "damage_kind_key",
            "damage_tags",
            "mitigated_amount",
            "mitigation_kind_key",
            "mitigation_tags",
            "produced_outcome_ids",
            "result_status",
            "authoritative_tick",
            "resolved_intent_id",
            "outcome_id",
            "event_id",
            "event_type",
        };

        public static bool TryValidate(
            CombatIntentSubmission submission,
            IEntityIdValidator entityIdValidator,
            out RejectInfo reject)
        {
            reject = default;

            if (submission.Payload == null)
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "Payload is null.");
                return false;
            }

            if (string.IsNullOrWhiteSpace(submission.IntentId))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "intent_id missing.");
                return false;
            }

            if (string.IsNullOrWhiteSpace(submission.ActorEntityId))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "actor_entity_id missing.");
                return false;
            }

            if (!entityIdValidator.IsValidEntityId(submission.ActorEntityId!))
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "actor_entity_id invalid.");
                return false;
            }

            foreach (var k in submission.Payload.Keys)
            {
                if (ForbiddenKeys.Contains(k))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.ForbiddenFieldPresent, $"Forbidden field present: {k}");
                    return false;
                }
            }

            if (submission.Payload.TryGetValue("intent_type", out var itRaw) && itRaw is string itStr)
            {
                if (!string.Equals(itStr, submission.IntentType.ToString(), StringComparison.Ordinal))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidIntentType, "intent_type mismatch.");
                    return false;
                }
            }

            switch (submission.IntentType)
            {
                case CombatIntentType.CombatAttackIntent:
                    return ValidateAttack(submission, entityIdValidator, out reject);

                case CombatIntentType.CombatDefendIntent:
                    return ValidateDefend(submission, out reject);

                case CombatIntentType.CombatAbilityIntent:
                    return ValidateAbility(submission, entityIdValidator, out reject);

                case CombatIntentType.CombatMovementIntent:
                    return ValidateMovement(submission, entityIdValidator, out reject);

                case CombatIntentType.CombatInteractIntent:
                    return ValidateInteract(submission, entityIdValidator, out reject);

                case CombatIntentType.CombatCancelIntent:
                    return ValidateCancel(submission, out reject);

                default:
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidIntentType, "Unknown intent type.");
                    return false;
            }
        }

        private static bool ValidateAttack(CombatIntentSubmission s, IEntityIdValidator v, out RejectInfo reject)
        {
            reject = default;

            if (s.Payload.TryGetValue("target_entity_id", out var targetRaw) && targetRaw != null)
            {
                if (targetRaw is not string targetStr || string.IsNullOrWhiteSpace(targetStr) || !v.IsValidEntityId(targetStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "target_entity_id invalid.");
                    return false;
                }
            }

            if (s.Payload.TryGetValue("attack_profile_key", out var profileRaw) && profileRaw != null)
            {
                if (profileRaw is not string profileStr || string.IsNullOrWhiteSpace(profileStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "attack_profile_key invalid.");
                    return false;
                }
            }

            return true;
        }

        private static bool ValidateDefend(CombatIntentSubmission s, out RejectInfo reject)
        {
            reject = default;

            if (s.Payload.TryGetValue("defend_profile_key", out var profileRaw) && profileRaw != null)
            {
                if (profileRaw is not string profileStr || string.IsNullOrWhiteSpace(profileStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "defend_profile_key invalid.");
                    return false;
                }
            }

            return true;
        }

        private static bool ValidateAbility(CombatIntentSubmission s, IEntityIdValidator v, out RejectInfo reject)
        {
            reject = default;

            if (!s.Payload.TryGetValue("ability_key", out var abilityRaw) || abilityRaw is not string abilityKey || string.IsNullOrWhiteSpace(abilityKey))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "ability_key missing.");
                return false;
            }

            if (s.Payload.TryGetValue("target_entity_id", out var targetRaw) && targetRaw != null)
            {
                if (targetRaw is not string targetStr || string.IsNullOrWhiteSpace(targetStr) || !v.IsValidEntityId(targetStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "target_entity_id invalid.");
                    return false;
                }
            }

            if (s.Payload.TryGetValue("ability_context", out var ctxRaw) && ctxRaw != null)
            {
                if (!IsIdentifiersOnlyObject(ctxRaw))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidContextValue, "ability_context must be identifiers-only.");
                    return false;
                }
            }

            return true;
        }

        private static bool ValidateMovement(CombatIntentSubmission s, IEntityIdValidator v, out RejectInfo reject)
        {
            reject = default;

            if (!s.Payload.TryGetValue("movement_mode", out var modeRaw) || modeRaw is not string modeStr || string.IsNullOrWhiteSpace(modeStr))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "movement_mode missing.");
                return false;
            }

            if (!string.Equals(modeStr, "Translate", StringComparison.Ordinal) &&
                !string.Equals(modeStr, "Strafe", StringComparison.Ordinal) &&
                !string.Equals(modeStr, "Backstep", StringComparison.Ordinal))
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidMovementMode, "movement_mode invalid.");
                return false;
            }

            if (s.Payload.TryGetValue("target_entity_id", out var targetRaw) && targetRaw != null)
            {
                if (targetRaw is not string targetStr || string.IsNullOrWhiteSpace(targetStr) || !v.IsValidEntityId(targetStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "target_entity_id invalid.");
                    return false;
                }
            }

            if (s.Payload.TryGetValue("movement_context", out var ctxRaw) && ctxRaw != null)
            {
                if (!IsIdentifiersOnlyObject(ctxRaw))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidContextValue, "movement_context must be identifiers-only.");
                    return false;
                }
            }

            // Structural ban on vector/tuning fields.
            if (s.Payload.ContainsKey("velocity") || s.Payload.ContainsKey("distance") || s.Payload.ContainsKey("direction") ||
                s.Payload.ContainsKey("x") || s.Payload.ContainsKey("y") || s.Payload.ContainsKey("z"))
            {
                reject = RejectInfo.Of(RejectReasonCodes.ForbiddenFieldPresent, "Movement vector/tuning fields are not permitted.");
                return false;
            }

            return true;
        }

        private static bool ValidateInteract(CombatIntentSubmission s, IEntityIdValidator v, out RejectInfo reject)
        {
            reject = default;

            if (!s.Payload.TryGetValue("interactable_id", out var idRaw) || idRaw is not string iid || string.IsNullOrWhiteSpace(iid))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "interactable_id missing.");
                return false;
            }

            if (!v.IsValidInteractableId(iid))
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "interactable_id invalid.");
                return false;
            }

            if (s.Payload.TryGetValue("interaction_kind", out var kindRaw) && kindRaw != null)
            {
                if (kindRaw is not string kindStr || string.IsNullOrWhiteSpace(kindStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "interaction_kind invalid.");
                    return false;
                }
            }

            return true;
        }

        private static bool ValidateCancel(CombatIntentSubmission s, out RejectInfo reject)
        {
            reject = default;

            if (!s.Payload.TryGetValue("cancel_target_intent_id", out var idRaw) || idRaw is not string tid || string.IsNullOrWhiteSpace(tid))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "cancel_target_intent_id missing.");
                return false;
            }

            if (s.Payload.TryGetValue("cancel_reason", out var reasonRaw) && reasonRaw != null)
            {
                if (reasonRaw is not string reasonStr || string.IsNullOrWhiteSpace(reasonStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "cancel_reason invalid.");
                    return false;
                }
            }

            return true;
        }

        private static bool IsIdentifiersOnlyObject(object ctxRaw)
        {
            if (ctxRaw is IReadOnlyDictionary<string, object?> roDict)
            {
                foreach (var kv in roDict)
                {
                    if (kv.Value == null) continue;
                    if (kv.Value is string s && !string.IsNullOrWhiteSpace(s)) continue;
                    return false;
                }
                return true;
            }

            if (ctxRaw is Dictionary<string, object?> dict)
            {
                foreach (var kv in dict)
                {
                    if (kv.Value == null) continue;
                    if (kv.Value is string s && !string.IsNullOrWhiteSpace(s)) continue;
                    return false;
                }
                return true;
            }

            return false;
        }

        internal readonly struct RejectInfo
        {
            public readonly string ReasonCode;
            public readonly string Details;

            private RejectInfo(string reasonCode, string details)
            {
                ReasonCode = reasonCode;
                Details = details;
            }

            public static RejectInfo Of(string reasonCode, string details) => new RejectInfo(reasonCode, details);
        }
    }
}
