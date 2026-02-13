from pydantic import BaseModel
from typing import List, Optional

class MovieSchema(BaseModel):
    title: str
    overview: Optional[str]
    rating: Optional[float]
    poster_url: Optional[str]

class RecommendationResponse(BaseModel):
    user_id: int
    recommendations: List[MovieSchema]

class HealthResponse(BaseModel):
    status: str