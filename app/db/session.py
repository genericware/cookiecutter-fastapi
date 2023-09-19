from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
import rapidjson as json


engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=settings.SQLALCHEMY_ECHO,
    echo_pool=settings.SQLALCHEMY_ECHO_POOL,
    pool_pre_ping=settings.SQLALCHEMY_POOL_PRE_PING,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    json_deserializer=json.loads,
    json_serializer=json.dumps,
    future=True
)
async_session = async_sessionmaker(engine)
