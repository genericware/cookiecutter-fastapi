from fastapi import FastAPI
from app.core.config import settings
from app import __version__

# app
app = FastAPI(
    debug=settings.DEBUG,
    title=settings.NAME,
    description=settings.DESCRIPTION,
    version=__version__
)

# routes
app.include_router(app_router)
