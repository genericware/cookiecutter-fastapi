# Standard Library ---------------------------------------------------------------------
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

# Third-Party --------------------------------------------------------------------------
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Project ------------------------------------------------------------------------------
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base create, read, update, and delete actions."""

    def __init__(self, model: type[ModelType]):
        """
        Object with default database actions.

        :param model:
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> ModelType | None:
        """
        Retrieve a row.

        :param db:
        :param id:
        :return:
        """
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.unique().scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> Sequence[ModelType]:
        """
        Retrieve rows.

        :param db:
        :param skip:
        :param limit:
        :return:
        """
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a row.

        :param db:
        :param obj_in:
        :return:
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        """
        Update a row.

        :param db:
        :param db_obj:
        :param obj_in:
        :return:
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: Any) -> ModelType:
        """
        Remove a row.

        :param db:
        :param id:
        :return:
        """
        result = await db.execute(select(self.model).where(self.model.id == id))
        db_obj = result.scalar_one()
        await db.delete(db_obj)
        await db.commit()
        return db_obj
