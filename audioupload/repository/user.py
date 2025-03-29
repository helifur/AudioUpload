from audioupload.models.user import User
from audioupload.repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User
