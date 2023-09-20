from typing import Generator, AsyncGenerator

import structlog
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from structlog.stdlib import BoundLogger
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base
from app.db.session import async_session, engine
from app.models import User

log: BoundLogger = structlog.get_logger(__name__)


async def get_db() -> Generator[AsyncSession]:
    """todo"""
    db: AsyncSession | None = None
    try:
        db = async_session()
        yield db
    finally:
        if db is not None:
            await db.close()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# todo: combine with get_db(...)
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
