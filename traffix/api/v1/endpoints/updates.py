from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from traffix_sdk.dependencies.fastapi import DatabaseDep
from traffix_sdk.models import (
    TraffixUpdateCreate,
    TraffixUpdateRead,
    TraffixUpdateUpdate,
)
from traffix_sdk.database.async_drivers import sqlmodel as crud
from traffix_sdk.dependencies.user import get_active_superuser

router = APIRouter(dependencies=[Depends(get_active_superuser)])


@router.post("/", response_model=TraffixUpdateRead)
async def create_update(db: DatabaseDep, update_obj_in: TraffixUpdateCreate):
    """Creates an Update in the database."""
    update_exist = await crud.traffix_update.get_by_name(db=db, name=update_obj_in.name)
    if update_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Update already exist"
        )

    release_exist = await crud.traffix_release.get(db=db, id=update_obj_in.release_id)
    if not release_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Release {update_obj_in.release_id} does not exist",
        )

    update_created = await crud.traffix_update.create(db=db, obj_in=update_obj_in)
    return update_created


@router.get("/", response_model=List[TraffixUpdateRead])
async def get_updates(db: DatabaseDep, skip: int = 0, limit: int = 100):
    """Get all Updates from the database."""
    updates = await crud.traffix_update.get_multi(db=db, skip=skip, limit=limit)
    return updates


@router.get("/{id}", response_model=TraffixUpdateRead)
async def get_update(db: DatabaseDep, id: int):
    """Get a specific Update from the database."""
    update_exist = await crud.traffix_update.get(db=db, id=id)
    if not update_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Update does not exist"
        )

    return update_exist


@router.patch("/{id}", response_model=TraffixUpdateRead)
async def update_update(db: DatabaseDep, id: int, update_obj_in: TraffixUpdateUpdate):
    """Update a specific Update from the database."""
    update_exist = await crud.traffix_update.get(db=db, id=id)
    if not update_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Update does not exist"
        )

    if update_obj_in.release_id:
        release_exist = await crud.traffix_release.get(
            db=db, id=update_obj_in.release_id
        )
        if not release_exist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Release does not exist"
            )

    updated_release = await crud.traffix_update.update(
        db=db, db_obj=update_exist, obj_in=update_obj_in
    )
    return updated_release


@router.delete("/{id}", response_model=TraffixUpdateRead)
async def delete_update(db: DatabaseDep, id: int):
    """Delete a specific Update from the database."""
    update_exist = await crud.traffix_update.get(db=db, id=id)
    if not update_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Update does not exist"
        )

    await crud.traffix_update.remove(db=db, id=id)
    return update_exist


'''
@router.get("/", response_model=List[TraffixReleaseRead])
async def get_releases(db: DatabaseDep, skip: int = 0, limit: int = 100):
    """Get all Releases from the database."""
    releases = await crud.traffix_release.get_multi(db=db, skip=skip, limit=limit)
    return releases


@router.get("/{id}", response_model=TraffixReleaseRead)
async def get_release(db: DatabaseDep, id: int):
    """Get a specific Release from the database."""
    release_exist = await crud.traffix_release.get(db=db, id=id)
    if not release_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Release does not exist"
        )

    return release_exist


@router.patch("/{id}", response_model=TraffixReleaseRead)
async def update_release(
    db: DatabaseDep, id: int, release_obj_in: TraffixReleaseUpdate
):
    """Update a specific Release in the database."""
    release_exist = await crud.traffix_release.get(db=db, id=id)
    if not release_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Release does not exist"
        )

    if release_obj_in.name and release_obj_in.name != release_exist.name:
        release_already_exist = await crud.traffix_release.get_by_name(
            db=db, name=release_obj_in.name
        )
        if release_already_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Release already exist"
            )

    updated_release = await crud.traffix_release.update(
        db=db, db_obj=release_exist, obj_in=release_obj_in
    )
    return updated_release


@router.delete("/{id}", response_model=TraffixReleaseRead)
async def delete_release(db: DatabaseDep, id: int):
    """Delete a specific Release from the database."""
    release_exist = await crud.traffix_release.get(db=db, id=id)
    if not release_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Release does not exist"
        )

    await crud.traffix_release.remove(db=db, id=id)
    return release_exist
'''
