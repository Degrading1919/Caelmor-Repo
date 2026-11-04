param([string]$Stage='final')
# Reuses the established System.Drawing contact-sheet technique and v08 PNGs.
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $PSScriptRoot
$evidence=Join-Path $root 'evidence/materials_v09'
$capture=Join-Path $evidence $Stage
$manifest=Get-Content (Join-Path $capture 'manifest.json') -Raw | ConvertFrom-Json
$out=Join-Path $evidence 'comparison'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$tileW=1024;$tileH=704;$labelW=200;$titleH=46;$headH=34
$font=[Drawing.Font]::new('Segoe UI',14,[Drawing.FontStyle]::Bold)
$title=[Drawing.Font]::new('Segoe UI',18,[Drawing.FontStyle]::Bold)
$brush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(238,235,225))
$sheets=[Collections.Generic.List[object]]::new()
function Draw-Source($g,$path,$hash,$x,$y,$inputs){
    $actual=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if($actual -ne $hash){throw "Image hash mismatch: $path"}
    $im=[Drawing.Image]::FromFile($path)
    try {
        if($im.Width -ne $tileW -or $im.Height -ne $tileH){throw "Wrong image dimensions: $path"}
        $g.DrawImage($im,$x,$y,$tileW,$tileH)
    } finally {$im.Dispose()}
    $inputs.Add([pscustomobject]@{path=[IO.Path]::GetRelativePath($evidence,$path).Replace('\','/');sha256=$actual})
}
function New-Sheet($function,$kind,$rows){
    $width=$labelW+2*$tileW;$height=$titleH+$rows.Count*($headH+$tileH)
    $bitmap=[Drawing.Bitmap]::new($width,$height);$g=[Drawing.Graphics]::FromImage($bitmap)
    $inputs=[Collections.Generic.List[object]]::new()
    try {
        $g.Clear([Drawing.Color]::FromArgb(35,36,38))
        $g.DrawString("$function | $kind | identical geometry, camera and lighting",$title,$brush,10,8)
        $r=0
        foreach($row in $rows){
            $y=$titleH+$r*($headH+$tileH)
            $g.DrawString($row.label,$font,$brush,10,$y+40)
            for($c=0;$c -lt 2;$c++){
                $g.DrawString($row.titles[$c],$font,$brush,($labelW+$c*$tileW+10),($y+6))
                Draw-Source $g $row.paths[$c] $row.hashes[$c] ($labelW+$c*$tileW) ($y+$headH) $inputs
            }
            $r++
        }
        $file="$($function.ToLowerInvariant())_$kind.png";$path=Join-Path $out $file
        $bitmap.Save($path,[Drawing.Imaging.ImageFormat]::Png)
        $sheets.Add([pscustomobject]@{function=$function;kind=$kind;image="comparison/$file";width=$width;height=$height;
            sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant();inputs=@($inputs)})
    } finally {$g.Dispose();$bitmap.Dispose()}
}
try {
    foreach($function in @('SMITHY','GATEHOUSE')){
        $oldRoot=Join-Path $root 'evidence/benchmarks_v08/after'
        $old=Get-Content (Join-Path $oldRoot "cases/$($function.ToLowerInvariant()).json") -Raw | ConvertFrom-Json
        $rows=@()
        foreach($distance in @('normal','close')){
            $before=@($old.images | Where-Object {$_.distance -eq $distance -and $_.finish -eq 'material' -and $_.view -eq 0})[0]
            $after=@($manifest.images | Where-Object {$_.function -eq $function -and $_.variant -eq 'reference' -and $_.distance -eq $distance})[0]
            if(-not $before -or -not $after){throw "Missing controlled before/after $function $distance"}
            if($before.ortho_scale -ne $after.ortho_scale){throw 'Camera scale changed'}
            $rows+=@{label=$distance.ToUpperInvariant();titles=@('BEFORE v0.8 / age35 upkeep0.7','AFTER v0.9 / age35 upkeep0.7');
                paths=@((Join-Path $oldRoot $before.image),(Join-Path $capture $after.image));
                hashes=@($before.image_sha256,$after.image_sha256)}
        }
        New-Sheet $function 'before_after' $rows
        foreach($distance in @('normal','close')){
            $rows=@()
            foreach($pair in @(
                @{label='AGE';a='young';b='old';titles=@('5 years / upkeep0.7','120 years / upkeep0.7')},
                @{label='MAINTENANCE';a='neglected';b='maintained';titles=@('120 years / upkeep0.15','120 years / upkeep0.95')},
                @{label='INVESTMENT';a='modest';b='affluent';titles=@('Modest / age35 upkeep0.7','Affluent / age35 upkeep0.7')},
                @{label='CRAFTSMANSHIP';a='rough';b='fine';titles=@('Rough / age35 upkeep0.7','Fine / age35 upkeep0.7')},
                @{label="RESOURCES vs`nCARE";a='modest_maintained';b='affluent_neglected';titles=@('Modest / 120yrs / upkeep0.95','Affluent / 120yrs / upkeep0.15')}
            )){
                $a=@($manifest.images | Where-Object {$_.function -eq $function -and $_.variant -eq $pair.a -and $_.distance -eq $distance})[0]
                $b=@($manifest.images | Where-Object {$_.function -eq $function -and $_.variant -eq $pair.b -and $_.distance -eq $distance})[0]
                if(-not $a -or -not $b){throw "Missing condition pair: $function $($pair.label)"}
                $rows+=@{label=$pair.label;titles=$pair.titles;paths=@((Join-Path $capture $a.image),(Join-Path $capture $b.image));hashes=@($a.image_sha256,$b.image_sha256)}
            }
            New-Sheet $function "conditions_$distance" $rows
        }
    }
} finally {$font.Dispose();$title.Dispose();$brush.Dispose()}
[pscustomobject]@{capture_stage=$Stage;source_revision=$manifest.source_revision;sheets=@($sheets)} |
    ConvertTo-Json -Depth 12 | Set-Content (Join-Path $out 'manifest.json') -Encoding utf8
Write-Output "MATERIAL_COMPARISON_SHEETS $($sheets.Count)"
