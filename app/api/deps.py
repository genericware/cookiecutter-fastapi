from collections.abc import AsyncGenerator, AsyncIterator
from uuid import UUID

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base
from app.db.session import async_session, engine
from app.models import User
from app.models.user import OAuthAccount


async def create_db_and_tables() -> None:
    """
    Create database and tables.

    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Retrieve an async database session.

    :return:
    """
    async with async_session() as session:
        yield session


async def get_user_db(
    session: AsyncSession = Depends(get_db),
) -> AsyncIterator[SQLAlchemyUserDatabase[User, UUID]]:
    """
    Retrieve the user database.

    :param session:
    :return:
    """
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)
