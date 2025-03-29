import os

import asyncio_redis
from dotenv import load_dotenv

__factory = None


async def init_redis():
    global __factory

    if __factory:
        return

    load_dotenv()
    host = os.getenv("REDIS_HOSTNAME")
    port = os.getenv("REDIS_PORT")
    user = os.getenv("REDIS_USER")
    password = os.getenv("REDIS_PASSWORD")

    __factory = await asyncio_redis.Connection.create(
        host=host, port=port, password=password
    )


def get_connection():
    return __factory
