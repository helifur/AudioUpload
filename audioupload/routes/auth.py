import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from yandexid import YandexOAuth

auth_router = APIRouter()

load_dotenv()


@auth_router.post("/token")
async def auth():
    # yandex_oauth = YandexOAuth(
    #     client_id="8d7e704d59674519b7d9a0e1c458b5d5",
    #     client_secret="23d54c1d3c82461c88602258b08c0cff",
    #     redirect_uri="https://oauth.yandex.ru/verification_code",
    # )
    #
    # token = yandex_oauth.get_token_from_code("cblhycitgghpyldo")

    return {
        "access_token": os.getenv("ACCESS_TOKEN"),
        "refresh_token": os.getenv("REFRESH_TOKEN"),
    }
