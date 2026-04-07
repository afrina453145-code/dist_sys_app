from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from api.models.student import StudentCreate, StudentResponse
from api.endpoints.student.save import save_student
from api.endpoints.student.get import get_students, get_student_by_matric
from typing import List
from src.telemetry.logger import log_osi_trace

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentResponse)
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    log_osi_trace(0, "ENDPOINT_CALL", f"POST /students/ - matric_id: {student.matric_id}")
    return await save_student(db, student)

@router.get("/", response_model=List[StudentResponse])
async def read_students(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    log_osi_trace(0, "ENDPOINT_CALL", f"GET /students/ - skip: {skip}, limit: {limit}")
    return await get_students(db, skip=skip, limit=limit)

@router.get("/{matric_id}", response_model=StudentResponse)
async def read_student(matric_id: str, db: AsyncSession = Depends(get_db)):
    db_student = await get_student_by_matric(db, matric_id=matric_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student
