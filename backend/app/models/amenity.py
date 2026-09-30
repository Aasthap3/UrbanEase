from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import DateTime, Float, Index, String, UniqueConstraint
from sqlalchemy import event
from sqlalchemy.orm import Mapped, Mapper, mapped_column

from app.core.database import Base


class AmenityCategory(str, Enum):
    GROCERY = 'grocery'
    HOSPITAL = 'hospital'
    PHARMACY = 'pharmacy'
    BANK = 'bank'
    ATM = 'atm'
    BUS_STOP = 'bus_stop'
    METRO_STATION = 'metro_station'
    RESTAURANT = 'restaurant'
    HOTEL = 'hotel'
    PETROL_PUMP = 'petrol_pump'
    POLICE_STATION = 'police_station'
    LAUNDRY = 'laundry'
    GYM = 'gym'
    SCHOOL = 'school'
    COLLEGE = 'college'


class Amenity(Base):
    __tablename__ = 'amenities'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    osm_id: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
    osm_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[AmenityCategory] = mapped_column(String(50), nullable=False, index=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(100), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    opening_hours: Mapped[str | None] = mapped_column(String(200), nullable=True)
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    geometry: Mapped[object | None] = mapped_column(Geometry('POINT', srid=4326, spatial_index=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        Index('ix_amenities_geometry', 'geometry', postgresql_using='gist'),
        UniqueConstraint('source', 'osm_type', 'osm_id', name='uq_amenities_source_osm_element'),
    )

    def __repr__(self) -> str:
        return f'<Amenity {self.name}>'


@event.listens_for(Amenity, 'before_insert')
@event.listens_for(Amenity, 'before_update')
def synchronize_geometry(mapper: Mapper[Amenity], connection: object, target: Amenity) -> None:
    if target.latitude is None or target.longitude is None:
        target.geometry = None
        return
    target.geometry = WKTElement(
        f'POINT({target.longitude} {target.latitude})',
        srid=4326,
    )
