import secrets
from typing import List

from pydantic import AnyHttpUrl, PostgresDsn, BaseSettings


# todo: pydantic validation
class Settings(BaseSettings):
    TITLE: str
    DESCRIPTION: str

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: List["AnyHttpUrl"] = []

    DEBUG: bool
    LOG_JSON_FORMAT: bool
    LOG_LEVEL: str

    ZIPKIN_HOST: str
    ZIPKIN_PORT: int = 9411
    ZIPKIN_SERVICE_NAME: str
    ZIPKIN_SAMPLE_RATE: float = 0.1

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None


