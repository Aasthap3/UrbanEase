from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SavedLocation(Base):
    __tablename__ = 'saved_locations'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    location_id: Mapped[UUID] = mapped_column(ForeignKey('locations.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user: Mapped['User'] = relationship(back_populates='saved_locations')
    location: Mapped['Location'] = relationship(back_populates='saved_by')

    __table_args__ = (
        UniqueConstraint('user_id', 'location_id', name='uq_saved_locations_user_location'),
    )

    def __repr__(self) -> str:
        return f'<SavedLocation user={self.user_id} location={self.location_id}>'
