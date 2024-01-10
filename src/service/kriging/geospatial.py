import asyncio
from uuid import UUID

import gstools as gs
import numpy as np

from celery_app import celery_client
from config import DataBaseType, settings
from entity.kriging import (
    GeoKrigingData,
    GeoKrigingModel,
    KrigingModel,
    ProcessStatus,
    Variogram,
)
from entity.point import (
    GeoPoint,
    GeoPointFeature,
    GeoPointFeatureCollection,
    GeoPointProperties,
)
from repository.exceptions import ItemNotFoundInRepoException
from repository.kriging.base import AbstractKrigingRepo
from repository.kriging.geospatial import MongoGeoKrigingRepo
from service.exceptions import ItemNotFoundException

from ..points.coordinate import CoordinateService, CoordinateServiceFactory
from .exceptions import (
    IncorrectKrigingException,
    IncorrectVariogramException,
    KrigingNotCompletedException,
)

__all__ = (
    "GeoKrigingService",
    "GeoKrigingServiceFactory",
)


class GeoKrigingService:
    """
    Сервис геопространственного кригинга
    """

    _ALLOWED_VARIO_TYPES = {
        Variogram.GAUSSIAN,
        Variogram.EXPONENTIAL,
        Variogram.SPHERICAL,
    }
    _ALLOWED_KRIGING_MODELS = {
        KrigingModel.SIMPLE,
        KrigingModel.ORDINARY,
        KrigingModel.UNIVERSAL,
    }

    def __init__(self, kriging_repo: AbstractKrigingRepo, coordinate_service: CoordinateService):
        self._repo = kriging_repo
        self._coordinate_service = coordinate_service

    def get_variogram(self, vario_type: Variogram) -> gs.CovModel:
        """
        Получение вариограммы
        """
        match vario_type:
            case Variogram.GAUSSIAN:
                return gs.Gaussian(latlon=True, geo_scale=gs.KM_SCALE)
            case Variogram.EXPONENTIAL:
                return gs.Exponential(latlon=True, geo_scale=gs.KM_SCALE)
            case Variogram.SPHERICAL:
                return gs.Spherical(latlon=True, geo_scale=gs.KM_SCALE)
            case _:
                raise IncorrectVariogramException

    def get_kriging_model(
        self,
        kriging_type: KrigingModel,
        model: gs.CovModel,
        lat: list[float],
        lon: list[float],
        val: list[float],
    ) -> gs.krige.Krige:
        """
        Получение модели кригинга
        """
        match kriging_type:
            case KrigingModel.SIMPLE:
                return gs.krige.Simple(model=model, cond_pos=(lat, lon), cond_val=val)
            case KrigingModel.ORDINARY:
                return gs.krige.Ordinary(model=model, cond_pos=(lat, lon), cond_val=val)
            case KrigingModel.UNIVERSAL:
                return gs.krige.Universal(
                    model=model,
                    cond_pos=(lat, lon),
                    cond_val=val,
                    drift_functions=None,
                )
            case _:
                raise IncorrectKrigingException

    async def create_process(self, data: GeoKrigingData) -> UUID:
        """
        Создание процесса
        """
        if data.vario not in self._ALLOWED_VARIO_TYPES:
            raise IncorrectVariogramException
        if data.kriging not in self._ALLOWED_KRIGING_MODELS:
            raise IncorrectKrigingException

        await self._coordinate_service.get(data.points_id)
        kriging_model = await self._repo.save_process(data)

        geo_kriging_process.delay(kriging_model.id)

        return kriging_model.id

    async def kriging_execute(self, process_id: UUID):
        """
        Выполнение кригинга
        """
        kriging_model = await self.get_process(process_id)
        points = await self._coordinate_service.get(kriging_model.kriging_data.points_id)

        lon = []
        lat = []
        values = []
        for point in points.features:
            lon.append(point.geometry.coordinates[0])
            lat.append(point.geometry.coordinates[1])
            values.append(point.geometry.properties.value)

        bin_center, vario1 = gs.vario_estimate((lat, lon), values, latlon=True, geo_scale=gs.KM_SCALE, max_dist=900)

        vario = self.get_variogram(vario_type=kriging_model.kriging_data.vario)
        vario.fit_variogram(bin_center, vario1, nugget=False)

        model = self.get_kriging_model(
            kriging_type=kriging_model.kriging_data.kriging,
            model=vario,
            lat=lat,
            lon=lon,
            val=values,
        )

        g_lat = np.arange(*kriging_model.kriging_data.grid.lat)
        g_lon = np.arange(*kriging_model.kriging_data.grid.lon)
        model.set_pos((g_lat, g_lon), mesh_type="structured")
        model(return_var=False, store="val_field")
        model(only_mean=True, store="mean_field")

        fetaure_points = []
        for lat_index, lat_value in np.ndenumerate(g_lat):
            for lon_index, lon_value in np.ndenumerate(g_lon):
                point = GeoPoint(
                    coordinates=[lon_value, lat_value],
                    properties=GeoPointProperties(value=model["val_field"][lat_index][lon_index]),
                )
                fetaure_points.append(GeoPointFeature(geometry=point))

        await self._repo.save_result(
            process_id=kriging_model.id,
            result=GeoPointFeatureCollection(features=fetaure_points),
        )

    async def get_process_status(self, process_id: UUID) -> ProcessStatus:
        """
        Получение статуса процесса
        """
        kriging_model = await self.get_process(process_id)
        return kriging_model.status

    async def get_process_result(self, process_id: UUID) -> GeoPointFeatureCollection:
        """
        Получение результатов процесса кригинга
        """
        kriging_model = await self.get_process(process_id)
        if kriging_model.status != ProcessStatus.SUCCESS:
            raise KrigingNotCompletedException
        return kriging_model.result

    async def get_process(self, process_id: UUID) -> GeoKrigingModel:
        """
        Получение процесса кригинга
        """
        try:
            kriging_model = await self._repo.get_process(process_id)
        except ItemNotFoundInRepoException:
            raise ItemNotFoundException
        return kriging_model


@celery_client.task
def geo_kriging_process(process_id: UUID):
    service_factory = GeoKrigingServiceFactory()
    asyncio.get_event_loop().run_until_complete(service_factory().kriging_execute(process_id))


class GeoKrigingServiceFactory:
    """
    Фабрика серисов работы с геопространственным кригингом
    """

    _ALLOWED_DB_TYPES = {DataBaseType.MONGO}

    __slots__ = (
        "_service_type",
        "_coordinate_service_factory",
    )

    def __init__(
        self,
        service_type: DataBaseType = settings.service_types.geo_kriging,
        coordinate_service_factory: CoordinateServiceFactory = CoordinateServiceFactory(),
    ) -> None:
        if service_type not in self._ALLOWED_DB_TYPES:
            raise ValueError("Select incorrect service type")
        self._service_type = service_type
        self._coordinate_service_factory = coordinate_service_factory

    def __call__(self) -> CoordinateService:
        match self._service_type:
            case DataBaseType.MONGO:
                return GeoKrigingService(MongoGeoKrigingRepo(), self._coordinate_service_factory())
