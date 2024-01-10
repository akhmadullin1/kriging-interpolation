from fastapi import APIRouter

from .kriging.router import kriging_router
from .points.router import points_router

api_v0_router = APIRouter(prefix="/v0")
api_v0_router.include_router(points_router)
api_v0_router.include_router(kriging_router)
