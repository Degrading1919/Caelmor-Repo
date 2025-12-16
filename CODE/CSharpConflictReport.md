# C# Conflict Report

This repository contains several conflicting or duplicated interface definitions that could lead to integration or compilation errors when wiring the systems together.

## Multiple `IValidationScenario` contracts

The validation harness in `Caelmor.Systems` expects scenarios implementing `ScenarioId`, `Reset`, and `OnTick` methods. Other validation modules (Onboarding, Player Runtime Instance, and Player ↔ Save Binding) define their own `IValidationScenario` interfaces with only `Name` and `Run(IAssert)` members. Because the signatures are incompatible, these scenarios cannot be registered with the harness without adapters or refactors.

* Tick-driven harness contract: `CODE/Systems/ValidationHarness_ConfigAndInterfaces.cs` lines 97-102.
* Onboarding scenarios contract: `CODE/Systems/OnboardingValidationScenarioExecution.cs` lines 428-432.
* Player runtime instance contract: `CODE/Systems/PlayerRuntimeInstanceValidationScenarios.cs` lines 159-163.
* Player ↔ save binding contract: `CODE/Systems/PlayerId↔SaveBindingValidationScenarios.cs` lines 193-197.

## Multiple `IAssert` surfaces

Each validation module also declares its own `IAssert` interface. Even though their members match, the separate declarations (with different namespaces) force consumers to reimplement identical adapters for each area or risk ambiguous references when adding `using` directives.

* Onboarding `IAssert`: `CODE/Systems/OnboardingValidationScenarioExecution.cs` lines 434-443.
* Player runtime instance `IAssert`: `CODE/Systems/PlayerRuntimeInstanceValidationScenarios.cs` lines 165-174.
* Player ↔ save binding `IAssert`: `CODE/Systems/PlayerId↔SaveBindingValidationScenarios.cs` lines 199-208.

## Repeated `IServerAuthority` definitions

There are three separate `IServerAuthority` interfaces across the runtime subsystems (Players, Sessions, Persistence). They share the same single `IsServerAuthoritative` property but live in different namespaces. This duplication encourages drift and makes it easy to pass the wrong authority type between systems.

* Persistence `IServerAuthority`: `CODE/Systems/PlayerIdentity+SaveBindingRuntime.cs` lines 183-185.
* Players `IServerAuthority`: `CODE/Systems/PlayerRuntimeInstanceManagement.cs` lines 203-208.
* Sessions `IServerAuthority`: `CODE/Systems/PlayerSessionSystem.cs` lines 338-341.

## Recommended next steps

* Unify the validation scenario and assert contracts (either via shared interfaces or adapters) so that all scenario sets can run under a common harness without duplication.
* Consolidate `IServerAuthority` into a single shared interface under a common namespace to prevent accidental mismatches between systems.
