from audioupload.models.audiofile import AudioFile
from audioupload.repository.base import BaseRepository
from audioupload.schemas.audiofile import AudioFileSchema


class AudioFileRepository(BaseRepository):
    model = AudioFile
    model_schema = AudioFileSchema
