import duckdb

def load_data(db_path="/app/data/homeflix.duckdb"):
    con = duckdb.connect(db_path, read_only=True)
    df_ratings = con.execute("SELECT * FROM ratings").fetchdf()
    df_films = con.execute("SELECT * FROM films").fetchdf()
    con.close()
    return df_ratings, df_films
