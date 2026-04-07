from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models.bus import BusModel
from src.telemetry.logger import log_osi_trace

async def get_buses(db: AsyncSession, skip: int = 0, limit: int = 100):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT buses OFFSET {skip} LIMIT {limit}")
    result = await db.execute(select(BusModel).offset(skip).limit(limit))
    return result.scalars().all()

async def get_bus_by_plate(db: AsyncSession, plate_id: str):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT bus WHERE plate_id='{plate_id}'")
    result = await db.execute(select(BusModel).filter(BusModel.plate_id == plate_id))
    return result.scalars().first()
