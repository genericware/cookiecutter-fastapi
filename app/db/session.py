import orjson as json
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings

engine = create_async_engine(
    url=settings.sqlalchemy_url,
    echo=settings.sqlalchemy_echo,
    echo_pool=settings.sqlalchemy_echo_pool,
    pool_pre_ping=settings.sqlalchemy_pool_pre_ping,
    pool_size=settings.sqlalchemy_pool_size,
    max_overflow=settings.sqlalchemy_max_overflow,
    pool_recycle=settings.sqlalchemy_pool_recycle,
    pool_timeout=settings.sqlalchemy_pool_timeout,
    insertmanyvalues_page_size=settings.sqlalchemy_insertmanyvalues_page_size,
    json_deserializer=json.loads,
    json_serializer=json.dumps,
    future=True,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)
