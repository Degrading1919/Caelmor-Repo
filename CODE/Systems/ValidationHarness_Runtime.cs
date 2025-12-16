using System;
using System.Collections.Generic;

namespace Caelmor.Systems
{
    public sealed class ValidationHarness
    {
        private readonly IScenarioContext _ctx;
        private readonly IValidationLogger _log;
        private readonly List<IValidationScenario> _scenarios;

        private int _scenarioIndex;
        private IValidationScenario? _current;
        private bool _running;
        private bool _completed;

        public ValidationHarness(IScenarioContext ctx, IReadOnlyList<IValidationScenario> scenarios)
        {
            _ctx = ctx ?? throw new ArgumentNullException(nameof(ctx));
            _log = ctx.Log ?? throw new ArgumentNullException(nameof(ctx.Log));

            if (scenarios == null) throw new ArgumentNullException(nameof(scenarios));
            _scenarios = new List<IValidationScenario>(scenarios.Count);
            for (int i = 0; i < scenarios.Count; i++)
                _scenarios.Add(scenarios[i] ?? throw new ArgumentNullException($"scenarios[{i}]"));
        }

        public void Start()
        {
            if (_running) return;
            _running = true;
            _completed = false;

            _scenarioIndex = 0;
            _current = null;

            _log.Info("VALIDATION: Harness starting.");
            _ctx.TickSource.Tick += OnTick;
        }

        private void OnTick(int tick)
        {
            if (!_running || _completed)
                return;

            if (_current == null)
            {
                if (_scenarioIndex >= _scenarios.Count)
                {
                    _completed = true;
                    _running = false;
                    _ctx.TickSource.Tick -= OnTick;
                    _log.Info("VALIDATION: Harness complete.");
                    return;
                }

                _current = _scenarios[_scenarioIndex++];
                _log.Info($"VALIDATION: Starting scenario '{_current.ScenarioId}'.");
                _current.Reset(_ctx);
            }

            var step = _current.OnTick(_ctx, tick);

            if (step.Status == ScenarioStepStatus.Running)
                return;

            if (step.Status == ScenarioStepStatus.Passed)
            {
                _log.Pass(_current.ScenarioId);
                _current = null;
                return;
            }

            string reason = step.FailureReason ?? "unknown_failure";
            _log.Fail(_current.ScenarioId, reason);

            _completed = true;
            _running = false;
            _ctx.TickSource.Tick -= OnTick;

            throw new InvalidOperationException(
                $"VALIDATION FAILED: Scenario='{_current.ScenarioId}', Reason='{reason}'.");
        }
    }
}
