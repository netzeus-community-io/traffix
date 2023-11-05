from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from traffix_sdk.dependencies.fastapi import DatabaseDep
from traffix_sdk.models import (
    TraffixCategoryCreate,
    TraffixCategoryRead,
    TraffixCategoryUpdate,
)
from traffix_sdk.database.async_drivers import sqlmodel as crud
from traffix_sdk.dependencies.user import get_active_superuser

router = APIRouter(dependencies=[Depends(get_active_superuser)])


@router.post("/", response_model=TraffixCategoryRead)
async def create_category(db: DatabaseDep, category_obj_in: TraffixCategoryCreate):
    """Creates a Category in the database."""
    category_exist = await crud.traffix_category.get_by_name(
        db=db, name=category_obj_in.name
    )
    if category_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category already exist"
        )

    category_created = await crud.traffix_category.create(db=db, obj_in=category_obj_in)
    return category_created


@router.get("/", response_model=List[TraffixCategoryRead])
async def get_categories(db: DatabaseDep, skip: int = 0, limit: int = 100):
    """Get all Categories in the database."""
    categories = await crud.traffix_category.get_multi(db=db, skip=skip, limit=limit)
    return categories


@router.get("/{id}", response_model=TraffixCategoryRead)
async def get_category(db: DatabaseDep, id: int):
    """Get a specific Category from the database."""
    category_exist = await crud.traffix_category.get(db=db, id=id)
    if not category_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist"
        )

    return category_exist


@router.patch("/{id}", response_model=TraffixCategoryRead)
async def update_category(
    db: DatabaseDep, id: int, category_obj_in: TraffixCategoryUpdate
):
    """Update a specific Category based on a name in the database."""
    category_exist = await crud.traffix_category.get(db=db, id=id)
    if not category_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist"
        )

    if category_obj_in.name and category_exist.name != category_obj_in.name:
        category_already_exist = await crud.traffix_category.get_by_name(
            db=db, name=category_obj_in.name
        )
        if category_already_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exist"
            )

    updated_category = await crud.traffix_category.update(
        db=db, db_obj=category_exist, obj_in=category_obj_in
    )
    return updated_category


@router.delete("/{id}", response_model=TraffixCategoryRead)
async def delete_category(db: DatabaseDep, id: int):
    category_exist = await crud.traffix_category.get(db=db, id=id)
    if not category_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist"
        )

    await crud.traffix_category.remove(db=db, id=id)
    return category_exist
