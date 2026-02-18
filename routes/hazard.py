from fastapi import APIRouter
from models.hazard import HazardReport
from typing import List

hazard_router = APIRouter()

# In-memory store for demonstration (replace with DB integration)
hazard_reports: List[HazardReport] = []

@hazard_router.post("/hazard", response_model=HazardReport)
def report_hazard(hazard: HazardReport):
    hazard_reports.append(hazard)
    return hazard

@hazard_router.get("/hazards", response_model=List[HazardReport])
def get_hazards():
    return hazard_reports
