import secrets
from enum import Enum
from typing import Literal, Optional

from pydantic import AnyHttpUrl, Field, field_validator, ValidationInfo, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIPrefix(str, Enum):
    """API prefixes."""

    v1 = "/api/v1"
    auth = "/auth"
    users = "/users"
    items = "/items"


class APITags(str, Enum):
    """API tags."""

    auth = "auth"
    users = "users"
    items = "items"


class DatabaseScheme(str, Enum):
    """Database schemes."""

    asyncpg = "postgresql+asyncpg"


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=(".env.development", ".env"))

    uvicorn_host: str = Field(...)
    uvicorn_port: int = Field(...)
    uvicorn_workers: int = Field(...)
    uvicorn_log_level: str = Field(...)
    uvicorn_loop: Literal["none", "auto", "asyncio", "uvloop"] = Field(...)
    uvicorn_http: Literal["auto", "h11", "httptools"] = Field(...)
    uvicorn_ws: Literal["auto", "none", "websockets"] = Field(...)
    uvicorn_interface: Literal["auto", "asgi3", "asgi2", "wsgi"] = Field(...)
    uvicorn_backlog: int = Field(...)
    uvicorn_timeout_keep_alive: int = Field(...)
    uvicorn_timeout_graceful_shutdown: int = Field(...)
    fastapi_debug: bool = Field(...)
    fastapi_title: str = Field(...)
    fastapi_description: str = Field(...)
    fastapi_secret_key: str = Field(default=secrets.token_urlsafe(32))
    fastapi_access_token_expire_minutes: int = Field(...)
    cors_allow_origins: list["AnyHttpUrl"] = Field(...)
    cors_allow_credentials: bool = Field(...)
    cors_allow_methods: list[str] = Field(...)
    cors_allow_headers: list[str] = Field(...)
    cors_expose_headers: list[str] = Field(...)
    sqlalchemy_echo: bool = Field(...)
    sqlalchemy_echo_pool: bool = Field(...)
    sqlalchemy_pool_pre_ping: bool = Field(...)
    sqlalchemy_pool_size: int = Field(...)
    sqlalchemy_max_overflow: int = Field(...)
    sqlalchemy_pool_recycle: int = Field(...)
    sqlalchemy_pool_timeout: int = Field(...)
    sqlalchemy_insertmanyvalues_page_size: int = Field(...)
    sqlalchemy_scheme: str = Field(DatabaseScheme.asyncpg)
    sqlalchemy_db: str = Field(...)
    sqlalchemy_host: str = Field(...)
    sqlalchemy_port: int = Field(...)
    sqlalchemy_user: str = Field(...)
    sqlalchemy_password: str = Field(...)
    sqlalchemy_dsn: PostgresDsn | str | None = Field(...)
    loguru_format: str = Field(...)
    loguru_level: str = Field(...)

    @field_validator("sqlalchemy_dsn", mode="before")
    @classmethod
    def build_sqlalchemy_dsn(cls, v: str | None, info: ValidationInfo) -> str | PostgresDsn:

        if isinstance(v, str):
            return v

        return PostgresDsn.build(
                scheme=info.data["sqlalchemy_scheme"],
                username=info.data["sqlalchemy_username"],
                password=info.data["sqlalchemy_password"],
                host=info.data["sqlalchemy_host"],
                port=info.data["sqlalchemy_port"],
                path=info.data["sqlalchemy_path"]
            )


settings = Settings()
