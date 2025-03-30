from sqlalchemy import update

from audioupload.database.db_init import create_session
from audioupload.models.user import User
from audioupload.repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    @classmethod
    async def update(cls, id_, **values):
        async with await create_session() as session:
            query = (
                update(cls.model)
                .filter_by(user_id=id_)
                .values(**values)
                .returning(cls.model.user_id)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar()
