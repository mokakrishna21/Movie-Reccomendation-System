import streamlit as st
import pandas as pd
import numpy as np

# Sample movie data (replace this with your data loading logic)
data = {
    'title': ['Movie 1', 'Movie 2', 'Movie 3', 'Movie 4', 'Movie 5'],
    'overview': ['Overview 1', 'Overview 2', 'Overview 3', 'Overview 4', 'Overview 5'],
    'release_date': ['2021-01-01', '2022-02-02', '2023-03-03', '2024-04-04', '2025-05-05'],
    'vote_average': [7.5, 8.0, 6.5, 7.0, 8.5],
    'vote_count': [100, 200, 150, 180, 250],
    'genres': [['Action', 'Adventure'], ['Comedy', 'Drama'], ['Sci-Fi'], ['Horror'], ['Drama', 'Romance']]
}

movies = pd.DataFrame(data)

# Streamlit app
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

    # Dummy recommendations (replace with your recommendation logic)
    recommended_movies = np.random.choice(movies['title'], num_recommendations, replace=False)
    
    st.subheader("Recommended Movies:")
    cols = st.columns(5)
    for col, movie_title in zip(cols, recommended_movies):
        with col:
            st.write(f"**{movie_title}**")  # Display recommended movie titles

    st.subheader("Movie Details:")
    selected_movie_data = movies[movies['title'] == selected_movie].iloc[0]
    st.write(f"**Title:** {selected_movie_data['title']}")
    st.write(f"**Overview:** {selected_movie_data['overview']}")
    st.write(f"**Release Date:** {selected_movie_data['release_date']}")
    st.write(f"**Average Vote:** {selected_movie_data['vote_average']}")
    st.write(f"**Vote Count:** {selected_movie_data['vote_count']}")
    st.write(f"**Genres:** {', '.join(selected_movie_data['genres'])}")

    st.subheader("Cast:")
    # Dummy cast information (replace with your data)
    cast_info = ['Actor 1 as Character 1', 'Actor 2 as Character 2', 'Actor 3 as Character 3']
    for cast in cast_info:
        st.write(f"- {cast}")
