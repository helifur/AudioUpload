from dotenv import load_dotenv
from fastapi import HTTPException, status
from httpx import HTTPStatusError
from yandexid import AsyncYandexID

from audioupload.database.redis_init import get_connection
from audioupload.repository.user import UserRepository

load_dotenv()


async def get_refresh_token_by_user(user_id: str):
    """Get refresh token by yandex user id

    Args:
        user_id: yandex user id

    Returns:
        Refresh token
    """
    async with await get_connection() as conn:
        return await conn.get(f"refresh_{user_id}")


async def get_user_yandex_data_from_token(token: str):
    """Get yandex data of user by access token

    Args:
        token: access token

    Returns:
        Yandex data of user
    """
    yandex_id = AsyncYandexID(token)
    return await yandex_id.get_user_info_json()


async def get_user_local_data_from_token(token: str):
    """Get local data of user by access token

    Args:
        token: access token

    Returns:
        Local data of user
    """
    user_data = await get_user_yandex_data_from_token(token)
    return await UserRepository.get_one_or_none(yandex_user_id=user_data.id)


async def set_refresh_token_to_user(token: str, user_id: str):
    """Set refresh token in Redis by user id

    Args:
        token: refresh token
        user_id: yandex user id
    """
    async with await get_connection() as conn:
        await conn.set(f"refresh_{user_id}", token)


async def authenticate_user(token: str):
    """Authenticate user (validation)

    Args:
        token: access token

    Returns:
        access token

    Raises:
        HTTPException: if token is invalid or user not authorized
    """
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
