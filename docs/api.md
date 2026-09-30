# Authentication

Authentication uses Argon2 password hashes and short-lived JWT access tokens. Configure `JWT_SECRET_KEY`, `JWT_ALGORITHM`, and `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` in the environment.

## Endpoints

- `POST /api/auth/register` creates a user and returns public user data.
- `POST /api/auth/login` returns `{ "access_token": "...", "token_type": "bearer" }`.
- `GET /api/auth/me` returns the authenticated user and requires `Authorization: Bearer <token>`.

Invalid login attempts return the same generic error whether or not the email exists.

# Nearby amenities

`GET /api/amenities/nearby` discovers OpenStreetMap amenities through the public Overpass API, stores normalized records, and returns a PostGIS spatial query.

Parameters:

- `latitude`: -90 to 90
- `longitude`: -180 to 180
- `radius`: one of 500, 1000, 2000, or 5000 meters
- `category`: optional supported category such as `pharmacy` or `restaurant`

Example:

```bash
curl 'http://127.0.0.1:8000/api/amenities/nearby?latitude=18.5007&longitude=73.9379&radius=1000&category=pharmacy'
```

Results include normalized OSM identity, category, coordinates, optional metadata, and `distance_meters`, sorted nearest first. Repeated discoveries update the same record using `(source, osm_type, osm_id)`. No matches return a successful empty result.

# Location search

`GET /api/locations/search?q=<query>&limit=<limit>` uses the public Nominatim geocoding service to find cities, neighborhoods, addresses, and landmarks. Queries are trimmed, must contain 2-200 characters, and the limit defaults to 5 with a maximum of 10.

The response contains normalized `id`, `name`, `display_name`, numeric `latitude` and `longitude`, and selected `address` fields. Invalid upstream coordinates are ignored. No matches return `200 OK` with an empty list; upstream failures return `503 Service Unavailable`.

Example:

```bash
curl 'http://127.0.0.1:8000/api/locations/search?q=Hadapsar%2C%20Pune&limit=5'
```

## Example

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
	-H "Content-Type: application/json" \
	-d '{"email":"aastha@example.com","password":"securepassword"}'

curl http://127.0.0.1:8000/api/auth/me \
	-H "Authorization: Bearer <access-token>"
```

# API overview

The backend exposes a REST API for health, geocoding, neighborhood metrics, and future recommendation services.

## Current endpoints

- GET /api/health
- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/me
- GET /api/locations/search

## Planned endpoints

- GET /api/amenities/nearby
- POST /api/score/calculate
- POST /api/score/compare
- GET /api/categories
