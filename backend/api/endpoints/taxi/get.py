from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models.taxi import TaxiModel
from src.telemetry.logger import log_osi_trace

async def get_taxis(db: AsyncSession, skip: int = 0, limit: int = 100):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT taxis OFFSET {skip} LIMIT {limit}")
    result = await db.execute(select(TaxiModel).offset(skip).limit(limit))
    return result.scalars().all()

async def get_taxi_by_plate(db: AsyncSession, plate_id: str):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT taxi WHERE plate_id='{plate_id}'")
    result = await db.execute(select(TaxiModel).filter(TaxiModel.plate_id == plate_id))
    return result.scalars().first()
