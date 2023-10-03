import pytest
from pytest import FixtureRequest
from traffix.config import Settings, settings


@pytest.fixture(scope="module")
def traffix_settings(request: FixtureRequest) -> Settings:
    return settings
