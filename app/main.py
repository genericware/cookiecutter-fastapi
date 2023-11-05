# Third-Party --------------------------------------------------------------------------
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

# Project ------------------------------------------------------------------------------
from app import __version__
from app.api.api_v1.api import api_router
from app.api.deps import create_db_and_tables
from app.core.config import settings
from app.middleware.access_log import AccessLogMiddleware

# app
app = FastAPI(
    debug=settings.debug,
    title=settings.title,
    description=settings.description,
    version=__version__,
)

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

# log middleware
app.add_middleware(AccessLogMiddleware)

# correlation middleware
app.add_middleware(CorrelationIdMiddleware)

# tracing middleware
FastAPIInstrumentor.instrument_app(app)

# app routes
app.include_router(api_router, prefix=settings.api_v1_str)


# app start
@app.on_event("startup")
async def _startup():
    """
    Application start up hook.

    :return:
    """
    await create_db_and_tables()
