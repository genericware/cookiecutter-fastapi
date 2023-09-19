import secrets
from typing import List

from pydantic import AnyHttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


# todo: pydantic validation
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    BACKEND_CORS_ORIGINS: List["AnyHttpUrl"] = []
    DEBUG: bool
    LOG_JSON_FORMAT: bool
    LOG_LEVEL: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None
    SQLALCHEMY_ECHO: bool
    SQLALCHEMY_ECHO_POOL: bool
    SQLALCHEMY_POOL_PRE_PING: bool
    SQLALCHEMY_POOL_SIZE: int
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    ZIPKIN_SERVICE_NAME: str
    ZIPKIN_HOST: str
    ZIPKIN_PORT: int = 9411
    ZIPKIN_SAMPLE_RATE: float = 0.1

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
