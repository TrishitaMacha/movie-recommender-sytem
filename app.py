import streamlit as st
import pickle
import pandas as pd
import requests
import google.generativeai as genai

# -------------------- UI STYLE --------------------
st.markdown("""
<style>
.movie-card {
    background-color: #111;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
    color: white;
    transition: 0.3s;
}
.movie-card:hover {
    transform: scale(1.05);
}
.movie-title {
    font-size: 14px;
    font-weight: bold;
    margin-top: 8px;
}
.movie-info {
    font-size: 12px;
    color: #bbb;
}
</style>
""", unsafe_allow_html=True)

# -------------------- API KEYS --------------------
TMDB_API_KEY = "0fa89fe348ea2bd36baa2961437188b2"
OMDB_API_KEY = "d8c15a91"

genai.configure(api_key="AIzaSyCtn6E36p4apU7xpkTFZGYKROV_SJzyNrw")
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------- GEMINI DESCRIPTION --------------------
def generate_ai_description(movie_name):
    try:
        response = model.generate_content(
            f"Give a simple 2-line description of the movie '{movie_name}'. Only plain text."
        )
        if response and response.text:
            return response.text.strip()
    except:
        pass
    return f"{movie_name} is an engaging movie with an interesting storyline."

# -------------------- OMDB BACKUP --------------------
def fetch_from_omdb(movie_name):
    try:
        clean_name = movie_name.replace(":", "").replace("-", " ")

        # 1️⃣ Try exact title
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={clean_name}"
        data = requests.get(url, timeout=5).json()

        if data.get("Poster") and data["Poster"] != "N/A":
            return data["Poster"]

        # 2️⃣ Try search API (IMPORTANT FIX)
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={clean_name}"
        data = requests.get(url, timeout=5).json()

        if data.get("Search"):
            for movie in data["Search"]:
                if movie.get("Poster") and movie["Poster"] != "N/A":
                    return movie["Poster"]

    except:
        pass

    return None
# -------------------- MAIN FETCH --------------------
def fetch_movie_data(movie_id, movie_name):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        data = requests.get(url, timeout=5).json()

        poster_url = None

        # TMDb
        poster_path = data.get("poster_path")
        if poster_path:
            poster_url = "https://image.tmdb.org/t/p/w500" + poster_path

        # OMDb fallback
        if not poster_url:
            poster_url = fetch_from_omdb(movie_name)

        # Final fallback
        if not poster_url:
            poster_url = f"https://via.placeholder.com/300x450/111/fff?text={movie_name}"

        # Overview
        overview = data.get("overview")
        if not overview or overview.strip() == "":
            overview = generate_ai_description(movie_name)

        return poster_url, overview

    except:
        return (
            f"https://via.placeholder.com/300x450/111/fff?text={movie_name}",
            generate_ai_description(movie_name)
        )

# -------------------- RECOMMEND --------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names, posters, overviews = [], [], []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title

        poster, overview = fetch_movie_data(movie_id, movie_title)

        names.append(movie_title)
        posters.append(poster)
        overviews.append(overview)

    return names, posters, overviews

# -------------------- LOAD DATA --------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# -------------------- UI --------------------
st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select any Movie",
    movies['title'].values
)

if st.button("Recommend"):

    with st.spinner("Fetching movies... 🎬"):
        names, posters, overviews = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)

            img = posters[i]
            if not img:
                img = f"https://via.placeholder.com/300x450/111/fff?text={names[i]}"

            st.image(img, use_container_width=True)
            st.markdown(f"**{names[i]}**")

            clean_text = overviews[i].replace("\n", " ")
            st.caption(clean_text[:140] + "...")

            st.markdown('</div>', unsafe_allow_html=True)