from typing import Annotated

from fastapi import APIRouter, Depends
from yandexid import AsyncYandexID

from audioupload.core.security import oauth2_scheme

user_router = APIRouter()


async def get_current_user():
    pass


@user_router.get("/user")
async def cur_user(token: Annotated[str, Depends(oauth2_scheme)]):
    yandex_id = AsyncYandexID(token)
    return await yandex_id.get_user_info_json()
