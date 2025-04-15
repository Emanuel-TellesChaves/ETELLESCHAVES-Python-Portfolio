#!/bin/bash

# Make sure the script stops on first error
set -e

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Link spaCy model (don't try to download it again)
python -m spacy link en_core_web_sm en_core_web_sm 