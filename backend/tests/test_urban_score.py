from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.scoring import CATEGORY_WEIGHTS, SUPPORTED_RADII
from app.main import app
from app.models.amenity import AmenityCategory
from app.schemas.amenity import NearbyAmenity
from app.services.urban_score_service import calculate_score, distance_decay

client = TestClient(app)


def nearby_amenity(category: AmenityCategory, distance_meters: float) -> NearbyAmenity:
    return NearbyAmenity(
        id=uuid4(),
        osm_id=None,
        osm_type=None,
        name=f'{category.value} test',
        category=category,
        latitude=18.5,
        longitude=73.9,
        distance_meters=distance_meters,
        address=None,
        opening_hours=None,
        phone=None,
        website=None,
    )


@pytest.mark.parametrize(
    ('distance', 'expected'),
    [(0, 1.0), (500, 2 / 3), (1000, 0.5), (2000, 1 / 3), (5000, 1 / 6)],
)
def test_distance_decay(distance: float, expected: float) -> None:
    assert distance_decay(distance) == pytest.approx(expected)


def test_category_uses_maximum_contribution_and_nearest_distance() -> None:
    result = calculate_score(
        18.5,
        73.9,
        1000,
        [
            nearby_amenity(AmenityCategory.GROCERY, 200),
            nearby_amenity(AmenityCategory.GROCERY, 900),
        ],
    )

    grocery = next(category for category in result.categories if category.category == AmenityCategory.GROCERY)
    assert grocery.score == pytest.approx(distance_decay(200), abs=0.0001)
    assert grocery.nearest_distance_meters == 200
    assert grocery.amenity_count == 2


def test_weights_cover_all_categories_and_total_100() -> None:
    assert set(CATEGORY_WEIGHTS) == set(AmenityCategory)
    assert sum(CATEGORY_WEIGHTS.values()) == 100


def test_missing_categories_contribute_zero() -> None:
    result = calculate_score(18.5, 73.9, 500, [nearby_amenity(AmenityCategory.PHARMACY, 500)])

    hospital = next(category for category in result.categories if category.category == AmenityCategory.HOSPITAL)
    pharmacy = next(category for category in result.categories if category.category == AmenityCategory.PHARMACY)
    assert hospital.score == 0
    assert hospital.contribution == 0
    assert hospital.nearest_distance_meters is None
    assert pharmacy.score == pytest.approx(2 / 3, abs=0.0001)


def test_empty_dataset_returns_zero_for_every_category() -> None:
    result = calculate_score(18.5, 73.9, 1000, [])

    assert result.score == 0
    assert len(result.categories) == len(AmenityCategory)
    assert all(category.score == 0 and category.contribution == 0 for category in result.categories)


def test_overall_score_matches_weighted_category_contributions() -> None:
    result = calculate_score(
        18.5007,
        73.9379,
        1000,
        [
            nearby_amenity(AmenityCategory.GROCERY, 200),
            nearby_amenity(AmenityCategory.HOSPITAL, 1000),
        ],
    )

    expected = 12 * distance_decay(200) + 12 * distance_decay(1000)
    assert result.score == pytest.approx(round(expected, 1))
    assert result.latitude == 18.5007
    assert result.longitude == 73.9379
    assert result.radius_meters == 1000


def test_score_endpoint_returns_typed_response(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.api import score as score_api

    expected = calculate_score(18.5, 73.9, 1000, [nearby_amenity(AmenityCategory.PHARMACY, 300)])
    monkeypatch.setattr(score_api, 'calculate_score_for_location', lambda *args: expected)

    response = client.get('/api/score?latitude=18.5&longitude=73.9&radius=1000')

    assert response.status_code == 200
    payload = response.json()
    assert payload['score'] == expected.score
    assert len(payload['categories']) == len(AmenityCategory)
    assert payload['categories'][2]['category'] == 'pharmacy'
    assert payload['categories'][2]['nearest_distance_meters'] == 300


@pytest.mark.parametrize(
    'params',
    [
        {'latitude': 91, 'longitude': 73.9, 'radius': 1000},
        {'latitude': 18.5, 'longitude': 73.9, 'radius': 750},
    ],
)
def test_score_endpoint_validates_coordinates_and_radius(params: dict[str, object]) -> None:
    response = client.get('/api/score', params=params)

    assert response.status_code == 400
    assert 750 not in SUPPORTED_RADII