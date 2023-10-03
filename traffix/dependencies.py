from fastapi import Cookie, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from loguru import logger
from redis import asyncio as aioredis
from redis.client import PubSub
from redis.exceptions import ConnectionError

from traffix.config import settings
from traffix.auth import decode_access_token


async def get_db(
    uri: str = settings.MONGODB_URI, db: str = settings.MONGODB_DATABASE
) -> AsyncIOMotorDatabase:
    """Gets a MongoDB database object to be used with database operations.

    Args:
        uri:        MongoDB URI
        db:         Name of database in MongoDB
    """
    client = AsyncIOMotorClient(str(uri))
    database = client[db]
    return database


async def get_redis() -> aioredis.Redis:
    """Returns instance of redis for caching purposes."""
    try:
        client = await aioredis.from_url(
            str(settings.REDIS_URI), encoding="utf8", decode_responses=True
        )

        logger.success(f"Connected to redis - {settings.REDIS_URI}")
        return client

    except ConnectionError as e:
        logger.error(f"Redis ConnectionError occured: {e}")

    except Exception as e:
        logger.error(f"Redis Generic Exception occured: {e}")


async def get_admin_from_cookie(user_token: str = Cookie(None)):
    # Need to redo this function and figure out if I should just build separate admin dashboard for validating manual requests
    if not user_token:
        return None

    try:
        payload = decode_access_token(token=user_token)
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    logger.info(payload)

    return payload
