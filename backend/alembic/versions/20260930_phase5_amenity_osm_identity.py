"""add OSM identity fields to amenities

Revision ID: 20260930_phase5_osm
Revises: 20260930_initial_schema
Create Date: 2026-09-30 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = '20260930_phase5_osm'
down_revision = '20260930_initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('amenities', sa.Column('osm_type', sa.String(length=20), nullable=True))
    op.add_column('amenities', sa.Column('website', sa.String(length=500), nullable=True))
    op.create_unique_constraint(
        'uq_amenities_source_osm_element',
        'amenities',
        ['source', 'osm_type', 'osm_id'],
    )


def downgrade() -> None:
    op.drop_constraint('uq_amenities_source_osm_element', 'amenities', type_='unique')
    op.drop_column('amenities', 'website')
    op.drop_column('amenities', 'osm_type')