# Database plan

UrbanEase uses PostgreSQL with PostGIS for neighborhood and amenity analysis.

## Core tables

- users
- amenities
- locations
- neighborhoods
- user_preferences
- saved_locations

## Relationship overview

```text
User
├── preferences
└── saved_locations

Location
└── saved_by users

Neighborhood
└── spatial area definition

Amenity
└── independent spatial entity
```

## Spatial columns

The database uses PostGIS geometry columns for spatial queries, including:

- amenities.geometry
- locations.geometry
- neighborhoods.geometry

Each geometry column uses SRID 4326 to match standard latitude/longitude coordinates.

## Spatial indexes

GiST indexes are created for the spatial columns to support efficient radius-based queries such as:

```sql
SELECT *
FROM amenities
WHERE ST_DWithin(
  geometry::geography,
  ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography,
  :radius_m
);
```

## Migration workflow

Create a database and run the Alembic migration:

```bash
docker compose up -d postgres
cd backend
C:/Python313/python.exe -m alembic upgrade head
```

## Model notes

- `users` stores account metadata and hashed password values.
- `amenities` stores OSM or seed-source place metadata and a geometry point.
- OSM amenities are deduplicated with the `(source, osm_type, osm_id)` unique identity.
- `locations` stores user-selected or searched coordinates for neighborhood analysis.
- `user_preferences` stores future score weighting per user and category.
- `saved_locations` stores favorites and prevents duplicate entries per user and location.

## Seed data

A development seed script is provided in `database/seed/seed_dev_data.py` and is intended only for local testing. It does not represent real OpenStreetMap data.

## Environment variables

```env
POSTGRES_DB=urbanease
POSTGRES_USER=urbanease
POSTGRES_PASSWORD=urbanease
DATABASE_URL=postgresql+psycopg://urbanease:urbanease@localhost:5432/urbanease
```

## Health endpoint

- `GET /api/health/db`

This verifies both database connectivity and PostGIS availability.
