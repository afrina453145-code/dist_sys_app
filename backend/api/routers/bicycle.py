from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from api.models.bicycle import BicycleCreate, BicycleResponse
from api.endpoints.bicycle.save import save_bicycle
from api.endpoints.bicycle.get import get_bicycles, get_bicycle_by_fleet
from typing import List
from src.telemetry.logger import log_osi_trace

router = APIRouter(prefix="/bicycles", tags=["Bicycles"])

@router.post("/", response_model=BicycleResponse)
async def create_bicycle(bicycle: BicycleCreate, db: AsyncSession = Depends(get_db)):
    log_osi_trace(0, "ENDPOINT_CALL", f"POST /bicycles/ - fleet_id: {bicycle.fleet_id}")
    return await save_bicycle(db, bicycle)

@router.get("/", response_model=List[BicycleResponse])
async def read_bicycles(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    log_osi_trace(0, "ENDPOINT_CALL", f"GET /bicycles/ - skip: {skip}, limit: {limit}")
    return await get_bicycles(db, skip=skip, limit=limit)

@router.get("/{fleet_id}", response_model=BicycleResponse)
async def read_bicycle(fleet_id: str, db: AsyncSession = Depends(get_db)):
    db_bike = await get_bicycle_by_fleet(db, fleet_id=fleet_id)
    if db_bike is None:
        raise HTTPException(status_code=404, detail="Bicycle not found")
    return db_bike
