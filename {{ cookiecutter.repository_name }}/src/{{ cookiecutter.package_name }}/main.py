import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

from app import __version__
from app.api.v1 import routers as api_v1
from app.config import settings, setup_logging

# logging
setup_logging(log_level=settings.loguru_level, json_logs=settings.loguru_serialize)

# app
app = FastAPI(
    debug=settings.fastapi_debug,
    title=settings.fastapi_title,
    description=settings.fastapi_description,
    version=__version__,
)

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
    expose_headers=settings.cors_expose_headers,
)

# prometheus
Instrumentator(
    should_group_status_codes=settings.prometheus_instrumentator_should_group_status_codes,
    should_ignore_untemplated=settings.prometheus_instrumentator_should_ignore_untemplated,
    should_respect_env_var=settings.prometheus_instrumentator_should_respect_env_var,
    should_instrument_requests_inprogress=settings.prometheus_instrumentator_should_instrument_requests_in_progress,
    excluded_handlers=settings.prometheus_instrumentator_excluded_handlers,
    env_var_name=settings.prometheus_instrumentator_env_var_name,
    inprogress_name=settings.prometheus_instrumentator_inprogress_name,
    inprogress_labels=settings.prometheus_instrumentator_inprogress_labels,
).instrument(app).expose(
    app,
    include_in_schema=settings.prometheus_instrumentator_include_in_schema,
    should_gzip=settings.prometheus_instrumentator_should_gzip,
)

# opentelemetry
FastAPIInstrumentor.instrument_app(app)

# routers
app.include_router(api_v1.router)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        workers=settings.uvicorn_workers,
        log_config=settings.uvicorn_log_config,
        loop=settings.uvicorn_loop,
        http=settings.uvicorn_http,
        ws=settings.uvicorn_ws,
        interface=settings.uvicorn_interface,
        backlog=settings.uvicorn_backlog,
        timeout_keep_alive=settings.uvicorn_timeout_keep_alive,
        timeout_graceful_shutdown=settings.uvicorn_timeout_graceful_shutdown,
    )
