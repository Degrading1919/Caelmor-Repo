param(
    [string]$Gallery='archetypes_v05',
    [string[]]$Functions,
    [switch]$Proof
)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing

if([string]::IsNullOrWhiteSpace($Gallery) -or $Gallery -in @('.', '..') -or $Gallery -match '[/\\]'){
    throw "Gallery must be a single folder name, not a path: '$Gallery'."
}
$generatorRoot=Split-Path -Parent $PSScriptRoot
$evidenceRoot=Join-Path $generatorRoot 'evidence'
$galleryRoot=Join-Path $evidenceRoot $Gallery
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
if($Proof){
    $proofSelection=@(
        @{Function='SMITHY';Region='LOWMARK'},
        @{Function='MARKET_HALL';Region='THORNFELL'},
        @{Function='STABLE';Region='MIRE'},
        @{Function='GATEHOUSE';Region='EMBERHOLT'}
    )
    if($Gallery -notin @('function_v06_pilot','function_v06_pilot_refined')){throw "-Proof supports -Gallery function_v06_pilot or function_v06_pilot_refined."}
} else {$proofSelection=@()}
New-Item -ItemType Directory -Force -Path $sheetRoot | Out-Null

$tileW=1024; $tileH=704; $titleH=72; $regionHeaderH=48; $rowHeaderW=220
$fontHeader=[System.Drawing.Font]::new('Segoe UI',18,[System.Drawing.FontStyle]::Bold)
$fontRow=[System.Drawing.Font]::new('Segoe UI',15,[System.Drawing.FontStyle]::Bold)
$fontBody=[System.Drawing.Font]::new('Segoe UI',14,[System.Drawing.FontStyle]::Regular)
$sheetRecords=[System.Collections.Generic.List[object]]::new()
try {
    $sheetSpecs=[System.Collections.Generic.List[object]]::new()
    if($Proof){
        $columns=[System.Collections.Generic.List[object]]::new()
        foreach($selection in $proofSelection){
            $manifestPath=Join-Path $manifestRoot ($selection.Function.ToLowerInvariant()+'.json')
            if(-not (Test-Path -LiteralPath $manifestPath)){throw "Proof manifest missing: $manifestPath"}
            $manifest=Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
            $records=@($manifest.records | Where-Object {$_.region -eq $selection.Region -or $_.settings.region -eq $selection.Region})
            if($records.Count -ne 1){throw "$($selection.Function) manifest must contain exactly one record for $($selection.Region); found $($records.Count)."}
            $columns.Add([pscustomobject]@{Function=$selection.Function;Region=$selection.Region;Manifest=$manifest;Record=$records[0]})
        }
        $sheetSpecs.Add([pscustomobject]@{Name='functional_proof';Title='FUNCTIONAL PROOF | FUNCTION / REGION';Columns=@($columns)})
    } else {
        foreach($function in $selected){
            $manifestPath=Join-Path $manifestRoot ($function.ToLowerInvariant()+'.json')
            if(-not (Test-Path -LiteralPath $manifestPath)){Write-Warning "Skipping $function; manifest not found: $manifestPath"; continue}
            $manifest=Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
            $records=@($manifest.records)
            $columns=[System.Collections.Generic.List[object]]::new()
            foreach($region in $regionOrder){
                $matches=@($records | Where-Object {$_.region -eq $region -or $_.settings.region -eq $region})
                if($matches.Count -ne 1){throw "$function manifest must contain exactly one record for $region; found $($matches.Count)."}
                $columns.Add([pscustomobject]@{Function=$function;Region=$region;Manifest=$manifest;Record=$matches[0]})
            }
            $sheetSpecs.Add([pscustomobject]@{Name=$function.ToLowerInvariant();Title="$($typeSpecs[$function]) | $function";Columns=@($columns)})
        }
    }

    foreach($sheetSpec in $sheetSpecs){
        $columns=@($sheetSpec.Columns)
        $canvasW=$rowHeaderW+($tileW*$columns.Count)
        $canvasH=$titleH+$regionHeaderH+(($tileH+36)*$rowOrder.Count)
        $bitmap=[System.Drawing.Bitmap]::new($canvasW,$canvasH)
        $graphics=[System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.Clear([System.Drawing.Color]::FromArgb(35,36,38))
        $graphics.TextRenderingHint=[System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
        $brush=[System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(236,232,220))
        $mutedBrush=[System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(185,182,172))
        $sourceIndividuals=[System.Collections.Generic.List[object]]::new()
        try {
            $sourceRevisions=@($columns | ForEach-Object {if($_.Record.source_revision){[string]$_.Record.source_revision}else{[string]$_.Manifest.source_revision}} | Select-Object -Unique) -join '; '
            $profileHashes=@($columns | ForEach-Object {if($_.Manifest.source_sha256 -and $_.Manifest.source_sha256.'profiles.py'){([string]$_.Manifest.source_sha256.'profiles.py').Substring(0,8)}} | Select-Object -Unique)
            $profileShort=if($profileHashes.Count){$profileHashes -join ','}else{'unknown'}
            $graphics.DrawString($sheetSpec.Title,$fontHeader,$brush,12,6)
            $subtitle="Settings: seed 91 | ESTABLISHED | STANDARD | age 35 | upkeep 0.7 | MEDIUM / EFFICIENT | world + grammar ON | context AUTO | opposed front / rear views | source $sourceRevisions | profiles.py $profileShort"
            $graphics.DrawString($subtitle,$fontBody,$mutedBrush,12,40)
            for($col=0;$col -lt $columns.Count;$col++){
                $x=$rowHeaderW+$col*$tileW
                $header=if($Proof){"$($columns[$col].Function) | $($columns[$col].Region)"}else{$columns[$col].Region}
                $graphics.DrawString($header,$fontHeader,$brush,$x+12,$titleH+4)
            }
            for($row=0;$row -lt $rowOrder.Count;$row++){
                $spec=$rowOrder[$row]
                $y=$titleH+$regionHeaderH+$row*($tileH+36)
                $graphics.DrawString($spec.Label,$fontRow,$brush,12,$y+10)
                for($col=0;$col -lt $columns.Count;$col++){
                    $column=$columns[$col]; $x=$rowHeaderW+$col*$tileW
                    $record=$column.Record
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
                            if(-not $view.image_sha256){$reason='Image SHA-256 is missing from manifest'}
                            elseif($actualHash -ne ([string]$view.image_sha256).ToLowerInvariant()){$reason='Image SHA-256 does not match manifest'}
                        }
                    }
                    if(-not $reason){
                        $img=[System.Drawing.Image]::FromFile($imagePath)
                        try {
                            if($img.Width -ne $tileW -or $img.Height -ne $tileH){$reason="Unexpected dimensions: $($img.Width)x$($img.Height)"}
                            elseif($view.width -ne $tileW -or $view.height -ne $tileH){$reason="Manifest dimensions are not ${tileW}x${tileH}"}
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
                            function=$column.Function; region=$column.Region; mode=$spec.Mode; view=$spec.View; image=[string]$view.image
                            declared_sha256=[string]$view.image_sha256; actual_sha256=$actualHash
                            result=if($reason){'placeholder'}else{'included'}; reason=$reason
                        })
                    } else {
                        $sourceIndividuals.Add([pscustomobject]@{function=$column.Function;region=$column.Region;mode=$spec.Mode;view=$spec.View;image=$null;declared_sha256=$null;actual_sha256=$null;result='placeholder';reason=$reason})
                    }
                }
            }
            $sheetPath=Join-Path $sheetRoot ($sheetSpec.Name+'.png')
            $bitmap.Save($sheetPath,[System.Drawing.Imaging.ImageFormat]::Png)
        } finally {$brush.Dispose();$mutedBrush.Dispose();$graphics.Dispose();$bitmap.Dispose()}
        $sheetHash=(Get-FileHash -LiteralPath $sheetPath -Algorithm SHA256).Hash.ToLowerInvariant()
        $sheetRecords.Add([pscustomobject]@{
            function=$sheetSpec.Name; label=$sheetSpec.Title; source_revision=$sourceRevisions
            contact_sheet="contact_sheets/$($sheetSpec.Name).png"; contact_sheet_sha256=$sheetHash
            contact_sheet_width=$canvasW; contact_sheet_height=$canvasH
            source_individuals=@($sourceIndividuals)
        })
        Write-Output "Composed $($sheetSpec.Name) ($sheetHash)"
    }
} finally {$fontHeader.Dispose();$fontRow.Dispose();$fontBody.Dispose()}
$sheetManifest=[pscustomobject]@{schema='caelmor.archetype-gallery.v1';gallery=$Gallery;regions=$regionOrder;rows=@($rowOrder | ForEach-Object {$_.Label});sheets=@($sheetRecords)}
$sheetManifest | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $sheetRoot 'manifest.json') -Encoding utf8
Write-Output "Gallery manifest written for $($sheetRecords.Count) sheets."
