import pickle
import streamlit as st
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from tmdbv3api import TMDb, Movie

# Load movie data from pickle file
movies = pickle.load(open('movie_list.pkl', 'rb'))

# Initialize TMDb API
tmdb = TMDb()
tmdb.api_key = "c6ac6f6b45fdf5951c59c02520f63b5c"

# CountVectorizer for calculating cosine similarity
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(movies['tags']).toarray()
similarity = cosine_similarity(vector)

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c6ac6f6b45fdf5951c59c02520f63b5c&language=en-US"
        data = requests.get(url)
        data = data.json()
        if 'poster_path' in data:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return None
    except Exception as e:
        st.error("Error fetching poster.")
        return None

def fetch_movie_details(movie_id):
    try:
        movie_api = Movie()
        movie_details = movie_api.details(movie_id)
        return movie_details
    except Exception as e:
        st.error("Error fetching movie details.")
        return None

def recommend(movie, num_recommendations=10):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies = []
        for i in distances[1:num_recommendations + 1]:
            movie_id = movies.iloc[i[0]]['movie_id']
            recommended_movies.append((movie_id, fetch_poster(movie_id)))

        return recommended_movies
    except Exception as e:
        st.error("Error generating recommendations.")
        return []

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
    for movie_id, movie_poster in recommended_movies:
        col1, col2 = st.columns([1, 3])
        with col1:
            if movie_poster:
                st.image(movie_poster, use_container_width=True)  # Fixed parameter here
            else:
                st.write("Poster not available")

        with col2:
            movie_details = fetch_movie_details(movie_id)
            if movie_details:
                st.markdown(f"<h2><b>{movie_details.title}</b></h2>", unsafe_allow_html=True)
                st.write("Overview:", movie_details.overview)
                st.write("Release Date:", movie_details.release_date)
                st.write("Average Vote:", movie_details.vote_average)
                st.write("Vote Count:", movie_details.vote_count)
                st.write("Genres:", ", ".join([genre.name for genre in movie_details.genres]))
            else:
                st.write("Movie details not available.")
