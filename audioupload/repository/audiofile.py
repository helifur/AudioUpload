from audioupload.models.audiofile import AudioFile
from audioupload.repository.base import BaseRepository


class AudioFileRepository(BaseRepository):
    model = AudioFile
