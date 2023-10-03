from typing import Any
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
import json

from traffix.config import settings
from traffix.dependencies import get_db, get_redis
from traffix.initial_data import data
from traffix.models import RUCreate
from traffix import crud


app = FastAPI()

app.mount("/static", StaticFiles(directory="traffix/ui/static"), name="static")

templates = Jinja2Templates(directory="traffix/ui/templates")


@app.on_event("startup")
async def startup_event():
    # Import initial data
    db = await get_db()

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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> Any:
    return templates.TemplateResponse("index.html", {"request": request})


# View controller
from traffix import views

app.include_router(views.views_router)

# API Controller
from traffix.api import v1

app.include_router(v1.api_router, prefix=settings.API_PATH_V1)
