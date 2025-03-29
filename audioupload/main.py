from contextlib import asynccontextmanager

from fastapi import FastAPI

from audioupload.database.db_init import global_init
from audioupload.routes import auth, upload, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await global_init()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.auth_router)
app.include_router(upload.upload_router)
app.include_router(user.user_router)
