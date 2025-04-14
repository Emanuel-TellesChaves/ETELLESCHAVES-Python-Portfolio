"""
Entry point for Streamlit Cloud deployment.
"""
import os
import sys
import streamlit as st

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    # Import packages in correct order with versions compatible with Python 3.12
    import numpy as np
    import pandas as pd
    import spacy
    
    # Print versions for debugging
    st.sidebar.markdown("### Environment Info")
    st.sidebar.markdown(f"NumPy: {np.__version__}")
    st.sidebar.markdown(f"pandas: {pd.__version__}")
    st.sidebar.markdown(f"spaCy: {spacy.__version__}")
    
    # Try to import the app module
    from app import *
except ImportError as e:
    st.error(f"ImportError: {e}")
    st.info("Trying to fix dependencies...")
    
    try:
        import subprocess
        
        # Install latest setuptools and wheel
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "setuptools", "wheel"])
        
        # Install Python 3.12 compatible NumPy first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy>=1.26.0", "pandas>=2.0.0"])
        
        # Install remaining dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        # Reload the app
        st.success("Dependencies installed. Reloading app...")
        st.experimental_rerun()
    except Exception as fix_error:
        st.error(f"Failed to fix dependencies: {fix_error}")
        
        # Show system info
        st.write("### System Information")
        import platform
        st.code(f"""
        Python version: {sys.version}
        Platform: {platform.platform()}
        Path: {sys.path}
        Current directory: {os.getcwd()}
        """)
except Exception as e:
    st.error(f"An error occurred: {e}")
    # Try loading diagnostic tool
    try:
        import check_environment
    except:
        st.error("Could not load diagnostics.") 