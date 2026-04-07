#!/usr/bin/env bash

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

# Install pandas
echo "Installing pandas..."
pip install pandas

# Install WFDB library
#echo "Installing WFBD library"
#pip install wfdb

# Install Neurokit library
#echo "Installing NeuroKit library"
#pip install neurokit2

# Install sklearn
echo "Installing Sklearn"
pip install scikit-learn

#------------------------------------------
# Info printout
#------------------------------------------
echo "Virtual environment '$ENV_NAME' created and installed."
echo "To activate later, run:"
echo "     source $ENV_NAME/bin/activate"