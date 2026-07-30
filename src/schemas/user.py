from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class User(BaseModel):
    id: int
    name: str
    email: str
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BaseLoggedinUser(BaseModel):
    id: int
    name: str
    email: str
    is_verified: bool
    last_login: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoggedinUser(BaseModel):
    user: BaseLoggedinUser
    tokens: TokenResponse
