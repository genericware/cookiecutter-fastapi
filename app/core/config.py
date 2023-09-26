# Standard Library ---------------------------------------------------------------------
import secrets

# Third-Party --------------------------------------------------------------------------
from dotenv import find_dotenv
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    title: str = "python-fastapi-app"
    description: str = "Gotta go fast."
    api_v1_str: str = "/api/v1"
    secret_key: str = Field(default=secrets.token_urlsafe(32))
    access_token_expire_minutes: int = 3600
    cors_allow_origins: list["AnyHttpUrl"] = []
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["X-Requested-With", "X-Request-ID"]
    cors_expose_headers: list[str] = ["X-Request-ID"]
    debug: bool
    log_json_format: bool
    log_level: str
    sqlalchemy_echo: bool
    sqlalchemy_echo_pool: bool
    sqlalchemy_pool_pre_ping: bool
    sqlalchemy_pool_size: int
    postgres_db: str
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    otel_excluded_urls: str = "client/.*/info,healthcheck"

    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env"), env_file_encoding="utf-8"
    )


settings = Settings()
