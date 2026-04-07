from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models.bus import BusModel, BusCreate
from src.telemetry.logger import log_osi_trace

async def save_bus(db: AsyncSession, bus_data: BusCreate):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT/UPSERT bus WHERE plate_id='{bus_data.plate_id}'")
    
    # Check if exists
    result = await db.execute(select(BusModel).filter(BusModel.plate_id == bus_data.plate_id))
    db_bus = result.scalars().first()
    
    if db_bus:
        for key, value in bus_data.model_dump().items():
            setattr(db_bus, key, value)
    else:
        db_bus = BusModel(**bus_data.model_dump())
        db.add(db_bus)
    
    await db.commit()
    await db.refresh(db_bus)
    return db_bus
