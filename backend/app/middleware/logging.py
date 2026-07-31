from __future__ import annotations

import logging
from time import perf_counter

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.middleware.request_id import get_request_id


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger("cyberfusion.request")
        started_at = perf_counter()
        response = None
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            elapsed_ms = (perf_counter() - started_at) * 1000
            logger.info(
                "%s %s -> %s in %.2f ms",
                request.method,
                request.url.path,
                status_code,
                elapsed_ms,
                extra={"request_id": get_request_id()},
            )
            if response is not None:
                response.headers["X-Process-Time"] = f"{elapsed_ms:.2f}ms"
