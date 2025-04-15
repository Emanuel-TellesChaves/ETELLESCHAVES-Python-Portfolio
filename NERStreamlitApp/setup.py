from setuptools import setup, find_packages

setup(
    name="NERStreamlitApp",
    version="0.1.0",
    description="Custom Named Entity Recognition using spaCy and Streamlit",
    python_requires=">=3.10,<3.11",
    install_requires=[
        "streamlit>=1.32.0",
        "spacy>=3.8.0",
        "pandas>=2.0.0",
        "numpy>=1.26.0",
        # Pillow is installed separately in setup.sh
    ],
) 