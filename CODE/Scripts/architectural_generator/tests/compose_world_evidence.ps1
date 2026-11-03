param(
    [string]$Stem = "first_four_clay",
    [string]$Root = (Split-Path -Parent $PSScriptRoot),
    [switch]$Matrix,
    [switch]$Wealth,
    [switch]$High
)
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing
$evidence = Join-Path $Root "evidence"
$frames = Join-Path $evidence "_world_frames"
$manifestName = if ($Matrix) { "world_matrix_render_manifest.json" }
    elseif ($Wealth) { "world_wealth_cottages_render_manifest.json" }
    elseif ($High) { "world_high_profiles_render_manifest.json" }
    else { "world_{0}_manifest.json" -f $Stem }
$manifestPath = Join-Path $evidence $manifestName
$records = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ($records.Count -ne $(if ($Matrix -or $High) { 16 } elseif ($Wealth) { 12 } else { 4 })) { throw "Unexpected evidence frame count: $($records.Count)." }
$first = [System.Drawing.Image]::FromFile((Join-Path $frames $records[0].image))
$tileWidth = $first.Width
$tileHeight = $first.Height
$first.Dispose()
$columns = if ($Matrix -or $Wealth -or $High) { 4 } else { 2 }
$rows = [Math]::Ceiling($records.Count / $columns)
$header = 54
$canvas = [System.Drawing.Bitmap]::new($tileWidth * $columns, ($tileHeight + $header) * $rows)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
$graphics.Clear([System.Drawing.Color]::FromArgb(27, 28, 30))
$font = [System.Drawing.Font]::new("Segoe UI", 18, [System.Drawing.FontStyle]::Bold)
$brush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::White)
try {
    for ($i = 0; $i -lt $records.Count; $i++) {
        $row = $records[$i]
        $image = [System.Drawing.Image]::FromFile((Join-Path $frames $row.image))
        $x = ($i % $columns) * $tileWidth
        $y = [Math]::Floor($i / $columns) * ($tileHeight + $header)
        $blind = [string]$row.blind_id
        if ($Matrix -or $Wealth) { $caption = "$($row.settings.region)  |  $($row.settings.function)  |  $($row.settings.wealth)" }
        elseif ($High) { $caption = "$($row.settings.region)  |  $($row.settings.wealth)  |  $($row.settings.geometry_mode)" }
        else { $caption = $blind }
        $graphics.DrawString($caption, $font, $brush, $x + 12, $y + 10)
        $graphics.DrawImage($image, $x, $y + $header, $tileWidth, $tileHeight)
        $image.Dispose()
    }
    if ($Matrix -or $Wealth -or $High) {
        if ($Matrix) { $labelledPath = Join-Path $evidence "world_matrix_clay_labelled.png" }
        elseif ($Wealth) { $labelledPath = Join-Path $evidence "world_wealth_cottages_clay_labelled.png" }
        else { $labelledPath = Join-Path $evidence "world_high_profiles_clay_labelled.png" }
        $canvas.Save($labelledPath, [System.Drawing.Imaging.ImageFormat]::Png)
        Write-Output $labelledPath
        return
    }
    $blindPath = Join-Path $evidence ("world_{0}_blind.png" -f $Stem)
    $labelledPath = Join-Path $evidence ("world_{0}_labelled.png" -f $Stem)
    $canvas.Save($blindPath, [System.Drawing.Imaging.ImageFormat]::Png)
    # A separate blinded-ID-to-region key is kept beside the render manifest.
    $key = @{}
    foreach ($row in $records) { $key[[string]$row.blind_id] = $row.settings }
    $key | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $evidence ("world_{0}_blind_key.json" -f $Stem)) -Encoding UTF8

    # Re-compose with the identifiers omitted from the visible header; the
    # backing manifest remains the separate answer key for reviewers.
    $graphics.Clear([System.Drawing.Color]::FromArgb(27, 28, 30))
    for ($i = 0; $i -lt $records.Count; $i++) {
        $row = $records[$i]
        $image = [System.Drawing.Image]::FromFile((Join-Path $frames $row.image))
        $x = ($i % $columns) * $tileWidth
        $y = [Math]::Floor($i / $columns) * ($tileHeight + $header)
        $graphics.DrawString("$($row.settings.region)  |  $($row.settings.function)", $font, $brush, $x + 12, $y + 10)
        $graphics.DrawImage($image, $x, $y + $header, $tileWidth, $tileHeight)
        $image.Dispose()
    }
    $canvas.Save($labelledPath, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Output $blindPath
    Write-Output $labelledPath
}
finally {
    $brush.Dispose()
    $font.Dispose()
    $graphics.Dispose()
    $canvas.Dispose()
}
