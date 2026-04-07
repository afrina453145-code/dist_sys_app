from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models.bicycle import BicycleModel
from src.telemetry.logger import log_osi_trace

async def get_bicycles(db: AsyncSession, skip: int = 0, limit: int = 100):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT bicycles OFFSET {skip} LIMIT {limit}")
    result = await db.execute(select(BicycleModel).offset(skip).limit(limit))
    return result.scalars().all()

async def get_bicycle_by_fleet(db: AsyncSession, fleet_id: str):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT bicycle WHERE fleet_id='{fleet_id}'")
    result = await db.execute(select(BicycleModel).filter(BicycleModel.fleet_id == fleet_id))
    return result.scalars().first()
