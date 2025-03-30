from sqlalchemy import delete, update

from audioupload.database.db_init import create_session
from audioupload.models.user import User
from audioupload.repository.base import BaseRepository
from audioupload.schemas.user import UserSchema


class UserRepository(BaseRepository):
    model = User
    model_schema = UserSchema

    @classmethod
    async def update(cls, id_, **values) -> int:
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

    @classmethod
    async def delete(cls, id_) -> bool:
        async with await create_session() as session:
            query = delete(cls.model).filter_by(user_id=id_)
            await session.execute(query)
            await session.commit()
            return True
