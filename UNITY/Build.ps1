param(
    [string]$UnityEditor = 'C:\Program Files\Unity\Hub\Editor\6000.5.5f1\Editor\Unity.exe',
    [string]$OutputDirectory = (Join-Path $PSScriptRoot 'Builds\Windows'),
    [switch]$StageOnly,
    [switch]$SkipSmoke
)
$ErrorActionPreference = 'Stop'
$projectDirectory = $PSScriptRoot
$repositoryDirectory = Split-Path -Parent $projectDirectory
$editorDirectory = Split-Path -Parent $UnityEditor
$dotnet = Join-Path $editorDirectory 'Data\DotNetSdk\dotnet.exe'
$contentPath = Join-Path $repositoryDirectory '04_CONTENT_PRODUCTION\Quests\LowmarkGameplay.json'
$schemaPath = Join-Path $repositoryDirectory 'DESIGNS\Templates & Schemas\GameplayContent.schema.json'
if (!(Test-Json -LiteralPath $contentPath -SchemaFile $schemaPath -ErrorAction Stop)) { throw 'Gameplay content schema validation failed' }
$resourceDirectory = Join-Path $projectDirectory 'Assets\_Project\Content\Resources'
New-Item -ItemType Directory -Force -Path $resourceDirectory | Out-Null
Copy-Item -LiteralPath $contentPath -Destination (Join-Path $resourceDirectory 'LowmarkGameplay.json') -Force
if (!(Test-Path -LiteralPath $UnityEditor)) { throw "Unity editor missing: $UnityEditor" }
& $dotnet build (Join-Path $repositoryDirectory 'CODE\Caelmor.Runtime.csproj') --configuration Release --nologo --verbosity quiet '-clp:ErrorsOnly;Summary'
if ($LASTEXITCODE -ne 0) { throw "Runtime assembly build failed with exit code $LASTEXITCODE" }
$pluginsDirectory = Join-Path $projectDirectory 'Assets\_Project\Core\Plugins'
New-Item -ItemType Directory -Force -Path $pluginsDirectory, $OutputDirectory | Out-Null
Copy-Item -LiteralPath (Join-Path $repositoryDirectory 'CODE\bin\Release\netstandard2.1\Caelmor.Runtime.dll') -Destination $pluginsDirectory -Force
if ($StageOnly) { Write-Output "Runtime staged. Open Unity project: $projectDirectory"; exit 0 }
$env:CAELMOR_BUILD_OUTPUT = Join-Path $OutputDirectory 'Caelmor.exe'
$editorLog = Join-Path $OutputDirectory 'unity-build.log'
$unityArguments = @('-batchmode', '-nographics', '-quit', '-projectPath', ('"' + $projectDirectory + '"'), '-executeMethod', 'Caelmor.Unity.Editor.CaelmorBuild.BuildWindows', '-logFile', ('"' + $editorLog + '"'))
$buildProcess = Start-Process -FilePath $UnityEditor -ArgumentList $unityArguments -WindowStyle Hidden -Wait -PassThru
if ($buildProcess.ExitCode -ne 0) { throw "Unity build failed with exit code $($buildProcess.ExitCode). Log: $editorLog" }
if (!$SkipSmoke)
{
    $smokeLog = Join-Path $OutputDirectory 'standalone-smoke.log'
    $smokeProcess = Start-Process -FilePath $env:CAELMOR_BUILD_OUTPUT -ArgumentList @('-batchmode', '-nographics', '--caelmor-smoke', '-logFile', ('"' + $smokeLog + '"')) -WindowStyle Hidden -PassThru
    if (!$smokeProcess.WaitForExit(60000)) { $smokeProcess.Kill(); throw "Standalone smoke timed out. Log: $smokeLog" }
    if ($smokeProcess.ExitCode -ne 0) { throw "Standalone smoke failed with exit code $($smokeProcess.ExitCode). Log: $smokeLog" }
    if (!(Select-String -LiteralPath $smokeLog -Pattern 'CAELMOR_SMOKE_PASSED' -Quiet)) { throw "Standalone did not emit success marker. Log: $smokeLog" }
}
Write-Output "Build ready: $env:CAELMOR_BUILD_OUTPUT"
