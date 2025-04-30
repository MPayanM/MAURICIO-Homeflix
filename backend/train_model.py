import pickle
import duckdb
import pandas as pd
from surprise import SVD, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split
import time
import os

model_dir = "models"
os.makedirs(model_dir, exist_ok=True)

print("Conectando a la base de datos DuckDB...")
con = duckdb.connect("../data/homeflix.duckdb", read_only=True)

print("Cargando datos desde la tabla 'ratings'...")
df = con.execute("SELECT user_id, film_id, rating FROM ratings").fetchdf()
con.close()
print(f"Datos cargados: {len(df)} registros")

print("Preparando los datos para Surprise...")
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(df[['user_id', 'film_id', 'rating']], reader)
trainset, testset = train_test_split(data, test_size=0.2)

print("Entrenando el modelo SVD...")
start_time = time.time()
model = SVD()
model.fit(trainset)
print(f"Entrenamiento completado en {round(time.time() - start_time, 2)} segundos")

print("Evaluando el modelo con el conjunto de prueba...")
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
print(f"Error cuadrático medio (RMSE): {rmse:.4f}")

print("Guardando el modelo entrenado en 'backend/models/svd_model.pkl'...")
with open("backend/models/svd_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Modelo entrenado y guardado correctamente.")
