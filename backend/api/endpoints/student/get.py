from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models.student import StudentModel
from src.telemetry.logger import log_osi_trace

async def get_students(db: AsyncSession, skip: int = 0, limit: int = 100):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT students OFFSET {skip} LIMIT {limit}")
    result = await db.execute(select(StudentModel).offset(skip).limit(limit))
    return result.scalars().all()

async def get_student_by_matric(db: AsyncSession, matric_id: str):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT student WHERE matric_id='{matric_id}'")
    result = await db.execute(select(StudentModel).filter(StudentModel.matric_id == matric_id))
    return result.scalars().first()
