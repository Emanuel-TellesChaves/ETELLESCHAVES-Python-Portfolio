"""
Entry point for Streamlit Cloud deployment.
"""
import os
import sys
import traceback

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# First verify all required dependencies are available
try:
    import streamlit as st
    
    # Try to import typing to diagnose issues
    try:
        import typing
        st.write(f"Typing version: {typing.__version__}")
    except Exception as e:
        st.error(f"Error with typing module: {e}")
        st.code(traceback.format_exc())
        
    # Try to import pydantic to diagnose issues
    try:
        import pydantic
        st.write(f"Pydantic version: {pydantic.__version__}")
    except Exception as e:
        st.error(f"Error with pydantic module: {e}")
        st.code(traceback.format_exc())
    
    # Try to load the spaCy model
    try:
        import spacy
        st.write(f"spaCy version: {spacy.__version__}")
        try:
            import en_core_web_sm
            nlp = en_core_web_sm.load()
        except ImportError:
            # Try loading directly
            try:
                nlp = spacy.load("en_core_web_sm")
            except Exception as e:
                st.error(f"Error loading spaCy model: {e}")
                st.info("Please verify the model is installed correctly.")
                st.stop()
    except Exception as e:
        st.error(f"Error with spaCy: {e}")
        st.code(traceback.format_exc())
            
except ImportError as e:
    import streamlit as st
    st.error(f"Required dependency missing: {e}")
    st.info("Please make sure all required packages are installed.")
    st.stop()

# Import the app module
try:
    from app import *
except Exception as e:
    import streamlit as st
    st.error(f"Error loading application: {e}")
    st.code(traceback.format_exc())
    st.stop() 