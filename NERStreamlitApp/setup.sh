#!/bin/bash

# Make sure the script stops on first error
set -e

# Upgrade pip to the latest version
pip install --upgrade pip

# Install pre-built Pillow wheel first
echo "Installing Pillow from pre-built wheel..."
pip install https://files.pythonhosted.org/packages/cd/87/3e0241e04a93b3599d455277e79e9e92e07ac476da1a8db9e155e2ff58ff/Pillow-9.5.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# Install other dependencies
echo "Installing other dependencies..."
sed '/Pillow/d' requirements.txt > requirements_without_pillow.txt
pip install -r requirements_without_pillow.txt --no-cache-dir

# Make sure spaCy model is linked - using the correct version
python -m spacy link en_core_web_sm-3.7.1 en_core_web_sm

# Verify installations
echo "Setup complete!"
pip list | grep -E "pillow|numpy|pandas|spacy|streamlit"
python -c "import PIL; print('Pillow version:', PIL.__version__)"
python -c "import spacy; print('spaCy version:', spacy.__version__)"
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model loaded successfully')" 