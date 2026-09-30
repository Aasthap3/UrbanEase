from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.amenity import AmenityCategory


class NormalizedAmenity(BaseModel):
    osm_id: str
    osm_type: str
    category: AmenityCategory
    name: str | None = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    address: str | None = None
    opening_hours: str | None = None
    phone: str | None = None
    website: str | None = None
    source: str = 'openstreetmap'


class NearbyAmenity(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    osm_id: str | None
    osm_type: str | None
    name: str | None
    category: AmenityCategory
    latitude: float
    longitude: float
    distance_meters: float
    address: str | None
    opening_hours: str | None
    phone: str | None
    website: str | None


class NearbyAmenitiesResponse(BaseModel):
    center: dict[str, float]
    radius_meters: int
    category: AmenityCategory | None
    count: int
    amenities: list[NearbyAmenity]