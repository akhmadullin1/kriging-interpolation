from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, conlist, field_validator

from .base import Feature, FeatureCollection, GeoModel


class GeoPointProperties(BaseModel):
    value: float


class GeoPoint(GeoModel):
    type: Literal["Point"]
    coordinates: conlist(float, min_length=2, max_length=2)
    properties: GeoPointProperties

    @field_validator("coordinates")
    @classmethod
    def validate_coordinates(cls, coordinates: list[float]) -> list[float]:
        if not (-180 <= coordinates[0] <= 180):
            raise ValueError("Point longitude value should be between -180 and 180")
        if not (-90 <= coordinates[1] <= 90):
            raise ValueError("Point latitude value should be between -90 and 90")
        return coordinates


class GeoPointFeature(Feature):
    geometry: GeoPoint


class GeoPointFeatureCollection(FeatureCollection):
    features: list[GeoPointFeature]


class GeoPointsModel(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    points: GeoPointFeatureCollection
