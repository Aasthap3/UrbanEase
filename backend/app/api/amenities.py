from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.scoring import SUPPORTED_RADII
from app.models.amenity import AmenityCategory
from app.schemas.amenity import NearbyAmenitiesResponse
from app.services.amenity_service import discover_and_query_nearby
from app.services.overpass_service import OverpassServiceError

router = APIRouter(prefix='/amenities', tags=['amenities'])


@router.get('/nearby', response_model=NearbyAmenitiesResponse)
async def nearby_amenities(
    latitude: Annotated[float, Query()],
    longitude: Annotated[float, Query()],
    radius: Annotated[int, Query()],
    category: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> NearbyAmenitiesResponse:
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        raise HTTPException(status_code=400, detail='Invalid geographic coordinates')
    if radius not in SUPPORTED_RADII:
        raise HTTPException(status_code=400, detail='Radius must be one of 500, 1000, 2000, or 5000 meters')
    try:
        selected_category = AmenityCategory(category) if category else None
    except ValueError:
        raise HTTPException(status_code=400, detail='Unsupported amenity category') from None

    try:
        amenities = await discover_and_query_nearby(db, latitude, longitude, radius, selected_category)
    except OverpassServiceError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Amenity discovery service is currently unavailable',
        ) from None
    return NearbyAmenitiesResponse(
        center={'latitude': latitude, 'longitude': longitude},
        radius_meters=radius,
        category=selected_category,
        count=len(amenities),
        amenities=amenities,
    )