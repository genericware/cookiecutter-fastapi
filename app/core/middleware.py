import time

import structlog
from asgi_correlation_id import correlation_id
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from uvicorn.protocols.utils import get_path_with_query_string

from app.core.config_logging import access_log


# todo: integration with asgi-correlation-id
class AccessLogMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
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
            url = get_path_with_query_string(request.scope)  # fixme: wrong type
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
