from fastapi import APIRouter, Request, Form, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import ValidationError
from loguru import logger
from redis import Redis
import json

from traffix.main import templates
from traffix.ui.templates.fragments import render_alert
from traffix.models import RUCreate, Alert, RU
from traffix.dependencies import get_db, get_redis
from traffix import crud


router = APIRouter()


@router.get("/create_request")
async def ru_create_request(request: Request):
    print(request.client.host)

    return templates.TemplateResponse(
        name="ru/create_request.html", context={"request": request}
    )


@router.get("/game_releases")
async def ru_game_releases(request: Request, redis: Redis = Depends(get_redis)):
    data = await redis.get("ru_releases")
    data_decoded = json.loads(data)
    releases = [
        RU(**json.loads(release)) for release in data_decoded
    ]  # Cringe sorry one day I'll use redis properly...

    return templates.TemplateResponse(
        name="ru/game_releases.html", context={"request": request, "releases": releases}
    )

@router.get("/game_updates")
async def ru_game_updates(request: Request, redis: Redis = Depends(get_redis)):
    data = await redis.get("ru_updates")
    data_decoded = json.loads(data)
    updates = [
        RU(**json.loads(update)) for update in data_decoded
    ]  # Cringe sorry one day I'll use redis properly...

    return templates.TemplateResponse(
        name="ru/game_updates.html", context={"request": request, "updates": updates}
    )

@router.post("/create_request")
async def ru_create_request(
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_db),
    name: str = Form(None),
    estimated_size: int = Form(None),
    ru_type: str = Form(None),
    release_date: str = Form(None),
    image_url: str = Form(None),
):
    try:
        ru_obj = RUCreate(
            name=name,
            estimated_size=estimated_size,
            ru_type=ru_type,
            release_date=release_date,
            image_url=image_url,
        )
    except ValidationError as e:
        errors = e.errors()
        response = templates.TemplateResponse(
            name="fragments/validation_errors.html",
            context={"request": request, "errors": errors},
        )
        return response

    # Check if Request/Update already exist in database
    ru_exist = await crud.ru.get_by_name(db=db, name=name)
    if ru_exist:
        # return templates.TemplateResponse(name="fragments/alert.html", context={"request": request, "alert": Alert(colour="danger", title="Error", text="Request/Update already exist with that name")})
        return render_alert(
            request=request,
            colour="danger",
            title="Error",
            text="Request/Update already exist with that name",
        )

    try:
        await crud.ru.create(db=db, obj_in=ru_obj)
    except Exception as err:
        logger.error(err)
        return render_alert(
            request=request,
            colour="danger",
            title="Error",
            text="Unable to add this request/update. Please contact an administrator",
        )
        # return templates.TemplateResponse(name="fragments/alert.html", context={"request": request, "alert": Alert(colour="danger", title="Error", text="Request/Update already exist with that name")})

    return templates.TemplateResponse(
        name="fragments/alert.html",
        context={
            "request": request,
            "alert": Alert(
                colour="success",
                title="Sent Request",
                text="Please wait for an administrator to approve the request",
            ),
        },
    )


@router.post("/test")
async def ru_test():
    return ""
