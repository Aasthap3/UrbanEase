# Database plan

UrbanEase will use PostgreSQL with PostGIS for neighborhood and amenity analysis.

## Planned core tables

- users
- amenities
- locations
- user_preferences
- saved_locations
- neighborhoods

## Notes

- Use PostGIS geometry and geography where appropriate.
- Add spatial indexes to support radius and distance queries.
- Use OSM identifiers and original source metadata where available.
