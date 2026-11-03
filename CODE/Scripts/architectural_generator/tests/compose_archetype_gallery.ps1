param([string[]]$Functions)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing

$generatorRoot=Split-Path -Parent $PSScriptRoot
$galleryRoot=Join-Path (Join-Path $generatorRoot 'evidence') 'archetypes_v05'
$manifestRoot=Join-Path $galleryRoot 'manifests'
$sheetRoot=Join-Path $galleryRoot 'contact_sheets'
$regionOrder=@('LOWMARK','THORNFELL','MIRE','EMBERHOLT')
$typeSpecs=[ordered]@{
    FARMHOUSE='Farmhouse'; BARN='Barn'; GRAIN_STORE='Grain Store'; MILLER='Miller House';
    INN='Inn'; COTTAGE='Cottage'; TOWNHOUSE='Townhouse'; MERCHANT_HOUSE='Merchant House';
    LONGHOUSE='Longhouse'; SHOP='Shop'; WAREHOUSE='Warehouse'; MARKET_HALL='Market Hall';
    STABLE='Stable'; SMITHY='Smithy'; WORKSHOP='Workshop'; ASSEMBLY_HALL='Assembly Hall';
    WATCHTOWER='Watchtower'; GATEHOUSE='Gatehouse'; BARRACKS='Barracks'; BOATHOUSE='Boathouse'
}
$rowOrder=@(
    @{Mode='clay';View=0;Label='CLAY | FRONT'},
    @{Mode='clay';View=1;Label='CLAY | REAR'},
    @{Mode='material';View=0;Label='MATERIAL | FRONT'},
    @{Mode='material';View=1;Label='MATERIAL | REAR'}
)
if($Functions -and $Functions.Count -gt 0){
    $selected=@($Functions | ForEach-Object {$_.ToUpperInvariant()})
    foreach($function in $selected){if(-not $typeSpecs.Contains($function)){throw "Unknown function '$function'. Supported: $($typeSpecs.Keys -join ', ')"}}
} else {$selected=@($typeSpecs.Keys)}
New-Item -ItemType Directory -Force -Path $sheetRoot | Out-Null

