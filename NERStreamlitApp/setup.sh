#!/bin/bash

# Make sure the script stops on first error
set -e

# Upgrade pip to the latest version
pip install --upgrade pip

# Print Python version
python --version

# Check if we're on Linux and Python 3.12 (likely Streamlit Cloud)
if [[ "$(python -c 'import sys; import platform; print(platform.system() == "Linux" and sys.version_info[:2] == (3, 12))')" == "True" ]]; then
    echo "Detected Linux with Python 3.12, installing Pillow from wheel..."
    pip install https://files.pythonhosted.org/packages/8d/6e/5374c9df9c3a389fe4e07227604b76923fcf95705b5f42dba56fa1ac1200/Pillow-10.1.0-cp312-cp312-manylinux_2_28_x86_64.whl --no-cache-dir
    grep -v "Pillow" requirements.txt > requirements_filtered.txt
    pip install -r requirements_filtered.txt --no-cache-dir --prefer-binary
else
    # For all other platforms, use the regular requirements.txt
    echo "Installing all dependencies..."
    pip install -r requirements.txt --no-cache-dir --prefer-binary
fi

# Make sure spaCy model is linked - using the correct version
python -m spacy link en_core_web_sm-3.7.1 en_core_web_sm

# Verify installations
echo "Setup complete!"
pip list | grep -E "pillow|numpy|pandas|spacy|streamlit"
python -c "import PIL; print('Pillow version:', PIL.__version__)"
python -c "import spacy; print('spaCy version:', spacy.__version__)"
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model loaded successfully')" 