from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from src.infrastructure.database import Base
from pydantic import BaseModel
from typing import Optional

class BicycleModel(Base):
    __tablename__ = "bicycle_metadata"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    color = Column(String)
    fleet_id = Column(String, unique=True, index=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

class BicycleBase(BaseModel):
    name: str
    color: str
    fleet_id: str
    lat: Optional[float] = None
    lng: Optional[float] = None

class BicycleCreate(BicycleBase):
    pass

class BicycleResponse(BicycleBase):
    id: int

    class Config:
        from_attributes = True
