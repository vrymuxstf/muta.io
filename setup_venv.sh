#!/bin/bash

# Name of the virtual environment directory
VENV_DIR=".venv"

# Check if the virtual environment exists; if not, create it
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo "Virtual environment activated."

# Create a requirements.txt file with the list of installed packages
echo "Generating requirements.txt..."
pip freeze > requirements.txt
echo "requirements.txt generated."

# Install packages from the requirements.txt file
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "Dependencies installed from requirements.txt."

# Additional script operations
echo "Setup complete. You can start your application."

# Keep the terminal open
read -p "Press [Enter] to exit..."