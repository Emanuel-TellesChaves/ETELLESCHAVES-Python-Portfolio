# Python Data Science & Analytics Portfolio

This repository showcases my expertise in data analysis, visualization, and application development using Python. Each project demonstrates different technical skills and approaches to solving real-world data problems.

## Portfolio Overview

This collection represents a progression of skills from data analysis to interactive applications:

- **Data Transformation & Analysis**: The Tidy Data project demonstrates fundamental data cleaning, transformation, and statistical analysis skills—the foundation of any data science work.

- **Data Visualization & Storytelling**: All projects incorporate visualization techniques, with each showing different approaches from static matplotlib plots to interactive Plotly charts.

- **Interactive Application Development**: The Streamlit projects showcase my ability to transform data analysis into user-facing applications, making insights accessible to non-technical users.

- **Natural Language Processing**: The NER application demonstrates more advanced ML/AI capabilities, applying computational linguistics to extract structured information from text.

Together, these projects reflect my comprehensive skillset across the data science pipeline—from data preparation to insight generation to application development.

## Projects

### 1. Headline Finder with Sentiment Analysis (basic_streamlit_app)
An interactive web application built with Streamlit that analyzes news headlines and performs sentiment analysis based on user input.

**Key Features:**
- Closest headline search using TF-IDF and cosine similarity
- Weighted sentiment analysis of top 100 matching headlines
- Interactive filtering by sentiment and similarity threshold
- Dynamic pie chart visualization of sentiment distribution
- Real-time results update based on user parameters

**Technologies:**
- Streamlit for interactive web interface
- Pandas for data manipulation
- scikit-learn (TF-IDF, Cosine Similarity) for text matching
- NLTK for sentiment analysis
- Plotly for interactive visualizations

**Implementation Details:**
- Reads and processes a dataset of news headlines
- Computes similarity scores between user queries and headlines
- Applies sentiment analysis algorithms to determine headline sentiment
- Provides an intuitive interface for exploring headline sentiments

**Files in this Project:**
- `main.py` - Core application that handles UI, data processing, and visualization
- `all-data.csv` - Dataset containing thousands of news headlines for analysis
- `requirements.txt` - Dependencies required to run the application
- `README.md` - Project documentation and usage instructions

**[View Project →](./basic_streamlit_app)**

### 2. Portfolio Performance Analyzer & Backtester (StreamlitAppFinal)
A comprehensive Streamlit application for analyzing historical performance of stock portfolios against market benchmarks, allowing investors to make data-driven decisions.

**Key Features:**
- Portfolio performance analysis against market benchmarks
- Key financial metrics calculation (returns, volatility, Sharpe ratio, etc.)
- Interactive asset allocation visualization with customizable parameters
- Investment growth charts with performance comparison
- Risk assessment visualization

**Technologies:**
- Streamlit for interactive web interface
- Pandas and NumPy for financial calculations
- yfinance for retrieving historical stock data
- Plotly for interactive financial charts and visualizations
- Modular application architecture with separate utility modules

**Implementation Details:**
- Retrieves real-time and historical financial data
- Implements financial calculations based on Modern Portfolio Theory
- Provides visualization of portfolio performance metrics
- Features a clean, intuitive user interface for financial analysis

**Files in this Project:**
- `run.py` - Entry point that initializes and launches the Streamlit application
- `src/` directory:
  - Contains core application logic including portfolio analysis, data processing, and UI components
  - Modular structure separating concerns for maintainability
- `utils/` directory:
  - Helper functions for data processing, financial calculations, and visualization
  - Reusable components for chart generation and data transformations
- `data/` directory:
  - Contains sample portfolio data and cached market information
- `requirements.txt` - Dependencies required to run the application
- `README.md` - Project documentation with usage instructions

**[View Project →](./StreamlitAppFinal)**

### 3. Federal R&D Spending Analysis (TidyData_Project)
A comprehensive analysis of U.S. Federal Research & Development spending patterns from 1976 to 2017, showcasing the application of tidy data principles to transform messy data into a structured format for meaningful analysis.

**Key Features:**
- Data transformation using tidy data principles (each variable in a column, each observation in a row)
- Time series analysis of spending patterns across four decades
- Department-wise comparative analysis revealing shifts in R&D priorities
- GDP-relative spending trends showing the evolution of national R&D investment
- Advanced data visualization with clear explanations of historical patterns

