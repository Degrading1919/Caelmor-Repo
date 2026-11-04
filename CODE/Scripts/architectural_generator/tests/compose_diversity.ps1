$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$root = Join-Path (Split-Path -Parent $PSScriptRoot) 'evidence/diversity_v12'
$before = Get-Content (Join-Path $root 'before/manifest.json') -Raw | ConvertFrom-Json
$after = Get-Content (Join-Path $root 'after/manifest.json') -Raw | ConvertFrom-Json
$font = [Drawing.Font]::new('Segoe UI', 14, [Drawing.FontStyle]::Bold)
$brush = [Drawing.SolidBrush]::new([Drawing.Color]::WhiteSmoke)
$sheets = @()
try {
    foreach ($function in 'SMITHY','GATEHOUSE') {
        $oldCases = @($before.cases | Where-Object {$_.settings.function -eq $function})
        $newCases = @($after.cases | Where-Object {$_.settings.function -eq $function})
        if ($oldCases.Count -ne 5 -or $newCases.Count -ne 5) { throw 'Expected five seeds per stage' }
        $width=3200; $height=1904; $tileWidth=640; $tileHeight=440
        $bitmap = [Drawing.Bitmap]::new($width,$height)
        $graphics = [Drawing.Graphics]::FromImage($bitmap)
        $frames=@()
        try {
            $graphics.Clear([Drawing.Color]::FromArgb(29,31,34))
            $graphics.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $graphics.DrawString("$function | matched gameplay views", $font, $brush, 12, 10)
            for ($col=0; $col -lt 5; $col++) {
                $oldCase=$oldCases[$col]; $newCase=$newCases[$col]
                $seed=$oldCase.settings.seed
                if ($seed -ne $newCase.settings.seed) { throw 'Mismatched seeds' }
                foreach ($key in $oldCase.settings.PSObject.Properties.Name) {
                    if ($key -ne 'seed_massing' -and $oldCase.settings.$key -ne $newCase.settings.$key) {
                        throw "Mismatched settings for $function seed $seed ($key)"
                    }
                }
                $row=0
                foreach ($finish in 'clay','material') {
                    $old = @($oldCase.images | Where-Object {$_.finish -eq $finish -and $_.view -eq 0})
                    $new = @($newCase.images | Where-Object {$_.finish -eq $finish -and $_.view -eq 0})
                    if ($old.Count -ne 1 -or $new.Count -ne 1) { throw 'Expected one matching front frame' }
                    foreach ($key in 'camera_location','camera_target','ortho_scale') {
                        if (($old[0].$key -join ',') -ne ($new[0].$key -join ',')) { throw 'Camera changed' }
                    }
                    foreach ($stage in 'before','after') {
                        $record = if ($stage -eq 'before') {$old[0]} else {$new[0]}
                        $relative = "$stage/$($record.image)"
                        $path = Join-Path $root $relative
                        $hash = (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()
                        if ($hash -ne $record.sha256) { throw "Changed input $relative" }
                        $x = $col*$tileWidth; $y = 40+$row*466
                        $graphics.DrawString("Seed $seed | $stage | $finish", $font, $brush, ($x+9), ($y+1))
                        $image = [Drawing.Image]::FromFile($path)
                        try { $graphics.DrawImage($image,$x,($y+25),$tileWidth,$tileHeight) }
                        finally { $image.Dispose() }
                        $frames+=@{image=$relative;sha256=$hash}
                        $row++
                    }
                }
            }
            $name = "$($function.ToLowerInvariant()).png"
            $path = Join-Path $root $name
            $bitmap.Save($path,[Drawing.Imaging.ImageFormat]::Png)
            $sheets+=@{image=$name;width=$width;height=$height;inputs=$frames
                       sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
        } finally {$graphics.Dispose(); $bitmap.Dispose()}
    }
} finally {$font.Dispose(); $brush.Dispose()}
@{before=$before.revision;after=$after.revision;sheets=$sheets} |
    ConvertTo-Json -Depth 6 | Set-Content (Join-Path $root 'sheets.json') -Encoding utf8
