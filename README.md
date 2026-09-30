# UrbanEase

UrbanEase is a geospatial neighborhood discovery platform designed to help people understand how convenient a neighborhood is for everyday life.

## Phase 5 status

Nearby amenity discovery is available through OpenStreetMap data queried with the Overpass API:

- `GET /api/amenities/nearby?latitude=<lat>&longitude=<lon>&radius=<meters>`
- Supported radii are 500, 1000, 2000, and 5000 meters.
- Supported categories include grocery, hospital, pharmacy, bank, atm, bus_stop, metro_station, restaurant, hotel, petrol_pump, police_station, laundry, gym, school, and college.
- Results are normalized, upserted by `(source, osm_type, osm_id)`, and queried with PostGIS.
- No matches return `200 OK` with `count: 0` and an empty `amenities` list.

Amenity data originates from OpenStreetMap through the public Overpass API. Overpass settings are configurable through the environment.

Location search is available through the public Nominatim geocoding service:

- `GET /api/locations/search?q=<query>&limit=<limit>`
- Queries are trimmed, require 2-200 characters, and return up to 10 results.
- No results return `200 OK` with `[]`.
- Nominatim failures return `503 Service Unavailable`.

Search results are temporary normalized responses; searches are not automatically persisted as `Location` records.

The project now includes password-based authentication with Argon2 password hashing and JWT access tokens.

Authentication endpoints:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me` (Bearer token required)

Register and log in with curl:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Aastha","email":"aastha@example.com","password":"securepassword"}'

curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"aastha@example.com","password":"securepassword"}'

curl http://127.0.0.1:8000/api/auth/me \
  -H "Authorization: Bearer <access-token>"
```

Open `/docs` to authorize Swagger UI with the returned Bearer token.

## Phase 2 status

The project now includes the database and PostGIS layer required for the next feature stages:

- PostgreSQL + PostGIS Docker setup
- SQLAlchemy session and configuration layer
- Core data models for users, amenities, locations, neighborhoods, preferences, and saved locations
- Spatial geometry columns and GiST indexes
- Alembic initial migration
- Database seed script for development data
- Database health endpoint at `/api/health/db`

## Project structure

```text
UrbanEase/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── index.html
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env.example
├── database/
│   ├── init/
│   └── seed/
├── docs/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
└── package-lock.json
```

## Database architecture

```mermaid
graph LR
  Frontend --> API[FastAPI API]
  API --> DB[(PostgreSQL + PostGIS)]
  DB --> Amenities[Amenities]
  DB --> Users[Users]
  DB --> Locations[Locations]
  DB --> Neighborhoods[Neighborhoods]
```

## Quick start

### 1. Start PostgreSQL + PostGIS

```bash
docker compose up -d postgres
```

### 2. Configure environment values

Copy the example file if needed:

```bash
cp .env.example .env
```

Example settings:

```env
POSTGRES_DB=urbanease
POSTGRES_USER=urbanease
POSTGRES_PASSWORD=urbanease
DATABASE_URL=postgresql+psycopg://urbanease:urbanease@localhost:5432/urbanease
JWT_SECRET_KEY=change-this-development-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org
NOMINATIM_USER_AGENT=UrbanEase/0.1
NOMINATIM_TIMEOUT_SECONDS=10
OVERPASS_BASE_URL=https://overpass-api.de/api/interpreter
OVERPASS_TIMEOUT_SECONDS=30
OVERPASS_USER_AGENT=UrbanEase/1.0
```

### 3. Run the database migration

```bash
cd backend
C:/Python313/python.exe -m alembic upgrade head
```

Windows PowerShell example:

```powershell
cd backend
$env:PYTHONPATH=(Get-Location).Path
C:/Python313/python.exe -m alembic upgrade head
```

### 4. Start the backend

```bash
cd backend
$env:PYTHONPATH=(Get-Location).Path
C:/Python313/python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Start the frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Then open:

- Frontend: http://localhost:5173
- Health endpoint: http://localhost:8000/api/health
- Database health endpoint: http://localhost:8000/api/health/db

## Database health

The backend exposes a database health check that validates the connection and PostGIS availability:

```json
{
  "status": "ok",
  "database": "connected",
  "postgis": "available",
  "version": "..."
}
```

## Seed data

Development seed data is available in:

- [database/seed/seed_dev_data.py](database/seed/seed_dev_data.py)

Run it with:

```bash
cd backend
C:/Python313/python.exe -c "import sys; sys.path.insert(0, r'../backend'); from database.seed.seed_dev_data import seed_dev_data; seed_dev_data()"
```

Or from the project root when the path is adjusted as needed.

## Notes

UrbanEase is a decision-support system that interprets convenience through measurable access to amenities, distance, density, and user preferences. It is not an authority on whether a neighborhood is universally good or bad.
