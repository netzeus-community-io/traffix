from fastapi import APIRouter

api_router = APIRouter()

from traffix.api.v1.endpoints import releases

api_router.include_router(releases.router, prefix="/releases")
