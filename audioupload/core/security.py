from yandexid import AsyncYandexID

from audioupload.database.redis_init import get_connection


async def get_refresh_token_by_user(user_id: str):
    connection = get_connection()

    return await connection.get(f"refresh_{user_id}")


async def get_current_user_from_token(token):
    yandex_id = AsyncYandexID(token)
    return await yandex_id.get_user_info_json()


async def set_refresh_token_to_user(token, user_id):
    connection = get_connection()

    await connection.set(f"refresh_{user_id}", token)
