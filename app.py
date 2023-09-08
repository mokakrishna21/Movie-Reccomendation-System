import pickle
import streamlit as st
import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from tmdbv3api import TMDb, Movie

movies = pickle.load(open('movie_list.pkl', 'rb'))
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(movies['tags']).toarray()
similarity = cosine_similarity(vector)

tmdb = TMDb()
tmdb.api_key = "c6ac6f6b45fdf5951c59c02520f63b5c"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c6ac6f6b45fdf5951c59c02520f63b5c&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def fetch_cast_info(movie_id):
    movie_api = Movie()
    credits = movie_api.credits(movie_id)
    cast = credits['cast']
    return cast

def recommend(movie, num_recommendations=10):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:num_recommendations + 1]:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies.append((movie_id, fetch_poster(movie_id)))
    return recommended_movies

def fetch_movie_details(movie_id):
    movie_api = Movie()
    movie_details = movie_api.details(movie_id)
    return movie_details

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
    row = st.beta_columns(5)
    for movie_id, movie_poster in recommended_movies:
        with row.pop():
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
