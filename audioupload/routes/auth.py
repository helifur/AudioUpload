import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from yandexid import AsyncYandexOAuth

from audioupload.core.security import (
    get_refresh_token_by_user,
    get_user_yandex_data_from_token,
    set_refresh_token_to_user,
)
from audioupload.database import redis_init
from audioupload.database.redis_init import init_redis
from audioupload.models.user import User
from audioupload.repository.user import UserRepository

auth_router = APIRouter()

load_dotenv()


@auth_router.post("/auth")
async def auth():
    yandex_oauth = AsyncYandexOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
    )
    token = yandex_oauth.get_token_from_code(os.getenv("SECRET_CODE"))

    user_data = await get_user_yandex_data_from_token(token.access_token)

    if not await UserRepository.get_one_or_none(yandex_user_id=user_data.id):
        await UserRepository.insert(
            yandex_user_id=user_data.id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role_id=0,
        )

    await set_refresh_token_to_user(token.refresh_token, user_data.id)

    return token


@auth_router.post("/refresh")
async def refresh(user_id: str):
    yandex_oauth = AsyncYandexOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
    )

    refresh_token = await get_refresh_token_by_user(user_id)
    new_tokens = await yandex_oauth.get_token_from_refresh_token(refresh_token)

    await set_refresh_token_to_user(new_tokens.refresh_token, user_id)

    return new_tokens
