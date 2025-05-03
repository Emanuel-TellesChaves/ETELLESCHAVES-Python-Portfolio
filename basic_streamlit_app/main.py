import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px  # For the pie chart

# Cache the data loading function to improve app performance
@st.cache_data
def load_data():
    """
    Load and preprocess the headline dataset.
    
    Returns:
        pandas.DataFrame: DataFrame containing sentiment labels and headlines
    """
    # Load CSV with flexible separator detection and proper column naming
    df = pd.read_csv("all-data.csv", sep=None, engine='python', header=None,
                     names=["label", "headline"], encoding="latin-1")

    # Clean the headline column by filling NA values and ensuring string type
    df['headline'] = df['headline'].fillna("").astype(str)
    return df

# Cache the vectorization process to improve performance
@st.cache_data
def vectorize_headlines(headlines):
    """
    Convert headlines to TF-IDF vectors for similarity comparison.
    
    Args:
        headlines (pandas.Series): Series of headline texts
        
    Returns:
        tuple: (TfidfVectorizer, sparse matrix of TF-IDF vectors)
    """
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(headlines)
    return vectorizer, vectors

def main():
    """
    Main function that runs the Streamlit application.
    """
    # Set up the app title and introduction
    st.title("Headline Finder with Sentiment Analysis")
    st.write("Enter a phrase below and the app will find matching headlines from the corpus.")

    # Load the dataset
    df = load_data()
    
    # Create sidebar filters for user interaction
    st.sidebar.header("Filters")
    
    # Sentiment filter dropdown
    sentiment_filter = st.sidebar.selectbox(
        "Filter by Sentiment",
        options=["All", "positive", "neutral", "negative"]
    )
    
    # Similarity threshold slider
    similarity_threshold = st.sidebar.slider(
        "Minimum Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01
    )
    
    # Apply sentiment filter if selected
    if sentiment_filter != "All":
        df = df[df["label"].str.lower() == sentiment_filter.lower()]
        if df.empty:
            st.error("No headlines with the selected sentiment found.")
            return

    # Show data preview to user
    st.write("Data preview:", df.head())
    
    # Vectorize headlines for similarity comparison
    vectorizer, headline_vectors = vectorize_headlines(df['headline'])
    
    # Get user input for phrase to search
    user_input = st.text_input("Enter a phrase:")

    # Create tabs for different analysis views
    tab1, tab2 = st.tabs(["Closest Headline", "Sentiment Analysis using 100 closest headlines"])
    
    # Process user input if provided
    if user_input:
        # Convert user input to vector and calculate similarity with all headlines
        user_vector = vectorizer.transform([user_input])
        similarities = cosine_similarity(user_vector, headline_vectors)
        similarities_array = similarities.flatten()
        
        # Find the highest similarity score
        best_similarity = np.max(similarities_array)
        
        # TAB 1: Show the closest headline
        with tab1:
            if best_similarity < similarity_threshold:
                st.warning("No headline found with similarity above the threshold.")
            else:
                # Get the index of the best match
                best_idx = np.argmax(similarities_array)
                best_headline = df.iloc[best_idx]["headline"]
                best_label = df.iloc[best_idx]["label"]
                
                # Display results
                st.subheader("Closest Headline")
                st.write(best_headline)
                st.subheader("Sentiment")
                st.write(best_label)
                st.write(f"**Cosine Similarity:** {best_similarity:.2f}")
        
        # TAB 2: Show sentiment analysis for top 100 headlines
        with tab2:
            if best_similarity < similarity_threshold:
                st.warning("No headline found with similarity above the threshold.")
            else:
                # Get top 100 headlines by similarity
                sorted_indices = np.argsort(similarities_array)[::-1]
                top_n = min(100, len(sorted_indices))
                top_indices = sorted_indices[:top_n]
                
                # Create dataframe with top matches
                top_df = df.iloc[top_indices].copy()
                top_df["similarity"] = similarities_array[top_indices]
                
                # Calculate weighted sentiment scores based on similarity
                sentiment_scores = top_df.groupby("label")["similarity"].sum()
                total_score = sentiment_scores.sum()
                
                # Calculate percentage contribution of each sentiment
                sentiment_percentages = (sentiment_scores / total_score * 100).reset_index()
                sentiment_percentages.columns = ["Sentiment", "Percentage"]
                
                # Display tabular results
                st.subheader("Weighted Sentiment Distribution (Top 100 Headlines)")
                st.write(sentiment_percentages)
                
                # Create pie chart visualization
                fig = px.pie(sentiment_percentages, values='Percentage', names='Sentiment',
                             title="Weighted Sentiment Distribution",
                             color="Sentiment",
                             color_discrete_map={"positive": "green", "neutral": "gray", "negative": "red"})
                st.plotly_chart(fig, use_container_width=True)
    
    # Add detailed instructions and explanation section
    st.markdown("---")
    st.markdown("#### Instructions & Explanation")
    st.write("**Instructions:**")
    st.write("1. Use the sidebar to filter headlines by sentiment (for the closest headline) and to set a minimum similarity threshold.")
    st.write("2. Enter a phrase in the text input box above.")
    st.write("3. In the **Closest Headline** tab, you'll see the single best matching headline along with its sentiment and cosine similarity score.")
    st.write("4. In the **Sentiment Analysis using 100 closest headlines** tab, the top 100 headlines (by cosine similarity) are analyzed. "
             "Each headline's cosine similarity is used as a weight to calculate what percentage of the total similarity score "
             "corresponds to each sentiment (positive, neutral, negative). The result is displayed as a pie chart.")
    
    st.write("**Explanation:**")
    st.write("This app uses TF-IDF (Term Frequency-Inverse Document Frequency) to convert headlines into numerical vectors and "
             "cosine similarity to compare your input phrase with each headline. The weighted sentiment analysis uses the cosine "
             "similarity scores of the top 100 matching headlines to estimate which sentiment dominates. This weighted analysis "
             "is then visualized as a pie chart.")

# Entry point of the application
if __name__ == '__main__':
    main()


