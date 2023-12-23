from typing import Literal

from pydantic import BaseModel


class GeoModel(BaseModel):
    pass


class Feature(BaseModel):
    type: Literal["Feature"]
    geometry: GeoModel


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"]
    features: list[Feature]
