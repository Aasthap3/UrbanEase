from typing import Any
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.amenity import Amenity, AmenityCategory
from app.schemas.amenity import NearbyAmenity, NormalizedAmenity
from app.services.category_mapping import category_for_tags
from app.services.overpass_service import fetch_overpass_elements


def _element_coordinates(element: dict[str, Any]) -> tuple[float, float] | None:
    if element.get('type') == 'node':
        latitude, longitude = element.get('lat'), element.get('lon')
    else:
        center = element.get('center') or {}
        latitude, longitude = center.get('lat'), center.get('lon')
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        return None
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        return None
    return latitude, longitude


def _address_from_tags(tags: dict[str, Any]) -> str | None:
    parts = [tags.get('addr:housenumber'), tags.get('addr:street'), tags.get('addr:city') or tags.get('addr:town')]
    address = ', '.join(str(part) for part in parts if part)
    return address or None


def normalize_element(
    element: dict[str, Any],
    requested_category: AmenityCategory | None = None,
) -> NormalizedAmenity | None:
    element_type = element.get('type')
    element_id = element.get('id')
    tags = element.get('tags') or {}
    if element_type not in {'node', 'way', 'relation'} or element_id is None or not isinstance(tags, dict):
        return None
    coordinates = _element_coordinates(element)
    category = category_for_tags(tags, requested_category)
    if coordinates is None or category is None:
        return None
    return NormalizedAmenity(
        osm_id=str(element_id),
        osm_type=element_type,
        category=category,
        name=tags.get('name'),
        latitude=coordinates[0],
        longitude=coordinates[1],
        address=_address_from_tags(tags),
        opening_hours=tags.get('opening_hours'),
        phone=tags.get('phone') or tags.get('contact:phone'),
        website=tags.get('website') or tags.get('contact:website'),
    )


def normalize_elements(
    elements: list[dict[str, Any]],
    requested_category: AmenityCategory | None = None,
) -> list[NormalizedAmenity]:
    normalized: dict[tuple[str, str, str], NormalizedAmenity] = {}
    for element in elements:
        amenity = normalize_element(element, requested_category)
        if amenity is not None:
            normalized[(amenity.source, amenity.osm_type, amenity.osm_id)] = amenity
    return list(normalized.values())


def upsert_amenities(db: Session, amenities: list[NormalizedAmenity]) -> None:
    for normalized in amenities:
        existing = db.query(Amenity).filter_by(
            source=normalized.source,
            osm_type=normalized.osm_type,
            osm_id=normalized.osm_id,
        ).one_or_none()
        values = normalized.model_dump()
        if existing is None:
            db.add(Amenity(**values))
        else:
            for key, value in values.items():
                setattr(existing, key, value)
    db.commit()


def query_nearby_amenities(
    db: Session,
    latitude: float,
    longitude: float,
    radius: int,
    category: AmenityCategory | None = None,
) -> list[NearbyAmenity]:
    query = text(
        """
        SELECT id, osm_id, osm_type, name, category, latitude, longitude,
               address, opening_hours, phone, website,
               ST_Distance(
                   geometry::geography,
                   ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography
               ) AS distance_meters
        FROM amenities
        WHERE geometry IS NOT NULL
          AND ST_DWithin(
              geometry::geography,
              ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography,
              :radius
          )
          AND (CAST(:category AS TEXT) IS NULL OR category = CAST(:category AS TEXT))
        ORDER BY distance_meters ASC
        """
    )
    rows = db.execute(
        query,
        {
            'latitude': latitude,
            'longitude': longitude,
            'radius': radius,
            'category': category.value if category else None,
        },
    ).mappings().all()
    return [NearbyAmenity(**row) for row in rows]


async def discover_and_query_nearby(
    db: Session,
    latitude: float,
    longitude: float,
    radius: int,
    category: AmenityCategory | None = None,
) -> list[NearbyAmenity]:
    elements = await fetch_overpass_elements(latitude, longitude, radius, category)
    upsert_amenities(db, normalize_elements(elements, category))
    return query_nearby_amenities(db, latitude, longitude, radius, category)