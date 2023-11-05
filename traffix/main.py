from typing import Any
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel.ext.asyncio.session import AsyncSession
from loguru import logger
import json

from traffix.config import settings
from traffix.initial_data import data
from traffix_sdk.dependencies.database import get_db


app = FastAPI()


@app.on_event("startup")
async def startup_event(db: AsyncSession = Depends(get_db)):
    # Import initial data

    """

    for game in data:
        try:
            ru = RUCreate(**game)
        except:
            logger.error(f"Unable to validate game: {game}")

        game_already_exist = await crud.ru.get_by_name(db=db, name=ru.name)
        if game_already_exist:
            continue

        await crud.ru.create(db=db, obj_in=ru)

    # Load reviewed Requests into redis
    redis = await get_redis()

    all_releases = await crud.ru.get_multi(db=db, limit=None, query={"ru_type": "release"})
    data_to_encode = json.dumps([release.model_dump_json() for release in all_releases])
    await redis.set(name="ru_releases", value=data_to_encode)

    all_updates = await crud.ru.get_multi(db=db, limit=None, query={"ru_type": "update"})
    data_to_encode = json.dumps([update.model_dump_json() for update in all_updates])
    await redis.set(name="ru_updates", value=data_to_encode)
    """


# API Controller
from traffix.api import v1

app.include_router(v1.api_router, prefix=settings.API_PATH_V1)