**Technologies:**
- Pandas for data cleaning and transformation
- Matplotlib and Seaborn for statistical visualizations
- NumPy for numerical analysis
- Statistical analysis techniques for trend identification

**Implementation Details:**
- Transforms complex, nested data into tidy format
- Applies data normalization techniques for consistent analysis
- Implements time series visualization with multi-variable comparison
- Provides historical context with annotated visualizations

**Files in this Project:**
- `tidy-data-project.py` - Main script containing the entire analysis workflow
- `fed_rd_year&gdp.csv` - Source data with R&D spending figures and GDP values
- `tidy_federal_rd_data.csv` - Transformed dataset in tidy format
- `spending_over_time.png` - Generated visualization of spending trends
- `spending_percent_gdp.png` - Visualization of R&D spending as percentage of GDP
- `README.md` - Project documentation describing the analysis and findings

**[View Project →](./TidyData_Project)**

### 4. Custom Named Entity Recognition (NER) Application (NERStreamlitApp)
A sophisticated Streamlit-based application for custom Named Entity Recognition that allows users to define and visualize their own entity types without machine learning model training, demonstrating practical NLP techniques.

**Key Features:**
- Custom entity definition through pattern matching and rule creation
- Text processing from direct input, file upload, or sample texts
- Interactive visualization of recognized entities with color-coded highlighting
- Rule-based entity recognition using spaCy's EntityRuler
- Sample texts for immediate testing and demonstration
- Entity distribution analytics

**Technologies:**
- Streamlit for interactive web interface
- spaCy for natural language processing and entity recognition
- pandas for structured data handling
- NLTK for text preprocessing
- Object-oriented design for maintainable code architecture

**Implementation Details:**
- Implements custom NER without requiring machine learning training
- Features a modular architecture separating UI, processing logic, and utilities
- Applies tidy data principles to transform unstructured text into structured entity data
- Provides intuitive visualization of extracted entities
- Includes comprehensive sample texts demonstrating different entity types

**Files in this Project:**
- `streamlit_app.py` - Main Streamlit application entry point
- `app.py` - Core application logic handling the NER interface
- `ner_processor.py` - NER processing engine that performs entity extraction
- `utils.py` - Utility functions for text processing and visualization
- `main.py` - Alternative entry point
- `__init__.py` - Package initialization
- `sample_texts/` - Directory with sample texts for demonstration
- `.streamlit/` - Configuration directory for Streamlit settings
- `setup.sh` - Setup script for deployment environments
- `requirements.txt` - Python dependencies
- `packages.txt` - System-level package requirements
- `runtime.txt` - Python version specification
- `pyproject.toml` & `setup.py` - Package configuration files
- `MANIFEST.in` - Package manifest for distribution
- `.gitignore` - Git configuration for ignored files
- `README.md` - Project documentation with setup and usage instructions

**[View Project →](./NERStreamlitApp)**

## Complete Repository Structure
```
ETELLESCHAVES-Python-Portfolio/
├── README.md                     # Main portfolio documentation
├── .gitattributes                # Git attributes configuration
│
├── basic_streamlit_app/          # Headline Finder App
│   ├── main.py                   # Main Streamlit application
│   ├── all-data.csv              # Dataset with headlines
│   ├── requirements.txt          # Dependencies
│   └── README.md                 # Project documentation
│
├── StreamlitAppFinal/            # Portfolio Analyzer App
│   ├── run.py                    # Entry point
│   ├── src/                      # Core application code
│   │   └── ...                   # Various application modules
│   ├── utils/                    # Utility functions
│   │   └── ...                   # Helper modules and functions
│   ├── data/                     # Sample data and caches
│   │   └── ...                   # Data files
│   ├── requirements.txt          # Dependencies
│   └── README.md                 # Project documentation
│
├── TidyData_Project/             # R&D Spending Analysis
│   ├── tidy-data-project.py      # R&D spending analysis script
│   ├── fed_rd_year&gdp.csv       # Source data
│   ├── tidy_federal_rd_data.csv  # Transformed tidy dataset
│   ├── spending_over_time.png    # Generated visualization
│   ├── spending_percent_gdp.png  # Generated visualization
│   └── README.md                 # Project documentation
│
└── NERStreamlitApp/              # NER Application
    ├── streamlit_app.py          # Main Streamlit entry point
    ├── app.py                    # Core application logic
    ├── ner_processor.py          # NER processing logic
    ├── utils.py                  # Utility functions
    ├── main.py                   # Alternative entry point
    ├── __init__.py               # Package initialization
    ├── sample_texts/             # Sample text files
    │   └── ...                   # Various text samples
    ├── .streamlit/               # Streamlit configuration
    │   └── ...                   # Configuration files
    ├── requirements.txt          # Python dependencies
    ├── packages.txt              # System package requirements
    ├── setup.sh                  # Deployment setup script
    ├── runtime.txt               # Python version specification
    ├── pyproject.toml            # Project configuration
    ├── setup.py                  # Package setup script
    ├── MANIFEST.in               # Package manifest
    ├── .gitignore                # Git ignore configuration
    └── README.md                 # Project documentation
```

