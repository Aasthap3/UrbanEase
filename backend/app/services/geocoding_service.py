from collections.abc import Mapping
from typing import Any

import httpx
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.location import LocationSearchResult


class GeocodingServiceError(Exception):
    pass


async def _fetch_results(query: str, limit: int) -> list[dict[str, Any]]:
    params = {
        'q': query,
        'format': 'json',
        'addressdetails': 1,
        'limit': limit,
    }
    headers = {'User-Agent': settings.NOMINATIM_USER_AGENT}
    timeout = httpx.Timeout(settings.NOMINATIM_TIMEOUT_SECONDS)

    try:
        async with httpx.AsyncClient(base_url=settings.NOMINATIM_BASE_URL, timeout=timeout) as client:
            response = await client.get('/search', params=params, headers=headers)
            response.raise_for_status()
            payload = response.json()
    except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPStatusError) as exc:
        raise GeocodingServiceError from exc

    if not isinstance(payload, list):
        raise GeocodingServiceError
    return [item for item in payload if isinstance(item, dict)]


def _normalized_address(raw_address: object) -> dict[str, str]:
    if not isinstance(raw_address, Mapping):
        return {}

    address: dict[str, str] = {}
    city = raw_address.get('city') or raw_address.get('town') or raw_address.get('village') or raw_address.get('municipality')
    if city:
        address['city'] = str(city)
    for key in ('state', 'country', 'postcode'):
        if raw_address.get(key):
            address[key] = str(raw_address[key])
    return address


def _normalize_result(raw_result: dict[str, Any]) -> LocationSearchResult | None:
    display_name = raw_result.get('display_name')
    if not display_name:
        return None

    try:
        return LocationSearchResult(
            id=str(raw_result['place_id']) if raw_result.get('place_id') is not None else None,
            name=str(raw_result.get('name') or display_name),
            display_name=str(display_name),
            latitude=raw_result.get('lat'),
            longitude=raw_result.get('lon'),
            address=_normalized_address(raw_result.get('address')),
        )
    except (KeyError, ValidationError):
        return None


async def search_locations(query: str, limit: int = 5) -> list[LocationSearchResult]:
    raw_results = await _fetch_results(query, limit)
    return [result for raw_result in raw_results if (result := _normalize_result(raw_result)) is not None]