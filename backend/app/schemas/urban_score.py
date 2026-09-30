from uuid import UUID

from pydantic import BaseModel, Field

from app.models.amenity import AmenityCategory


class CategoryScore(BaseModel):
    category: AmenityCategory
    weight: int
    score: float = Field(ge=0, le=1)
    nearest_distance_meters: float | None = Field(default=None, ge=0)
    amenity_count: int = Field(ge=0)
    contribution: float = Field(ge=0)


class UrbanScoreResponse(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    radius_meters: int
    score: float = Field(ge=0, le=100)
    categories: list[CategoryScore]