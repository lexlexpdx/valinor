#!/bin/bash

# This script just allows for the easy movement of resource packs to the prism launcher
# folder for minecraft

# Source and Destination directories
SRC="$HOME/Downloads"
DST="$HOME/.var/app/org.prismlauncher.PrismLauncher/data/PrismLauncher/instances/1.21.10/minecraft/resourcepacks"

# Ensure destination folder exists

if [ ! -d "$DST" ]
then
    echo "Desitnation folder does not exist:"
    echo "$DST"
    exit 1
fi

# Find zip files and move them
shopt -s nullglob
files=("$SRC"/*.zip)

if (( ${#files[@]} == 0))
then
    echo "No resource packs found in downloads"
    exit 0
fi

echo "Moving resource packs to PrismLauncher..."
mv -n "${files[@]}" "$DST"

echo "Done."
