from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.scoring import SUPPORTED_RADII
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.personalized_score import PersonalizedScoreResponse
from app.services.preference_service import get_user_preferences
from app.services.urban_score_service import calculate_personalized_score_for_location

router = APIRouter(prefix='/score', tags=['scoring'])


@router.get('/personalized', response_model=PersonalizedScoreResponse)
def personalized_score(
    latitude: Annotated[float, Query()],
    longitude: Annotated[float, Query()],
    radius: Annotated[int, Query()],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PersonalizedScoreResponse:
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        raise HTTPException(status_code=400, detail='Invalid geographic coordinates')
    if radius not in SUPPORTED_RADII:
        raise HTTPException(status_code=400, detail='Radius must be one of 500, 1000, 2000, or 5000 meters')
    preferences = get_user_preferences(db, current_user)
    weights = {item.category: item.weight for item in preferences.weights}
    return calculate_personalized_score_for_location(
        db,
        latitude,
        longitude,
        radius,
        preferences.profile,
        weights,
    )