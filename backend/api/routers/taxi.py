from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from api.models.taxi import TaxiCreate, TaxiResponse
from api.endpoints.taxi.save import save_taxi
from api.endpoints.taxi.get import get_taxis, get_taxi_by_plate
from typing import List
from src.telemetry.logger import log_osi_trace

router = APIRouter(prefix="/taxis", tags=["Taxis"])

@router.post("/", response_model=TaxiResponse)
async def create_taxi(taxi: TaxiCreate, db: AsyncSession = Depends(get_db)):
    log_osi_trace(0, "ENDPOINT_CALL", f"POST /taxis/ - plate_id: {taxi.plate_id}")
    return await save_taxi(db, taxi)

@router.get("/", response_model=List[TaxiResponse])
async def read_taxis(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    log_osi_trace(0, "ENDPOINT_CALL", f"GET /taxis/ - skip: {skip}, limit: {limit}")
    return await get_taxis(db, skip=skip, limit=limit)

@router.get("/{plate_id}", response_model=TaxiResponse)
async def read_taxi(plate_id: str, db: AsyncSession = Depends(get_db)):
    db_taxi = await get_taxi_by_plate(db, plate_id=plate_id)
    if db_taxi is None:
        raise HTTPException(status_code=404, detail="Taxi not found")
    return db_taxi
