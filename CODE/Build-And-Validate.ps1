param(
    [string]$UnityEditorRoot = 'C:\Program Files\Unity\Hub\Editor\6000.5.5f1\Editor',
    [ValidateSet('Debug', 'Release')][string]$Configuration = 'Debug'
)
$ErrorActionPreference = 'Stop'
$repoDirectory = Split-Path -Parent $PSScriptRoot
if (!(Test-Json -LiteralPath (Join-Path $repoDirectory '04_CONTENT_PRODUCTION\Quests\LowmarkGameplay.json') -SchemaFile (Join-Path $repoDirectory 'DESIGNS\Templates & Schemas\GameplayContent.schema.json') -ErrorAction Stop)) { throw 'Gameplay schema validation failed' }
$sdk = Join-Path $UnityEditorRoot 'Data\DotNetSdk\dotnet.exe'
if (-not (Test-Path -LiteralPath $sdk)) {
    $sdk = (Get-Command dotnet -ErrorAction Stop).Source
}
& $sdk build (Join-Path $PSScriptRoot 'Validation\Caelmor.Validation.csproj') -c $Configuration --nologo "-p:UnityEditorRoot=$UnityEditorRoot"
if ($LASTEXITCODE -ne 0) { throw "C# build failed with exit code $LASTEXITCODE." }
& $sdk run --project (Join-Path $PSScriptRoot 'Validation\Caelmor.Validation.csproj') -c $Configuration --no-build --no-launch-profile
if ($LASTEXITCODE -ne 0) { throw "Runtime validation failed with exit code $LASTEXITCODE." }
