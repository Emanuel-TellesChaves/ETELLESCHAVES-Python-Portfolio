import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px  # For the pie chart

@st.cache_data
def load_data():
   

    df = pd.read_csv("all-data.csv", sep=None, engine='python', header=None,
                     names=["label", "headline"], encoding="latin-1")

    df['headline'] = df['headline'].fillna("").astype(str)
    return df

@st.cache_data
def vectorize_headlines(headlines):
 
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(headlines)
    return vectorizer, vectors

def main():
    st.title("Headline Finder with Sentiment Analysis")
    st.write("Enter a phrase below and the app will find matching headlines from the corpus.")

    
    df = load_data()
    

    st.sidebar.header("Filters")
    

    sentiment_filter = st.sidebar.selectbox(
        "Filter by Sentiment",
        options=["All", "positive", "neutral", "negative"]
    )
    
    
    similarity_threshold = st.sidebar.slider(
        "Minimum Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01
    )
    
 
    if sentiment_filter != "All":
        df = df[df["label"].str.lower() == sentiment_filter.lower()]
        if df.empty:
            st.error("No headlines with the selected sentiment found.")
            return

    st.write("Data preview:", df.head())
    

    vectorizer, headline_vectors = vectorize_headlines(df['headline'])
    

    user_input = st.text_input("Enter a phrase:")


    tab1, tab2 = st.tabs(["Closest Headline", "Sentiment Analysis using 100 closest headlines"])
    
    if user_input:

        user_vector = vectorizer.transform([user_input])
        similarities = cosine_similarity(user_vector, headline_vectors)
        similarities_array = similarities.flatten()
        
    
        best_similarity = np.max(similarities_array)
        
      
        with tab1:
            if best_similarity < similarity_threshold:
                st.warning("No headline found with similarity above the threshold.")
            else:
                best_idx = np.argmax(similarities_array)
                best_headline = df.iloc[best_idx]["headline"]
                best_label = df.iloc[best_idx]["label"]
                
                st.subheader("Closest Headline")
                st.write(best_headline)
                st.subheader("Sentiment")
                st.write(best_label)
                st.write(f"**Cosine Similarity:** {best_similarity:.2f}")
        
   
        with tab2:
            if best_similarity < similarity_threshold:
                st.warning("No headline found with similarity above the threshold.")
            else:
             
                sorted_indices = np.argsort(similarities_array)[::-1]
                top_n = min(100, len(sorted_indices))
                top_indices = sorted_indices[:top_n]
                
              
                top_df = df.iloc[top_indices].copy()
                top_df["similarity"] = similarities_array[top_indices]
                
              
                sentiment_scores = top_df.groupby("label")["similarity"].sum()
                total_score = sentiment_scores.sum()
                
          
                sentiment_percentages = (sentiment_scores / total_score * 100).reset_index()
                sentiment_percentages.columns = ["Sentiment", "Percentage"]
                
                st.subheader("Weighted Sentiment Distribution (Top 100 Headlines)")
                st.write(sentiment_percentages)
                
               
                fig = px.pie(sentiment_percentages, values='Percentage', names='Sentiment',
                             title="Weighted Sentiment Distribution",
                             color="Sentiment",
                             color_discrete_map={"positive": "green", "neutral": "gray", "negative": "red"})
                st.plotly_chart(fig, use_container_width=True)
    

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

if __name__ == '__main__':
    main()


