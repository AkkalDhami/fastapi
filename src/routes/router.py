from fastapi import APIRouter

from routes.v1 import auth

from .v1 import health
# from .v1 import auth, todos, users, health

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
# router.include_router(users.router)
# router.include_router(todos.router)

router.include_router(health.router)
