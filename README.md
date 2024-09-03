## Poppy's Recommender System

Poppy's Recommender System is a web-based movie recommendation application that helps users discover movies similar to their favorite ones. Built using Streamlit and leveraging machine learning techniques like cosine similarity, this application provides users with personalized movie recommendations.
<br>
https://poppy-movie-reccomendation-system.streamlit.app

## Features

- **Movie Recommendation**: Select a movie from the dropdown list and receive similar movie recommendations.
- **Movie Posters**: Displays posters of the recommended movies alongside their details.
- **Movie Details**: Provides information such as the title, overview, release date, genres, and ratings of the recommended movies.

## Setup

### Prerequisites

- Python 3.x
- Streamlit
- TMDb API

### Installation

1. **Install Required Packages**:

    ```bash
    pip install streamlit requests scikit-learn tmdbv3api
    ```

2. **Set Up Environment Variables**:

    Create a `.env` file in the project directory with your TMDb API key:

    ```env
    TMDB_API_KEY=your_tmdb_api_key
    ```

### Running the Application

1. **Start the Streamlit App**:

    ```bash
    streamlit run app.py
    ```

2. **Access the App**:

    Open a web browser and navigate to `http://localhost:8501` to interact with Poppy's Recommender System.

## Customization

- **Update Movie Data**: Modify the `movie_list.pkl` file with your own movie titles and tags.
- **Change TMDb API Key**: Update the `.env` file with a new TMDb API key if needed.

## Troubleshooting

- Ensure the `.env` file contains the correct TMDb API key.
- Check your internet connection if you experience issues with fetching movie details or posters.

## Contact

For questions or suggestions, please reach out to [mokakrishna212@gmail.com].
