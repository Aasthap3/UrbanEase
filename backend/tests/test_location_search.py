import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import geocoding_service

client = TestClient(app)


class FakeResponse:
    def __init__(self, payload: object, error: Exception | None = None) -> None:
        self.payload = payload
        self.error = error

    def raise_for_status(self) -> None:
        if self.error is not None:
            raise self.error

    def json(self) -> object:
        return self.payload


class FakeAsyncClient:
    response: FakeResponse
    calls: list[dict[str, object]] = []

    def __init__(self, **kwargs: object) -> None:
        self.settings = kwargs

    async def __aenter__(self) -> 'FakeAsyncClient':
        return self

    async def __aexit__(self, *args: object) -> None:
        return None

    async def get(self, path: str, **kwargs: object) -> FakeResponse:
        self.calls.append({'path': path, 'settings': self.settings, **kwargs})
        return self.response


@pytest.fixture(autouse=True)
def reset_fake_client() -> None:
    FakeAsyncClient.calls = []
    FakeAsyncClient.response = FakeResponse([])


def test_search_normalizes_results_and_builds_nominatim_request(monkeypatch: pytest.MonkeyPatch) -> None:
    FakeAsyncClient.response = FakeResponse(
        [
            {
                'place_id': 123,
                'name': 'Hadapsar',
                'display_name': 'Hadapsar, Pune, Maharashtra, India',
                'lat': '18.5089',
                'lon': '73.9260',
                'address': {'city': 'Pune', 'state': 'Maharashtra', 'country': 'India'},
            }
        ]
    )
    monkeypatch.setattr(geocoding_service.httpx, 'AsyncClient', FakeAsyncClient)

    response = client.get('/api/locations/search', params={'q': ' Hadapsar, Pune ', 'limit': 1})

    assert response.status_code == 200
    assert response.json() == [
        {
            'id': '123',
            'name': 'Hadapsar',
            'display_name': 'Hadapsar, Pune, Maharashtra, India',
            'latitude': 18.5089,
            'longitude': 73.926,
            'address': {'city': 'Pune', 'state': 'Maharashtra', 'country': 'India'},
        }
    ]
    request = FakeAsyncClient.calls[0]
    assert request['path'] == '/search'
    assert request['params'] == {'q': 'Hadapsar, Pune', 'format': 'json', 'addressdetails': 1, 'limit': 1}
    assert request['headers'] == {'User-Agent': 'UrbanEase/0.1'}


def test_search_uses_default_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(geocoding_service.httpx, 'AsyncClient', FakeAsyncClient)

    response = client.get('/api/locations/search?q=Pune')

    assert response.status_code == 200
    assert FakeAsyncClient.calls[0]['params']['limit'] == 5


@pytest.mark.parametrize('query', ['', ' ', 'a', 'x' * 201])
def test_search_rejects_invalid_queries(query: str) -> None:
    response = client.get('/api/locations/search', params={'q': query})

    assert response.status_code == 422


def test_search_rejects_limit_above_maximum() -> None:
    response = client.get('/api/locations/search', params={'q': 'Pune', 'limit': 11})

    assert response.status_code == 422


def test_search_skips_malformed_or_out_of_range_coordinates(monkeypatch: pytest.MonkeyPatch) -> None:
    FakeAsyncClient.response = FakeResponse(
        [
            {'display_name': 'Bad latitude', 'lat': 'not-a-number', 'lon': '73.9'},
            {'display_name': 'Bad longitude', 'lat': '18.5', 'lon': '181'},
        ]
    )
    monkeypatch.setattr(geocoding_service.httpx, 'AsyncClient', FakeAsyncClient)

    response = client.get('/api/locations/search?q=Pune')

    assert response.status_code == 200
    assert response.json() == []


def test_search_returns_empty_list_when_nominatim_has_no_results(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(geocoding_service.httpx, 'AsyncClient', FakeAsyncClient)

    response = client.get('/api/locations/search?q=Unknown%20Place')

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    'error',
    [
        httpx.TimeoutException('timeout', request=httpx.Request('GET', 'https://nominatim.openstreetmap.org')),
        httpx.RequestError('connection failed', request=httpx.Request('GET', 'https://nominatim.openstreetmap.org')),
    ],
)
def test_search_returns_503_for_upstream_request_failures(
    monkeypatch: pytest.MonkeyPatch,
    error: Exception,
) -> None:
    FakeAsyncClient.response = FakeResponse([], error)
    monkeypatch.setattr(geocoding_service.httpx, 'AsyncClient', FakeAsyncClient)

    response = client.get('/api/locations/search?q=Pune')

    assert response.status_code == 503


def test_search_returns_503_for_upstream_http_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    request = httpx.Request('GET', 'https://nominatim.openstreetmap.org/search')
    upstream_response = httpx.Response(502, request=request)
    FakeAsyncClient.response = FakeResponse(
        [],
        httpx.HTTPStatusError('upstream failure', request=request, response=upstream_response),
    )
    monkeypatch.setattr(geocoding_service.httpx, 'AsyncClient', FakeAsyncClient)

    response = client.get('/api/locations/search?q=Pune')

    assert response.status_code == 503