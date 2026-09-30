from collections.abc import Iterable

from sqlalchemy.orm import Session

from app.core.scoring import CATEGORY_WEIGHTS
from app.models.amenity import AmenityCategory
from app.schemas.amenity import NearbyAmenity
from app.schemas.urban_score import CategoryScore, UrbanScoreResponse
from app.schemas.personalized_score import PersonalizedScoreResponse
from app.services.amenity_service import query_nearby_amenities


def distance_decay(distance_meters: float) -> float:
    return 1 / (1 + distance_meters / 1000)


def calculate_score(
    latitude: float,
    longitude: float,
    radius: int,
    amenities: Iterable[NearbyAmenity],
) -> UrbanScoreResponse:
    category_scores = calculate_category_scores(amenities, CATEGORY_WEIGHTS)
    return UrbanScoreResponse(
        latitude=latitude,
        longitude=longitude,
        radius_meters=radius,
        score=round(sum(category.contribution for category in category_scores), 1),
        categories=category_scores,
    )


def calculate_category_scores(
    amenities: Iterable[NearbyAmenity],
    weights: dict[AmenityCategory, float],
) -> list[CategoryScore]:
    amenities_by_category: dict[AmenityCategory, list[NearbyAmenity]] = {
        category: [] for category in weights
    }
    for amenity in amenities:
        if amenity.category in amenities_by_category:
            amenities_by_category[amenity.category].append(amenity)

    category_scores: list[CategoryScore] = []
    for category, weight in weights.items():
        category_amenities = amenities_by_category[category]
        contributions = [distance_decay(amenity.distance_meters) for amenity in category_amenities]
        category_score = max(contributions, default=0.0)
        nearest_distance = min(
            (amenity.distance_meters for amenity in category_amenities),
            default=None,
        )
        category_scores.append(
            CategoryScore(
                category=category,
                weight=weight,
                score=round(category_score, 4),
                nearest_distance_meters=round(nearest_distance, 1) if nearest_distance is not None else None,
                amenity_count=len(category_amenities),
                contribution=round(weight * category_score, 4),
            )
        )

    return category_scores


def calculate_personalized_score(
    latitude: float,
    longitude: float,
    radius: int,
    profile: str,
    weights: dict[AmenityCategory, float],
    amenities: Iterable[NearbyAmenity],
) -> PersonalizedScoreResponse:
    category_scores = calculate_category_scores(amenities, weights)
    return PersonalizedScoreResponse(
        latitude=latitude,
        longitude=longitude,
        radius_meters=radius,
        profile=profile,
        weight_total=sum(weights.values()),
        score=round(sum(category.contribution for category in category_scores), 1),
        categories=category_scores,
    )


def calculate_score_for_location(
    db: Session,
    latitude: float,
    longitude: float,
    radius: int,
) -> UrbanScoreResponse:
    amenities = query_nearby_amenities(db, latitude, longitude, radius)
    return calculate_score(latitude, longitude, radius, amenities)


def calculate_personalized_score_for_location(
    db: Session,
    latitude: float,
    longitude: float,
    radius: int,
    profile: str,
    weights: dict[AmenityCategory, float],
) -> PersonalizedScoreResponse:
    amenities = query_nearby_amenities(db, latitude, longitude, radius)
    return calculate_personalized_score(latitude, longitude, radius, profile, weights, amenities)