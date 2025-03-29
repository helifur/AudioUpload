import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from yandexid import YandexOAuth

from audioupload.core.security import get_current_user_from_token
from audioupload.database import redis_init
from audioupload.database.redis_init import init_redis
from audioupload.models.user import User
from audioupload.repository.user import UserRepository

auth_router = APIRouter()

load_dotenv()


@auth_router.post("/token")
async def auth():
    # yandex_oauth = YandexOAuth(
    #     client_id=os.getenv("CLIENT_ID"),
    #     client_secret=os.getenv("CLIENT_SECRET"),
    #     redirect_uri=os.getenv("REDIRECT_URI"),
    # )
    # token = yandex_oauth.get_token_from_code(os.getenv("SECRET_CODE"))
    # print(token)
    token = {
        "access_token": "y0__xDYhrWdAhiiwDYgk4fh1RI3qMGnGcLVMf2YWeyYX5OKGnW6Og",
        "token_type": "bearer",
        "refresh_token": "1:AAA:1:9Dck31XL_tPVIweO:6DWEw-m5s0ZU0feEsK27XuLrt9SJPSq3-Gbp3ZR1ii9bt7JqbuuKbcrPPZR-x0b-u1Ukmx4:lKlIvDtYID8oTBfewAESog",
        "expires_in": 31526053,
    }

    user_data = await get_current_user_from_token(token["access_token"])

    if not await UserRepository.get_one_or_none(
        yandex_user_id=int(user_data.id)
    ):
        await UserRepository.insert(
            yandex_user_id=int(user_data.id),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role_id=0,
        )

    return token


@auth_router.post("/refresh")
async def refresh(token):
    yandex_oauth = YandexOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
    )

    res = yandex_oauth.get_token_from_refresh_token(token)

    yandex_oauth.get_token_from_refresh_token()
