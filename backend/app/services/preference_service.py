from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.scoring import CATEGORY_WEIGHTS, PROFILE_WEIGHTS, SCORING_CATEGORIES
from app.models.amenity import AmenityCategory
from app.models.preference import UserPreference
from app.models.user import User
from app.schemas.preferences import PreferenceResponse, PreferenceUpdate, PreferenceWeight


def preference_response(profile: str, weights: dict[AmenityCategory, float]) -> PreferenceResponse:
    ordered_weights = [PreferenceWeight(category=category, weight=weights[category]) for category in SCORING_CATEGORIES]
    return PreferenceResponse(profile=profile, weights=ordered_weights, weight_total=sum(item.weight for item in ordered_weights))


def get_user_preferences(db: Session, user: User) -> PreferenceResponse:
    rows = db.scalars(select(UserPreference).where(UserPreference.user_id == user.id)).all()
    if not rows:
        return preference_response('custom', {category: float(weight) for category, weight in CATEGORY_WEIGHTS.items()})

    profile = rows[0].profile
    weights = {category: float(weight) for category, weight in CATEGORY_WEIGHTS.items()}
    for row in rows:
        try:
            weights[AmenityCategory(row.category)] = float(row.weight)
        except ValueError:
            continue
    return preference_response(profile, weights)


def save_user_preferences(db: Session, user: User, preferences: PreferenceUpdate) -> PreferenceResponse:
    db.execute(delete(UserPreference).where(UserPreference.user_id == user.id))
    db.add_all(
        [
            UserPreference(
                user_id=user.id,
                profile=preferences.profile,
                category=item.category.value,
                weight=item.weight,
            )
            for item in preferences.weights
        ]
    )
    db.commit()
    return preference_response(
        preferences.profile,
        {item.category: item.weight for item in preferences.weights},
    )


def profile_preferences(profile: str) -> PreferenceResponse:
    weights = PROFILE_WEIGHTS[profile]
    return preference_response(profile, {category: float(weight) for category, weight in weights.items()})