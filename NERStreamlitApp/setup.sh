#!/bin/bash

# Make sure the script stops on first error
set -e

# Upgrade pip to the latest version
pip install --upgrade pip==25.0.1

# Install Pillow as pre-built wheel first
pip install --only-binary :all: pillow==9.5.0

# Install Python dependencies
pip install -r requirements.txt

# Link spaCy model (don't try to download it again)
python -m spacy link en_core_web_sm en_core_web_sm 