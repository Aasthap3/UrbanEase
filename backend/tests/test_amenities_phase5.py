import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from app.core.database import SessionLocal
from app.main import app
from app.models.amenity import Amenity, AmenityCategory
from app.schemas.amenity import NormalizedAmenity
from app.services import amenity_service, overpass_service
from app.services.category_mapping import category_for_tags
from app.services.overpass_service import OverpassServiceError

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_phase5_amenities() -> None:
    yield
    with SessionLocal() as session:
        session.execute(delete(Amenity).where(Amenity.osm_id.like('phase5-%')))
        session.commit()


@pytest.mark.parametrize(
    ('tags', 'expected'),
    [
        ({'shop': 'supermarket'}, AmenityCategory.GROCERY),
        ({'amenity': 'hospital'}, AmenityCategory.HOSPITAL),
        ({'amenity': 'pharmacy'}, AmenityCategory.PHARMACY),
        ({'amenity': 'bank'}, AmenityCategory.BANK),
        ({'amenity': 'atm'}, AmenityCategory.ATM),
        ({'highway': 'bus_stop'}, AmenityCategory.BUS_STOP),
        ({'railway': 'station', 'station': 'subway'}, AmenityCategory.METRO_STATION),
        ({'amenity': 'restaurant'}, AmenityCategory.RESTAURANT),
        ({'tourism': 'hotel'}, AmenityCategory.HOTEL),
        ({'amenity': 'fuel'}, AmenityCategory.PETROL_PUMP),
        ({'amenity': 'police'}, AmenityCategory.POLICE_STATION),
        ({'shop': 'laundry'}, AmenityCategory.LAUNDRY),
        ({'leisure': 'fitness_centre'}, AmenityCategory.GYM),
        ({'amenity': 'school'}, AmenityCategory.SCHOOL),
        ({'amenity': 'college'}, AmenityCategory.COLLEGE),
    ],
)
def test_category_mapping_covers_supported_categories(tags: dict[str, str], expected: AmenityCategory) -> None:
    assert category_for_tags(tags) == expected


class FakeOverpassResponse:
    def __init__(self, payload: object, error: Exception | None = None) -> None:
        self.payload = payload
        self.error = error

    def raise_for_status(self) -> None:
        if self.error is not None:
            raise self.error

    def json(self) -> object:
        return self.payload


class FakeAsyncClient:
    response = FakeOverpassResponse({'elements': []})
    calls: list[dict[str, object]] = []

    def __init__(self, **kwargs: object) -> None:
        self.settings = kwargs

    async def __aenter__(self) -> 'FakeAsyncClient':
        return self

    async def __aexit__(self, *args: object) -> None:
        return None

    async def post(self, url: str, **kwargs: object) -> FakeOverpassResponse:
        self.calls.append({'url': url, 'settings': self.settings, **kwargs})
        return self.response


def test_overpass_client_builds_query_and_returns_elements(monkeypatch: pytest.MonkeyPatch) -> None:
    FakeAsyncClient.calls = []
    FakeAsyncClient.response = FakeOverpassResponse({'elements': [{'type': 'node', 'id': 1}]})
    monkeypatch.setattr(overpass_service.httpx, 'AsyncClient', FakeAsyncClient)

    elements = __import__('asyncio').run(
        overpass_service.fetch_overpass_elements(18.5, 73.9, 1000, AmenityCategory.PHARMACY)
    )

    assert elements == [{'type': 'node', 'id': 1}]
    request = FakeAsyncClient.calls[0]
    assert request['url'] == 'https://overpass-api.de/api/interpreter'
    assert 'nwr[amenity="pharmacy"](around:1000,18.5,73.9);' in request['content']
    assert request['headers'] == {'User-Agent': 'UrbanEase/1.0'}


@pytest.mark.parametrize(
    'error',
    [
        httpx.TimeoutException('timeout', request=httpx.Request('POST', 'https://overpass-api.de')),
        httpx.RequestError('connection failed', request=httpx.Request('POST', 'https://overpass-api.de')),
        httpx.HTTPStatusError(
            'upstream failure',
            request=httpx.Request('POST', 'https://overpass-api.de'),
            response=httpx.Response(502),
        ),
    ],
)
def test_overpass_client_wraps_request_failures(monkeypatch: pytest.MonkeyPatch, error: Exception) -> None:
    FakeAsyncClient.response = FakeOverpassResponse({}, error)
    monkeypatch.setattr(overpass_service.httpx, 'AsyncClient', FakeAsyncClient)

    with pytest.raises(OverpassServiceError):
        __import__('asyncio').run(overpass_service.fetch_overpass_elements(18.5, 73.9, 1000))


def test_overpass_client_rejects_malformed_response(monkeypatch: pytest.MonkeyPatch) -> None:
    FakeAsyncClient.response = FakeOverpassResponse({'unexpected': []})
    monkeypatch.setattr(overpass_service.httpx, 'AsyncClient', FakeAsyncClient)

    with pytest.raises(OverpassServiceError):
        __import__('asyncio').run(overpass_service.fetch_overpass_elements(18.5, 73.9, 1000))


