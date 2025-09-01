import streamlit as st
import pickle
import pandas as pd

import requests

def fetch_posters(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=06c88b624faad94a0bcb2e9b59538063'.format(movie_id))
    data=response.json()
    print(data)
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/original" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"


# Load data
movies = pickle.load(open('movies.pkl', 'rb'))  # DataFrame
similarity = pickle.load(open('similarity.pkl', 'rb'))  # similarity matrix

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id   # ✅ must use actual TMDB ID column
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_posters(movie_id))
    return recommended_movies, recommended_movie_posters


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'What do you want to watch?',
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movies, recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(5)  # create 5 columns

    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movies[idx])
            st.image(recommended_movie_posters[idx])
