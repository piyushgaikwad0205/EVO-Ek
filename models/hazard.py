from pydantic import BaseModel

class HazardReport(BaseModel):
    latitude: float
    longitude: float
    description: str
    hazard_type: str  # e.g., 'no streetlight', 'unsafe area', 'stray animals'
    reported_by: str  # user identifier (can be anonymous)
    timestamp: str
