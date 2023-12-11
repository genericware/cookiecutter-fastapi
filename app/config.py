import secrets
from enum import Enum
from typing import Literal

from pydantic import AnyHttpUrl, Field, PostgresDsn, ValidationInfo, field_validator
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

    uvicorn_host: str
    uvicorn_port: int
    uvicorn_workers: int
    uvicorn_log_level: Literal["critical", "error", "warning", "info", "debug", "trace"]
    uvicorn_loop: Literal["none", "auto", "asyncio", "uvloop"]
    uvicorn_http: Literal["auto", "h11", "httptools"]
    uvicorn_ws: Literal["auto", "none", "websockets"]
    uvicorn_interface: Literal["auto", "asgi3", "asgi2", "wsgi"]
    uvicorn_backlog: int
    uvicorn_timeout_keep_alive: int
    uvicorn_timeout_graceful_shutdown: int
    fastapi_debug: bool
    fastapi_title: str
    fastapi_description: str
    fastapi_secret_key: str = Field(default=secrets.token_urlsafe(32))
    fastapi_access_token_expire_minutes: int
    oauth_name: str
    oauth_client_id: str
    oauth_client_secret: str
    oauth_authorize_endpoint: str
    oauth_access_token_endpoint: str
    oauth_refresh_token_endpoint: str | None
    oauth_revoke_token_endpoint: str | None
    cors_allow_origins: list["AnyHttpUrl"]
    cors_allow_credentials: bool
    cors_allow_methods: list[str]
    cors_allow_headers: list[str]
    cors_expose_headers: list[str]
    sqlalchemy_echo: bool
    sqlalchemy_echo_pool: bool
    sqlalchemy_pool_pre_ping: bool
    sqlalchemy_pool_size: int
    sqlalchemy_max_overflow: int
    sqlalchemy_pool_recycle: int
    sqlalchemy_pool_timeout: int
    sqlalchemy_insertmanyvalues_page_size: int
    sqlalchemy_scheme: str
    sqlalchemy_username: str
    sqlalchemy_password: str
    sqlalchemy_host: str
    sqlalchemy_port: int
    sqlalchemy_path: str
    sqlalchemy_dsn: PostgresDsn | str | None = Field(None)
    loguru_format: str
    loguru_level: str
    prometheus_instrumentator_should_group_status_codes: bool
    prometheus_instrumentator_should_ignore_untemplated: bool
    prometheus_instrumentator_should_respect_env_var: bool
    prometheus_instrumentator_should_instrument_requests_in_progress: bool
    prometheus_instrumentator_excluded_handlers: list[str]
    prometheus_instrumentator_env_var_name: str
    prometheus_instrumentator_enable: bool
    prometheus_instrumentator_inprogress_name: str
    prometheus_instrumentator_inprogress_labels: bool
    prometheus_instrumentator_include_in_schema: bool
    prometheus_instrumentator_should_gzip: bool
    # otel_service_name: str
    # otel_traces_exporter: str
    # otel_metrics_exporters: str
    otel_instrumentation_http_capture_headers_server_request: str
    otel_instrumentation_http_capture_headers_server_response: str

    @field_validator("sqlalchemy_dsn", mode="before")
    @classmethod
    def build_sqlalchemy_dsn(
        cls, v: str | None, info: ValidationInfo
    ) -> str | PostgresDsn:
        """
        Build SQLAlchemy's DSN.

        :param v:
        :param info:
        :return:
        """
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme=info.data["sqlalchemy_scheme"],
            username=info.data["sqlalchemy_username"],
            password=info.data["sqlalchemy_password"],
            host=info.data["sqlalchemy_host"],
            port=info.data["sqlalchemy_port"],
            path=info.data["sqlalchemy_path"],
        )


settings = Settings()
