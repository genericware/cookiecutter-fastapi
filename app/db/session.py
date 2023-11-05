# Third-Party --------------------------------------------------------------------------
import rapidjson as json
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Project ------------------------------------------------------------------------------
from app.core.config import settings

engine = create_async_engine(
    str(settings.db_url()),
    echo=settings.sqlalchemy_echo,
    echo_pool=settings.sqlalchemy_echo_pool,
    pool_pre_ping=settings.sqlalchemy_pool_pre_ping,
    pool_size=settings.sqlalchemy_pool_size,
    json_deserializer=json.loads,
    json_serializer=json.dumps,
    future=True,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)
