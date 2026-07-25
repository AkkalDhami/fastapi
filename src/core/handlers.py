from fastapi import Request
from fastapi.responses import JSONResponse

from core.exceptions import AppException


async def app_exception_handler(
    _: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "success": False,
            "message": exc.message,
            "errors": exc.errors,
        },
    )
