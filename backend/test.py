import os
import duckdb

# Ruta absoluta a la base de datos homeflix.duckdb
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'homeflix.duckdb')

# Conectar a DuckDB usando la ruta completa
con = duckdb.connect(db_path)

# Verificar las tablas disponibles
tables = con.execute("SHOW TABLES").fetchall()
print("Tablas disponibles en la base de datos:", tables)

# Verificar los registros en la tabla 'films'
film_count = con.execute("SELECT COUNT(*) FROM films").fetchone()[0]
print(f"Total de películas en la tabla 'films': {film_count}")

# Verificar los registros en la tabla 'ratings'
rating_count = con.execute("SELECT COUNT(*) FROM ratings").fetchone()[0]
print(f"Total de registros en la tabla 'ratings': {rating_count}")

# Cerrar la conexión
con.close()
