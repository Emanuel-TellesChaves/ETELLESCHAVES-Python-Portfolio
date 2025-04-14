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

### 1. Basic Streamlit Application
An interactive web application built with Streamlit that analyzes and visualizes student performance data.

**Key Features:**
- Interactive data filtering and visualization
- Statistical analysis of student performance
- Dynamic charts and graphs
- User-friendly interface for data exploration

**Technologies:**
- Streamlit
- Pandas
- Plotly
- Scikit-learn

### 2. Federal R&D Spending Analysis
A comprehensive analysis of U.S. Federal Research & Development spending patterns from 1976 to 2017.

**Key Features:**
- Data transformation using tidy data principles
- Time series analysis of spending patterns
- Department-wise comparative analysis
- GDP-relative spending trends
- Advanced data visualization

**Technologies:**
- Pandas
- Matplotlib
- Seaborn
- NumPy

### 3. Custom Named Entity Recognition (NER) Application
A Streamlit-based application for custom Named Entity Recognition that allows users to define and visualize their own entity types without model training.

**Key Features:**
- Custom entity definition through pattern matching
- Text processing from direct input or file upload
- Interactive visualization of recognized entities
- Rule-based entity recognition using spaCy's EntityRuler
- Sample texts for immediate testing

**Technologies:**
- Streamlit
- spaCy
- pandas
- NLTK

## Repository Structure
```
ETELLESCHAVES-Python-Portfolio/
├── basic_streamlit_app/
│   ├── app.py                  # Main Streamlit application
│   └── requirements.txt        # Dependencies
├── TidyData_Project/
│   ├── tidy-data-project.py    # R&D spending analysis
│   ├── fed_rd_year&gdp.csv     # Source data
│   └── README.md               # Project documentation
└── NERStreamlitApp/
    ├── app.py                  # Main NER application
    ├── ner_processor.py        # NER processing logic
    ├── utils.py                # Utility functions
    ├── sample_texts/           # Sample text files
    ├── requirements.txt        # Dependencies
    └── README.md               # Project documentation
```

## Getting Started

### Running the Streamlit App
```bash
cd basic_streamlit_app
pip install -r requirements.txt
streamlit run app.py
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
streamlit run app.py
```

## Skills Demonstrated
- Data cleaning and transformation
- Statistical analysis
- Data visualization
- Interactive web application development
- Natural language processing
- Pattern-based entity recognition
- Documentation
- Version control


