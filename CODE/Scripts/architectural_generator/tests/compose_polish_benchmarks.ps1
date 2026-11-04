$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Join-Path (Split-Path -Parent $PSScriptRoot) 'evidence/polish_v10'
$out=Join-Path $root 'comparison'
New-Item -ItemType Directory -Force $out | Out-Null
$before=Get-Content (Join-Path $root 'before/manifest.json') -Raw | ConvertFrom-Json
$after=Get-Content (Join-Path $root 'after/manifest.json') -Raw | ConvertFrom-Json
$pilot=Get-Content (Join-Path $root 'pilot/manifest.json') -Raw | ConvertFrom-Json
$font=[Drawing.Font]::new('Segoe UI',16,[Drawing.FontStyle]::Bold)
$brush=[Drawing.SolidBrush]::new([Drawing.Color]::WhiteSmoke)
$sheets=[Collections.Generic.List[object]]::new()
function New-Sheet($name,$title,$rows,$columns){
    $w=1024*$columns
    $h=46+738*$rows.Count
    $bitmap=[Drawing.Bitmap]::new($w,$h)
    $g=[Drawing.Graphics]::FromImage($bitmap)
    $inputs=[Collections.Generic.List[object]]::new()
    try {
        $g.Clear([Drawing.Color]::FromArgb(31,33,36))
        $g.DrawString($title,$font,$brush,12,9)
        for($r=0;$r -lt $rows.Count;$r++){
            for($c=0;$c -lt $rows[$r].Count;$c++){
                $tile=$rows[$r][$c]
                $path=Join-Path $root "$($tile.stage)/$($tile.row.image)"
                $hash=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()
                if($hash -ne $tile.row.sha256){throw "Changed capture $path"}
                $x=$c*1024
                $y=46+$r*738
                $g.DrawString($tile.label,$font,$brush,($x+9),($y+4))
                $image=[Drawing.Image]::FromFile($path)
                try {
                    if($image.Width -ne 1024 -or $image.Height -ne 704){throw "Unexpected dimensions $path"}
                    $g.DrawImage($image,$x,($y+34),1024,704)
                } finally {$image.Dispose()}
                $inputs.Add(@{image="$($tile.stage)/$($tile.row.image)";sha256=$hash;label=$tile.label})
            }
        }
        $path=Join-Path $out "$name.png"
        $bitmap.Save($path,[Drawing.Imaging.ImageFormat]::Png)
        $sheets.Add(@{image="comparison/$name.png";width=$w;height=$h;inputs=@($inputs)
            sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()})
    } finally {$g.Dispose();$bitmap.Dispose()}
}
function Find-Frame($manifest,$function,$distance,$finish,$view){
    $found=@($manifest.images | Where-Object {$_.function -eq $function -and $_.distance -eq $distance -and $_.finish -eq $finish -and $_.view -eq $view})
    if($found.Count -ne 1){throw "Expected one frame for $function $distance $finish view $view"}
    return $found[0]
}
try {
    $experiment=@()
    foreach($function in @('SMITHY','GATEHOUSE')){
        $base=Find-Frame $before $function normal material 0
        $variants=@($pilot.images | Where-Object {$_.function -eq $function -and $_.finish -eq 'material'})
        $experiment+=,@(@{stage='before';row=$base;label="$function / v0.9 control"},
            @{stage='pilot';row=($variants | Where-Object variant -eq 'material_only');label='New material / same geometry'},
            @{stage='pilot';row=($variants | Where-Object variant -eq 'crafted');label='New material / first edge pass'})
        foreach($distance in @('distant','normal','close')){
            $rows=@()
            foreach($finish in @('clay','material')){
                $row=@()
                foreach($view in 0,1){
                    $angle=if($distance -eq 'close'){"detail $($view+1)"}elseif($view -eq 0){'front'}else{'rear'}
                    $row+=@{stage='before';row=(Find-Frame $before $function $distance $finish $view);label="v0.9 $finish / $angle"}
                    $row+=@{stage='after';row=(Find-Frame $after $function $distance $finish $view);label="v0.10 $finish / $angle"}
                }
                $rows+=,$row
            }
            $rows+=,@(
                @{stage='after';row=(Find-Frame $after $function $distance exported_material 0);label='GLB reimport / view 1'},
                @{stage='after';row=(Find-Frame $after $function $distance exported_material 1);label='GLB reimport / view 2'})
            New-Sheet "$($function.ToLowerInvariant())_$distance" "$function / $distance / matched studio and camera" $rows 4
        }
    }
    New-Sheet 'experiment_normal' 'Controlled normal-distance experiment' $experiment 3
} finally {$font.Dispose();$brush.Dispose()}
@{sheets=@($sheets);before=$before.source_revision;after=$after.source_revision} |
    ConvertTo-Json -Depth 10 | Set-Content (Join-Path $out 'manifest.json') -Encoding utf8
Write-Output "POLISH_SHEETS $($sheets.Count)"
