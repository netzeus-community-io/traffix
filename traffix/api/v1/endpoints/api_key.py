from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from traffix_sdk.dependencies.fastapi import DatabaseDep
from traffix_sdk.models import (
    TraffixAPIKeyRead,
    TraffixAPIKeyCreate,
    TraffixAPIKeyUpdate,
)
from traffix_sdk.database.async_drivers import sqlmodel as crud
from traffix_sdk.dependencies.user import get_active_superuser

router = APIRouter(dependencies=[Depends(get_active_superuser)])


@router.post("/", response_model=TraffixAPIKeyRead)
async def create_api_key(db: DatabaseDep, api_key_obj_in: TraffixAPIKeyCreate):
    """Create an API Key in the database."""
    existing_api_key = await crud.traffix_api_key.get_by_api_key(
        db=db, api_key=api_key_obj_in.api_key
    )
    if existing_api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="API Key already exist"
        )

    if api_key_obj_in.user_id:
        user_exist = await crud.traffix_user.get(db=db, id=api_key_obj_in.user_id)
        if not user_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist"
            )

    api_key = await crud.traffix_api_key.create(db=db, obj_in=api_key_obj_in)
    return api_key


@router.get("/", response_model=List[TraffixAPIKeyRead])
async def get_api_keys(db: DatabaseDep, skip: int = 0, limit: int = 100):
    """Get all API Keys from the database."""
    api_keys = await crud.traffix_api_key.get_multi(db=db, skip=skip, limit=limit)
    return api_keys


@router.get("/{id}", response_model=TraffixAPIKeyRead)
async def get_api_key(db: DatabaseDep, id: int):
    """Get a specific API Key from the database."""
    api_key = await crud.traffix_api_key.get(db=db, id=id)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="API Key does not exist"
        )

    return api_key


@router.patch("/{id}", response_model=TraffixAPIKeyRead)
async def update_api_key(db: DatabaseDep, id: int, api_key_obj_in: TraffixAPIKeyUpdate):
    """Update a specific API Key in the database."""
    api_key = await crud.traffix_api_key.get(db=db, id=id)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="API Key does not exist"
        )

    if api_key_obj_in.api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can not update an API Key. You must remove it and add it again",
        )

    updated_api_key = await crud.traffix_api_key.update(
        db=db, db_obj=api_key, obj_in=api_key_obj_in
    )
    return updated_api_key


@router.delete("/{id}", response_model=TraffixAPIKeyRead)
async def delete_api_key(db: DatabaseDep, id: int):
    """Delete a specific API Key from the database."""
    api_key = await crud.traffix_api_key.get(db=db, id=id)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="API Key does not exist"
        )

    await crud.traffix_api_key.remove(db=db, id=id)
    return api_key
