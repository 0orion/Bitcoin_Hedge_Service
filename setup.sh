#!/bin/bash

# Create a virtual environment if not already created
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

# Optionally, run the Flask app
# FLASK_APP=hedge_service.py FLASK_ENV=development flask run
