from fastapi import APIRouter
from utils.models_loader import model_manager

scoring_router = APIRouter()

@scoring_router.get("/score")
def get_score(latitude: float, longitude: float, hazard_type: str):
    score = model_manager.score_location(latitude, longitude, hazard_type)
    return {"latitude": latitude, "longitude": longitude, "hazard_type": hazard_type, "safety_score": score}
