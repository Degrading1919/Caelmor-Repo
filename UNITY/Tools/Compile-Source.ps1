param([string]$UnityEditorRoot = 'C:\Program Files\Unity\Hub\Editor\6000.5.5f1\Editor')
$ErrorActionPreference = 'Stop'
$dotnet = Join-Path $UnityEditorRoot 'Data\DotNetSdk\dotnet.exe'
$scratchDirectory = Join-Path (Split-Path -Parent $PSScriptRoot) 'Obj\SourceCheck'
$intermediateDirectory = Join-Path $scratchDirectory 'obj\'
$binaryDirectory = Join-Path $scratchDirectory 'bin\'
& $dotnet build (Join-Path $PSScriptRoot 'Caelmor.Unity.SourceCheck.csproj') --configuration Release --nologo --verbosity quiet "-p:UnityEditorRoot=$UnityEditorRoot" "-p:BaseIntermediateOutputPath=$intermediateDirectory" "-p:OutputPath=$binaryDirectory"
if ($LASTEXITCODE -ne 0) { throw "Unity adapter source compilation failed with exit code $LASTEXITCODE" }
Write-Output 'Source compilation passed. This does not replace licensed Unity import, scene validation, or standalone smoke.'
