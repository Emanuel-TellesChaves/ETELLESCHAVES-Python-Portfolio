from setuptools import setup, find_packages

setup(
    name="NERStreamlitApp",
    version="0.1.0",
    description="Custom Named Entity Recognition using spaCy and Streamlit",
    python_requires=">=3.9,<3.10",
    install_requires=[
        "streamlit>=1.24.0",
        "spacy>=3.8.0",
        "pandas>=1.5.3",
        "numpy>=1.23.5",
        # Pillow is installed separately in setup.sh
    ],
) 