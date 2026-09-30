from sqlalchemy import text

from app.core.database import SessionLocal, engine
from app.models.amenity import Amenity
from app.models.location import Location
from app.models.preference import UserPreference
from app.models.saved_location import SavedLocation
from app.models.user import User


def test_database_connects() -> None:
    with engine.connect() as connection:
        result = connection.execute(text('SELECT 1')).scalar_one()
    assert result == 1


def test_core_models_can_be_created() -> None:
    with SessionLocal() as session:
        user = User(name='Test User', email='test@example.com', password_hash='hashed-value')
        session.add(user)
        session.flush()

        location = Location(
            name='Test Location',
            address='123 Test Street',
            latitude=23.2599,
            longitude=77.4126,
        )
        session.add(location)
        session.flush()

        amenity = Amenity(
            osm_id='test-amenity-1',
            name='Sample Grocery',
            category='grocery',
            latitude=23.2599,
            longitude=77.4126,
            address='Sample Street',
            source='development_seed',
        )
        session.add(amenity)

        preference = UserPreference(user_id=user.id, category='grocery', weight=30)
        session.add(preference)

        saved = SavedLocation(user_id=user.id, location_id=location.id)
        session.add(saved)

        session.commit()

        assert user.id is not None
        assert location.id is not None
        assert amenity.id is not None
        assert preference.id is not None
        assert saved.id is not None


def test_nearby_amenity_query_returns_expected_results() -> None:
    with SessionLocal() as session:
        session.execute(text("DELETE FROM saved_locations"))
        session.execute(text("DELETE FROM user_preferences"))
        session.execute(text("DELETE FROM amenities"))
        session.execute(text("DELETE FROM locations"))
        session.execute(text("DELETE FROM users"))
        session.commit()

        user = User(name='Spatial User', email='spatial@example.com', password_hash='hash')
        session.add(user)
        session.flush()

        center = Location(
            name='Center',
            address='City Center',
            latitude=23.2599,
            longitude=77.4126,
        )
        session.add(center)
        session.flush()

        near = Amenity(
            osm_id='near-1',
            name='Nearby Grocery',
            category='grocery',
            latitude=23.2650,
            longitude=77.4170,
            address='Near Address',
            source='development_seed',
        )
        far = Amenity(
            osm_id='far-1',
            name='Far Grocery',
            category='grocery',
            latitude=23.3300,
            longitude=77.5000,
            address='Far Address',
            source='development_seed',
        )
        session.add_all([near, far])
        session.commit()

        nearby = session.execute(
            text(
                """
                SELECT id
                FROM amenities
                WHERE ST_DWithin(
                    geometry::geography,
                    ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
                    :radius_m
                )
                ORDER BY id
                """
            ),
            {'lon': center.longitude, 'lat': center.latitude, 'radius_m': 1000},
        ).fetchall()

        nearby_ids = {row[0] for row in nearby}

        assert near.id in nearby_ids
        assert far.id not in nearby_ids
