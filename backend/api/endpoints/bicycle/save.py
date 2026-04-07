from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models.bicycle import BicycleModel, BicycleCreate
from src.telemetry.logger import log_osi_trace

async def save_bicycle(db: AsyncSession, bicycle_data: BicycleCreate):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT/UPSERT bicycle WHERE fleet_id='{bicycle_data.fleet_id}'")
    
    # Check if exists
    result = await db.execute(select(BicycleModel).filter(BicycleModel.fleet_id == bicycle_data.fleet_id))
    db_bike = result.scalars().first()
    
    if db_bike:
        for key, value in bicycle_data.model_dump().items():
            setattr(db_bike, key, value)
    else:
        db_bike = BicycleModel(**bicycle_data.model_dump())
        db.add(db_bike)
    
    await db.commit()
    await db.refresh(db_bike)
    return db_bike
