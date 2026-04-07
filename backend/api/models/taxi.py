from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from src.infrastructure.database import Base
from pydantic import BaseModel
from typing import Optional

class TaxiModel(Base):
    __tablename__ = "taxi_metadata"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    color = Column(String)
    plate_id = Column(String, unique=True, index=True)
    start = Column(String)
    destination = Column(String)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

class TaxiBase(BaseModel):
    name: str
    color: str
    plate_id: str
    start: str
    destination: str
    lat: Optional[float] = None
    lng: Optional[float] = None

class TaxiCreate(TaxiBase):
    pass

class TaxiResponse(TaxiBase):
    id: int

    class Config:
        from_attributes = True
