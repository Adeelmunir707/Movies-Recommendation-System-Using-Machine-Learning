# we can use flask, but we will use streamlit library for our API
import streamlit as st
import pickle
import pandas as pd
import requests

#=====================================
st.set_page_config(
    page_title="AI Movie Recommender",
    page_icon="🎬",
    layout="wide"
)
# ======================================

st.markdown("""
<style>

/* Remove default padding/margins */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100% !important;
}

/* Make app stretch full width */
.css-18e3th9 {
    padding: 0 !important;
}

/* Remove extra whitespace */
.css-1d391kg {
    padding: 0 !important;
}

/* Optional: center content nicely */
.main {
    max-width: 100%;
}

/* Movie cards spacing */
.movie-card {
    width: 100%;
}

/* Background */
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Title */
.big-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.sub-text {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

/* Card */
.movie-card {
    background: #1e293b;
    padding: 10px;
    border-radius: 15px;
    text-align: center;
    transition: 0.3s;
}

.movie-card:hover {
    transform: scale(1.05);
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #38bdf8);
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recomended_movies = []
    recomended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id                                 # similar movie index will replace i[0]
        recomended_movies.append(movies.iloc[i[0]].title)      # now extract the movies names of these 5 indices
    # fetching poster for movies from API
        recomended_movies_poster.append(fetch(movie_id))
    return recomended_movies,recomended_movies_poster

def fetch(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url)

        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=API+Error"

        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except:
        return "https://via.placeholder.com/500x750?text=Error"


# movies file
movies_dict =  pickle.load(open('movies_dict.pkl','rb'))          # loading movies list and opeingin it in read binary
movies = pd.DataFrame(movies_dict)

# similarity file
similarity= pickle.load(open('similarity.pkl','rb'))          # loading movies list and opeingin it in read binary

st.markdown('<p class="big-title">🤖 AI Movie Recommender</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Discover movies powered by Machine Learning</p>', unsafe_allow_html=True)

# getting the movies list from the movie_recomender.ipynb to here,
# using pikkle library
selected_movie_name = st.selectbox(
    '🎬 Choose a movie',
    movies['title'].values
)

# button
if st.button('✨ Recommend Movies'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            st.image(posters[i])
            st.markdown(f"**{names[i]}**")
            st.markdown('</div>', unsafe_allow_html=True)
