from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models.driver import DriverModel, DriverCreate
from src.telemetry.logger import log_osi_trace

async def save_driver(db: AsyncSession, driver_data: DriverCreate):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT/UPSERT driver WHERE driver_id='{driver_data.driver_id}'")
    
    # Check if exists
    result = await db.execute(select(DriverModel).filter(DriverModel.driver_id == driver_data.driver_id))
    db_driver = result.scalars().first()
    
    if db_driver:
        for key, value in driver_data.model_dump().items():
            setattr(db_driver, key, value)
    else:
        db_driver = DriverModel(**driver_data.model_dump())
        db.add(db_driver)
    
    await db.commit()
    await db.refresh(db_driver)
    return db_driver
