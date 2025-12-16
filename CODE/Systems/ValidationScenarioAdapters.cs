using System;
using Caelmor.Validation;

namespace Caelmor.Systems
{
    /// <summary>
    /// Bridges one-shot validation scenarios onto the tick-driven validation harness.
    /// </summary>
    public sealed class ValidationScenarioAdapter : IValidationScenario
    {
        private readonly Caelmor.Validation.IValidationScenario _scenario;
        private bool _hasRun;
        private AssertAdapter? _assert;

        public ValidationScenarioAdapter(Caelmor.Validation.IValidationScenario scenario)
        {
            _scenario = scenario ?? throw new ArgumentNullException(nameof(scenario));
        }

        public string ScenarioId => _scenario.Name;

        public void Reset(IScenarioContext ctx)
        {
            _ = ctx ?? throw new ArgumentNullException(nameof(ctx));
            _hasRun = false;
            _assert?.Reset();
        }

        public ScenarioStepResult OnTick(IScenarioContext ctx, int tick)
        {
            _ = ctx ?? throw new ArgumentNullException(nameof(ctx));
            _assert ??= new AssertAdapter(_scenario.Name, ctx.Log);

            if (_hasRun)
            {
                return ScenarioStepResult.Passed();
            }

            _assert.Reset();

            try
            {
                _scenario.Run(_assert);
            }
            catch (Exception ex)
            {
                ctx.Log.Fail(ScenarioId, ex.Message);
                _hasRun = true;
                return ScenarioStepResult.Failed(ex.Message);
            }

            _hasRun = true;

            if (_assert.HasFailure)
            {
                ctx.Log.Fail(ScenarioId, _assert.FailureMessage ?? "Unknown validation failure.");
                return ScenarioStepResult.Failed(_assert.FailureMessage ?? "Unknown validation failure.");
            }

            ctx.Log.Pass(ScenarioId);
            return ScenarioStepResult.Passed();
        }

        private sealed class AssertAdapter : Caelmor.Validation.IAssert
        {
            private readonly string _scenarioId;
            private readonly IValidationLogger _logger;

            public AssertAdapter(string scenarioId, IValidationLogger logger)
            {
                _scenarioId = scenarioId;
                _logger = logger ?? throw new ArgumentNullException(nameof(logger));
            }

            public bool HasFailure => FailureMessage != null;
            public string? FailureMessage { get; private set; }

            public void Reset()
            {
                FailureMessage = null;
            }

            public void True(bool condition, string message)
            {
                if (!condition)
                {
                    RecordFailure(message);
                }
            }

            public void False(bool condition, string message)
            {
                if (condition)
                {
                    RecordFailure(message);
                }
            }

            public void Equal<T>(T expected, T actual, string message) where T : IEquatable<T>
            {
                if (!Equals(expected, actual))
                {
                    RecordFailure(message);
                }
            }

            private void RecordFailure(string message)
            {
                if (FailureMessage != null)
                {
                    return;
                }

                FailureMessage = message;
                _logger.Fail(_scenarioId, message);
            }
        }
    }
}
