from traffix.models import Release, Update, RUTypeEnum
from traffix.config import Settings
from datetime import datetime
import pytest
from pydantic import ValidationError


def test_release_model_good(traffix_settings: Settings):
    Release(
        name="example_release",
        estimated_size=123456,
        size=123456,
        categories=["test", "test2", "test3"],
        release_date=datetime.now(),
        image_url="https://www.google.com/images/branding/googlelogo/1x/googlelogo_light_color_272x92dp.png",
    )


def test_update_model_good(traffix_settings: Settings):
    Update(
        name="example_update",
        estimated_size=123456,
        size=123456,
        categories=["test", "test2", "test3"],
        release_date=datetime.now(),
        image_url="https://www.google.com/images/branding/googlelogo/1x/googlelogo_light_color_272x92dp.png",
    )


def test_release_model_bad(traffix_settings: Settings):
    with pytest.raises(ValidationError):
        Release(
            name="example_release",
            estimated_size=123456123456123456,
            size=123456123456123456,
        )  # Missing required fields


def test_update_model_bad(traffix_settings: Settings):
    with pytest.raises(ValidationError):
        Update(
            name="example_update",
            estimated_size=123456123456123456,
            size=123456123456123456,
            release_date=datetime.now(),
            image_url="https://www.google.com/images/branding/googlelogo/1x/googlelogo_light_color_272x92dp.png",
        )
