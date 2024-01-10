from uuid import UUID

from db.mongo.collections import get_kriging
from entity.kriging import GeoKrigingData, GeoKrigingModel, ProcessStatus
from entity.point import GeoPointFeatureCollection

from ..exceptions import ItemNotFoundInRepoException
from .base import AbstractKrigingRepo

__all__ = ("MongoGeoKrigingRepo",)


class MongoGeoKrigingRepo(AbstractKrigingRepo):
    """
    Репозиторий геопространственного кригинга для MongoDB
    """

    def __init__(self) -> None:
        self._collection = get_kriging()

    async def save_process(self, kriging_data: GeoKrigingData) -> GeoKrigingModel:
        """
        Сохранение процесса кригинга
        """
        model = GeoKrigingModel(kriging_data=kriging_data, status=ProcessStatus.PENDING)
        await self._collection.insert_one(model.model_dump(by_alias=True))
        return model

    async def save_result(
        self, process_id: UUID, result: GeoPointFeatureCollection
    ) -> None:
        """
        Сохранение результата кригинга
        """
        await self._collection.update_one(
            {"_id": process_id},
            {"$set": {"result": result.model_dump(), "status": ProcessStatus.SUCCESS}},
        )

    async def get_process(self, process_id: UUID) -> GeoKrigingModel:
        """
        Получение процесса кригинга
        """
        kriging_doc = await self._collection.find_one({"_id": process_id})
        if kriging_doc is None:
            raise ItemNotFoundInRepoException
        return GeoKrigingModel(**kriging_doc)
