from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models.driver import DriverModel
from src.telemetry.logger import log_osi_trace

async def get_drivers(db: AsyncSession, skip: int = 0, limit: int = 100):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT drivers OFFSET {skip} LIMIT {limit}")
    result = await db.execute(select(DriverModel).offset(skip).limit(limit))
    return result.scalars().all()

async def get_driver_by_id(db: AsyncSession, driver_id: str):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT driver WHERE driver_id='{driver_id}'")
    result = await db.execute(select(DriverModel).filter(DriverModel.driver_id == driver_id))
    return result.scalars().first()
