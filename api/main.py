from fastapi import FastAPI, HTTPException
from api.schemas import RecommendationResponse, HealthResponse
from api.dependencies import recommender_service

app = FastAPI(title="Movie Recommendation API")

@app.get("/health", response_model=HealthResponse)
def health_check():
    return {"status":"ok"}

@app.get("/recommend/user/{user_id}", response_model=RecommendationResponse)
def recommend_user(user_id: int, top_n: int=10):
    recommendation = recommender_service.recommend_for_user(
        user_id=user_id,
        top_n=top_n
    )

    return {
        "user_id": user_id,
        "recommendations": recommendation
    }
        