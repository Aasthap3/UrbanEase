# UrbanEase

UrbanEase is a geospatial neighborhood discovery platform designed to help people understand how convenient a neighborhood is for everyday life.

## Phase 1 status

This repository currently contains the foundational project setup for the first development phase:

- React + Vite frontend
- FastAPI backend
- PostGIS/PostgreSQL Docker setup
- Shared environment configuration
- Simple health-check communication between frontend and backend
- UrbanEase landing page with product messaging

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
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── database/
│   ├── migrations/
│   └── seed/
├── docs/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
└── package-lock.json
```

## Quick start

### 1. Start PostgreSQL + PostGIS

```bash
docker compose up -d
```

### 2. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev -- --host
```

Then open the Vite local URL printed in the terminal, usually http://localhost:5173.

## Environment configuration

Copy the root `.env.example` file and update values as needed.

```bash
cp .env.example .env
```

## Backend health check

The API exposes a simple health endpoint at:

- http://localhost:8000/api/health

The frontend is configured to call this endpoint for basic connectivity validation.

## Frontend landing page

The landing page includes:

- navigation
- hero section
- search input
- key amenity categories
- product explanation
- score overview
- footer

## Next phase

The next milestone is the database and PostGIS layer, followed by authentication and location search.

## Data and methodology note

UrbanEase is a decision-support system that interprets convenience through measurable access to amenities, distance, density, and user preferences. It is not an authority on whether a neighborhood is universally good or bad.
