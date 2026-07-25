from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Todo API - FastAPI"

    APP_ENV: str

    PORT: int = Field(default=8000, gt=0, lt=65536)

    APP_VERSION: str

    DEBUG: bool = True

    DATABASE_URL: str

    JWT_ACCESS_SECRET: str = Field(min_length=32)

    JWT_REFRESH_SECRET: str = Field(min_length=32)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
