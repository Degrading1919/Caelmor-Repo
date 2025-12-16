using System;
using System.Collections.Generic;

namespace Caelmor.Systems
{
    /// <summary>
    /// Stage 9.4 — Scenario registration helper.
    /// Called from server composition root only when validation mode is enabled.
    /// Does not modify gameplay systems.
    /// </summary>
    public static class ValidationScenarioRegistration
    {
        public static IReadOnlyList<IValidationScenario> CreateStage9Scenarios(ValidationScenarioDeps deps)
            => ValidationScenario_Stage9Matrix.BuildAll(deps);
    }
}
