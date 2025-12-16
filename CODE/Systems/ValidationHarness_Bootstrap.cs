using System;
using System.Collections.Generic;

namespace Caelmor.Systems
{
    /// <summary>
    /// Stage 9.2: Bootstrap entry point.
    /// Call this from your existing server composition root after Stage 7–8 systems are constructed.
    ///
    /// When validation mode is disabled, this returns null and does nothing.
    /// When enabled, scenarios auto-run on server start.
    /// </summary>
    public static class ValidationHarnessBootstrap
    {
        public static ValidationHarness? TryBoot(
            string[] startupArgs,
            IScenarioContext scenarioContext,
            IReadOnlyList<IValidationScenario> scenarios)
        {
            if (!ValidationMode.IsEnabled(startupArgs))
                return null;

            if (scenarioContext == null) throw new ArgumentNullException(nameof(scenarioContext));
            if (scenarios == null) throw new ArgumentNullException(nameof(scenarios));

            var harness = new ValidationHarness(scenarioContext, scenarios);
            harness.Start();
            return harness;
        }
    }
}
