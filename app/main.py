from asgi_correlation_id import CorrelationIdMiddleware
import rapidjson as json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_prometheus import PrometheusMiddleware, metrics
from starlette_zipkin import ZipkinMiddleware, ZipkinConfig, B3Headers

from app.api.api_v1.api import api_router
from app.api.deps import create_db_and_tables
from app.core.config import settings
from app import __version__
from app.middleware.access_log import AccessLogMiddleware

# app
app = FastAPI(
    debug=settings.DEBUG,
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
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
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
        host=settings.ZIPKIN_HOST,
        port=settings.ZIPKIN_PORT,
        service_name=settings.ZIPKIN_SERVICE_NAME,
        sample_rate=settings.ZIPKIN_SAMPLE_RATE,
        inject_response_headers=True,
        force_new_trace=False,
        json_encoder=json.dumps,
        header_formatter=B3Headers,
    ),
)
