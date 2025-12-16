using System;

namespace Caelmor.Validation
{
    /// <summary>
    /// Minimal validation scenario contract used by onboarding, player runtime,
    /// and save-binding validation suites. Scenarios run atomically when invoked.
    /// </summary>
    public interface IValidationScenario
    {
        string Name { get; }
        void Run(IAssert assert);
    }

    /// <summary>
    /// Shared assertion surface used by validation scenarios. Implementations
    /// may translate failures into harness-friendly diagnostics.
    /// </summary>
    public interface IAssert
    {
        void True(bool condition, string message);
        void False(bool condition, string message);
        void Equal<T>(T expected, T actual, string message) where T : IEquatable<T>;
    }
}
