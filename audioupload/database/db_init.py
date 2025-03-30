import asyncio
import logging
import os
import subprocess

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

load_dotenv()

__factory = None


async def run_migrations():
    """Alembic migrations"""
    process = await asyncio.create_subprocess_exec(
        "alembic",
        "upgrade",
        "head",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        logging.info("Migrations completed successfully.")
    else:
        logging.error(f"Migration failed: {stderr.decode()}")


async def revert_migrations():
    process = await asyncio.create_subprocess_exec(
        "alembic",
        "downgrade",
        "-1",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        logging.info("Migrations downgraded successfully.")
    else:
        logging.error(f"Migration downgrading failed: {stderr.decode()}")


async def global_init() -> None:
    """Initialize a database"""
    global __factory

    if __factory:
        return

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    try:
        engine = create_async_engine(
            f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
        )
    except Exception as e:
        logging.error(f"Database initializing error! ERR: {e}")

    __factory = async_sessionmaker(bind=engine)

    from ..models import __all_models

    async with engine.begin() as conn:
        await conn.run_sync(__all_models.base.Base.metadata.create_all)

    await run_migrations()


async def create_session() -> AsyncSession:
    """Create a session"""
    global __factory
    return __factory()


async def global_stop():
    await revert_migrations()
