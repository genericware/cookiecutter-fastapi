import time

import structlog
from asgi_correlation_id import CorrelationIdMiddleware, correlation_id
import rapidjson as json
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette_prometheus import PrometheusMiddleware, metrics
from starlette_zipkin import ZipkinMiddleware, ZipkinConfig, B3Headers
from uvicorn.protocols.utils import get_path_with_query_string

from app.api.api_v1.api import api_router
from app.core.config import settings
from app import __version__
from app.core.config_logging import setup_logging

# logging
setup_logging(json_logs=settings.LOG_JSON_FORMAT)
access_log: structlog.stdlib.BoundLogger = structlog.stdlib.get_logger("api.access")

# app
app = FastAPI(
    debug=settings.DEBUG,
    title="python-fastapi-app",
    description="Server application for integration testing.",
    version=__version__,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# cors middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# prometheus middleware
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)


# logging middleware
# todo: one-line configuration
@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    """
    Emits essential information for requests.
    :param request: Request
    :param call_next:
    :return: Response
    """
    structlog.contextvars.clear_contextvars()
    request_id = correlation_id.get()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = time.perf_counter_ns()
    response = Response(status_code=500)
    try:
        response = await call_next(request)
    except Exception:
        structlog.stdlib.get_logger("api.error").exception("Uncaught exception")
        raise
    finally:
        process_time = time.perf_counter_ns() - start_time
        status_code = response.status_code
        url = get_path_with_query_string(request.scope)  # fixme: unexpected type
        client_host = request.client.host
        client_port = request.client.port
        http_method = request.method
        http_version = request.scope["http_version"]

        # uvicorn access log format
        client_info = f"{client_host}:{client_port}"
        http_info = f"\"{http_method} {url} HTTP/{http_version}\" {status_code}"
        access_log.info(
            f"{client_info} - {http_info}",
            http={
                "url": str(request.url),
                "status_code": status_code,
                "method": http_method,
                "request_id": request_id,
                "version": http_version,
            },
            network={"client": {"ip": client_host, "port": client_port}},
            duration=process_time,
        )
        response.headers["X-Process-Time"] = str(process_time / 10**9)
        return response

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
