"""
Main entry point for the NER Streamlit App.
This is the file Streamlit Cloud should run.
"""
import os
import sys

# Add the current directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Just import from app.py which has all the Streamlit code
from app import * 