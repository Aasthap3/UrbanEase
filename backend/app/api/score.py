from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.scoring import SUPPORTED_RADII
from app.schemas.urban_score import UrbanScoreResponse
from app.services.urban_score_service import calculate_score_for_location

router = APIRouter(prefix='/score', tags=['scoring'])


@router.get('', response_model=UrbanScoreResponse)
def urban_score(
    latitude: Annotated[float, Query()],
    longitude: Annotated[float, Query()],
    radius: Annotated[int, Query()],
    db: Session = Depends(get_db),
) -> UrbanScoreResponse:
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        raise HTTPException(status_code=400, detail='Invalid geographic coordinates')
    if radius not in SUPPORTED_RADII:
        raise HTTPException(status_code=400, detail='Radius must be one of 500, 1000, 2000, or 5000 meters')
    return calculate_score_for_location(db, latitude, longitude, radius)