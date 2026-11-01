param(
    [string]$UnityEditorRoot = 'C:\Program Files\Unity\Hub\Editor\6000.5.5f1\Editor',
    [ValidateSet('Debug', 'Release')][string]$Configuration = 'Debug'
)
$ErrorActionPreference = 'Stop'
$sdk = Join-Path $UnityEditorRoot 'Data\DotNetSdk\dotnet.exe'
if (-not (Test-Path -LiteralPath $sdk)) {
    $sdk = (Get-Command dotnet -ErrorAction Stop).Source
}
& $sdk build (Join-Path $PSScriptRoot 'Validation\Caelmor.Validation.csproj') -c $Configuration --nologo "-p:UnityEditorRoot=$UnityEditorRoot"
if ($LASTEXITCODE -ne 0) { throw "C# build failed with exit code $LASTEXITCODE." }
& $sdk run --project (Join-Path $PSScriptRoot 'Validation\Caelmor.Validation.csproj') -c $Configuration --no-build --no-launch-profile
if ($LASTEXITCODE -ne 0) { throw "Runtime validation failed with exit code $LASTEXITCODE." }