def test_normalization_handles_node_way_relation_and_optional_data() -> None:
    elements = [
        {
            'type': 'node',
            'id': 101,
            'lat': 18.5007,
            'lon': 73.9379,
            'tags': {'amenity': 'pharmacy', 'name': 'Near Pharmacy', 'phone': '123'},
        },
        {
            'type': 'way',
            'id': 102,
            'center': {'lat': 18.505, 'lon': 73.94},
            'tags': {'amenity': 'restaurant', 'name': 'Way Restaurant'},
        },
        {
            'type': 'relation',
            'id': 103,
            'center': {'lat': 18.51, 'lon': 73.95},
            'tags': {'amenity': 'school'},
        },
    ]

    normalized = amenity_service.normalize_elements(elements)

    assert [(item.osm_type, item.osm_id) for item in normalized] == [
        ('node', '101'),
        ('way', '102'),
        ('relation', '103'),
    ]
    assert normalized[0].latitude == 18.5007
    assert normalized[0].longitude == 73.9379
    assert normalized[0].phone == '123'
    assert normalized[2].name is None


def test_upsert_updates_same_osm_identity_without_duplicates() -> None:
    first = NormalizedAmenity(
        osm_id='phase5-upsert',
        osm_type='node',
        category=AmenityCategory.PHARMACY,
        name='Original Pharmacy',
        latitude=18.5,
        longitude=73.9,
    )
    updated = first.model_copy(update={'name': 'Updated Pharmacy', 'longitude': 73.91})

    with SessionLocal() as session:
        amenity_service.upsert_amenities(session, [first])
        amenity_service.upsert_amenities(session, [updated])
        rows = session.scalars(select(Amenity).where(Amenity.osm_id == 'phase5-upsert')).all()

        assert len(rows) == 1
        assert rows[0].name == 'Updated Pharmacy'
        geometry = session.execute(
            __import__('sqlalchemy').text('SELECT ST_AsText(geometry), ST_SRID(geometry) FROM amenities WHERE id = :id'),
            {'id': rows[0].id},
        ).one()
        assert geometry[0] == 'POINT(73.91 18.5)'
        assert geometry[1] == 4326


def test_nearby_endpoint_discovers_queries_orders_and_filters(monkeypatch: pytest.MonkeyPatch) -> None:
    elements = [
        {
            'type': 'node',
            'id': 'phase5-near-pharmacy',
            'lat': 18.5009,
            'lon': 73.9380,
            'tags': {'amenity': 'pharmacy', 'name': 'Near Pharmacy'},
        },
        {
            'type': 'node',
            'id': 'phase5-far-pharmacy',
            'lat': 18.505,
            'lon': 73.94,
            'tags': {'amenity': 'pharmacy', 'name': 'Far Pharmacy'},
        },
        {
            'type': 'node',
            'id': 'phase5-near-bank',
            'lat': 18.5008,
            'lon': 73.9381,
            'tags': {'amenity': 'bank', 'name': 'Near Bank'},
        },
    ]

    async def fake_fetch(*args: object, **kwargs: object) -> list[dict[str, object]]:
        return elements

    monkeypatch.setattr(amenity_service, 'fetch_overpass_elements', fake_fetch)

    response = client.get(
        '/api/amenities/nearby',
        params={'latitude': 18.5007, 'longitude': 73.9379, 'radius': 1000, 'category': 'pharmacy'},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload['count'] == 2
    assert [item['name'] for item in payload['amenities']] == ['Near Pharmacy', 'Far Pharmacy']
    assert payload['amenities'][0]['distance_meters'] < payload['amenities'][1]['distance_meters']
    assert payload['amenities'][0]['distance_meters'] > 0


def test_nearby_endpoint_returns_successful_empty_result(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_fetch(*args: object, **kwargs: object) -> list[dict[str, object]]:
        return []

    monkeypatch.setattr(amenity_service, 'fetch_overpass_elements', fake_fetch)

    response = client.get(
        '/api/amenities/nearby',
        params={'latitude': 18.5007, 'longitude': 73.9379, 'radius': 5000},
    )

    assert response.status_code == 200
    assert response.json()['count'] == 0
    assert response.json()['amenities'] == []


@pytest.mark.parametrize(
    'params',
    [
        {'latitude': 91, 'longitude': 73.9, 'radius': 1000},
        {'latitude': 18.5, 'longitude': 73.9, 'radius': 750},
        {'latitude': 18.5, 'longitude': 73.9, 'radius': 1000, 'category': 'unknown'},
    ],
)
def test_nearby_endpoint_validates_coordinates_radius_and_category(params: dict[str, object]) -> None:
    response = client.get('/api/amenities/nearby', params=params)

    assert response.status_code == 400