from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session


def get_db() -> Generator:
    db: AsyncSession | None = None
    try:
        db = async_session()
        yield db
    finally:
        if db is None:
            # todo: logging
            ...
        else:
            db.close()
