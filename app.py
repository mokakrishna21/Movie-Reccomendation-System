import pickle
import streamlit as st
import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from tmdbv3api import TMDb, Movie
import pprint

# Load movie data and perform necessary setup
movies = pickle.load(open('movie_list.pkl', 'rb'))
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(movies['tags']).toarray()
similarity = cosine_similarity(vector)

tmdb = TMDb()
tmdb.api_key = "c6ac6f6b45fdf5951c59c02520f63b5c"

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c6ac6f6b45fdf5951c59c02520f63b5c&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to fetch movie details
def fetch_movie_details(movie_id):
    movie_api = Movie()
    movie_details = movie_api.details(movie_id)
    return movie_details

# Function to extract cast information
def get_cast_info(movie_details):
    cast_info = []
    if 'credits' in movie_details:
        cast_list = movie_details['credits']['cast']
        for cast_member in cast_list[:5]:
            cast_name = cast_member.get('name', 'N/A')
            character_name = cast_member.get('character', 'N/A')
            cast_info.append(f"{cast_name} as {character_name}")
    return cast_info

# Function to recommend movies
def recommend(movie, num_recommendations=10):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:num_recommendations + 1]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append((movies.iloc[i[0]].title, fetch_poster(movie_id), movie_id))

    return recommended_movies

# Streamlit app UI
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
            expander = st.expander(movie_name)
            movie_details = fetch_movie_details(movie_id)
            st.markdown(f"<h2><b>{movie_name}</b></h2>", unsafe_allow_html=True)
            st.write("Overview:", movie_details.get('overview', 'N/A'))
            st.write("Release Date:", movie_details.get('release_date', 'N/A'))
            st.write("Average Vote:", movie_details.get('vote_average', 'N/A'))
            st.write("Vote Count:", movie_details.get('vote_count', 'N/A'))
            st.write("Genres:", ", ".join([genre['name'] for genre in movie_details.get('genres', [])]))
            
            # Print the structure of movie_details to inspect it
            st.write("Movie Details Structure:")
            pprint.pprint(movie_details)
            
            cast_info = get_cast_info(movie_details)
            if cast_info:
                st.write("Cast:")
                for cast in cast_info:
                    st.write(f"- {cast}")
            else:
                st.write("Cast information not available.")
