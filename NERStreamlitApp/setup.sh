#!/bin/bash

# Make sure the script stops on first error
set -e

# Upgrade pip to the latest version
pip install --upgrade pip

# Install required dependencies first
pip install -r requirements.txt

# Make sure spaCy model is linked
python -m spacy link en_core_web_sm en_core_web_sm

# Verify installations
echo "Setup complete!"
echo "Pillow version: $(python -c 'import PIL; print(PIL.__version__)')"
echo "spaCy version: $(python -c 'import spacy; print(spacy.__version__)')" 