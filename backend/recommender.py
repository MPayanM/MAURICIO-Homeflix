from surprise import SVD, Dataset
import pandas as pd

def get_recommendations(model, df_ratings: pd.DataFrame, df_films: pd.DataFrame, user_id: int, n_recommendations: int = 5):
    predictions = []
    user_seen = df_ratings[df_ratings['user_id'] == user_id]['film_id'].values

    for movie_id in df_films['id']:
        if movie_id not in user_seen:
            pred = model.predict(uid=user_id, iid=movie_id)
            predictions.append((movie_id, pred.est))

    predictions.sort(key=lambda x: x[1], reverse=True)

    results = []
    for movie_id, rating in predictions[:n_recommendations]:
        movie = df_films[df_films['id'] == movie_id].iloc[0]
        results.append({
            'id': int(movie['id']),
            'title': movie['title'],
            'rating_predicted': round(rating, 1)
        })
    
    return {"user_id": user_id, "recommendations": results}

def predict_rating(model, user_id: int, movie_id: int):
    prediction = model.predict(uid=user_id, iid=movie_id)
    return {
        "user_id": user_id,
        "movie_id": movie_id,
        "predicted_rating": round(prediction.est, 1)
    }
