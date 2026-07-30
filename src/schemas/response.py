from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    status_code: int
    success: bool
    message: str
    data: T | None = None
    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel, Generic[T]):
    status_code: int
    success: bool = False
    message: str
    errors: T | None = None
