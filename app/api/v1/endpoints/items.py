from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.db.users import current_active_user

router = APIRouter()


@router.get("/", response_model=list[schemas.Item])
async def read_items(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.UserRead = Depends(current_active_user),
) -> Any:
    """Read items."""
    if current_user.is_superuser:
        items = await crud.item.get_multi(db=db, skip=skip, limit=limit)
    else:
        items = await crud.item.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return items


@router.post("/", response_model=schemas.Item)
async def create_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
    current_user: schemas.UserRead = Depends(current_active_user),
) -> Any:
    """Create an item."""
    item = await crud.item.create_with_owner(
        db=db, obj_in=item_in, owner_id=current_user.id
    )
    return item


@router.put("/{id}", response_model=schemas.Item)
async def update_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    item_in: schemas.ItemUpdate,
    current_user: schemas.UserRead = Depends(current_active_user),
) -> Any:
    """Update an item."""
    item = await crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404)
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400)
    item = await crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}", response_model=schemas.Item)
async def read_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: schemas.UserRead = Depends(current_active_user),
) -> Any:
    """Read an item."""
    item = await crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404)
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400)
    return item


@router.get("/{id}", response_model=schemas.Item)
async def delete_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: schemas.UserRead = Depends(current_active_user),
) -> Any:
    """Delete an item."""
    item = await crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404)
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400)
    item = await crud.item.remove(db=db, id=id)
    return item
