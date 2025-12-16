# =====================================================================
# Caelmor_File_Manifest_Autogen.ps1
# ALWAYS starts at the Caelmor project root and scans recursively.
# Includes all directories—even empty ones.
# =====================================================================

# --- 1. Explicitly define the Caelmor project root ---
# Modify this path ONLY if you move your Caelmor folder.
$ProjectRoot = "C:\Users\CK\Documents\Caelmor"

# --- 2. Get directory where the script is located (for saving output) ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# --- 3. Determine next manifest version ---
$BaseName = "Caelmor_File_Manifest_v"
$Existing = Get-ChildItem -Path $ScriptDir -Filter "$BaseName*.txt" -ErrorAction SilentlyContinue

if ($Existing.Count -eq 0) {
    $NextVersion = 1
} else {
    $Versions = foreach ($f in $Existing) {
        if ($f.Name -match "${BaseName}(\d+)\.txt") { [int]$Matches[1] }
    }
    $NextVersion = ($Versions | Measure-Object -Maximum).Maximum + 1
}

$OutputFile = Join-Path $ScriptDir ("{0}{1}.txt" -f $BaseName, $NextVersion)

# --- 4. Helper for formatting section headers ---
function Write-Header($title) {
    return "`n============================================================`n$title`n============================================================`n"
}

# --- 5. Collect ALL directories including empty ---
$Directories = Get-ChildItem -Path $ProjectRoot -Directory -Recurse -ErrorAction SilentlyContinue

# --- 6. Collect all files ---
$Files = Get-ChildItem -Path $ProjectRoot -Recurse -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer }

# --- 7. Begin manifest ---
$Manifest = @()
$Manifest += "CAELMOR_FILE_MANIFEST_v$NextVersion"
$Manifest += "Generated automatically from full Caelmor project root."
$Manifest += "Project root: $ProjectRoot"
$Manifest += "Update timestamp: $(Get-Date)"
$Manifest += Write-Header "DIRECTORY STRUCTURE (Including Empty Folders)"

# --- 8. Output directory + file structure ---
foreach ($dir in $Directories) {
    # Convert to relative path
    $Relative = $dir.FullName.Replace($ProjectRoot, "").TrimStart("\")
    $Manifest += "$Relative/"

    # Files directly under this directory
    $ChildFiles = Get-ChildItem -Path $dir.FullName -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer }
    foreach ($file in $ChildFiles) {
        $Manifest += "    - $($file.Name)"
    }
}

# --- 9. Write manifest file ---
$Manifest -join "`n" | Set-Content -Path $OutputFile -Encoding UTF8

Write-Host "Manifest created successfully:"
Write-Host " → $OutputFile" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..."
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null
