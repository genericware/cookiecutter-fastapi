# Third-Party --------------------------------------------------------------------------
import rapidjson as json
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Project ------------------------------------------------------------------------------
from app.core.config import settings

engine = create_async_engine(
    PostgresDsn.build(
        scheme="postgresql+asyncpg",  # todo: enum
        username=settings.postgres_user,
        password=settings.postgres_password,
        host=settings.postgres_host,
        port=settings.postgres_port,
        path=f"/{settings.postgres_db or ''}",
    ),
    echo=settings.sqlalchemy_echo,
    echo_pool=settings.sqlalchemy_echo_pool,
    pool_pre_ping=settings.sqlalchemy_pool_pre_ping,
    pool_size=settings.sqlalchemy_pool_size,
    json_deserializer=json.loads,
    json_serializer=json.dumps,
    future=True,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)
