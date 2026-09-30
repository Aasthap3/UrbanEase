"""initial_schema

Revision ID: 20260930_initial_schema
Revises: 
Create Date: 2026-09-30 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = '20260930_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis;')

    op.create_table(
        'users',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    op.create_table(
        'locations',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('geometry', Geometry('POINT', srid=4326), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_locations_geometry', 'locations', ['geometry'], unique=False, postgresql_using='gist')

    op.create_table(
        'neighborhoods',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('city', sa.String(length=150), nullable=True),
        sa.Column('state', sa.String(length=150), nullable=True),
        sa.Column('country', sa.String(length=150), nullable=True),
        sa.Column('geometry', Geometry('MULTIPOLYGON', srid=4326), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_neighborhoods_geometry', 'neighborhoods', ['geometry'], unique=False, postgresql_using='gist')

    op.create_table(
        'amenities',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('osm_id', sa.String(length=200), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('phone', sa.String(length=100), nullable=True),
        sa.Column('opening_hours', sa.String(length=200), nullable=True),
        sa.Column('source', sa.String(length=100), nullable=True),
        sa.Column('geometry', Geometry('POINT', srid=4326), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_amenities_category'), 'amenities', ['category'], unique=False)
    op.create_index(op.f('ix_amenities_osm_id'), 'amenities', ['osm_id'], unique=False)
    op.create_index('ix_amenities_geometry', 'amenities', ['geometry'], unique=False, postgresql_using='gist')

    op.create_table(
        'user_preferences',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('weight', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'category', name='uq_user_preferences_user_category'),
    )
    op.create_index(op.f('ix_user_preferences_user_id'), 'user_preferences', ['user_id'], unique=False)

    op.create_table(
        'saved_locations',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('location_id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'location_id', name='uq_saved_locations_user_location'),
    )
    op.create_index(op.f('ix_saved_locations_location_id'), 'saved_locations', ['location_id'], unique=False)
    op.create_index(op.f('ix_saved_locations_user_id'), 'saved_locations', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_saved_locations_user_id'), table_name='saved_locations')
    op.drop_index(op.f('ix_saved_locations_location_id'), table_name='saved_locations')
    op.drop_table('saved_locations')
    op.drop_index(op.f('ix_user_preferences_user_id'), table_name='user_preferences')
    op.drop_table('user_preferences')
    op.drop_index('ix_amenities_geometry', table_name='amenities')
    op.drop_index(op.f('ix_amenities_osm_id'), table_name='amenities')
    op.drop_index(op.f('ix_amenities_category'), table_name='amenities')
    op.drop_table('amenities')
    op.drop_index('ix_neighborhoods_geometry', table_name='neighborhoods')
    op.drop_table('neighborhoods')
    op.drop_index('ix_locations_geometry', table_name='locations')
    op.drop_table('locations')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
