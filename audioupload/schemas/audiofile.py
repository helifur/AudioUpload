from pydantic import BaseModel


class AudioFileSchema(BaseModel):
    file_id: int | None = None
    path: str | None = None
    owner_id: int | None = None
