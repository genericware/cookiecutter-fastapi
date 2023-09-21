import secrets
from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = secrets.token_urlsafe(32)
    access_token_expire_minutes: int
    backend_cors_origin: List["AnyHttpUrl"] = []
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
    postgres_username: str
    postgres_password: str
    zipkin_service_name: str
    zipkin_host: str
    zipkin_port: int = 9411
    zipkin_sample_rate: float = 0.1


settings = Settings()
