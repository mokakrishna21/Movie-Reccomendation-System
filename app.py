import pickle
import streamlit as st
import requests
from tmdbv3api import TMDb, Movie

# Load movie data from your movie_list.pkl
with open('movie_list.pkl', 'rb') as file:
    movies = pickle.load(file)

# Initialize TMDb API
tmdb = TMDb()
tmdb.api_key = "c6ac6f6b45fdf5951c59c02520f63b5c"

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c6ac6f6b45fdf5951c59c02520f63b5c&language=en-US"
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
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
        cv = CountVectorizer(max_features=5000, stop_words='english')
        vector = cv.fit_transform(movies['tags']).toarray()
        similarity = cosine_similarity(vector)
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies = []
        for i in distances[1:num_recommendations + 1]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append((movies.iloc[i[0]].title, fetch_poster(movie_id), movie_id))
        return recommended_movies
    except Exception as e:
        st.error("Error generating recommendations.")
        return []

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
    
    if recommended_movies:
        st.subheader("Recommended Movies:")
        cols = st.columns(5)
        for col, (movie_name, movie_poster, movie_id) in zip(cols, recommended_movies):
            with col:
                st.image(movie_poster, use_column_width=True)
        
        st.subheader("Movie Details:")
        movie_details = fetch_movie_details(recommended_movies[0][2])
        if movie_details:
            st.write(f"**Title:** {movie_details.title}")
            st.write(f"**Overview:** {movie_details.overview}")
            st.write(f"**Release Date:** {movie_details.release_date}")
            st.write(f"**Average Vote:** {movie_details.vote_average}")
            st.write(f"**Vote Count:** {movie_details.vote_count}")
            st.write(f"**Genres:** {', '.join([genre.name for genre in movie_details.genres])}")
            
            cast_info = movie_details.casts['cast'][:5]
            st.subheader("Cast:")
            for cast in cast_info:
                st.write(f"- {cast['name']} as {cast['character']}")
        else:
            st.warning("Movie details not available.")
    else:
        st.warning("No recommendations found.")
