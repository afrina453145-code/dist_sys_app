from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from api.models.bus import BusCreate, BusResponse
from api.endpoints.bus.save import save_bus
from api.endpoints.bus.get import get_buses, get_bus_by_plate
from typing import List
from src.telemetry.logger import log_osi_trace

router = APIRouter(prefix="/buses", tags=["Buses"])

@router.post("/", response_model=BusResponse)
async def create_bus(bus: BusCreate, db: AsyncSession = Depends(get_db)):
    log_osi_trace(0, "ENDPOINT_CALL", f"POST /buses/ - plate_id: {bus.plate_id}")
    return await save_bus(db, bus)

@router.get("/", response_model=List[BusResponse])
async def read_buses(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    log_osi_trace(0, "ENDPOINT_CALL", f"GET /buses/ - skip: {skip}, limit: {limit}")
    return await get_buses(db, skip=skip, limit=limit)

@router.get("/{plate_id}", response_model=BusResponse)
async def read_bus(plate_id: str, db: AsyncSession = Depends(get_db)):
    db_bus = await get_bus_by_plate(db, plate_id=plate_id)
    if db_bus is None:
        raise HTTPException(status_code=404, detail="Bus not found")
    return db_bus
