from geoalchemy2 import WKTElement

from app.core.database import SessionLocal
from app.models.amenity import Amenity


def seed_dev_data() -> None:
    with SessionLocal() as session:
        existing = session.query(Amenity).first()
        if existing is not None:
            return

        sample_amenities = [
            Amenity(
                osm_id='seed-grocery-1',
                name='Fresh Mart',
                category='grocery',
                latitude=23.2599,
                longitude=77.4126,
                address='12 Market Road, Test City',
                source='development_seed',
                geometry=WKTElement('POINT(77.4126 23.2599)', srid=4326),
            ),
            Amenity(
                osm_id='seed-hospital-1',
                name='City Care Hospital',
                category='hospital',
                latitude=23.2610,
                longitude=77.4160,
                address='24 Wellness Avenue',
                source='development_seed',
                geometry=WKTElement('POINT(77.4160 23.2610)', srid=4326),
            ),
            Amenity(
                osm_id='seed-pharmacy-1',
                name='Wellness Pharmacy',
                category='pharmacy',
                latitude=23.2584,
                longitude=77.4098,
                address='9 Pharmacy Lane',
                source='development_seed',
                geometry=WKTElement('POINT(77.4098 23.2584)', srid=4326),
            ),
            Amenity(
                osm_id='seed-bank-1',
                name='Urban Bank',
                category='bank',
                latitude=23.2622,
                longitude=77.4118,
                address='18 Finance Plaza',
                source='development_seed',
                geometry=WKTElement('POINT(77.4118 23.2622)', srid=4326),
            ),
            Amenity(
                osm_id='seed-bus-1',
                name='Central Bus Stop',
                category='bus_stop',
                latitude=23.2589,
                longitude=77.4140,
                address='Bus Terminal Road',
                source='development_seed',
                geometry=WKTElement('POINT(77.4140 23.2589)', srid=4326),
            ),
            Amenity(
                osm_id='seed-restaurant-1',
                name='City Table',
                category='restaurant',
                latitude=23.2607,
                longitude=77.4192,
                address='30 Food Street',
                source='development_seed',
                geometry=WKTElement('POINT(77.4192 23.2607)', srid=4326),
            ),
        ]
        session.add_all(sample_amenities)
        session.commit()


if __name__ == '__main__':
    seed_dev_data()
    print('Development seed data inserted.')
