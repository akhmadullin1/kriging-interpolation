from abc import ABC, abstractmethod
from uuid import UUID

from entity.point import GeoPointFeatureCollection, GeoPointsModel

__all__ = ("AbstractCoordinateRepo",)


class AbstractCoordinateRepo(ABC):
    """
    Абстрактный базовый класс репозитория точек координат
    """

    @abstractmethod
    async def save(self, points: GeoPointFeatureCollection) -> UUID:
        """
        Сохранение точек координат
        """

    @abstractmethod
    async def get(self, file_id: UUID) -> GeoPointsModel:
        """
        Получение точек координат
        """
