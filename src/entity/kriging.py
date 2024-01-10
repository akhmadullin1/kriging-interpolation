from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ValidationInfo, conlist, field_validator

from .point import GeoPointFeatureCollection


class Variogram(StrEnum):
    GAUSSIAN = "gaussian"
    EXPONENTIAL = "exponential"
    SPHERICAL = "spherical"


class KrigingModel(StrEnum):
    SIMPLE = "simple"
    ORDINARY = "ordinary"
    UNIVERSAL = "universal"


class ProcessStatus(StrEnum):
    PENDING = "pending"
    STARTED = "started"
    SUCCESS = "success"


class GeoGrid(BaseModel):
    lat: conlist(float, min_length=3, max_length=3)
    lon: conlist(float, min_length=3, max_length=3)

    @field_validator("lat", "lon")
    @classmethod
    def validate_coordinates(
        cls, grid: list[float], info: ValidationInfo
    ) -> list[float]:
        if grid[0] >= grid[1]:
            raise ValueError("Incorrect coordinate")
        if grid[2] < 0.1 or grid[2] > grid[1] - grid[0]:
            raise ValueError("Incorrect grid step")

        if info.field_name == "lat" and (
            not (-90 <= grid[0] <= 90) or not (-90 <= grid[1] <= 90)
        ):
            raise ValueError("Point latitude value should be between -90 and 90")
        elif not (-180 <= grid[0] <= 180) or not (-180 <= grid[1] <= 180):
            raise ValueError("Point longitude value should be between -180 and 180")

        return grid


class GeoKrigingData(BaseModel):
    points_id: UUID
    grid: GeoGrid
    vario: Variogram
    kriging: KrigingModel


class GeoKrigingModel(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    status: ProcessStatus
    kriging_data: GeoKrigingData
    result: GeoPointFeatureCollection | None = None
