from typing import Any

import httpx

from app.core.config import settings
from app.models.amenity import AmenityCategory
from app.services.category_mapping import overpass_selectors


class OverpassServiceError(Exception):
    pass


def build_overpass_query(
    latitude: float,
    longitude: float,
    radius: int,
    category: AmenityCategory | None = None,
) -> str:
    clauses = []
    for selector in overpass_selectors(category):
        filters = ''.join(f'[{key}="{value}"]' for key, value in selector.items())
        clauses.append(f'  nwr{filters}(around:{radius},{latitude},{longitude});')
    query_timeout = int(settings.OVERPASS_TIMEOUT_SECONDS)
    return f'[out:json][timeout:{query_timeout}];\n(\n' + '\n'.join(clauses) + '\n);\nout center tags;'


async def fetch_overpass_elements(
    latitude: float,
    longitude: float,
    radius: int,
    category: AmenityCategory | None = None,
) -> list[dict[str, Any]]:
    query = build_overpass_query(latitude, longitude, radius, category)
    headers = {'User-Agent': settings.OVERPASS_USER_AGENT}
    timeout = httpx.Timeout(settings.OVERPASS_TIMEOUT_SECONDS)
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(settings.OVERPASS_BASE_URL, content=query, headers=headers)
            response.raise_for_status()
            payload = response.json()
    except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPStatusError) as exc:
        raise OverpassServiceError from exc

    if not isinstance(payload, dict) or not isinstance(payload.get('elements'), list):
        raise OverpassServiceError
    return [element for element in payload['elements'] if isinstance(element, dict)]