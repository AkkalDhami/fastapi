import time

from fastapi import APIRouter

from configs import settings, START_TIME

from schemas import ApiResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "/",
    response_model=ApiResponse[dict],
)
def health_check():
    uptime = int(time.time() - START_TIME)
    return ApiResponse(
        status_code=200,
        success=True,
        message="Service is healthy",
        data={
            "status": "ok",
            "app_name": settings.APP_NAME,
            "environment": settings.APP_ENV,
            "version": settings.APP_VERSION,
            "uptime": uptime,
        },
    )
