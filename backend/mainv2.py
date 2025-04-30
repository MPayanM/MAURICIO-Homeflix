from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import pickle
import pandas as pd
import os

from utils.db import load_data
from recommender import get_recommendations, predict_rating

# Variables globales
model = None
df_ratings: pd.DataFrame = None
df_films: pd.DataFrame = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, df_ratings, df_films
    try:
        print("🔄 Cargando modelo SVD...")

        # Asegura una ruta absoluta al modelo
        model_path = os.path.join(os.path.dirname(__file__), "models", "svd_model.pkl")
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        print("✅ Modelo cargado")

        print("🔄 Cargando datos desde DuckDB...")
        df_ratings, df_films = load_data()
        print(f"✅ Ratings: {len(df_ratings)}, Films: {len(df_films)}")

        yield

    except Exception as e:
        print(f"❌ Error en la carga de datos o modelo: {e}")
        raise HTTPException(status_code=500, detail="Fallo al iniciar el backend")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Buenas tardes "}

# =====================
# Modelos de respuesta
# =====================
class RecommendationResponse(BaseModel):
    user_id: int
    recommendations: list

class PredictionResponse(BaseModel):
    user_id: int
    movie_id: int
    predicted_rating: float

# ===========
# Endpoints
# ===========

@app.get("/recommend_movies/{user_id}", response_model=RecommendationResponse)
def recommend_movies(user_id: int):
    try:
        return get_recommendations(model, df_ratings, df_films, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predict_rating/{user_id}/{movie_id}", response_model=PredictionResponse)
def predict_movie_rating(user_id: int, movie_id: int):
    try:
        return predict_rating(model, user_id, movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/films")
def list_films():
    try:
        return df_films[['id', 'title']].to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ratings")
def get_ratings():
    try:
        return df_ratings.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
