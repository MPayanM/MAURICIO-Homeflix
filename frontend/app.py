import streamlit as st
import pandas as pd
import requests
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os

st.set_page_config(page_title="HomeFlix", layout="wide")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("static/icon.png", caption="Experience cinema like never before", width=400)

st.title("🎬 HomeFlix - Movie Recommender and Insights")
section = st.sidebar.radio("Choose a section", ["📊 Data Analysis", "🎥 Movie Recommendations"])


db_path = "/app/data/homeflix.duckdb"




# Leer host del backend desde variable de entorno, con fallback a localhost
BACKEND_HOST = os.getenv("BACKEND_HOST", "localhost")  # Cambié el valor predeterminado a "localhost"
BACKEND_PORT = 8000
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"  # Ahora construye correctamente la URL

def load_duckdb_data():
    try:
        con = duckdb.connect(db_path, read_only=True)
        df_ratings = con.execute("SELECT * FROM ratings").fetchdf()
        df_films = con.execute("SELECT * FROM films").fetchdf()
        con.close()
        return df_ratings, df_films
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def fetch_with_retries(url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                raise e

# ========================
# SECTION 1: DATA ANALYSIS
# ========================
if section == "📊 Data Analysis":
    st.header("📈 Movie Ratings and User Statistics")

    df_ratings, df_films = load_duckdb_data()

    if df_ratings is not None and df_films is not None:
        merged = df_ratings.merge(df_films, left_on="film_id", right_on="id")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🎞️ Movies Average Rating")
            avg_ratings = merged.groupby("title")["rating"].mean()
            fig, ax = plt.subplots(figsize=(5, 4))
            sns.violinplot(x=avg_ratings.values, ax=ax, color="skyblue", linewidth=1.25, inner="stick")
            ax.collections[0].set_edgecolor("black")
            ax.collections[0].set_alpha(0.3)
            ax.set_xlabel("Average Rating")
            st.pyplot(fig)

        with col2:
            st.subheader("📅 Releases per Year")
            df_films["release_year"] = pd.to_datetime(df_films["release_date"], errors="coerce").dt.year
            year_counts = df_films["release_year"].value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(5, 4))
            year_counts.plot(kind="line", marker="o", color="#ff7f0e", ax=ax)
            ax.set_xlabel("Year")
            ax.set_ylabel("Number of Releases")
            st.pyplot(fig)

        with col3:
            st.subheader("👤 Rating Distribution")
            df_ratings_dist = df_ratings.groupby("rating").size().reset_index(name='count')
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.bar(df_ratings_dist['rating'], df_ratings_dist['count'], color="#2ca02c")
            ax.set_xlabel("Rating")
            ax.set_ylabel("Votes")
            st.pyplot(fig)

        top_voted = df_films[['title', 'vote_count', 'vote_average']].sort_values(by='vote_count', ascending=False).head(10)
        st.subheader("🏆 Top 10 Most Voted Movies & their Average Rating")
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(top_voted['title'], top_voted['vote_count'], color='steelblue')
        ax.set_xlabel("Vote Count")
        ax.set_title("Top Voted Movies")
        ax.invert_yaxis()

        for bar, avg in zip(bars, top_voted['vote_average']):
            ax.text(bar.get_width() - 200, bar.get_y() + bar.get_height()/2, f"{avg:.1f}",
                    va='center', ha='right', color='white', fontweight='bold')

        st.pyplot(fig)

        st.markdown("---")
        st.caption("© 2025 Mauricio Media Group. Mauricio and related elements are the property of Mauricio Media Group. All rights reserved.")

# ==============================
# SECTION 2: MOVIE RECOMMENDER
# ==============================
elif section == "🎥 Movie Recommendations":
    st.header("🎯 Personalized Movie Recommender")
    user_id = st.number_input("Enter a user ID to get movie recommendations:", min_value=1, step=1)

    if st.button("Get Recommendations"):
        try:
            url = f"{BACKEND_URL}/recommend_movies/{user_id}"
            data = fetch_with_retries(url)
            st.success(f"Top recommended movies for user {user_id}:")
            for movie in data["recommendations"]:
                st.write(f"🎬 **{movie['title']}** — ⭐ {movie['rating_predicted']}")
        except Exception as e:
            st.error(f"Failed to connect to backend at {BACKEND_URL}: {e}")

    st.markdown("---")
    st.caption("© 2025 Mauricio Media Group. Mauricio and related elements are the property of Mauricio Media Group. All rights reserved.")
