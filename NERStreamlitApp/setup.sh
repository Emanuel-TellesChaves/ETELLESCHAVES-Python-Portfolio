#!/bin/bash

# Make sure the script stops on first error
set -e

# Upgrade pip to the latest version
pip install --upgrade pip

# Print Python version
python --version

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --no-cache-dir --prefer-binary

# Make sure spaCy model is linked - using the correct version
python -m spacy link en_core_web_sm-3.7.1 en_core_web_sm

# Verify installations
echo "Setup complete!"
pip list | grep -E "pillow|numpy|pandas|spacy|streamlit"
python -c "import PIL; print('Pillow version:', PIL.__version__)"
python -c "import spacy; print('spaCy version:', spacy.__version__)"
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model loaded successfully')" 