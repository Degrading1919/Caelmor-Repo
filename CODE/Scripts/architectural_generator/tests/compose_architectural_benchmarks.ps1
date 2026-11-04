param(
    [string]$BeforeStage='before',
    [string]$AfterStage='after',
    [string[]]$Cases=@('SMITHY','GATEHOUSE')
)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $PSScriptRoot
$evidence=Join-Path $root 'evidence\benchmarks_v08'
$out=Join-Path $evidence 'comparison'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$tiles=@('normal','distant','close')
$finishes=@('clay','material')
$tileW=1024;$tileH=704;$labelW=180;$titleH=42;$colHeaderH=40
$fontTitle=[System.Drawing.Font]::new('Segoe UI',18,[System.Drawing.FontStyle]::Bold)
$fontHeader=[System.Drawing.Font]::new('Segoe UI',14,[System.Drawing.FontStyle]::Bold)
$fontRow=[System.Drawing.Font]::new('Segoe UI',14,[System.Drawing.FontStyle]::Bold)
$brush=[System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(238,235,225))
$records=[System.Collections.Generic.List[object]]::new()
$functionViews=@{
    SMITHY=@('front','rear'); GATEHOUSE=@('front','rear')
}
try {
    foreach($functionInput in $Cases){
        $function=$functionInput.ToUpperInvariant()
        if(-not $functionViews.ContainsKey($function)){throw "Unsupported benchmark case: $function"}
        foreach($distance in $tiles){
            $canvasW=$labelW+4*$tileW;$canvasH=$titleH+$colHeaderH+2*$tileH
            $bitmap=[System.Drawing.Bitmap]::new($canvasW,$canvasH)
            $g=[System.Drawing.Graphics]::FromImage($bitmap)
            $g.Clear([System.Drawing.Color]::FromArgb(35,36,38))
            $inputs=[System.Collections.Generic.List[object]]::new()
            try {
                $g.DrawString("$function | $distance | fixed-camera comparison",$fontTitle,$brush,12,8)
                $frontLabel='FRONT';$otherLabel=$functionViews[$function][1].ToUpperInvariant()
                if($function -eq 'SMITHY' -and $distance -eq 'close'){$frontLabel='WORKFRONT A';$otherLabel='WORKFRONT B'}
                $columns=@(
                    @{Stage=$BeforeStage;View=0;Label="$($BeforeStage.ToUpperInvariant()) $frontLabel"},
                    @{Stage=$AfterStage;View=0;Label="$($AfterStage.ToUpperInvariant()) $frontLabel"},
                    @{Stage=$BeforeStage;View=1;Label="$($BeforeStage.ToUpperInvariant()) $otherLabel"},
                    @{Stage=$AfterStage;View=1;Label="$($AfterStage.ToUpperInvariant()) $otherLabel"}
                )
                for($c=0;$c -lt $columns.Count;$c++){
                    $x=$labelW+$c*$tileW
                    $g.DrawString($columns[$c].Label,$fontHeader,$brush,$x+10,$titleH+8)
                }
                for($r=0;$r -lt $finishes.Count;$r++){
                    $finish=$finishes[$r];$y=$titleH+$colHeaderH+$r*$tileH
                    $g.DrawString($finish.ToUpperInvariant(),$fontRow,$brush,12,$y+12)
                    for($c=0;$c -lt $columns.Count;$c++){
                        $column=$columns[$c];$stage=$column.Stage
                        $casePath=Join-Path (Join-Path (Join-Path $evidence $stage) 'cases') ($function.ToLowerInvariant()+'.json')
                        if(-not (Test-Path -LiteralPath $casePath)){throw "Missing case manifest: $casePath"}
                        $caseManifest=Get-Content -LiteralPath $casePath -Raw | ConvertFrom-Json
                        $distanceRow=@($caseManifest.images | Where-Object {$_.distance -eq $distance -and $_.finish -eq $finish -and [int]$_.view -eq [int]$column.View}) | Select-Object -First 1
                        if(-not $distanceRow){throw "Missing $stage/$function/$distance/$finish/view$($column.View) record"}
                        $imagePath=Join-Path (Join-Path $evidence $stage) ($distanceRow.image -replace '/', [IO.Path]::DirectorySeparatorChar)
                        if(-not (Test-Path -LiteralPath $imagePath)){throw "Missing benchmark image: $imagePath"}
                        $actual=(Get-FileHash -LiteralPath $imagePath -Algorithm SHA256).Hash.ToLowerInvariant()
                        if($actual -ne ([string]$distanceRow.image_sha256).ToLowerInvariant()){throw "Image hash mismatch: $imagePath"}
                        $img=[System.Drawing.Image]::FromFile($imagePath)
                        try {
                            if($img.Width -ne $tileW -or $img.Height -ne $tileH){throw "Unexpected image dimensions: $imagePath $($img.Width)x$($img.Height)"}
                            $g.DrawImage($img,$labelW+$c*$tileW,$y,$tileW,$tileH)
                        } finally {$img.Dispose()}
                        $inputs.Add([pscustomobject]@{stage=$stage;finish=$finish;view=[int]$column.View;image=$distanceRow.image;image_sha256=$actual;source_revision=$caseManifest.source_revision;geometry_hash=$caseManifest.geometry_hash})
                    }
                }
                $sheet=Join-Path $out ("{0}_{1}.png" -f $function.ToLowerInvariant(),$distance)
                $bitmap.Save($sheet,[System.Drawing.Imaging.ImageFormat]::Png)
            } finally {$g.Dispose();$bitmap.Dispose()}
            $records.Add([pscustomobject]@{function=$function;distance=$distance;image="comparison/$([IO.Path]::GetFileName($sheet))";image_sha256=(Get-FileHash -LiteralPath $sheet -Algorithm SHA256).Hash.ToLowerInvariant();width=$canvasW;height=$canvasH;inputs=@($inputs)})
            Write-Output "Composed $function $distance"
        }
    }
} finally {$fontTitle.Dispose();$fontHeader.Dispose();$fontRow.Dispose();$brush.Dispose()}
$manifest=[pscustomobject]@{schema='caelmor.architectural-benchmarks.v1';before_stage=$BeforeStage;after_stage=$AfterStage;sheets=@($records)}
$manifest | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $out 'manifest.json') -Encoding utf8
Write-Output "Benchmark comparisons composed: $($records.Count)."
