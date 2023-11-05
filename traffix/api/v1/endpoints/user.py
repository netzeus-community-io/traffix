from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from traffix_sdk.dependencies.fastapi import DatabaseDep
from traffix_sdk.models import (
    TraffixAPIUserRead,
    TraffixAPIUserCreate,
    TraffixAPIUserUpdate,
)
from traffix_sdk.database.async_drivers import sqlmodel as crud
from traffix_sdk.dependencies.user import get_active_superuser

router = APIRouter(dependencies=[Depends(get_active_superuser)])


@router.post("/", response_model=TraffixAPIUserRead)
async def create_user(db: DatabaseDep, user_obj_in: TraffixAPIUserCreate):
    """Create a User in the database."""
    user_exist = await crud.traffix_user.get_by_email(db=db, email=user_obj_in.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exist with that email",
        )

    user_created = await crud.traffix_user.create(db=db, obj_in=user_obj_in)
    return user_created


@router.get("/", response_model=List[TraffixAPIUserRead])
async def get_users(db: DatabaseDep, skip: int = 0, limit: int = 100):
    """Get all Users in the database."""
    users = await crud.traffix_user.get_multi(db=db, skip=skip, limit=limit)
    return users


@router.get("/{id}", response_model=TraffixAPIUserRead)
async def get_user(db: DatabaseDep, id: int):
    """Get a specific User in the database."""
    user_exist = await crud.traffix_user.get(db=db, id=id)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    return user_exist


@router.patch("/{id}", response_model=TraffixAPIUserRead)
async def update_user(db: DatabaseDep, id: int, user_obj_in: TraffixAPIUserUpdate):
    """Update a specific User in the database."""
    user_exist = await crud.traffix_user.get(db=db, id=id)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    if user_obj_in.email and user_obj_in.email != user_exist.email:
        email_already_used = await crud.traffix_user.get_by_email(
            db=db, email=user_obj_in.email
        )
        if email_already_used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A User with this email already exist",
            )

    updated_user = await crud.traffix_user.update(
        db=db, db_obj=user_exist, obj_in=user_obj_in
    )
    return updated_user


@router.delete("/{id}", response_model=TraffixAPIUserRead)
async def delete_user(db: DatabaseDep, id: int):
    """Delete a User in the database."""
    user_exist = await crud.traffix_user.get(db=db, id=id)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    await crud.traffix_user.remove(db=db, id=user_exist.id)
    return user_exist
