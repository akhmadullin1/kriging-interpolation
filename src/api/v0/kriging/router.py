from fastapi import APIRouter

from .geospatial import geokriging_router

kriging_router = APIRouter(
    prefix="/kriging",
    tags=["kriging"],
)
kriging_router.include_router(geokriging_router)
