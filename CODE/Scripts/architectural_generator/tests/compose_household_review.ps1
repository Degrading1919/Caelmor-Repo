param([string]$Stage='study1',[string]$Function='COTTAGE',[string]$Mode='clay')
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $PSScriptRoot
$out=Join-Path $root 'evidence'
$stem="v05_${Stage}_$($Function.ToLower())_${Mode}"
$manifest=Get-Content -LiteralPath (Join-Path $out "${stem}_manifest.json") -Raw | ConvertFrom-Json
$regions=@($manifest.records | ForEach-Object {$_.settings.region} | Select-Object -Unique)
foreach($region in $regions){
    $regionRows=@($manifest.records | Where-Object {$_.settings.region -eq $region})
    $tiers=@(@('MODEST','ESTABLISHED','AFFLUENT') | Where-Object {$regionRows.slot -contains $_})
    $views=@($regionRows | ForEach-Object {$_.view} | Select-Object -Unique)
    $canvas=[System.Drawing.Bitmap]::new(640*$tiers.Count,472*$views.Count)
    $g=[System.Drawing.Graphics]::FromImage($canvas)
    $g.Clear([System.Drawing.Color]::FromArgb(27,28,30))
    $font=[System.Drawing.Font]::new('Segoe UI',14,[System.Drawing.FontStyle]::Bold)
    try {
        foreach($record in @($manifest.records | Where-Object {$_.settings.region -eq $region})){
            $column=$tiers.IndexOf($record.slot)
            $x=$column*640; $y=[int]$record.view*472
            $label="$region | $($record.slot) | $Function | view $($record.view+1)"
            if($manifest.study -eq 'condition'){
                $label="$region | age $($record.settings.age) | upkeep $($record.settings.maintenance) | view $($record.view+1)"
            }
            if($manifest.study -eq 'craft'){
                $label="$region | $($record.settings.craftsmanship) | CRAFT | view $($record.view+1)"
            }
            $g.DrawString($label,$font,[System.Drawing.Brushes]::White,$x+8,$y+5)
            $image=[System.Drawing.Image]::FromFile((Join-Path (Join-Path $out '_household_frames') $record.image))
            try {$g.DrawImage($image,$x,$y+32,640,440)} finally {$image.Dispose()}
        }
        $canvas.Save((Join-Path $out "${stem}_$($region.ToLower()).png"),[System.Drawing.Imaging.ImageFormat]::Png)
    } finally {$font.Dispose();$g.Dispose();$canvas.Dispose()}
}
Write-Output "Composed $($regions.Count) matched household panels."
