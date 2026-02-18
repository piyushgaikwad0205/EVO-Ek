from fastapi import APIRouter
from utils.models_loader import ai_model
from db.database import get_hazards

scoring_router = APIRouter()

@scoring_router.get("/score")
def get_score(latitude: float, longitude: float, hazard_type: str = "unknown"):
    """
    AI-powered location safety scoring
    Returns: safety_score (0.0 = dangerous, 1.0 = very safe)
    """
    # Get nearby hazards for context
    all_hazards = get_hazards()
    nearby_hazards = [h for h in all_hazards 
                     if abs(h.get('latitude', 0) - latitude) < 0.1 
                     and abs(h.get('longitude', 0) - longitude) < 0.1]
    
    # Generate AI-based safety score
    safety_score = ai_model.score_location(latitude, longitude, hazard_type, len(nearby_hazards))
    
    return {
        "latitude": latitude,
        "longitude": longitude,
        "hazard_type": hazard_type,
        "safety_score": safety_score,
        "nearby_hazards_count": len(nearby_hazards),
        "risk_level": ai_model._get_risk_level(safety_score)
    }

@scoring_router.get("/route_safety")
def get_route_safety(route_points: str):
    """
    Analyze entire route safety using AI models
    route_points: JSON array of {lat, lon} objects
    """
    import json
    try:
        points = json.loads(route_points)
        all_hazards = get_hazards()
        route_analysis = ai_model.score_route(points, all_hazards)
        return route_analysis
    except Exception as e:
        return {"error": str(e)}

