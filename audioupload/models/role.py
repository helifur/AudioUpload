from sqlalchemy import VARCHAR
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from audioupload.models.base import Base


class Role(Base):
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(20))
