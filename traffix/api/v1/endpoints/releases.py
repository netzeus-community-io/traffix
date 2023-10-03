from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

from traffix.dependencies import get_db
from traffix.models import RURead
from traffix import crud

router = APIRouter()


@router.get("/", response_model=List[RURead])
async def get_releases(
    db: AsyncIOMotorDatabase = Depends(get_db), skip: int = 0, limit: int = 1000, after_now: bool = False, before_now: bool = False
):
    if after_now and before_now:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="after_now and before_now can not be set together.")

    query_filter = {"reviewed": True}
    if after_now or before_now:
        query_filter["release_date"] = {"$gte" if after_now else "$lte": datetime.utcnow()}

    releases = await crud.ru.get_multi(db=db, skip=skip, limit=limit, query=query_filter)
    return releases

@router.get("/{name}", response_model=RURead)
async def get_release(
    *, db: AsyncIOMotorDatabase = Depends(get_db), name: str
):
    release_exist = await crud.ru.get_by_name(db=db, name=name)
    if not release_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Release {name} not found")
    
    return release_exist