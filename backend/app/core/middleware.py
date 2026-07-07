import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        logger.info(
            f"Request started | request_id={request_id} | "
            f"method={request.method} | path={request.url.path}"
        )

        response = await call_next(request)

        process_time = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"Request completed | request_id={request_id} | "
            f"status_code={response.status_code} | time_ms={process_time}"
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-MS"] = str(process_time)

        return response