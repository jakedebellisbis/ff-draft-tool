# setup.ps1  — run from: ff-draft-tool\backend
# One-time setup: create Python 3.12 venv, install deps, init DB.

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Write-Host "== Backend setup starting =="

# Go to the folder this script lives in (backend/)
Set-Location -Path $PSScriptRoot

# Make sure Python 3.12 is available
Write-Host "Checking for Python 3.12..."
try {
  $ver = & py -3.12 -V
  Write-Host "Found: $ver"
} catch {
  Write-Host "Python 3.12 not found. If winget is available, run:"
  Write-Host "    winget install --id Python.Python.3.12 -e"
  Write-Host "Or download from https://www.python.org/downloads/windows/ (check 'Add Python to PATH')"
  throw
}

# (Re)create venv if missing
if (!(Test-Path ".\.venv\Scripts\python.exe")) {
  Write-Host "Creating virtual environment (.venv) with Python 3.12..."
  & py -3.12 -m venv .venv
}

$venvPy = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

# Upgrade pip (quietly)
& $venvPy -m pip install --upgrade pip > $null

# Install dependencies
Write-Host "Installing backend dependencies..."
& $venvPy -m pip install -r requirements.txt

# Initialize the database (create tables)
Write-Host "Initializing the SQLite database..."
& $venvPy -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

Write-Host "== Backend setup complete =="
Write-Host "Next: run .\run_api.ps1 to start the server."
