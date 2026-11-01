using System;
using System.Collections.Generic;

namespace Caelmor.Systems
{
    /// <summary>
    /// Stage 9.2: Validation runs only when explicitly enabled at server startup.
    /// This must not affect normal gameplay when disabled.
    /// </summary>
    public static class ValidationMode
    {
        public static bool IsEnabled(string[] args)
        {
            if (args == null) return false;

            for (int i = 0; i < args.Length; i++)
            {
                string a = args[i] ?? string.Empty;
                if (string.Equals(a, "-validate", StringComparison.OrdinalIgnoreCase) ||
                    string.Equals(a, "-validation", StringComparison.OrdinalIgnoreCase) ||
                    string.Equals(a, "-validateEconomy", StringComparison.OrdinalIgnoreCase))
                {
                    return true;
                }
            }

            return false;
        }
    }

    public interface IValidationLogger
    {
        void Info(string message);
        void Fail(string scenarioId, string reason);
        void Pass(string scenarioId);
    }

    public interface IAuthoritativeTickSource
    {
        int CurrentTick { get; }
        event Action<int> Tick;
    }

    public interface ISaveCheckpointInvoker
    {
        void RequestCheckpoint(string reasonCode);
        void CommitCheckpointIfRequested();

        /// <summary>
        /// Commits a checkpoint ONLY if a valid checkpoint boundary already exists.
        /// This must NOT force mid-tick, partial, or speculative commits.
        /// Intended for validation scenarios that need an explicit boundary.
        /// </summary>
        void CommitCheckpointNow();
    }

    public interface IRestoreInvoker
    {
        void RestorePlayerInventory(int playerId);
        void RestoreWorldAndZone(string zoneId);
    }

    public interface IAuthoritativeStateCapture
    {
        InventorySnapshot CaptureInventory(int playerId);
        NodeSnapshot CaptureNode(int nodeInstanceId);
    }

    public readonly struct InventorySnapshot
    {
        public readonly int PlayerId;
        public readonly IReadOnlyList<(string key, int count)> Entries;

        public InventorySnapshot(int playerId, IReadOnlyList<(string key, int count)> entries)
        {
            PlayerId = playerId;
            Entries = entries ?? Array.Empty<(string, int)>();
        }
    }

    public readonly struct NodeSnapshot
    {
        public readonly int NodeInstanceId;
        public readonly bool Exists;
        public readonly bool Available;
        public readonly int RespawnTicksRemaining;

        public NodeSnapshot(int nodeInstanceId, bool exists, bool available, int respawnTicksRemaining)
        {
            NodeInstanceId = nodeInstanceId;
            Exists = exists;
            Available = available;
            RespawnTicksRemaining = respawnTicksRemaining;
        }
    }

    public interface IValidationScenario
    {
        string ScenarioId { get; }
        void Reset(IScenarioContext ctx);
        ScenarioStepResult OnTick(IScenarioContext ctx, int tick);
    }

    public enum ScenarioStepStatus : byte
    {
        Running = 0,
        Passed = 1,
        Failed = 2
    }

    public readonly struct ScenarioStepResult
    {
        public readonly ScenarioStepStatus Status;
        public readonly string? FailureReason;

        private ScenarioStepResult(ScenarioStepStatus status, string? failureReason)
        {
            Status = status;
            FailureReason = failureReason;
        }

        public static ScenarioStepResult Running() => new ScenarioStepResult(ScenarioStepStatus.Running, null);
        public static ScenarioStepResult Passed() => new ScenarioStepResult(ScenarioStepStatus.Passed, null);
        public static ScenarioStepResult Failed(string reason) => new ScenarioStepResult(ScenarioStepStatus.Failed, reason);
    }

    public interface IScenarioContext
    {
        IAuthoritativeTickSource TickSource { get; }
        IAuthoritativeStateCapture State { get; }
        ISaveCheckpointInvoker Save { get; }
        IRestoreInvoker Restore { get; }
        IValidationLogger Log { get; }

        void EnqueueSerializedAction(string actionLabel, Action action);
    }
}
