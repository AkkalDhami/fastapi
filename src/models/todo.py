from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from configs.database import Base
from models.base import TimestampMixin


if TYPE_CHECKING:
    from models.user import UserModel


class TodoModel(TimestampMixin, Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    user: Mapped["UserModel"] = relationship(
        back_populates="todos",
    )
