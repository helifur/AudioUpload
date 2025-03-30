from dotenv import load_dotenv
from fastapi import HTTPException, status
from httpx import HTTPStatusError
from yandexid import AsyncYandexID

from audioupload.database.redis_init import get_connection
from audioupload.repository.user import UserRepository

load_dotenv()


async def get_refresh_token_by_user(user_id: str):
    connection = get_connection()

    return await connection.get(f"refresh_{user_id}")


async def get_user_yandex_data_from_token(token):
    yandex_id = AsyncYandexID(token)
    return await yandex_id.get_user_info_json()


async def get_user_local_data_from_token(token):
    user_data = await get_user_yandex_data_from_token(token)
    return await UserRepository.get_one_or_none(yandex_user_id=user_data.id)


async def set_refresh_token_to_user(token, user_id):
    connection = get_connection()

    await connection.set(f"refresh_{user_id}", token)


async def authenticate_user(token: str):
    try:
        user_data = await get_user_yandex_data_from_token(token)

    except HTTPStatusError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Token is invalid!",
        )

    if not await UserRepository.get_one_or_none(yandex_user_id=user_data.id):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "User not authorized!",
        )

    return token
