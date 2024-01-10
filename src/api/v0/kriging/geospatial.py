from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from entity.kriging import GeoKrigingData
from entity.point import GeoPointFeatureCollection
from service.exceptions import ItemNotFoundException
from service.kriging.exceptions import KrigingNotCompletedException
from service.kriging.geospatial import (
    GeoKrigingService,
    GeoKrigingServiceFactory,
)

from .schemas import KrigingStatusResponse

geokriging_router = APIRouter(prefix="/geospatial")

GeoKrigingServiceDep = Annotated[
    GeoKrigingService,
    Depends(GeoKrigingServiceFactory()),
]


@geokriging_router.post(
    path="/process",
    summary="Создать процесс геопространственного кригинга",
    status_code=status.HTTP_200_OK,
)
async def create_geospatial_kriging_process(data: GeoKrigingData, service: GeoKrigingServiceDep):
    process_id = await service.create_process(data)
    return {"id": process_id}


@geokriging_router.get(
    path="/process/{process_id}",
    summary="Получение результатов процесса кригинга",
    status_code=status.HTTP_200_OK,
)
async def get_geospatial_kriging_process(process_id: UUID, service: GeoKrigingServiceDep) -> GeoPointFeatureCollection:
    try:
        points = await service.get_process_result(process_id)
    except ItemNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.args[0])
    except KrigingNotCompletedException as ex:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail=ex.args[0])
    return points


@geokriging_router.get(
    path="/process/{process_id}/status",
    summary="Получение статуса процесса кригинга",
    status_code=status.HTTP_200_OK,
)
async def get_status_geospatial_kriging(process_id: UUID, service: GeoKrigingServiceDep) -> KrigingStatusResponse:
    try:
        kriging_status = await service.get_process_status(process_id)
    except ItemNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.args[0])
    return KrigingStatusResponse(status=kriging_status)
