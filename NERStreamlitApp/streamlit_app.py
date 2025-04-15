"""
Entry point for Streamlit Cloud deployment.
"""
import os
import sys

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import NERProcessor - verify module is loaded before importing app.py
try:
    import spacy
    # Explicitly ensure spaCy model is installed
    import en_core_web_sm
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)

# Import the app module
from app import * 