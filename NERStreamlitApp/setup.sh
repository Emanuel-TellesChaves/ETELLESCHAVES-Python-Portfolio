#!/bin/bash

# Make sure the script stops on first error
set -e

# Fix numpy first to avoid compatibility issues
pip install numpy==1.24.3 --progress-bar off

# Install Python dependencies
pip install -r requirements.txt --progress-bar off

# Check if spaCy model is already downloaded 
if python -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
  echo "spaCy model already downloaded"
else
  # Download spaCy model if not already present
  python -m spacy download en_core_web_sm==3.8.0
fi

# Create directories for models if needed
mkdir -p ~/.cache/spacy 