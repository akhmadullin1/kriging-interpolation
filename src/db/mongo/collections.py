from motor.motor_asyncio import AsyncIOMotorCollection

from .base import get_db

__POINTS_COLLECTION = "points"
__KRIGING_COLLECTION = "kriging"


def get_geo_points() -> AsyncIOMotorCollection:
    """Получить коллекцию points"""
    return get_db()[__POINTS_COLLECTION]


def get_kriging() -> AsyncIOMotorCollection:
    """Получить коллекцию kriging"""
    return get_db()[__KRIGING_COLLECTION]
