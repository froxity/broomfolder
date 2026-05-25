$ErrorActionPreference = "Stop"

$repoDir = $PSScriptRoot

$launcherSource = Join-Path $repoDir "bin\broomfolder.cmd"
$scriptSource = Join-Path $repoDir "broomfolder.py"
$installDir = if ($env:BROOMFOLDER_INSTALL_DIR) {
    $env:BROOMFOLDER_INSTALL_DIR
} else {
    Join-Path $HOME "AppData\Local\Programs\broomfolder\bin"
}

New-Item -ItemType Directory -Force -Path $installDir | Out-Null
Copy-Item -Force $launcherSource (Join-Path $installDir "broomfolder.cmd")
Copy-Item -Force $scriptSource (Join-Path $installDir "broomfolder.py")

Write-Host "Installed broomfolder at $installDir\broomfolder.cmd"
Write-Host "Make sure $installDir is in your PATH."
