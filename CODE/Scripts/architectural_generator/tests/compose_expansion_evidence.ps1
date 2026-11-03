$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$base = (Get-Location).Path
$evidence = Join-Path $base 'evidence'
$frames = Join-Path $evidence '_expansion_frames'
$font = New-Object System.Drawing.Font('Arial', 18, [System.Drawing.FontStyle]::Bold)
$labelFont = New-Object System.Drawing.Font('Arial', 12, [System.Drawing.FontStyle]::Bold)
$textBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(245,242,232))
$background = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(28,31,34))

function Add-Labels([string]$source, [string]$target, [array]$labels) {
    $bitmap = [System.Drawing.Bitmap]::FromFile((Join-Path $evidence $source))
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    foreach ($label in $labels) {
        $size = $graphics.MeasureString($label.Text, $font)
        $rect = [System.Drawing.RectangleF]::new([single]$label.X,[single]$label.Y,[single]($size.Width+20),[single]($size.Height+12))
        $graphics.FillRectangle($background,$rect)
        $graphics.DrawString($label.Text,$font,$textBrush,$label.X+10,$label.Y+5)
    }
    $bitmap.Save((Join-Path $evidence $target),[System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()
}

Add-Labels 'four_regions_comparison.png' 'four_regions_comparison_labeled.png' @(
    @{X=38;Y=36;Text='MIRE · upper left'}, @{X=1120;Y=36;Text='EMBERHOLT · upper right'},
    @{X=38;Y=620;Text='LOWMARK · lower left'}, @{X=1090;Y=620;Text='THORNFELL · lower right'})
Add-Labels 'lowmark_wealth_comparison.png' 'lowmark_wealth_comparison_labeled.png' @(
    @{X=130;Y=35;Text='MODEST'}, @{X=670;Y=35;Text='ESTABLISHED'}, @{X=1270;Y=35;Text='AFFLUENT'})
Add-Labels 'lowmark_maintenance_comparison.png' 'lowmark_maintenance_comparison_labeled.png' @(
    @{X=260;Y=35;Text='MAINTAINED'}, @{X=1040;Y=35;Text='NEGLECTED'})

$manifest = Get-Content (Join-Path $evidence 'expansion_evidence_manifest.json') -Raw | ConvertFrom-Json
$rows = $manifest.rows
$gridCols=4; $cardW=330; $cardH=295; $labelH=36
$sheetWidth=[int]($gridCols*$cardW)
$sheetHeight=[int]([Math]::Ceiling($rows.Count/[double]$gridCols)*$cardH)
$sheet=[System.Drawing.Bitmap]::new($sheetWidth,$sheetHeight)
$graphics=[System.Drawing.Graphics]::FromImage($sheet)
$graphics.Clear([System.Drawing.Color]::FromArgb(35,39,43))
for ($i=0; $i -lt $rows.Count; $i++) {
    $x=($i % $gridCols)*$cardW; $y=[Math]::Floor($i/$gridCols)*$cardH
    $graphics.DrawString($rows[$i].label,$labelFont,$textBrush,$x+8,$y+5)
    $image=[System.Drawing.Bitmap]::FromFile((Join-Path $frames ('item_{0:D2}.png' -f $i)))
    $availableW=$cardW-12; $availableH=$cardH-$labelH-8
    $scale=[Math]::Min($availableW/$image.Width,$availableH/$image.Height)
    $width=[int]($image.Width*$scale); $height=[int]($image.Height*$scale)
    $graphics.DrawImage($image,$x+[int](($cardW-$width)/2),$y+$labelH,$width,$height)
    $image.Dispose()
}
$sheet.Save((Join-Path $evidence 'expanded_type_gallery.png'),[System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose(); $sheet.Dispose(); $font.Dispose(); $labelFont.Dispose(); $textBrush.Dispose(); $background.Dispose()
Get-ChildItem $evidence -File | Where-Object {$_.Name -like '*expansion*' -or $_.Name -like '*comparison_labeled*' -or $_.Name -like 'solid_efficient*'} | Select-Object Name,Length
