from typing import Any

from constants import HttpStatus

""" 

Usage:
    
    raise NotFoundException("Todo not found")
    raise BadRequestException("Invalid request")
    raise UnauthorizedException("Unauthorized access")
    raise ForbiddenException("Forbidden access")
    raise ConflictException("Conflict error")
    raise ValidationException("Validation error")
    raise InternalServerErrorException("Internal Server Error")

"""


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = HttpStatus.BAD_REQUEST,
        errors: Any = None,
    ):
        self.message = message
        self.status_code = status_code
        self.errors = errors

        super().__init__(message)


class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "Resource not found",
        errors: Any = None,
    ):
        super().__init__(
            message=message,
            status_code=HttpStatus.NOT_FOUND,
            errors=errors,
        )


class BadRequestException(AppException):
    def __init__(
        self,
        message: str = "Bad request",
        errors: Any = None,
    ):
        super().__init__(
            message=message,
            status_code=HttpStatus.BAD_REQUEST,
            errors=errors,
        )


class UnauthorizedException(AppException):
    def __init__(
        self,
        message: str = "Unauthorized",
        errors: Any = None,
    ):
        super().__init__(
            message=message,
            status_code=HttpStatus.UNAUTHORIZED,
            errors=errors,
        )


class ForbiddenException(AppException):
    def __init__(
        self,
        message: str = "Forbidden",
        errors: Any = None,
    ):
        super().__init__(
            message=message,
            status_code=HttpStatus.FORBIDDEN,
            errors=errors,
        )


class ConflictException(AppException):
    def __init__(
        self,
        message: str = "Conflict",
        errors: Any = None,
    ):
        super().__init__(
            message=message,
            status_code=HttpStatus.CONFLICT,
            errors=errors,
        )


class ValidationException(AppException):
    def __init__(
        self,
        message: str = "Validation error",
        errors: Any = None,
    ):
        super().__init__(
            message=message,
            status_code=HttpStatus.UNPROCESSABLE_ENTITY,
            errors=errors,
        )


class InternalServerErrorException(AppException):
    def __init__(
        self,
        message: str = "Internal Server Error",
        errors: Any = None,
    ):
        super().__init__(
            message=message,
            status_code=HttpStatus.INTERNAL_SERVER_ERROR,
            errors=errors,
        )
