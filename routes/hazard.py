from fastapi import APIRouter
from models.hazard import HazardReport
from typing import List
from datetime import datetime

hazard_router = APIRouter()

# In-memory store for demonstration (replace with DB integration)
hazard_reports: List[HazardReport] = []

@hazard_router.post("/hazard", response_model=HazardReport)
def report_hazard(hazard: HazardReport):
    # Auto-generate timestamp if not provided
    if not hazard.timestamp:
        hazard.timestamp = datetime.utcnow().isoformat()
    hazard_reports.append(hazard)
    return hazard

@hazard_router.get("/hazards", response_model=List[HazardReport])
def get_hazards():
    return hazard_reports
