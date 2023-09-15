from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/ping")
async def ping():
    return PlainTextResponse()


@router.head("/ping", response_class=Response)
async def head_ping():
    return
