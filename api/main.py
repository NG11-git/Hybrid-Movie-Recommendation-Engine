from fastapi import FastAPI, HTTPException
from api.schemas import RecommendationResponse, HealthResponse
from api.dependencies import recommender_service

app = FastAPI(title="Movie Recommendation API")

@app.get("/health", response_model=HealthResponse)
def health_check():
    return {"status":"ok"}

@app.get("/recommend/user/{user_id}", response_model=RecommendationResponse)
def recommend_user(user_id: int, top_n: int=10):
    try:
        recommendation = recommender_service.recommend_for_user(
            user_id=user_id,
            top_n=top_n
        )
        if not recommendation:
            raise HTTPException(status_code=404, detail="NO Recommendation Found")
        
        return {
            "user_id": user_id,
            "recommendation": recommendation

        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        