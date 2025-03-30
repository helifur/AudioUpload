import asyncio
import logging
from contextlib import asynccontextmanager

import anyio
import sqlalchemy as sa
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncConnection

from alembic import command, op
from alembic.config import Config
from audioupload.database.db_init import global_init, global_stop
from audioupload.database.redis_init import init_redis, stop_connection
from audioupload.repository.role import RoleRepository
from audioupload.routes import auth, upload, users

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await global_init()

        await init_redis()
        # await run_async_migrations()

        # 3. Вставляем начальные данные (опционально)
        # await insert_initial_data()

        yield

        await global_stop()
        await stop_connection()
    except Exception as e:
        print(e)


app = FastAPI(lifespan=lifespan)

app.include_router(auth.auth_router)
app.include_router(upload.upload_router)
app.include_router(users.user_router)
