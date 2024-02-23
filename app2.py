import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path


def recommend(movie, num_recommendations):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    
    # Uwzględnienie wybranej liczby rekomendacji
    for i in distances[1:num_recommendations+1]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


st.header('Movie Recommender System Using Machine Learning')

movies = pickle.load(open('a/movie_list.pkl', 'rb'))
similarity = pickle.load(open('a/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

num_recommendations = st.slider("Select the number of recommendations", 1, 20, 5)

if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie, num_recommendations)
    
    # Ustawienie rekomendacji w jednym wierszu po 5
    rows = num_recommendations // 5 + (num_recommendations % 5 > 0)
    
    for row in range(rows):
        cols = st.columns(min(5, num_recommendations - row * 5))
        for col, (movie_name, movie_poster) in zip(cols, zip(recommended_movie_names[row * 5:],
                                                             recommended_movie_posters[row * 5:])):
            with col:
                st.text(movie_name)
                st.image(movie_poster)

