from fastapi import APIRouter

from .health import health_router
from .v0.router import api_v0_router

api_router = APIRouter(prefix="/api")
api_router.include_router(api_v0_router)
api_router.include_router(health_router)
