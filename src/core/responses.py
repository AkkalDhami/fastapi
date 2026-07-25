from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from constants.http_status import HttpStatus
from schemas.response import ApiResponse, ErrorResponse


class ResponseHandler:
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = HttpStatus.OK,
        cookies: list[dict] | None = None,
    ) -> JSONResponse:

        body = ApiResponse(
            status_code=status_code,
            success=True,
            message=message,
            data=data,
        )

        response = JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(body),
        )

        if cookies:
            for cookie in cookies:
                response.set_cookie(**cookie)

        return response

    @staticmethod
    def error(
        message: str = "Something went wrong",
        status_code: int = HttpStatus.BAD_REQUEST,
        errors: Any = None,
    ) -> JSONResponse:

        body = ErrorResponse(
            status_code=status_code,
            success=False,
            message=message,
            errors=errors,
        )

        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(body),
        )
