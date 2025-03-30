from sqlalchemy import delete

from audioupload.database.db_init import create_session
from audioupload.models.role import Role
from audioupload.repository.base import BaseRepository
from audioupload.schemas.role import RoleSchema


class RoleRepository(BaseRepository):
    model = Role
    model_schema = RoleSchema

    @classmethod
    async def delete(cls, name_) -> bool:
        async with await create_session() as session:
            query = delete(cls.model).filter_by(name=name_)
            await session.execute(query)
            await session.commit()
            return True
