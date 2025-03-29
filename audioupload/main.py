from fastapi import FastAPI

from audioupload.routes import auth

app = FastAPI()

app.include_router(auth.auth_router)
