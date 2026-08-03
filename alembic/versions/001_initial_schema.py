"""001_initial_schema: Create PostGIS tables for users, damage_reports, fleet_vehicles, notifications

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-08-03 19:40:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Enable PostGIS & UUID extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    # 2. Create Users Table
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=100), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='citizen'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('idx_users_email', 'users', ['email'])

    # 3. Create Damage Reports Table
    op.create_table(
        'damage_reports',
        sa.Column('id', sa.String(length=100), primary_key=True),
        sa.Column('image_id', sa.String(length=255), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=False, server_default='Citizen'),
        sa.Column('damage_type', sa.String(length=100), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('severity', sa.String(length=50), nullable=False, server_default='Low'),
        sa.Column('priority_score', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('estimated_width_m', sa.Float(), nullable=True),
        sa.Column('estimated_length_m', sa.Float(), nullable=True),
        sa.Column('estimated_area_m2', sa.Float(), nullable=True),
        sa.Column('estimated_depth_cm', sa.Float(), nullable=True),
        sa.Column('road_occupancy', sa.Float(), nullable=True),
        sa.Column('road_health_score', sa.Float(), nullable=True),
        sa.Column('road_condition', sa.String(length=50), nullable=True),
        sa.Column('weather_condition', sa.String(length=50), nullable=True),
        sa.Column('temperature_c', sa.Float(), nullable=True),
        sa.Column('humidity_pct', sa.Integer(), nullable=True),
        sa.Column('visibility_km', sa.Float(), nullable=True),
        sa.Column('wind_speed_kmh', sa.Integer(), nullable=True),
        sa.Column('rain_probability_pct', sa.Integer(), nullable=True),
        sa.Column('weather_risk', sa.String(length=50), nullable=True),
        sa.Column('vehicle_id', sa.String(length=100), nullable=True),
        sa.Column('vehicle_type', sa.String(length=100), nullable=True),
        sa.Column('department', sa.String(length=150), nullable=True),
        sa.Column('camera_id', sa.String(length=100), nullable=True),
        sa.Column('driver_name', sa.String(length=150), nullable=True),
        sa.Column('inspection_route', sa.String(length=255), nullable=True),
        sa.Column('shift', sa.String(length=50), nullable=True),
        sa.Column('before_image_url', sa.Text(), nullable=True),
        sa.Column('after_image_url', sa.Text(), nullable=True),
        sa.Column('timeline', sa.JSON(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('road_name', sa.Text(), nullable=True),
        sa.Column('area', sa.Text(), nullable=True),
        sa.Column('city', sa.Text(), nullable=True),
        sa.Column('district', sa.Text(), nullable=True),
        sa.Column('state', sa.Text(), nullable=True),
        sa.Column('country', sa.Text(), nullable=True),
        sa.Column('postal_code', sa.Text(), nullable=True),
        sa.Column('formatted_address', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=100), nullable=False, server_default='Pending Verification'),
        sa.Column('verification_count', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('assigned_contractor', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('idx_damage_reports_status', 'damage_reports', ['status'])
    op.create_index('idx_damage_reports_priority', 'damage_reports', ['priority_score'])

    # 4. Add PostGIS Geometry Point SRID 4326
    op.execute("""
        ALTER TABLE damage_reports 
        ADD COLUMN IF NOT EXISTS geom GEOMETRY(Point, 4326) 
        GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)) STORED;
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_damage_reports_geom ON damage_reports USING GIST (geom);")

    # 5. Create Fleet Vehicles Table
    op.create_table(
        'fleet_vehicles',
        sa.Column('vehicle_id', sa.String(length=100), primary_key=True),
        sa.Column('vehicle_type', sa.String(length=100), nullable=False),
        sa.Column('department', sa.String(length=150), nullable=False),
        sa.Column('camera_id', sa.String(length=100), nullable=False),
        sa.Column('driver_name', sa.String(length=150), nullable=True),
        sa.Column('inspection_route', sa.String(length=255), nullable=True),
        sa.Column('shift', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='active'),
        sa.Column('last_latitude', sa.Float(), nullable=True),
        sa.Column('last_longitude', sa.Float(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    # 6. Create Notifications Table
    op.create_table(
        'notifications',
        sa.Column('id', sa.String(length=100), primary_key=True),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'))
    )


def downgrade() -> None:
    op.drop_table('notifications')
    op.drop_table('fleet_vehicles')
    op.drop_table('damage_reports')
    op.drop_table('users')
