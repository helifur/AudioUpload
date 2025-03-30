from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from audioupload.models.base import Base


class AudioFile(Base):
    __tablename__ = "audiofiles"

    file_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column(VARCHAR(100))
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )
