from pydantic_settings import BaseSettings
from pydantic import RedisDsn, MongoDsn


class Settings(BaseSettings):
    # Default API Path
    API_PATH_V1: str = "/v1"

    # Max Size in bytes a Release or Update is
    MAX_RU_SIZE: int = 250000000000

    # Max characters for the image URL to load for a release/update
    MAX_IMAGE_URL_LENGTH: int = 128

    # Default redis Dsn
    REDIS_URI: RedisDsn = "redis://localhost:6379"

    # Default MongoDB Dsn
    MONGODB_URI: MongoDsn = "mongodb://localhost:27017"

    # Default MongoDB Database
    MONGODB_DATABASE: str = "traffix-dev"

    # Default JWT Expire Timer
    JWT_EXPIRE: int = 60 * 24 * 3  # 3 Days

    # JWT Shared Secret
    JWT_SHARED_SECRET: str = "change-me-please"

    # JWT Algorithm
    JWT_ALGORITHM: str = "HS256"


settings = Settings()
