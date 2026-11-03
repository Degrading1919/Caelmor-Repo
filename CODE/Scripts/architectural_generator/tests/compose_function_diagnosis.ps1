$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing

$generatorRoot=Split-Path -Parent $PSScriptRoot
$diagnosisRoot=Join-Path (Join-Path $generatorRoot 'evidence') 'function_v07_diagnosis'
$baselineRoot=Join-Path (Join-Path $generatorRoot 'evidence') 'function_v06'
$manifestPath=Join-Path $diagnosisRoot 'manifest.json'
if(-not (Test-Path -LiteralPath $manifestPath)){throw "Diagnosis manifest missing: $manifestPath"}
$manifest=Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$baselineSpecifications=@(
    @{Function='SMITHY';Region='LOWMARK';Label='SMITHY | LOWMARK'},
    @{Function='GATEHOUSE';Region='EMBERHOLT';Label='GATEHOUSE | EMBERHOLT'}
)
$rowSpecifications=@(
    @{Function='SMITHY';Region='LOWMARK';Mode='clay';Label='SMITHY | LOWMARK | CLAY'},
    @{Function='SMITHY';Region='LOWMARK';Mode='material';Label='SMITHY | LOWMARK | MATERIAL'},
    @{Function='GATEHOUSE';Region='EMBERHOLT';Mode='clay';Label='GATEHOUSE | EMBERHOLT | CLAY'},
    @{Function='GATEHOUSE';Region='EMBERHOLT';Mode='material';Label='GATEHOUSE | EMBERHOLT | MATERIAL'}
)
$columnSpecifications=@(
    @{Treatment='baseline';Label='BASELINE STUDIO'},
    @{Treatment='raking_light';Label='RAKING LIGHT ONLY'},
    @{Treatment='lower_frontage';Label='LOWER FRONTAGE ONLY'}
)
$tileW=1024; $tileH=704; $titleH=72; $columnHeaderH=48; $rowHeaderW=260; $rowLabelH=36
$canvasW=$rowHeaderW+($tileW*$columnSpecifications.Count)
$canvasH=$titleH+$columnHeaderH+(($tileH+$rowLabelH)*$rowSpecifications.Count)
$bitmap=[System.Drawing.Bitmap]::new($canvasW,$canvasH)
$graphics=[System.Drawing.Graphics]::FromImage($bitmap)
$graphics.Clear([System.Drawing.Color]::FromArgb(35,36,38))
$graphics.TextRenderingHint=[System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$headerFont=[System.Drawing.Font]::new('Segoe UI',18,[System.Drawing.FontStyle]::Bold)
$rowFont=[System.Drawing.Font]::new('Segoe UI',14,[System.Drawing.FontStyle]::Bold)
$bodyFont=[System.Drawing.Font]::new('Segoe UI',12,[System.Drawing.FontStyle]::Regular)
$ink=[System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(236,232,220))
$muted=[System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(185,182,172))
function Get-VerifiedImage($basePath,[string]$relative,[string]$expectedHash){
    $path=Join-Path $basePath ($relative -replace '/', [IO.Path]::DirectorySeparatorChar)
    if(-not (Test-Path -LiteralPath $path)){throw "Image missing: $path"}
    $actual=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if(-not $expectedHash -or $actual -ne $expectedHash.ToLowerInvariant()){throw "Image hash mismatch: $path"}
    $image=[System.Drawing.Image]::FromFile($path)
    if($image.Width -ne $tileW -or $image.Height -ne $tileH){$image.Dispose();throw "Image must be ${tileW}x${tileH}: $path"}
    return $image
}
try {
    $graphics.DrawString('FUNCTION DIAGNOSIS | CONTROLLED PRESENTATION COMPARISON',$headerFont,$ink,12,6)
    $graphics.DrawString('Existing v0.6 geometry and materials; compare one presentation factor at a time.',$bodyFont,$muted,12,40)
    for($column=0;$column -lt $columnSpecifications.Count;$column++){
        $x=$rowHeaderW+($column*$tileW)
        $graphics.DrawString($columnSpecifications[$column].Label,$headerFont,$ink,$x+12,$titleH+4)
    }
    for($rowIndex=0;$rowIndex -lt $rowSpecifications.Count;$rowIndex++){
        $rowSpec=$rowSpecifications[$rowIndex]
        $y=$titleH+$columnHeaderH+($rowIndex*($tileH+$rowLabelH))
        $graphics.DrawString($rowSpec.Label,$rowFont,$ink,12,$y+8)
        $diagnosisRecord=@($manifest.records | Where-Object {$_.function -eq $rowSpec.Function -and $_.region -eq $rowSpec.Region})
        if($diagnosisRecord.Count -ne 1){throw "Expected exactly one diagnosis record for $($rowSpec.Function)/$($rowSpec.Region); found $($diagnosisRecord.Count)."}
        $record=$diagnosisRecord[0]
        $baselineManifestPath=Join-Path (Join-Path $baselineRoot 'manifests') ($rowSpec.Function.ToLowerInvariant()+'.json')
        if(-not (Test-Path -LiteralPath $baselineManifestPath)){throw "v0.6 baseline manifest missing: $baselineManifestPath"}
        $baselineManifest=Get-Content -LiteralPath $baselineManifestPath -Raw | ConvertFrom-Json
        $baselineRecords=@($baselineManifest.records | Where-Object {$_.function -eq $rowSpec.Function -and $_.region -eq $rowSpec.Region})
        if($baselineRecords.Count -ne 1){throw "Expected one v0.6 baseline record for $($rowSpec.Function)/$($rowSpec.Region)."}
        $baselineRecord=$baselineRecords[0]
        if($record.geometry_hash -ne $baselineRecord.geometry_hash){throw "Diagnosis geometry differs from v0.6 baseline for $($rowSpec.Function)/$($rowSpec.Region)."}
        if(($record.settings | ConvertTo-Json -Compress -Depth 8) -ne ($baselineRecord.settings | ConvertTo-Json -Compress -Depth 8)){throw "Diagnosis settings differ from v0.6 baseline for $($rowSpec.Function)/$($rowSpec.Region)."}

        $baselineView=@($baselineRecord.views | Where-Object {$_.mode -eq $rowSpec.Mode -and [int]$_.view -eq 0})
        if($baselineView.Count -ne 1){throw "Missing v0.6 baseline front view for $($rowSpec.Function)/$($rowSpec.Region)/$($rowSpec.Mode)."}
        $diagnosisViews=@($record.views | Where-Object {$_.mode -eq $rowSpec.Mode})
        if($diagnosisViews.Count -ne 2){throw "Expected two diagnosis treatments for $($rowSpec.Function)/$($rowSpec.Region)/$($rowSpec.Mode)."}
        foreach($columnIndex in 0..2){
            $columnSpec=$columnSpecifications[$columnIndex]
            $x=$rowHeaderW+($columnIndex*$tileW)
            $image=$null
            if($columnSpec.Treatment -eq 'baseline'){
                $image=Get-VerifiedImage $baselineRoot ([string]$baselineView[0].image) ([string]$baselineView[0].image_sha256)
            } else {
                $view=@($diagnosisViews | Where-Object {$_.treatment -eq $columnSpec.Treatment})
                if($view.Count -ne 1){throw "Expected one $($columnSpec.Treatment) $($rowSpec.Mode) view for $($rowSpec.Function)/$($rowSpec.Region)."}
                $image=Get-VerifiedImage $diagnosisRoot ([string]$view[0].image) ([string]$view[0].sha256)
            }
            try {$graphics.DrawImage($image,$x,$y+$rowLabelH,$tileW,$tileH)} finally {$image.Dispose()}
            $graphics.DrawRectangle([System.Drawing.Pens]::DimGray,$x,$y+$rowLabelH,$tileW-1,$tileH-1)
        }
    }
    $outputPath=Join-Path $diagnosisRoot 'comparison.png'
    $bitmap.Save($outputPath,[System.Drawing.Imaging.ImageFormat]::Png)
    Write-Output "Composed comparison.png ($canvasW x $canvasH)"
} finally {
    $ink.Dispose();$muted.Dispose();$headerFont.Dispose();$rowFont.Dispose();$bodyFont.Dispose();$graphics.Dispose();$bitmap.Dispose()
}
