param(
    [switch]$InstallDependencies,
    [switch]$SkipMesh,
    [string]$Blender = 'C:\Program Files\Blender Foundation\Blender 5.0\blender.exe'
)
$ErrorActionPreference = 'Stop'
$repository = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$scratch = Join-Path $PSScriptRoot '.scratch'
$dependencies = Join-Path $scratch 'deps'
$output = Join-Path $repository 'MEDIA/Maps/Lowmark_Terrain'
$names = @('PYTHONPATH','PYTHONDONTWRITEBYTECODE','MPLCONFIGDIR','TEMP','TMP')
$previous = @{}
foreach($name in $names){$previous[$name]=[Environment]::GetEnvironmentVariable($name,'Process')}
Push-Location $repository
try {
    New-Item -ItemType Directory -Force -Path $dependencies,(Join-Path $scratch 'tmp'),(Join-Path $scratch 'matplotlib') | Out-Null
    $env:PYTHONPATH = $dependencies
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:MPLCONFIGDIR = Join-Path $scratch 'matplotlib'
    $env:TEMP = Join-Path $scratch 'tmp'
    $env:TMP = $env:TEMP
    if($InstallDependencies){
        & py -3 -m pip install --disable-pip-version-check --no-cache-dir --target $dependencies --upgrade -r (Join-Path $PSScriptRoot 'requirements.txt')
        if($LASTEXITCODE -ne 0){throw 'Terrain dependency setup failed'}
    }
    & py -3 -c 'import numpy, matplotlib, PIL; assert (numpy.__version__, matplotlib.__version__, PIL.__version__) == ("2.3.4", "3.10.7", "12.0.0"), "Pinned terrain dependency versions required"'
    if($LASTEXITCODE -ne 0){throw 'Run Generate-Lowmark.ps1 -InstallDependencies once to prepare checkout-local packages.'}
    & py -3 -m unittest discover -s $PSScriptRoot -p test_terrain.py -v
    if($LASTEXITCODE -ne 0){throw 'Terrain mathematical regression checks failed'}
    & py -3 -m unittest discover -s (Join-Path $PSScriptRoot 'tests') -p 'test_hydrology_review.py' -v
    if($LASTEXITCODE -ne 0){throw 'Independent terrain/hydrology checks failed'}
    & py -3 (Join-Path $PSScriptRoot 'build_prototype.py') --output $output
    if($LASTEXITCODE -ne 0){throw 'Terrain generation/verification failed'}
    if(!$SkipMesh){
        if(!(Test-Path -LiteralPath $Blender -PathType Leaf)){throw 'Blender missing. Set -Blender to the installed executable or use -SkipMesh for array/figure generation only.'}
        $log = Join-Path $scratch 'blender-export.log'
        $arguments = @('--background','--factory-startup','--python-exit-code','1','--python',('"'+(Join-Path $PSScriptRoot 'export_blender.py')+'"'),'--','--arrays',('"'+(Join-Path $output 'terrain_arrays.npz')+'"'),'--output',('"'+(Join-Path $output 'terrain.glb')+'"'))
        $process = Start-Process -FilePath $Blender -ArgumentList $arguments -WindowStyle Hidden -RedirectStandardOutput $log -RedirectStandardError (Join-Path $scratch 'blender-export-errors.log') -Wait -PassThru
        if($process.ExitCode -ne 0){throw "Terrain GLB export failed; inspect $log"}
        & py -3 (Join-Path $PSScriptRoot 'verify_glb.py') --arrays (Join-Path $output 'terrain_arrays.npz') --glb (Join-Path $output 'terrain.glb') --report (Join-Path $output 'mesh_verification.json')
        if($LASTEXITCODE -ne 0){throw 'Full-resolution terrain GLB verification failed'}
    }
    Write-Output "Lowmark offline terrain ready: $output"
} finally {
    foreach($name in $names){[Environment]::SetEnvironmentVariable($name,$previous[$name],'Process')}
    Pop-Location
}
