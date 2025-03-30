import os

import sqlalchemy.exc as exc
import sqlalchemy.orm as orm
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

__factory = None
load_dotenv()


async def global_init() -> None:
    """Initialize a database"""
    global __factory

    if __factory:
        return

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")

    engine = create_async_engine(
        f"postgresql+asyncpg://{user}:{password}@172.26.0.3:5432/{db_name}"
    )

    __factory = async_sessionmaker(bind=engine)

    from ..models import __all_models

    async with engine.begin() as conn:
        await conn.run_sync(__all_models.base.Base.metadata.create_all)


async def create_session() -> AsyncSession:
    """Create a session"""
    global __factory
    return __factory()
