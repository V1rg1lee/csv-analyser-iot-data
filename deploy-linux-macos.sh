#!/bin/bash

# Check if Python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Please install Python3 to proceed."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv env
else
    echo "Virtual environment already exists."
fi

# Check if data directory and subdirectories exist
dataDir="data"
subDirs=("fr" "kr" "sp" "us")

if [ ! -d "$dataDir" ]; then
    echo "Data directory not found. Please make sure the 'data' directory exists."
    exit 1
fi

for subDir in "${subDirs[@]}"; do
    if [ ! -d "$dataDir/$subDir" ]; then
        echo "Subdirectory '$subDir' not found in 'data' directory. Please make sure it exists."
        exit 1
    fi
done

# Activate the virtual environment
source env/bin/activate

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Please make sure it is in the current directory."
    exit 1
fi

# Run the Python scripts in order
echo "Running absence-patterns.py..."
python absence-patterns.py

echo "Running device-country-per-hour.py..."
python device-country-per-hour.py

echo "Running diversity-index.py..."
python diversity-index.py

echo "Running top-ten-country.py..."
python top-ten-country.py

echo "All scripts executed successfully!"

# Deactivate the virtual environment
deactivate