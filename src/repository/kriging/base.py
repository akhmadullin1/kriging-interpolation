from abc import ABC, abstractmethod
from uuid import UUID

from entity.kriging import GeoKrigingData, GeoKrigingModel
from entity.point import GeoPointFeatureCollection

__all__ = ("AbstractKrigingRepo",)


class AbstractKrigingRepo(ABC):
    """
    Абстрактный базовый класс репозитория кригинга
    """

    @abstractmethod
    async def save_process(self, kriging_data: GeoKrigingData) -> GeoKrigingModel:
        """
        Сохранение процесса кригинга
        """

    @abstractmethod
    async def save_result(self, process_id: UUID, result: GeoPointFeatureCollection) -> None:
        """
        Сохранение результата кригинга
        """

    @abstractmethod
    async def get_process(self, process_id: UUID) -> GeoKrigingModel:
        """
        Получение процесса кригинга
        """
