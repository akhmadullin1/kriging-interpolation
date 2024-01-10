from uuid import UUID

from config import DataBaseType, settings
from entity.point import GeoPointFeatureCollection
from repository.coordinate import AbstractCoordinateRepo, MongoCoordinateRepo
from repository.exceptions import ItemNotFoundInRepoException

from ..exceptions import ItemNotFoundException

__all__ = (
    "CoordinateService",
    "CoordinateServiceFactory",
)


class CoordinateService:
    """
    Сервис точек координат
    """

    def __init__(self, coordinate_repo: AbstractCoordinateRepo):
        self._repo = coordinate_repo

    async def save(self, points: GeoPointFeatureCollection) -> UUID:
        """
        Сохранение точек координат
        """
        return await self._repo.save(points)

    async def get(self, file_id: UUID) -> GeoPointFeatureCollection:
        """
        Получение точек координат
        """
        try:
            points_model = await self._repo.get(file_id)
        except ItemNotFoundInRepoException:
            raise ItemNotFoundException
        return points_model.points


class CoordinateServiceFactory:
    """
    Фабрика серисов работы с точками координат
    """

    _ALLOWED_DB_TYPES = {DataBaseType.MONGO}

    __slots__ = ("_service_type",)

    def __init__(self, service_type: DataBaseType = settings.service_types.coordinate) -> None:
        if service_type not in self._ALLOWED_DB_TYPES:
            raise ValueError("Select incorrect service type")
        self._service_type = service_type

    def __call__(self) -> CoordinateService:
        match self._service_type:
            case DataBaseType.MONGO:
                return CoordinateService(MongoCoordinateRepo())
