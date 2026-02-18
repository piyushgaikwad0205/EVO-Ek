from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Hazard(Base):
    __tablename__ = 'hazards'
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    hazard_type = Column(String, nullable=False)
    reported_by = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    safety_score = Column(Float, nullable=True)
