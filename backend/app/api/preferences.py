from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.preferences import PreferenceResponse, PreferenceUpdate
from app.services.preference_service import get_user_preferences, save_user_preferences

router = APIRouter(prefix='/preferences', tags=['preferences'])


@router.get('', response_model=PreferenceResponse)
def read_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PreferenceResponse:
    return get_user_preferences(db, current_user)


@router.put('', response_model=PreferenceResponse)
def update_preferences(
    preferences: PreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PreferenceResponse:
    return save_user_preferences(db, current_user, preferences)