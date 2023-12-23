from typing import Annotated
from uuid import UUID

from entity.point import GeoPointFeatureCollection
from fastapi import APIRouter, Depends, HTTPException, status
from service.exceptions import ItemNotFoundException
from service.points.coordinate import (
    CoordinateService,
    CoordinateServiceFactory,
    CoordinateServiceType,
)

from ...schemas import IdSchema

coordinate_router = APIRouter(prefix="/coordinate")

CoordinateServiceDep = Annotated[
    CoordinateService,
    Depends(CoordinateServiceFactory(CoordinateServiceType.MONGO_SERVICE)),
]


@coordinate_router.post(
    path="/save",
    summary="Сохранить координаты",
    status_code=status.HTTP_201_CREATED,
)
async def save_coordinates(
    points: GeoPointFeatureCollection, service: CoordinateServiceDep
) -> IdSchema:
    file_id = await service.save(points)
    return IdSchema(id=file_id)


@coordinate_router.get(
    path="/{points_id}",
    summary="Получить координаты",
    status_code=status.HTTP_200_OK,
)
async def get_coordinates(
    points_id: UUID, service: CoordinateServiceDep
) -> GeoPointFeatureCollection:
    try:
        points = await service.get(points_id)
    except ItemNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.args[0])
    return points
