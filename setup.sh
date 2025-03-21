#!/bin/bash

# Create necessary directories
mkdir -p logs

# Create a copy of the crude service file
cp hedge_service.py hedge_service2.py

# Create a virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Setup complete! Please edit hedge_service.py with your credentials before running." 