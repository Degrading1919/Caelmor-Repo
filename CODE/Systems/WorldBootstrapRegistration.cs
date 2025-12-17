using System;
using Caelmor.Runtime.WorldSimulation;

namespace Caelmor.Runtime.Host
{
    /// <summary>
    /// Explicit, IL2CPP-safe registration helper for world simulation participants.
    /// Avoids reflection-based discovery and ensures deterministic ordering across builds.
    /// </summary>
    public static class WorldBootstrapRegistration
    {
        /// <summary>
        /// Registers gates, participants, and hooks in the order provided. No reflection or runtime codegen.
        /// </summary>
        public static void Apply(
            WorldSimulationCore simulation,
            ReadOnlySpan<ISimulationEligibilityGate> eligibilityGates,
            ReadOnlySpan<ParticipantRegistration> participants,
            ReadOnlySpan<PhaseHookRegistration> phaseHooks)
        {
            if (simulation is null) throw new ArgumentNullException(nameof(simulation));

            for (int i = 0; i < eligibilityGates.Length; i++)
            {
                var gate = eligibilityGates[i] ?? throw new ArgumentNullException($"{nameof(eligibilityGates)}[{i}]");
                simulation.RegisterEligibilityGate(gate);
            }

            for (int i = 0; i < participants.Length; i++)
            {
                var entry = participants[i];
                if (entry.Participant is null)
                    throw new ArgumentNullException($"{nameof(participants)}[{i}]");

                simulation.RegisterParticipant(entry.Participant, entry.OrderKey);
            }

            for (int i = 0; i < phaseHooks.Length; i++)
            {
                var entry = phaseHooks[i];
                if (entry.Hook is null)
                    throw new ArgumentNullException($"{nameof(phaseHooks)}[{i}]");

                simulation.RegisterPhaseHook(entry.Hook, entry.OrderKey);
            }
        }
    }

    /// <summary>
    /// Deterministic registration descriptor for a simulation participant.
    /// </summary>
    public readonly struct ParticipantRegistration
    {
        public ISimulationParticipant Participant { get; }
        public int OrderKey { get; }

        public ParticipantRegistration(ISimulationParticipant participant, int orderKey)
        {
            Participant = participant ?? throw new ArgumentNullException(nameof(participant));
            OrderKey = orderKey;
        }
    }

    /// <summary>
    /// Deterministic registration descriptor for a tick phase hook.
    /// </summary>
    public readonly struct PhaseHookRegistration
    {
        public ITickPhaseHook Hook { get; }
        public int OrderKey { get; }

        public PhaseHookRegistration(ITickPhaseHook hook, int orderKey)
        {
            Hook = hook ?? throw new ArgumentNullException(nameof(hook));
            OrderKey = orderKey;
        }
    }
}
