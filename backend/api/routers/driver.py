from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from api.models.driver import DriverCreate, DriverResponse
from api.endpoints.driver.save import save_driver
from api.endpoints.driver.get import get_drivers, get_driver_by_id
from typing import List
from src.telemetry.logger import log_osi_trace

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.post("/", response_model=DriverResponse)
async def create_driver(driver: DriverCreate, db: AsyncSession = Depends(get_db)):
    log_osi_trace(0, "ENDPOINT_CALL", f"POST /drivers/ - driver_id: {driver.driver_id}")
    return await save_driver(db, driver)

@router.get("/", response_model=List[DriverResponse])
async def read_drivers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    log_osi_trace(0, "ENDPOINT_CALL", f"GET /drivers/ - skip: {skip}, limit: {limit}")
    return await get_drivers(db, skip=skip, limit=limit)

@router.get("/{driver_id}", response_model=DriverResponse)
async def read_driver(driver_id: str, db: AsyncSession = Depends(get_db)):
    db_driver = await get_driver_by_id(db, driver_id=driver_id)
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_driver
