from uuid import UUID

from db.mongo.collections import get_geo_points
from entity.point import GeoPointFeatureCollection, GeoPointsModel

from ..exceptions import ItemNotFoundInRepoException
from .base import AbstractCoordinateRepo

__all__ = ("MongoCoordinateRepo",)


class MongoCoordinateRepo(AbstractCoordinateRepo):
    """
    Репозиторий точек координат для MongoDB
    """

    def __init__(self) -> None:
        self._collection = get_geo_points()

    async def save(self, points: GeoPointFeatureCollection) -> UUID:
        """
        Сохранение точек координат
        """
        model = GeoPointsModel(points=points)
        await self._collection.insert_one(model.model_dump(by_alias=True))
        return model.id

    async def get(self, file_id: UUID) -> GeoPointsModel:
        """
        Получение точек координат
        """
        points_doc = await self._collection.find_one({"_id": file_id})
        if points_doc is None:
            raise ItemNotFoundInRepoException
        return GeoPointsModel(**points_doc)
