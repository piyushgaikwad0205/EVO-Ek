from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HazardReport(BaseModel):
    latitude: float
    longitude: float
    description: str
    hazard_type: str  # e.g., 'no streetlight', 'unsafe area', 'stray animals'
    reported_by: str  # user identifier (can be anonymous)
    timestamp: Optional[str] = None  # Auto-generated if not provided
