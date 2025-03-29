from contextlib import asynccontextmanager

from fastapi import FastAPI

from audioupload.database.db_init import global_init
from audioupload.database.redis_init import init_redis
from audioupload.routes import auth, upload, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await global_init()
    await init_redis()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.auth_router)
app.include_router(upload.upload_router)
app.include_router(user.user_router)
