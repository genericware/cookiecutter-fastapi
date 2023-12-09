import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

from app import __version__
from app.api.v1 import routers as api_v1
from app.config import settings

# app
app = FastAPI(
    debug=settings.fastapi_debug,
    title=settings.fastapi_title,
    description=settings.fastapi_description,
    version=__version__,
)

# logging
logger.add(sys.stderr, format=settings.loguru_format, level=settings.loguru_level)

# cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
    expose_headers=settings.cors_expose_headers,
)

# metrics middleware
Instrumentator().instrument(app).expose(app)

# tracing middleware
FastAPIInstrumentor.instrument_app(app)

# app routes
app.include_router(api_v1.router)
