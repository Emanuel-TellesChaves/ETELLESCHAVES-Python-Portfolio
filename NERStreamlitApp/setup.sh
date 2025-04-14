#!/bin/bash

# Make sure the script stops on first error
set -e

# Install Python dependencies
pip install -r requirements.txt --progress-bar off

# Download spaCy model if not already present
python -m spacy download en_core_web_sm

# Create directories for models if needed
mkdir -p ~/.cache/spacy 