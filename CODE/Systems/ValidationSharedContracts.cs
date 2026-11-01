using System;
using System.Collections.Generic;

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
        void Equal<T>(T expected, T actual, string message);
    }

    public static class AssertExtensions
    {
        public static void SequenceEqual<T>(this IAssert assert, IEnumerable<T> expected, IEnumerable<T> actual, string message)
        {
            using (var left = expected.GetEnumerator())
            using (var right = actual.GetEnumerator())
            {
                while (left.MoveNext())
                {
                    if (!right.MoveNext() || !EqualityComparer<T>.Default.Equals(left.Current, right.Current))
                    {
                        assert.True(false, message);
                        return;
                    }
                }
                assert.False(right.MoveNext(), message);
            }
        }
    }
}
