from sqlalchemy import INTEGER, VARCHAR, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from audioupload.models.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    yandex_user_id: Mapped[int] = mapped_column(INTEGER, unique=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(20))
    last_name: Mapped[str] = mapped_column(VARCHAR(20))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id"))
