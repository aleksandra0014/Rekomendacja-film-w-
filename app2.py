import pickle
import streamlit as st
import requests
import pandas as pd


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path


def recommend(movie, num_rec):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    
    # Uwzględnienie wybranej liczby rekomendacji
    for i in distances[1:num_rec+1]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


def actor(name):
    movies = []
    for j in range(0, len(data2)):
        if name in data2['cast'][j]:
            movies.append(data2[['title', 'popularity', 'movie_id']].iloc[j].tolist())
    movies_sorted = sorted(movies, reverse=True, key=lambda x: x[1])
    title = []
    popularity = []
    ids = []
    for i in movies_sorted[:11]:
        title.append(i[0])
        popularity.append(i[1])
        ids.append(i[2])
    df = pd.DataFrame()
    df['title'] = title
    df['popularity'] = popularity
    df['movie_id'] = ids
    return df


def genres(kind):
    movies2 = []
    for j in range(0, len(data2)):
        if kind in data2['genres'][j]:
            movies2.append(data2[['title', 'popularity', 'movie_id']].iloc[j].tolist())
    movies_sorted = sorted(movies2, reverse=True, key=lambda x: x[1])
    title = []
    popularity = []
    ids = []
    for i in movies_sorted[:11]:
        title.append(i[0])
        popularity.append(i[1])
        ids.append(i[2])
    df = pd.DataFrame()
    df['title'] = title
    df['popularity'] = popularity
    df['movie_id'] = ids
    return df


def popular(person):
    df = actor(person)
    pop_movie_posters = []
    ids = df['movie_id'].to_list()
    for j in ids:
        pop_movie_posters.append(fetch_poster(j))
    pop_movie_names = df['title'].to_list()

    return pop_movie_names, pop_movie_posters


def gen_movies(gen):
    df = genres(gen)
    gen_movie_posters = []
    ids = df['movie_id'].to_list()
    for j in ids:
        gen_movie_posters.append(fetch_poster(j))
    gen_movie_names = df['title'].to_list()

    return gen_movie_names, gen_movie_posters


st.header('Movie Recommender System Using Machine Learning')

movies = pickle.load(open('a/movie_list.pkl', 'rb'))
similarity = pickle.load(open('a/similarity.pkl', 'rb'))
data2 = pickle.load(open('b/pop_movie.pkl', 'rb'))
genres_list = pickle.load(open('b/genres.pkl', 'rb'))

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

st.markdown('### 5 most popular movies with a given actor')
actor_name = st.text_input("Enter actor's name")

if st.button('Show to 5 Movies'):
    movie_names, movie_posters = popular(actor_name)

    if len(movie_names) == 0:
        st.markdown('Sorry, we did not find this actor.')
    else:
        cols = st.columns(5)
        for col, (movie_name, movie_poster) in zip(cols, zip(movie_names, movie_posters)):
            with col:
                st.text(movie_name)
                st.image(movie_poster)


st.markdown('### 5 most popular movies with a given genre')
gen_name = st.selectbox(
    "Type or select a movie genre from the dropdown",
    genres_list
)

if st.button('Show top 10 Movies'):
    movie_names2, movie_posters2 = gen_movies(gen_name)

    if len(movie_names2) == 0:
        st.markdown('Sorry, we did not find this actor.')
    else:
        num_movies = len(movie_names2)
        num_cols = 5
        num_rows = 2

        for row in range(num_rows):
            cols = st.columns(num_cols)
            start_idx = row * num_cols
            end_idx = min(start_idx + num_cols, num_movies)
            for col, (movie_name, movie_poster) in zip(cols, zip(movie_names2[start_idx:end_idx],
                                                                 movie_posters2[start_idx:end_idx])):
                with col:
                    st.text(movie_name)
                    st.image(movie_poster)

