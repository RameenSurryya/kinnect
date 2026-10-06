# Builds the assignment submission zip OUTSIDE the repo (C:\dev\submission), then checks that
# the zipped source code still builds. Run from the project root:
#   powershell -ExecutionPolicy Bypass -File tools\make_submission.ps1
#
# Zip layout:
#   23I-0806_RameenSurryya_Assignment01\
#     SourceCode\i230806\   full project (no build output, .gradle, .idea, .git, local.properties,
#                           design\check, design\photos, __pycache__)
#     LayoutAndKotlin\      layout\*.xml, the Kotlin sources (ui\auth, ui\home, ...) and
#                           androidTest\*.kt

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem

$repo    = (Resolve-Path "$PSScriptRoot\..").Path
$name    = '23I-0806_RameenSurryya_Assignment01'
$outDir  = 'C:\dev\submission'
$stage   = Join-Path $outDir $name
$zipPath = Join-Path $outDir "$name.zip"

# Start from an empty staging folder and no old zip
if (Test-Path $stage)   { Remove-Item $stage -Recurse -Force }
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
New-Item -ItemType Directory -Force $stage | Out-Null

# ---- 1. SourceCode\i230806 ------------------------------------------------------------------
# git lists tracked files plus new files that are not ignored, so build\, .gradle\,
# local.properties and __pycache__\ are left out by .gitignore. The rest is filtered here.
$src = Join-Path $stage 'SourceCode\i230806'
Push-Location $repo
$files = git ls-files --cached --others --exclude-standard
Pop-Location
$excluded = '^(\.idea/|\.claude/|\.kotlin/|design/check/|design/photos/)|(^|/)(build|\.gradle|__pycache__)/|(^|/)local\.properties$'
$copied = 0
foreach ($f in $files) {
    if ($f -match $excluded) { continue }
    $from = Join-Path $repo $f
    if (-not (Test-Path $from -PathType Leaf)) { continue }   # deleted but not yet committed
    $to = Join-Path $src $f
    New-Item -ItemType Directory -Force (Split-Path $to) | Out-Null
    Copy-Item $from $to
    $copied++
}
Write-Output "SourceCode: $copied files"

# ---- 2. LayoutAndKotlin -------------------------------------------------------------------
$lk = Join-Path $stage 'LayoutAndKotlin'
New-Item -ItemType Directory -Force "$lk\layout", "$lk\androidTest" | Out-Null
Copy-Item "$repo\app\src\main\res\layout\*.xml" "$lk\layout"

$kotlinRoot = "$repo\app\src\main\java\com\rameen\i230806"
Get-ChildItem $kotlinRoot -Recurse -Filter *.kt | ForEach-Object {
    $rel = $_.FullName.Substring($kotlinRoot.Length + 1)        # e.g. ui\auth\LoginActivity.kt
    $to  = Join-Path $lk $rel
    New-Item -ItemType Directory -Force (Split-Path $to) | Out-Null
    Copy-Item $_.FullName $to
}
Copy-Item "$repo\app\src\androidTest\java\com\rameen\i230806\*.kt" "$lk\androidTest"

# ---- 3. Zip (top-level folder inside the zip = $name) --------------------------------------
# Entries are added one by one so their names use "/" (Windows PowerShell's CreateFromDirectory
# writes "\", which macOS / Linux unzip tools treat as part of the file name).
$zip = [System.IO.Compression.ZipFile]::Open($zipPath, 'Create')
Get-ChildItem $stage -Recurse -File | ForEach-Object {
    $entry = $name + '/' + $_.FullName.Substring($stage.Length + 1).Replace('\', '/')
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $entry,
        [System.IO.Compression.CompressionLevel]::Optimal) | Out-Null
}
$zip.Dispose()
Write-Output ("Zip: {0} ({1:N1} MB)" -f $zipPath, ((Get-Item $zipPath).Length / 1MB))

# ---- 4. Report the contents ----------------------------------------------------------------
$zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
$entries = $zip.Entries | ForEach-Object { $_.FullName.Replace('\', '/') }
$zip.Dispose()
Write-Output "Top two levels under $name/:"
$entries | ForEach-Object {
    $p = $_ -split '/'
    if ($p.Count -gt 3) { "  " + ($p[1..2] -join '/') + '/' }    # a folder at level 2
    elseif ($p.Count -eq 3) { "  " + ($p[1..2] -join '/') }      # a file at level 2
} | Sort-Object -Unique
foreach ($part in 'SourceCode', 'LayoutAndKotlin') {
    $inPart = $entries | Where-Object { $_ -like "$name/$part/*" }
    $xml = ($inPart | Where-Object { $_ -like '*.xml' }).Count
    $kt  = ($inPart | Where-Object { $_ -like '*.kt' }).Count
    Write-Output ("{0}: {1} files, {2} XML, {3} Kotlin" -f $part, $inPart.Count, $xml, $kt)
}

# ---- 5. Check the zipped source builds -----------------------------------------------------
$verify = Join-Path $env:TEMP 'i230806_verify'
if (Test-Path $verify) { Remove-Item $verify -Recurse -Force }
[System.IO.Compression.ZipFile]::ExtractToDirectory($zipPath, $verify)
if (-not $env:ANDROID_HOME) {   # the copy has no local.properties, so point Gradle at the SDK
    $sdkLine = Select-String -Path "$repo\local.properties" -Pattern '^sdk\.dir=' | Select-Object -First 1
    $env:ANDROID_HOME = ($sdkLine.Line -replace '^sdk\.dir=', '') -replace '\\\\', '\' -replace '\\:', ':'
}
Push-Location "$verify\$name\SourceCode\i230806"
& .\gradlew.bat assembleDebug --no-daemon -q
$code = $LASTEXITCODE
$apk = Test-Path 'app\build\outputs\apk\debug\app-debug.apk'
Pop-Location
Remove-Item $verify -Recurse -Force
if ($code -ne 0 -or -not $apk) { throw "Zipped SourceCode did NOT build (exit $code)" }
Write-Output "Zipped SourceCode builds: OK (app-debug.apk produced); temp folder deleted"
