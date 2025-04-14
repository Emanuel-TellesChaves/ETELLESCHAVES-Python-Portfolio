#!/bin/bash

# Make sure the script stops on first error
set -e

# Upgrade pip first
pip install --upgrade pip

# Install setuptools and wheel first to avoid dependency issues
pip install setuptools>=65.5.1 wheel>=0.42.0 setuptools-scm>=7.1.0 --no-cache-dir

# Install Pillow first to avoid build issues
pip install pillow>=10.0.0 --no-cache-dir

# Install NumPy and pandas first (Python 3.12 compatible versions)
pip install numpy>=1.26.0 pandas>=2.0.0 --no-cache-dir

# Install the spaCy model directly
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl --no-cache-dir

# Install remaining dependencies
pip install streamlit==1.24.0 --no-cache-dir
pip install spacy==3.8.0 --no-cache-dir
pip install -r requirements.txt --no-cache-dir

# Check if spaCy model is properly installed
if python -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
  echo "spaCy model successfully installed"
else
  echo "Manual installation of spaCy model"
  python -m spacy download en_core_web_sm
fi

# Create directories for models if needed
mkdir -p ~/.cache/spacy 