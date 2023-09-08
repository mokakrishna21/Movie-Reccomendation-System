import pickle
import streamlit as st
import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from tmdbv3api import TMDb, Movie

# ... (previous code remains unchanged)

st.set_page_config(
    page_title="Poppy's Movie Recommender",
    page_icon=":movie_camera:",
    layout="wide",
)

st.title("Poppy's Movie Recommender")

st.sidebar.header("Settings")
selected_movie = st.sidebar.selectbox("Select a movie:", movies['title'].values)
num_recommendations = st.sidebar.slider("Number of Recommendations", min_value=1, max_value=20, value=5)

if st.sidebar.button('Show Recommendations'):
    st.sidebar.info("Fetching recommendations...")

    recommended_movies = recommend(selected_movie, num_recommendations)
    
    st.subheader("Recommended Movies:")
    cols = st.columns(5)  # Use st.columns instead of st.beta_columns
    for col, (movie_id, movie_poster) in zip(cols, recommended_movies):
        with col:
            st.image(movie_poster, use_column_width=True)

    st.subheader("Movie Details:")
    movie_details = fetch_movie_details(recommended_movies[0][0])
    if movie_details:
        st.write(f"**Title:** {movie_details.title}")
        st.write(f"**Overview:** {movie_details.overview}")
        st.write(f"**Release Date:** {movie_details.release_date}")
        st.write(f"**Average Vote:** {movie_details.vote_average}")
        st.write(f"**Vote Count:** {movie_details.vote_count}")
        st.write(f"**Genres:** {', '.join([genre.name for genre in movie_details.genres])}")

        cast_info = fetch_cast_info(recommended_movies[0][0])
        st.subheader("Cast:")
        for i, cast in enumerate(cast_info[:5]):
            st.write(f"- {cast['name']} as {cast['character']}")
    else:
        st.warning("Movie details not available.")
