from typing import Annotated

from fastapi import APIRouter, Depends
from yandexid import AsyncYandexID

user_router = APIRouter()


@user_router.get("/user")
async def cur_user(token: str):
    yandex_id = AsyncYandexID(token)
    return await yandex_id.get_user_info_json()
