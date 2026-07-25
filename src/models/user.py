import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from configs.database import Base
from models.base import TimestampMixin


if TYPE_CHECKING:
    from models.todo import TodoModel


class UserModel(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    last_login: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )

    todos: Mapped[list["TodoModel"]] = relationship(back_populates="user")
