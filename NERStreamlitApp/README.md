# Custom Named Entity Recognition (NER) Application

## Project Overview

This application provides a user-friendly interface for Named Entity Recognition (NER) using spaCy and Streamlit. Named Entity Recognition is an NLP technique that identifies and classifies named entities in text into predefined categories such as person names, organizations, locations, dates, etc.

The unique feature of this application is that it allows users to define custom entity labels and patterns without needing to train a full NLP model, leveraging spaCy's EntityRuler component.

## Features

- **Text Input**: Enter text directly or upload text files for analysis
- **Custom Entity Definition**: Define your own entity categories and patterns
- **Rule-Based Recognition**: Leverage spaCy's EntityRuler for pattern matching
- **Interactive Visualization**: See highlighted entities in the processed text
- **Sample Texts**: Try the application with pre-loaded examples
- **Override Capabilities**: Custom entities can override spaCy's default entities

## Setup Instructions

### Prerequisites

- Python 3.7+
- Python 3.12 (Streamlit Cloud deployment)
- pip (Python package installer)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/NERStreamlitApp.git
   cd NERStreamlitApp
   cd ETELLESCHAVES-Python-Portfolio/NERStreamlitApp
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Install the spaCy language model:
   ```
   python -m spacy download en_core_web_sm
   ```

### Running the Application

Start the Streamlit application:
```
streamlit run streamlit_app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Usage Guide

### Defining Custom Entities

1. Enter entity label (e.g., "PRODUCT", "COMPANY", "TECHNOLOGY")
2. Define patterns that match this entity
3. Patterns can be:
   - Exact text matches (e.g., "Microsoft", "Python")
   - Token patterns with attributes like lowercase, shape, etc.

Example patterns:
- Simple text: "Google", "Tesla", "Python"
- Pattern with attributes: `[{"LOWER": "artificial"}, {"LOWER": "intelligence"}]`

### Processing Text

1. Enter or upload text in the "Text Input" tab
2. Add your custom entity definitions in the "Entity Definition" tab
3. Click "Process Text" in the "Results" tab
4. View the highlighted entities in the output

### Text Input Tab
This tab allows users to:
- Enter text directly in a text area
- Upload a text file (with .txt extension)
- Select from sample texts
- Clear all content

### Entity Definition Tab
This tab enables users to:
- Create custom entity labels (like COMPANY, PRODUCT, TECHNOLOGY)
- Define patterns that match each entity
- View and manage current entity patterns
- Access help for pattern syntax and examples

### Results Tab
In this tab, users can:
- Process the text with the defined entity patterns
- View the text with color-coded entity highlighting
- See a table of all detected entities
- View entity counts by category

## Project Structure

```
NERStreamlitApp/
├── streamlit_app.py           # Entry point for Streamlit Cloud
├── app.py                     # Main application logic
├── ner_processor.py           # NER processing logic
├── utils.py                   # Utility functions
├── sample_texts/              # Sample text files for testing
│   ├── tech_news.txt          # Technology news sample
│   └── business.txt           # Business news sample
├── .streamlit/                # Streamlit configuration
│   └── config.toml            # Configuration settings
├── requirements.txt           # Python dependencies
├── packages.txt               # System dependencies for Streamlit Cloud
├── setup.sh                   # Setup script for Streamlit Cloud deployment
├── runtime.txt                # Python version specification
└── README.md                  # Project documentation
```

## Required Libraries

- spaCy: For NLP and entity recognition
- Streamlit: For the web interface
- pandas: For data handling
- nltk: For additional text processing capabilities

## How It Works

1. **Entity Definition**: The application uses spaCy's `EntityRuler` component to define custom entity patterns
2. **Pattern Matching**: When you process text, the application uses these patterns to identify entities
3. **Custom Override**: The custom entities will override spaCy's default entities when there are conflicts
4. **Visual Highlighting**: Entities are highlighted with distinct colors based on their labels

## Deployment

### Local Deployment

To run the application locally:

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Download the spaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

### Streamlit Cloud Deployment

This app is configured for easy deployment to Streamlit Cloud:

1. Fork this repository to your GitHub account
2. Sign in to [Streamlit Cloud](https://share.streamlit.io/)
3. Create a new app and select your repository
4. Choose the main branch and set the main file path to `NERStreamlitApp/streamlit_app.py`
5. Click "Deploy"

The application will automatically use:
- `requirements.txt` for Python dependencies
- `packages.txt` for system dependencies
- `setup.sh` for additional setup commands
- `runtime.txt` for Python version specification

## References

- [spaCy Documentation](https://spacy.io/usage)
- [Streamlit Documentation](https://docs.streamlit.io)
- [EntityRuler Documentation](https://spacy.io/usage/rule-based-matching#entityruler)
- [Streamlit Cloud Deployment](https://docs.streamlit.io/streamlit-cloud)