$tileW=1024; $tileH=704; $titleH=72; $regionHeaderH=48; $rowHeaderW=220
$fontHeader=[System.Drawing.Font]::new('Segoe UI',18,[System.Drawing.FontStyle]::Bold)
$fontRow=[System.Drawing.Font]::new('Segoe UI',15,[System.Drawing.FontStyle]::Bold)
$fontBody=[System.Drawing.Font]::new('Segoe UI',14,[System.Drawing.FontStyle]::Regular)
$sheetRecords=[System.Collections.Generic.List[object]]::new()
try {
    foreach($function in $selected){
        $manifestPath=Join-Path $manifestRoot ($function.ToLowerInvariant()+'.json')
        if(-not (Test-Path -LiteralPath $manifestPath)){Write-Warning "Skipping $function; manifest not found: $manifestPath"; continue}
        $manifest=Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
        $records=@($manifest.records)
        $byRegion=@{}
        foreach($region in $regionOrder){
            $matches=@($records | Where-Object {$_.region -eq $region -or $_.settings.region -eq $region})
            if($matches.Count -ne 1){throw "$function manifest must contain exactly one record for $region; found $($matches.Count)."}
            $byRegion[$region]=$matches[0]
        }
        $canvasW=$rowHeaderW+($tileW*$regionOrder.Count)
        $canvasH=$titleH+$regionHeaderH+(($tileH+36)*$rowOrder.Count)
        $bitmap=[System.Drawing.Bitmap]::new($canvasW,$canvasH)
        $graphics=[System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.Clear([System.Drawing.Color]::FromArgb(35,36,38))
        $graphics.TextRenderingHint=[System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
        $brush=[System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(236,232,220))
        $mutedBrush=[System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(185,182,172))
        $sourceIndividuals=[System.Collections.Generic.List[object]]::new()
        try {
            $profileShort='unknown'
            if($manifest.source_sha256 -and $manifest.source_sha256.'profiles.py'){$profileShort=([string]$manifest.source_sha256.'profiles.py').Substring(0,8)}
            $graphics.DrawString("$($typeSpecs[$function]) | $function",$fontHeader,$brush,12,6)
            $revisionShort=([string]$manifest.source_revision).Substring(0,8)
            $subtitle="Settings: seed 91 | ESTABLISHED | STANDARD | age 35 | upkeep 0.7 | MEDIUM / EFFICIENT | world + grammar ON | context AUTO | common scale across regions, independently fit across types | opposed front / rear views | source $revisionShort | profiles.py $profileShort"
            $graphics.DrawString($subtitle,$fontBody,$mutedBrush,12,40)
            for($col=0;$col -lt $regionOrder.Count;$col++){
                $x=$rowHeaderW+$col*$tileW
                $graphics.DrawString($regionOrder[$col],$fontHeader,$brush,$x+12,$titleH+4)
            }
            for($row=0;$row -lt $rowOrder.Count;$row++){
                $spec=$rowOrder[$row]
                $y=$titleH+$regionHeaderH+$row*($tileH+36)
                $graphics.DrawString($spec.Label,$fontRow,$brush,12,$y+10)
                for($col=0;$col -lt $regionOrder.Count;$col++){
                    $region=$regionOrder[$col]; $x=$rowHeaderW+$col*$tileW
                    $record=$byRegion[$region]
                    $view=@($record.views | Where-Object {$_.mode -eq $spec.Mode -and [int]$_.view -eq $spec.View}) | Select-Object -First 1
                    $reason=$null; $imagePath=$null; $actualHash=$null
                    if($record.status -ne 'rendered'){$reason="Record status: $($record.status)"}
                    elseif(-not $view){$reason='Expected view is missing'}
                    else {
                        $relative=[string]$view.image
                        $imagePath=Join-Path $galleryRoot ($relative -replace '/', [IO.Path]::DirectorySeparatorChar)
                        if(-not (Test-Path -LiteralPath $imagePath)){$reason='Image file is missing'}
                        else {
                            $actualHash=(Get-FileHash -LiteralPath $imagePath -Algorithm SHA256).Hash.ToLowerInvariant()
                            if($view.image_sha256 -and $actualHash -ne ([string]$view.image_sha256).ToLowerInvariant()){$reason='Image SHA-256 does not match manifest'}
                        }
                    }
                    if(-not $reason){
                        $img=[System.Drawing.Image]::FromFile($imagePath)
                        try {
                            if($img.Width -ne $tileW -or $img.Height -ne $tileH){$reason="Unexpected dimensions: $($img.Width)x$($img.Height)"}
                            else {$graphics.DrawImage($img,$x,$y+36,$tileW,$tileH)}
                        } finally {$img.Dispose()}
                    }
                    if($reason){
                        $graphics.FillRectangle([System.Drawing.Brushes]::DarkSlateGray,$x,$y+36,$tileW,$tileH)
                        $graphics.DrawRectangle([System.Drawing.Pens]::Tomato,$x+1,$y+37,$tileW-2,$tileH-2)
                        $graphics.DrawString('IMAGE NOT AVAILABLE',$fontRow,[System.Drawing.Brushes]::Tomato,$x+28,$y+76)
                        $graphics.DrawString($reason,$fontBody,$brush,[System.Drawing.RectangleF]::new($x+28,$y+112,$tileW-56,100))
                    }
                    $graphics.DrawRectangle([System.Drawing.Pens]::DimGray,$x,$y+36,$tileW-1,$tileH-1)
                    if($view){
                        $sourceIndividuals.Add([pscustomobject]@{
                            region=$region; mode=$spec.Mode; view=$spec.View; image=[string]$view.image
                            declared_sha256=[string]$view.image_sha256; actual_sha256=$actualHash
                            result=if($reason){'placeholder'}else{'included'}; reason=$reason
                        })
                    } else {
                        $sourceIndividuals.Add([pscustomobject]@{region=$region;mode=$spec.Mode;view=$spec.View;image=$null;declared_sha256=$null;actual_sha256=$null;result='placeholder';reason=$reason})
                    }
                }
            }
            $sheetPath=Join-Path $sheetRoot ($function.ToLowerInvariant()+'.png')
            $bitmap.Save($sheetPath,[System.Drawing.Imaging.ImageFormat]::Png)
        } finally {$brush.Dispose();$mutedBrush.Dispose();$graphics.Dispose();$bitmap.Dispose()}
        $sheetHash=(Get-FileHash -LiteralPath $sheetPath -Algorithm SHA256).Hash.ToLowerInvariant()
        $sheetRecords.Add([pscustomobject]@{
            function=$function; label=$typeSpecs[$function]; source_revision=$manifest.source_revision
            source_sha256=$manifest.source_sha256; settings_contract=$manifest.settings_contract
            contact_sheet="contact_sheets/$($function.ToLowerInvariant()).png"; contact_sheet_sha256=$sheetHash
            contact_sheet_width=$canvasW; contact_sheet_height=$canvasH
            source_individuals=@($sourceIndividuals)
        })
        Write-Output "Composed $function ($sheetHash)"
    }
} finally {$fontHeader.Dispose();$fontRow.Dispose();$fontBody.Dispose()}
$sheetManifest=[pscustomobject]@{schema='caelmor.archetype-gallery.v1';regions=$regionOrder;rows=@($rowOrder | ForEach-Object {$_.Label});sheets=@($sheetRecords)}
$sheetManifest | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $sheetRoot 'manifest.json') -Encoding utf8
Write-Output "Gallery manifest written for $($sheetRecords.Count) archetypes."
