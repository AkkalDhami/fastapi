from fastapi import FastAPI

from configs import settings
from core.exceptions import AppException
from core.handlers import app_exception_handler
from lifespan import lifespan
from routes.router import router

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)


app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.include_router(router)
