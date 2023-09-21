from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
import rapidjson as json


# todo: use PostgresDsn from pydantic
engine = create_async_engine(
    f"postgresql+asyncpg://{settings.postgres_username}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}",
    echo=settings.sqlalchemy_echo,
    echo_pool=settings.sqlalchemy_echo_pool,
    pool_pre_ping=settings.sqlalchemy_pool_pre_ping,
    pool_size=settings.sqlalchemy_pool_size,
    json_deserializer=json.loads,
    json_serializer=json.dumps,
    future=True,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)
