import streamlit as st
import pickle
import requests

# page title
st.set_page_config(
   page_title="Movie Recommender",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

# hide footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

movies_list = pickle.load(open('movie.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
     response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=9f3bd4b3ec28b3e219376628a4e3feee&language=en-US')
     data = response.json()
     return 'http://image.tmdb.org/t/p/w500/' +data['poster_path']

def recommend(movie):
     movie_index = movies_list[movies_list['title'] == movie].index[0]
     distances = similarity[movie_index]
     dis_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1: 6]
     recommended_movies = []
     posters = []
     for i in dis_list:
          movie_id = movies_list.iloc[i[0]].movie_id
          # fecth poster from tmdb api
          posters.append(fetch_poster(movie_id))
          recommended_movies.append(movies_list.iloc[i[0]].title)
     return recommended_movies, posters

st.title('Movie Recommender System')

selected_movie = st.selectbox(
     'Choose A Movie you like ',
     movies_list.title.values)

if st.button('Recommend'):
     names, posters =  recommend(selected_movie)
     col1, col2, col3, col4, col5 = st.columns(5)

     col1.image(posters[0], use_column_width=True)
     col1.write(names[0])

     col2.image(posters[1], use_column_width=True)
     col2.write(names[1])

     col3.image(posters[2], use_column_width=True)
     col3.write(names[2])

     col4.image(posters[3], use_column_width=True)
     col4.write(names[3])

     col5.image(posters[4], use_column_width=True)
     col5.write(names[4])

