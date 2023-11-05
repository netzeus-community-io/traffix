from pydantic import RedisDsn, MongoDsn
from traffix_sdk.config import Settings


class Settings(Settings):
    # Default API Path
    API_PATH_V1: str = "/v1"

    # Max Size in bytes a Release or Update is
    MAX_RU_SIZE: int = 250000000000

    # Max characters for the image URL to load for a release/update
    MAX_IMAGE_URL_LENGTH: int = 128

    # Default redis Dsn
    REDIS_URI: RedisDsn = "redis://localhost:6379"

    # Default JWT Expire Timer
    JWT_EXPIRE: int = 60 * 24 * 3  # 3 Days

    # JWT Shared Secret
    JWT_SHARED_SECRET: str = "change-me-please"

    # JWT Algorithm
    JWT_ALGORITHM: str = "HS256"


settings = Settings()
