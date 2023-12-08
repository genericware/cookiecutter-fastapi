from collections.abc import Sequence
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    """Item create, read, update, delete actions."""

    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: schemas.ItemCreate, owner_id: UUID
    ) -> models.Item:
        """
        Create an Item that is owned by a User.

        :param db:
        :param obj_in:
        :param owner_id:
        :return:
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[models.Item]:
        """
        Retrieve items that are owned by a User.

        :param db:
        :param owner_id:
        :param skip:
        :param limit:
        :return:
        """
        result = await db.execute(
            select(self.model)
            .where(self.model.id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


item = CRUDItem(models.Item)
