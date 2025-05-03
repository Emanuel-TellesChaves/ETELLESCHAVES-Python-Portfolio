# Headline Finder with Sentiment Analysis

## Project Overview

This Streamlit application demonstrates the principles of tidy data and natural language processing to analyze news headlines. It allows users to enter a phrase and find the closest matching headline from a dataset, while also performing sentiment analysis on the top 100 closest matching headlines.

The project follows tidy data principles by:
1. Ensuring each variable forms a column (sentiment and headline text)
2. Each observation forms a row (one headline per row)
3. Each type of observational unit forms a table (the headlines dataset)

The application demonstrates how properly structured data can be effectively analyzed and visualized to extract meaningful insights through natural language processing techniques.

## Features

- **Closest Headline Search:**  
  Enter a phrase and the app will display the headline that is most similar to your input using TF-IDF vectorization and cosine similarity. It also shows the sentiment (positive, neutral, or negative) and the cosine similarity score of that headline.

- **Weighted Sentiment Analysis (100 Closest Headlines):**  
  The app analyzes the top 100 headlines closest to your input. It weights the sentiment (positive, neutral, or negative) of each headline by its cosine similarity score, calculates the percentage contribution of each sentiment, and displays the results as a pie chart.

- **Interactive Filters:**  
  Use sidebar filters to narrow down the search by sentiment and to set a minimum cosine similarity threshold.

## Dataset Details

The application uses a dataset (`all-data.csv`) containing news headlines with sentiment labels:

- **Format**: CSV file with two columns
- **Columns**:
  - `label`: The sentiment classification (positive, neutral, or negative)
  - `headline`: The news headline text
- **Size**: ~4800 labeled headlines
- **Source**: This dataset combines news headlines from various sources with sentiment labels generated using NLTK's VADER sentiment analyzer

The data has been preprocessed to ensure consistency and cleanliness, following tidy data principles to make analysis straightforward.

## Installation and Setup

Before running the app, make sure you have Python 3.6+ installed. Then, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ETELLESCHAVES-Python-Portfolio.git
   cd ETELLESCHAVES-Python-Portfolio/basic_streamlit_app
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install these packages individually:
   ```bash
   pip install streamlit pandas numpy scikit-learn plotly
   ```

4. Run the application:
   ```bash
   streamlit run main.py
   ```

5. The application will open in your default web browser at `http://localhost:8501`.

## Usage Guide

1. When the app loads, you'll see a text input field where you can enter your phrase.
2. Use the sidebar to:
   - Filter headlines by sentiment (positive, neutral, negative, or all)
   - Set a minimum similarity threshold to control quality of matches
3. After entering your phrase, the app will display:
   - The closest matching headline with its sentiment and similarity score
   - A pie chart showing the weighted sentiment distribution of the top 100 matching headlines
4. Experiment with different phrases and filters to explore the dataset.

## Implementation Details

The application uses several key NLP and data analysis techniques:

- **TF-IDF Vectorization**: Converts text into numerical vectors based on term frequency and inverse document frequency
- **Cosine Similarity**: Measures the similarity between vectors, regardless of their magnitude
- **Weighted Sentiment Analysis**: Uses similarity scores as weights to provide a more nuanced analysis of sentiment distribution
- **Data Visualization**: Visualizes complex analysis results as an intuitive pie chart

## References

- Streamlit Documentation: [https://docs.streamlit.io/](https://docs.streamlit.io/)
- scikit-learn Documentation: [https://scikit-learn.org/stable/documentation.html](https://scikit-learn.org/stable/documentation.html)
- TF-IDF Vectorization: [https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- Cosine Similarity: [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
- Plotly Documentation: [https://plotly.com/python/](https://plotly.com/python/)
- Tidy Data Principles: Wickham, H. (2014). Tidy Data. Journal of Statistical Software, 59(10), 1–23. [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10)
