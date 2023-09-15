from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings

engine = create_async_engine(
    ...,  # fixme
    echo=settings.SQLALCHEMY_ECHO,
    # pool_pre_ping=settings.SQLALCHEMY_POOL_PRE_PING,
    # pool_size=settings.SQLALCHEMY_POOL_SIZE,
    # max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
    poolclass=NullPool,
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
