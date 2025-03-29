from sqlalchemy import VARCHAR
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from audioupload.models.base import Base
from audioupload.models.user import User


class AudioFile(Base):
    __tablename__ = "audiofiles"

    file_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column(VARCHAR(20))
    owner_id: Mapped["User"] = relationship()
