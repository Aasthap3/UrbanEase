# Architecture

UrbanEase is structured as a separation between frontend and backend services, with future database and geospatial modules layered behind the API.

## Current phase

- Frontend: React + Vite + TypeScript + Tailwind
- Backend: FastAPI + Pydantic
- Data layer: PostgreSQL + PostGIS planned for the next phase
- Data flow: frontend requests are routed through the API layer and can then access geocoding, amenities, and scoring services

## Planned structure

- frontend/src/components
- frontend/src/pages
- frontend/src/services
- backend/app/api
- backend/app/models
- backend/app/services
- backend/app/geospatial
- backend/app/ml
- database/migrations
