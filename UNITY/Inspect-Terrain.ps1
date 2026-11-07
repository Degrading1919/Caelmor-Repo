param(
    [string]$UnityEditor = 'C:\Program Files\Unity\Hub\Editor\6000.5.5f1\Editor\Unity.exe',
    [switch]$Build,
    [switch]$SkipSmoke
)
$ErrorActionPreference = 'Stop'
$repositoryDirectory = Split-Path -Parent $PSScriptRoot
$terrainTools = Join-Path $repositoryDirectory 'CODE/Scripts/terrain_generation'
$previousPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = Join-Path $terrainTools '.scratch/deps'
    & py -3 -X utf8 (Join-Path $terrainTools 'export_inspection_payload.py')
    if ($LASTEXITCODE -ne 0) { throw 'Terrain payload export failed. Generate verified local outputs first.' }
} finally { $env:PYTHONPATH = $previousPythonPath }
& (Join-Path $PSScriptRoot 'Build.ps1') -UnityEditor $UnityEditor -StageOnly
if ($LASTEXITCODE -ne 0) { throw 'Runtime staging failed.' }
New-Item -ItemType Directory -Force -Path (Join-Path $PSScriptRoot 'Logs') | Out-Null
function Invoke-InspectionEditor([string]$method,[string]$logName) {
    $log = Join-Path $PSScriptRoot ('Logs/' + $logName)
    $process = Start-Process -FilePath $UnityEditor -ArgumentList @('-batchmode','-nographics','-quit','-projectPath',('"' + $PSScriptRoot + '"'),'-executeMethod',$method,'-logFile',('"' + $log + '"')) -WindowStyle Hidden -Wait -PassThru
    if ($process.ExitCode -ne 0) { throw "Terrain inspection operation failed ($($process.ExitCode)): $log" }
    Write-Output "Inspection log: $log"
}
Invoke-InspectionEditor 'Caelmor.Unity.Editor.TerrainInspectionEditor.GenerateAndValidate' 'terrain-inspection-generation.log'
if ($Build) {
    Invoke-InspectionEditor 'Caelmor.Unity.Editor.TerrainInspectionEditor.BuildWindows' 'terrain-inspection-build.log'
    $executable = Join-Path $PSScriptRoot 'Builds/TerrainInspection/CaelmorTerrainInspector.exe'
    if (!$SkipSmoke) {
        $log = Join-Path $PSScriptRoot 'Logs/terrain-inspection-player.log'
        $process = Start-Process -FilePath $executable -ArgumentList @('-batchmode','-nographics','--caelmor-terrain-smoke','-logFile',('"' + $log + '"')) -WindowStyle Hidden -PassThru
        if (!$process.WaitForExit(60000)) { $process.Kill(); throw "Terrain inspector smoke timed out: $log" }
        if ($process.ExitCode -ne 0 -or !(Select-String -LiteralPath $log -Pattern 'CAELMOR_TERRAIN_WALK_SMOKE_PASSED' -Quiet)) { throw "Terrain inspector smoke failed: $log" }
    }
    Write-Output "Walk the terrain: $executable"
} else { Write-Output 'Open Assets/_Project/World/TerrainInspection/LowmarkTerrainInspection.unity in Unity and press Play.' }
