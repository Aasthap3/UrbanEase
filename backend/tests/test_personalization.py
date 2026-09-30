from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import delete

from app.api.personalized_score import personalized_score
from app.core.database import SessionLocal
from app.core.scoring import PROFILE_WEIGHTS
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.amenity import AmenityCategory
from app.models.user import User
from app.schemas.amenity import NearbyAmenity
from app.schemas.preferences import PreferenceUpdate
from app.services.urban_score_service import calculate_personalized_score, distance_decay

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_phase8_users() -> None:
    yield
    with SessionLocal() as session:
        session.execute(delete(User).where(User.email.like('phase8-%')))
        session.commit()


def create_user_token() -> str:
    with SessionLocal() as session:
        user = User(
            name='Phase 8 User',
            email=f'phase8-{uuid4()}@example.com',
            password_hash=hash_password('secure-password'),
        )
        session.add(user)
        session.commit()
        return create_access_token({'sub': str(user.id)})


def complete_weights(**overrides: float) -> list[dict[str, object]]:
    return [
        {'category': category.value, 'weight': overrides.get(category.value, 0)}
        for category in AmenityCategory
    ]


def test_profiles_cover_all_categories_and_total_100() -> None:
    assert set(PROFILE_WEIGHTS) == {'student', 'working_professional', 'family', 'custom'}
    for weights in PROFILE_WEIGHTS.values():
        assert set(weights) == set(AmenityCategory)
        assert sum(weights.values()) == 100


@pytest.mark.parametrize(
    'weights',
    [
        complete_weights(grocery=50),
        complete_weights(grocery=103),
        complete_weights(grocery=-1, hospital=101),
        [{'category': 'not-a-category', 'weight': 100}],
        complete_weights(grocery=50)[:-1],
        complete_weights(grocery=50) + [{'category': 'grocery', 'weight': 0}],
    ],
)
def test_invalid_weights_are_rejected(weights: list[dict[str, object]]) -> None:
    with pytest.raises(ValidationError):
        PreferenceUpdate(profile='custom', weights=weights)


def test_float_weight_total_uses_tolerance() -> None:
    weights = complete_weights()
    weights[0]['weight'] = 33.335
    weights[1]['weight'] = 33.335
    weights[2]['weight'] = 33.33

    preferences = PreferenceUpdate(profile='custom', weights=weights)

    assert sum(item.weight for item in preferences.weights) == pytest.approx(100)


def test_preferences_require_authentication() -> None:
    assert client.get('/api/preferences').status_code == 401
    assert client.get('/api/score/personalized?latitude=18.5&longitude=73.9&radius=1000').status_code == 401


def test_authenticated_preferences_persist_profile_and_weights() -> None:
    token = create_user_token()
    headers = {'Authorization': f'Bearer {token}'}
    student = [
        {'category': category.value, 'weight': weight}
        for category, weight in PROFILE_WEIGHTS['student'].items()
    ]

    update = client.put('/api/preferences', headers=headers, json={'profile': 'student', 'weights': student})
    retrieved = client.get('/api/preferences', headers=headers)

    assert update.status_code == 200
    assert update.json()['profile'] == 'student'
    assert update.json()['weight_total'] == 100
    assert retrieved.status_code == 200
    assert retrieved.json()['profile'] == 'student'
    assert retrieved.json()['weights'][0]['category'] == 'grocery'


def test_preferences_are_isolated_between_users() -> None:
    first_token = create_user_token()
    second_token = create_user_token()
    weights = complete_weights(college=100)

    response = client.put(
        '/api/preferences',
        headers={'Authorization': f'Bearer {first_token}'},
        json={'profile': 'custom', 'weights': weights},
    )

    second_preferences = client.get('/api/preferences', headers={'Authorization': f'Bearer {second_token}'})

    assert response.status_code == 200
    assert second_preferences.status_code == 200
    assert second_preferences.json()['profile'] == 'custom'
    assert next(item for item in second_preferences.json()['weights'] if item['category'] == 'college')['weight'] != 100


def test_personalized_score_uses_user_weights_deterministically() -> None:
    weights = {category: 0.0 for category in AmenityCategory}
    weights[AmenityCategory.GROCERY] = 50
    weights[AmenityCategory.HOSPITAL] = 30
    weights[AmenityCategory.PHARMACY] = 20
    amenities = [
        NearbyAmenity(
            id=uuid4(), osm_id=None, osm_type=None, name='Grocery', category=AmenityCategory.GROCERY,
            latitude=18.5, longitude=73.9, distance_meters=0, address=None, opening_hours=None, phone=None, website=None,
        ),
        NearbyAmenity(
            id=uuid4(), osm_id=None, osm_type=None, name='Hospital', category=AmenityCategory.HOSPITAL,
            latitude=18.5, longitude=73.9, distance_meters=1000, address=None, opening_hours=None, phone=None, website=None,
        ),
    ]

    result = calculate_personalized_score(18.5, 73.9, 1000, 'custom', weights, amenities)

    assert result.score == pytest.approx(65)
    assert result.weight_total == 100
    assert next(item for item in result.categories if item.category == AmenityCategory.PHARMACY).score == 0
    assert distance_decay(1000) == 0.5


def test_personalized_endpoint_validates_coordinates_and_radius() -> None:
    token = create_user_token()
    headers = {'Authorization': f'Bearer {token}'}

    invalid_coordinates = client.get('/api/score/personalized', headers=headers, params={'latitude': 91, 'longitude': 73.9, 'radius': 1000})
    invalid_radius = client.get('/api/score/personalized', headers=headers, params={'latitude': 18.5, 'longitude': 73.9, 'radius': 750})

    assert invalid_coordinates.status_code == 400
    assert invalid_radius.status_code == 400