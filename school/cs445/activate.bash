#!/bin/bash

# This just a stupid script that helps me activate my venv because
# my shell doesn't show when the venv is active :(

# Check if the directory exists
if [ ! -d "./myenv" ]
then
    echo "Error: Virtual environment doesn't exist"
    echo "Run ./python_env.bash to create"
fi

# Check to see if activation script exists
if [ ! -f "./myenv/bin/activate" ]
then
    echo "Error: Activation script not found"
    exit 1
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source ./myenv/bin/activate

# confirm virtual environment
if [ -n "$VIRTUAL_ENV" ]
then
    echo "✓ Virtual environment active at: $VIRTUAL_ENV"
    echo "✓ Using python: $(which python)"
    echo ""
    echo "To deactivate later, run: deactivate"
else
    echo "Failed to activate virtual environment"
    exit 1
fi