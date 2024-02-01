from collections.abc import AsyncGenerator, AsyncIterator
from uuid import UUID

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.user import OAuthAccount

from app.db.session import async_session
from app.models import User


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
