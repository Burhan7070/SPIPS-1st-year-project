# PowerShell script to create a virtual environment, install dependencies and build the EXE
$ErrorActionPreference = 'Stop'

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not found on PATH. Install Python 3.8+ and try again."
    exit 1
}

# Create venv if missing
if (-not (Test-Path -Path ".venv")) {
    python -m venv .venv
}

# Activate venv for the current PowerShell session
. ".\.venv\Scripts\Activate.ps1"

pip install --upgrade pip
pip install -r requirements.txt

# Build with PyInstaller
pyinstaller --noconsole --onefile --name HotelApp "Final project.py"

if (Test-Path -Path "dist\HotelApp.exe") {
    Write-Host "Build succeeded: dist\HotelApp.exe"
} else {
    Write-Error "Build failed. Check PyInstaller output above for errors."
}
