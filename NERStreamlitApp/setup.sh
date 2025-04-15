#!/bin/bash

# Make sure the script stops on first error
set -e

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Make sure spaCy model is downloaded and linked
python -m spacy download en_core_web_sm
python -m spacy link en_core_web_sm en_core_web_sm 