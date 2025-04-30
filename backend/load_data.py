import json
import requests
import pandas as pd
import duckdb
from datetime import datetime
import os

# Ruta a ratings y ubicación donde se guardará la base
db_path = os.path.join("..", "data", "homeflix.duckdb")
ratings_path = os.path.join("..", "data", "ratings.csv")

API_KEY = '8e9da0b6235dd1f75599c57dac8a13f2'

# Crear conexión con DuckDB
con = duckdb.connect(db_path)

# Crear tablas
con.execute("""
CREATE TABLE IF NOT EXISTS ratings (
    user_id INTEGER,
    film_id INTEGER,
    rating FLOAT,
    timestamp INTEGER,
    PRIMARY KEY (user_id, film_id)
)
""")

con.execute("""
CREATE TABLE IF NOT EXISTS films (
    id INTEGER PRIMARY KEY,
    title VARCHAR,
    genres VARCHAR,
    description TEXT,
    release_date DATE,
    vote_average FLOAT,
    vote_count INTEGER
)
""")

# Vaciar tablas por si ya existen datos
con.execute("DELETE FROM ratings")
con.execute("DELETE FROM films")

# Cargar ratings CSV
df_ratings = pd.read_csv(ratings_path, usecols=['userId', 'movieId', 'rating', 'timestamp'])

# Procesar columnas
df_ratings['userId'] = pd.to_numeric(df_ratings['userId'], errors='coerce')
df_ratings['movieId'] = pd.to_numeric(df_ratings['movieId'], errors='coerce')
df_ratings['rating'] = pd.to_numeric(df_ratings['rating'], errors='coerce')
df_ratings['timestamp'] = pd.to_datetime(df_ratings['timestamp'], errors='coerce')
df_ratings['timestamp'] = df_ratings['timestamp'].astype('int64') // 10**9

df_ratings_clean = df_ratings.dropna(subset=['userId', 'movieId', 'rating', 'timestamp'])
df_ratings_clean.rename(columns={'userId': 'user_id', 'movieId': 'film_id'}, inplace=True)

# Registrar e insertar
con.register('ratings_df', df_ratings_clean)
con.execute("""
    INSERT INTO ratings (user_id, film_id, rating, timestamp)
    SELECT user_id, film_id, rating, timestamp FROM ratings_df
""")

# Cargar películas populares desde TMDB
total_pages = 20
movies_data_all = []

for page in range(1, total_pages + 1):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
    response = requests.get(url)

    if response.status_code == 200:
        movies_data = response.json()
        movies_data_all.extend(movies_data['results'])
    else:
        print(f"Error al cargar página {page}: {response.status_code}")

unique_movies = {movie['id']: movie for movie in movies_data_all}
movies_data_all = list(unique_movies.values())

for movie in movies_data_all:
    try:
        genres = ','.join([str(genre) for genre in movie['genre_ids']])
        release_date = datetime.strptime(movie['release_date'], '%Y-%m-%d').date() if movie.get('release_date') else None

        con.execute("""
            INSERT INTO films (id, title, genres, description, release_date, vote_average, vote_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            movie['id'],
            movie['title'],
            genres,
            movie.get('overview', ''),
            release_date,
            movie.get('vote_average', 0.0),
            movie.get('vote_count', 0)
        ))
    except Exception as e:
        print(f"Error con la película {movie['id']}: {e}")

con.close()
print("✅ Base de datos creada en: data/homeflix.duckdb")
