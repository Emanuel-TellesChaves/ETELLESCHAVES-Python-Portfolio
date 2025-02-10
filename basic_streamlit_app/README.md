 # Headline Finder with Sentiment Analysis

This project is a simple Streamlit application that takes a user-inputted phrase and finds the closest matching headline from a provided dataset. In addition, it performs a sentiment analysis on the 100 closest headlines by weighting each headline's sentiment based on its cosine similarity score, and displays the result as a pie chart.

## Features

- **Closest Headline Search:**  
  Enter a phrase and the app will display the headline that is most similar to your input using TF-IDF vectorization and cosine similarity. It also shows the sentiment (positive, neutral, or negative) and the cosine similarity score of that headline.

- **Weighted Sentiment Analysis (100 Closest Headlines):**  
  The app analyzes the top 100 headlines closest to your input. It weights the sentiment (positive, neutral, or negative) of each headline by its cosine similarity score, calculates the percentage contribution of each sentiment, and displays the results as a pie chart.

- **Interactive Filters:**  
  Use sidebar filters to narrow down the search by sentiment and to set a minimum cosine similarity threshold.

## Installation

Before running the app, make sure you have Python installed. Then, install the necessary packages using pip:

```bash
pip install streamlit
pip install plotly
pip install scikit-learn
