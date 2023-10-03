from fastapi import APIRouter

views_router = APIRouter()

from traffix.views import ru

views_router.include_router(ru.router, prefix="/ru")
