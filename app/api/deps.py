from typing import AsyncGenerator

import structlog
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from structlog.stdlib import BoundLogger
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base
from app.db.session import async_session, engine
from app.models import User

log: BoundLogger = structlog.get_logger(__name__)


async def create_db_and_tables():
    """todo"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """todo"""
    async with async_session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_db)):
    """todo"""
    yield SQLAlchemyUserDatabase(session, User)
