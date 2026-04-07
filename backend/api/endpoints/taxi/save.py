from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models.taxi import TaxiModel, TaxiCreate
from src.telemetry.logger import log_osi_trace

async def save_taxi(db: AsyncSession, taxi_data: TaxiCreate):
    # --- Database Layer Trace (Layer 0) ---
    log_osi_trace(0, "SQL_QUERY", f"SELECT/UPSERT taxi WHERE plate_id='{taxi_data.plate_id}'")
    
    # Check if exists
    result = await db.execute(select(TaxiModel).filter(TaxiModel.plate_id == taxi_data.plate_id))
    db_taxi = result.scalars().first()
    
    if db_taxi:
        for key, value in taxi_data.model_dump().items():
            setattr(db_taxi, key, value)
    else:
        db_taxi = TaxiModel(**taxi_data.model_dump())
        db.add(db_taxi)
    
    await db.commit()
    await db.refresh(db_taxi)
    return db_taxi
