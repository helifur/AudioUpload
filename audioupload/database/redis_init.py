import logging
import os

import redis.asyncio as redis
from dotenv import load_dotenv

__factory = None


async def init_redis():
    """Creates Redis client"""
    global __factory

    if __factory:
        return

    load_dotenv()
    host = os.getenv("REDIS_HOSTNAME")
    port = os.getenv("REDIS_PORT")

    try:
        __factory = redis.Redis.from_url(f"redis://{host}:{port}")
    except Exception as e:
        logging.error(f"Redis initializing error! ERR: {e}")


async def get_connection():
    """Returns Redis connection"""
    return __factory


async def stop_connection():
    """Stops Redis client and connections"""
    await __factory.close()
