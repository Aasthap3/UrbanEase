import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / '.env')
load_dotenv(PROJECT_ROOT / 'backend' / '.env')


class Settings:
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'postgresql+psycopg://urbanease:urbanease@localhost:5432/urbanease',
    )
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'urbanease')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'urbanease')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'urbanease')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', os.getenv('JWT_SECRET', 'change-this-development-secret'))
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    NOMINATIM_BASE_URL = os.getenv('NOMINATIM_BASE_URL', 'https://nominatim.openstreetmap.org')
    NOMINATIM_USER_AGENT = os.getenv('NOMINATIM_USER_AGENT', 'UrbanEase/0.1')
    NOMINATIM_TIMEOUT_SECONDS = float(os.getenv('NOMINATIM_TIMEOUT_SECONDS', '10'))
    OVERPASS_BASE_URL = os.getenv('OVERPASS_BASE_URL', 'https://overpass-api.de/api/interpreter')
    OVERPASS_TIMEOUT_SECONDS = float(os.getenv('OVERPASS_TIMEOUT_SECONDS', '30'))
    OVERPASS_USER_AGENT = os.getenv('OVERPASS_USER_AGENT', 'UrbanEase/1.0')


settings = Settings()
