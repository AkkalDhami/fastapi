from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from configs import get_db
from constants import HttpStatus
from core import ResponseHandler
from schemas import ApiResponse, LoggedinUser, LoginRequest, User, UserCreate
from schemas.user import BaseLoggedinUser
from services import auth_service
from utils.helpers import get_current_user_id

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=ApiResponse[User])
def create_user(user: UserCreate, db: Session = Depends(get_db)):  # noqa: B008
    new_user = auth_service.register(db, user)

    user_response = User.model_validate(new_user)

    return ResponseHandler.success(
        data=user_response,
        message="User created successfully",
        status_code=HttpStatus.CREATED,
    )


@router.post(
    "/login",
    response_model=ApiResponse[LoggedinUser],
)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),  # noqa: B008
):

    result = auth_service.login(
        db,
        payload.email,
        payload.password,
    )

    user_response = BaseLoggedinUser.model_validate(result["user"])

    # response.set_cookie(
    #     key="access_token",
    #     value=result["access_token"],
    #     httponly=True,
    #     secure=True,  # HTTPS only (disable in local dev)
    #     samesite="lax",
    #     max_age=60 * 15,  # 15 minutes
    # )

    # response.set_cookie(
    #     key="refresh_token",
    #     value=result["refresh_token"],
    #     httponly=True,
    #     secure=True,
    #     samesite="lax",
    #     max_age=60 * 60 * 24 * 7,  # 7 days
    # )

    return ResponseHandler.success(
        data={
            "user": user_response,
            "access_token": result["access_token"],
        },
        cookies=[
            {
                "key": "access_token",
                "value": result["access_token"],
                "httponly": True,
                "secure": False,  # localhost
                "samesite": "lax",
                "max_age": 60 * 15,
            },
            {
                "key": "refresh_token",
                "value": result["refresh_token"],
                "httponly": True,
                "secure": False,
                "samesite": "lax",
                "max_age": 60 * 60 * 24 * 7,
            },
        ],
        message="Login successful",
    )


@router.get("/profile")
def profile(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),  # noqa: B008
):

    user = auth_service.get_profile(db, user_id)

    return ResponseHandler.success(
        data=User.model_validate(user),
        message="Profile fetched successfully",
    )
