import streamlit as st
import sys
import platform
import subprocess
import importlib.util

st.set_page_config(page_title="Environment Check", page_icon="🔍")
st.title("Environment Diagnostics")

# Basic environment info
st.write("### System Information")
st.code(f"""
Python version: {sys.version}
Platform: {platform.platform()}
Architecture: {platform.architecture()}
""")

# Check for required packages
packages = [
    "numpy", "pandas", "spacy", "streamlit", 
    "pydantic", "nltk", "setuptools"
]

st.write("### Package Versions")
package_info = []

for package in packages:
    try:
        spec = importlib.util.find_spec(package)
        if spec is not None:
            module = importlib.import_module(package)
            version = getattr(module, "__version__", "Unknown")
            package_info.append(f"{package}: {version} (✅ Installed)")
        else:
            package_info.append(f"{package}: ❌ Not found")
    except ImportError:
        package_info.append(f"{package}: ❌ Import error")
    except Exception as e:
        package_info.append(f"{package}: ⚠️ Error: {str(e)}")

st.code("\n".join(package_info))

# Check numpy compatibility
st.write("### NumPy Compatibility Check")
try:
    import numpy as np
    st.write(f"NumPy version: {np.__version__}")
    st.write(f"NumPy path: {np.__file__}")
    
    # Test numpy operations
    test_array = np.array([1, 2, 3])
    st.write(f"NumPy test operation: {test_array.mean()}")
    st.success("NumPy is working correctly!")
except Exception as e:
    st.error(f"NumPy error: {str(e)}")

# Check spaCy model
st.write("### spaCy Model Check")
try:
    import spacy
    st.write(f"spaCy version: {spacy.__version__}")
    
    try:
        nlp = spacy.load("en_core_web_sm")
        st.success("✅ spaCy model loaded successfully!")
        
        # Test processing
        doc = nlp("This is a test sentence.")
        tokens = [token.text for token in doc]
        st.write(f"Tokenized test sentence: {tokens}")
    except Exception as model_error:
        st.error(f"❌ Error loading spaCy model: {str(model_error)}")
        
        # Try downloading the model
        st.warning("Attempting to download spaCy model...")
        try:
            spacy.cli.download("en_core_web_sm")
            st.success("Model downloaded. Please refresh the page.")
        except Exception as download_error:
            st.error(f"Failed to download model: {str(download_error)}")
except Exception as e:
    st.error(f"spaCy error: {str(e)}")

# Continue to main app button
st.write("### Continue")
if st.button("Continue to Main Application"):
    st.success("Environment checked successfully! Redirecting to main app...")
    st.markdown("""
    <meta http-equiv="refresh" content="2;URL='app'">
    """, unsafe_allow_html=True) 