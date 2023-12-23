from fastapi import APIRouter

from .coordinate import coordinate_router

points_router = APIRouter(
    prefix="/points",
    tags=["points"],
)
points_router.include_router(coordinate_router)
