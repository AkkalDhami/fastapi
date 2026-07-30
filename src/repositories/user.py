from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models import UserModel


class UserRepository:
    def create(
        self,
        db: Session,
        user: UserModel,
    ) -> UserModel:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> UserModel | None:

        return db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_id(
        self,
        db: Session,
        user_id: int,
    ) -> UserModel | None:
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def update_last_login(
        db: Session,
        user: UserModel,
    ) -> UserModel:

        user.last_login = datetime.now(timezone.utc) # pyright: ignore[reportAttributeAccessIssue]

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
