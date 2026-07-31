from sqlalchemy.orm import Session

from core import (
    ConflictException,
    UnauthorizedException,
    hash_password,
    verify_password,
)
from core.exceptions import NotFoundException
from core.jwt import create_access_token, create_refresh_token
from models import UserModel
from repositories import UserRepository
from schemas import UserCreate


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    def register(
        self,
        db: Session,
        user_data: UserCreate,
    ) -> UserModel:

        existing_user = self.user_repository.get_by_email(
            db,
            user_data.email,
        )

        if existing_user:
            raise ConflictException("Email already exists")

        user = UserModel(
            name=user_data.name,
            email=user_data.email,
            password=hash_password(user_data.password),
        )

        return self.user_repository.create(
            db,
            user,
        )

    def login(
        self,
        db: Session,
        email: str,
        password: str,
    ):

        user = self.user_repository.get_by_email(db, email)

        if not user:
            raise UnauthorizedException("Invalid email or password")

        # if not user.is_verified:
        #     raise UnauthorizedException("Email is not verified")

        is_valid = verify_password(
            user.password,
            password,
        )

        if not is_valid:
            raise UnauthorizedException("Invalid email or password")

        user = self.user_repository.update_last_login(
            db,
            user,
        )

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
            }
        )

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def get_profile(
        self,
        db: Session,
        user_id: int,
    ) -> UserModel:

        user = self.user_repository.get_by_id(db, user_id)

        if not user:
            raise NotFoundException("User not found")

        return user
