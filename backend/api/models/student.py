from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from src.infrastructure.database import Base
from pydantic import BaseModel
from typing import Optional

class StudentModel(Base):
    __tablename__ = "student_metadata"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    matric_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

class StudentBase(BaseModel):
    name: str
    matric_id: str
    email: str
    lat: Optional[float] = None
    lng: Optional[float] = None

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True
