{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyP6oP36rOqBeo2dNbHf4vMs"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "3yALMbeNyZ3N"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "import pickle\n",
        "import pandas as pd\n",
        "\n",
        "import requests\n",
        "\n",
        "def fetch_posters(movie_id):\n",
        "    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=06c88b624faad94a0bcb2e9b59538063'.format(movie_id))\n",
        "    data=response.json()\n",
        "    print(data)\n",
        "    if 'poster_path' in data and data['poster_path']:\n",
        "        return \"https://image.tmdb.org/t/p/original\" + data['poster_path']\n",
        "    else:\n",
        "        return \"https://via.placeholder.com/500x750?text=No+Poster\"\n",
        "\n",
        "\n",
        "# Load data\n",
        "movies = pickle.load(open('movies.pkl', 'rb'))  # DataFrame\n",
        "similarity = pickle.load(open('similarity.pkl', 'rb'))  # similarity matrix\n",
        "\n",
        "def recommend(movie):\n",
        "    movie_index = movies[movies['title'] == movie].index[0]\n",
        "    distances = similarity[movie_index]\n",
        "    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]\n",
        "\n",
        "    recommended_movies = []\n",
        "    recommended_movie_posters = []\n",
        "    for i in movies_list:\n",
        "        movie_id = movies.iloc[i[0]].movie_id   # ✅ must use actual TMDB ID column\n",
        "        recommended_movies.append(movies.iloc[i[0]].title)\n",
        "        recommended_movie_posters.append(fetch_posters(movie_id))\n",
        "    return recommended_movies, recommended_movie_posters\n",
        "\n",
        "\n",
        "st.title('Movie Recommender System')\n",
        "\n",
        "selected_movie_name = st.selectbox(\n",
        "    'What do you want to watch?',\n",
        "    movies['title'].values\n",
        ")\n",
        "\n",
        "if st.button('Recommend'):\n",
        "    recommended_movies, recommended_movie_posters = recommend(selected_movie_name)\n",
        "    cols = st.columns(5)  # create 5 columns\n",
        "\n",
        "    for idx, col in enumerate(cols):\n",
        "        with col:\n",
        "            st.text(recommended_movies[idx])\n",
        "            st.image(recommended_movie_posters[idx])\n"
      ]
    }
  ]
}