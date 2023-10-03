from traffix.models import Release, Update, RUTypeEnum
from traffix.config import Settings
from traffix.dependencies import get_db, get_redis
from datetime import datetime
import pytest
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_database_connection(traffix_settings: Settings):
    db = await get_db(uri=traffix_settings.MONGODB_URI, db="traffix")

    server_info = await db.client.server_info()
    assert server_info
    assert server_info["version"]


@pytest.mark.asyncio
async def test_database_create_release(traffix_settings: Settings):
    release = Release(
        name="Call of Duty: Warzone",
        estimated_size=125000000000,
        categories=["fps"],
        release_date=datetime(2020, 3, 10),
        image_url="https://upload.wikimedia.org/wikipedia/en/0/01/Call_of_Duty_Warzone_cover.png",
    )
