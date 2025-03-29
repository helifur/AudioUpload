from abc import ABC, abstractmethod

from sqlalchemy import delete, insert, select, update

from audioupload.database.db_init import create_session


class AbstractRepository(ABC):
    @staticmethod
    @abstractmethod
    async def get_all(**filter_by):
        pass

    @staticmethod
    @abstractmethod
    async def get_one_or_none(**filter_by):
        pass


class BaseRepository(AbstractRepository):
    model = None

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with await create_session() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            mapping_result = result.mappings().one_or_none()
            return mapping_result if mapping_result else None

    @classmethod
    async def insert(cls, **values) -> None:
        async with await create_session() as session:
            query = insert(cls.model).values(**values)
            result = await session.execute(query)
            await session.commit()
