import uvicorn

from app.config import settings
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        workers=settings.uvicorn_workers,
        log_level=settings.uvicorn_log_level,
        loop=settings.uvicorn_loop,
        http=settings.uvicorn_http,
        ws=settings.uvicorn_ws,
        interface=settings.uvicorn_interface,
        backlog=settings.uvicorn_backlog,
        timeout_keep_alive=settings.uvicorn_timeout_keep_alive,
        timeout_graceful_shutdown=settings.uvicorn_timeout_graceful_shutdown,
    )
