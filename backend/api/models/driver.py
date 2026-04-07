from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from src.infrastructure.database import Base
from pydantic import BaseModel
from typing import Optional

class DriverModel(Base):
    __tablename__ = "driver_metadata"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    driver_id = Column(String, unique=True, index=True)
    status = Column(String, default="Active")
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

class DriverBase(BaseModel):
    name: str
    driver_id: str
    status: str
    lat: Optional[float] = None
    lng: Optional[float] = None

class DriverCreate(DriverBase):
    pass

class DriverResponse(DriverBase):
    id: int

    class Config:
        from_attributes = True
