from audioupload.models.role import Role
from audioupload.repository.base import BaseRepository


class RoleRepository(BaseRepository):
    model = Role
