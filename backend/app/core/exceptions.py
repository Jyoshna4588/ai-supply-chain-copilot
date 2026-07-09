from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logger import logger


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled error | path={request.url.path} | error={str(exc)}",
        exc_info=True,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong while processing the request",
            "status_code": 500,
        },
    )