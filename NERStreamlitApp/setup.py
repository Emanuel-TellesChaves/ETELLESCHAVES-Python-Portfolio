from setuptools import setup

setup(
    name="NERStreamlitApp",
    version="0.1.0",
    description="Custom Named Entity Recognition using spaCy and Streamlit",
    python_requires=">=3.8,<3.12",
    install_requires=[
        "streamlit==1.24.0",
        "numpy==1.23.5",
        "pandas==1.5.3",
        "spacy==3.8.0",
        "nltk==3.8.1",
        "pydantic==1.10.8",
        "typing-extensions==4.5.0",
    ],
) 