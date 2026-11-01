import os
import streamlit as st
import pandas as pd
import pickle
import requests
import time

session = requests.Session()

def get_tmdb_api_key():
    """Reads the TMDB API key from Streamlit secrets, falling back to an environment variable."""
    try:
        return st.secrets["TMDB_API_KEY"]
    except (KeyError, FileNotFoundError):
        return os.getenv("TMDB_API_KEY")

TMDB_API_KEY = get_tmdb_api_key()

def fetch_posters(movie_id):
    """Fetches the movie poster URL from the TMDB API with a robust retry mechanism."""
    retries = 3
    delay = 0.5
    for i in range(retries):
        try:
            response = session.get(
                f'https://api.themoviedb.org/3/movie/{movie_id}',
                params={'api_key': TMDB_API_KEY, 'language': 'en-US'},
                timeout=5
            )
            
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 2))
                st.warning(f"Rate limited by API. Waiting for {retry_after} seconds...")
                time.sleep(retry_after)
                continue 
            
            data = response.json()
            poster_path = data.get('poster_path')
            
            if poster_path:
                return 'https://image.tmdb.org/t/p/w500/' + poster_path
            else:
                return 'https://placehold.co/500x750/333/FFF?text=No+Poster'
                
        except requests.exceptions.RequestException as e:
            print(f"API request failed (attempt {i+1}/{retries}): {e}")
            time.sleep(delay * (i + 1)) 
    return 'https://placehold.co/500x750/333/FFF?text=API+Error'


def recommend(movie):
    """Recommends movies based on the selected movie."""
    recommended = []
    recommended_posters = []
    try:
        movie_index = movies[movies['original_title'] == movie].index[0]
        
        distances = similarity[movie_index]
        movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:11]

        for i in movies_list:
            if len(recommended) >= 6:
                break
            
            movie_id = movies.iloc[i[0]].id 
            recommended.append(movies.iloc[i[0]].original_title)
            recommended_posters.append(fetch_posters(movie_id))
            time.sleep(0.1) 
            
    except IndexError:
        st.error(f"Error: Movie '{movie}' not found in the dataset. Please try another popular movie.")
        return [], []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return [], []
        
    return recommended, recommended_posters

try:
    with open('movies.pkl', 'rb') as f:
        movies_list = pickle.load(f)
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
    # Row positions must match the similarity matrix; the pickled frame keeps gappy labels from dropna
    movies = pd.DataFrame(movies_list).reset_index(drop=True)
except FileNotFoundError:
    st.error("Error: The 'movies.pkl' or 'similarity.pkl' file was not found.")
    st.stop()

st.title('Movie Recommender System')

if not TMDB_API_KEY:
    st.warning("TMDB_API_KEY is not set, so posters will not load. Add it to .streamlit/secrets.toml or the environment.")

movie_titles = movies['original_title'].values
selected_movie = st.selectbox('Select a Movie to get Recommendation', movie_titles)

if st.button("Recommend Movies"):
    with st.spinner('Finding recommendations and fetching posters...'):
        names, posters = recommend(selected_movie)
    
    if names and posters:
        cols = st.columns(6)
        for i in range(min(6, len(names))):
            with cols[i]:
                st.image(posters[i])
                st.caption(names[i])

