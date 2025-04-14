import streamlit as st
import sys
import os

# Set the working directory to this file's location
working_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(working_dir)

# Add the current directory to the path
if working_dir not in sys.path:
    sys.path.append(working_dir)

try:
    # First try importing numpy to ensure it's properly loaded
    import numpy as np
    print(f"NumPy version: {np.__version__}")
    
    # Then import other dependencies
    import pandas as pd
    import spacy
    
    print(f"Pandas version: {pd.__version__}")
    print(f"spaCy version: {spacy.__version__}")
    
    # Check if spaCy model is available
    try:
        nlp = spacy.load("en_core_web_sm")
        print("spaCy model loaded successfully")
    except:
        print("spaCy model not found, attempting to download")
        spacy.cli.download("en_core_web_sm")
    
    # Now import the app module
    from app import *
    
except Exception as e:
    st.set_page_config(page_title="Error", page_icon="⚠️")
    st.title("⚠️ Application Error")
    st.error(f"An error occurred during initialization: {str(e)}")
    
    # Display system information for debugging
    st.write("### System Information")
    st.code(f"""
    Python version: {sys.version}
    Path: {sys.path}
    Working directory: {os.getcwd()}
    """)
    
    # Offer to run diagnostics
    st.write("### Diagnostics")
    if st.button("Run Diagnostics"):
        try:
            import check_environment
        except Exception as diag_error:
            st.error(f"Failed to run diagnostics: {str(diag_error)}")
            
            # Try to manually fix the most common issues
            st.warning("Attempting to fix common issues...")
            import subprocess
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.23.5", "--force-reinstall", "--no-cache-dir"])
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--no-deps", "--no-cache-dir"])
                st.success("Dependencies reinstalled. Please refresh the page.")
            except Exception as fix_error:
                st.error(f"Failed to fix issues: {str(fix_error)}")
    
    # Show requirements
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read()
        st.write("### Current Requirements")
        st.code(requirements, language="text")
    except Exception as req_error:
        st.error(f"Failed to read requirements: {str(req_error)}") 