from fastapi import APIRouter
from app.api.api_v1.endpoints import meta


api_router = APIRouter()
api_router.include_router(meta.router, prefix="/meta", tags=["meta"])
