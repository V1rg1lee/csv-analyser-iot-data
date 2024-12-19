# PowerShell Script for Windows

# Check if Python3 is installed
if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Host "Python3 could not be found. Please install Python3 to proceed." -ForegroundColor Red
    exit 1
}

# Check if data directory and subdirectories exist
$dataDir = "data"
$subDirs = @("fr", "kr", "sp", "us")

if (-not (Test-Path -Path $dataDir)) {
    Write-Host "Data directory not found. Please make sure the 'data' directory exists." -ForegroundColor Red
    exit 1
}

foreach ($subDir in $subDirs) {
    if (-not (Test-Path -Path (Join-Path $dataDir $subDir))) {
        Write-Host "Subdirectory '$subDir' not found in 'data' directory. Please make sure it exists." -ForegroundColor Red
        exit 1
    }
}

# Create a virtual environment if it doesn't exist
if (-not (Test-Path -Path "env")) {
    Write-Host "Creating virtual environment..."
    python -m venv env
} else {
    Write-Host "Virtual environment already exists."
}

# Activate the virtual environment
& .\env\Scripts\Activate.ps1

# Install dependencies from requirements.txt
if (Test-Path -Path "requirements.txt") {
    Write-Host "Installing dependencies..."
    pip install -r requirements.txt
} else {
    Write-Host "requirements.txt not found. Please make sure it is in the current directory." -ForegroundColor Red
    exit 1
}

# Run the Python scripts in order
Write-Host "Running absence-patterns.py..."
python absence-patterns.py

Write-Host "Running device-country-per-hour.py..."
python device-country-per-hour.py

Write-Host "Running diversity-index.py..."
python diversity-index.py

Write-Host "Running top-ten-country.py..."
python top-ten-country.py

Write-Host "All scripts executed successfully!" -ForegroundColor Green

# Deactivate the virtual environment
deactivate
