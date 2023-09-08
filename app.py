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

def recommend(movie, num_recommendations=10):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:num_recommendations + 1]:
        movie_name = movies.iloc[i[0]]['title']
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies.append((movie_name, fetch_poster(movie_id), movie_id))

    return recommended_movies

st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="font-size: 48px;">Poppy's Recommender System</h1>
    </div>
    """,
    unsafe_allow_html=True
)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movies = recommend(selected_movie, num_recommendations=5)
    for movie_name, movie_poster, movie_id in recommended_movies:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(movie_poster, use_column_width=True)

        with col2:
            st.write("Movie Title:", movie_name)
            st.write("Movie ID:", movie_id)

            # Display the movie title in bigger and bold text
            st.markdown(f"<h2><b>{movie_name}</b></h2>", unsafe_allow_html=True)
            st.write("Overview:", movie_details.overview)
            st.write("Release Date:", movie_details.release_date)
            st.write("Average Vote:", movie_details.vote_average)
            st.write("Vote Count:", movie_details.vote_count)
            st.write("Genres:", ", ".join([genre.name for genre in movie_details.genres]))
            st.write("Cast:")
            cast_info = movie_details.casts.get('cast', [])
            if cast_info:
                for cast in cast_info[:5]:
                    st.write(f"- {cast['name']} as {cast['character']}")
            else:
                st.write("Cast information not available.")
