#!/bin/bash

# Make sure the script stops on first error
set -e

# Upgrade pip first
pip install --upgrade pip

# Clean install numpy first to avoid compatibility issues
pip uninstall -y numpy || true
pip install numpy==1.24.3 --no-cache-dir

# Install Python dependencies in order
pip install streamlit>=1.24.0 --no-cache-dir
pip install pandas==1.5.3 --no-cache-dir
pip install -r requirements.txt --no-cache-dir --no-deps
pip install -r requirements.txt --no-cache-dir

# Check if spaCy model is already downloaded 
if python -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
  echo "spaCy model already downloaded"
else
  # Download spaCy model if not already present
  python -m spacy download en_core_web_sm==3.8.0
fi

# Create directories for models if needed
mkdir -p ~/.cache/spacy 