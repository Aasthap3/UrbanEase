from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.location import LocationSearchParams, LocationSearchResult
from app.services.geocoding_service import GeocodingServiceError, search_locations

router = APIRouter(prefix='/locations', tags=['locations'])


@router.get('/search', response_model=list[LocationSearchResult])
async def search(
    params: Annotated[LocationSearchParams, Depends()],
) -> list[LocationSearchResult]:
    try:
        return await search_locations(params.q, params.limit)
    except GeocodingServiceError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Location search service is currently unavailable',
        ) from None