import rapidjson as json
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_prometheus import PrometheusMiddleware, metrics
from starlette_zipkin import B3Headers, ZipkinConfig, ZipkinMiddleware

from app import __version__
from app.api.api_v1.api import api_router
from app.api.deps import create_db_and_tables
from app.core.config import settings
from app.middleware.access_log import AccessLogMiddleware

# app
app = FastAPI(
    debug=settings.debug,
    title="python-fastapi-app",
    description="Server application for integration testing.",
    version=__version__,
)


@app.on_event("startup")
async def on_startup():
    # todo: use alembic instead
    await create_db_and_tables()


# app api routes
app.include_router(api_router, prefix="/api/v1")

# cors middleware
if settings.backend_cors_origin:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.backend_cors_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["X-Requested-With", "X-Request-ID"],
        expose_headers=["X-Request-ID"],
    )

# prometheus middleware
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)


# logging middleware
app.add_middleware(AccessLogMiddleware)

# correlation middleware
app.add_middleware(CorrelationIdMiddleware)

# zipkin middleware
# fixme: https://github.com/mchlvl/starlette-zipkin/issues/42
app.add_middleware(
    ZipkinMiddleware,
    config=ZipkinConfig(
        host=settings.zipkin_host,
        port=settings.zipkin_port,
        service_name=settings.zipkin_service_name,
        sample_rate=settings.zipkin_sample_rate,
        inject_response_headers=True,
        force_new_trace=False,
        json_encoder=json.dumps,
        header_formatter=B3Headers,
    ),
)
