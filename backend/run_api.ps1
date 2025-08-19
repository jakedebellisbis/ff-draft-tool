# run_api.ps1  — run from: ff-draft-tool\backend
# Starts the FastAPI server using the venv's Python.

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
Set-Location -Path $PSScriptRoot

$venvPy = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (!(Test-Path $venvPy)) {
  Write-Host "Virtual env not found. Run .\setup.ps1 first." -ForegroundColor Yellow
  exit 1
}

# Run Uvicorn (development server)
& $venvPy -m uvicorn app.main:app --reload
