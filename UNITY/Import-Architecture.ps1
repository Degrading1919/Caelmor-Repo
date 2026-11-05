[CmdletBinding(DefaultParameterSetName = 'Import')]
param(
    [Parameter(Mandatory, ParameterSetName = 'Import')][string]$Source,
    [Parameter(Mandatory, ParameterSetName = 'Import')][string]$Key,
    [Parameter(ParameterSetName = 'Import')][string]$Bindings,
    [Parameter(Mandatory, ParameterSetName = 'Validate')][switch]$Validate,
    [string]$UnityEditor = 'C:\Program Files\Unity\Hub\Editor\6000.5.5f1\Editor\Unity.exe'
)
$ErrorActionPreference = 'Stop'
if (!(Test-Path -LiteralPath $UnityEditor -PathType Leaf)) { throw "Unity editor missing: $UnityEditor" }
if (!$Validate) {
    $Source = (Resolve-Path -LiteralPath $Source).Path
    $repositoryPath = [IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot)) + [IO.Path]::DirectorySeparatorChar
    if (!$Source.StartsWith($repositoryPath, [StringComparison]::OrdinalIgnoreCase)) { throw 'Keep building exports inside the designated Caelmor checkout before importing.' }
    if ([IO.Path]::GetExtension($Source) -ine '.glb') { throw 'Export a GLB with its .caelmor.json sidecar and collision GLB.' }
    if ($Key -cnotmatch '^[a-z0-9][a-z0-9_-]*$') { throw 'Key must be a stable lowercase asset ID containing letters, digits, underscore or hyphen.' }
    $sidecar = [IO.Path]::ChangeExtension($Source, '.caelmor.json')
    if (!(Test-Path -LiteralPath $sidecar -PathType Leaf)) { throw "Missing export sidecar: $sidecar" }
}
& (Join-Path $PSScriptRoot 'Build.ps1') -UnityEditor $UnityEditor -StageOnly
if ($LASTEXITCODE -ne 0) { throw 'Runtime staging failed.' }
$logDirectory = Join-Path $PSScriptRoot 'Logs'
New-Item -ItemType Directory -Force -Path $logDirectory | Out-Null
$environmentNames = @('CAELMOR_ARCHITECTURE_SOURCE','CAELMOR_ARCHITECTURE_KEY','CAELMOR_ARCHITECTURE_BINDINGS','CAELMOR_ARCHITECTURE_BUILD_OUTPUT')
$previousEnvironment = @{}
foreach ($name in $environmentNames) { $previousEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, 'Process') }
function Invoke-ArchitectureEditor([string]$method, [string]$logName, [string]$successMarker) {
    $logPath = Join-Path $logDirectory $logName
    $arguments = @('-batchmode','-nographics','-quit','-projectPath',('"' + $PSScriptRoot + '"'),'-executeMethod',$method,'-logFile',('"' + $logPath + '"'))
    $process = Start-Process -FilePath $UnityEditor -ArgumentList $arguments -WindowStyle Hidden -Wait -PassThru
    if ($process.ExitCode -ne 0) { throw "Architecture operation failed ($($process.ExitCode)). Inspect $logPath" }
    if (!(Select-String -LiteralPath $logPath -SimpleMatch $successMarker -Quiet)) { throw "Architecture operation emitted no success marker. Inspect $logPath" }
    Write-Output "Architecture log: $logPath"
}
try {
    $env:CAELMOR_ARCHITECTURE_SOURCE = $Source
    $env:CAELMOR_ARCHITECTURE_KEY = $Key
    $env:CAELMOR_ARCHITECTURE_BINDINGS = $Bindings
    if ($Validate) {
        Invoke-ArchitectureEditor 'Caelmor.Unity.Editor.SceneOwnershipValidation.Run' 'scene-ownership-validation.log' 'CAELMOR_SCENE_OWNERSHIP_CHECKS_PASSED'
        Invoke-ArchitectureEditor 'Caelmor.Unity.Editor.ArchitectureValidation.Run' 'architecture-validation.log' 'CAELMOR_ARCHITECTURE_VALIDATION_PASSED'
        Invoke-ArchitectureEditor 'Caelmor.Unity.Editor.ArchitectureValidation.ValidateSavedAssets' 'architecture-persistence.log' 'CAELMOR_ARCHITECTURE_PERSISTENCE_PASSED'
        $env:CAELMOR_ARCHITECTURE_BUILD_OUTPUT = Join-Path $PSScriptRoot 'Builds/ArchitectureValidation/CaelmorArchitectureValidation.exe'
        Invoke-ArchitectureEditor 'Caelmor.Unity.Editor.ArchitectureValidation.BuildValidationPlayer' 'architecture-player-build.log' 'CAELMOR_ARCHITECTURE_PLAYER_BUILT'
        $playerLog = Join-Path $logDirectory 'architecture-player.log'
        # Null graphics does not expose the custom shader's runtime properties.
        # Use a real renderer in hidden, non-interactive batch mode for this check.
        $player = Start-Process -FilePath $env:CAELMOR_ARCHITECTURE_BUILD_OUTPUT -ArgumentList @('-batchmode','-force-d3d11','-screen-width','64','-screen-height','64','-logFile',('"' + $playerLog + '"')) -WindowStyle Hidden -PassThru
        if (!$player.WaitForExit(60000)) { $player.Kill(); throw "Architecture player timed out. Inspect $playerLog" }
        if ($player.ExitCode -ne 0 -or !(Select-String -LiteralPath $playerLog -SimpleMatch 'CAELMOR_ARCHITECTURE_PLAYER_PASSED' -Quiet)) { throw "Architecture player verification failed. Inspect $playerLog" }
        Write-Output "Architecture player verification passed. Log: $playerLog"
    } else {
        Invoke-ArchitectureEditor 'Caelmor.Unity.Editor.ArchitectureImport.ImportFromEnvironment' ('architecture-import-' + $Key + '.log') 'CAELMOR_ARCHITECTURE_IMPORTED'
    }
} finally {
    foreach ($name in $environmentNames) { [Environment]::SetEnvironmentVariable($name, $previousEnvironment[$name], 'Process') }
}
