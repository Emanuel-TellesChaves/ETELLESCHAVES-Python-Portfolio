#!/bin/bash

# Make sure the script stops on first error
set -e

# Install Python dependencies
pip install -r requirements.txt

# Create directories for models if needed
mkdir -p ~/.cache/spacy 