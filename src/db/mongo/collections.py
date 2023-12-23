from motor.motor_asyncio import AsyncIOMotorCollection

from .base import get_db

__POINTS_COLLECTION = "points"


def get_geo_points() -> AsyncIOMotorCollection:
    """Получить коллекцию points"""
    return get_db()[__POINTS_COLLECTION]
