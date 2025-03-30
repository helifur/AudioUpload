from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from audioupload.models.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    yandex_user_id: Mapped[str] = mapped_column(VARCHAR(20), unique=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(20))
    last_name: Mapped[str] = mapped_column(VARCHAR(20))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id"))

    audiofile = relationship("AudioFile", cascade="all, delete")
