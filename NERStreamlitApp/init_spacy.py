"""
Initialization script to ensure spaCy and its models are properly loaded
before the main application starts.
"""

import os
import sys
import site
import numpy as np
import pandas as pd
import spacy

def check_installation():
    """Print details about the installation for debugging."""
    print("Python version:", sys.version)
    print("Site packages:", site.getsitepackages())
    print("NumPy version:", np.__version__)
    print("NumPy path:", np.__file__)
    print("pandas version:", pd.__version__)
    print("spaCy version:", spacy.__version__)
    print("spaCy path:", spacy.__file__)

def load_models():
    """Load spaCy models to verify they work."""
    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp("This is a test sentence to verify spaCy works.")
        print("spaCy model loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading spaCy model: {e}")
        return False

if __name__ == "__main__":
    check_installation()
    success = load_models()
    
    if not success:
        try:
            print("Trying to download model...")
            spacy.cli.download("en_core_web_sm")
            success = load_models()
        except Exception as e:
            print(f"Failed to download model: {e}")
    
    print("Initialization complete") 