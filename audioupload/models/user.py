from sqlalchemy import VARCHAR
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from audioupload.models.base import Base
from audioupload.models.role import Role


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(VARCHAR(20))
    first_name: Mapped[str] = mapped_column(VARCHAR(20))
    last_name: Mapped[str] = mapped_column(VARCHAR(20))
    role_id: Mapped["Role"] = relationship()
