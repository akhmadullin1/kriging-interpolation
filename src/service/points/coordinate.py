from enum import Enum, unique
from uuid import UUID

from entity.point import GeoPointFeatureCollection
from repository.coordinate import AbstractCoordinateRepo, MongoCoordinateRepo
from repository.exceptions import ItemNotFoundInRepoException

from ..exceptions import ItemNotFoundException

__all__ = (
    "CoordinateService",
    "CoordinateServiceType",
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
        try:
            points_model = await self._repo.get(file_id)
        except ItemNotFoundInRepoException:
            raise ItemNotFoundException
        return points_model.points


@unique
class CoordinateServiceType(Enum):
    MONGO_SERVICE = 0


class CoordinateServiceFactory:
    """
    Фабрика серисов работы с точеками координат
    """

    __slots__ = ("_service_type",)

    def __init__(self, service_type: CoordinateServiceType) -> None:
        if service_type not in CoordinateServiceType:
            raise ValueError("Select incorrect service type")
        self._service_type = service_type

    def __call__(self) -> CoordinateService:
        match self._service_type:
            case CoordinateServiceType.MONGO_SERVICE:
                return CoordinateService(MongoCoordinateRepo())
