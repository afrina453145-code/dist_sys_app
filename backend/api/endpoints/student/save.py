from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models.student import StudentModel, StudentCreate
from src.telemetry.logger import log_osi_trace

async def save_student(db: AsyncSession, student_data: StudentCreate):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT/UPSERT student WHERE matric_id='{student_data.matric_id}'")
    
    # Check if exists
    result = await db.execute(select(StudentModel).filter(StudentModel.matric_id == student_data.matric_id))
    db_student = result.scalars().first()
    
    if db_student:
        for key, value in student_data.model_dump().items():
            setattr(db_student, key, value)
    else:
        db_student = StudentModel(**student_data.model_dump())
        db.add(db_student)
    
    await db.commit()
    await db.refresh(db_student)
    return db_student
