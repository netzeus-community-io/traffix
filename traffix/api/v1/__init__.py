from fastapi import APIRouter

api_router = APIRouter()

from traffix.api.v1.endpoints import (
    api_key,
    category,
    platforms,
    releases,
    updates,
    user,
)

api_router.include_router(api_key.router, prefix="/api_keys")
api_router.include_router(category.router, prefix="/categories")
api_router.include_router(platforms.router, prefix="/platforms")
api_router.include_router(releases.router, prefix="/releases")
api_router.include_router(updates.router, prefix="/updates")
api_router.include_router(user.router, prefix="/users")
