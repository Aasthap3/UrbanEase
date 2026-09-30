from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import DateTime, Float, Index, String
from sqlalchemy import event
from sqlalchemy.orm import Mapped, Mapper, mapped_column, relationship

from app.core.database import Base


class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    geometry: Mapped[object | None] = mapped_column(Geometry('POINT', srid=4326, spatial_index=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    saved_by: Mapped[list['SavedLocation']] = relationship(back_populates='location', cascade='all, delete-orphan')

    __table_args__ = (
        Index('ix_locations_geometry', 'geometry', postgresql_using='gist'),
    )

    def __repr__(self) -> str:
        return f'<Location {self.name}>'


@event.listens_for(Location, 'before_insert')
@event.listens_for(Location, 'before_update')
def synchronize_geometry(mapper: Mapper[Location], connection: object, target: Location) -> None:
    if target.latitude is None or target.longitude is None:
        target.geometry = None
        return
    target.geometry = WKTElement(
        f'POINT({target.longitude} {target.latitude})',
        srid=4326,
    )
