import secrets

from dotenv import find_dotenv
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str = Field(default=secrets.token_urlsafe(32))
    access_token_expire_minutes: int
    backend_cors_origins: list["AnyHttpUrl"]
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
    zipkin_service_name: str
    zipkin_host: str
    zipkin_port: int = 9411
    zipkin_sample_rate: float = 0.1

    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env"), env_file_encoding="utf-8"
    )


settings = Settings()