## Getting Started

### Running the Headline Finder App
```bash
cd basic_streamlit_app
pip install -r requirements.txt
streamlit run main.py
```

### Running the Portfolio Analyzer
```bash
cd StreamlitAppFinal
pip install -r requirements.txt
streamlit run run.py
```

### Running the R&D Analysis
```bash
cd TidyData_Project
python tidy-data-project.py
```

### Running the NER Application
```bash
cd NERStreamlitApp
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run streamlit_app.py
```

## Skills Demonstrated
- Data cleaning and transformation
- Statistical analysis
- Data visualization
- Interactive web application development
- Natural language processing
- Pattern-based entity recognition
- Financial analysis and backtesting
- Documentation
- Version control
- Object-oriented programming
- Modern Python development practices
- Package management and deployment configuration

# Project-Specific Documentation

## Named Entity Recognition (NER) Application

### Project Overview

This custom Named Entity Recognition (NER) application demonstrates the application of tidy data principles to natural language processing. By transforming unstructured text into structured data, the app allows users to extract and visualize meaningful entities without machine learning model training.

### Tidy Data Principles Applied

This project applies Hadley Wickham's tidy data principles to text analysis:

1. **Each variable forms a column**: Extracted entities are organized by their type (label), text value, and position.
2. **Each observation forms a row**: Each entity occurrence is treated as a distinct observation with its own attributes.
3. **Each type of observational unit forms a table**: Text content and entity definitions are stored in separate data structures.

The application transforms messy, unstructured text into a clean, structured format suitable for analysis—a core tenet of tidy data methodology.

### Features

- **Custom Entity Definition**: Define your own entity types through pattern matching
- **Text Processing**: Process text from direct input, file upload, or sample texts
- **Interactive Visualization**: Visualize recognized entities with color coding
- **Rule-based Recognition**: Utilize spaCy's EntityRuler for efficient pattern matching
- **Sample Texts**: Immediate testing with provided examples

### Technologies

- **Streamlit**: Web application framework
- **spaCy**: Natural language processing library
- **pandas**: Data manipulation
- **NLTK**: Natural language toolkit

### Setup Instructions

#### Prerequisites

- Python 3.8 or higher
- pip package manager

#### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ETELLESCHAVES-Python-Portfolio.git
   cd ETELLESCHAVES-Python-Portfolio/NERStreamlitApp
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the spaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

### Running the Application

1. Start the Streamlit application:
   ```bash
   streamlit run streamlit_app.py
   ```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

### Usage Guide

1. **Define Entities**: Navigate to the "Entity Definition" tab and create custom entity types
2. **Enter Text**: Input text directly, upload a file, or select a sample text
3. **Process**: Click "Process Text" to extract entities from the text
4. **View Results**: See highlighted entities and their distribution in the "Results" tab

### Dataset Details

The application includes several sample texts in the `sample_texts/` directory covering diverse domains:
- Technology articles
- Business news
- Scientific papers
- General content

These samples demonstrate the application's versatility across different text types and entity extraction needs.

## References

- Wickham, H. (2014). "Tidy Data." Journal of Statistical Software, 59(10).
- Honnibal, M., & Montani, I. (2017). "spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing."
- Streamlit documentation: https://docs.streamlit.io/

## License

MIT License


