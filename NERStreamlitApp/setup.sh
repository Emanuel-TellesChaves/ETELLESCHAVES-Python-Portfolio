#!/bin/bash

# Make sure the script stops on first error
set -e

# Upgrade pip to the latest version
pip install --upgrade pip

# Print Python version
python --version

# Install Pillow directly from wheel
echo "Installing Pillow from pre-built wheel..."
pip install https://files.pythonhosted.org/packages/8d/6e/5374c9df9c3a389fe4e07227604b76923fcf95705b5f42dba56fa1ac1200/Pillow-10.1.0-cp312-cp312-manylinux_2_28_x86_64.whl --no-cache-dir

# Install all other dependencies with no-cache-dir to ensure fresh download
echo "Installing dependencies..."
grep -v "Pillow" requirements.txt | grep -v "https://files.pythonhosted.org" > requirements_filtered.txt
pip install -r requirements_filtered.txt --no-cache-dir --prefer-binary

# Make sure spaCy model is linked - using the correct version
python -m spacy link en_core_web_sm-3.7.1 en_core_web_sm

# Verify installations
echo "Setup complete!"
pip list | grep -E "pillow|numpy|pandas|spacy|streamlit"
python -c "import PIL; print('Pillow version:', PIL.__version__)"
python -c "import spacy; print('spaCy version:', spacy.__version__)"
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model loaded successfully')" 