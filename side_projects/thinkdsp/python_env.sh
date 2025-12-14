#!/usr/bin/env bash
set -e                  # Exit on error

#------------------------------------------
# Config
#------------------------------------------
ENV_NAME="${1:-myenv}"  # Use first argument as env name, default = myenv
PYTHON_BIN="python3"

#------------------------------------------
# Create virtual environment
#------------------------------------------
echo "Creating virtual environment: $ENV_NAME"          # Prints to console
$PYTHON_BIN -m venv "$ENV_NAME"                         # python3 -m venv myvenv

#------------------------------------------
# Activate environment
#------------------------------------------
source "$ENV_NAME/bin/activate"                         # source myenv/bin/activate

#------------------------------------------
# Install packages
#------------------------------------------
#Note: you can update these as needed
echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing packages..."

# Install jupyter notebooks
echo "Installing jupyter..."
pip install jupyter

# Install numpy
echo "Installing numpy..."
pip install numpy

# Install scipy
echo "Installing scipy..."
pip install scipy

# Install matplotlib
echo "Installing matplotlib..."
pip install matplotlib

#------------------------------------------
# Info printout
#------------------------------------------
echo "Virtual environment '$ENV_NAME' created and installed."
echo "To activate later, run:"
echo "     source $ENV_NAME/bin/activate"