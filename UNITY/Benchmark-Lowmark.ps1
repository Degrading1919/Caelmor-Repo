[CmdletBinding()]
param(
    [string]$UnityEditor = 'C:\Program Files\Unity\Hub\Editor\6000.5.5f1\Editor\Unity.exe',
    [string]$Blender = 'C:\Program Files\Blender Foundation\Blender 5.0\blender.exe',
    [string]$ExportDirectory,
    [ValidateSet('baseline','optimized','nomips','all')][string]$Configuration = 'all'
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$showcase = Join-Path $repo 'CODE/Scripts/architectural_generator/evidence/lowmark_settlement'
$working = Join-Path $showcase '.perf'
$results = Join-Path $PSScriptRoot 'Builds/LowmarkPerformance'
New-Item -ItemType Directory -Force -Path $working,$results | Out-Null
if (!$ExportDirectory) {
    $log = Join-Path $working 'export.log'
    & $Blender --background --factory-startup (Join-Path $showcase 'Lowmark_Settlement.blend') --python-exit-code 1 --python (Join-Path $showcase 'export_performance.py') *> $log
    if ($LASTEXITCODE -ne 0) { throw "Showcase export failed. See $log" }
    $marker = Select-String -LiteralPath $log -Pattern '^CAELMOR_PERF_EXPORT (.+)$' | Select-Object -Last 1
    if (!$marker) { throw "Showcase export marker missing. See $log" }
    $ExportDirectory = $marker.Matches[0].Groups[1].Value
}
$ExportDirectory = (Resolve-Path -LiteralPath $ExportDirectory).Path
$previous = @{}
$names = @('CAELMOR_PERF_SOURCE','CAELMOR_PERF_BUILDS','CAELMOR_PERF_COMPRESSED','CAELMOR_PERF_OUTPUT','CAELMOR_PERF_FORCE_RESIDENT')
foreach ($name in $names) { $previous[$name] = [Environment]::GetEnvironmentVariable($name,'Process') }
try {
    & (Join-Path $PSScriptRoot 'Build.ps1') -UnityEditor $UnityEditor -StageOnly
    if ($LASTEXITCODE -ne 0) { throw 'Runtime staging failed' }
    $env:CAELMOR_PERF_SOURCE = $ExportDirectory
    $env:CAELMOR_PERF_BUILDS = $results
    $cases = if ($Configuration -eq 'all') { @('baseline','optimized','nomips') } else { @($Configuration) }
    foreach ($case in $cases) {
        $env:CAELMOR_PERF_COMPRESSED = switch ($case) { 'optimized' { '1' }; 'nomips' { '2' }; default { '0' } }
        $folder = switch ($case) { 'optimized' { 'compressed_streaming_nonreadable' }; 'nomips' { 'uncompressed_nomips' }; default { 'baseline' } }
        $log = Join-Path $results "$case-build.log"
        $args = @('-batchmode','-nographics','-quit','-projectPath',('"' + $PSScriptRoot + '"'),'-executeMethod','Caelmor.Unity.Editor.LowmarkPerformanceBuild.Build','-logFile',('"' + $log + '"'))
        $operation = Start-Process -FilePath $UnityEditor -ArgumentList $args -WindowStyle Hidden -Wait -PassThru
        if ($operation.ExitCode -ne 0 -or !(Select-String -LiteralPath $log -Pattern 'CAELMOR_PERF_BUILT' -Quiet)) { throw "Unity build failed. See $log" }
        $runs = if ($case -eq 'optimized') { @('optimized','resident') } else { @($case) }
        foreach ($run in $runs) {
            $env:CAELMOR_PERF_FORCE_RESIDENT = if ($run -eq 'resident') { '1' } else { '0' }
            $env:CAELMOR_PERF_OUTPUT = Join-Path $results "$run-results"
            $playerLog = Join-Path $results "$run-player.log"
            $player = Start-Process -FilePath (Join-Path $results "$folder/LowmarkPerformance.exe") -ArgumentList @('-force-d3d11','-screen-fullscreen','0','-screen-width','1920','-screen-height','1080','-logFile',('"' + $playerLog + '"')) -WindowStyle Hidden -PassThru
            if (!$player.WaitForExit(300000)) { $player.Kill(); throw "Benchmark timed out. See $playerLog" }
            if ($player.ExitCode -ne 0 -or !(Select-String -LiteralPath $playerLog -Pattern 'CAELMOR_PERFORMANCE_COMPLETE' -Quiet)) { throw "Benchmark run failed. See $playerLog" }
            Write-Output "Completed $run at $env:CAELMOR_PERF_OUTPUT"
        }
    }
} finally {
    foreach ($name in $names) { [Environment]::SetEnvironmentVariable($name,$previous[$name],'Process') }
}
