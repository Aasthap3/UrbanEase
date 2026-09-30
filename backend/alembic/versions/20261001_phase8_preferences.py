"""add profile and decimal weights to user preferences

Revision ID: 20261001_phase8_preferences
Revises: 20260930_phase5_osm
Create Date: 2026-10-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = '20261001_phase8_preferences'
down_revision = '20260930_phase5_osm'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user_preferences', sa.Column('profile', sa.String(length=50), nullable=True))
    op.execute("UPDATE user_preferences SET profile = 'custom' WHERE profile IS NULL")
    op.alter_column('user_preferences', 'profile', nullable=False)
    op.alter_column(
        'user_preferences',
        'weight',
        existing_type=sa.Integer(),
        type_=sa.Float(),
        postgresql_using='weight::double precision',
    )


def downgrade() -> None:
    op.alter_column(
        'user_preferences',
        'weight',
        existing_type=sa.Float(),
        type_=sa.Integer(),
        postgresql_using='round(weight)::integer',
    )
    op.drop_column('user_preferences', 'profile')