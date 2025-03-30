from audioupload.models.role import Role
from audioupload.repository.base import BaseRepository
from audioupload.schemas.role import RoleSchema


class RoleRepository(BaseRepository):
    model = Role
    model_schema = RoleSchema
