import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from audioupload.database.db_init import global_init
from audioupload.database.redis_init import init_redis, stop_connection
from audioupload.routes import auth, upload, users

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await global_init()

        await init_redis()

        yield

        await stop_connection()
    except Exception as e:
        print(e)


app = FastAPI(lifespan=lifespan)

app.include_router(auth.auth_router)
app.include_router(upload.upload_router)
app.include_router(users.user_router)
